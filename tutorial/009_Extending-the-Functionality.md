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


# 9. Extending the Functionality

Datalidator is designed in a modular manner; therefore, it is possible to extend its functionality to suit your needs 
and use cases. You have several options of implementing your own blueprints, filters, validators, exceptions and 
errors, as described below.


## Basic characteristics of Datalidator objects
Datalidator objects (i.e. blueprints, filters and validators; most characteristics apply to exceptions and errors as well):
- must adhere to the rules of **strict defensive programming** (this is especially important for blueprints, as they may 
  deal with *untrusted* input data; see this [Wikipedia article](https://en.wikipedia.org/wiki/Defensive_programming)),
- must **not raise other exceptions than subclasses of `DatalidatorExc` or `DatalidatorError`** (routines in the 
  `Default(Blueprint/Filter/Validator)ImplBase` base classes automatically catch and handle unexpected exceptions; 
  however, "expected" exceptions should always be handled manually!),
- must be **thread-safe**,
- should be **immutable** (all built-in objects are immutable, as it is probably the easiest way to achieve 
  thread-safety; however, it is not necessary to *ensure* the immutability – it is perfectly sufficient if changing the
  internal state of an object is not a *feature*),
- should **return the exact data type** they are supposed to return (and not its subclasses, since they may not respect 
  the Liskov substitution principle),
- should **not modify the input** and **return an instance which is different from the input one** (in some rare cases, 
  this is not possible – [`GenericBlueprint`](../datalidator/blueprints/impl/GenericBlueprint.py)), 
- should be **data-source-agnostic** (blueprints should be able to parse any *valid* input data regardless of their 
  source),
- should **not be dependent upon the environment** they are used in (--> they should not access external resources, 
  such as the filesystem or network), and
- should have **extensive automated test coverage** (this is especially true for blueprints, as they may deal with
  *untrusted* input data, and they must not get into an unexpected state during that; this is the reason why the tests 
  of built-in blueprints and other objects can often seem unnecessarily "extreme").

**NOTE:** The above characteristics are just recommendations of what properties the Datalidator objects you implement 
should have if you want them to work well and be interoperable with built-in objects. You are, of course, absolutely 
free not to follow these recommendations and do everything the way you want, unless you plan to submit your 
contributions to the upstream.


## Implementing your own blueprints
There are several classes that can be subclassed when implementing a blueprint, providing different levels of already 
implemented features:
- [**BlueprintIface**](../datalidator/blueprints/BlueprintIface.py) – The *interface* (or, to be exact, abstract base 
  class) all blueprints must implement. Since it is an *interface*, it does not contain any code, only method 
  declarations, allowing you to have absolute control over your blueprints' functionality. If you decide to implement 
  this interface, you will have to implement the `use()` method – be sure to read its docstring and follow the 
  instructions!
- [**DefaultBlueprintImplBase**](../datalidator/blueprints/DefaultBlueprintImplBase.py) – The default blueprint base
  class which all built-in blueprints extend. It implements `BlueprintIface`; if you decide to extend this base class, 
  you will have to implement the `_use()` protected method instead – be sure to read its docstring and follow the 
  instructions! This base class automatically catches and handles unexpected exceptions raised while the `_use()` 
  method is being executed, and it is able to store and then hand out an initializer-provided [tag](008_Tags.md) 
  string (using the `get_tag()` method).
- [**DefaultBlueprintWithStandardFeaturesImplBase**](../datalidator/blueprints/DefaultBlueprintWithStandardFeaturesImplBase.py) –
  A blueprint base class which most of the built-in blueprints extend. In addition to the features of its superclass, 
  `DefaultBlueprintImplBase`, it contains standard functionality that most blueprints need to have – the ability to run 
  parsed data through initializer-provided sequences of filters and validators, the optional last-resort safety check 
  of output data type and instances of 
  [`InvalidInputDataExcFactory`](../datalidator/blueprints/exc/utils/InvalidInputDataExcFactory.py) (accessible through 
  `self._invalid_input_data_exc_factory`) and [`DataConversionHelper`](../datalidator/blueprints/DataConversionHelper.py) 
  (accessible through `self._data_conversion_helper`) classes to simplify the input data parsing process. If you decide
  to extend this base class, you will have to implement the `_parse()` and `_get_allowed_output_data_types()` methods – 
  be sure to read their docstrings and follow the instructions! **This is the base class you are most likely to want to 
  extend when implementing your own blueprints**, due to its balanced feature set for most use cases.
- [**DefaultBlueprintWithModeSupportImplBase**](../datalidator/blueprints/DefaultBlueprintWithModeSupportImplBase.py) –
  A blueprint base class providing the necessary infrastructure for its subclasses that need to adjust their means
  of parsing input data according to an initializer-provided `parsing_mode` (described in the 
  [second chapter](002_Using-Blueprints.md) of this tutorial). If you decide to extend this base class, you will need 
  to implement the `_parse_in_loose_mode()`, `_parse_in_rational_mode()`, `_parse_in_strict_mode()` and 
  `_get_allowed_output_data_types()` methods – be sure to read their docstrings and follow the instructions!


## Implementing your own filters
There is one interface and one base class that you can extend when implementing a filter:
- [**FilterIface**](../datalidator/filters/FilterIface.py) – The *interface* all filters must implement. Since it is an
  *interface*, it does not contain any code, only method declarations, allowing you to have absolute control over your
  filters' functionality. If you decide to implement this interface, you will have to implement the `filter()` method – 
  be sure to read its docstring and follow the instructions!
- [**DefaultFilterImplBase**](../datalidator/filters/DefaultFilterImplBase.py) – The default filter base class which all 
  built-in filters extend. It implements `FilterIface`; if you decide to extend this base class, you will need to 
  implement the `_filter()` protected method instead – be sure to read its docstring and follow the instructions! This 
  base class automatically catches and handles unexpected exceptions raised while the `_filter()` method is being 
  executed, and it is able to store and then hand out an initializer-provided [tag](008_Tags.md) string (using the 
  `get_tag()` method).


## Implementing your own validators
There is one interface and two base classes that you can extend when implementing a validator:
- [**ValidatorIface**](../datalidator/validators/ValidatorIface.py) – The *interface* all validators must implement. 
  Since it is an *interface*, it does not contain any code, only method declarations, allowing you to have absolute 
  control over your validators' functionality. If you decide to implement this interface, you will have to implement 
  the `validate()` method – be sure to read its docstring and follow the instructions!
- [**DefaultValidatorImplBase**](../datalidator/validators/DefaultValidatorImplBase.py) – The default validator base 
  class which all built-in validators extend. It implements `ValidatorIface`; if you decide to extend this base class, 
  you will have to implement the `_validate()` protected method instead – be sure to read its docstring and follow the 
  instructions! This base class automatically catches and handles unexpected exceptions raised while the `_validate()` 
  method is being executed, and it is able to store and then hand out an initializer-provided [tag](008_Tags.md) string 
  (using the `get_tag()` method). This class also provides the `_generate_data_validation_failed_exc()` method which 
  should be used by its subclasses to generate instances of `DataValidationFailedExc`.
- [**DefaultValidatorWithNegationSupportImplBase**](../datalidator/validators/DefaultValidatorWithNegationSupportImplBase.py) – 
  A validator base class providing its subclasses with a standard way of negating their validated condition, 
  as described in the [fourth chapter](004_Using-Validators.md) of this tutorial. If you decide to extend this base 
  class, you will have to implement the `_validate_positively()` and `_validate_negatively()` methods – be sure to read 
  their docstrings and follow the instructions!


## Exceptions & errors
As already mentioned in the [first chapter](001_The-Basics.md) of this tutorial, Datalidator objects should raise 
exceptions (= subclasses of `DatalidatorExc`) when they get into an "expected" bad state, such as when input data are 
unparsable, or they do not meet a validator's requirements, whereas errors (= subclasses of `DatalidatorError`) should 
be raised only in "fatal" states usually connected with being unable to initialize an instance of a Datalidator object 
(such as when an invalid value is passed to an initializer argument). Another significant difference is that exceptions 
should get caught and handled by programs using this library, whereas errors should (usually) not.

When implementing Datalidator objects, you may choose to raise either a built-in exception/error (see the 
[exception hierarchy document](Appendix-002_Exception-Hierarchy.md)), or implement your own one:
- Exceptions and errors raised by **blueprints** should be subclasses of the 
  [`BlueprintExc`](../datalidator/blueprints/exc/BlueprintExc.py) or the
  [`BlueprintError`](../datalidator/blueprints/exc/err/BlueprintError.py) base class. However, most exceptions raised 
  by blueprints are related to the invalidity of input data – in such case, 
  [`InvalidInputDataExc`](../datalidator/blueprints/exc/InvalidInputDataExc.py) or one of its subclasses should be 
  raised.
- Exceptions and errors raised by **filters** should be subclasses of the 
  [`FilterExc`](../datalidator/filters/exc/FilterExc.py) or the
  [`FilterError`](../datalidator/filters/exc/err/FilterError.py) base class.
- Exceptions and errors raised by **validators** should be subclasses of the 
  [`ValidatorExc`](../datalidator/validators/exc/ValidatorExc.py) or the 
  [`ValidatorError`](../datalidator/validators/exc/err/ValidatorError.py) base class. However, in most cases, the only 
  exception you'll need to raise from a validator is the aforementioned 
  [`DataValidationFailedExc`](../datalidator/validators/exc/DataValidationFailedExc.py), which should not be subclassed, 
  in case the parsed and filtered data do not meet the validator's requirements.


### Example 1: A blueprint, filter and validator for the `complex` data type
The following example shows how a blueprint, filter and validator could be implemented for complex numbers:
```python
from typing import final, Any, Optional, Tuple, Type
from datalidator.blueprints.ParsingMode import ParsingMode
from datalidator.blueprints.DefaultBlueprintWithModeSupportImplBase import DefaultBlueprintWithModeSupportImplBase
from datalidator.filters.DefaultFilterImplBase import DefaultFilterImplBase
from datalidator.validators.DefaultValidatorWithNegationSupportImplBase import DefaultValidatorWithNegationSupportImplBase


class ComplexBlueprint(DefaultBlueprintWithModeSupportImplBase[complex]):  
    def _get_allowed_output_data_types(self) -> Optional[Tuple[Type, ...]]:
        return complex,
  
    def _parse_in_loose_mode(self, input_data: Any) -> complex:
        return self.__convert_input_data_to_complex(input_data)
    
    def _parse_in_rational_mode(self, input_data: Any) -> complex:
        return self._data_conversion_helper.convert_input_with_data_type_allowlist(
            self.__convert_input_data_to_complex,  # Converter function
            (complex, str),  # Data type allowlist
            input_data  # Input data
        )
    
    def _parse_in_strict_mode(self, input_data: Any) -> complex:
        return self._data_conversion_helper.convert_input_with_data_type_allowlist(
            self.__convert_input_data_to_complex,  # Converter function
            (complex,),  # Data type allowlist
            input_data  # Input data
        )

    @final
    def __convert_input_data_to_complex(self, input_data: Any) -> complex:
        try:
            return complex(input_data)
        except Exception:
            raise self._invalid_input_data_exc_factory.generate_input_data_not_convertible_exc((complex,), input_data)


class ComplexRemoveRealPartFilter(DefaultFilterImplBase[complex]):
    def _filter(self, data: complex) -> complex:
        return complex(real=0.0, imag=data.imag)


class ComplexIsZeroValidator(DefaultValidatorWithNegationSupportImplBase[complex]):
    def _validate_positively(self, data: complex) -> None:  # Complex is zero? -> Valid
        if self.__is_complex_number_zero(data):
            return
        
        raise self._generate_data_validation_failed_exc("The input complex number is not zero: {}".format(repr(data)))
    
    def _validate_negatively(self, data: complex) -> None:  # Complex is not zero? -> Valid
        if self.__is_complex_number_zero(data):
            raise self._generate_data_validation_failed_exc("The input complex number is zero: {}".format(repr(data)))

    @final
    def __is_complex_number_zero(self, complex_number: complex) -> bool:
        return abs(complex_number) == 0.0


blueprint = ComplexBlueprint(
    filters=[ComplexRemoveRealPartFilter()], 
    validators=[ComplexIsZeroValidator(negate=True)], 
    parsing_mode=ParsingMode.MODE_RATIONAL
)

blueprint.use(10+5j)  # == 0+5j
blueprint.use("10+5j")  # == 0+5j
blueprint.use(0+0j)  # raises DataValidationFailedExc (= a subclass of DatalidatorExc)
blueprint.use("0+0j")  # raises DataValidationFailedExc (= a subclass of DatalidatorExc)
blueprint.use("hello")  # raises InputDataNotConvertibleExc (= a subclass of DatalidatorExc)
blueprint.use(None)  # raises InputDataTypeNotInAllowlistExc (= a subclass of DatalidatorExc)
blueprint.use([])  # raises InputDataTypeNotInAllowlistExc (= a subclass of DatalidatorExc)
```


### Example 2: Implementing a validator for an existing blueprint
It is, of course, possible to implement your own filters and validators and use them with built-in blueprints and vice
versa – **the only thing that _technically_ matters when it comes to blueprint-to-filter/validator compatibility is the 
data type**:
```python
from datalidator.blueprints.impl.StringBlueprint import StringBlueprint
from datalidator.validators.DefaultValidatorImplBase import DefaultValidatorImplBase


class StringIsNumericValidator(DefaultValidatorImplBase[str]):
    def _validate(self, data: str) -> None:  # Is string numeric? -> Valid
        if data.isnumeric():
            return

        raise self._generate_data_validation_failed_exc("The input string is not numeric: {}".format(repr(data)))


blueprint = StringBlueprint(
    validators=[StringIsNumericValidator()]
)

blueprint.use("123")  # == '123'
blueprint.use("hello")  # raises DataValidationFailedExc (= a subclass of DatalidatorExc) 
blueprint.use("")  # raises DataValidationFailedExc (= a subclass of DatalidatorExc) 
```

---

* Next chapter: [10. Real Use Case Examples](010_Real-Use-Case-Examples.md)
* Previous chapter: [8. Tags](008_Tags.md)
