<!--
Copyright (c) 2022 Vít Labuda. All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
following conditions are met:
 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following
    disclaimer.
 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
    following disclaimer in the documentation and/or other materials provided with the distribution.
 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
    products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
-->


# 7. Special Blueprints

Datalidator comes with a number of blueprints which do not parse a specific data type, but instead wrap ("decorate") 
another blueprints and (usually) provide them with additional features. Such blueprints are called 
**special blueprints** and are located in the 
[datalidator/blueprints/specialimpl](../datalidator/blueprints/specialimpl) directory:
- [BlueprintChainingBlueprint](../datalidator/blueprints/specialimpl/BlueprintChainingBlueprint.py) – The input data 
  are passed into the first blueprint of the initializer-provided `blueprint_chain` sequence, its output is passed into 
  the second blueprint in the chain and so on. The output of the last blueprint in the chain is returned.
- [DefaultValueNoneHandlingBlueprint](../datalidator/blueprints/specialimpl/DefaultValueNoneHandlingBlueprint.py) –
  If the input is `None`, the initializer-provided `default_value` is returned. Otherwise, the input is passed into
  `wrapped_blueprint`.
- [ExceptionHandlingBlueprint](../datalidator/blueprints/specialimpl/ExceptionHandlingBlueprint.py) – If the 
  initializer-provided `wrapped_blueprint` raises `DatalidatorExc` (or, to be exact, one of its subclasses) while 
  dealing with the input data, the initializer-provided `default_value` is returned.
- [JSONBlueprint](../datalidator/blueprints/specialimpl/JSONBlueprint.py) – The input JSON string is deserialized using 
  `json.loads()`, the deserialized data is passed into the initializer-provided `wrapped_blueprint` and its return 
  value is returned.
- [NoneHandlingBlueprint](../datalidator/blueprints/specialimpl/NoneHandlingBlueprint.py) – If the input is `None`, 
  `None` is returned. Otherwise, the input is passed into the initializer-provided `wrapped_blueprint`.


### Example 1: JSON Blueprint
The following example shows how the input JSON document is parsed by `JSONBlueprint`, and then passed into the 
wrapped `ListBlueprint`:
```python
from typing import List
from datalidator.blueprints.specialimpl.JSONBlueprint import JSONBlueprint
from datalidator.blueprints.impl.ListBlueprint import ListBlueprint
from datalidator.blueprints.impl.IntegerBlueprint import IntegerBlueprint

blueprint = JSONBlueprint[List[int]](
    wrapped_blueprint=ListBlueprint(item_blueprint=IntegerBlueprint())
)

blueprint.use('[1, 2, 3, -4, -5, -6]')  # == [1, 2, 3, -4, -5, -6]
blueprint.use('[1, "  2\\r\\n", 3.9, -4, "-5", -6.1]')  # == [1, 2, 3, -4, -5, -6]
blueprint.use('[]')  # == []

blueprint.use('[1, "hello", 3.9, -4, "-5", -6.1]')  # raises InputDataNotConvertibleExc (= a subclass of DatalidatorExc)
blueprint.use('[1, "  2\\r\\n", null, -4, "-5", -6.1]')  # raises InputDataTypeNotInAllowlistExc (= a subclass of DatalidatorExc)
blueprint.use('"hello"')  # raises InputDataTypeInBlocklistExc (= a subclass of DatalidatorExc)
blueprint.use('invalid JSON')  # raises InvalidInputDataExc (= a subclass of DatalidatorExc)
blueprint.use('')  # raises InvalidInputDataExc (= a subclass of DatalidatorExc)
```


### Example 2: Exception Handling Blueprint
The following example shows that if the wrapped `IntegerBlueprint` raises an exception, it is caught by the 
`ExceptionHandlingBlueprint` and the `default_value` (`-1`) is returned:
```python
from datalidator.blueprints.specialimpl.ExceptionHandlingBlueprint import ExceptionHandlingBlueprint
from datalidator.blueprints.impl.IntegerBlueprint import IntegerBlueprint

blueprint = ExceptionHandlingBlueprint[int](
    wrapped_blueprint=IntegerBlueprint(),
    default_value=-1
)

blueprint.use(100_000.1)  # == 100000
blueprint.use("  1\r\n")  # == 1
blueprint.use("0")  # == 0
blueprint.use(-1)  # == -1
blueprint.use(-100_000.9)  # == -100000

blueprint.use("hello")  # == -1
blueprint.use("")  # == -1
blueprint.use(None)  # == -1
blueprint.use([])  # == -1
```

---

* Next chapter: [8. Tags](008_Tags.md)
* Previous chapter: [6. Object Blueprint](006_Object-Blueprint.md)
