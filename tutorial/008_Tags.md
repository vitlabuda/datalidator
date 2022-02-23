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


# 8. Tags

When instantiating any Datalidator object (i.e. blueprint, filter or validator), you can save a string tag to its 
instance using the `tag` initializer argument (always optional, empty string by default), and later retrieve it using 
the `get_tag()` method:
```python
from datalidator.blueprints.impl.StringBlueprint import StringBlueprint
from datalidator.filters.impl.StringStripFilter import StringStripFilter
from datalidator.validators.impl.StringIsOnlySingleLineValidator import StringIsOnlySingleLineValidator


tagged_blueprint = StringBlueprint(tag="This blueprint has a tag...")
tagged_filter = StringStripFilter(tag="... and this filter too...")
tagged_validator = StringIsOnlySingleLineValidator(tag="... and this validator too.")

tagged_blueprint.get_tag()  # == 'This blueprint has a tag...'
tagged_filter.get_tag()  # == '... and this filter too...'
tagged_validator.get_tag()  # == '... and this validator too.'


untagged_blueprint = StringBlueprint()
untagged_filter = StringStripFilter()
untagged_validator = StringIsOnlySingleLineValidator()

untagged_blueprint.get_tag()  # == ''
untagged_filter.get_tag()  # == ''
untagged_validator.get_tag()  # == ''
```

**However, the main purpose of tags is to make it possible to very easily identify the originator of a raised 
subclass of `DatalidatorExc` (or `DatalidatorError`).** When a blueprint, filter or validator raises such exception,
its tag is saved into the exception instance, and it can be retrieved from it using the `get_originator_tag()` method:
```python
from datalidator.blueprints.impl.IntegerBlueprint import IntegerBlueprint
from datalidator.exc.DatalidatorExc import DatalidatorExc

blueprint = IntegerBlueprint(tag="This IntegerBlueprint is tagged!")

try:
    blueprint.use("hello")
except DatalidatorExc as e:
    print("The exception originator's tag:", e.get_originator_tag())  # == "The exception originator's tag: This IntegerBlueprint is tagged!"
```

This feature becomes especially useful when working with many nested Datalidator objects:
```python
from datalidator.blueprints.impl.ListBlueprint import ListBlueprint
from datalidator.blueprints.impl.IntegerBlueprint import IntegerBlueprint
from datalidator.blueprints.specialimpl.JSONBlueprint import JSONBlueprint
from datalidator.filters.impl.ListDeduplicateItemsFilter import ListDeduplicateItemsFilter
from datalidator.filters.impl.ListSortFilter import ListSortFilter
from datalidator.validators.impl.NumberMinimumValueValidator import NumberMinimumValueValidator
from datalidator.validators.impl.NumberMaximumValueValidator import NumberMaximumValueValidator
from datalidator.validators.impl.SequenceMinimumLengthValidator import SequenceMinimumLengthValidator
from datalidator.validators.impl.SequenceMaximumLengthValidator import SequenceMaximumLengthValidator
from datalidator.exc.DatalidatorExc import DatalidatorExc

blueprint = JSONBlueprint(
    wrapped_blueprint=ListBlueprint(
        item_blueprint=IntegerBlueprint(
            validators=[
                NumberMinimumValueValidator(10, tag="number_minimum_value_validator_tag"),
                NumberMaximumValueValidator(20, tag="number_maximum_value_validator_tag")
            ],
            tag="integer_blueprint_tag"
        ),
        filters=[
            ListDeduplicateItemsFilter(tag="list_deduplicate_items_filter_tag"),
            ListSortFilter(tag="list_sort_filter_tag")
        ],
        validators=[
            SequenceMinimumLengthValidator(3, tag="sequence_minimum_length_validator_tag"),
            SequenceMaximumLengthValidator(5, tag="sequence_maximum_length_validator_tag")
        ],
        tag="list_blueprint_tag"
    ),
    tag="json_blueprint_tag"
)

try:
    blueprint.use("invalid JSON")
except DatalidatorExc as e:
    print(e.get_originator_tag())  # == 'json_blueprint_tag'

try:
    blueprint.use("15")
except DatalidatorExc as e:
    print(e.get_originator_tag())  # == 'list_blueprint_tag'

try:
    blueprint.use('[12, "hello", 14]')
except DatalidatorExc as e:
    print(e.get_originator_tag())  # == 'integer_blueprint_tag'

try:
    blueprint.use('[12, 5, 14]')
except DatalidatorExc as e:
    print(e.get_originator_tag())  # == 'number_minimum_value_validator_tag'

try:
    blueprint.use('[12, 30, 14]')
except DatalidatorExc as e:
    print(e.get_originator_tag())  # == 'number_maximum_value_validator_tag'

try:
    blueprint.use('[12, 13]')
except DatalidatorExc as e:
    print(e.get_originator_tag())  # == 'sequence_minimum_length_validator_tag'

try:
    blueprint.use('[12, 13, 14, 15, 16, 17]')
except DatalidatorExc as e:
    print(e.get_originator_tag())  # == 'sequence_maximum_length_validator_tag'
```

---

* Next chapter: [9. Extending the Functionality](009_Extending-the-Functionality.md)
* Previous chapter: [7. Special Blueprints](007_Special-Blueprints.md)
