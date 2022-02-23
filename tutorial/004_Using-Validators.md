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


# 4. Using Validators

As already mentioned before, the purpose of validators is to check whether data already parsed by a blueprint and 
optionally filtered by "zero or more" filters (i.e. NOT the untrusted input data!) meet certain requirements and if not, 
raise `DataValidationFailedExc`. Validators must not change the validated data in any way (that's what filters are 
there for)!

This library already comes with a considerable number of validator implementations, for example:
- [AllowlistValidator](../datalidator/validators/impl/AllowlistValidator.py)
- [BlocklistValidator](../datalidator/validators/impl/BlocklistValidator.py)
- [DatetimeNotAfterValidator](../datalidator/validators/impl/DatetimeNotAfterValidator.py)
- [DatetimeNotBeforeValidator](../datalidator/validators/impl/DatetimeNotBeforeValidator.py)
- [IPAddressIsGlobalValidator](../datalidator/validators/impl/IPAddressIsGlobalValidator.py)
- [IPAddressIsIPv4Validator](../datalidator/validators/impl/IPAddressIsIPv4Validator.py)
- [IPAddressIsIPv6Validator](../datalidator/validators/impl/IPAddressIsIPv6Validator.py)
- [IPAddressIsPrivateValidator](../datalidator/validators/impl/IPAddressIsPrivateValidator.py)
- [NumberMaximumValueValidator](../datalidator/validators/impl/NumberMaximumValueValidator.py)
- [NumberMinimumValueValidator](../datalidator/validators/impl/NumberMinimumValueValidator.py)
- [SequenceIsNotEmptyValidator](../datalidator/validators/impl/SequenceIsNotEmptyValidator.py) *(Keep in mind that strings are sequences as well.)*
- [SequenceMaximumLengthValidator](../datalidator/validators/impl/SequenceMaximumLengthValidator.py) *(Keep in mind that strings are sequences as well.)*
- [SequenceMinimumLengthValidator](../datalidator/validators/impl/SequenceMinimumLengthValidator.py) *(Keep in mind that strings are sequences as well.)*
- [StringContainsSubstringValidator](../datalidator/validators/impl/StringContainsSubstringValidator.py)
- [StringIsOnlySingleCharacterValidator](../datalidator/validators/impl/StringIsOnlySingleCharacterValidator.py)
- [StringIsOnlySingleLineValidator](../datalidator/validators/impl/StringIsOnlySingleLineValidator.py)
- [StringIsOnlySingleWordValidator](../datalidator/validators/impl/StringIsOnlySingleWordValidator.py)
- [StringMatchesRegexValidator](../datalidator/validators/impl/StringMatchesRegexValidator.py)
- [UnixFilesystemPathIsAbsoluteValidator](../datalidator/validators/impl/UnixFilesystemPathIsAbsoluteValidator.py)
- [UnixFilesystemPathIsRelativeValidator](../datalidator/validators/impl/UnixFilesystemPathIsRelativeValidator.py)

See the [datalidator/validators/impl](../datalidator/validators/impl) directory or the 
[class hierarchy document](Appendix-001_Class-Hierarchy.md) to see all the validator implementations that come with this 
library.

Validators should not be used directly; instead, they should be passed into a blueprint's `__init__()` method, as shown 
in the examples below. The blueprint will use the validators in the order in which they were passed into its initializer 
automatically after the untrusted input data are parsed and the result is passed through all the initializer-provided 
filters (if there are any).


### Example 1: Basic use
The following example shows how integers parsed using `IntegerBlueprint` are validated by consecutive 3 validators:
* `NumberMinimumValueValidator` – Checks whether the blueprint's output integers are greater than or equal to 10
* `NumberMaximumValueValidator` – Checks whether the blueprint's output integers are less than or equal to 20
* `BlocklistValidator` – Checks whether the blueprint's output integers are not 14 or 16
```python
from datalidator.blueprints.impl.IntegerBlueprint import IntegerBlueprint
from datalidator.validators.impl.NumberMinimumValueValidator import NumberMinimumValueValidator
from datalidator.validators.impl.NumberMaximumValueValidator import NumberMaximumValueValidator
from datalidator.validators.impl.BlocklistValidator import BlocklistValidator

blueprint = IntegerBlueprint(validators=[
    NumberMinimumValueValidator(10),
    NumberMaximumValueValidator(20),
    BlocklistValidator(blocklist=[14, 16])
])

blueprint.use(-1000)  # raises DataValidationFailedExc (= a subclass of DatalidatorExc)
blueprint.use(9)  # raises DataValidationFailedExc (= a subclass of DatalidatorExc)
blueprint.use(10)  # == 10
blueprint.use(11)  # == 11
blueprint.use(14)  # raises DataValidationFailedExc (= a subclass of DatalidatorExc)
blueprint.use(15)  # == 15
blueprint.use(16)  # raises DataValidationFailedExc (= a subclass of DatalidatorExc)
blueprint.use(19)  # == 19
blueprint.use(20)  # == 20
blueprint.use(21)  # raises DataValidationFailedExc (= a subclass of DatalidatorExc)
blueprint.use(1000)  # raises DataValidationFailedExc (= a subclass of DatalidatorExc)
```

Note that validators (just as filters) can, but don't have to be bound to a specific data type – they can be more or 
less universal. In this example, there are 2 validators, `NumberMinimumValueValidator` and 
`NumberMaximumValueValidator`, which can be used to validate both integers and floats, and then there is 
`BlocklistValidator` which can be used to validate (almost) any data type.


### Example 2: Validators with negation support
Validators that are subclasses of the 
[`DefaultValidatorWithNegationSupportImplBase`](../datalidator/validators/DefaultValidatorWithNegationSupportImplBase.py) 
base class are provided with a standard way of negating their validated condition. For example, the built-in 
`StringContainsSubstringValidator` considers the input string valid if it contains the initializer-provided substring 
by default. When negated (using the optional `negate` initializer argument), it considers the input string valid if it 
does NOT contain the substring:
```python
from datalidator.blueprints.impl.StringBlueprint import StringBlueprint
from datalidator.validators.impl.StringContainsSubstringValidator import StringContainsSubstringValidator


default_validation = StringBlueprint(validators=[
    # The optional 'negate' argument is 'False' by default, so omitting it would have the same effect
    StringContainsSubstringValidator("ll", negate=False)  # --> Valid if the string contains the substring
])
default_validation.use("hello")  # == 'hello'
default_validation.use("something else")  # raises DataValidationFailedExc (= a subclass of DatalidatorExc)


negated_validation = StringBlueprint(validators=[
    StringContainsSubstringValidator("ll", negate=True)  # --> Valid if the string DOES NOT contain the substring
])
negated_validation.use("hello")  # raises DataValidationFailedExc (= a subclass of DatalidatorExc)
negated_validation.use("something else")  # == 'something else'
```

Built-in validators with negation support have their behaviour in both validation modes documented in their docstrings.

---

* Next chapter: [5. Lists and Dictionaries](005_Lists-and-Dictionaries.md)
* Previous chapter: [3. Using Filters](003_Using-Filters.md)
