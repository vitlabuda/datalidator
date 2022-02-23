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
import ipaddress
import urllib.parse
import uuid
from datalidator.blueprints.ParsingMode import ParsingMode
from datalidator.blueprints.impl.IntegerBlueprint import IntegerBlueprint
from datalidator.blueprints.exc.InputDataTypeNotInAllowlistExc import InputDataTypeNotInAllowlistExc
from datalidator.blueprints.exc.InputDataNotConvertibleExc import InputDataNotConvertibleExc
from datalidator.blueprints.exc.UnexpectedOutputDataTypeExc import UnexpectedOutputDataTypeExc
from datalidator.filters.impl.NumberAbsoluteValueFilter import NumberAbsoluteValueFilter
from datalidator.filters.impl.NumberMaximumClampFilter import NumberMaximumClampFilter
from datalidator.filters.impl.NumberMinimumClampFilter import NumberMinimumClampFilter
from datalidator.filters.impl.NumberRoundFilter import NumberRoundFilter
from datalidator.validators.impl.IntegerIsPositiveValidator import IntegerIsPositiveValidator
from datalidator.validators.impl.IntegerIsZeroOrPositiveValidator import IntegerIsZeroOrPositiveValidator
from datalidator.validators.impl.NumberMaximumValueValidator import NumberMaximumValueValidator
from datalidator.validators.impl.NumberMinimumValueValidator import NumberMinimumValueValidator
from datalidator.validators.exc.DataValidationFailedExc import DataValidationFailedExc


# Because for example: 0 == 0.0 == -0.0
def expected_output_int_value(value: str):  # DP: Factory
    return lambda output: (output.__class__ is int) and (str(output) == value)


class IntableObject:
    def __init__(self, returned_value):
        self.__returned_value = returned_value

    def __int__(self):
        return self.__returned_value


class ExceptionRaisingIntableObject:
    def __int__(self):
        raise theoretical_testutils.TestException()


__INTEGER_BLUEPRINT_TEST_SUITE = (
    (IntegerBlueprint(parsing_mode=ParsingMode.MODE_LOOSE), (
        (0, expected_output_int_value("0")),
        (-0, expected_output_int_value("0")),
        (1, expected_output_int_value("1")),
        (-1, expected_output_int_value("-1")),
        (123, expected_output_int_value("123")),
        (-123, expected_output_int_value("-123")),
        (0.0, expected_output_int_value("0")),
        (-0.0, expected_output_int_value("0")),
        (1.0, expected_output_int_value("1")),
        (-1.0, expected_output_int_value("-1")),
        (123.456, expected_output_int_value("123")),
        (-123.456, expected_output_int_value("-123")),
        (float("inf"), InputDataNotConvertibleExc),
        (float("-inf"), InputDataNotConvertibleExc),
        (float("nan"), InputDataNotConvertibleExc),
        (float("-nan"), InputDataNotConvertibleExc),
        (True, expected_output_int_value("1")),
        (False, expected_output_int_value("0")),
        ("0", expected_output_int_value("0")),
        ("+0", expected_output_int_value("0")),
        ("-0", expected_output_int_value("0")),
        ("1", expected_output_int_value("1")),
        ("+1", expected_output_int_value("1")),
        ("-1", expected_output_int_value("-1")),
        ("123", expected_output_int_value("123")),
        ("+123", expected_output_int_value("123")),
        ("-123", expected_output_int_value("-123")),
        ("000123", expected_output_int_value("123")),
        ("+000123", expected_output_int_value("123")),
        ("-000123", expected_output_int_value("-123")),
        ("123_456", expected_output_int_value("123456")),
        ("+123_456", expected_output_int_value("123456")),
        ("-123_456", expected_output_int_value("-123456")),
        ("0b111", InputDataNotConvertibleExc),
        ("0x111", InputDataNotConvertibleExc),
        ("0o111", InputDataNotConvertibleExc),
        ("0.0", InputDataNotConvertibleExc),
        ("+0.0", InputDataNotConvertibleExc),
        ("-0.0", InputDataNotConvertibleExc),
        ("1.0", InputDataNotConvertibleExc),
        ("+1.0", InputDataNotConvertibleExc),
        ("-1.0", InputDataNotConvertibleExc),
        ("123.456", InputDataNotConvertibleExc),
        ("+123.456", InputDataNotConvertibleExc),
        ("-123.456", InputDataNotConvertibleExc),
        ("123.456", InputDataNotConvertibleExc),
        ("+123.456", InputDataNotConvertibleExc),
        ("-123.456", InputDataNotConvertibleExc),
        ("1e6", InputDataNotConvertibleExc),
        ("+1e6", InputDataNotConvertibleExc),
        ("-1e6", InputDataNotConvertibleExc),
        ("inf", InputDataNotConvertibleExc),
        ("+inf", InputDataNotConvertibleExc),
        ("-inf", InputDataNotConvertibleExc),
        ("nan", InputDataNotConvertibleExc),
        ("+nan", InputDataNotConvertibleExc),
        ("-nan", InputDataNotConvertibleExc),
        ("   456\t\t", expected_output_int_value("456")),
        ("\r\n789\v", expected_output_int_value("789")),
        ("123a456", InputDataNotConvertibleExc),
        ("a123456", InputDataNotConvertibleExc),
        ("123456a", InputDataNotConvertibleExc),
        ("123\x00456", InputDataNotConvertibleExc),
        ("\x00123456", InputDataNotConvertibleExc),
        ("123456\x00", InputDataNotConvertibleExc),
        ("\x00", InputDataNotConvertibleExc),
        ("", InputDataNotConvertibleExc),
        ("hello", InputDataNotConvertibleExc),
        ("   \t Hello World\f", InputDataNotConvertibleExc),
        ("\r fasdasfqwe\v\vf fsadf   \r\nqw    ", InputDataNotConvertibleExc),
        ([], InputDataNotConvertibleExc),
        ({}, InputDataNotConvertibleExc),
        ([1, 2], InputDataNotConvertibleExc),
        ({1: 2}, InputDataNotConvertibleExc),
        (None, InputDataNotConvertibleExc),
        (b'', InputDataNotConvertibleExc),
        (b'\x00', InputDataNotConvertibleExc),
        (b'\x01', InputDataNotConvertibleExc),
        (b'123789', expected_output_int_value("123789")),
        (b'+123789', expected_output_int_value("123789")),
        (b'-123789', expected_output_int_value("-123789")),
        (b'123.789', InputDataNotConvertibleExc),
        (bytearray(b'444555'), expected_output_int_value("444555")),
        (int, InputDataNotConvertibleExc),
        (theoretical_testutils.EmptyObject, InputDataNotConvertibleExc),
        (datetime.datetime.now(), InputDataNotConvertibleExc),
        (datetime.datetime.now().date(), InputDataNotConvertibleExc),
        (datetime.datetime.now().time(), InputDataNotConvertibleExc),
        (ipaddress.ip_address("127.1.2.3"), expected_output_int_value("2130772483")),
        (ipaddress.ip_address("::1"), expected_output_int_value("1")),
        (ipaddress.ip_network("127.0.0.0/8"), InputDataNotConvertibleExc),
        (ipaddress.ip_network("2001:db8::/32"), InputDataNotConvertibleExc),
        (urllib.parse.urlparse("https://www.google.com/test"), InputDataNotConvertibleExc),
        (uuid.UUID('{12345678-1234-5678-1234-567812345678}'), expected_output_int_value("24197857161011715162171839636988778104")),
        (theoretical_testutils.EmptyObject(), InputDataNotConvertibleExc),
        (IntableObject(333222), expected_output_int_value("333222")),
        (IntableObject(333222.111), InputDataNotConvertibleExc),
        # (IntableObject(True), expected_output_int_value("1")),  # Raises DeprecationWarning! (For historic reasons, 'bool' is a subclass of 'int'.)
        # (IntableObject(False), expected_output_int_value("0")),  # Raises DeprecationWarning!  (For historic reasons, 'bool' is a subclass of 'int'.)
        (IntableObject("333222"), InputDataNotConvertibleExc),
        (IntableObject(None), InputDataNotConvertibleExc),
        (IntableObject(theoretical_testutils.EmptyObject()), InputDataNotConvertibleExc),
        (ExceptionRaisingIntableObject(), InputDataNotConvertibleExc)
    )),
    (IntegerBlueprint(parsing_mode=ParsingMode.MODE_RATIONAL), (
        (0, expected_output_int_value("0")),
        (-0, expected_output_int_value("0")),
        (1, expected_output_int_value("1")),
        (-1, expected_output_int_value("-1")),
        (123, expected_output_int_value("123")),
        (-123, expected_output_int_value("-123")),
        (0.0, expected_output_int_value("0")),
        (-0.0, expected_output_int_value("0")),
        (1.0, expected_output_int_value("1")),
        (-1.0, expected_output_int_value("-1")),
        (123.456, expected_output_int_value("123")),
        (-123.456, expected_output_int_value("-123")),
        (float("inf"), InputDataNotConvertibleExc),
        (float("-inf"), InputDataNotConvertibleExc),
        (float("nan"), InputDataNotConvertibleExc),
        (float("-nan"), InputDataNotConvertibleExc),
        (True, expected_output_int_value("1")),
        (False, expected_output_int_value("0")),
        ("0", expected_output_int_value("0")),
        ("+0", expected_output_int_value("0")),
        ("-0", expected_output_int_value("0")),
        ("1", expected_output_int_value("1")),
        ("+1", expected_output_int_value("1")),
        ("-1", expected_output_int_value("-1")),
        ("123", expected_output_int_value("123")),
        ("+123", expected_output_int_value("123")),
        ("-123", expected_output_int_value("-123")),
        ("000123", expected_output_int_value("123")),
        ("+000123", expected_output_int_value("123")),
        ("-000123", expected_output_int_value("-123")),
        ("123_456", expected_output_int_value("123456")),
        ("+123_456", expected_output_int_value("123456")),
        ("-123_456", expected_output_int_value("-123456")),
        ("0b111", InputDataNotConvertibleExc),
        ("0x111", InputDataNotConvertibleExc),
        ("0o111", InputDataNotConvertibleExc),
        ("0.0", InputDataNotConvertibleExc),
        ("+0.0", InputDataNotConvertibleExc),
        ("-0.0", InputDataNotConvertibleExc),
        ("1.0", InputDataNotConvertibleExc),
        ("+1.0", InputDataNotConvertibleExc),
        ("-1.0", InputDataNotConvertibleExc),
        ("123.456", InputDataNotConvertibleExc),
        ("+123.456", InputDataNotConvertibleExc),
        ("-123.456", InputDataNotConvertibleExc),
        ("123.456", InputDataNotConvertibleExc),
        ("+123.456", InputDataNotConvertibleExc),
        ("-123.456", InputDataNotConvertibleExc),
        ("1e6", InputDataNotConvertibleExc),
        ("+1e6", InputDataNotConvertibleExc),
        ("-1e6", InputDataNotConvertibleExc),
        ("inf", InputDataNotConvertibleExc),
        ("+inf", InputDataNotConvertibleExc),
        ("-inf", InputDataNotConvertibleExc),
        ("nan", InputDataNotConvertibleExc),
        ("+nan", InputDataNotConvertibleExc),
        ("-nan", InputDataNotConvertibleExc),
        ("   456\t\t", expected_output_int_value("456")),
        ("\r\n789\v", expected_output_int_value("789")),
        ("123a456", InputDataNotConvertibleExc),
        ("a123456", InputDataNotConvertibleExc),
        ("123456a", InputDataNotConvertibleExc),
        ("123\x00456", InputDataNotConvertibleExc),
        ("\x00123456", InputDataNotConvertibleExc),
        ("123456\x00", InputDataNotConvertibleExc),
        ("\x00", InputDataNotConvertibleExc),
        ("", InputDataNotConvertibleExc),
        ("hello", InputDataNotConvertibleExc),
        ("   \t Hello World\f", InputDataNotConvertibleExc),
        ("\r fasdasfqwe\v\vf fsadf   \r\nqw    ", InputDataNotConvertibleExc),
        ([], InputDataTypeNotInAllowlistExc),
        ({}, InputDataTypeNotInAllowlistExc),
        ([1, 2], InputDataTypeNotInAllowlistExc),
        ({1: 2}, InputDataTypeNotInAllowlistExc),
        (None, InputDataTypeNotInAllowlistExc),
        (b'', InputDataTypeNotInAllowlistExc),
        (b'\x00', InputDataTypeNotInAllowlistExc),
        (b'\x01', InputDataTypeNotInAllowlistExc),
        (b'123789', InputDataTypeNotInAllowlistExc),
        (b'+123789', InputDataTypeNotInAllowlistExc),
        (b'-123789', InputDataTypeNotInAllowlistExc),
        (b'123.789', InputDataTypeNotInAllowlistExc),
        (bytearray(b'444555'), InputDataTypeNotInAllowlistExc),
        (int, InputDataTypeNotInAllowlistExc),
        (theoretical_testutils.EmptyObject, InputDataTypeNotInAllowlistExc),
        (datetime.datetime.now(), InputDataTypeNotInAllowlistExc),
        (datetime.datetime.now().date(), InputDataTypeNotInAllowlistExc),
        (datetime.datetime.now().time(), InputDataTypeNotInAllowlistExc),
        (ipaddress.ip_address("127.1.2.3"), InputDataTypeNotInAllowlistExc),
        (ipaddress.ip_address("::1"), InputDataTypeNotInAllowlistExc),
        (ipaddress.ip_network("127.0.0.0/8"), InputDataTypeNotInAllowlistExc),
        (ipaddress.ip_network("2001:db8::/32"), InputDataTypeNotInAllowlistExc),
        (urllib.parse.urlparse("https://www.google.com/test"), InputDataTypeNotInAllowlistExc),
        (uuid.UUID('{12345678-1234-5678-1234-567812345678}'), InputDataTypeNotInAllowlistExc),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc),
        (IntableObject(333222), InputDataTypeNotInAllowlistExc),
        (IntableObject(333222.111), InputDataTypeNotInAllowlistExc),
        (IntableObject(True), InputDataTypeNotInAllowlistExc),
        (IntableObject(False), InputDataTypeNotInAllowlistExc),
        (IntableObject("333222"), InputDataTypeNotInAllowlistExc),
        (IntableObject(None), InputDataTypeNotInAllowlistExc),
        (IntableObject(theoretical_testutils.EmptyObject()), InputDataTypeNotInAllowlistExc),
        (ExceptionRaisingIntableObject(), InputDataTypeNotInAllowlistExc)
    )),
    (IntegerBlueprint(parsing_mode=ParsingMode.MODE_STRICT), (
        (0, expected_output_int_value("0")),
        (-0, expected_output_int_value("0")),
        (1, expected_output_int_value("1")),
        (-1, expected_output_int_value("-1")),
        (123, expected_output_int_value("123")),
        (-123, expected_output_int_value("-123")),
        (0.0, InputDataTypeNotInAllowlistExc),
        (-0.0, InputDataTypeNotInAllowlistExc),
        (1.0, InputDataTypeNotInAllowlistExc),
        (-1.0, InputDataTypeNotInAllowlistExc),
        (123.456, InputDataTypeNotInAllowlistExc),
        (-123.456, InputDataTypeNotInAllowlistExc),
        (float("inf"), InputDataTypeNotInAllowlistExc),
        (float("-inf"), InputDataTypeNotInAllowlistExc),
        (float("nan"), InputDataTypeNotInAllowlistExc),
        (float("-nan"), InputDataTypeNotInAllowlistExc),
        (True, expected_output_int_value("1")),  # For historic reasons, 'bool' is a subclass of 'int'.
        (False, expected_output_int_value("0")),  # For historic reasons, 'bool' is a subclass of 'int'.
        ("0", InputDataTypeNotInAllowlistExc),
        ("+0", InputDataTypeNotInAllowlistExc),
        ("-0", InputDataTypeNotInAllowlistExc),
        ("1", InputDataTypeNotInAllowlistExc),
        ("+1", InputDataTypeNotInAllowlistExc),
        ("-1", InputDataTypeNotInAllowlistExc),
        ("123", InputDataTypeNotInAllowlistExc),
        ("+123", InputDataTypeNotInAllowlistExc),
        ("-123", InputDataTypeNotInAllowlistExc),
        ("000123", InputDataTypeNotInAllowlistExc),
        ("+000123", InputDataTypeNotInAllowlistExc),
        ("-000123", InputDataTypeNotInAllowlistExc),
        ("123_456", InputDataTypeNotInAllowlistExc),
        ("+123_456", InputDataTypeNotInAllowlistExc),
        ("-123_456", InputDataTypeNotInAllowlistExc),
        ("0b111", InputDataTypeNotInAllowlistExc),
        ("0x111", InputDataTypeNotInAllowlistExc),
        ("0o111", InputDataTypeNotInAllowlistExc),
        ("0.0", InputDataTypeNotInAllowlistExc),
        ("+0.0", InputDataTypeNotInAllowlistExc),
        ("-0.0", InputDataTypeNotInAllowlistExc),
        ("1.0", InputDataTypeNotInAllowlistExc),
        ("+1.0", InputDataTypeNotInAllowlistExc),
        ("-1.0", InputDataTypeNotInAllowlistExc),
        ("123.456", InputDataTypeNotInAllowlistExc),
        ("+123.456", InputDataTypeNotInAllowlistExc),
        ("-123.456", InputDataTypeNotInAllowlistExc),
        ("123.456", InputDataTypeNotInAllowlistExc),
        ("+123.456", InputDataTypeNotInAllowlistExc),
        ("-123.456", InputDataTypeNotInAllowlistExc),
        ("1e6", InputDataTypeNotInAllowlistExc),
        ("+1e6", InputDataTypeNotInAllowlistExc),
        ("-1e6", InputDataTypeNotInAllowlistExc),
        ("inf", InputDataTypeNotInAllowlistExc),
        ("+inf", InputDataTypeNotInAllowlistExc),
        ("-inf", InputDataTypeNotInAllowlistExc),
        ("nan", InputDataTypeNotInAllowlistExc),
        ("+nan", InputDataTypeNotInAllowlistExc),
        ("-nan", InputDataTypeNotInAllowlistExc),
        ("   456\t\t", InputDataTypeNotInAllowlistExc),
        ("\r\n789\v", InputDataTypeNotInAllowlistExc),
        ("123a456", InputDataTypeNotInAllowlistExc),
        ("a123456", InputDataTypeNotInAllowlistExc),
        ("123456a", InputDataTypeNotInAllowlistExc),
        ("123\x00456", InputDataTypeNotInAllowlistExc),
        ("\x00123456", InputDataTypeNotInAllowlistExc),
        ("123456\x00", InputDataTypeNotInAllowlistExc),
        ("\x00", InputDataTypeNotInAllowlistExc),
        ("", InputDataTypeNotInAllowlistExc),
        ("hello", InputDataTypeNotInAllowlistExc),
        ("   \t Hello World\f", InputDataTypeNotInAllowlistExc),
        ("\r fasdasfqwe\v\vf fsadf   \r\nqw    ", InputDataTypeNotInAllowlistExc),
        ([], InputDataTypeNotInAllowlistExc),
        ({}, InputDataTypeNotInAllowlistExc),
        ([1, 2], InputDataTypeNotInAllowlistExc),
        ({1: 2}, InputDataTypeNotInAllowlistExc),
        (None, InputDataTypeNotInAllowlistExc),
        (b'', InputDataTypeNotInAllowlistExc),
        (b'\x00', InputDataTypeNotInAllowlistExc),
        (b'\x01', InputDataTypeNotInAllowlistExc),
        (b'123789', InputDataTypeNotInAllowlistExc),
        (b'+123789', InputDataTypeNotInAllowlistExc),
        (b'-123789', InputDataTypeNotInAllowlistExc),
        (b'123.789', InputDataTypeNotInAllowlistExc),
        (bytearray(b'444555'), InputDataTypeNotInAllowlistExc),
        (int, InputDataTypeNotInAllowlistExc),
        (theoretical_testutils.EmptyObject, InputDataTypeNotInAllowlistExc),
        (datetime.datetime.now(), InputDataTypeNotInAllowlistExc),
        (datetime.datetime.now().date(), InputDataTypeNotInAllowlistExc),
        (datetime.datetime.now().time(), InputDataTypeNotInAllowlistExc),
        (ipaddress.ip_address("127.1.2.3"), InputDataTypeNotInAllowlistExc),
        (ipaddress.ip_address("::1"), InputDataTypeNotInAllowlistExc),
        (ipaddress.ip_network("127.0.0.0/8"), InputDataTypeNotInAllowlistExc),
        (ipaddress.ip_network("2001:db8::/32"), InputDataTypeNotInAllowlistExc),
        (urllib.parse.urlparse("https://www.google.com/test"), InputDataTypeNotInAllowlistExc),
        (uuid.UUID('{12345678-1234-5678-1234-567812345678}'), InputDataTypeNotInAllowlistExc),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc),
        (IntableObject(333222), InputDataTypeNotInAllowlistExc),
        (IntableObject(333222.111), InputDataTypeNotInAllowlistExc),
        (IntableObject(True), InputDataTypeNotInAllowlistExc),
        (IntableObject(False), InputDataTypeNotInAllowlistExc),
        (IntableObject("333222"), InputDataTypeNotInAllowlistExc),
        (IntableObject(None), InputDataTypeNotInAllowlistExc),
        (IntableObject(theoretical_testutils.EmptyObject()), InputDataTypeNotInAllowlistExc),
        (ExceptionRaisingIntableObject(), InputDataTypeNotInAllowlistExc)
    )),
    (IntegerBlueprint(filters=(NumberAbsoluteValueFilter(),)), (
        (64, expected_output_int_value("64")),
        (-64, expected_output_int_value("64")),
        ("64", expected_output_int_value("64")),
        ("-64", expected_output_int_value("64")),
        (0, expected_output_int_value("0")),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc)  # "Checks" if the blueprint is not affected by the filter
    )),
    (IntegerBlueprint(filters=(NumberMaximumClampFilter(150),)), (
        (-1000000, expected_output_int_value("-1000000")),
        (149, expected_output_int_value("149")),
        (150, expected_output_int_value("150")),
        (151, expected_output_int_value("150")),
        (1000000, expected_output_int_value("150")),
        ("-1000000", expected_output_int_value("-1000000")),
        ("149", expected_output_int_value("149")),
        ("150", expected_output_int_value("150")),
        ("151", expected_output_int_value("150")),
        ("1000000", expected_output_int_value("150")),
        (0, expected_output_int_value("0")),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc)  # "Checks" if the blueprint is not affected by the filter
    )),
    (IntegerBlueprint(filters=(NumberMaximumClampFilter(150.123),)), (
        # This is an example of how NOT to use the filter (the filter's input data are of type 'int' and the 'maximum_value' is of type 'float').
        (-1000000, expected_output_int_value("-1000000")),
        (149, expected_output_int_value("149")),
        (150, expected_output_int_value("150")),
        (151, UnexpectedOutputDataTypeExc),
        (1000000, UnexpectedOutputDataTypeExc),
        ("-1000000", expected_output_int_value("-1000000")),
        ("149", expected_output_int_value("149")),
        ("150", expected_output_int_value("150")),
        ("151", UnexpectedOutputDataTypeExc),
        ("1000000", UnexpectedOutputDataTypeExc),
        (0, expected_output_int_value("0")),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc)  # "Checks" if the blueprint is not affected by the filter
    )),
    (IntegerBlueprint(filters=(NumberMinimumClampFilter(150),)), (
        (-1000000, expected_output_int_value("150")),
        (149, expected_output_int_value("150")),
        (150, expected_output_int_value("150")),
        (151, expected_output_int_value("151")),
        (1000000, expected_output_int_value("1000000")),
        ("-1000000", expected_output_int_value("150")),
        ("149", expected_output_int_value("150")),
        ("150", expected_output_int_value("150")),
        ("151", expected_output_int_value("151")),
        ("1000000", expected_output_int_value("1000000")),
        (0, expected_output_int_value("150")),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc)  # "Checks" if the blueprint is not affected by the filter
    )),
    (IntegerBlueprint(filters=(NumberMinimumClampFilter(150.123),)), (
        # This is an example of how NOT to use the filter (the filter's input data are of type 'int' and the 'minimum_value' is of type 'float').
        (-1000000, UnexpectedOutputDataTypeExc),
        (149, UnexpectedOutputDataTypeExc),
        (150, UnexpectedOutputDataTypeExc),
        (151, expected_output_int_value("151")),
        (1000000, expected_output_int_value("1000000")),
        ("-1000000", UnexpectedOutputDataTypeExc),
        ("149", UnexpectedOutputDataTypeExc),
        ("150", UnexpectedOutputDataTypeExc),
        ("151", expected_output_int_value("151")),
        ("1000000", expected_output_int_value("1000000")),
        (0, UnexpectedOutputDataTypeExc),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc)  # "Checks" if the blueprint is not affected by the filter
    )),
    (IntegerBlueprint(filters=(NumberRoundFilter(-1),)), (
        (550, expected_output_int_value("550")),
        (554, expected_output_int_value("550")),
        (555, expected_output_int_value("560")),
        (556, expected_output_int_value("560")),
        (560, expected_output_int_value("560")),
        ("550", expected_output_int_value("550")),
        ("554", expected_output_int_value("550")),
        ("555", expected_output_int_value("560")),
        ("556", expected_output_int_value("560")),
        ("560", expected_output_int_value("560")),
        (0, expected_output_int_value("0")),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc)  # "Checks" if the blueprint is not affected by the filter
    )),
    (IntegerBlueprint(filters=(NumberRoundFilter(0),)), (  
        (550, expected_output_int_value("550")),
        (554, expected_output_int_value("554")),
        (555, expected_output_int_value("555")),
        (556, expected_output_int_value("556")),
        (560, expected_output_int_value("560")),
        ("550", expected_output_int_value("550")),
        ("554", expected_output_int_value("554")),
        ("555", expected_output_int_value("555")),
        ("556", expected_output_int_value("556")),
        ("560", expected_output_int_value("560")),
        (0, expected_output_int_value("0")),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc)  # "Checks" if the blueprint is not affected by the filter
    )),
    (IntegerBlueprint(filters=(NumberRoundFilter(1),)), (  
        (550, expected_output_int_value("550")),
        (554, expected_output_int_value("554")),
        (555, expected_output_int_value("555")),
        (556, expected_output_int_value("556")),
        (560, expected_output_int_value("560")),
        ("550", expected_output_int_value("550")),
        ("554", expected_output_int_value("554")),
        ("555", expected_output_int_value("555")),
        ("556", expected_output_int_value("556")),
        ("560", expected_output_int_value("560")),
        (0, expected_output_int_value("0")),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc)  # "Checks" if the blueprint is not affected by the filter
    )),
    (IntegerBlueprint(validators=(IntegerIsPositiveValidator(),)), (
        (-1000000, DataValidationFailedExc),
        (-1, DataValidationFailedExc),
        (0, DataValidationFailedExc),
        (1, expected_output_int_value("1")),
        (1000000, expected_output_int_value("1000000")),
        ("-1000000", DataValidationFailedExc),
        ("-1", DataValidationFailedExc),
        ("0", DataValidationFailedExc),
        ("1", expected_output_int_value("1")),
        ("1000000", expected_output_int_value("1000000")),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc)  # "Checks" if the blueprint is not affected by the validator
    )),
    (IntegerBlueprint(validators=(IntegerIsZeroOrPositiveValidator(),)), (
        (-1000000, DataValidationFailedExc),
        (-1, DataValidationFailedExc),
        (0, expected_output_int_value("0")),
        (1, expected_output_int_value("1")),
        (1000000, expected_output_int_value("1000000")),
        ("-1000000", DataValidationFailedExc),
        ("-1", DataValidationFailedExc),
        ("0", expected_output_int_value("0")),
        ("1", expected_output_int_value("1")),
        ("1000000", expected_output_int_value("1000000")),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc)  # "Checks" if the blueprint is not affected by the validator
    )),
    (IntegerBlueprint(validators=(NumberMaximumValueValidator(150),)), (
        (-1000000, expected_output_int_value("-1000000")),
        (149, expected_output_int_value("149")),
        (150, expected_output_int_value("150")),
        (151, DataValidationFailedExc),
        (1000000, DataValidationFailedExc),
        ("-1000000", expected_output_int_value("-1000000")),
        ("149", expected_output_int_value("149")),
        ("150", expected_output_int_value("150")),
        ("151", DataValidationFailedExc),
        ("1000000", DataValidationFailedExc),
        (0, expected_output_int_value("0")),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc)  # "Checks" if the blueprint is not affected by the validator
    )),
    (IntegerBlueprint(validators=(NumberMaximumValueValidator(150.123),)), (
        # This is an example of how NOT to use the validator (the validator's input data are of type 'int' and the 'maximum_acceptable_number' is of type 'float').
        # Even though it works at the moment, there is NO GUARANTEE that it will work in the future!
        (-1000000, expected_output_int_value("-1000000")),
        (149, expected_output_int_value("149")),
        (150, expected_output_int_value("150")),
        (151, DataValidationFailedExc),
        (1000000, DataValidationFailedExc),
        ("-1000000", expected_output_int_value("-1000000")),
        ("149", expected_output_int_value("149")),
        ("150", expected_output_int_value("150")),
        ("151", DataValidationFailedExc),
        ("1000000", DataValidationFailedExc),
        (0, expected_output_int_value("0")),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc)  # "Checks" if the blueprint is not affected by the validator
    )),
    (IntegerBlueprint(validators=(NumberMinimumValueValidator(150),)), (
        (-1000000, DataValidationFailedExc),
        (149, DataValidationFailedExc),
        (150, expected_output_int_value("150")),
        (151, expected_output_int_value("151")),
        (1000000, expected_output_int_value("1000000")),
        ("-1000000", DataValidationFailedExc),
        ("149", DataValidationFailedExc),
        ("150", expected_output_int_value("150")),
        ("151", expected_output_int_value("151")),
        ("1000000", expected_output_int_value("1000000")),
        (0, DataValidationFailedExc),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc)  # "Checks" if the blueprint is not affected by the validator
    )),
    (IntegerBlueprint(validators=(NumberMinimumValueValidator(150.123),)), (
        # This is an example of how NOT to use the validator (the validator's input data are of type 'int' and the 'minimum_acceptable_number' is of type 'float').
        # Even though it works at the moment, there is NO GUARANTEE that it will work in the future!
        (-1000000, DataValidationFailedExc),
        (149, DataValidationFailedExc),
        (150, DataValidationFailedExc),
        (151, expected_output_int_value("151")),
        (1000000, expected_output_int_value("1000000")),
        ("-1000000", DataValidationFailedExc),
        ("149", DataValidationFailedExc),
        ("150", DataValidationFailedExc),
        ("151", expected_output_int_value("151")),
        ("1000000", expected_output_int_value("1000000")),
        (0, DataValidationFailedExc),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc)  # "Checks" if the blueprint is not affected by the validator
    )),
    (IntegerBlueprint(
        filters=(NumberAbsoluteValueFilter(), NumberRoundFilter(-1)),
        validators=(NumberMinimumValueValidator(250), NumberMaximumValueValidator(350))
    ), (
        (-200, DataValidationFailedExc),
        (-240, DataValidationFailedExc),
        (-244, DataValidationFailedExc),
        (-245, DataValidationFailedExc),  # round() can sometimes behave weirdly - https://docs.python.org/3/library/functions.html#round
        (-246, expected_output_int_value("250")),
        (-250, expected_output_int_value("250")),
        (-299, expected_output_int_value("300")),
        (-300, expected_output_int_value("300")),
        (-301, expected_output_int_value("300")),
        (-350, expected_output_int_value("350")),
        (-354, expected_output_int_value("350")),
        (-355, DataValidationFailedExc),
        (-356, DataValidationFailedExc),
        (-360, DataValidationFailedExc),
        (-400, DataValidationFailedExc),
        (200, DataValidationFailedExc),
        (240, DataValidationFailedExc),
        (244, DataValidationFailedExc),
        (245, DataValidationFailedExc),  # round() can sometimes behave weirdly - https://docs.python.org/3/library/functions.html#round
        (246, expected_output_int_value("250")),
        (250, expected_output_int_value("250")),
        (299, expected_output_int_value("300")),
        (300, expected_output_int_value("300")),
        (301, expected_output_int_value("300")),
        (350, expected_output_int_value("350")),
        (354, expected_output_int_value("350")),
        (355, DataValidationFailedExc),
        (356, DataValidationFailedExc),
        (360, DataValidationFailedExc),
        (400, DataValidationFailedExc),
        (0, DataValidationFailedExc),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc),  # "Checks" if the blueprint is not affected by the filters & validators
    ))
)


@pytest.mark.parametrize(("blueprint", "input_", "output"), theoretical_testutils.test_function_parameter_generator(__INTEGER_BLUEPRINT_TEST_SUITE))
def test_integer_blueprint(blueprint, input_, output):
    theoretical_testutils.perform_test(blueprint, input_, output)


def test_integer_blueprint_default_parsing_mode():
    assert IntegerBlueprint().get_parsing_mode() == ParsingMode.MODE_RATIONAL


def test_integer_blueprint_instance_attributes():
    filter_seq = (NumberAbsoluteValueFilter(), NumberMaximumClampFilter(64), NumberMinimumClampFilter(32), NumberRoundFilter(3))
    validator_seq = (IntegerIsPositiveValidator(), IntegerIsZeroOrPositiveValidator(), NumberMaximumValueValidator(128), NumberMinimumValueValidator(96))
    integer_bp = IntegerBlueprint(filters=filter_seq, validators=validator_seq)

    assert (integer_bp.get_filters() == filter_seq) and (integer_bp.get_validators() == validator_seq)


def test_number_maximum_clamp_filter_maximum_value():
    assert NumberMaximumClampFilter(888).get_maximum_value() == 888


def test_number_minimum_clamp_filter_minimum_value():
    assert NumberMinimumClampFilter(777).get_minimum_value() == 777


def test_number_round_filter_decimal_places():
    assert NumberRoundFilter(-3).get_decimal_places() == -3


def test_number_maximum_value_validator_maximum_acceptable_number():
    assert NumberMaximumValueValidator(1_337_000).get_maximum_acceptable_number() == 1_337_000


def test_number_minimum_value_validator_minimum_acceptable_number():
    assert NumberMinimumValueValidator(2_337_000).get_minimum_acceptable_number() == 2_337_000
