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


# 3. Using Filters

As already mentioned before, the purpose of filters is to modify data already parsed by a blueprint (i.e. NOT the 
untrusted input data!) in some way without changing their data type.

This library already comes with a considerable number of filter implementations, for example:
- [DatetimeAddTimezoneFilter](../datalidator/filters/impl/DatetimeAddTimezoneFilter.py)
- [DatetimeChangeTimezoneFilter](../datalidator/filters/impl/DatetimeChangeTimezoneFilter.py)
- [ListDeduplicateItemsFilter](../datalidator/filters/impl/ListDeduplicateItemsFilter.py)
- [ListSortFilter](../datalidator/filters/impl/ListSortFilter.py)
- [NumberMaximumClampFilter](../datalidator/filters/impl/NumberMaximumClampFilter.py)
- [NumberMinimumClampFilter](../datalidator/filters/impl/NumberMinimumClampFilter.py)
- [NumberRoundFilter](../datalidator/filters/impl/NumberRoundFilter.py)
- [ReplacementMapFilter](../datalidator/filters/impl/ReplacementMapFilter.py)
- [StringLowercaseFilter](../datalidator/filters/impl/StringLowercaseFilter.py)
- [StringRegexReplaceFilter](../datalidator/filters/impl/StringRegexReplaceFilter.py)
- [StringReplaceFilter](../datalidator/filters/impl/StringReplaceFilter.py)
- [StringStripFilter](../datalidator/filters/impl/StringStripFilter.py)
- [StringUppercaseFilter](../datalidator/filters/impl/StringUppercaseFilter.py)
- [UnixFilesystemPathAddTrailingSlashFilter](../datalidator/filters/impl/UnixFilesystemPathAddTrailingSlashFilter.py)
- [UnixFilesystemPathStripTrailingSlashesFilter](../datalidator/filters/impl/UnixFilesystemPathStripTrailingSlashesFilter.py)

See the [datalidator/filters/impl](../datalidator/filters/impl) directory or the 
[class hierarchy document](Appendix-001_Class-Hierarchy.md) to see all the filter implementations that come with this 
library.

Filters should not be used directly; instead, they should be passed into a blueprint's `__init__()` method, as shown in 
the examples below. The blueprint will use the filters in the order in which they were passed into its initializer 
automatically after the untrusted input data are parsed.


### Example 1: Basic use
The following example shows how strings parsed using `StringBlueprint` have their leading and trailing whitespace 
characters stripped using `StringStripFilter`, and then are lowercased using `StringLowercaseFilter`:
```python
from datalidator.blueprints.impl.StringBlueprint import StringBlueprint
from datalidator.filters.impl.StringStripFilter import StringStripFilter
from datalidator.filters.impl.StringLowercaseFilter import StringLowercaseFilter

blueprint = StringBlueprint(filters=[
    StringStripFilter(),  # Strips leading and trailing whitespace characters (by default)
    StringLowercaseFilter()  # Lowercases the string
])

blueprint.use("hello")  # == 'hello'
blueprint.use("Hello")  # == 'hello'
blueprint.use("HELLO")  # == 'hello'
blueprint.use("   hello\r\n")  # == 'hello'
blueprint.use("   Hello\r\n")  # == 'hello'
blueprint.use("   HELLO\r\n")  # == 'hello'
```


### Example 2: Generic filters
While most filters are likely to be bound to a specific data type (such as in the above example), filters that can be
used on more or even all data types can exist as well. The following example shows the only such filter bundled with 
this library, `ReplacementMapFilter`, which can be used to replace certain output values with another:
```python
from datalidator.blueprints.impl.StringBlueprint import StringBlueprint
from datalidator.filters.impl.ReplacementMapFilter import ReplacementMapFilter

blueprint = StringBlueprint(filters=[
    ReplacementMapFilter(replacement_map=[
        ("hello", "hi"),
        ("goodbye", "bye")
    ])
])

blueprint.use("hello")  # == 'hi'
blueprint.use("Hello")  # == 'Hello'
blueprint.use("hello!")  # == 'hello!'
blueprint.use("hi")  # == 'hi'

blueprint.use("goodbye")  # == 'bye'
blueprint.use("Goodbye")  # == 'Goodbye'
blueprint.use("goodbye!")  # == 'goodbye!'
blueprint.use("bye")  # == 'bye'

blueprint.use("something else")  # == 'something else'
blueprint.use("")  # == ''
```

---

* Next chapter: [4. Using Validators](004_Using-Validators.md)
* Previous chapter: [2. Using Blueprints](002_Using-Blueprints.md)
