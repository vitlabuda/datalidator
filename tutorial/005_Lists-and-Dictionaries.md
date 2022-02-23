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


# 5. Lists and Dictionaries

Datalidator has built-in support for the following two (probably the most common) collections: **lists** and 
**dictionaries**.


## Lists
To parse lists, use [`ListBlueprint`](../datalidator/blueprints/impl/ListBlueprint.py). The blueprint takes an input 
value, converts it to a `list` object, runs its items through the blueprint passed to the mandatory `item_blueprint` 
initializer argument, and returns a resulting `list` object (which contains items returned by `item_blueprint`).

The following example shows how to parse a list of integers:
```python
from datalidator.blueprints.impl.ListBlueprint import ListBlueprint
from datalidator.blueprints.impl.IntegerBlueprint import IntegerBlueprint

blueprint = ListBlueprint(
    item_blueprint=IntegerBlueprint()
)

blueprint.use([2, 1, 3])  # == [2, 1, 3]
blueprint.use([2.9, "1", "  3\r\n"])  # == [2, 1, 3]
blueprint.use((2, 1, 3))  # == [2, 1, 3]
blueprint.use((2.9, "1", "  3\r\n"))  # == [2, 1, 3]

blueprint.use([2, None, 3])  # raises InputDataTypeNotInAllowlistExc (= a subclass of DatalidatorExc)
blueprint.use((2, None, 3))  # raises InputDataTypeNotInAllowlistExc (= a subclass of DatalidatorExc)
blueprint.use(1)  # raises InputDataNotConvertibleExc (= a subclass of DatalidatorExc)
blueprint.use(None)  # raises InputDataNotConvertibleExc (= a subclass of DatalidatorExc)
```


## Dictionaries
To parse dictionaries, use [`DictionaryBlueprint`](../datalidator/blueprints/impl/DictionaryBlueprint.py). The blueprint 
takes an input value, converts it to a `dict` object, runs its keys and values through the blueprints passed to the 
mandatory `key_blueprint` and `value_blueprint` initializer arguments, and returns a resulting `dict` object (which 
contains keys returned by `key_blueprint` and values returned by `value_blueprint`).

The following example shows how to parse a `str -> int` dictionary:
```python
from datalidator.blueprints.impl.DictionaryBlueprint import DictionaryBlueprint
from datalidator.blueprints.impl.StringBlueprint import StringBlueprint
from datalidator.blueprints.impl.IntegerBlueprint import IntegerBlueprint

blueprint = DictionaryBlueprint(
    key_blueprint=StringBlueprint(),
    value_blueprint=IntegerBlueprint()
)

blueprint.use({"hello": 1, "True": -2, "5": 3})  # == {"hello": 1, "True": -2, "5": 3}
blueprint.use({"hello": 1, "True": "  -2\r\n", "5": 3.9})  # == {"hello": 1, "True": -2, "5": 3}
blueprint.use({"hello": 1, True: -2, 5: 3})  # == {"hello": 1, "True": -2, "5": 3}
blueprint.use({"hello": 1, True: "  -2\r\n", 5: 3.9})  # == {"hello": 1, "True": -2, "5": 3}
blueprint.use([["hello", 1], ["True", -2], ["5", 3]])  # == {"hello": 1, "True": -2, "5": 3}
blueprint.use([["hello", 1], [True, "  -2\r\n"], [5, 3.9]])  # == {"hello": 1, "True": -2, "5": 3}

blueprint.use({"hello": 1, "True": None, "5": 3})  # raises InputDataTypeNotInAllowlistExc (= a subclass of DatalidatorExc)
blueprint.use({"hello": 1, tuple(): -2, "5": 3})  # raises InputDataTypeNotInAllowlistExc (= a subclass of DatalidatorExc)
blueprint.use(1)  # raises InputDataNotConvertibleExc (= a subclass of DatalidatorExc)
blueprint.use(None)  # raises InputDataNotConvertibleExc (= a subclass of DatalidatorExc)
```

NOTE: `DictionaryBlueprint` does not have the ability to check whether certain keys are present in the dictionary and
to pass values of different keys to different blueprints which is something you are very likely to want when parsing
structured data (e.g. config files, API outputs, etc.). However, there are two built-in blueprints available 
which have the aforementioned features: 
[`PredefinedDictionaryBlueprint`](../datalidator/blueprints/impl/PredefinedDictionaryBlueprint.py) and 
[`ObjectBlueprint`](../datalidator/blueprints/impl/ObjectBlueprint.py). These blueprints are described in the 
[next chapter](006_Object-Blueprint.md) of this tutorial.

---

* Next chapter: [6. Object Blueprint](006_Object-Blueprint.md)
* Previous chapter: [4. Using Validators](004_Using-Validators.md)
