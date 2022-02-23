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
from datalidator.blueprints.impl.BytesBlueprint import BytesBlueprint
from datalidator.blueprints.exc.InputDataTypeNotInAllowlistExc import InputDataTypeNotInAllowlistExc
from datalidator.blueprints.exc.InputDataTypeInBlocklistExc import InputDataTypeInBlocklistExc
from datalidator.blueprints.exc.InputDataNotConvertibleExc import InputDataNotConvertibleExc


class BytesableObject:
    def __init__(self, returned_bytes):
        self.__returned_bytes = returned_bytes

    def __bytes__(self):
        return self.__returned_bytes


class ExceptionRaisingBytesableObject:
    def __bytes__(self):
        raise theoretical_testutils.TestException()


__BYTES_BLUEPRINT_TEST_SUITE = (
    (BytesBlueprint(parsing_mode=ParsingMode.MODE_LOOSE), (
        (b'', b''),
        (b'hello', b'hello'),
        (b'\r\nhe llo\t', b'\r\nhe llo\t'),
        (bytes(b'abcd'), b'abcd'),
        (bytearray(b'xyz'), b'xyz'),
        (True, InputDataTypeInBlocklistExc),
        (False, InputDataTypeInBlocklistExc),
        (None, InputDataNotConvertibleExc),
        (0, InputDataTypeInBlocklistExc),
        (123, InputDataTypeInBlocklistExc),
        (0.0, InputDataTypeInBlocklistExc),
        (123.456, InputDataTypeInBlocklistExc),
        ("", b''),
        ("Hello", b'Hello'),
        ("Hello World", b'Hello World'),
        ("\r\n Te\tstString\t\t ", b'\r\n Te\tstString\t\t '),
        ("\xee\xee", b'\xc3\xae\xc3\xae'),
        ("řeřicha", b'\xc5\x99e\xc5\x99icha'),
        ("Příliš žluťoučký kůň úpěl ďábelské ódy.", b'P\xc5\x99\xc3\xadli\xc5\xa1 \xc5\xbelu\xc5\xa5ou\xc4\x8dk\xc3\xbd k\xc5\xaf\xc5\x88 \xc3\xbap\xc4\x9bl \xc4\x8f\xc3\xa1belsk\xc3\xa9 \xc3\xb3dy.'),
        ("🤍", b'\xf0\x9f\xa4\x8d'),
        (datetime.datetime.now(), InputDataNotConvertibleExc),
        (datetime.datetime.now().date(), InputDataNotConvertibleExc),
        (datetime.datetime.now().time(), InputDataNotConvertibleExc),
        ([], b''),
        ([b'a', b'x'], InputDataNotConvertibleExc),
        (["hello", "world"], InputDataNotConvertibleExc),
        ([1, 127, 254], b'\x01\x7f\xfe'),
        ((1, 127, 254), b'\x01\x7f\xfe'),
        ({}, b''),
        ({224: "x"}, b'\xe0'),
        (range(5), b'\x00\x01\x02\x03\x04'),
        (int, InputDataNotConvertibleExc),
        (theoretical_testutils.EmptyObject, InputDataNotConvertibleExc),
        (ipaddress.ip_address("127.0.0.1"), InputDataNotConvertibleExc),
        (ipaddress.ip_address("::1"), InputDataNotConvertibleExc),
        (ipaddress.ip_network("127.0.0.0/8"), InputDataNotConvertibleExc),
        (ipaddress.ip_network("2001:db8::/32"), InputDataNotConvertibleExc),
        (urllib.parse.urlparse("https://www.google.com/test?abc=def"), InputDataNotConvertibleExc),
        (uuid.UUID('{12345678-1234-5678-1234-567812345678}'), InputDataNotConvertibleExc),
        (theoretical_testutils.EmptyObject(), InputDataNotConvertibleExc),
        (BytesableObject(b'123456 test'), b'123456 test'),
        (BytesableObject(bytearray(b'abcdef')), InputDataNotConvertibleExc),
        (BytesableObject(True), InputDataNotConvertibleExc),
        (BytesableObject(None), InputDataNotConvertibleExc),
        (BytesableObject(123), InputDataNotConvertibleExc),
        (BytesableObject(123.456), InputDataNotConvertibleExc),
        (BytesableObject([]), InputDataNotConvertibleExc),
        (BytesableObject(theoretical_testutils.EmptyObject()), InputDataNotConvertibleExc),
        (ExceptionRaisingBytesableObject(), InputDataNotConvertibleExc)
    )),
    (BytesBlueprint(parsing_mode=ParsingMode.MODE_RATIONAL), (
        (b'', b''),
        (b'hello', b'hello'),
        (b'\r\nhe llo\t', b'\r\nhe llo\t'),
        (bytes(b'abcd'), b'abcd'),
        (bytearray(b'xyz'), b'xyz'),
        (True, InputDataTypeNotInAllowlistExc),
        (False, InputDataTypeNotInAllowlistExc),
        (None, InputDataTypeNotInAllowlistExc),
        (0, InputDataTypeNotInAllowlistExc),
        (123, InputDataTypeNotInAllowlistExc),
        (0.0, InputDataTypeNotInAllowlistExc),
        (123.456, InputDataTypeNotInAllowlistExc),
        ("", b''),
        ("Hello", b'Hello'),
        ("Hello World", b'Hello World'),
        ("\r\n Te\tstString\t\t ", b'\r\n Te\tstString\t\t '),
        ("\xee\xee", b'\xc3\xae\xc3\xae'),
        ("řeřicha", b'\xc5\x99e\xc5\x99icha'),
        ("Příliš žluťoučký kůň úpěl ďábelské ódy.", b'P\xc5\x99\xc3\xadli\xc5\xa1 \xc5\xbelu\xc5\xa5ou\xc4\x8dk\xc3\xbd k\xc5\xaf\xc5\x88 \xc3\xbap\xc4\x9bl \xc4\x8f\xc3\xa1belsk\xc3\xa9 \xc3\xb3dy.'),
        ("🤍", b'\xf0\x9f\xa4\x8d'),
        (datetime.datetime.now(), InputDataTypeNotInAllowlistExc),
        (datetime.datetime.now().date(), InputDataTypeNotInAllowlistExc),
        (datetime.datetime.now().time(), InputDataTypeNotInAllowlistExc),
        ([], InputDataTypeNotInAllowlistExc),
        ([b'a', b'x'], InputDataTypeNotInAllowlistExc),
        (["hello", "world"], InputDataTypeNotInAllowlistExc),
        ([1, 127, 254], InputDataTypeNotInAllowlistExc),
        ((1, 127, 254), InputDataTypeNotInAllowlistExc),
        ({}, InputDataTypeNotInAllowlistExc),
        ({224: "something"}, InputDataTypeNotInAllowlistExc),
        (range(5), InputDataTypeNotInAllowlistExc),
        (int, InputDataTypeNotInAllowlistExc),
        (theoretical_testutils.EmptyObject, InputDataTypeNotInAllowlistExc),
        (ipaddress.ip_address("127.0.0.1"), InputDataTypeNotInAllowlistExc),
        (ipaddress.ip_address("::1"), InputDataTypeNotInAllowlistExc),
        (ipaddress.ip_network("127.0.0.0/8"), InputDataTypeNotInAllowlistExc),
        (ipaddress.ip_network("2001:db8::/32"), InputDataTypeNotInAllowlistExc),
        (urllib.parse.urlparse("https://www.google.com/test?abc=def"), InputDataTypeNotInAllowlistExc),
        (uuid.UUID('{12345678-1234-5678-1234-567812345678}'), InputDataTypeNotInAllowlistExc),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc),
        (BytesableObject(b'123456 test'), InputDataTypeNotInAllowlistExc),
        (BytesableObject(bytearray(b'abcdef')), InputDataTypeNotInAllowlistExc),
        (BytesableObject(True), InputDataTypeNotInAllowlistExc),
        (BytesableObject(None), InputDataTypeNotInAllowlistExc),
        (BytesableObject(123), InputDataTypeNotInAllowlistExc),
        (BytesableObject(123.456), InputDataTypeNotInAllowlistExc),
        (BytesableObject([]), InputDataTypeNotInAllowlistExc),
        (BytesableObject(theoretical_testutils.EmptyObject()), InputDataTypeNotInAllowlistExc),
        (ExceptionRaisingBytesableObject(), InputDataTypeNotInAllowlistExc)
    )),
    (BytesBlueprint(parsing_mode=ParsingMode.MODE_STRICT), (
        (b'', b''),
        (b'hello', b'hello'),
        (b'\r\nhe llo\t', b'\r\nhe llo\t'),
        (bytes(b'abcd'), b'abcd'),
        (bytearray(b'xyz'), b'xyz'),
        (True, InputDataTypeNotInAllowlistExc),
        (False, InputDataTypeNotInAllowlistExc),
        (None, InputDataTypeNotInAllowlistExc),
        (0, InputDataTypeNotInAllowlistExc),
        (123, InputDataTypeNotInAllowlistExc),
        (0.0, InputDataTypeNotInAllowlistExc),
        (123.456, InputDataTypeNotInAllowlistExc),
        ("", InputDataTypeNotInAllowlistExc),
        ("Hello", InputDataTypeNotInAllowlistExc),
        ("Hello World", InputDataTypeNotInAllowlistExc),
        ("\r\n Te\tstString\t\t ", InputDataTypeNotInAllowlistExc),
        ("\xee\xee", InputDataTypeNotInAllowlistExc),
        ("řeřicha", InputDataTypeNotInAllowlistExc),
        ("Příliš žluťoučký kůň úpěl ďábelské ódy.", InputDataTypeNotInAllowlistExc),
        ("🤍", InputDataTypeNotInAllowlistExc),
        (datetime.datetime.now(), InputDataTypeNotInAllowlistExc),
        (datetime.datetime.now().date(), InputDataTypeNotInAllowlistExc),
        (datetime.datetime.now().time(), InputDataTypeNotInAllowlistExc),
        ([], InputDataTypeNotInAllowlistExc),
        ([b'a', b'x'], InputDataTypeNotInAllowlistExc),
        (["hello", "world"], InputDataTypeNotInAllowlistExc),
        ([1, 127, 254], InputDataTypeNotInAllowlistExc),
        ((1, 127, 254), InputDataTypeNotInAllowlistExc),
        ({}, InputDataTypeNotInAllowlistExc),
        ({224: "x"}, InputDataTypeNotInAllowlistExc),
        (range(5), InputDataTypeNotInAllowlistExc),
        (int, InputDataTypeNotInAllowlistExc),
        (theoretical_testutils.EmptyObject, InputDataTypeNotInAllowlistExc),
        (ipaddress.ip_address("127.0.0.1"), InputDataTypeNotInAllowlistExc),
        (ipaddress.ip_address("::1"), InputDataTypeNotInAllowlistExc),
        (ipaddress.ip_network("127.0.0.0/8"), InputDataTypeNotInAllowlistExc),
        (ipaddress.ip_network("2001:db8::/32"), InputDataTypeNotInAllowlistExc),
        (urllib.parse.urlparse("https://www.google.com/test?abc=def"), InputDataTypeNotInAllowlistExc),
        (uuid.UUID('{12345678-1234-5678-1234-567812345678}'), InputDataTypeNotInAllowlistExc),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc),
        (BytesableObject(b'123456 test'), InputDataTypeNotInAllowlistExc),
        (BytesableObject(bytearray(b'abcdef')), InputDataTypeNotInAllowlistExc),
        (BytesableObject(True), InputDataTypeNotInAllowlistExc),
        (BytesableObject(None), InputDataTypeNotInAllowlistExc),
        (BytesableObject(123), InputDataTypeNotInAllowlistExc),
        (BytesableObject(123.456), InputDataTypeNotInAllowlistExc),
        (BytesableObject([]), InputDataTypeNotInAllowlistExc),
        (BytesableObject(theoretical_testutils.EmptyObject()), InputDataTypeNotInAllowlistExc),
        (ExceptionRaisingBytesableObject(), InputDataTypeNotInAllowlistExc)
    )),
    (BytesBlueprint(string_encoding="ascii", parsing_mode=ParsingMode.MODE_LOOSE), (
        ("", b''),
        ("hello", b'hello'),
        ("\r\nTest  String\t", b'\r\nTest  String\t'),
        ("\ueeee", InputDataNotConvertibleExc),
        ("řeřicha", InputDataNotConvertibleExc),
        ("Pepík", InputDataNotConvertibleExc),
        (BytesableObject(b'123456 test'), b'123456 test'),
        (BytesableObject(theoretical_testutils.EmptyObject()), InputDataNotConvertibleExc),
        (ExceptionRaisingBytesableObject(), InputDataNotConvertibleExc)
    ))
)


@pytest.mark.parametrize(("blueprint", "input_", "output"), theoretical_testutils.test_function_parameter_generator(__BYTES_BLUEPRINT_TEST_SUITE))
def test_bytes_blueprint(blueprint, input_, output):
    theoretical_testutils.perform_test(blueprint, input_, output)


def test_bytes_blueprint_default_parsing_mode():
    assert BytesBlueprint().get_parsing_mode() == ParsingMode.MODE_RATIONAL


def test_bytes_blueprint_default_string_encoding():
    assert BytesBlueprint().get_string_encoding() == "utf-8"


def test_bytes_blueprint_custom_string_encoding():
    assert BytesBlueprint(string_encoding="ascii").get_string_encoding() == "ascii"
