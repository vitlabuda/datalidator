#!/bin/false

# Copyright (c) 2022 Vít Labuda. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#  1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following
#     disclaimer.
#  2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
#     following disclaimer in the documentation and/or other materials provided with the distribution.
#  3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
#     products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import os
import os.path
import sys
if "DATALIDATOR_TESTS_AUTOPATH" in os.environ:
    __TESTS_DIR = os.path.dirname(os.path.realpath(__file__))
    __MODULE_DIR = os.path.realpath(os.path.join(__TESTS_DIR, "../.."))
    if __TESTS_DIR not in sys.path:
        sys.path.insert(0, __TESTS_DIR)
    if __MODULE_DIR not in sys.path:
        sys.path.insert(0, __MODULE_DIR)

import pytest
import datetime
import ipaddress
from test_012_object_blueprint import GenericTestObjectModel
from datalidator.blueprints.impl.BooleanBlueprint import BooleanBlueprint
from datalidator.blueprints.impl.BytesBlueprint import BytesBlueprint
from datalidator.blueprints.impl.DateBlueprint import DateBlueprint
from datalidator.blueprints.impl.DatetimeBlueprint import DatetimeBlueprint
from datalidator.blueprints.impl.DictionaryBlueprint import DictionaryBlueprint
from datalidator.blueprints.impl.FloatBlueprint import FloatBlueprint
from datalidator.blueprints.impl.GenericBlueprint import GenericBlueprint
from datalidator.blueprints.impl.IPAddressBlueprint import IPAddressBlueprint
from datalidator.blueprints.impl.IPNetworkBlueprint import IPNetworkBlueprint
from datalidator.blueprints.impl.IntegerBlueprint import IntegerBlueprint
from datalidator.blueprints.impl.ListBlueprint import ListBlueprint
from datalidator.blueprints.impl.ObjectBlueprint import ObjectBlueprint
from datalidator.blueprints.impl.PredefinedDictionaryBlueprint import PredefinedDictionaryBlueprint
from datalidator.blueprints.impl.StringBlueprint import StringBlueprint
from datalidator.blueprints.impl.TimeBlueprint import TimeBlueprint
from datalidator.blueprints.impl.TimeIntervalBlueprint import TimeIntervalBlueprint
from datalidator.blueprints.impl.URLBlueprint import URLBlueprint
from datalidator.blueprints.impl.UUIDBlueprint import UUIDBlueprint
from datalidator.blueprints.impl.UnixFilesystemPathBlueprint import UnixFilesystemPathBlueprint
from datalidator.blueprints.specialimpl.BlueprintChainingBlueprint import BlueprintChainingBlueprint
from datalidator.blueprints.specialimpl.DefaultValueNoneHandlingBlueprint import DefaultValueNoneHandlingBlueprint
from datalidator.blueprints.specialimpl.ExceptionHandlingBlueprint import ExceptionHandlingBlueprint
from datalidator.blueprints.specialimpl.JSONBlueprint import JSONBlueprint
from datalidator.blueprints.specialimpl.NoneHandlingBlueprint import NoneHandlingBlueprint
from datalidator.filters.impl.DatetimeAddTimezoneFilter import DatetimeAddTimezoneFilter
from datalidator.filters.impl.DatetimeChangeTimezoneFilter import DatetimeChangeTimezoneFilter
from datalidator.filters.impl.ListDeduplicateItemsFilter import ListDeduplicateItemsFilter
from datalidator.filters.impl.ListSortFilter import ListSortFilter
from datalidator.filters.impl.NumberAbsoluteValueFilter import NumberAbsoluteValueFilter
from datalidator.filters.impl.NumberMaximumClampFilter import NumberMaximumClampFilter
from datalidator.filters.impl.NumberMinimumClampFilter import NumberMinimumClampFilter
from datalidator.filters.impl.NumberRoundFilter import NumberRoundFilter
from datalidator.filters.impl.ReplacementMapFilter import ReplacementMapFilter
from datalidator.filters.impl.StringAlwaysEmptyFilter import StringAlwaysEmptyFilter
from datalidator.filters.impl.StringCapitalizeFilter import StringCapitalizeFilter
from datalidator.filters.impl.StringControlAndSeparatorCharacterFilter import StringControlAndSeparatorCharacterFilter
from datalidator.filters.impl.StringDeduplicateWhitespaceFilter import StringDeduplicateWhitespaceFilter
from datalidator.filters.impl.StringLowercaseFilter import StringLowercaseFilter
from datalidator.filters.impl.StringRegexReplaceFilter import StringRegexReplaceFilter
from datalidator.filters.impl.StringReplaceFilter import StringReplaceFilter
from datalidator.filters.impl.StringStripFilter import StringStripFilter
from datalidator.filters.impl.StringUnicodeNormalizeFilter import StringUnicodeNormalizeFilter
from datalidator.filters.impl.StringUnifyNewlinesFilter import StringUnifyNewlinesFilter
from datalidator.filters.impl.StringUnifyWhitespaceFilter import StringUnifyWhitespaceFilter
from datalidator.filters.impl.StringUppercaseFilter import StringUppercaseFilter
from datalidator.filters.impl.UnixFilesystemPathAddTrailingSlashFilter import UnixFilesystemPathAddTrailingSlashFilter
from datalidator.filters.impl.UnixFilesystemPathStripTrailingSlashesFilter import UnixFilesystemPathStripTrailingSlashesFilter
from datalidator.validators.impl.AllowlistValidator import AllowlistValidator
from datalidator.validators.impl.BlocklistValidator import BlocklistValidator
from datalidator.validators.impl.DatetimeIsAwareValidator import DatetimeIsAwareValidator
from datalidator.validators.impl.DatetimeNotAfterValidator import DatetimeNotAfterValidator
from datalidator.validators.impl.DatetimeNotBeforeValidator import DatetimeNotBeforeValidator
from datalidator.validators.impl.IPAddressIsGlobalValidator import IPAddressIsGlobalValidator
from datalidator.validators.impl.IPAddressIsIPv4Validator import IPAddressIsIPv4Validator
from datalidator.validators.impl.IPAddressIsIPv6Validator import IPAddressIsIPv6Validator
from datalidator.validators.impl.IPAddressIsInNetworkValidator import IPAddressIsInNetworkValidator
from datalidator.validators.impl.IPAddressIsLinkLocalValidator import IPAddressIsLinkLocalValidator
from datalidator.validators.impl.IPAddressIsLoopbackValidator import IPAddressIsLoopbackValidator
from datalidator.validators.impl.IPAddressIsMulticastValidator import IPAddressIsMulticastValidator
from datalidator.validators.impl.IPAddressIsPrivateValidator import IPAddressIsPrivateValidator
from datalidator.validators.impl.IntegerIsPositiveValidator import IntegerIsPositiveValidator
from datalidator.validators.impl.IntegerIsZeroOrPositiveValidator import IntegerIsZeroOrPositiveValidator
from datalidator.validators.impl.NumberMaximumValueValidator import NumberMaximumValueValidator
from datalidator.validators.impl.NumberMinimumValueValidator import NumberMinimumValueValidator
from datalidator.validators.impl.SequenceContainsItemValidator import SequenceContainsItemValidator
from datalidator.validators.impl.SequenceHasAllItemsUniqueValidator import SequenceHasAllItemsUniqueValidator
from datalidator.validators.impl.SequenceIsNotEmptyValidator import SequenceIsNotEmptyValidator
from datalidator.validators.impl.SequenceMaximumLengthValidator import SequenceMaximumLengthValidator
from datalidator.validators.impl.SequenceMinimumLengthValidator import SequenceMinimumLengthValidator
from datalidator.validators.impl.StringContainsNoControlOrSeparatorCharactersValidator import StringContainsNoControlOrSeparatorCharactersValidator
from datalidator.validators.impl.StringContainsSubstringValidator import StringContainsSubstringValidator
from datalidator.validators.impl.StringIsOnlySingleCharacterValidator import StringIsOnlySingleCharacterValidator
from datalidator.validators.impl.StringIsOnlySingleLineValidator import StringIsOnlySingleLineValidator
from datalidator.validators.impl.StringIsOnlySingleWordValidator import StringIsOnlySingleWordValidator
from datalidator.validators.impl.StringMatchesRegexValidator import StringMatchesRegexValidator
from datalidator.validators.impl.UnixFilesystemPathContainsOnlyFilenameValidator import UnixFilesystemPathContainsOnlyFilenameValidator
from datalidator.validators.impl.UnixFilesystemPathIsAbsoluteValidator import UnixFilesystemPathIsAbsoluteValidator
from datalidator.validators.impl.UnixFilesystemPathIsRelativeValidator import UnixFilesystemPathIsRelativeValidator


__CUSTOM_TAGS = (
    "",
    "abc",
    "123",
    "řeřicha",
    "Příliš žluťoučký kůň úpěl ďábelské ódy.",
    "🤍🤍🤍",
    "\r\n",
    "   ",
    "\x00",
    bytes(range(0, 256)).decode("iso-8859-1"),
)

__CUSTOM_TAG_TEST_SUITE = (
    lambda tag: BooleanBlueprint(tag=tag),
    lambda tag: BytesBlueprint(tag=tag),
    lambda tag: DateBlueprint(datetime_blueprint=DatetimeBlueprint(), tag=tag),
    lambda tag: DatetimeBlueprint(tag=tag),
    lambda tag: DictionaryBlueprint(key_blueprint=StringBlueprint(), value_blueprint=IntegerBlueprint(), tag=tag),
    lambda tag: FloatBlueprint(tag=tag),
    lambda tag: GenericBlueprint(tag=tag),
    lambda tag: IPAddressBlueprint(tag=tag),
    lambda tag: IPNetworkBlueprint(tag=tag),
    lambda tag: IntegerBlueprint(tag=tag),
    lambda tag: ListBlueprint(item_blueprint=IntegerBlueprint(), tag=tag),  
    lambda tag: ObjectBlueprint(object_model=GenericTestObjectModel, tag=tag),
    lambda tag: PredefinedDictionaryBlueprint(dict_specification={"item": StringBlueprint()}, tag=tag),
    lambda tag: StringBlueprint(tag=tag),
    lambda tag: TimeBlueprint(datetime_blueprint=DatetimeBlueprint(), tag=tag),
    lambda tag: TimeIntervalBlueprint(tag=tag),
    lambda tag: URLBlueprint(tag=tag),
    lambda tag: UUIDBlueprint(tag=tag),
    lambda tag: UnixFilesystemPathBlueprint(tag=tag),
    lambda tag: BlueprintChainingBlueprint(blueprint_chain=[IntegerBlueprint(), StringBlueprint()], tag=tag),
    lambda tag: DefaultValueNoneHandlingBlueprint(wrapped_blueprint=StringBlueprint(), default_value="default", tag=tag),
    lambda tag: ExceptionHandlingBlueprint(wrapped_blueprint=StringBlueprint(), default_value="default", tag=tag),
    lambda tag: JSONBlueprint(wrapped_blueprint=StringBlueprint(), tag=tag),
    lambda tag: NoneHandlingBlueprint(wrapped_blueprint=StringBlueprint(), tag=tag),
    lambda tag: DatetimeAddTimezoneFilter(added_timezone=datetime.timezone.utc, tag=tag),
    lambda tag: DatetimeChangeTimezoneFilter(new_timezone=datetime.timezone.utc, tag=tag),
    lambda tag: ListDeduplicateItemsFilter(tag=tag),
    lambda tag: ListSortFilter(tag=tag),
    lambda tag: NumberAbsoluteValueFilter(tag=tag),
    lambda tag: NumberMaximumClampFilter(maximum_value=10, tag=tag),
    lambda tag: NumberMinimumClampFilter(minimum_value=5, tag=tag),
    lambda tag: NumberRoundFilter(tag=tag),
    lambda tag: ReplacementMapFilter(replacement_map=[("abc", "def"), ("123", "xyz")], tag=tag),
    lambda tag: StringAlwaysEmptyFilter(tag=tag),
    lambda tag: StringCapitalizeFilter(tag=tag),
    lambda tag: StringControlAndSeparatorCharacterFilter(tag=tag),
    lambda tag: StringDeduplicateWhitespaceFilter(tag=tag),
    lambda tag: StringLowercaseFilter(tag=tag),
    lambda tag: StringRegexReplaceFilter(regex_pattern=r'[0-9]', replacement='', tag=tag),
    lambda tag: StringReplaceFilter(old_substring="abc", new_substring="", tag=tag),
    lambda tag: StringStripFilter(tag=tag),
    lambda tag: StringUnicodeNormalizeFilter(tag=tag),
    lambda tag: StringUnifyNewlinesFilter(tag=tag),
    lambda tag: StringUnifyWhitespaceFilter(tag=tag),
    lambda tag: StringUppercaseFilter(tag=tag),
    lambda tag: UnixFilesystemPathAddTrailingSlashFilter(tag=tag),
    lambda tag: UnixFilesystemPathStripTrailingSlashesFilter(tag=tag),
    lambda tag: AllowlistValidator(allowlist=["a", "b", "c"], tag=tag),
    lambda tag: BlocklistValidator(blocklist=["1", "2", "3"], tag=tag),
    lambda tag: DatetimeIsAwareValidator(tag=tag),
    lambda tag: DatetimeNotAfterValidator(latest_acceptable_datetime=datetime.datetime.now(tz=datetime.timezone.utc), tag=tag),
    lambda tag: DatetimeNotBeforeValidator(earliest_acceptable_datetime=datetime.datetime.now(tz=datetime.timezone.utc), tag=tag),
    lambda tag: IPAddressIsGlobalValidator(tag=tag),
    lambda tag: IPAddressIsIPv4Validator(tag=tag),
    lambda tag: IPAddressIsIPv6Validator(tag=tag),
    lambda tag: IPAddressIsInNetworkValidator(ip_network=ipaddress.ip_network("127.0.0.0/8"), tag=tag),
    lambda tag: IPAddressIsLinkLocalValidator(tag=tag),
    lambda tag: IPAddressIsLoopbackValidator(tag=tag),
    lambda tag: IPAddressIsMulticastValidator(tag=tag),
    lambda tag: IPAddressIsPrivateValidator(tag=tag),
    lambda tag: IntegerIsPositiveValidator(tag=tag),
    lambda tag: IntegerIsZeroOrPositiveValidator(tag=tag),
    lambda tag: NumberMaximumValueValidator(maximum_acceptable_number=10, tag=tag),
    lambda tag: NumberMinimumValueValidator(minimum_acceptable_number=5, tag=tag),
    lambda tag: SequenceContainsItemValidator(checked_item="hello", tag=tag),
    lambda tag: SequenceHasAllItemsUniqueValidator(tag=tag),
    lambda tag: SequenceIsNotEmptyValidator(tag=tag),
    lambda tag: SequenceMaximumLengthValidator(maximum_acceptable_length=10, tag=tag),
    lambda tag: SequenceMinimumLengthValidator(minimum_acceptable_length=5, tag=tag),
    lambda tag: StringContainsNoControlOrSeparatorCharactersValidator(tag=tag),
    lambda tag: StringContainsSubstringValidator(checked_substring="test", tag=tag),
    lambda tag: StringIsOnlySingleCharacterValidator(tag=tag),
    lambda tag: StringIsOnlySingleLineValidator(tag=tag),
    lambda tag: StringIsOnlySingleWordValidator(tag=tag),
    lambda tag: StringMatchesRegexValidator(regex_pattern=r'^[0-9]+\Z', tag=tag),
    lambda tag: UnixFilesystemPathContainsOnlyFilenameValidator(tag=tag),
    lambda tag: UnixFilesystemPathIsAbsoluteValidator(tag=tag),
    lambda tag: UnixFilesystemPathIsRelativeValidator(tag=tag),
)


__DEFAULT_TAG_TEST_SUITE = (
    BooleanBlueprint(),
    BytesBlueprint(),
    DateBlueprint(datetime_blueprint=DatetimeBlueprint()),
    DatetimeBlueprint(),
    DictionaryBlueprint(key_blueprint=StringBlueprint(), value_blueprint=IntegerBlueprint()),
    FloatBlueprint(),
    GenericBlueprint(),
    IPAddressBlueprint(),
    IPNetworkBlueprint(),
    IntegerBlueprint(),
    ListBlueprint(item_blueprint=IntegerBlueprint()),  
    ObjectBlueprint(object_model=GenericTestObjectModel),
    PredefinedDictionaryBlueprint(dict_specification={"item": StringBlueprint()}),
    StringBlueprint(),
    TimeBlueprint(datetime_blueprint=DatetimeBlueprint()),
    TimeIntervalBlueprint(),
    URLBlueprint(),
    UUIDBlueprint(),
    UnixFilesystemPathBlueprint(),
    BlueprintChainingBlueprint(blueprint_chain=[IntegerBlueprint(), StringBlueprint()]),
    DefaultValueNoneHandlingBlueprint(wrapped_blueprint=StringBlueprint(), default_value="default"),
    ExceptionHandlingBlueprint(wrapped_blueprint=StringBlueprint(), default_value="default"),
    JSONBlueprint(wrapped_blueprint=StringBlueprint()),
    NoneHandlingBlueprint(wrapped_blueprint=StringBlueprint()),
    DatetimeAddTimezoneFilter(added_timezone=datetime.timezone.utc),
    DatetimeChangeTimezoneFilter(new_timezone=datetime.timezone.utc),
    ListDeduplicateItemsFilter(),
    ListSortFilter(),
    NumberAbsoluteValueFilter(),
    NumberMaximumClampFilter(maximum_value=10),
    NumberMinimumClampFilter(minimum_value=5),
    NumberRoundFilter(),
    ReplacementMapFilter(replacement_map=[("abc", "def"), ("123", "xyz")]),
    StringAlwaysEmptyFilter(),
    StringCapitalizeFilter(),
    StringControlAndSeparatorCharacterFilter(),
    StringDeduplicateWhitespaceFilter(),
    StringLowercaseFilter(),
    StringRegexReplaceFilter(regex_pattern=r'[0-9]', replacement=''),
    StringReplaceFilter(old_substring="abc", new_substring=""),
    StringStripFilter(),
    StringUnicodeNormalizeFilter(),
    StringUnifyNewlinesFilter(),
    StringUnifyWhitespaceFilter(),
    StringUppercaseFilter(),
    UnixFilesystemPathAddTrailingSlashFilter(),
    UnixFilesystemPathStripTrailingSlashesFilter(),
    AllowlistValidator(allowlist=["a", "b", "c"]),
    BlocklistValidator(blocklist=["1", "2", "3"]),
    DatetimeIsAwareValidator(),
    DatetimeNotAfterValidator(latest_acceptable_datetime=datetime.datetime.now(tz=datetime.timezone.utc)),
    DatetimeNotBeforeValidator(earliest_acceptable_datetime=datetime.datetime.now(tz=datetime.timezone.utc)),
    IPAddressIsGlobalValidator(),
    IPAddressIsIPv4Validator(),
    IPAddressIsIPv6Validator(),
    IPAddressIsInNetworkValidator(ip_network=ipaddress.ip_network("127.0.0.0/8")),
    IPAddressIsLinkLocalValidator(),
    IPAddressIsLoopbackValidator(),
    IPAddressIsMulticastValidator(),
    IPAddressIsPrivateValidator(),
    IntegerIsPositiveValidator(),
    IntegerIsZeroOrPositiveValidator(),
    NumberMaximumValueValidator(maximum_acceptable_number=10),
    NumberMinimumValueValidator(minimum_acceptable_number=5),
    SequenceContainsItemValidator(checked_item="hello"),
    SequenceHasAllItemsUniqueValidator(),
    SequenceIsNotEmptyValidator(),
    SequenceMaximumLengthValidator(maximum_acceptable_length=10),
    SequenceMinimumLengthValidator(minimum_acceptable_length=5),
    StringContainsNoControlOrSeparatorCharactersValidator(),
    StringContainsSubstringValidator(checked_substring="test"),
    StringIsOnlySingleCharacterValidator(),
    StringIsOnlySingleLineValidator(),
    StringIsOnlySingleWordValidator(),
    StringMatchesRegexValidator(regex_pattern=r'^[0-9]+\Z'),
    UnixFilesystemPathContainsOnlyFilenameValidator(),
    UnixFilesystemPathIsAbsoluteValidator(),
    UnixFilesystemPathIsRelativeValidator(),
)


def custom_tag_test_function_parameter_generator(custom_tags, custom_tag_test_suite):
    for tag in custom_tags:
        for tagged_object_factory in custom_tag_test_suite:
            yield tagged_object_factory(tag), tag


@pytest.mark.parametrize(("tagged_object", "tag"), custom_tag_test_function_parameter_generator(__CUSTOM_TAGS, __CUSTOM_TAG_TEST_SUITE))
def test_custom_tag(tagged_object, tag):
    assert tagged_object.get_tag() == tag


@pytest.mark.parametrize("tagged_object", __DEFAULT_TAG_TEST_SUITE)
def test_default_tag(tagged_object):
    assert tagged_object.get_tag() == ""
