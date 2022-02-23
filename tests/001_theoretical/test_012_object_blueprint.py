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
from datalidator.blueprints.impl.ObjectBlueprint import ObjectBlueprint
from datalidator.blueprints.impl.IntegerBlueprint import IntegerBlueprint
from datalidator.blueprints.impl.StringBlueprint import StringBlueprint
from datalidator.blueprints.impl.BooleanBlueprint import BooleanBlueprint
from datalidator.blueprints.impl.IPAddressBlueprint import IPAddressBlueprint
from datalidator.blueprints.impl.DatetimeBlueprint import DatetimeBlueprint
from datalidator.blueprints.impl.DateBlueprint import DateBlueprint
from datalidator.blueprints.impl.ListBlueprint import ListBlueprint
from datalidator.blueprints.impl.GenericBlueprint import GenericBlueprint
from datalidator.blueprints.extras.ObjectModel import ObjectModel
from datalidator.blueprints.extras.OptionalItem import OptionalItem
from datalidator.blueprints.exc.InvalidInputDataExc import InvalidInputDataExc
from datalidator.blueprints.exc.InputDataNotConvertibleExc import InputDataNotConvertibleExc
from datalidator.blueprints.exc.InputDataValueNotAllowedForDataTypeExc import InputDataValueNotAllowedForDataTypeExc
from datalidator.blueprints.exc.InputDataTypeNotInAllowlistExc import InputDataTypeNotInAllowlistExc
from datalidator.blueprints.exc.InputDataTypeInBlocklistExc import InputDataTypeInBlocklistExc
from datalidator.blueprints.exc.err.InvalidBlueprintConfigError import InvalidBlueprintConfigError
from datalidator.filters.impl.StringStripFilter import StringStripFilter
from datalidator.filters.impl.StringLowercaseFilter import StringLowercaseFilter
from datalidator.filters.impl.DatetimeAddTimezoneFilter import DatetimeAddTimezoneFilter
from datalidator.filters.impl.DatetimeChangeTimezoneFilter import DatetimeChangeTimezoneFilter
from datalidator.validators.impl.AllowlistValidator import AllowlistValidator
from datalidator.validators.impl.SequenceMinimumLengthValidator import SequenceMinimumLengthValidator
from datalidator.validators.impl.StringMatchesRegexValidator import StringMatchesRegexValidator
from datalidator.validators.impl.DatetimeNotAfterValidator import DatetimeNotAfterValidator
from datalidator.validators.impl.DatetimeNotBeforeValidator import DatetimeNotBeforeValidator
from datalidator.validators.exc.DataValidationFailedExc import DataValidationFailedExc


class GenericTestObjectModel(ObjectModel):
    __hidden1 = GenericBlueprint()
    _hidden2 = GenericBlueprint()
    __hidden3__ = GenericBlueprint()
    ignored1 = "hello world"
    ignored2 = theoretical_testutils.EmptyObject()

    item = StringBlueprint(parsing_mode=ParsingMode.MODE_STRICT)
    another_item = IntegerBlueprint(parsing_mode=ParsingMode.MODE_STRICT)
    third__item = OptionalItem(BooleanBlueprint(), False)
    list_variable_ = ListBlueprint(IPAddressBlueprint())
    datetime_variable__ = OptionalItem(DatetimeBlueprint(parsing_mode=ParsingMode.MODE_LOOSE), datetime.datetime(2025, 12, 15, 23, 45, 10, tzinfo=datetime.timezone.utc))


class RealUseCaseSimulationObjectModel(ObjectModel):
    username = StringBlueprint(
        filters=(StringStripFilter(),),
        validators=(StringMatchesRegexValidator(r'^[A-Za-z0-9]{3,15}\Z'),),
        parsing_mode=ParsingMode.MODE_STRICT
    )
    password = StringBlueprint(
        filters=(StringStripFilter(),),
        validators=(SequenceMinimumLengthValidator(8),),
        parsing_mode=ParsingMode.MODE_STRICT
    )
    email = StringBlueprint(
        filters=(StringStripFilter(), StringLowercaseFilter()),
        validators=(StringMatchesRegexValidator(r'^[a-z0-9.-]+@[a-z0-9.-]+\.[a-z]+\Z'),),
        parsing_mode=ParsingMode.MODE_STRICT
    )
    date_of_birth = DateBlueprint(DatetimeBlueprint(  
        additional_datetime_string_formats=("%Y-%m-%d",),
        filters=(DatetimeAddTimezoneFilter(datetime.timezone.utc), DatetimeChangeTimezoneFilter(datetime.timezone.utc)),
        validators=(DatetimeNotBeforeValidator(datetime.datetime(1900, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)), DatetimeNotAfterValidator(datetime.datetime(2019, 12, 31, 23, 59, 59, tzinfo=datetime.timezone.utc))),
        parsing_mode=ParsingMode.MODE_STRICT
    ))
    gender = OptionalItem(wrapped_blueprint=StringBlueprint(
        filters=(StringStripFilter(), StringLowercaseFilter()),
        validators=(AllowlistValidator(("male", "female", "other")),),
        parsing_mode=ParsingMode.MODE_STRICT
    ), default_value="other")


__OBJECT_BLUEPRINT_TEST_SUITE = (
    (ObjectBlueprint(GenericTestObjectModel, ignore_input_keys_which_are_not_in_model=True), (
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
            {"another_item": 456, "third__item": True, "list_variable_": ["127.1.2.3", "fe80::1234"], "datetime_variable__": "2001-01-15T07:08:04+01:00"},
            InvalidInputDataExc
        ),
        (
            {" item": "  hello world!\r\n", "another_item": 456, "third__item": True, "list_variable_": ["127.1.2.3", "fe80::1234"], "datetime_variable__": "2001-01-15T07:08:04+01:00"},
            InvalidInputDataExc
        ),
        (  
            {"item": "  hello world!\r\n", "another_item": 456, "third__item": True, "list_variable_": ["127.1.2.3", "fe80::1234"]},
            GenericTestObjectModel(item="  hello world!\r\n", another_item=456, third__item=True, list_variable_=[ipaddress.ip_address("127.1.2.3"), ipaddress.ip_address("fe80::1234")], datetime_variable__=datetime.datetime(2025, 12, 15, 23, 45, 10, tzinfo=datetime.timezone.utc))
        ),
        (
            {"item": "  hello world!\r\n", "another_item": 456, "third__item": True, "list_variable_": ["127.1.2.3", "fe80::1234"], "datetime_variable__\n": "2001-01-15T07:08:04+01:00"},
            GenericTestObjectModel(item="  hello world!\r\n", another_item=456, third__item=True, list_variable_=[ipaddress.ip_address("127.1.2.3"), ipaddress.ip_address("fe80::1234")], datetime_variable__=datetime.datetime(2025, 12, 15, 23, 45, 10, tzinfo=datetime.timezone.utc))
        ),
        (
            {"item": "  hello world!\r\n", "another_item": 456, "third__item": True, "list_variable_": ["127.1.2.3", "fe80::1234"], "datetime_variable__": "2001-01-15T07:08:04+01:00", "123": "def"},
            GenericTestObjectModel(item="  hello world!\r\n", another_item=456, third__item=True, list_variable_=[ipaddress.ip_address("127.1.2.3"), ipaddress.ip_address("fe80::1234")], datetime_variable__=datetime.datetime(2001, 1, 15, 7, 8, 4, tzinfo=zoneinfo.ZoneInfo("Europe/Prague")))
        ),
        (
            {"item": "  hello world!\r\n", "another_item": 456, "third__item": True, "list_variable_": ["127.1.2.3", "fe80::1234"], "datetime_variable__": "2001-01-15T07:08:04+01:00", "123": "def", ipaddress.ip_network("8.8.8.0/24"): True, object(): 888, (7, 8, 9): (1, 2, 3)},
            GenericTestObjectModel(item="  hello world!\r\n", another_item=456, third__item=True, list_variable_=[ipaddress.ip_address("127.1.2.3"), ipaddress.ip_address("fe80::1234")], datetime_variable__=datetime.datetime(2001, 1, 15, 7, 8, 4, tzinfo=zoneinfo.ZoneInfo("Europe/Prague")))
        ),
        (
            {"item": None, "another_item": 456, "third__item": True, "list_variable_": ["127.1.2.3", "fe80::1234"], "datetime_variable__": "2001-01-15T07:08:04+01:00"},
            InputDataTypeNotInAllowlistExc
        ),
        (
            {"item": "  hello world!\r\n", "another_item": 456.123, "third__item": True, "list_variable_": ["127.1.2.3", "fe80::1234"], "datetime_variable__": "2001-01-15T07:08:04+01:00"},
            InputDataTypeNotInAllowlistExc
        ),
        (
            {"item": "  hello world!\r\n", "another_item": 456, "third__item": theoretical_testutils.EmptyObject(), "list_variable_": ["127.1.2.3", "fe80::1234"], "datetime_variable__": "2001-01-15T07:08:04+01:00"},
            InputDataTypeNotInAllowlistExc
        ),
        (
            {"item": "  hello world!\r\n", "another_item": 456, "third__item": "hello", "list_variable_": ["127.1.2.3", "fe80::1234"], "datetime_variable__": "2001-01-15T07:08:04+01:00"},
            InputDataValueNotAllowedForDataTypeExc
        ),
        (
            {"item": "  hello world!\r\n", "another_item": 456, "third__item": True, "list_variable_": -123, "datetime_variable__": "2001-01-15T07:08:04+01:00"},
            InputDataNotConvertibleExc
        ),
        (
            {"item": "  hello world!\r\n", "another_item": 456, "third__item": True, "list_variable_": "-123", "datetime_variable__": "2001-01-15T07:08:04+01:00"},
            InputDataTypeInBlocklistExc
        ),
        (
            {"item": "  hello world!\r\n", "another_item": 456, "third__item": True, "list_variable_": ["127.1.2.3", "fe80x::1234"], "datetime_variable__": "2001-01-15T07:08:04+01:00"},
            InputDataNotConvertibleExc
        ),
        (
            {"item": "  hello world!\r\n", "another_item": 456, "third__item": True, "list_variable_": ["127.1.2.3", 123456], "datetime_variable__": "2001-01-15T07:08:04+01:00"},
            InputDataTypeNotInAllowlistExc
        ),
        (
            {"item": "  hello world!\r\n", "another_item": 456, "third__item": True, "list_variable_": ["127.1.2.3", "fe80::1234"], "datetime_variable__": "2001-01-\x0015T07:08:04+01:00"},
            InputDataNotConvertibleExc
        ),
        (
            {"item": "  hello world!\r\n", "another_item": 456, "third__item": True, "list_variable_": ["127.1.2.3", "fe80::1234"], "datetime_variable__": float("inf")},
            InputDataNotConvertibleExc
        ),
        (
            {"item": "  hello world!\r\n", "another_item": 456, "third__item": True, "list_variable_": ["127.1.2.3", "fe80::1234"], "datetime_variable__": theoretical_testutils.EmptyObject()},
            InputDataTypeNotInAllowlistExc
        ),
        (  
            {"item": "  hello world!\r\n", "another_item": 456, "third__item": True, "list_variable_": ["127.1.2.3", "fe80::1234"], "datetime_variable__": "2001-01-15T07:08:04+01:00"},
            GenericTestObjectModel(item="  hello world!\r\n", another_item=456, third__item=True, list_variable_=[ipaddress.ip_address("127.1.2.3"), ipaddress.ip_address("fe80::1234")], datetime_variable__=datetime.datetime(2001, 1, 15, 7, 8, 4, tzinfo=zoneinfo.ZoneInfo("Europe/Prague")))
        ),
        (  
            {"item": "  hello\t\t  world!\r\n", "another_item": -321, "third__item": "\r\n  TrUe\t\t\f   ", "list_variable_": [ipaddress.ip_address("127.3.2.1"), "fe80:0000:0::0789"], "datetime_variable__": datetime.date(2008, 8, 4)},
            GenericTestObjectModel(item="  hello\t\t  world!\r\n", another_item=-321, third__item=True, list_variable_=[ipaddress.ip_address("127.3.2.1"), ipaddress.ip_address("fe80::789")], datetime_variable__=datetime.datetime(2008, 8, 4, 0, 0, 0))
        ),
        (  
            {"item": "  hello\t\t  world!\r\n", "another_item": -321, "list_variable_": [ipaddress.ip_address("127.3.2.1"), "fe80:0000:0::0789"]},
            GenericTestObjectModel(item="  hello\t\t  world!\r\n", another_item=-321, third__item=False, list_variable_=[ipaddress.ip_address("127.3.2.1"), ipaddress.ip_address("fe80::789")], datetime_variable__=datetime.datetime(2025, 12, 15, 23, 45, 10, tzinfo=datetime.timezone.utc))
        ),
        (
            {"extra": True, "item": "  hello\t\t  world!\r\n", "another_item": -321, "third__item": "\r\n  TrUe\t\t\f   ", "list_variable_": [ipaddress.ip_address("127.3.2.1"), "fe80:0000:0::0789"], "datetime_variable__": datetime.date(2008, 8, 4)},
            GenericTestObjectModel(item="  hello\t\t  world!\r\n", another_item=-321, third__item=True, list_variable_=[ipaddress.ip_address("127.3.2.1"), ipaddress.ip_address("fe80::789")], datetime_variable__=datetime.datetime(2008, 8, 4, 0, 0, 0))
        ),
        (
            {"extra": True, 8+6j: "foobar", "item": "  hello\t\t  world!\r\n", "another_item": -321, "third__item": "\r\n  TrUe\t\t\f   ", "list_variable_": [ipaddress.ip_address("127.3.2.1"), "fe80:0000:0::0789"], "datetime_variable__": datetime.date(2008, 8, 4)},
            GenericTestObjectModel(item="  hello\t\t  world!\r\n", another_item=-321, third__item=True, list_variable_=[ipaddress.ip_address("127.3.2.1"), ipaddress.ip_address("fe80::789")], datetime_variable__=datetime.datetime(2008, 8, 4, 0, 0, 0))
        ),
    )),
    (ObjectBlueprint(GenericTestObjectModel, ignore_input_keys_which_are_not_in_model=False), (
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
            {"another_item": 456, "third__item": True, "list_variable_": ["127.1.2.3", "fe80::1234"], "datetime_variable__": "2001-01-15T07:08:04+01:00"},
            InvalidInputDataExc
        ),
        (
            {" item": "  hello world!\r\n", "another_item": 456, "third__item": True, "list_variable_": ["127.1.2.3", "fe80::1234"], "datetime_variable__": "2001-01-15T07:08:04+01:00"},
            InvalidInputDataExc
        ),
        (  
            {"item": "  hello world!\r\n", "another_item": 456, "third__item": True, "list_variable_": ["127.1.2.3", "fe80::1234"]},
            GenericTestObjectModel(item="  hello world!\r\n", another_item=456, third__item=True, list_variable_=[ipaddress.ip_address("127.1.2.3"), ipaddress.ip_address("fe80::1234")], datetime_variable__=datetime.datetime(2025, 12, 15, 23, 45, 10, tzinfo=datetime.timezone.utc))
        ),
        (
            {"item": "  hello world!\r\n", "another_item": 456, "third__item": True, "list_variable_": ["127.1.2.3", "fe80::1234"], "datetime_variable__\n": "2001-01-15T07:08:04+01:00"},
            InvalidInputDataExc
        ),
        (
            {"item": "  hello world!\r\n", "another_item": 456, "third__item": True, "list_variable_": ["127.1.2.3", "fe80::1234"], "datetime_variable__": "2001-01-15T07:08:04+01:00", "123": "def"},
            InvalidInputDataExc
        ),
        (
            {"item": "  hello world!\r\n", "another_item": 456, "third__item": True, "list_variable_": ["127.1.2.3", "fe80::1234"], "datetime_variable__": "2001-01-15T07:08:04+01:00", "123": "def", ipaddress.ip_network("8.8.8.0/24"): True, object(): 888, (7, 8, 9): (1, 2, 3)},
            InvalidInputDataExc
        ),
        (
            {"item": None, "another_item": 456, "third__item": True, "list_variable_": ["127.1.2.3", "fe80::1234"], "datetime_variable__": "2001-01-15T07:08:04+01:00"},
            InputDataTypeNotInAllowlistExc
        ),
        (
            {"item": "  hello world!\r\n", "another_item": 456.123, "third__item": True, "list_variable_": ["127.1.2.3", "fe80::1234"], "datetime_variable__": "2001-01-15T07:08:04+01:00"},
            InputDataTypeNotInAllowlistExc
        ),
        (
            {"item": "  hello world!\r\n", "another_item": 456, "third__item": theoretical_testutils.EmptyObject(), "list_variable_": ["127.1.2.3", "fe80::1234"], "datetime_variable__": "2001-01-15T07:08:04+01:00"},
            InputDataTypeNotInAllowlistExc
        ),
        (
            {"item": "  hello world!\r\n", "another_item": 456, "third__item": "hello", "list_variable_": ["127.1.2.3", "fe80::1234"], "datetime_variable__": "2001-01-15T07:08:04+01:00"},
            InputDataValueNotAllowedForDataTypeExc
        ),
        (
            {"item": "  hello world!\r\n", "another_item": 456, "third__item": True, "list_variable_": -123, "datetime_variable__": "2001-01-15T07:08:04+01:00"},
            InputDataNotConvertibleExc
        ),
        (
            {"item": "  hello world!\r\n", "another_item": 456, "third__item": True, "list_variable_": "-123", "datetime_variable__": "2001-01-15T07:08:04+01:00"},
            InputDataTypeInBlocklistExc
        ),
        (
            {"item": "  hello world!\r\n", "another_item": 456, "third__item": True, "list_variable_": ["127.1.2.3", "fe80x::1234"], "datetime_variable__": "2001-01-15T07:08:04+01:00"},
            InputDataNotConvertibleExc
        ),
        (
            {"item": "  hello world!\r\n", "another_item": 456, "third__item": True, "list_variable_": ["127.1.2.3", 123456], "datetime_variable__": "2001-01-15T07:08:04+01:00"},
            InputDataTypeNotInAllowlistExc
        ),
        (
            {"item": "  hello world!\r\n", "another_item": 456, "third__item": True, "list_variable_": ["127.1.2.3", "fe80::1234"], "datetime_variable__": "2001-01-\x0015T07:08:04+01:00"},
            InputDataNotConvertibleExc
        ),
        (
            {"item": "  hello world!\r\n", "another_item": 456, "third__item": True, "list_variable_": ["127.1.2.3", "fe80::1234"], "datetime_variable__": float("inf")},
            InputDataNotConvertibleExc
        ),
        (
            {"item": "  hello world!\r\n", "another_item": 456, "third__item": True, "list_variable_": ["127.1.2.3", "fe80::1234"], "datetime_variable__": theoretical_testutils.EmptyObject()},
            InputDataTypeNotInAllowlistExc
        ),
        (  
            {"item": "  hello world!\r\n", "another_item": 456, "third__item": True, "list_variable_": ["127.1.2.3", "fe80::1234"], "datetime_variable__": "2001-01-15T07:08:04+01:00"},
            GenericTestObjectModel(item="  hello world!\r\n", another_item=456, third__item=True, list_variable_=[ipaddress.ip_address("127.1.2.3"), ipaddress.ip_address("fe80::1234")], datetime_variable__=datetime.datetime(2001, 1, 15, 7, 8, 4, tzinfo=zoneinfo.ZoneInfo("Europe/Prague")))
        ),
        (  
            {"item": "  hello\t\t  world!\r\n", "another_item": -321, "third__item": "\r\n  TrUe\t\t\f   ", "list_variable_": [ipaddress.ip_address("127.3.2.1"), "fe80:0000:0::0789"], "datetime_variable__": datetime.date(2008, 8, 4)},
            GenericTestObjectModel(item="  hello\t\t  world!\r\n", another_item=-321, third__item=True, list_variable_=[ipaddress.ip_address("127.3.2.1"), ipaddress.ip_address("fe80::789")], datetime_variable__=datetime.datetime(2008, 8, 4, 0, 0, 0))
        ),
        (  
            {"item": "  hello\t\t  world!\r\n", "another_item": -321, "list_variable_": [ipaddress.ip_address("127.3.2.1"), "fe80:0000:0::0789"]},
            GenericTestObjectModel(item="  hello\t\t  world!\r\n", another_item=-321, third__item=False, list_variable_=[ipaddress.ip_address("127.3.2.1"), ipaddress.ip_address("fe80::789")], datetime_variable__=datetime.datetime(2025, 12, 15, 23, 45, 10, tzinfo=datetime.timezone.utc))
        ),
        (
            {"extra": True, "item": "  hello\t\t  world!\r\n", "another_item": -321, "third__item": "\r\n  TrUe\t\t\f   ", "list_variable_": [ipaddress.ip_address("127.3.2.1"), "fe80:0000:0::0789"], "datetime_variable__": datetime.date(2008, 8, 4)},
            InvalidInputDataExc
        ),
        (
            {"extra": True, 8+6j: "foobar", "item": "  hello\t\t  world!\r\n", "another_item": -321, "third__item": "\r\n  TrUe\t\t\f   ", "list_variable_": [ipaddress.ip_address("127.3.2.1"), "fe80:0000:0::0789"], "datetime_variable__": datetime.date(2008, 8, 4)},
            InvalidInputDataExc
        ),
    )),
    (ObjectBlueprint(RealUseCaseSimulationObjectModel, ignore_input_keys_which_are_not_in_model=True), (
        ([["username", "test"], ["password", "123456789"], ["email"], ["date_of_birth", "1995-06-20"], ["gender", "female"]], InputDataNotConvertibleExc),
        ([["username", "test"], ["password", "123456789"], ["email", "nobody@example.com", "!!!"], ["date_of_birth", "1995-06-20"], ["gender", "female"]], InputDataNotConvertibleExc),
        (
            [["username", "test"], ["password", "123456789"], ["email", "nobody@example.com"], ["date_of_birth", "1995-06-20"], ["gender", "female"]],
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
        ),
        ({"password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"}, InvalidInputDataExc),
        ({"username ": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"}, InvalidInputDataExc),
        ({"username": "test", "password": "123456789", "email": "nobody@example.com", "gender": "female"}, InvalidInputDataExc),
        ({"username": "test", "password": "123456789", "email": "nobody@example.com", "\ndate_of_birth": "1995-06-20", "gender": "female"}, InvalidInputDataExc),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20"},
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="other"),
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender_": "female"},
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="other"),
        ),
        (
            {"something": "else", "username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
        ),
        (
            {"something": "else", ipaddress.ip_address("127.0.0.1"): 123, "username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
        ),
        (
            {"something": "else", object(): theoretical_testutils.EmptyObject(), "username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
        ),
        (
            {"username": "\n  \r\v   test\f\f", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
        ),
        (
            {"username": "test\n", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
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
            RealUseCaseSimulationObjectModel(username="tes", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
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
            RealUseCaseSimulationObjectModel(username="012345678901234", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
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
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
        ),
        (
            {"username": "test", "password": "12345678", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            RealUseCaseSimulationObjectModel(username="test", password="12345678", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
        ),
        (
            {"username": "test", "password": "\t\f  \r\n1234567     ", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            DataValidationFailedExc
        ),
        (
            {"username": "test", "password": "  \t ěřš čř ěšč ř qwřč ěšč\nř+š \v\f\tč ěšč ř+ě ššč +ě šč+ ě š žčřě  čšě + ěšč +ěš č+ě   \t\r", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            RealUseCaseSimulationObjectModel(username="test", password="ěřš čř ěšč ř qwřč ěšč\nř+š \v\f\tč ěšč ř+ě ššč +ě šč+ ě š žčřě  čšě + ěšč +ěš č+ě", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
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
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
        ),
        (
            {"username": "test", "password": "123456789", "email": "no-bo.dy@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="no-bo.dy@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
        ),
        (
            {"username": "test", "password": "123456789", "email": "NOBODY@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@EXAMPLE.com", "date_of_birth": "1995-06-20", "gender": "female"},
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
        ),
        (
            {"username": "test", "password": "123456789", "email": "NOboDY@EXAMPLE.COm", "date_of_birth": "1995-06-20", "gender": "female"},
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
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
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@server.example.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@exa-mple.com", "date_of_birth": "1995-06-20", "gender": "female"},
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@exa-mple.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
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
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
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
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20T12:45:50+06:00", "gender": "female"},
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20T12:45:50.112233-08:00", "gender": "female"},
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-\x0020", "gender": "female"},
            InputDataNotConvertibleExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1900-01-01", "gender": "female"},
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1900, 1, 1), gender="female"),
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1899-12-31", "gender": "female"},
            DataValidationFailedExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "2019-12-31", "gender": "female"},
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(2019, 12, 31), gender="female"),
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "2020-01-01", "gender": "female"},
            DataValidationFailedExc
        ),
        (  
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.datetime(1995, 6, 20, 15, 23, 45), "gender": "female"},
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
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
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "\r\n   fEMaLe   \v\f "},
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "\r\n   MaLe   \v\f "},
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="male"),
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "\r\n   OTHeR   \v\f "},
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="other"),
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
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="other"),
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
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", 123: True, ipaddress.ip_network("127.0.0.0/8"): 8+2j},
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="other"),
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
    (ObjectBlueprint(RealUseCaseSimulationObjectModel, ignore_input_keys_which_are_not_in_model=False), (
        ([["username", "test"], ["password", "123456789"], ["email"], ["date_of_birth", "1995-06-20"], ["gender", "female"]], InputDataNotConvertibleExc),
        ([["username", "test"], ["password", "123456789"], ["email", "nobody@example.com", "!!!"], ["date_of_birth", "1995-06-20"], ["gender", "female"]], InputDataNotConvertibleExc),
        (
            [["username", "test"], ["password", "123456789"], ["email", "nobody@example.com"], ["date_of_birth", "1995-06-20"], ["gender", "female"]],
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
        ),
        ({"password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"}, InvalidInputDataExc),
        ({"username ": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"}, InvalidInputDataExc),
        ({"username": "test", "password": "123456789", "email": "nobody@example.com", "gender": "female"}, InvalidInputDataExc),
        ({"username": "test", "password": "123456789", "email": "nobody@example.com", "\ndate_of_birth": "1995-06-20", "gender": "female"}, InvalidInputDataExc),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20"},
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="other"),
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
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
        ),
        (
            {"username": "test\n", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
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
            RealUseCaseSimulationObjectModel(username="tes", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
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
            RealUseCaseSimulationObjectModel(username="012345678901234", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
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
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
        ),
        (
            {"username": "test", "password": "12345678", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            RealUseCaseSimulationObjectModel(username="test", password="12345678", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
        ),
        (
            {"username": "test", "password": "\t\f  \r\n1234567     ", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            DataValidationFailedExc
        ),
        (
            {"username": "test", "password": "  \t ěřš čř ěšč ř qwřč ěšč\nř+š \v\f\tč ěšč ř+ě ššč +ě šč+ ě š žčřě  čšě + ěšč +ěš č+ě   \t\r", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            RealUseCaseSimulationObjectModel(username="test", password="ěřš čř ěšč ř qwřč ěšč\nř+š \v\f\tč ěšč ř+ě ššč +ě šč+ ě š žčřě  čšě + ěšč +ěš č+ě", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
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
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
        ),
        (
            {"username": "test", "password": "123456789", "email": "no-bo.dy@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="no-bo.dy@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
        ),
        (
            {"username": "test", "password": "123456789", "email": "NOBODY@example.com", "date_of_birth": "1995-06-20", "gender": "female"},
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@EXAMPLE.com", "date_of_birth": "1995-06-20", "gender": "female"},
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
        ),
        (
            {"username": "test", "password": "123456789", "email": "NOboDY@EXAMPLE.COm", "date_of_birth": "1995-06-20", "gender": "female"},
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
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
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@server.example.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@exa-mple.com", "date_of_birth": "1995-06-20", "gender": "female"},
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@exa-mple.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
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
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
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
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20T12:45:50+06:00", "gender": "female"},
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20T12:45:50.112233-08:00", "gender": "female"},
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-\x0020", "gender": "female"},
            InputDataNotConvertibleExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1900-01-01", "gender": "female"},
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1900, 1, 1), gender="female"),
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1899-12-31", "gender": "female"},
            DataValidationFailedExc
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "2019-12-31", "gender": "female"},
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(2019, 12, 31), gender="female"),
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "2020-01-01", "gender": "female"},
            DataValidationFailedExc
        ),
        (  
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": datetime.datetime(1995, 6, 20, 15, 23, 45), "gender": "female"},
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
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
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "\r\n   fEMaLe   \v\f "},
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="female"),
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "\r\n   MaLe   \v\f "},
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="male"),
        ),
        (
            {"username": "test", "password": "123456789", "email": "nobody@example.com", "date_of_birth": "1995-06-20", "gender": "\r\n   OTHeR   \v\f "},
            RealUseCaseSimulationObjectModel(username="test", password="123456789", email="nobody@example.com", date_of_birth=datetime.date(1995, 6, 20), gender="other"),
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


@pytest.mark.parametrize(("blueprint", "input_", "output"), theoretical_testutils.test_function_parameter_generator(__OBJECT_BLUEPRINT_TEST_SUITE))
def test_object_blueprint(blueprint, input_, output):
    theoretical_testutils.perform_test(blueprint, input_, output)


def test_object_blueprint_object_model():
    class __TestObjectModel(ObjectModel):
        item = GenericBlueprint()

    assert ObjectBlueprint(__TestObjectModel).get_object_model() is __TestObjectModel


def test_object_blueprint_empty_object_model():
    class __EmptyObjectModel(ObjectModel):
        pass

    with pytest.raises(InvalidBlueprintConfigError):
        ObjectBlueprint(__EmptyObjectModel)


def test_object_blueprint_effectively_empty_object_model():
    class __EffectivelyEmptyObjectModel(ObjectModel):
        __hidden1 = GenericBlueprint()
        _hidden2 = GenericBlueprint()
        ignored1 = "test"
        ignored2 = 123.456

    with pytest.raises(InvalidBlueprintConfigError):
        ObjectBlueprint(__EffectivelyEmptyObjectModel)


def test_object_blueprint_default_ignore_input_keys_which_are_not_in_model():
    class __TestObjectModel(ObjectModel):
        item = GenericBlueprint()

    assert ObjectBlueprint(__TestObjectModel).are_input_keys_which_are_not_in_model_ignored() is True


def test_object_blueprint_ignore_input_keys_which_are_not_in_model():
    class __TestObjectModel(ObjectModel):
        item = GenericBlueprint()

    assert ObjectBlueprint(__TestObjectModel, ignore_input_keys_which_are_not_in_model=False).are_input_keys_which_are_not_in_model_ignored() is False
