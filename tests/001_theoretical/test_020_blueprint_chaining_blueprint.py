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

from typing import Sequence
import theoretical_testutils
import pytest
import datetime
import zoneinfo
import time
from datalidator.blueprints.BlueprintIface import BlueprintIface
from datalidator.blueprints.ParsingMode import ParsingMode
from datalidator.blueprints.impl.StringBlueprint import StringBlueprint
from datalidator.blueprints.impl.IntegerBlueprint import IntegerBlueprint
from datalidator.blueprints.impl.FloatBlueprint import FloatBlueprint
from datalidator.blueprints.impl.BooleanBlueprint import BooleanBlueprint
from datalidator.blueprints.impl.DatetimeBlueprint import DatetimeBlueprint
from datalidator.blueprints.impl.BytesBlueprint import BytesBlueprint
from datalidator.blueprints.specialimpl.BlueprintChainingBlueprint import BlueprintChainingBlueprint
from datalidator.blueprints.exc.InputDataTypeNotInAllowlistExc import InputDataTypeNotInAllowlistExc
from datalidator.blueprints.exc.InputDataNotConvertibleExc import InputDataNotConvertibleExc
from datalidator.blueprints.exc.err.InvalidBlueprintConfigError import InvalidBlueprintConfigError
from datalidator.filters.impl.DatetimeChangeTimezoneFilter import DatetimeChangeTimezoneFilter
from datalidator.filters.impl.StringStripFilter import StringStripFilter
from datalidator.filters.impl.StringLowercaseFilter import StringLowercaseFilter
from datalidator.filters.impl.StringRegexReplaceFilter import StringRegexReplaceFilter
from datalidator.filters.impl.ReplacementMapFilter import ReplacementMapFilter
from datalidator.filters.exc.RegexFailedInFilterExc import RegexFailedInFilterExc
from datalidator.validators.impl.DatetimeIsAwareValidator import DatetimeIsAwareValidator
from datalidator.validators.impl.AllowlistValidator import AllowlistValidator
from datalidator.validators.exc.DataValidationFailedExc import DataValidationFailedExc


__BLUEPRINT_CHAINING_BLUEPRINT_TEST_SUITE = (
    (BlueprintChainingBlueprint(blueprint_chain=(
        # Allowing only Unix timestamp integer to be input into DatetimeBlueprint
        IntegerBlueprint(parsing_mode=ParsingMode.MODE_STRICT),
        DatetimeBlueprint(parsing_mode=ParsingMode.MODE_RATIONAL)
    )), (
        (datetime.datetime.now(), InputDataTypeNotInAllowlistExc),
        (datetime.datetime.now().date(), InputDataTypeNotInAllowlistExc),
        (datetime.datetime.now().time(), InputDataTypeNotInAllowlistExc),
        (time.localtime(), InputDataTypeNotInAllowlistExc),
        ("123.0", InputDataTypeNotInAllowlistExc),
        ("123", InputDataTypeNotInAllowlistExc),
        ("2020-01-01T15:20:35", InputDataTypeNotInAllowlistExc),
        (1644140893.5, InputDataTypeNotInAllowlistExc),
        (1644140893.0, InputDataTypeNotInAllowlistExc),
        (1644140893, datetime.datetime(2022, 2, 6, 9, 48, 13, tzinfo=datetime.timezone.utc)),
        (-10**12, InputDataNotConvertibleExc),
        (0, datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)),
        (0.0, InputDataTypeNotInAllowlistExc),
        (10**12, InputDataNotConvertibleExc),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc),
    )),
    (BlueprintChainingBlueprint(blueprint_chain=(
        # Checking if parsed datetime objects are aware before changing their timezone (which would fail in case of a naive datetime object)
        DatetimeBlueprint(validators=(DatetimeIsAwareValidator(),), parsing_mode=ParsingMode.MODE_STRICT),
        DatetimeBlueprint(filters=(DatetimeChangeTimezoneFilter(zoneinfo.ZoneInfo("Europe/Prague")),), parsing_mode=ParsingMode.MODE_STRICT)
    )), (
        (datetime.datetime(2021, 2, 25, 16, 30, 48), DataValidationFailedExc),
        (datetime.datetime(2021, 2, 25, 16, 30, 48, tzinfo=datetime.timezone.utc), datetime.datetime(2021, 2, 25, 17, 30, 48, tzinfo=zoneinfo.ZoneInfo("Europe/Prague"))),
        (datetime.datetime(2021, 2, 25, 16, 30, 48, tzinfo=zoneinfo.ZoneInfo("Europe/Prague")), datetime.datetime(2021, 2, 25, 16, 30, 48, tzinfo=zoneinfo.ZoneInfo("Europe/Prague"))),
        (datetime.datetime(2021, 2, 25, 16, 30, 48, tzinfo=zoneinfo.ZoneInfo("America/New_York")), datetime.datetime(2021, 2, 25, 22, 30, 48, tzinfo=zoneinfo.ZoneInfo("Europe/Prague"))),
        (time.struct_time((2022, 2, 6, 12, 17, 50, 6, 37, 0)), datetime.datetime(2022, 2, 6, 12, 17, 50, tzinfo=zoneinfo.ZoneInfo("Europe/Prague"))),
        ("2022-02-06T12:17:50", DataValidationFailedExc),
        ("2022-02-06T12:17:50+00:00", datetime.datetime(2022, 2, 6, 13, 17, 50, tzinfo=zoneinfo.ZoneInfo("Europe/Prague"))),
        ("2022-02-06T12:17:50+01:00", datetime.datetime(2022, 2, 6, 12, 17, 50, tzinfo=zoneinfo.ZoneInfo("Europe/Prague"))),
        ("2022-02-06T12:17:50-05:00", datetime.datetime(2022, 2, 6, 18, 17, 50, tzinfo=zoneinfo.ZoneInfo("Europe/Prague"))),
    )),
    (BlueprintChainingBlueprint(blueprint_chain=(
        # Localizing BooleanBlueprint
        StringBlueprint(
            filters=(
                StringStripFilter(),
                StringLowercaseFilter(),
            ),
            validators=(
                AllowlistValidator(["zapnuto", "vypnuto"]),
            ),
            parsing_mode=ParsingMode.MODE_STRICT
        ),
        StringBlueprint(
            filters=(
                ReplacementMapFilter([("zapnuto", "true"), ("vypnuto", "false")]),
            ),
            parsing_mode=ParsingMode.MODE_STRICT
        ),
        BooleanBlueprint(
            parsing_mode=ParsingMode.MODE_RATIONAL
        )
    )), (
        (True, InputDataTypeNotInAllowlistExc),
        (0, InputDataTypeNotInAllowlistExc),
        (0.0, InputDataTypeNotInAllowlistExc),
        (b'zapnuto', InputDataTypeNotInAllowlistExc),
        (b'vypnuto', InputDataTypeNotInAllowlistExc),
        (bytearray(b'zapnuto'), InputDataTypeNotInAllowlistExc),
        (bytearray(b'vypnuto'), InputDataTypeNotInAllowlistExc),
        ("true", DataValidationFailedExc),
        ("\r\nFALSE\t   ", DataValidationFailedExc),
        ("on", DataValidationFailedExc),
        ("\r\noff\t   ", DataValidationFailedExc),
        ("1", DataValidationFailedExc),
        ("\r\n0\t   ", DataValidationFailedExc),
        ("zapnuto", True),
        ("vypnuto", False),
        ("Zapnuto", True),
        ("Vypnuto", False),
        ("ZAPNUTO", True),
        ("VYPNUTO", False),
        ("\n\t\x85   \f  zapnuto\r\r   \u2029", True),
        ("\n\t\x85   \f  vypnuto\r\r   \u2029", False),
        ("\n\t\x85   \f  Zapnuto\r\r   \u2029", True),
        ("\n\t\x85   \f  Vypnuto\r\r   \u2029", False),
        ("\n\t\x85   \f  ZAPNUTO\r\r   \u2029", True),
        ("\n\t\x85   \f  VYPNUTO\r\r   \u2029", False),
        ("zap\nnuto", DataValidationFailedExc),
        ("vyp\nnuto", DataValidationFailedExc),
        ("", DataValidationFailedExc),
        ("\x00", DataValidationFailedExc),
        ("\n", DataValidationFailedExc),
        ("hello", DataValidationFailedExc),
        ("hello world", DataValidationFailedExc),
        ("\n\r\t    hello\t\n\x01\x00world \u2028", DataValidationFailedExc),
        (str, InputDataTypeNotInAllowlistExc),
        (object(), InputDataTypeNotInAllowlistExc),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc),
    )),
    (BlueprintChainingBlueprint(blueprint_chain=(
        # Re-encoding bytes from one encoding to another (from UTF-8 to Windows-1250 in this case)
        BytesBlueprint(parsing_mode=ParsingMode.MODE_STRICT),
        StringBlueprint(bytes_encoding="utf-8", parsing_mode=ParsingMode.MODE_RATIONAL),
        BytesBlueprint(string_encoding="windows-1250", parsing_mode=ParsingMode.MODE_RATIONAL)
    )), (
        (True, InputDataTypeNotInAllowlistExc),
        (0, InputDataTypeNotInAllowlistExc),
        (0.5, InputDataTypeNotInAllowlistExc),
        (None, InputDataTypeNotInAllowlistExc),
        ("", InputDataTypeNotInAllowlistExc),
        ("hello", InputDataTypeNotInAllowlistExc),
        (" hello world\r\n", InputDataTypeNotInAllowlistExc),
        (b'', b''),
        (b'hello', b'hello'),
        (b' hello world\r\n', b' hello world\r\n'),
        (b'\x00', b'\x00'),
        (b' hello\x00world\r\n', b' hello\x00world\r\n'),
        (b'\xc5\x99e\xc5\x99icha', b'\xf8e\xf8icha'),
        (b'P\xc5\x99\xc3\xadli\xc5\xa1 \xc5\xbelu\xc5\xa5ou\xc4\x8dk\xc3\xbd k\xc5\xaf\xc5\x88 \xc3\xbap\xc4\x9bl \xc4\x8f\xc3\xa1belsk\xc3\xa9 \xc3\xb3dy.', b'P\xf8\xedli\x9a \x9elu\x9dou\xe8k\xfd k\xf9\xf2 \xfap\xecl \xef\xe1belsk\xe9 \xf3dy.'),
        (b'polskoj\xc4\x99zyczna', b'polskoj\xeazyczna'),
        (b'\xef\xbf\xbf', InputDataNotConvertibleExc),
        (b'\xf0\x9f\xa4\x8d', InputDataNotConvertibleExc),
        (b'\xd0\x94\xd0\xbe\xd0\xb1\xd1\x80\xd0\xbe \xd0\xbf\xd0\xbe\xd0\xb6\xd0\xb0\xd0\xbb\xd0\xbe\xd0\xb2\xd0\xb0\xd1\x82\xd1\x8c', InputDataNotConvertibleExc),
        (bytes, InputDataTypeNotInAllowlistExc),
        (object(), InputDataTypeNotInAllowlistExc),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc),
    )),
    (BlueprintChainingBlueprint(blueprint_chain=(
        # (Testing whether exceptions are propagated correctly - not a real use case simulation!)
        IntegerBlueprint(parsing_mode=ParsingMode.MODE_STRICT),
        StringBlueprint(
            filters=(StringRegexReplaceFilter('^[0-9]', lambda x: theoretical_testutils.EmptyObject()),),  # noqa
            parsing_mode=ParsingMode.MODE_RATIONAL
        ),
        IntegerBlueprint(parsing_mode=ParsingMode.MODE_RATIONAL)
    )), (
        (-100, -100),
        (-1, -1),
        (0, RegexFailedInFilterExc),
        (1, RegexFailedInFilterExc),
        (100, RegexFailedInFilterExc),
        (1.0, InputDataTypeNotInAllowlistExc),
        (1.0, InputDataTypeNotInAllowlistExc),
        ("", InputDataTypeNotInAllowlistExc),
        ("-1", InputDataTypeNotInAllowlistExc),
        ("1", InputDataTypeNotInAllowlistExc),
        (True, RegexFailedInFilterExc),  # For historic reasons, 'bool' is a subclass of 'int'.
        (False, RegexFailedInFilterExc),  # For historic reasons, 'bool' is a subclass of 'int'.
        (int, InputDataTypeNotInAllowlistExc),
        (object(), InputDataTypeNotInAllowlistExc),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc),
    )),
)


@pytest.mark.parametrize(("blueprint", "input_", "output"), theoretical_testutils.test_function_parameter_generator(__BLUEPRINT_CHAINING_BLUEPRINT_TEST_SUITE))
def test_blueprint_chaining_blueprint(blueprint, input_, output):
    theoretical_testutils.perform_test(blueprint, input_, output)


@pytest.mark.parametrize("chain", (tuple(), []))
def test_blueprint_chaining_blueprint_empty_blueprint_chain(chain):
    with pytest.raises(InvalidBlueprintConfigError):
        BlueprintChainingBlueprint(blueprint_chain=chain)


@pytest.mark.parametrize("chain", (
        (StringBlueprint(parsing_mode=ParsingMode.MODE_STRICT),),
        (StringBlueprint(parsing_mode=ParsingMode.MODE_STRICT), IntegerBlueprint()),
        (StringBlueprint(parsing_mode=ParsingMode.MODE_STRICT), IntegerBlueprint(), FloatBlueprint()),
        (StringBlueprint(parsing_mode=ParsingMode.MODE_STRICT), IntegerBlueprint(), FloatBlueprint(), BooleanBlueprint()),
        (StringBlueprint(parsing_mode=ParsingMode.MODE_STRICT), IntegerBlueprint(), FloatBlueprint(), BooleanBlueprint(), DatetimeBlueprint()),
))
def test_blueprint_chaining_blueprint_blueprint_chain(chain: Sequence[BlueprintIface]):
    assert BlueprintChainingBlueprint(blueprint_chain=chain).get_blueprint_chain() == chain
