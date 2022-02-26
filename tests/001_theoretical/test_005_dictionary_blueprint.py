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

from typing import Sequence, Tuple, Any
import theoretical_testutils
import pytest
import ipaddress
import datetime
import urllib.parse
import uuid
from datalidator.blueprints.ParsingMode import ParsingMode
from datalidator.blueprints.BlueprintIface import BlueprintIface
from datalidator.blueprints.impl.GenericBlueprint import GenericBlueprint
from datalidator.blueprints.impl.DictionaryBlueprint import DictionaryBlueprint
from datalidator.blueprints.impl.IntegerBlueprint import IntegerBlueprint
from datalidator.blueprints.impl.StringBlueprint import StringBlueprint
from datalidator.blueprints.exc.InvalidInputDataExc import InvalidInputDataExc
from datalidator.blueprints.exc.InputDataTypeNotInAllowlistExc import InputDataTypeNotInAllowlistExc
from datalidator.blueprints.exc.InputDataNotConvertibleExc import InputDataNotConvertibleExc
from datalidator.validators.impl.SequenceIsNotEmptyValidator import SequenceIsNotEmptyValidator
from datalidator.validators.impl.SequenceMaximumLengthValidator import SequenceMaximumLengthValidator
from datalidator.validators.impl.SequenceMinimumLengthValidator import SequenceMinimumLengthValidator
from datalidator.validators.exc.DataValidationFailedExc import DataValidationFailedExc
from datalidator.validators.exc.err.InvalidValidatorConfigError import InvalidValidatorConfigError


class DictableObject:
    def __init__(self, kv_pairs: Sequence[Tuple[Any, Any]]):
        self.__kv_pairs: Tuple[Tuple[Any, Any]] = tuple(kv_pairs)

    def __iter__(self):
        for pair in self.__kv_pairs:
            yield pair


class ExceptionRaisingDictableObject:
    def __init__(self, raise_: bool):
        self.__raise: bool = raise_

    def __iter__(self):
        yield "hello", "444"

        if self.__raise:
            raise theoretical_testutils.TestException()


class EmptyObjectReturningBlueprint(BlueprintIface[theoretical_testutils.EmptyObject]):
    def use(self, input_data: Any) -> theoretical_testutils.EmptyObject:
        return theoretical_testutils.EmptyObject()

    def get_tag(self) -> str:
        return self.__class__.__name__


__DICTIONARY_BLUEPRINT_TEST_SUITE = (
    (DictionaryBlueprint(
        key_blueprint=StringBlueprint(parsing_mode=ParsingMode.MODE_RATIONAL),
        value_blueprint=IntegerBlueprint(parsing_mode=ParsingMode.MODE_RATIONAL)
    ), (
        (
            {123: 456, 123.456: 789.123, True: False, complex(1, 2): "-123", None: "\r\n444  \t", "hello world": -0.0},
            {"123": 456, "123.456": 789, "True": 0, "(1+2j)": -123, "None": 444, "hello world": 0}
        ),
        (
            {ipaddress.ip_address("127.1.2.3"): 1.1, ipaddress.ip_network("2001:db8::0000/112"): 2.2, b'Hello\tWorld': 3.3, datetime.datetime(2020, 2, 29, 15, 30, 45): 4.4, urllib.parse.urlparse("HTTPS://www.google.com/test"): 5.5},
            {"127.1.2.3": 1, "2001:db8::/112": 2, "Hello\tWorld": 3, "2020-02-29T15:30:45": 4, "https://www.google.com/test": 5}
        ),
        ({"hello": 123, "world": float("inf"), "abc": 555}, InputDataNotConvertibleExc),
        ({"hello": 123, "world": float("nan"), "abc": 555}, InputDataNotConvertibleExc),
        ({"hello": 456, (3, 2, 1): 123.456, 789: 9.9}, InputDataTypeNotInAllowlistExc),
        ({"hello": 456, 123.456: (3, 2, 1), 789: 9.9}, InputDataTypeNotInAllowlistExc),
        ({"hello": 456, 123.456: theoretical_testutils.EmptyObject(), 789: 9.9}, InputDataTypeNotInAllowlistExc),
        (dict(hello=True, world="456"), {"hello": 1, "world": 456}),
        ([("abc", 123.999), ("def", 456.999), ("ghi", 789.999)], {"abc": 123, "def": 456, "ghi": 789}),
        ([("abc", 123.999), ("def",), ("ghi", 789.999)], InputDataNotConvertibleExc),
        ([("abc", 123.999), "def", ("ghi", 789.999)], InputDataNotConvertibleExc),
        ([("abc", 123.999), ("def", 456.999, True), ("ghi", 789.999)], InputDataNotConvertibleExc),
        (((i, i * i) for i in range(5)), {"0": 0, "1": 1, "2": 4, "3": 9, "4": 16}),
        (((i,) for i in range(5)), InputDataNotConvertibleExc),
        ((i for i in range(5)), InputDataNotConvertibleExc),
        (((i, i * i, i * i * i) for i in range(5)), InputDataNotConvertibleExc),
        ([(x+10 for x in range(2)), (x+20 for x in range(2)), (x+30 for x in range(2))], {"10": 11, "20": 21, "30": 31}),
        ([(x+10 for x in range(1)), (x+20 for x in range(1)), (x+30 for x in range(1))], InputDataNotConvertibleExc),
        ([(x+10 for x in range(3)), (x+20 for x in range(3)), (x+30 for x in range(3))], InputDataNotConvertibleExc),
        (dict(), {}),
        ({}, {}),
        ([], {}),
        (((i, i * i, i * i * i) for i in range(0)), {}),
        ([("hello", 123.123), ("hello", 456.456), ("world", 789.789)], {"hello": 456, "world": 789}),
        (["a1", "b2", "c3"], {"a": 1, "b": 2, "c": 3}),
        (["a1", "b", "c3"], InputDataNotConvertibleExc),
        (["a1", "b2x", "c3"], InputDataNotConvertibleExc),
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
        (urllib.parse.urlparse("a1://b2/3?e5#f6")._replace(params='d4'), {"a": 1, "b": 2, "/": 3, "d": 4, "e": 5, "f": 6}),  # This is a VERY specific case
        (uuid.UUID('{12345678-1234-5678-1234-567812345678}'), InputDataNotConvertibleExc),
        (int, InputDataNotConvertibleExc),
        (theoretical_testutils.EmptyObject, InputDataNotConvertibleExc),
        (theoretical_testutils.EmptyObject(), InputDataNotConvertibleExc),
        (DictableObject([("hello", "123"), (True, 456.789), (None, False)]), {"hello": 123, "True": 456, "None": 0}),
        (DictableObject([("hello", "123"), (True,), (None, False)]), InputDataNotConvertibleExc),
        (DictableObject([("hello", "123"), (True, 456.789, 111), (None, False)]), InputDataNotConvertibleExc),
        (ExceptionRaisingDictableObject(raise_=False), {"hello": 444}),
        (ExceptionRaisingDictableObject(raise_=True), InputDataNotConvertibleExc),
    )),
    (DictionaryBlueprint(
        key_blueprint=GenericBlueprint(),
        value_blueprint=GenericBlueprint()
    ), (
        ({True: None, "hello": 123, 456: float("inf")}, {True: None, "hello": 123, 456: float("inf")}),
        ([(True, None), ("hello", 123), (456, float("inf"))], {True: None, "hello": 123, 456: float("inf")}),
        ([(True, None), ("hello",), (456, float("inf"))], InputDataNotConvertibleExc),
        ([(True, None), ("hello", 123, 999), (456, float("inf"))], InputDataNotConvertibleExc),
        ({"abc": [1, 2, 3], "def": [4, 5, 6]}, {"abc": [1, 2, 3], "def": [4, 5, 6]}),
        ([("hello", 123), ("test", theoretical_testutils.EmptyObject()), ("world", 789)], {"hello": 123, "test": theoretical_testutils.EmptyObject(), "world": 789}),
        ([("hello", 123), (theoretical_testutils.EmptyObject(), "test"), ("world", 789)], InputDataNotConvertibleExc),
    )),
    (DictionaryBlueprint(
        key_blueprint=EmptyObjectReturningBlueprint(),
        value_blueprint=EmptyObjectReturningBlueprint(),
    ), (
        ({"hello": 123, "world": 456, "test": 789}, InvalidInputDataExc),
        ([("hello", 123), ("world", 456), ("test", 789)], InvalidInputDataExc),
        ({}, {}),
        ([], {})
    )),
    (DictionaryBlueprint(
        key_blueprint=GenericBlueprint(),
        value_blueprint=GenericBlueprint(),
        validators=(SequenceIsNotEmptyValidator(negate=False),)  
    ), (
        ({}, DataValidationFailedExc),
        ([], DataValidationFailedExc),
        (((i, i) for i in range(0)), DataValidationFailedExc),
        ({"a": 1}, {"a": 1}),
        ([("b", 2)], {"b": 2}),
        (((i, i) for i in range(1)), {0: 0}),
        ({"a": 1, "x": True}, {"a": 1, "x": True}),
        ([("b", 2), ("y", False)], {"b": 2, "y": False}),
        (((i, i) for i in range(2)), {0: 0, 1: 1}),
        ([(1, 2), (3, 4), (5, 6)], {1: 2, 3: 4, 5: 6}),
        ([(1, 2), (3, 4, 999), (5, 6)], InputDataNotConvertibleExc),
        ([(1, 2), (3,), (5, 6)], InputDataNotConvertibleExc),
        ([(1, 2), 3, (5, 6)], InputDataNotConvertibleExc),
    )),
    (DictionaryBlueprint(
        key_blueprint=GenericBlueprint(),
        value_blueprint=GenericBlueprint(),
        validators=(SequenceIsNotEmptyValidator(negate=True),)  
    ), (
        ({}, {}),
        ([], {}),
        (((i, i) for i in range(0)), {}),
        ({"a": 1}, DataValidationFailedExc),
        ([("b", 2)], DataValidationFailedExc),
        (((i, i) for i in range(1)), DataValidationFailedExc),
        ({"a": 1, "x": True}, DataValidationFailedExc),
        ([("b", 2), ("y", False)], DataValidationFailedExc),
        (((i, i) for i in range(2)), DataValidationFailedExc),
        ([(1, 2), (3, 4), (5, 6)], DataValidationFailedExc),
        ([(1, 2), (3, 4, 999), (5, 6)], InputDataNotConvertibleExc),
        ([(1, 2), (3,), (5, 6)], InputDataNotConvertibleExc),
        ([(1, 2), 3, (5, 6)], InputDataNotConvertibleExc),
    )),
    (DictionaryBlueprint(
        key_blueprint=GenericBlueprint(),
        value_blueprint=GenericBlueprint(),
        validators=(SequenceMaximumLengthValidator(5),)
    ), (
        ({}, {}),
        ([], {}),
        ({1: 1, 2: 2, 3: 3, 4: 4}, {1: 1, 2: 2, 3: 3, 4: 4}),
        ([(1, 1), (2, 2), (3, 3), (4, 4)], {1: 1, 2: 2, 3: 3, 4: 4}),
        ({1: 1, 2: 2, 3: 3, 4: 4, 5: 5}, {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}),
        ([(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}),
        ({1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6}, DataValidationFailedExc),
        ([(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)], DataValidationFailedExc),
        ([(1, 2), (3, 4), (5, 6)], {1: 2, 3: 4, 5: 6}),
        ([(1, 2), (3, 4, 999), (5, 6)], InputDataNotConvertibleExc),
        ([(1, 2), (3,), (5, 6)], InputDataNotConvertibleExc),
        ([(1, 2), 3, (5, 6)], InputDataNotConvertibleExc),
    )),
    (DictionaryBlueprint(
        key_blueprint=GenericBlueprint(),
        value_blueprint=GenericBlueprint(),
        validators=(SequenceMinimumLengthValidator(5),)
    ), (
        ({}, DataValidationFailedExc),
        ([], DataValidationFailedExc),
        ({1: 1, 2: 2, 3: 3, 4: 4}, DataValidationFailedExc),
        ([(1, 1), (2, 2), (3, 3), (4, 4)], DataValidationFailedExc),
        ({1: 1, 2: 2, 3: 3, 4: 4, 5: 5}, {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}),
        ([(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}),
        ({1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6}, {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6}),
        ([(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)], {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6}),
        ([(1, 2), (3, 4), (5, 6)], DataValidationFailedExc),
        ([(1, 2), (3, 4, 999), (5, 6)], InputDataNotConvertibleExc),
        ([(1, 2), (3,), (5, 6)], InputDataNotConvertibleExc),
        ([(1, 2), 3, (5, 6)], InputDataNotConvertibleExc),
    )),
    (DictionaryBlueprint(
        key_blueprint=GenericBlueprint(),
        value_blueprint=GenericBlueprint(),
        validators=(SequenceMinimumLengthValidator(3), SequenceMaximumLengthValidator(5))
    ), (
        ({}, DataValidationFailedExc),
        ({1: 1, 2: 2}, DataValidationFailedExc),
        ({1: 1, 2: 2, 3: 3}, {1: 1, 2: 2, 3: 3}),
        ({1: 1, 2: 2, 3: 3, 4: 4}, {1: 1, 2: 2, 3: 3, 4: 4}),
        ({1: 1, 2: 2, 3: 3, 4: 4, 5: 5}, {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}),
        ({1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6}, DataValidationFailedExc),
        ([(1, 2), (3, 4), (5, 6)], {1: 2, 3: 4, 5: 6}),
        ([(1, 2), (3, 4, 999), (5, 6)], InputDataNotConvertibleExc),
        ([(1, 2), (3,), (5, 6)], InputDataNotConvertibleExc),
        ([(1, 2), 3, (5, 6)], InputDataNotConvertibleExc),
    ))
)


@pytest.mark.parametrize(("blueprint", "input_", "output"), theoretical_testutils.test_function_parameter_generator(__DICTIONARY_BLUEPRINT_TEST_SUITE))
def test_dictionary_blueprint(blueprint, input_, output):
    theoretical_testutils.perform_test(blueprint, input_, output)


def test_dictionary_blueprint_instance_attributes():
    key_bp = StringBlueprint()
    value_bp = IntegerBlueprint()
    validator_seq = (SequenceIsNotEmptyValidator(), SequenceMaximumLengthValidator(9999), SequenceMinimumLengthValidator(8888))
    dict_bp = DictionaryBlueprint(key_blueprint=key_bp, value_blueprint=value_bp, validators=validator_seq)

    assert (dict_bp.get_key_blueprint() is key_bp) and (dict_bp.get_value_blueprint() is value_bp) and (dict_bp.get_validators() == validator_seq)


def test_sequence_is_not_empty_validator_default_negation():
    assert SequenceIsNotEmptyValidator().is_negated() is False


def test_sequence_maximum_length_validator_maximum_acceptable_length():
    assert SequenceMaximumLengthValidator(1337).get_maximum_acceptable_length() == 1337


def test_sequence_maximum_length_validator_invalid_maximum_acceptable_length():
    with pytest.raises(InvalidValidatorConfigError):
        SequenceMaximumLengthValidator(-1)

    # These must not raise an exception:
    SequenceMaximumLengthValidator(0)
    SequenceMaximumLengthValidator(1)


def test_sequence_minimum_length_validator_minimum_acceptable_length():
    assert SequenceMinimumLengthValidator(2337).get_minimum_acceptable_length() == 2337


def test_sequence_minimum_length_validator_invalid_minimum_acceptable_length():
    with pytest.raises(InvalidValidatorConfigError):
        SequenceMinimumLengthValidator(-1)

    # These must not raise an exception:
    SequenceMinimumLengthValidator(0)
    SequenceMinimumLengthValidator(1)
