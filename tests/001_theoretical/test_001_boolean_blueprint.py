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

import theoretical_testutils
import pytest
import datetime
import ipaddress
import urllib.parse
import uuid
from datalidator.blueprints.ParsingMode import ParsingMode
from datalidator.blueprints.impl.BooleanBlueprint import BooleanBlueprint
from datalidator.blueprints.exc.InputDataNotConvertibleExc import InputDataNotConvertibleExc
from datalidator.blueprints.exc.InputDataValueNotAllowedForDataTypeExc import InputDataValueNotAllowedForDataTypeExc
from datalidator.blueprints.exc.InputDataTypeNotInAllowlistExc import InputDataTypeNotInAllowlistExc


class BooleanableObject:
    def __init__(self, returned_value):
        self.__returned_value = returned_value

    def __bool__(self):
        return self.__returned_value


class ExceptionRaisingBooleanableObject:
    def __bool__(self):
        raise theoretical_testutils.TestException()


__BOOLEAN_BLUEPRINT_TEST_SUITE = (
    (BooleanBlueprint(parsing_mode=ParsingMode.MODE_LOOSE), (
        (True, True),
        (False, False),
        (1, True),
        (0, False),
        (123, True),
        (-1, True),
        (-0, False),
        (0.0, False),
        (1.0, True),
        (0.1, True),
        (1.1, True),
        (-0.0, False),
        (-1.0, True),
        (-0.1, True),
        (-1.1, True),
        (123.456, True),
        (float("nan"), True),
        (float("inf"), True),
        (None, False),
        ("1", True),
        ("yeS", True),
        ("y", True),
        ("tRUE", True),
        ("ON", True),
        ("0", True),
        ("no", True),
        ("n", True),
        ("False", True),
        ("OFf", True),
        ("  \r\noFF   \t", True),
        (" \t\tTrue   ", True),
        ("", False),
        ("abcdef", True),
        ("    fasd\rcxycvxy\t    ", True),
        ("\x00", True),
        ([], False),
        ({}, False),
        (["abc", "def"], True),
        ({"a": 1}, True),
        (datetime.datetime.now(), True),
        (datetime.datetime.now().date(), True),
        (datetime.datetime.now().time(), True),
        (b'', False),
        (b'a', True),
        (int, True),
        (theoretical_testutils.EmptyObject, True),
        (ipaddress.ip_address("127.0.0.1"), True),
        (ipaddress.ip_address("::1"), True),
        (ipaddress.ip_network("127.0.0.0/8"), True),
        (ipaddress.ip_network("2001:db8::/32"), True),
        (urllib.parse.urlparse("https://www.google.com/test?abc=def"), True),
        (uuid.UUID('{12345678-1234-5678-1234-567812345678}'), True),
        (theoretical_testutils.EmptyObject(), True),
        (BooleanableObject(True), True),
        (BooleanableObject(False), False),
        (BooleanableObject("hello world"), InputDataNotConvertibleExc),
        (BooleanableObject(123), InputDataNotConvertibleExc),
        (BooleanableObject(123.456), InputDataNotConvertibleExc),
        (BooleanableObject(None), InputDataNotConvertibleExc),
        (BooleanableObject([]), InputDataNotConvertibleExc),
        (BooleanableObject(theoretical_testutils.EmptyObject()), InputDataNotConvertibleExc),
        (ExceptionRaisingBooleanableObject(), InputDataNotConvertibleExc)
    )),
    (BooleanBlueprint(parsing_mode=ParsingMode.MODE_RATIONAL), (
        (True, True),
        (False, False),
        (1, True),
        (0, False),
        (123, InputDataValueNotAllowedForDataTypeExc),
        (-1, InputDataValueNotAllowedForDataTypeExc),
        (-0, False),
        (0.0, False),
        (1.0, True),
        (0.1, InputDataValueNotAllowedForDataTypeExc),
        (1.1, InputDataValueNotAllowedForDataTypeExc),
        (-0.0, False),
        (-1.0, InputDataValueNotAllowedForDataTypeExc),
        (-0.1, InputDataValueNotAllowedForDataTypeExc),
        (-1.1, InputDataValueNotAllowedForDataTypeExc),
        (123.456, InputDataValueNotAllowedForDataTypeExc),
        (float("nan"), InputDataValueNotAllowedForDataTypeExc),
        (float("inf"), InputDataValueNotAllowedForDataTypeExc),
        (None, InputDataTypeNotInAllowlistExc),
        ("1", True),
        ("yeS", True),
        ("y", True),
        ("tRUE", True),
        ("ON", True),
        ("0", False),
        ("no", False),
        ("n", False),
        ("False", False),
        ("OFf", False),
        ("  \r\noFF   \t", False),
        (" \t\tTrue   ", True),
        ("", InputDataValueNotAllowedForDataTypeExc),
        ("abcdef", InputDataValueNotAllowedForDataTypeExc),
        ("    fasd\rcxycvxy\t    ", InputDataValueNotAllowedForDataTypeExc),
        ("\x00", InputDataValueNotAllowedForDataTypeExc),
        ([], InputDataTypeNotInAllowlistExc),
        ({}, InputDataTypeNotInAllowlistExc),
        (["abc", "def"], InputDataTypeNotInAllowlistExc),
        ({"a": 1}, InputDataTypeNotInAllowlistExc),
        (datetime.datetime.now(), InputDataTypeNotInAllowlistExc),
        (datetime.datetime.now().date(), InputDataTypeNotInAllowlistExc),
        (datetime.datetime.now().time(), InputDataTypeNotInAllowlistExc),
        (b'', InputDataTypeNotInAllowlistExc),
        (b'a', InputDataTypeNotInAllowlistExc),
        (int, InputDataTypeNotInAllowlistExc),
        (theoretical_testutils.EmptyObject, InputDataTypeNotInAllowlistExc),
        (ipaddress.ip_address("127.0.0.1"), InputDataTypeNotInAllowlistExc),
        (ipaddress.ip_address("::1"), InputDataTypeNotInAllowlistExc),
        (ipaddress.ip_network("127.0.0.0/8"), InputDataTypeNotInAllowlistExc),
        (ipaddress.ip_network("2001:db8::/32"), InputDataTypeNotInAllowlistExc),
        (urllib.parse.urlparse("https://www.google.com/test?abc=def"), InputDataTypeNotInAllowlistExc),
        (uuid.UUID('{12345678-1234-5678-1234-567812345678}'), InputDataTypeNotInAllowlistExc),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc),
        (BooleanableObject(True), InputDataTypeNotInAllowlistExc),
        (BooleanableObject(False), InputDataTypeNotInAllowlistExc),
        (BooleanableObject("hello world"), InputDataTypeNotInAllowlistExc),
        (BooleanableObject(123), InputDataTypeNotInAllowlistExc),
        (BooleanableObject(123.456), InputDataTypeNotInAllowlistExc),
        (BooleanableObject(None), InputDataTypeNotInAllowlistExc),
        (BooleanableObject([]), InputDataTypeNotInAllowlistExc),
        (BooleanableObject(theoretical_testutils.EmptyObject()), InputDataTypeNotInAllowlistExc),
        (ExceptionRaisingBooleanableObject(), InputDataTypeNotInAllowlistExc)
    )),
    (BooleanBlueprint(parsing_mode=ParsingMode.MODE_STRICT), (
        (True, True),
        (False, False),
        (1, InputDataTypeNotInAllowlistExc),
        (0, InputDataTypeNotInAllowlistExc),
        (123, InputDataTypeNotInAllowlistExc),
        (-1, InputDataTypeNotInAllowlistExc),
        (-0, InputDataTypeNotInAllowlistExc),
        (0.0, InputDataTypeNotInAllowlistExc),
        (1.0, InputDataTypeNotInAllowlistExc),
        (0.1, InputDataTypeNotInAllowlistExc),
        (1.1, InputDataTypeNotInAllowlistExc),
        (-0.0, InputDataTypeNotInAllowlistExc),
        (-1.0, InputDataTypeNotInAllowlistExc),
        (-0.1, InputDataTypeNotInAllowlistExc),
        (-1.1, InputDataTypeNotInAllowlistExc),
        (123.456, InputDataTypeNotInAllowlistExc),
        (float("nan"), InputDataTypeNotInAllowlistExc),
        (float("inf"), InputDataTypeNotInAllowlistExc),
        (None, InputDataTypeNotInAllowlistExc),
        ("1", InputDataTypeNotInAllowlistExc),
        ("yeS", InputDataTypeNotInAllowlistExc),
        ("y", InputDataTypeNotInAllowlistExc),
        ("tRUE", InputDataTypeNotInAllowlistExc),
        ("ON", InputDataTypeNotInAllowlistExc),
        ("0", InputDataTypeNotInAllowlistExc),
        ("no", InputDataTypeNotInAllowlistExc),
        ("n", InputDataTypeNotInAllowlistExc),
        ("False", InputDataTypeNotInAllowlistExc),
        ("OFf", InputDataTypeNotInAllowlistExc),
        ("  \r\noFF   \t", InputDataTypeNotInAllowlistExc),
        (" \t\tTrue   ", InputDataTypeNotInAllowlistExc),
        ("", InputDataTypeNotInAllowlistExc),
        ("abcdef", InputDataTypeNotInAllowlistExc),
        ("    fasd\rcxycvxy\t    ", InputDataTypeNotInAllowlistExc),
        ("\x00", InputDataTypeNotInAllowlistExc),
        ([], InputDataTypeNotInAllowlistExc),
        ({}, InputDataTypeNotInAllowlistExc),
        (["abc", "def"], InputDataTypeNotInAllowlistExc),
        ({"a": 1}, InputDataTypeNotInAllowlistExc),
        (datetime.datetime.now(), InputDataTypeNotInAllowlistExc),
        (datetime.datetime.now().date(), InputDataTypeNotInAllowlistExc),
        (datetime.datetime.now().time(), InputDataTypeNotInAllowlistExc),
        (b'', InputDataTypeNotInAllowlistExc),
        (b'a', InputDataTypeNotInAllowlistExc),
        (int, InputDataTypeNotInAllowlistExc),
        (theoretical_testutils.EmptyObject, InputDataTypeNotInAllowlistExc),
        (ipaddress.ip_address("127.0.0.1"), InputDataTypeNotInAllowlistExc),
        (ipaddress.ip_address("::1"), InputDataTypeNotInAllowlistExc),
        (ipaddress.ip_network("127.0.0.0/8"), InputDataTypeNotInAllowlistExc),
        (ipaddress.ip_network("2001:db8::/32"), InputDataTypeNotInAllowlistExc),
        (urllib.parse.urlparse("https://www.google.com/test?abc=def"), InputDataTypeNotInAllowlistExc),
        (uuid.UUID('{12345678-1234-5678-1234-567812345678}'), InputDataTypeNotInAllowlistExc),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc),
        (BooleanableObject(True), InputDataTypeNotInAllowlistExc),
        (BooleanableObject(False), InputDataTypeNotInAllowlistExc),
        (BooleanableObject("hello world"), InputDataTypeNotInAllowlistExc),
        (BooleanableObject(123), InputDataTypeNotInAllowlistExc),
        (BooleanableObject(123.456), InputDataTypeNotInAllowlistExc),
        (BooleanableObject(None), InputDataTypeNotInAllowlistExc),
        (BooleanableObject([]), InputDataTypeNotInAllowlistExc),
        (BooleanableObject(theoretical_testutils.EmptyObject()), InputDataTypeNotInAllowlistExc),
        (ExceptionRaisingBooleanableObject(), InputDataTypeNotInAllowlistExc)
    ))
)


@pytest.mark.parametrize(("blueprint", "input_", "output"), theoretical_testutils.test_function_parameter_generator(__BOOLEAN_BLUEPRINT_TEST_SUITE))
def test_boolean_blueprint(blueprint, input_, output):
    theoretical_testutils.perform_test(blueprint, input_, output)


def test_boolean_blueprint_default_parsing_mode():
    assert BooleanBlueprint().get_parsing_mode() == ParsingMode.MODE_RATIONAL
