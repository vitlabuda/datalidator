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


# 2. Using Blueprints

As already mentioned before, the purpose of blueprints is to safely and reliably parse untrusted input data.  

This library already comes with a considerable number of blueprint implementations, which are able to parse both basic 
data types (such as strings and integers) and non-primitive data types and structures (such as URLs and lists), for 
example:
- [BooleanBlueprint](../datalidator/blueprints/impl/BooleanBlueprint.py)
- [DatetimeBlueprint](../datalidator/blueprints/impl/DatetimeBlueprint.py)
- [DictionaryBlueprint](../datalidator/blueprints/impl/DictionaryBlueprint.py)
- [FloatBlueprint](../datalidator/blueprints/impl/FloatBlueprint.py)
- [IPAddressBlueprint](../datalidator/blueprints/impl/IPAddressBlueprint.py)
- [IntegerBlueprint](../datalidator/blueprints/impl/IntegerBlueprint.py)
- [ListBlueprint](../datalidator/blueprints/impl/ListBlueprint.py)
- [StringBlueprint](../datalidator/blueprints/impl/StringBlueprint.py)
- [TimeIntervalBlueprint](../datalidator/blueprints/impl/TimeIntervalBlueprint.py)
- [URLBlueprint](../datalidator/blueprints/impl/URLBlueprint.py)
- [UnixFilesystemPathBlueprint](../datalidator/blueprints/impl/UnixFilesystemPathBlueprint.py)

See the [datalidator/blueprints/impl](../datalidator/blueprints/impl) directory or the 
[class hierarchy document](Appendix-001_Class-Hierarchy.md) to see all the blueprint implementations that come with this 
library.


### Example 1: Basic use
The following example shows the simplest way of using a blueprint (`IntegerBlueprint` in this case):
```python
from datalidator.blueprints.impl.IntegerBlueprint import IntegerBlueprint
from datalidator.exc.DatalidatorExc import DatalidatorExc

blueprint = IntegerBlueprint()

print(blueprint.use(-4))  # == -4
print(blueprint.use(5.9))  # == 5
print(blueprint.use(True))  # == 1
print(blueprint.use("789"))  # == 789
print(blueprint.use("   123_000\r\n"))  # == 123000

try:
    blueprint.use("hello")
except DatalidatorExc as e:
    # Although 'InputDataNotConvertibleExc' is raised in this case, 'DatalidatorExc' (= the superclass of all of this 
    # library's exceptions) should be caught in most cases, as the type of the raised exception depends on the 
    # unpredictable reason (as the input data are usually untrusted) why input data could not be converted to output data.
    print("{}: {}".format(e.__class__.__name__, str(e)))  # == InputDataNotConvertibleExc: The input data (of type 'str') are not convertible to 'int': 'hello'
```

**All blueprints bundled with this library have their allowed inputs and outputs documented in their docstrings!**


### Example 2: Parsing modes
Blueprints that are subclasses of the 
[`DefaultBlueprintWithModeSupportImplBase`](../datalidator/blueprints/DefaultBlueprintWithModeSupportImplBase.py) base 
class allow their users to change what input data are they able to parse and how they do it using the `parsing_mode` 
initializer argument, which takes a value of the [`ParsingMode`](../datalidator/blueprints/ParsingMode.py) enum. 
There are 3 parsing modes: loose, rational and strict. They behave differently across blueprints, but their general 
ideas are as follows:

- **Loose mode** – In loose mode, there is usually very little to no restriction on input data types by the blueprint 
  and the success of them getting parsed usually depends only on whether the underlying functions can deal with them. 
  Keep in mind that in this mode, resulting output data might seem unrelated or unexpected in relation to input data 
  (for example in `StringBlueprint`, where the input object is simply passed to the `str()` function, which might result 
  in unexpected strings being returned). In most cases, this parsing mode is not very useful in practice.

- **Rational mode _(default)_** – In rational mode, blueprints try to provide the most sensible output data in relation 
  to input data. Therefore, they usually restrict the data types accepted on input to a reasonable set. In addition, 
  some blueprints are programmed to handle some input values in a specific way or are programmed to be able to process 
  only a small set of input values (for example `BooleanBlueprint` accepts only a small set of input strings such as 
  `true`, `yes`, `false` or `no` in this mode). This behaviour is specific for this parsing mode only and is not present 
  in the other two modes. **This is the default parsing mode which is used unless you specify a different one when 
  instantiating a blueprint.** In practice, using this mode is usually the most reasonable option, as it can be used to 
  parse structured data in both typed (e.g. JSON) and non-typed (e.g. INI) formats. For example, `IntegerBlueprint` can 
  parse numeric strings to integers in this mode.

- **Strict mode** – In strict mode, the set of accepted input data types is usually very restricted and often contains 
  only the output data type (e.g. `StringBlueprint` only accepts `str` objects on input). Blueprints in this mode 
  usually also try to avoid losing any information when parsing the input data (e.g. `IntegerBlueprint` does not accept 
  `float` objects on its input as the decimal part of the number would get lost). In practice, this mode may be used to 
  parse structured data in typed formats (e.g. JSON) if the rules of rational mode were too loose for your use case.

Blueprints bundled with this library that have the ability to make use of parsing modes have their behaviour under all 
the parsing modes properly documented in their docstrings. It is recommended to check the documentation when using such 
blueprint in order to decide which parsing mode is the best one for your use case.

The following example shows how `BooleanBlueprint`'s behaviour changes when its parsing mode is changed: 
```python
from datalidator.blueprints.ParsingMode import ParsingMode
from datalidator.blueprints.impl.BooleanBlueprint import BooleanBlueprint

loose_blueprint = BooleanBlueprint(parsing_mode=ParsingMode.MODE_LOOSE)
loose_blueprint.use(False)  # == False
loose_blueprint.use(0)  # == False
loose_blueprint.use(2)  # == True
loose_blueprint.use("ON")  # == True 
loose_blueprint.use("OFF")  # == True
loose_blueprint.use("")  # == False 
loose_blueprint.use("hello")  # == True

rational_blueprint = BooleanBlueprint(parsing_mode=ParsingMode.MODE_RATIONAL)  # Since rational mode is the default one, the blueprint would behave the same if no parsing mode was specified
rational_blueprint.use(False)  # == False
rational_blueprint.use(0)  # == False
rational_blueprint.use(2)  # raises InputDataValueNotAllowedForDataTypeExc (= a subclass of DatalidatorExc)
rational_blueprint.use("ON")  # == True 
rational_blueprint.use("OFF")  # == False
rational_blueprint.use("")  # raises InputDataValueNotAllowedForDataTypeExc (= a subclass of DatalidatorExc)
rational_blueprint.use("hello")  # raises InputDataValueNotAllowedForDataTypeExc (= a subclass of DatalidatorExc)

strict_blueprint = BooleanBlueprint(parsing_mode=ParsingMode.MODE_STRICT)
strict_blueprint.use(False)  # == False
strict_blueprint.use(0)  # raises InputDataTypeNotInAllowlistExc (= a subclass of DatalidatorExc)
strict_blueprint.use(2)  # raises InputDataTypeNotInAllowlistExc (= a subclass of DatalidatorExc)
strict_blueprint.use("ON")  # raises InputDataTypeNotInAllowlistExc (= a subclass of DatalidatorExc)
strict_blueprint.use("OFF")  # raises InputDataTypeNotInAllowlistExc (= a subclass of DatalidatorExc)
strict_blueprint.use("")  # raises InputDataTypeNotInAllowlistExc (= a subclass of DatalidatorExc)
strict_blueprint.use("hello")  # raises InputDataTypeNotInAllowlistExc (= a subclass of DatalidatorExc)
```


### Example 3: Additional configuration of blueprints
Some blueprints' `__init__()` methods accept arguments that are used to customize the blueprint instance's functionality.
Such arguments can be either mandatory (e.g. `ListBlueprint` gets the blueprint for the list's items this way) or
optional (e.g. `DatetimeBlueprint` can be configured to be able to parse specifically formatted datetime strings this 
way):

```python
import datetime
from datalidator.blueprints.impl.DatetimeBlueprint import DatetimeBlueprint

blueprint = DatetimeBlueprint(additional_datetime_string_formats=["%d.%m.%Y", "%d. %m. %Y"])

blueprint.use(datetime.datetime(2021, 2, 25, 8, 30, 0))  # == datetime.datetime(2021, 2, 25, 8, 30)
blueprint.use("2021-02-25T08:30:05")  # == datetime.datetime(2021, 2, 25, 8, 30, 5) [ISO-8601-like datetime strings are always accepted] 
blueprint.use("25.02.2021")  # == datetime.datetime(2021, 2, 25, 0, 0)
blueprint.use("25. 02. 2021")  # == datetime.datetime(2021, 2, 25, 0, 0)
blueprint.use("25 02 2021")  # raises InputDataNotConvertibleExc
blueprint.use("hello")  # raises InputDataNotConvertibleExc
```

---

* Next chapter: [3. Using Filters](003_Using-Filters.md)
* Previous chapter: [1. The Basics](001_The-Basics.md)
