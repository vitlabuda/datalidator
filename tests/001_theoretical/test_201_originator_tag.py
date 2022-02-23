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


import os.path
import sys
__TESTS_DIR = os.path.dirname(os.path.realpath(__file__))  
__MODULE_DIR = os.path.realpath(os.path.join(__TESTS_DIR, "../.."))  
if __TESTS_DIR not in sys.path:  
    sys.path.insert(0, __TESTS_DIR)  
if __MODULE_DIR not in sys.path:  
    sys.path.insert(0, __MODULE_DIR)  

from typing import Any, Optional, Tuple, Type
import theoretical_testutils
import pytest
import datetime
from test_011_list_blueprint import exception_raising_comparison_key_extraction_function
from datalidator.blueprints.ParsingMode import ParsingMode
from datalidator.blueprints.DefaultBlueprintImplBase import DefaultBlueprintImplBase
from datalidator.blueprints.DefaultBlueprintWithStandardFeaturesImplBase import DefaultBlueprintWithStandardFeaturesImplBase
from datalidator.blueprints.impl.StringBlueprint import StringBlueprint
from datalidator.blueprints.impl.FloatBlueprint import FloatBlueprint
from datalidator.blueprints.impl.BytesBlueprint import BytesBlueprint
from datalidator.blueprints.impl.BooleanBlueprint import BooleanBlueprint
from datalidator.blueprints.impl.DatetimeBlueprint import DatetimeBlueprint
from datalidator.blueprints.impl.ListBlueprint import ListBlueprint
from datalidator.blueprints.impl.GenericBlueprint import GenericBlueprint
from datalidator.blueprints.specialimpl.BlueprintChainingBlueprint import BlueprintChainingBlueprint
from datalidator.blueprints.exc.InputDataNotConvertibleExc import InputDataNotConvertibleExc
from datalidator.blueprints.exc.InputDataTypeInBlocklistExc import InputDataTypeInBlocklistExc
from datalidator.blueprints.exc.InputDataTypeNotInAllowlistExc import InputDataTypeNotInAllowlistExc
from datalidator.blueprints.exc.InputDataValueNotAllowedForDataTypeExc import InputDataValueNotAllowedForDataTypeExc
from datalidator.blueprints.exc.InvalidInputDataExc import InvalidInputDataExc
from datalidator.blueprints.exc.UnexpectedExceptionRaisedInBlueprintExc import UnexpectedExceptionRaisedInBlueprintExc
from datalidator.blueprints.exc.UnexpectedOutputDataTypeExc import UnexpectedOutputDataTypeExc
from datalidator.blueprints.exc.err.InvalidBlueprintConfigError import InvalidBlueprintConfigError
from datalidator.exc.err.ThisShouldNeverHappenError import ThisShouldNeverHappenError
from datalidator.filters.DefaultFilterImplBase import DefaultFilterImplBase
from datalidator.filters.impl.StringRegexReplaceFilter import StringRegexReplaceFilter
from datalidator.filters.impl.DatetimeChangeTimezoneFilter import DatetimeChangeTimezoneFilter
from datalidator.filters.impl.ListSortFilter import ListSortFilter
from datalidator.filters.exc.err.InvalidFilterConfigError import InvalidFilterConfigError
from datalidator.filters.exc.err.RegexCompilationFailedInFilterError import RegexCompilationFailedInFilterError
from datalidator.filters.exc.InputDatetimeObjectIsNaiveInFilterExc import InputDatetimeObjectIsNaiveInFilterExc
from datalidator.filters.exc.RegexFailedInFilterExc import RegexFailedInFilterExc
from datalidator.filters.exc.SortingFailedInFilterExc import SortingFailedInFilterExc
from datalidator.filters.exc.UnexpectedExceptionRaisedInFilterExc import UnexpectedExceptionRaisedInFilterExc
from datalidator.validators.DefaultValidatorImplBase import DefaultValidatorImplBase
from datalidator.validators.impl.AllowlistValidator import AllowlistValidator
from datalidator.validators.impl.StringMatchesRegexValidator import StringMatchesRegexValidator
from datalidator.validators.impl.DatetimeNotAfterValidator import DatetimeNotAfterValidator
from datalidator.validators.exc.err.InvalidValidatorConfigError import InvalidValidatorConfigError
from datalidator.validators.exc.err.RegexCompilationFailedInValidatorError import RegexCompilationFailedInValidatorError
from datalidator.validators.exc.DataValidationFailedExc import DataValidationFailedExc
from datalidator.validators.exc.InputDatetimeObjectIsNaiveInValidatorExc import InputDatetimeObjectIsNaiveInValidatorExc
from datalidator.validators.exc.UnexpectedExceptionRaisedInValidatorExc import UnexpectedExceptionRaisedInValidatorExc


class UnexpectedExceptionRaisingBlueprint(DefaultBlueprintImplBase[Any]):
    def _use(self, input_data: Any) -> Any:
        raise Exception("This is an unexpected exception from a blueprint.")


class UnexpectedExceptionRaisingFilter(DefaultFilterImplBase[Any]):
    def _filter(self, data: Any) -> Any:
        raise Exception("This is an unexpected exception from a filter.")


class UnexpectedExceptionRaisingValidator(DefaultValidatorImplBase[Any]):
    def _validate(self, data: Any) -> None:
        raise Exception("This is an unexpected exception from a validator.")


class UnexpectedOutputDataTypeReturningBlueprint(DefaultBlueprintWithStandardFeaturesImplBase[Any]):
    def _get_allowed_output_data_types(self) -> Optional[Tuple[Type, ...]]:
        return int,

    def _parse(self, input_data: Any) -> Any:
        return "hello"


__TAGS = (
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

__ORIGINATOR_TAG_TEST_SUITE = (
    (lambda tag: FloatBlueprint(tag=tag).use("hello"), InputDataNotConvertibleExc),
    (lambda tag: BytesBlueprint(parsing_mode=ParsingMode.MODE_LOOSE, tag=tag).use(4), InputDataTypeInBlocklistExc),
    (lambda tag: FloatBlueprint(tag=tag).use(theoretical_testutils.EmptyObject()), InputDataTypeNotInAllowlistExc),
    (lambda tag: BooleanBlueprint(tag=tag).use("hello"), InputDataValueNotAllowedForDataTypeExc),
    (lambda tag: FloatBlueprint(tag=tag).use(float("inf")), InvalidInputDataExc),
    (lambda tag: UnexpectedExceptionRaisingBlueprint(tag=tag).use(None), UnexpectedExceptionRaisedInBlueprintExc),
    (lambda tag: UnexpectedOutputDataTypeReturningBlueprint(tag=tag).use(None), UnexpectedOutputDataTypeExc),
    (lambda tag: BlueprintChainingBlueprint(blueprint_chain=[], tag=tag), InvalidBlueprintConfigError),
    (lambda tag: FloatBlueprint(parsing_mode=ParsingMode._MODE_INVALID, tag=tag).use(123.5), ThisShouldNeverHappenError),  # noqa
    (lambda tag: StringBlueprint(filters=(StringRegexReplaceFilter(r'[0-9]', '', max_replacement_count=-10, tag=tag),), tag="!untagged"), InvalidFilterConfigError),
    (lambda tag: StringBlueprint(filters=(StringRegexReplaceFilter(r'[', '', tag=tag),), tag="!untagged"), RegexCompilationFailedInFilterError),
    (lambda tag: DatetimeBlueprint(filters=(DatetimeChangeTimezoneFilter(new_timezone=datetime.timezone.utc, tag=tag),), tag="!untagged").use(datetime.datetime.now()), InputDatetimeObjectIsNaiveInFilterExc),
    (lambda tag: StringBlueprint(filters=(StringRegexReplaceFilter(r'[0-9]', lambda x: int(x), tag=tag),), tag="!untagged").use("123"), RegexFailedInFilterExc),  # noqa
    (lambda tag: ListBlueprint(item_blueprint=StringBlueprint(tag="!untagged"), filters=(ListSortFilter(comparison_key_extraction_function=exception_raising_comparison_key_extraction_function, tag=tag),), tag="!untagged").use(["a", "b", "c"]), SortingFailedInFilterExc),
    (lambda tag: GenericBlueprint(filters=(UnexpectedExceptionRaisingFilter(tag=tag),), tag="!untagged").use(theoretical_testutils.EmptyObject()), UnexpectedExceptionRaisedInFilterExc),
    (lambda tag: StringBlueprint(validators=(AllowlistValidator(allowlist=[], tag=tag),), tag="!untagged"), InvalidValidatorConfigError),
    (lambda tag: StringBlueprint(validators=(StringMatchesRegexValidator(r'[', tag=tag),), tag="!untagged"), RegexCompilationFailedInValidatorError),
    (lambda tag: StringBlueprint(validators=(AllowlistValidator(allowlist=["a", "b"], tag=tag),), tag="!untagged").use("1"), DataValidationFailedExc),
    (lambda tag: DatetimeBlueprint(validators=(DatetimeNotAfterValidator(latest_acceptable_datetime=datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc), tag=tag),), tag="!untagged").use(datetime.datetime(2018, 1, 1)), InputDatetimeObjectIsNaiveInValidatorExc),
    (lambda tag: GenericBlueprint(validators=(UnexpectedExceptionRaisingValidator(tag=tag),), tag="!untagged").use(theoretical_testutils.EmptyObject()), UnexpectedExceptionRaisedInValidatorExc)
)


def originator_tag_test_function_parameter_generator(tags, originator_tag_test_suite):
    for tag in tags:
        for tagged_exception_raiser, exception_class in originator_tag_test_suite:
            yield tagged_exception_raiser, exception_class, tag


@pytest.mark.parametrize(("tagged_exception_raiser", "exception_class", "tag"), originator_tag_test_function_parameter_generator(__TAGS, __ORIGINATOR_TAG_TEST_SUITE))
def test_originator_tag(tagged_exception_raiser, exception_class, tag):
    with pytest.raises(exception_class) as e_info:
        tagged_exception_raiser(tag)
    assert e_info.value.get_originator_tag() == tag
