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


# Datalidator
**Datalidator** is a flexible, object-oriented Python library for parsing and validating untrusted input data.

One of its most prominent characteristics is that it is able to parse various kinds of input data: **configuration 
files, user inputs, web API outputs** etc.

*NOTE: Some links in this README may not work if the file is not viewed through 
[GitHub](https://github.com/vitlabuda/datalidator/blob/main/README.md).*


## Features and characteristics
- supports **Python 3.9 and above**
- no dependencies *(other than the Python standard library)* are required
- **object-oriented & polymorphic design** – there are 3 main types of *Datalidator objects*:
  - blueprints – parse untrusted input data to output data of a specific type, and then dispatch filters & validators
  - filters – modify the parsed data in some way while retaining their data type
  - validators – validate whether the parsed and filtered data meet certain conditions 
- adheres to the rules of [defensive programming](https://en.wikipedia.org/wiki/Defensive_programming)
- extensive automated test coverage
- **data-source-agnostic** – the library may be used to parse configuration files, user inputs, web API outputs, ...
- **environment-agnostic** – the library does not access any external resources (such as the filesystem or network)
- thread-safe
- many built-in & ready-to-use *Datalidator objects*:
  - for both *primitive* and *non-primitive* data types (e.g. strings, integers, lists, dictionaries, URLs, IP addresses, ...)
  - [19 blueprints](datalidator/blueprints/impl) + [5 *special blueprints*](datalidator/blueprints/specialimpl)
  - [23 filters](datalidator/filters/impl)
  - [31 validators](datalidator/validators/impl)


## How to use this library?
This library ships with a **tutorial** series:
1. [The Basics](tutorial/001_The-Basics.md)
2. [Using Blueprints](tutorial/002_Using-Blueprints.md)
3. [Using Filters](tutorial/003_Using-Filters.md)
4. [Using Validators](tutorial/004_Using-Validators.md)
5. [Lists and Dictionaries](tutorial/005_Lists-and-Dictionaries.md)
6. [Object Blueprint](tutorial/006_Object-Blueprint.md)
7. [Special Blueprints](tutorial/007_Special-Blueprints.md)
8. [Tags](tutorial/008_Tags.md)
9. [Extending the Functionality](tutorial/009_Extending-the-Functionality.md)
10. [Real Use Case Examples](tutorial/010_Real-Use-Case-Examples.md)

### Example
The following example shows how data from a simple hypothetical registration form could be parsed by this library:
```python
from datalidator.blueprints.impl.ObjectBlueprint import ObjectBlueprint
from datalidator.blueprints.impl.StringBlueprint import StringBlueprint
from datalidator.blueprints.impl.IntegerBlueprint import IntegerBlueprint
from datalidator.blueprints.impl.BooleanBlueprint import BooleanBlueprint
from datalidator.blueprints.extras.ObjectModel import ObjectModel
from datalidator.blueprints.extras.OptionalItem import OptionalItem
from datalidator.filters.impl.StringStripFilter import StringStripFilter
from datalidator.validators.impl.SequenceMinimumLengthValidator import SequenceMinimumLengthValidator
from datalidator.validators.impl.NumberMaximumValueValidator import NumberMaximumValueValidator
from datalidator.validators.impl.NumberMinimumValueValidator import NumberMinimumValueValidator
from datalidator.validators.impl.StringMatchesRegexValidator import StringMatchesRegexValidator

class RegistrationFormModel(ObjectModel):
    username = StringBlueprint(
        filters=[StringStripFilter()],
        validators=[StringMatchesRegexValidator(r'^[A-Za-z0-9_]{3,20}\Z')]
    )
    password = StringBlueprint(
        filters=[StringStripFilter()],
        validators=[SequenceMinimumLengthValidator(8)]
    )
    age = IntegerBlueprint(
        validators=[NumberMinimumValueValidator(13), NumberMaximumValueValidator(100)],
    )
    tos_accepted = OptionalItem(wrapped_blueprint=BooleanBlueprint(), default_value=False)  # "tos" = Terms of Service


blueprint = ObjectBlueprint(object_model=RegistrationFormModel)

blueprint.use({"username": "Joe_123", "password": "MyPassword", "age": "18\n", "tos_accepted": True})
# == RegistrationFormModel(username='Joe_123', password='MyPassword', age=18, tos_accepted=True)
```

**For simpler examples with explanation, see the [tutorial](tutorial).**


## Security
Despite the non-negligible efforts made to reduce the risk of bugs being present in this library (the adherence to the 
rules of defensive programming, extensive automated test coverage), it can never be guaranteed that there are no bugs 
or even security vulnerabilities present. *We all know what Murphy's law states, don't we?*

**As stated in the [license](LICENSE), this library comes with ABSOLUTELY NO WARRANTY:**
```text
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```


## Licensing
This project is licensed under the **3-clause BSD license** – see the [LICENSE](LICENSE) file.

Programmed by **[Vít Labuda](https://vitlabuda.cz/)**.
