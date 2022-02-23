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

import theoretical_testutils
import pytest
import datetime
import zoneinfo
import ipaddress
import urllib.parse
import uuid
from test_005_dictionary_blueprint import DictableObject, ExceptionRaisingDictableObject
from datalidator.blueprints.ParsingMode import ParsingMode
from datalidator.blueprints.impl.PredefinedDictionaryBlueprint import PredefinedDictionaryBlueprint
from datalidator.blueprints.impl.GenericBlueprint import GenericBlueprint
from datalidator.blueprints.impl.IntegerBlueprint import IntegerBlueprint
from datalidator.blueprints.impl.StringBlueprint import StringBlueprint
from datalidator.blueprints.impl.DatetimeBlueprint import DatetimeBlueprint
from datalidator.blueprints.impl.DateBlueprint import DateBlueprint
from datalidator.blueprints.impl.BooleanBlueprint import BooleanBlueprint
from datalidator.blueprints.extras.OptionalItem import OptionalItem
from datalidator.blueprints.exc.InvalidInputDataExc import InvalidInputDataExc
from datalidator.blueprints.exc.InputDataNotConvertibleExc import InputDataNotConvertibleExc
from datalidator.blueprints.exc.InputDataTypeNotInAllowlistExc import InputDataTypeNotInAllowlistExc
from datalidator.blueprints.exc.InputDataValueNotAllowedForDataTypeExc import InputDataValueNotAllowedForDataTypeExc
from datalidator.filters.impl.StringStripFilter import StringStripFilter
from datalidator.filters.impl.StringLowercaseFilter import StringLowercaseFilter
from datalidator.filters.impl.DatetimeAddTimezoneFilter import DatetimeAddTimezoneFilter
from datalidator.filters.impl.DatetimeChangeTimezoneFilter import DatetimeChangeTimezoneFilter
from datalidator.validators.impl.AllowlistValidator import AllowlistValidator
from datalidator.validators.impl.StringMatchesRegexValidator import StringMatchesRegexValidator
from datalidator.validators.impl.SequenceMinimumLengthValidator import SequenceMinimumLengthValidator
from datalidator.validators.impl.DatetimeNotAfterValidator import DatetimeNotAfterValidator
from datalidator.validators.impl.DatetimeNotBeforeValidator import DatetimeNotBeforeValidator
from datalidator.validators.exc.DataValidationFailedExc import DataValidationFailedExc


__PREDEFINED_DICTIONARY_BLUEPRINT_TEST_SUITE = (
    (PredefinedDictionaryBlueprint({}, ignore_unspecified_keys_in_input=True), (
        ([], {}),
        ({}, {}),
        ([("a", "b"), ("c", "d"), ("x", "y")], {}),
        ({"a": "b", "c": "d", "x": "y"}, {}),
        ("hello world", InputDataNotConvertibleExc),
        (theoretical_testutils.EmptyObject(), InputDataNotConvertibleExc),
    )),
    (PredefinedDictionaryBlueprint({}, ignore_unspecified_keys_in_input=False), (
        ([], {}),
        ({}, {}),
        ([("a", "b"), ("c", "d"), ("x", "y")], InvalidInputDataExc),
        ({"a": "b", "c": "d", "x": "y"}, InvalidInputDataExc),
        ("hello world", InputDataNotConvertibleExc),
        (theoretical_testutils.EmptyObject(), InputDataNotConvertibleExc),
    )),
    (PredefinedDictionaryBlueprint(
        dict_specification={  
            "item": StringBlueprint(parsing_mode=ParsingMode.MODE_STRICT),
            "\t\v te\fstitem  \n\r ": IntegerBlueprint(parsing_mode=ParsingMode.MODE_STRICT),
            "": OptionalItem(BooleanBlueprint(), False),
            123: StringBlueprint(),
            12.34: OptionalItem(DatetimeBlueprint(), datetime.datetime(2022, 1, 25, 15, 20, 44, tzinfo=datetime.timezone.utc)),
            True: GenericBlueprint()
        },
        ignore_unspecified_keys_in_input=True
    ), (
        ([("a", "b"), ("c",), ("x", "y")], InputDataNotConvertibleExc),
        ([("a", "b"), ("c", "d", "e"), ("x", "y")], InputDataNotConvertibleExc),
        (((i,) for i in range(10)), InputDataNotConvertibleExc),
        (((i, i, i) for i in range(10)), InputDataNotConvertibleExc),
        ([("a", "b"), (i for i in range(1)), ("x", "y")], InputDataNotConvertibleExc),
        ([("a", "b"), (i for i in range(3)), ("x", "y")], InputDataNotConvertibleExc),
        ("a", InputDataNotConvertibleExc),
        ("ab", InputDataNotConvertibleExc),
        ("abc", InputDataNotConvertibleExc),
        ("\v hello \fworld \t\n\r", InputDataNotConvertibleExc),
        (123, InputDataNotConvertibleExc),
        (123.456, InputDataNotConvertibleExc),
        (float("-inf"), InputDataNotConvertibleExc),
        (float("nan"), InputDataNotConvertibleExc),
        (True, InputDataNotConvertibleExc),
        (None, InputDataNotConvertibleExc),
        (b'hello', InputDataNotConvertibleExc),
        (bytearray(b'hello'), InputDataNotConvertibleExc),
        (ipaddress.ip_address("127.0.0.1"), InputDataNotConvertibleExc),
        (ipaddress.ip_address("::1"), InputDataNotConvertibleExc),
        (ipaddress.ip_network("127.0.0.0/8"), InputDataNotConvertibleExc),
        (ipaddress.ip_network("2001:db8::/112"), InputDataNotConvertibleExc),
        (datetime.datetime.now(), InputDataNotConvertibleExc),
        (datetime.datetime.now().date(), InputDataNotConvertibleExc),
        (datetime.datetime.now().time(), InputDataNotConvertibleExc),
        (urllib.parse.urlparse("https://www.google.com/test?abc=def"), InputDataNotConvertibleExc),
        (uuid.UUID('{12345678-1234-5678-1234-567812345678}'), InputDataNotConvertibleExc),
        (int, InputDataNotConvertibleExc),
        (theoretical_testutils.EmptyObject, InputDataNotConvertibleExc),
        (theoretical_testutils.EmptyObject(), InputDataNotConvertibleExc),
        (DictableObject([("a", "b"), ("c",), ("x", "y")]), InputDataNotConvertibleExc),
        (DictableObject([("a", "b"), ("c", "d", "e"), ("x", "y")]), InputDataNotConvertibleExc),
        (ExceptionRaisingDictableObject(raise_=True), InputDataNotConvertibleExc),
        ([("a", "b"), ("c", "d"), ("x", "y")], InvalidInputDataExc),
        (((i, i) for i in range(10)), InvalidInputDataExc),
        ([("a", "b"), (i for i in range(2)), ("x", "y")], InvalidInputDataExc),
        ({"a": "b", "c": "d", "x": "y"}, InvalidInputDataExc),
        ([], InvalidInputDataExc),
        (dict(), InvalidInputDataExc),
        (
            {"item": "test", "\t\v te\fstitem  \n\r ": 777, "": True, 12.34: datetime.datetime(1990, 10, 20, 15, 20, 40), True: theoretical_testutils.EmptyObject()},
            InvalidInputDataExc
        ),
        (
            {"item": "test", "": True, 123: 123.456, 12.34: datetime.datetime(1990, 10, 20, 15, 20, 40), True: theoretical_testutils.EmptyObject()},
            InvalidInputDataExc
        ),
        (
            {"item": "test", "\t\v te\fstitem  \n\r ": 777, "": True, 12: 123.456, 12.34: datetime.datetime(1990, 10, 20, 15, 20, 40), True: theoretical_testutils.EmptyObject()},
            InvalidInputDataExc
        ),
        (
            {"item": "test", "\t\v te\fstitem \n\r ": 777, "": True, 123: 123.456, 12.34: datetime.datetime(1990, 10, 20, 15, 20, 40), True: theoretical_testutils.EmptyObject()},
            InvalidInputDataExc
        ),
        (
            {"item": 888, "\t\v te\fstitem  \n\r ": 777, "": True, 123: 123.456, 12.34: datetime.datetime(1990, 10, 20, 15, 20, 40), True: theoretical_testutils.EmptyObject()},
            InputDataTypeNotInAllowlistExc
        ),
        (
            {"item": "test", "\t\v te\fstitem  \n\r ": 888.0, "": True, 123: 123.456, 12.34: datetime.datetime(1990, 10, 20, 15, 20, 40), True: theoretical_testutils.EmptyObject()},
            InputDataTypeNotInAllowlistExc
        ),
        (
            {"item": "test", "\t\v te\fstitem  \n\r ": 777, "": True, 123: theoretical_testutils.EmptyObject(), 12.34: datetime.datetime(1990, 10, 20, 15, 20, 40), True: theoretical_testutils.EmptyObject()},
            InputDataTypeNotInAllowlistExc
        ),
        (  
            {"item": "test", "\t\v te\fstitem  \n\r ": 777, 123: 123.456, 12.34: datetime.datetime(1990, 10, 20, 15, 20, 40), True: theoretical_testutils.EmptyObject()},
            {"item": "test", "\t\v te\fstitem  \n\r ": 777, "": False, 123: "123.456", 12.34: datetime.datetime(1990, 10, 20, 15, 20, 40), True: theoretical_testutils.EmptyObject()},
        ),
        (  
            {"item": "test", "\t\v te\fstitem  \n\r ": 777, "": True, 123: 123.456, True: theoretical_testutils.EmptyObject()},
            {"item": "test", "\t\v te\fstitem  \n\r ": 777, "": True, 123: "123.456", 12.34: datetime.datetime(2022, 1, 25, 15, 20, 44, tzinfo=datetime.timezone.utc), True: theoretical_testutils.EmptyObject()},
        ),
        (
            {"item": "test", "\t\v te\fstitem  \n\r ": 777, "": "x", 123: 123.456, 12.34: datetime.datetime(1990, 10, 20, 15, 20, 40), True: theoretical_testutils.EmptyObject()},
            InputDataValueNotAllowedForDataTypeExc
        ),
        (
            {"item": "test", "\t\v te\fstitem  \n\r ": 777, "": None, 123: 123.456, 12.34: datetime.datetime(1990, 10, 20, 15, 20, 40), True: theoretical_testutils.EmptyObject()},
            InputDataTypeNotInAllowlistExc
        ),
        (
            {"item": "test", "\t\v te\fstitem  \n\r ": 777, "": True, 123: 123.456, 12.34: datetime.datetime.now().time(), True: theoretical_testutils.EmptyObject()},
            InputDataTypeNotInAllowlistExc
        ),
        (
            {"item": "test", "\t\v te\fstitem  \n\r ": 777, "": True, 123: 123.456, 12.34: "abcdef", True: theoretical_testutils.EmptyObject()},
            InputDataNotConvertibleExc
        ),
        (
            {"extra": False, "item": "test", "\t\v te\fstitem  \n\r ": 777, "": True, 123: 123.456, 12.34: datetime.datetime(1990, 10, 20, 15, 20, 40), True: theoretical_testutils.EmptyObject()},
            {"item": "test", "\t\v te\fstitem  \n\r ": 777, "": True, 123: "123.456", 12.34: datetime.datetime(1990, 10, 20, 15, 20, 40), True: theoretical_testutils.EmptyObject()},
        ),
        (
            {"extra": False, "something": "abc", "item": "test", "\t\v te\fstitem  \n\r ": 777, "": True, 123: 123.456, 12.34: datetime.datetime(1990, 10, 20, 15, 20, 40), True: theoretical_testutils.EmptyObject()},
            {"item": "test", "\t\v te\fstitem  \n\r ": 777, "": True, 123: "123.456", 12.34: datetime.datetime(1990, 10, 20, 15, 20, 40), True: theoretical_testutils.EmptyObject()},
        ),
        (  
            {"item": "test", "\t\v te\fstitem  \n\r ": 777, "": True, 123: 123.456, 12.34: datetime.datetime(1990, 10, 20, 15, 20, 40), True: theoretical_testutils.EmptyObject()},
            {"item": "test", "\t\v te\fstitem  \n\r ": 777, "": True, 123: "123.456", 12.34: datetime.datetime(1990, 10, 20, 15, 20, 40), True: theoretical_testutils.EmptyObject()},
        ),
        (  
            {"item": "HEL\rLo WÖRLĎ!\f\f\n", "\t\v te\fstitem  \n\r ": -456, "": "trUE", 123: ipaddress.ip_address("0000:0::0001"), 12.34: "2021-12-30T08:09:05.123888+01:00", True: (float("inf"), theoretical_testutils.EmptyObject(), 3+2j)},
            {"item": "HEL\rLo WÖRLĎ!\f\f\n", "\t\v te\fstitem  \n\r ": -456, "": True, 123: "::1", 12.34: datetime.datetime(2021, 12, 30, 8, 9, 5, 123888, tzinfo=zoneinfo.ZoneInfo("Europe/Prague")), True: (float("inf"), theoretical_testutils.EmptyObject(), 3+2j)},
        ),
    )),
    (PredefinedDictionaryBlueprint(
        dict_specification={  
            "item": StringBlueprint(parsing_mode=ParsingMode.MODE_STRICT),
            "\t\v te\fstitem  \n\r ": IntegerBlueprint(parsing_mode=ParsingMode.MODE_STRICT),
            "": OptionalItem(BooleanBlueprint(), False),
            123: StringBlueprint(),
            12.34: OptionalItem(DatetimeBlueprint(), datetime.datetime(2022, 1, 25, 15, 20, 44, tzinfo=datetime.timezone.utc)),
            True: GenericBlueprint()
        },
        ignore_unspecified_keys_in_input=False
    ), (
        ([("a", "b"), ("c",), ("x", "y")], InputDataNotConvertibleExc),
        ([("a", "b"), ("c", "d", "e"), ("x", "y")], InputDataNotConvertibleExc),
        (((i,) for i in range(10)), InputDataNotConvertibleExc),
        (((i, i, i) for i in range(10)), InputDataNotConvertibleExc),
        ([("a", "b"), (i for i in range(1)), ("x", "y")], InputDataNotConvertibleExc),
        ([("a", "b"), (i for i in range(3)), ("x", "y")], InputDataNotConvertibleExc),
        ("a", InputDataNotConvertibleExc),
        ("ab", InputDataNotConvertibleExc),
        ("abc", InputDataNotConvertibleExc),
        ("\v hello \fworld \t\n\r", InputDataNotConvertibleExc),
        (123, InputDataNotConvertibleExc),
        (123.456, InputDataNotConvertibleExc),
        (float("-inf"), InputDataNotConvertibleExc),
        (float("nan"), InputDataNotConvertibleExc),
        (True, InputDataNotConvertibleExc),
        (None, InputDataNotConvertibleExc),
        (b'hello', InputDataNotConvertibleExc),
        (bytearray(b'hello'), InputDataNotConvertibleExc),
        (ipaddress.ip_address("127.0.0.1"), InputDataNotConvertibleExc),
        (ipaddress.ip_address("::1"), InputDataNotConvertibleExc),
        (ipaddress.ip_network("127.0.0.0/8"), InputDataNotConvertibleExc),
        (ipaddress.ip_network("2001:db8::/112"), InputDataNotConvertibleExc),
        (datetime.datetime.now(), InputDataNotConvertibleExc),
        (datetime.datetime.now().date(), InputDataNotConvertibleExc),
        (datetime.datetime.now().time(), InputDataNotConvertibleExc),
        (urllib.parse.urlparse("https://www.google.com/test?abc=def"), InputDataNotConvertibleExc),
        (uuid.UUID('{12345678-1234-5678-1234-567812345678}'), InputDataNotConvertibleExc),
        (int, InputDataNotConvertibleExc),
        (theoretical_testutils.EmptyObject, InputDataNotConvertibleExc),
        (theoretical_testutils.EmptyObject(), InputDataNotConvertibleExc),
        (DictableObject([("a", "b"), ("c",), ("x", "y")]), InputDataNotConvertibleExc),
        (DictableObject([("a", "b"), ("c", "d", "e"), ("x", "y")]), InputDataNotConvertibleExc),
        (ExceptionRaisingDictableObject(raise_=True), InputDataNotConvertibleExc),
        ([("a", "b"), ("c", "d"), ("x", "y")], InvalidInputDataExc),
        (((i, i) for i in range(10)), InvalidInputDataExc),
        ([("a", "b"), (i for i in range(2)), ("x", "y")], InvalidInputDataExc),
        ({"a": "b", "c": "d", "x": "y"}, InvalidInputDataExc),
        ([], InvalidInputDataExc),
        (dict(), InvalidInputDataExc),
        (
            {"item": "test", "\t\v te\fstitem  \n\r ": 777, "": True, 12.34: datetime.datetime(1990, 10, 20, 15, 20, 40), True: theoretical_testutils.EmptyObject()},
            InvalidInputDataExc
        ),
        (
            {"item": "test", "": True, 123: 123.456, 12.34: datetime.datetime(1990, 10, 20, 15, 20, 40), True: theoretical_testutils.EmptyObject()},
            InvalidInputDataExc
        ),
        (
            {"item": "test", "\t\v te\fstitem  \n\r ": 777, "": True, 12: 123.456, 12.34: datetime.datetime(1990, 10, 20, 15, 20, 40), True: theoretical_testutils.EmptyObject()},
            InvalidInputDataExc
        ),
        (
            {"item": "test", "\t\v te\fstitem \n\r ": 777, "": True, 123: 123.456, 12.34: datetime.datetime(1990, 10, 20, 15, 20, 40), True: theoretical_testutils.EmptyObject()},
            InvalidInputDataExc
        ),
        (
            {"item": 888, "\t\v te\fstitem  \n\r ": 777, "": True, 123: 123.456, 12.34: datetime.datetime(1990, 10, 20, 15, 20, 40), True: theoretical_testutils.EmptyObject()},
            InputDataTypeNotInAllowlistExc
        ),
        (
            {"item": "test", "\t\v te\fstitem  \n\r ": 888.0, "": True, 123: 123.456, 12.34: datetime.datetime(1990, 10, 20, 15, 20, 40), True: theoretical_testutils.EmptyObject()},
            InputDataTypeNotInAllowlistExc
        ),
        (
            {"item": "test", "\t\v te\fstitem  \n\r ": 777, "": True, 123: theoretical_testutils.EmptyObject(), 12.34: datetime.datetime(1990, 10, 20, 15, 20, 40), True: theoretical_testutils.EmptyObject()},
            InputDataTypeNotInAllowlistExc
        ),
        (  
            {"item": "test", "\t\v te\fstitem  \n\r ": 777, 123: 123.456, 12.34: datetime.datetime(1990, 10, 20, 15, 20, 40), True: theoretical_testutils.EmptyObject()},
            {"item": "test", "\t\v te\fstitem  \n\r ": 777, "": False, 123: "123.456", 12.34: datetime.datetime(1990, 10, 20, 15, 20, 40), True: theoretical_testutils.EmptyObject()},
        ),
        (  
            {"item": "test", "\t\v te\fstitem  \n\r ": 777, "": True, 123: 123.456, True: theoretical_testutils.EmptyObject()},
            {"item": "test", "\t\v te\fstitem  \n\r ": 777, "": True, 123: "123.456", 12.34: datetime.datetime(2022, 1, 25, 15, 20, 44, tzinfo=datetime.timezone.utc), True: theoretical_testutils.EmptyObject()},
        ),
        (
            {"item": "test", "\t\v te\fstitem  \n\r ": 777, "": "x", 123: 123.456, 12.34: datetime.datetime(1990, 10, 20, 15, 20, 40), True: theoretical_testutils.EmptyObject()},
            InputDataValueNotAllowedForDataTypeExc
        ),
        (
            {"item": "test", "\t\v te\fstitem  \n\r ": 777, "": None, 123: 123.456, 12.34: datetime.datetime(1990, 10, 20, 15, 20, 40), True: theoretical_testutils.EmptyObject()},
            InputDataTypeNotInAllowlistExc
        ),
        (
            {"item": "test", "\t\v te\fstitem  \n\r ": 777, "": True, 123: 123.456, 12.34: datetime.datetime.now().time(), True: theoretical_testutils.EmptyObject()},
            InputDataTypeNotInAllowlistExc
        ),
        (
            {"item": "test", "\t\v te\fstitem  \n\r ": 777, "": True, 123: 123.456, 12.34: "abcdef", True: theoretical_testutils.EmptyObject()},
            InputDataNotConvertibleExc
        ),
        (
            {"extra": False, "item": "test", "\t\v te\fstitem  \n\r ": 777, "": True, 123: 123.456, 12.34: datetime.datetime(1990, 10, 20, 15, 20, 40), True: theoretical_testutils.EmptyObject()},
            InvalidInputDataExc
        ),
        (
            {"extra": False, "something": "abc", "item": "test", "\t\v te\fstitem  \n\r ": 777, "": True, 123: 123.456, 12.34: datetime.datetime(1990, 10, 20, 15, 20, 40), True: theoretical_testutils.EmptyObject()},
            InvalidInputDataExc
        ),
        (  
            {"item": "test", "\t\v te\fstitem  \n\r ": 777, "": True, 123: 123.456, 12.34: datetime.datetime(1990, 10, 20, 15, 20, 40), True: theoretical_testutils.EmptyObject()},
            {"item": "test", "\t\v te\fstitem  \n\r ": 777, "": True, 123: "123.456", 12.34: datetime.datetime(1990, 10, 20, 15, 20, 40), True: theoretical_testutils.EmptyObject()},
        ),
        (  
            {"item": "HEL\rLo WÖRLĎ!\f\f\n", "\t\v te\fstitem  \n\r ": -456, "": "trUE", 123: ipaddress.ip_address("0000:0::0001"), 12.34: "2021-12-30T08:09:05.123888+01:00", True: (float("inf"), theoretical_testutils.EmptyObject(), 3+2j)},
            {"item": "HEL\rLo WÖRLĎ!\f\f\n", "\t\v te\fstitem  \n\r ": -456, "": True, 123: "::1", 12.34: datetime.datetime(2021, 12, 30, 8, 9, 5, 123888, tzinfo=zoneinfo.ZoneInfo("Europe/Prague")), True: (float("inf"), theoretical_testutils.EmptyObject(), 3+2j)},
        )
    )),
    (PredefinedDictionaryBlueprint(dict_specification={
        # "Weird" dictionary specification keys should work too
        float("-inf"): IntegerBlueprint(),
        ipaddress.ip_network("2001:db8::/96"): StringBlueprint(parsing_mode=ParsingMode.MODE_STRICT),
        urllib.parse.urlparse("https://www.google.com/keytest?abc=def"): OptionalItem(GenericBlueprint(), None)
    }, ignore_unspecified_keys_in_input=True), (
        (
            {float("-inf"): "   000_789_000\r\n", ipaddress.ip_network("2001:db8::/96"): "xyz", urllib.parse.urlparse("https://www.google.com/keytest?abc=def"): theoretical_testutils.EmptyObject()},
            {float("-inf"): 789000, ipaddress.ip_network("2001:db8::/96"): "xyz", urllib.parse.urlparse("https://www.google.com/keytest?abc=def"): theoretical_testutils.EmptyObject()},
        ),
        (
            {float("-inf"): "   000_789_000\r\n", ipaddress.ip_network("2001:db8::/96"): "xyz", urllib.parse.urlparse("https://www.google.com/keytest?abc=def"): theoretical_testutils.EmptyObject(), "abc": "def"},
            {float("-inf"): 789000, ipaddress.ip_network("2001:db8::/96"): "xyz", urllib.parse.urlparse("https://www.google.com/keytest?abc=def"): theoretical_testutils.EmptyObject()},
        ),
        (
            {float("-inf"): theoretical_testutils.EmptyObject(), ipaddress.ip_network("2001:db8::/96"): "xyz", urllib.parse.urlparse("https://www.google.com/keytest?abc=def"): theoretical_testutils.EmptyObject()},
            InputDataTypeNotInAllowlistExc
        ),
        (
            {float("-inf"): "   000_789_000\r\n", ipaddress.ip_network("2001:db8::/96"): 777, urllib.parse.urlparse("https://www.google.com/keytest?abc=def"): theoretical_testutils.EmptyObject()},
            InputDataTypeNotInAllowlistExc
        ),
        (
            {ipaddress.ip_network("2001:db8::/96"): "xyz", urllib.parse.urlparse("https://www.google.com/keytest?abc=def"): theoretical_testutils.EmptyObject()},
            InvalidInputDataExc
        ),
        (
            {float("-inf"): "   000_789_000\r\n", urllib.parse.urlparse("https://www.google.com/keytest?abc=def"): theoretical_testutils.EmptyObject()},
            InvalidInputDataExc
        ),
        (
            {float("-inf"): "   000_789_000\r\n", "2001:db8::/96": "xyz", urllib.parse.urlparse("https://www.google.com/keytest?abc=def"): theoretical_testutils.EmptyObject()},
            InvalidInputDataExc
        ),
        (
            {float("-inf"): "   000_789_000\r\n", ipaddress.ip_network("2001:db8::/96"): "xyz"},
            {float("-inf"): 789000, ipaddress.ip_network("2001:db8::/96"): "xyz", urllib.parse.urlparse("https://www.google.com/keytest?abc=def"): None},
        ),
        (
            {float("-inf"): "   000_789_000\r\n", ipaddress.ip_network("2001:db8::/96"): "xyz", urllib.parse.urlparse("https://www.google.com/keytest2?abc=def"): theoretical_testutils.EmptyObject()},
            {float("-inf"): 789000, ipaddress.ip_network("2001:db8::/96"): "xyz", urllib.parse.urlparse("https://www.google.com/keytest?abc=def"): None},
        ),
    )),
    (PredefinedDictionaryBlueprint(dict_specification={
        # "Weird" dictionary specification keys should work too
        float("-inf"): IntegerBlueprint(),
        ipaddress.ip_network("2001:db8::/96"): StringBlueprint(parsing_mode=ParsingMode.MODE_STRICT),
        urllib.parse.urlparse("https://www.google.com/keytest?abc=def"): OptionalItem(GenericBlueprint(), None)
    }, ignore_unspecified_keys_in_input=False), (
        (
            {float("-inf"): "   000_789_000\r\n", ipaddress.ip_network("2001:db8::/96"): "xyz", urllib.parse.urlparse("https://www.google.com/keytest?abc=def"): theoretical_testutils.EmptyObject()},
            {float("-inf"): 789000, ipaddress.ip_network("2001:db8::/96"): "xyz", urllib.parse.urlparse("https://www.google.com/keytest?abc=def"): theoretical_testutils.EmptyObject()},
        ),
        (
            {float("-inf"): "   000_789_000\r\n", ipaddress.ip_network("2001:db8::/96"): "xyz", urllib.parse.urlparse("https://www.google.com/keytest?abc=def"): theoretical_testutils.EmptyObject(), "abc": "def"},
            InvalidInputDataExc
        ),
        (
            {float("-inf"): theoretical_testutils.EmptyObject(), ipaddress.ip_network("2001:db8::/96"): "xyz", urllib.parse.urlparse("https://www.google.com/keytest?abc=def"): theoretical_testutils.EmptyObject()},
            InputDataTypeNotInAllowlistExc
        ),
        (
            {float("-inf"): "   000_789_000\r\n", ipaddress.ip_network("2001:db8::/96"): 777, urllib.parse.urlparse("https://www.google.com/keytest?abc=def"): theoretical_testutils.EmptyObject()},
            InputDataTypeNotInAllowlistExc
        ),
        (
            {ipaddress.ip_network("2001:db8::/96"): "xyz", urllib.parse.urlparse("https://www.google.com/keytest?abc=def"): theoretical_testutils.EmptyObject()},
            InvalidInputDataExc
        ),
        (
            {float("-inf"): "   000_789_000\r\n", urllib.parse.urlparse("https://www.google.com/keytest?abc=def"): theoretical_testutils.EmptyObject()},
            InvalidInputDataExc
        ),
        (
            {float("-inf"): "   000_789_000\r\n", "2001:db8::/96": "xyz", urllib.parse.urlparse("https://www.google.com/keytest?abc=def"): theoretical_testutils.EmptyObject()},
            InvalidInputDataExc
        ),
        (
            {float("-inf"): "   000_789_000\r\n", ipaddress.ip_network("2001:db8::/96"): "xyz"},
            {float("-inf"): 789000, ipaddress.ip_network("2001:db8::/96"): "xyz", urllib.parse.urlparse("https://www.google.com/keytest?abc=def"): None},
        ),
        (
            {float("-inf"): "   000_789_000\r\n", ipaddress.ip_network("2001:db8::/96"): "xyz", urllib.parse.urlparse("https://www.google.com/keytest2?abc=def"): theoretical_testutils.EmptyObject()},
            InvalidInputDataExc
        ),
    )),
    (PredefinedDictionaryBlueprint(dict_specification={  
        # Real use case simulation - a simple registration form
        "username": StringBlueprint(
            filters=(StringStripFilter(),),
            validators=(StringMatchesRegexValidator(r'^[A-Za-z0-9]{3,15}\Z'),),
            parsing_mode=ParsingMode.MODE_STRICT
        ),
        "password": StringBlueprint(
            filters=(StringStripFilter(),),
            validators=(SequenceMinimumLengthValidator(8),),
            parsing_mode=ParsingMode.MODE_STRICT
        ),
        "email": StringBlueprint(
            filters=(StringStripFilter(), StringLowercaseFilter()),
            validators=(StringMatchesRegexValidator(r'^[a-z0-9.-]+@[a-z0-9.-]+\.[a-z]+\Z'),),
            parsing_mode=ParsingMode.MODE_STRICT
        ),
        "date_of_birth": DateBlueprint(DatetimeBlueprint(
            additional_datetime_string_formats=("%Y-%m-%d",),
            filters=(DatetimeAddTimezoneFilter(datetime.timezone.utc), DatetimeChangeTimezoneFilter(datetime.timezone.utc)),
            validators=(DatetimeNotBeforeValidator(datetime.datetime(1900, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)), DatetimeNotAfterValidator(datetime.datetime(2019, 12, 31, 23, 59, 59, tzinfo=datetime.timezone.utc))),
            parsing_mode=ParsingMode.MODE_STRICT
        )),
        "gender": OptionalItem(wrapped_blueprint=StringBlueprint(
            filters=(StringStripFilter(), StringLowercaseFilter()),
            validators=(AllowlistValidator(("male", "female", "other")),),
            parsing_mode=ParsingMode.MODE_STRICT
        ), default_value="other")
    }, ignore_unspecified_keys_in_input=True), (
        ([["username", "test"], ["password", "123456789"], ["email"], ["date_of_birth", "1995-06-20"], ["gender", "female"]], InputDataNotConvertibleExc),
        ([["username", "test"], ["password", "123456789"], ["email", "nobody@example.com", "!!!"], ["date_of_birth", "1995-06-20"], ["gender", "female"]], InputDataNotConvertibleExc),
        (
            [["username", "test"], ["password", "123456789"], ["email", "nobody@example.com"], ["date_of_birth", "1995-06-20"], ["gender", "female"]],
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        ({"password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"}, InvalidInputDataExc),
        ({"username ": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"}, InvalidInputDataExc),
        ({"username": "test", "password": "123456789", "email": "nobody@example.com", "gender": "female"}, InvalidInputDataExc),
        ({"username": "test", "password": "123456789", "email": "nobody@example.com", "\ndate_of_birth": "1995-06-20", "gender": "female"}, InvalidInputDataExc),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20"},
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "other"}
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender_": "female"},
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "other"}
        ),
        (
            {"something": "else", "username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        (
            {"something": "else", ipaddress.ip_address("127.0.0.1"): 123, "username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        (
            {"something": "else", object(): theoretical_testutils.EmptyObject(), "username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        (
            {"username": "\n  \r\v   test\f\f", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        (
            {"username": "test\n", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        (
            {"username": "te\nst", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            DataValidationFailedExc
        ),
        (
            {"username": "tést", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            DataValidationFailedExc
        ),
        (
            {"username": "tes", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            {"username": "tes", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        (
            {"username": "\v\f  te   \t\t    ", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            DataValidationFailedExc
        ),
        (
            {"username": "te st", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            DataValidationFailedExc
        ),
        (
            {"username": "\t\f012345678901234  \r\n", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            {"username": "012345678901234", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        (
            {"username": "0123456789012345", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            DataValidationFailedExc
        ),
        (
            {"username": 123, "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            InputDataTypeNotInAllowlistExc
        ),
        (
            {"username": theoretical_testutils.EmptyObject(), "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            InputDataTypeNotInAllowlistExc
        ),
        (
            {"username": "test", "password": "\v\v\f   123456789 \t \r\n", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        (
            {"username": "test", "password": "12345678", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            {"username": "test", "password": "12345678", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        (
            {"username": "test", "password": "\t\f  \r\n1234567     ", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            DataValidationFailedExc
        ),
        (
            {"username": "test", "password": "  \t ěřš čř ěšč ř qwřč ěšč\nř+š \v\f\tč ěšč ř+ě ššč +ě šč+ ě š žčřě  čšě + ěšč +ěš č+ě   \t\r", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            {"username": "test", "password": "ěřš čř ěšč ř qwřč ěšč\nř+š \v\f\tč ěšč ř+ě ššč +ě šč+ ě š žčřě  čšě + ěšč +ěš č+ě", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        (
            {"username": "test", "password": 123, "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            InputDataTypeNotInAllowlistExc
        ),
        (
            {"username": "test", "password": theoretical_testutils.EmptyObject(), "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            InputDataTypeNotInAllowlistExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "\t nobody@example.com\r\n", "date_of_birth": "1995-06-20", "gender": "female"},
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        (
            {"username": "test", "password": "123456789", "email": "no-bo.dy@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            {"username": "test", "password": "123456789", "email": "no-bo.dy@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        (
            {"username": "test", "password": "123456789", "email": "NOBODY@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@EXAMPLE.com", "date_of_birth": "1995-06-20", "gender": "female"},
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        (
            {"username": "test", "password": "123456789", "email": "NOboDY@EXAMPLE.COm", "date_of_birth": "1995-06-20", "gender": "female"},
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobodyexample.com", "date_of_birth": "1995-06-20", "gender": "female"},
            DataValidationFailedExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            DataValidationFailedExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody @example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            DataValidationFailedExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "no body@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            DataValidationFailedExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nošbody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            DataValidationFailedExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@examplecom", "date_of_birth": "1995-06-20", "gender": "female"},
            DataValidationFailedExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@server.example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            {"username": "test", "password": "123456789", "email": "nobody@server.example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@exa-mple.com", "date_of_birth": "1995-06-20", "gender": "female"},
            {"username": "test", "password": "123456789", "email": "nobody@exa-mple.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@ example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            DataValidationFailedExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@exa mple.com", "date_of_birth": "1995-06-20", "gender": "female"},
            DataValidationFailedExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@exašmple.com", "date_of_birth": "1995-06-20", "gender": "female"},
            DataValidationFailedExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.", "date_of_birth": "1995-06-20", "gender": "female"},
            DataValidationFailedExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com1", "date_of_birth": "1995-06-20", "gender": "female"},
            DataValidationFailedExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example. com", "date_of_birth": "1995-06-20", "gender": "female"},
            DataValidationFailedExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.co m", "date_of_birth": "1995-06-20", "gender": "female"},
            DataValidationFailedExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.c-om", "date_of_birth": "1995-06-20", "gender": "female"},
            DataValidationFailedExc
        ),
        (
            {"username": "test", "password": "123456789", "email": 123, "date_of_birth": "1995-06-20", "gender": "female"},
            InputDataTypeNotInAllowlistExc
        ),
        (
            {"username": "test", "password": "123456789", "email": theoretical_testutils.EmptyObject(), "date_of_birth": "1995-06-20", "gender": "female"},
            InputDataTypeNotInAllowlistExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "   1995-06-20 \t\f\v", "gender": "female"},
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995- 06-20", "gender": "female"},
            InputDataNotConvertibleExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995x06-20", "gender": "female"},
            InputDataNotConvertibleExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995- 06-20", "gender": "female"},
            InputDataNotConvertibleExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20T12:45:50", "gender": "female"},
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20T12:45:50+06:00", "gender": "female"},
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20T12:45:50.112233-08:00", "gender": "female"},
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-\x0020", "gender": "female"},
            InputDataNotConvertibleExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1900-01-01", "gender": "female"},
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1900, 1, 1), "gender": "female"}
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1899-12-31", "gender": "female"},
            DataValidationFailedExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "2019-12-31", "gender": "female"},
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(2019, 12, 31), "gender": "female"}
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "2020-01-01", "gender": "female"},
            DataValidationFailedExc
        ),
        (  
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.datetime(1995, 6, 20, 15, 23, 45), "gender": "female"},
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": 123, "gender": "female"},
            InputDataTypeNotInAllowlistExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": 123.456, "gender": "female"},
            InputDataTypeNotInAllowlistExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": theoretical_testutils.EmptyObject(), "gender": "female"},
            InputDataTypeNotInAllowlistExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "\r\n   fEMaLe   \v\f "},
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "\r\n   MaLe   \v\f "},
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "male"}
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "\r\n   OTHeR   \v\f "},
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "other"}
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "fe male"},
            DataValidationFailedExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "\t\r\n"},
            DataValidationFailedExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "<nogender>"},
            DataValidationFailedExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "\r\n   fEMáLe   \v\f "},
            DataValidationFailedExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": 123},
            InputDataTypeNotInAllowlistExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": theoretical_testutils.EmptyObject()},
            InputDataTypeNotInAllowlistExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", float("nan"): "female"},
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "other"}
        ),
        (
            {object(): "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            InvalidInputDataExc
        ),
        (
            {123: "test", True: "123456789", None: "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            InvalidInputDataExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female", 123: True},
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", 123: True, ipaddress.ip_network("127.0.0.0/8"): 8+2j},
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "other"}
        ),
        ([], InvalidInputDataExc),
        (dict(), InvalidInputDataExc),
        (set(), InvalidInputDataExc),
        (tuple(), InvalidInputDataExc),
        (range(0), InvalidInputDataExc),
        ((i for i in range(0)), InvalidInputDataExc),
        ([("a", "b"), ("c",), ("x", "y")], InputDataNotConvertibleExc),
        ([("a", "b"), ("c", "d", "e"), ("x", "y")], InputDataNotConvertibleExc),
        (((i,) for i in range(10)), InputDataNotConvertibleExc),
        (((i, i, i) for i in range(10)), InputDataNotConvertibleExc),
        ([("a", "b"), (i for i in range(1)), ("x", "y")], InputDataNotConvertibleExc),
        ([("a", "b"), (i for i in range(3)), ("x", "y")], InputDataNotConvertibleExc),
        ("a", InputDataNotConvertibleExc),
        ("ab", InputDataNotConvertibleExc),
        ("abc", InputDataNotConvertibleExc),
        ("\v hello \fworld \t\n\r", InputDataNotConvertibleExc),
        (123, InputDataNotConvertibleExc),
        (123.456, InputDataNotConvertibleExc),
        (float("-inf"), InputDataNotConvertibleExc),
        (float("nan"), InputDataNotConvertibleExc),
        (True, InputDataNotConvertibleExc),
        (None, InputDataNotConvertibleExc),
        (b'hello', InputDataNotConvertibleExc),
        (bytearray(b'hello'), InputDataNotConvertibleExc),
        (ipaddress.ip_address("127.0.0.1"), InputDataNotConvertibleExc),
        (ipaddress.ip_address("::1"), InputDataNotConvertibleExc),
        (ipaddress.ip_network("127.0.0.0/8"), InputDataNotConvertibleExc),
        (ipaddress.ip_network("2001:db8::/112"), InputDataNotConvertibleExc),
        (datetime.datetime.now(), InputDataNotConvertibleExc),
        (datetime.datetime.now().date(), InputDataNotConvertibleExc),
        (datetime.datetime.now().time(), InputDataNotConvertibleExc),
        (urllib.parse.urlparse("https://www.google.com/test?abc=def"), InputDataNotConvertibleExc),
        (uuid.UUID('{12345678-1234-5678-1234-567812345678}'), InputDataNotConvertibleExc),
        (int, InputDataNotConvertibleExc),
        (theoretical_testutils.EmptyObject, InputDataNotConvertibleExc),
        (theoretical_testutils.EmptyObject(), InputDataNotConvertibleExc),
        (DictableObject([("a", "b"), ("c",), ("x", "y")]), InputDataNotConvertibleExc),
        (DictableObject([("a", "b"), ("c", "d", "e"), ("x", "y")]), InputDataNotConvertibleExc),
        (ExceptionRaisingDictableObject(raise_=True), InputDataNotConvertibleExc),
    )),
    (PredefinedDictionaryBlueprint(dict_specification={  
        # Real use case simulation - a simple registration form
        "username": StringBlueprint(
            filters=(StringStripFilter(),),
            validators=(StringMatchesRegexValidator(r'^[A-Za-z0-9]{3,15}\Z'),),
            parsing_mode=ParsingMode.MODE_STRICT
        ),
        "password": StringBlueprint(
            filters=(StringStripFilter(),),
            validators=(SequenceMinimumLengthValidator(8),),
            parsing_mode=ParsingMode.MODE_STRICT
        ),
        "email": StringBlueprint(
            filters=(StringStripFilter(), StringLowercaseFilter()),
            validators=(StringMatchesRegexValidator(r'^[a-z0-9.-]+@[a-z0-9.-]+\.[a-z]+\Z'),),
            parsing_mode=ParsingMode.MODE_STRICT
        ),
        "date_of_birth": DateBlueprint(DatetimeBlueprint(
            additional_datetime_string_formats=("%Y-%m-%d",),
            filters=(DatetimeAddTimezoneFilter(datetime.timezone.utc), DatetimeChangeTimezoneFilter(datetime.timezone.utc)),
            validators=(DatetimeNotBeforeValidator(datetime.datetime(1900, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)), DatetimeNotAfterValidator(datetime.datetime(2019, 12, 31, 23, 59, 59, tzinfo=datetime.timezone.utc))),
            parsing_mode=ParsingMode.MODE_STRICT
        )),
        "gender": OptionalItem(wrapped_blueprint=StringBlueprint(
            filters=(StringStripFilter(), StringLowercaseFilter()),
            validators=(AllowlistValidator(("male", "female", "other")),),
            parsing_mode=ParsingMode.MODE_STRICT
        ), default_value="other")
    }, ignore_unspecified_keys_in_input=False), (
        ([["username", "test"], ["password", "123456789"], ["email"], ["date_of_birth", "1995-06-20"], ["gender", "female"]], InputDataNotConvertibleExc),
        ([["username", "test"], ["password", "123456789"], ["email", "nobody@example.com", "!!!"], ["date_of_birth", "1995-06-20"], ["gender", "female"]], InputDataNotConvertibleExc),
        (
            [["username", "test"], ["password", "123456789"], ["email", "nobody@example.com"], ["date_of_birth", "1995-06-20"], ["gender", "female"]],
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        ({"password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"}, InvalidInputDataExc),
        ({"username ": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"}, InvalidInputDataExc),
        ({"username": "test", "password": "123456789", "email": "nobody@example.com", "gender": "female"}, InvalidInputDataExc),
        ({"username": "test", "password": "123456789", "email": "nobody@example.com", "\ndate_of_birth": "1995-06-20", "gender": "female"}, InvalidInputDataExc),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20"},
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "other"}
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender_": "female"},
            InvalidInputDataExc
        ),
        (
            {"something": "else", "username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            InvalidInputDataExc
        ),
        (
            {"something": "else", ipaddress.ip_address("127.0.0.1"): 123, "username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            InvalidInputDataExc
        ),
        (
            {"something": "else", object(): theoretical_testutils.EmptyObject(), "username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            InvalidInputDataExc
        ),
        (
            {"username": "\n  \r\v   test\f\f", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        (
            {"username": "test\n", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        (
            {"username": "te\nst", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            DataValidationFailedExc
        ),
        (
            {"username": "tést", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            DataValidationFailedExc
        ),
        (
            {"username": "tes", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            {"username": "tes", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        (
            {"username": "\v\f  te   \t\t    ", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            DataValidationFailedExc
        ),
        (
            {"username": "te st", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            DataValidationFailedExc
        ),
        (
            {"username": "\t\f012345678901234  \r\n", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            {"username": "012345678901234", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        (
            {"username": "0123456789012345", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            DataValidationFailedExc
        ),
        (
            {"username": 123, "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            InputDataTypeNotInAllowlistExc
        ),
        (
            {"username": theoretical_testutils.EmptyObject(), "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            InputDataTypeNotInAllowlistExc
        ),
        (
            {"username": "test", "password": "\v\v\f   123456789 \t \r\n", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        (
            {"username": "test", "password": "12345678", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            {"username": "test", "password": "12345678", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        (
            {"username": "test", "password": "\t\f  \r\n1234567     ", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            DataValidationFailedExc
        ),
        (
            {"username": "test", "password": "  \t ěřš čř ěšč ř qwřč ěšč\nř+š \v\f\tč ěšč ř+ě ššč +ě šč+ ě š žčřě  čšě + ěšč +ěš č+ě   \t\r", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            {"username": "test", "password": "ěřš čř ěšč ř qwřč ěšč\nř+š \v\f\tč ěšč ř+ě ššč +ě šč+ ě š žčřě  čšě + ěšč +ěš č+ě", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        (
            {"username": "test", "password": 123, "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            InputDataTypeNotInAllowlistExc
        ),
        (
            {"username": "test", "password": theoretical_testutils.EmptyObject(), "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            InputDataTypeNotInAllowlistExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "\t nobody@example.com\r\n", "date_of_birth": "1995-06-20", "gender": "female"},
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        (
            {"username": "test", "password": "123456789", "email": "no-bo.dy@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            {"username": "test", "password": "123456789", "email": "no-bo.dy@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        (
            {"username": "test", "password": "123456789", "email": "NOBODY@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@EXAMPLE.com", "date_of_birth": "1995-06-20", "gender": "female"},
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        (
            {"username": "test", "password": "123456789", "email": "NOboDY@EXAMPLE.COm", "date_of_birth": "1995-06-20", "gender": "female"},
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobodyexample.com", "date_of_birth": "1995-06-20", "gender": "female"},
            DataValidationFailedExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            DataValidationFailedExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody @example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            DataValidationFailedExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "no body@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            DataValidationFailedExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nošbody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            DataValidationFailedExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@examplecom", "date_of_birth": "1995-06-20", "gender": "female"},
            DataValidationFailedExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@server.example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            {"username": "test", "password": "123456789", "email": "nobody@server.example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@exa-mple.com", "date_of_birth": "1995-06-20", "gender": "female"},
            {"username": "test", "password": "123456789", "email": "nobody@exa-mple.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@ example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            DataValidationFailedExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@exa mple.com", "date_of_birth": "1995-06-20", "gender": "female"},
            DataValidationFailedExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@exašmple.com", "date_of_birth": "1995-06-20", "gender": "female"},
            DataValidationFailedExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.", "date_of_birth": "1995-06-20", "gender": "female"},
            DataValidationFailedExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com1", "date_of_birth": "1995-06-20", "gender": "female"},
            DataValidationFailedExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example. com", "date_of_birth": "1995-06-20", "gender": "female"},
            DataValidationFailedExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.co m", "date_of_birth": "1995-06-20", "gender": "female"},
            DataValidationFailedExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.c-om", "date_of_birth": "1995-06-20", "gender": "female"},
            DataValidationFailedExc
        ),
        (
            {"username": "test", "password": "123456789", "email": 123, "date_of_birth": "1995-06-20", "gender": "female"},
            InputDataTypeNotInAllowlistExc
        ),
        (
            {"username": "test", "password": "123456789", "email": theoretical_testutils.EmptyObject(), "date_of_birth": "1995-06-20", "gender": "female"},
            InputDataTypeNotInAllowlistExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "   1995-06-20 \t\f\v", "gender": "female"},
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995- 06-20", "gender": "female"},
            InputDataNotConvertibleExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995x06-20", "gender": "female"},
            InputDataNotConvertibleExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995- 06-20", "gender": "female"},
            InputDataNotConvertibleExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20T12:45:50", "gender": "female"},
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20T12:45:50+06:00", "gender": "female"},
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20T12:45:50.112233-08:00", "gender": "female"},
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-\x0020", "gender": "female"},
            InputDataNotConvertibleExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1900-01-01", "gender": "female"},
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1900, 1, 1), "gender": "female"}
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1899-12-31", "gender": "female"},
            DataValidationFailedExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "2019-12-31", "gender": "female"},
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(2019, 12, 31), "gender": "female"}
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "2020-01-01", "gender": "female"},
            DataValidationFailedExc
        ),
        (  
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.datetime(1995, 6, 20, 15, 23, 45), "gender": "female"},
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": 123, "gender": "female"},
            InputDataTypeNotInAllowlistExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": 123.456, "gender": "female"},
            InputDataTypeNotInAllowlistExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": theoretical_testutils.EmptyObject(), "gender": "female"},
            InputDataTypeNotInAllowlistExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "\r\n   fEMaLe   \v\f "},
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "female"}
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "\r\n   MaLe   \v\f "},
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "male"}
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "\r\n   OTHeR   \v\f "},
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.date(1995, 6, 20), "gender": "other"}
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "fe male"},
            DataValidationFailedExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "\t\r\n"},
            DataValidationFailedExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "<nogender>"},
            DataValidationFailedExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "\r\n   fEMáLe   \v\f "},
            DataValidationFailedExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": 123},
            InputDataTypeNotInAllowlistExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": theoretical_testutils.EmptyObject()},
            InputDataTypeNotInAllowlistExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", float("nan"): "female"},
            InvalidInputDataExc
        ),
        (
            {object(): "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            InvalidInputDataExc
        ),
        (
            {123: "test", True: "123456789", None: "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            InvalidInputDataExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female", 123: True},
            InvalidInputDataExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", 123: True, ipaddress.ip_network("127.0.0.0/8"): 8+2j},
            InvalidInputDataExc
        ),
        ([], InvalidInputDataExc),
        (dict(), InvalidInputDataExc),
        (set(), InvalidInputDataExc),
        (tuple(), InvalidInputDataExc),
        (range(0), InvalidInputDataExc),
        ((i for i in range(0)), InvalidInputDataExc),
        ([("a", "b"), ("c",), ("x", "y")], InputDataNotConvertibleExc),
        ([("a", "b"), ("c", "d", "e"), ("x", "y")], InputDataNotConvertibleExc),
        (((i,) for i in range(10)), InputDataNotConvertibleExc),
        (((i, i, i) for i in range(10)), InputDataNotConvertibleExc),
        ([("a", "b"), (i for i in range(1)), ("x", "y")], InputDataNotConvertibleExc),
        ([("a", "b"), (i for i in range(3)), ("x", "y")], InputDataNotConvertibleExc),
        ("a", InputDataNotConvertibleExc),
        ("ab", InputDataNotConvertibleExc),
        ("abc", InputDataNotConvertibleExc),
        ("\v hello \fworld \t\n\r", InputDataNotConvertibleExc),
        (123, InputDataNotConvertibleExc),
        (123.456, InputDataNotConvertibleExc),
        (float("-inf"), InputDataNotConvertibleExc),
        (float("nan"), InputDataNotConvertibleExc),
        (True, InputDataNotConvertibleExc),
        (None, InputDataNotConvertibleExc),
        (b'hello', InputDataNotConvertibleExc),
        (bytearray(b'hello'), InputDataNotConvertibleExc),
        (ipaddress.ip_address("127.0.0.1"), InputDataNotConvertibleExc),
        (ipaddress.ip_address("::1"), InputDataNotConvertibleExc),
        (ipaddress.ip_network("127.0.0.0/8"), InputDataNotConvertibleExc),
        (ipaddress.ip_network("2001:db8::/112"), InputDataNotConvertibleExc),
        (datetime.datetime.now(), InputDataNotConvertibleExc),
        (datetime.datetime.now().date(), InputDataNotConvertibleExc),
        (datetime.datetime.now().time(), InputDataNotConvertibleExc),
        (urllib.parse.urlparse("https://www.google.com/test?abc=def"), InputDataNotConvertibleExc),
        (uuid.UUID('{12345678-1234-5678-1234-567812345678}'), InputDataNotConvertibleExc),
        (int, InputDataNotConvertibleExc),
        (theoretical_testutils.EmptyObject, InputDataNotConvertibleExc),
        (theoretical_testutils.EmptyObject(), InputDataNotConvertibleExc),
        (DictableObject([("a", "b"), ("c",), ("x", "y")]), InputDataNotConvertibleExc),
        (DictableObject([("a", "b"), ("c", "d", "e"), ("x", "y")]), InputDataNotConvertibleExc),
        (ExceptionRaisingDictableObject(raise_=True), InputDataNotConvertibleExc),
    )),
)


@pytest.mark.parametrize(("blueprint", "input_", "output"), theoretical_testutils.test_function_parameter_generator(__PREDEFINED_DICTIONARY_BLUEPRINT_TEST_SUITE))
def test_predefined_dictionary_blueprint(blueprint, input_, output):
    theoretical_testutils.perform_test(blueprint, input_, output)


@pytest.mark.parametrize("specification", (
        {},
        {"abc": GenericBlueprint()},
        {0: GenericBlueprint(), True: OptionalItem(GenericBlueprint(), None), 3.5: GenericBlueprint()},
        {str(k): GenericBlueprint() for k in range(20)}
))
def test_predefined_dictionary_blueprint_dict_specification(specification):
    assert PredefinedDictionaryBlueprint(dict_specification=specification).get_dict_specification() == specification


def test_predefined_dictionary_blueprint_default_ignore_unspecified_keys_in_input():
    assert PredefinedDictionaryBlueprint({"hello": GenericBlueprint()}).are_unspecified_keys_in_input_ignored() is True


def test_predefined_dictionary_blueprint_ignore_unspecified_keys_in_input():
    assert PredefinedDictionaryBlueprint({"test": GenericBlueprint()}, ignore_unspecified_keys_in_input=False).are_unspecified_keys_in_input_ignored() is False
