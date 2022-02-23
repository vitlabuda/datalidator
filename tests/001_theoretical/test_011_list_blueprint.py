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

from typing import Iterable, Tuple, Any
import theoretical_testutils
import pytest
import string
import datetime
import ipaddress
import urllib.parse
import uuid
from datalidator.blueprints.ParsingMode import ParsingMode
from datalidator.blueprints.impl.ListBlueprint import ListBlueprint
from datalidator.blueprints.impl.IntegerBlueprint import IntegerBlueprint
from datalidator.blueprints.impl.StringBlueprint import StringBlueprint
from datalidator.blueprints.impl.GenericBlueprint import GenericBlueprint
from datalidator.blueprints.exc.InputDataNotConvertibleExc import InputDataNotConvertibleExc
from datalidator.blueprints.exc.InputDataTypeNotInAllowlistExc import InputDataTypeNotInAllowlistExc
from datalidator.blueprints.exc.InputDataTypeInBlocklistExc import InputDataTypeInBlocklistExc
from datalidator.filters.impl.ListDeduplicateItemsFilter import ListDeduplicateItemsFilter
from datalidator.filters.impl.ListSortFilter import ListSortFilter
from datalidator.filters.exc.SortingFailedInFilterExc import SortingFailedInFilterExc
from datalidator.validators.impl.SequenceContainsItemValidator import SequenceContainsItemValidator
from datalidator.validators.impl.SequenceHasAllItemsUniqueValidator import SequenceHasAllItemsUniqueValidator
from datalidator.validators.impl.SequenceIsNotEmptyValidator import SequenceIsNotEmptyValidator
from datalidator.validators.impl.SequenceMaximumLengthValidator import SequenceMaximumLengthValidator
from datalidator.validators.impl.SequenceMinimumLengthValidator import SequenceMinimumLengthValidator
from datalidator.validators.impl.IntegerIsPositiveValidator import IntegerIsPositiveValidator
from datalidator.validators.impl.NumberMaximumValueValidator import NumberMaximumValueValidator
from datalidator.validators.exc.DataValidationFailedExc import DataValidationFailedExc
from datalidator.validators.exc.err.InvalidValidatorConfigError import InvalidValidatorConfigError


# Some input collections (e.g. sets) are unordered!
def ignore_order_of_output_list(expected_output_list: list):  # DP: Factory
    return lambda output: (output.__class__ is list) and (sorted(output) == sorted(expected_output_list))


def exception_raising_comparison_key_extraction_function(item):  # noqa
    raise theoretical_testutils.TestException()


class IterableObject:
    def __init__(self, iter_: Iterable[Any]):
        self.__seq: Tuple[Any, ...] = tuple(iter_)

    def __iter__(self):
        for item in self.__seq:
            yield item


class ExceptionRaisingIterableObject:
    def __init__(self, raise_: bool):
        self.__raise: bool = raise_

    def __iter__(self):
        yield -123

        if self.__raise:
            raise theoretical_testutils.TestException()


class CustomTestListItem:
    def __init__(self, id_: int, name: str):
        self.__id: int = id_
        self.__name: str = name

    def get_id(self) -> int:
        return self.__id

    def get_name(self) -> str:
        return self.__name

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self.__id == other.get_id()) and (self.__name == other.get_name())

        return NotImplemented


__LIST_BLUEPRINT_TEST_SUITE = (
    (ListBlueprint(item_blueprint=IntegerBlueprint(), parsing_mode=ParsingMode.MODE_LOOSE), (
        ([789, -123, 2.5, 4.775, "456", "\r\n-888_222   \t", True, False], [789, -123, 2, 4, 456, -888222, 1, 0]),
        ((789, -123, 2.5, 4.775, "456", "\r\n-888_222   \t", True, False), [789, -123, 2, 4, 456, -888222, 1, 0]),
        ({789, -123, 2.5, 4.775, "456", "\r\n-888_222   \t", True, False}, ignore_order_of_output_list([789, -123, 2, 4, 456, -888222, 1, 0])),
        (frozenset((789, -123, 2.5, 4.775, "456", "\r\n-888_222   \t", True, False)), ignore_order_of_output_list([789, -123, 2, 4, 456, -888222, 1, 0])),
        (
            {789: theoretical_testutils.EmptyObject(), -123: "hello", 2.5: "hello", 4.775: "hello", "456": "hello", "\r\n-888_222   \t": "hello", True: "hello", False: "hello"},
            ignore_order_of_output_list([789, -123, 2, 4, 456, -888222, 1, 0])
        ),
        ([2.001, 2.499, 2.5, 2.501, 2.999, 0.0, -0.0], [2, 2, 2, 2, 2, 0, 0]),
        ("1234567890", [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]),
        (b"\x00\x00\x00\x00", [0, 0, 0, 0]),
        (b"abcdef", [97, 98, 99, 100, 101, 102]),  # list(bytes) returns a list of integers (ASCII values)!
        (bytearray(b"abcdef"), [97, 98, 99, 100, 101, 102]),  # list(bytes) returns a list of integers (ASCII values)!
        (range(5, 15), [5, 6, 7, 8, 9, 10, 11, 12, 13, 14]),
        (sorted((100, 5, 849, 2, -456, 999)), [-456, 2, 5, 100, 849, 999]),
        (sorted("18754522"), [1, 2, 2, 4, 5, 5, 7, 8]),
        (sorted(b"cabfdeee"), [97, 98, 99, 100, 101, 101, 101, 102]),
        (sorted(bytearray(b"cabfdeee")), [97, 98, 99, 100, 101, 101, 101, 102]),
        ((i * i for i in range(10)), [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]),
        (map(lambda x: x + "000", ("1", "2", "3")), [1000, 2000, 3000]),
        (map(lambda x: x ** 2, range(5)), [0, 1, 4, 9, 16]),
        (filter(lambda x: len(x) > 1, ("1", "123", "", "t", "789456", "\r\n9\t")), [123, 789456, 9]),
        (IterableObject([]), []),
        (IterableObject(["-555", 2.999, True, "\v+123_000\f", 999]), [-555, 2, 1, 123000, 999]),
        (IterableObject({"-789": "HelloWorld!", False: theoretical_testutils.EmptyObject(), 5.5: "xyz"}), ignore_order_of_output_list([-789, 0, 5])),
        (IterableObject(range(1, 10, 2)), [1, 3, 5, 7, 9]),
        (IterableObject("886644"), [8, 8, 6, 6, 4, 4]),
        (IterableObject(b"abc"), [97, 98, 99]),
        (IterableObject(bytearray(b"abc")), [97, 98, 99]),
        (ExceptionRaisingIterableObject(raise_=False), [-123]),
        ([], []),
        (tuple(), []),
        (set(), []),
        (dict(), []),
        ("", []),
        (b"", []),
        (("abc" for _ in range(0)), []),
        (("abc" for _ in range(1)), InputDataNotConvertibleExc),
        ((theoretical_testutils.EmptyObject() for _ in range(0)), []),
        ((theoretical_testutils.EmptyObject() for _ in range(1)), InputDataTypeNotInAllowlistExc),
        (map(lambda x: str(x) + "t", (1, 2, 3)), InputDataNotConvertibleExc),
        (map(lambda _: theoretical_testutils.EmptyObject(), (1, 2, 3)), InputDataTypeNotInAllowlistExc),
        ([789, float("inf"), True], InputDataNotConvertibleExc),
        ([789, float("-inf"), True], InputDataNotConvertibleExc),
        ([789, float("nan"), True], InputDataNotConvertibleExc),
        ([789, "", True], InputDataNotConvertibleExc),
        ((789, "", True), InputDataNotConvertibleExc),
        ({789, "", True}, InputDataNotConvertibleExc),
        ({789: "hello", "": "hello", True: theoretical_testutils.EmptyObject()}, InputDataNotConvertibleExc),
        ([789, ipaddress.ip_address("127.0.0.1"), ipaddress.ip_address("::1"), True], InputDataTypeNotInAllowlistExc),
        ([789, theoretical_testutils.EmptyObject(), True], InputDataTypeNotInAllowlistExc),
        ([ipaddress.ip_address("127.0.0.1"), ipaddress.ip_address("::1")], InputDataTypeNotInAllowlistExc),
        ([theoretical_testutils.EmptyObject()], InputDataTypeNotInAllowlistExc),
        ("123a456", InputDataNotConvertibleExc),
        ("-123", InputDataNotConvertibleExc),
        ("123_000", InputDataNotConvertibleExc),
        ("hello", InputDataNotConvertibleExc),
        (None, InputDataNotConvertibleExc),
        (False, InputDataNotConvertibleExc),
        (True, InputDataNotConvertibleExc),
        (-123, InputDataNotConvertibleExc),
        (0, InputDataNotConvertibleExc),
        (123, InputDataNotConvertibleExc),
        (-123.5, InputDataNotConvertibleExc),
        (-0.0, InputDataNotConvertibleExc),
        (0.0, InputDataNotConvertibleExc),
        (123.5, InputDataNotConvertibleExc),
        (float("inf"), InputDataNotConvertibleExc),
        (float("nan"), InputDataNotConvertibleExc),
        (int, InputDataNotConvertibleExc),
        (theoretical_testutils.EmptyObject, InputDataNotConvertibleExc),
        (datetime.datetime.now(), InputDataNotConvertibleExc),
        (datetime.datetime.now().date(), InputDataNotConvertibleExc),
        (datetime.datetime.now().time(), InputDataNotConvertibleExc),
        (ipaddress.ip_address("127.0.0.1"), InputDataNotConvertibleExc),
        (ipaddress.ip_address("::1"), InputDataNotConvertibleExc),
        (ipaddress.ip_network("127.0.0.0/30"), InputDataTypeNotInAllowlistExc),  # ipaddress.ip_network() can be converted to list of IP addresses, but they cannot be converted to int due to the IntegerBlueprint being in rational mode!
        (ipaddress.ip_network("2001:db8::/126"), InputDataTypeNotInAllowlistExc),  # ipaddress.ip_network() can be converted to list of IP addresses, but they cannot be converted to int due to the IntegerBlueprint being in rational mode!
        (urllib.parse.urlparse("https://www.google.cz/test?abc=def"), InputDataNotConvertibleExc),
        (uuid.UUID('{12345678-1234-5678-1234-567812345678}'), InputDataNotConvertibleExc),
        (theoretical_testutils.EmptyObject(), InputDataNotConvertibleExc),
        (IterableObject([1, "", 3]), InputDataNotConvertibleExc),
        (IterableObject([1, "hello", 3]), InputDataNotConvertibleExc),
        (IterableObject([1, theoretical_testutils.EmptyObject, 2]), InputDataTypeNotInAllowlistExc),
        (IterableObject([1, theoretical_testutils.EmptyObject(), 2]), InputDataTypeNotInAllowlistExc),
        (ExceptionRaisingIterableObject(raise_=True), InputDataNotConvertibleExc),
    )),
    (ListBlueprint(item_blueprint=IntegerBlueprint(), parsing_mode=ParsingMode.MODE_RATIONAL), (
        ([789, -123, 2.5, 4.775, "456", "\r\n-888_222   \t", True, False], [789, -123, 2, 4, 456, -888222, 1, 0]),
        ((789, -123, 2.5, 4.775, "456", "\r\n-888_222   \t", True, False), [789, -123, 2, 4, 456, -888222, 1, 0]),
        ({789, -123, 2.5, 4.775, "456", "\r\n-888_222   \t", True, False}, ignore_order_of_output_list([789, -123, 2, 4, 456, -888222, 1, 0])),
        (frozenset((789, -123, 2.5, 4.775, "456", "\r\n-888_222   \t", True, False)), ignore_order_of_output_list([789, -123, 2, 4, 456, -888222, 1, 0])),
        (
            {789: theoretical_testutils.EmptyObject(), -123: "hello", 2.5: "hello", 4.775: "hello", "456": "hello", "\r\n-888_222   \t": "hello", True: "hello", False: "hello"},
            InputDataTypeInBlocklistExc
        ),
        ([2.001, 2.499, 2.5, 2.501, 2.999, 0.0, -0.0], [2, 2, 2, 2, 2, 0, 0]),
        ("1234567890", InputDataTypeInBlocklistExc),
        (b"\x00\x00\x00\x00", InputDataTypeInBlocklistExc),
        (b"abcdef", InputDataTypeInBlocklistExc),
        (bytearray(b"abcdef"), InputDataTypeInBlocklistExc),
        (range(5, 15), [5, 6, 7, 8, 9, 10, 11, 12, 13, 14]),
        (sorted((100, 5, 849, 2, -456, 999)), [-456, 2, 5, 100, 849, 999]),
        (sorted("18754522"), [1, 2, 2, 4, 5, 5, 7, 8]),
        (sorted(b"cabfdeee"), [97, 98, 99, 100, 101, 101, 101, 102]),
        (sorted(bytearray(b"cabfdeee")), [97, 98, 99, 100, 101, 101, 101, 102]),
        ((i * i for i in range(10)), [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]),
        (map(lambda x: x + "000", ("1", "2", "3")), [1000, 2000, 3000]),
        (map(lambda x: x ** 2, range(5)), [0, 1, 4, 9, 16]),
        (filter(lambda x: len(x) > 1, ("1", "123", "", "t", "789456", "\r\n9\t")), [123, 789456, 9]),
        (IterableObject([]), []),
        (IterableObject(["-555", 2.999, True, "\v+123_000\f", 999]), [-555, 2, 1, 123000, 999]),
        (IterableObject({"-789": "HelloWorld!", False: theoretical_testutils.EmptyObject(), 5.5: "xyz"}), ignore_order_of_output_list([-789, 0, 5])),  # The blueprint only sees 'IterableObject', not 'dict', when checking the input data type. However, it's OK that the blueprint accepts it, as it would be unnecessarily complicated to program a check for such very unlikely inputs.
        (IterableObject(range(1, 10, 2)), [1, 3, 5, 7, 9]),
        (IterableObject("886644"), [8, 8, 6, 6, 4, 4]),  # The blueprint only sees 'IterableObject', not 'str', when checking the input data type. However, it's OK that the blueprint accepts it, as it would be unnecessarily complicated to program a check for such very unlikely inputs.
        (IterableObject(b"abc"), [97, 98, 99]),  # The blueprint only sees 'IterableObject', not 'bytes', when checking the input data type. However, it's OK that the blueprint accepts it, as it would be unnecessarily complicated to program a check for such very unlikely inputs.
        (IterableObject(bytearray(b"abc")), [97, 98, 99]),  # The blueprint only sees 'IterableObject', not 'bytearray', when checking the input data type. However, it's OK that the blueprint accepts it, as it would be unnecessarily complicated to program a check for such very unlikely inputs.
        (ExceptionRaisingIterableObject(raise_=False), [-123]),
        ([], []),
        (tuple(), []),
        (set(), []),
        (dict(), InputDataTypeInBlocklistExc),
        ("", InputDataTypeInBlocklistExc),
        (b"", InputDataTypeInBlocklistExc),
        (("abc" for _ in range(0)), []),
        (("abc" for _ in range(1)), InputDataNotConvertibleExc),
        ((theoretical_testutils.EmptyObject() for _ in range(0)), []),
        ((theoretical_testutils.EmptyObject() for _ in range(1)), InputDataTypeNotInAllowlistExc),
        (map(lambda x: str(x) + "t", (1, 2, 3)), InputDataNotConvertibleExc),
        (map(lambda _: theoretical_testutils.EmptyObject(), (1, 2, 3)), InputDataTypeNotInAllowlistExc),
        ([789, float("inf"), True], InputDataNotConvertibleExc),
        ([789, float("-inf"), True], InputDataNotConvertibleExc),
        ([789, float("nan"), True], InputDataNotConvertibleExc),
        ([789, "", True], InputDataNotConvertibleExc),
        ((789, "", True), InputDataNotConvertibleExc),
        ({789, "", True}, InputDataNotConvertibleExc),
        ({789: "hello", "": "hello", True: theoretical_testutils.EmptyObject()}, InputDataTypeInBlocklistExc),
        ([789, ipaddress.ip_address("127.0.0.1"), ipaddress.ip_address("::1"), True], InputDataTypeNotInAllowlistExc),
        ([789, theoretical_testutils.EmptyObject(), True], InputDataTypeNotInAllowlistExc),
        ([ipaddress.ip_address("127.0.0.1"), ipaddress.ip_address("::1")], InputDataTypeNotInAllowlistExc),
        ([theoretical_testutils.EmptyObject()], InputDataTypeNotInAllowlistExc),
        ("123a456", InputDataTypeInBlocklistExc),
        ("-123", InputDataTypeInBlocklistExc),
        ("123_000", InputDataTypeInBlocklistExc),
        ("hello", InputDataTypeInBlocklistExc),
        (None, InputDataNotConvertibleExc),
        (False, InputDataNotConvertibleExc),
        (True, InputDataNotConvertibleExc),
        (-123, InputDataNotConvertibleExc),
        (0, InputDataNotConvertibleExc),
        (123, InputDataNotConvertibleExc),
        (-123.5, InputDataNotConvertibleExc),
        (-0.0, InputDataNotConvertibleExc),
        (0.0, InputDataNotConvertibleExc),
        (123.5, InputDataNotConvertibleExc),
        (float("inf"), InputDataNotConvertibleExc),
        (float("nan"), InputDataNotConvertibleExc),
        (int, InputDataNotConvertibleExc),
        (theoretical_testutils.EmptyObject, InputDataNotConvertibleExc),
        (datetime.datetime.now(), InputDataNotConvertibleExc),
        (datetime.datetime.now().date(), InputDataNotConvertibleExc),
        (datetime.datetime.now().time(), InputDataNotConvertibleExc),
        (ipaddress.ip_address("127.0.0.1"), InputDataNotConvertibleExc),
        (ipaddress.ip_address("::1"), InputDataNotConvertibleExc),
        (ipaddress.ip_network("127.0.0.0/30"), InputDataTypeNotInAllowlistExc),  # ipaddress.ip_network() can be converted to list of IP addresses, but they cannot be converted to int due to the IntegerBlueprint being in rational mode!
        (ipaddress.ip_network("2001:db8::/126"), InputDataTypeNotInAllowlistExc),  # ipaddress.ip_network() can be converted to list of IP addresses, but they cannot be converted to int due to the IntegerBlueprint being in rational mode!
        (urllib.parse.urlparse("https://www.google.cz/test?abc=def"), InputDataNotConvertibleExc),
        (uuid.UUID('{12345678-1234-5678-1234-567812345678}'), InputDataNotConvertibleExc),
        (theoretical_testutils.EmptyObject(), InputDataNotConvertibleExc),
        (IterableObject([1, "", 3]), InputDataNotConvertibleExc),
        (IterableObject([1, "hello", 3]), InputDataNotConvertibleExc),
        (IterableObject([1, theoretical_testutils.EmptyObject, 2]), InputDataTypeNotInAllowlistExc),
        (IterableObject([1, theoretical_testutils.EmptyObject(), 2]), InputDataTypeNotInAllowlistExc),
        (ExceptionRaisingIterableObject(raise_=True), InputDataNotConvertibleExc),
    )),
    (ListBlueprint(item_blueprint=IntegerBlueprint(), parsing_mode=ParsingMode.MODE_STRICT), (
        ([789, -123, 2.5, 4.775, "456", "\r\n-888_222   \t", True, False], [789, -123, 2, 4, 456, -888222, 1, 0]),
        ((789, -123, 2.5, 4.775, "456", "\r\n-888_222   \t", True, False), [789, -123, 2, 4, 456, -888222, 1, 0]),
        ({789, -123, 2.5, 4.775, "456", "\r\n-888_222   \t", True, False}, ignore_order_of_output_list([789, -123, 2, 4, 456, -888222, 1, 0])),
        (frozenset((789, -123, 2.5, 4.775, "456", "\r\n-888_222   \t", True, False)), ignore_order_of_output_list([789, -123, 2, 4, 456, -888222, 1, 0])),
        (
            {789: theoretical_testutils.EmptyObject(), -123: "hello", 2.5: "hello", 4.775: "hello", "456": "hello", "\r\n-888_222   \t": "hello", True: "hello", False: "hello"},
            InputDataTypeNotInAllowlistExc
        ),
        ([2.001, 2.499, 2.5, 2.501, 2.999, 0.0, -0.0], [2, 2, 2, 2, 2, 0, 0]),
        ("1234567890", InputDataTypeNotInAllowlistExc),
        (b"\x00\x00\x00\x00", InputDataTypeNotInAllowlistExc),
        (b"abcdef", InputDataTypeNotInAllowlistExc),
        (bytearray(b"abcdef"), InputDataTypeNotInAllowlistExc),
        (range(5, 15), InputDataTypeNotInAllowlistExc),
        (sorted((100, 5, 849, 2, -456, 999)), [-456, 2, 5, 100, 849, 999]),  # sorted() returns a list object no matter what its input iterable was!
        (sorted("18754522"), [1, 2, 2, 4, 5, 5, 7, 8]),  # sorted() returns a list object no matter what its input iterable was!
        (sorted(b"cabfdeee"), [97, 98, 99, 100, 101, 101, 101, 102]),  # sorted() returns a list object no matter what its input iterable was!
        (sorted(bytearray(b"cabfdeee")), [97, 98, 99, 100, 101, 101, 101, 102]),  # sorted() returns a list object no matter what its input iterable was!
        ((i * i for i in range(10)), InputDataTypeNotInAllowlistExc),
        (map(lambda x: x + "000", ("1", "2", "3")), InputDataTypeNotInAllowlistExc),
        (map(lambda x: x ** 2, range(5)), InputDataTypeNotInAllowlistExc),
        (filter(lambda x: len(x) > 1, ("1", "123", "", "t", "789456", "\r\n9\t")), InputDataTypeNotInAllowlistExc),
        (IterableObject([]), InputDataTypeNotInAllowlistExc),
        (IterableObject(["-555", 2.999, True, "\v+123_000\f", 999]), InputDataTypeNotInAllowlistExc),
        (IterableObject({"-789": "HelloWorld!", False: theoretical_testutils.EmptyObject(), 5.5: "xyz"}), InputDataTypeNotInAllowlistExc),
        (IterableObject(range(1, 10, 2)), InputDataTypeNotInAllowlistExc),
        (IterableObject("886644"), InputDataTypeNotInAllowlistExc),
        (IterableObject(b"abc"), InputDataTypeNotInAllowlistExc),
        (IterableObject(bytearray(b"abc")), InputDataTypeNotInAllowlistExc),
        (ExceptionRaisingIterableObject(raise_=False), InputDataTypeNotInAllowlistExc),
        ([], []),
        (tuple(), []),
        (set(), []),
        (dict(), InputDataTypeNotInAllowlistExc),
        ("", InputDataTypeNotInAllowlistExc),
        (b"", InputDataTypeNotInAllowlistExc),
        (("abc" for _ in range(0)), InputDataTypeNotInAllowlistExc),
        (("abc" for _ in range(1)), InputDataTypeNotInAllowlistExc),
        ((theoretical_testutils.EmptyObject() for _ in range(0)), InputDataTypeNotInAllowlistExc),
        ((theoretical_testutils.EmptyObject() for _ in range(1)), InputDataTypeNotInAllowlistExc),
        (map(lambda x: str(x) + "t", (1, 2, 3)), InputDataTypeNotInAllowlistExc),
        (map(lambda _: theoretical_testutils.EmptyObject(), (1, 2, 3)), InputDataTypeNotInAllowlistExc),
        ([789, float("inf"), True], InputDataNotConvertibleExc),
        ([789, float("-inf"), True], InputDataNotConvertibleExc),
        ([789, float("nan"), True], InputDataNotConvertibleExc),
        ([789, "", True], InputDataNotConvertibleExc),
        ((789, "", True), InputDataNotConvertibleExc),
        ({789, "", True}, InputDataNotConvertibleExc),
        ({789: "hello", "": "hello", True: theoretical_testutils.EmptyObject()}, InputDataTypeNotInAllowlistExc),
        ([789, ipaddress.ip_address("127.0.0.1"), ipaddress.ip_address("::1"), True], InputDataTypeNotInAllowlistExc),
        ([789, theoretical_testutils.EmptyObject(), True], InputDataTypeNotInAllowlistExc),
        ([ipaddress.ip_address("127.0.0.1"), ipaddress.ip_address("::1")], InputDataTypeNotInAllowlistExc),
        ([theoretical_testutils.EmptyObject()], InputDataTypeNotInAllowlistExc),
        ("123a456", InputDataTypeNotInAllowlistExc),
        ("-123", InputDataTypeNotInAllowlistExc),
        ("123_000", InputDataTypeNotInAllowlistExc),
        ("hello", InputDataTypeNotInAllowlistExc),
        (None, InputDataTypeNotInAllowlistExc),
        (False, InputDataTypeNotInAllowlistExc),
        (True, InputDataTypeNotInAllowlistExc),
        (-123, InputDataTypeNotInAllowlistExc),
        (0, InputDataTypeNotInAllowlistExc),
        (123, InputDataTypeNotInAllowlistExc),
        (-123.5, InputDataTypeNotInAllowlistExc),
        (-0.0, InputDataTypeNotInAllowlistExc),
        (0.0, InputDataTypeNotInAllowlistExc),
        (123.5, InputDataTypeNotInAllowlistExc),
        (float("inf"), InputDataTypeNotInAllowlistExc),
        (float("nan"), InputDataTypeNotInAllowlistExc),
        (int, InputDataTypeNotInAllowlistExc),
        (theoretical_testutils.EmptyObject, InputDataTypeNotInAllowlistExc),
        (datetime.datetime.now(), InputDataTypeNotInAllowlistExc),
        (datetime.datetime.now().date(), InputDataTypeNotInAllowlistExc),
        (datetime.datetime.now().time(), InputDataTypeNotInAllowlistExc),
        (ipaddress.ip_address("127.0.0.1"), InputDataTypeNotInAllowlistExc),
        (ipaddress.ip_address("::1"), InputDataTypeNotInAllowlistExc),
        (ipaddress.ip_network("127.0.0.0/30"), InputDataTypeNotInAllowlistExc),
        (ipaddress.ip_network("2001:db8::/126"), InputDataTypeNotInAllowlistExc),
        (urllib.parse.urlparse("https://www.google.cz/test?abc=def"), InputDataNotConvertibleExc),  # ParseResult is a subclass of tuple!!!
        (uuid.UUID('{12345678-1234-5678-1234-567812345678}'), InputDataTypeNotInAllowlistExc),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc),
        (IterableObject([1, "", 3]), InputDataTypeNotInAllowlistExc),
        (IterableObject([1, "hello", 3]), InputDataTypeNotInAllowlistExc),
        (IterableObject([1, theoretical_testutils.EmptyObject, 2]), InputDataTypeNotInAllowlistExc),
        (IterableObject([1, theoretical_testutils.EmptyObject(), 2]), InputDataTypeNotInAllowlistExc),
        (ExceptionRaisingIterableObject(raise_=True), InputDataTypeNotInAllowlistExc),
    )),
    (ListBlueprint(item_blueprint=StringBlueprint(), parsing_mode=ParsingMode.MODE_LOOSE), (
        ([789, -123, 2.5, 4.775, "456", "\r\n-888_222   \t", True, False], ["789", "-123", "2.5", "4.775", "456", "\r\n-888_222   \t", "True", "False"]),
        ((789, -123, 2.5, 4.775, "456", "\r\n-888_222   \t", True, False), ["789", "-123", "2.5", "4.775", "456", "\r\n-888_222   \t", "True", "False"]),
        ({789, -123, 2.5, 4.775, "456", "\r\n-888_222   \t", True, False}, ignore_order_of_output_list(["789", "-123", "2.5", "4.775", "456", "\r\n-888_222   \t", "True", "False"])),
        (frozenset((789, -123, 2.5, 4.775, "456", "\r\n-888_222   \t", True, False)), ignore_order_of_output_list(["789", "-123", "2.5", "4.775", "456", "\r\n-888_222   \t", "True", "False"])),
        (
            {789: theoretical_testutils.EmptyObject(), -123: "hello", 2.5: "hello", 4.775: "hello", "456": "hello", "\r\n-888_222   \t": "hello", True: "hello", False: "hello"},
            ignore_order_of_output_list(["789", "-123", "2.5", "4.775", "456", "\r\n-888_222   \t", "True", "False"])
        ),
        ([2.001, 2.499, 2.5, 2.501, 2.999, 0.0, -0.0], ["2.001", "2.499", "2.5", "2.501", "2.999", "0.0", "-0.0"]),
        ("1234567890", ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]),
        (b"\x00\x00\x00\x00", ["0", "0", "0", "0"]),
        (b"abcdef", ["97", "98", "99", "100", "101", "102"]),  # list(bytes) returns a list of integers (ASCII values)!
        (bytearray(b"abcdef"), ["97", "98", "99", "100", "101", "102"]),  # list(bytes) returns a list of integers (ASCII values)!
        (range(5, 15), ["5", "6", "7", "8", "9", "10", "11", "12", "13", "14"]),
        (sorted((100, 5, 849, 2, -456, 999)), ["-456", "2", "5", "100", "849", "999"]),
        (sorted("18754522"), ["1", "2", "2", "4", "5", "5", "7", "8"]),
        (sorted(b"cabfdeee"), ["97", "98", "99", "100", "101", "101", "101", "102"]),
        (sorted(bytearray(b"cabfdeee")), ["97", "98", "99", "100", "101", "101", "101", "102"]),
        ((i * i for i in range(10)), ["0", "1", "4", "9", "16", "25", "36", "49", "64", "81"]),
        (map(lambda x: x + "000", ("1", "2", "3")), ["1000", "2000", "3000"]),
        (map(lambda x: x ** 2, range(5)), ["0", "1", "4", "9", "16"]),
        (filter(lambda x: len(x) > 1, ("1", "123", "", "t", "789456", "\r\n9\t")), ["123", "789456", "\r\n9\t"]),
        (IterableObject([]), []),
        (IterableObject(["-555", 2.999, True, "\v+123_000\f", 999]), ["-555", "2.999", "True", "\v+123_000\f", "999"]),
        (IterableObject({"-789": "HelloWorld!", False: theoretical_testutils.EmptyObject(), 5.5: "xyz"}), ignore_order_of_output_list(["-789", "False", "5.5"])),
        (IterableObject(range(1, 10, 2)), ["1", "3", "5", "7", "9"]),
        (IterableObject("886644"), ["8", "8", "6", "6", "4", "4"]),
        (IterableObject(b"abc"), ["97", "98", "99"]),
        (IterableObject(bytearray(b"abc")), ["97", "98", "99"]),
        (ExceptionRaisingIterableObject(raise_=False), ["-123"]),
        ([], []),
        (tuple(), []),
        (set(), []),
        (dict(), []),
        ("", []),
        (b"", []),
        (("abc" for _ in range(0)), []),
        (("abc" for _ in range(1)), ["abc"]),
        ((theoretical_testutils.EmptyObject() for _ in range(0)), []),
        ((theoretical_testutils.EmptyObject() for _ in range(1)), InputDataTypeNotInAllowlistExc),
        (map(lambda x: str(x) + "t", (1, 2, 3)), ["1t", "2t", "3t"]),
        (map(lambda _: theoretical_testutils.EmptyObject(), (1, 2, 3)), InputDataTypeNotInAllowlistExc),
        ([789, float("inf"), True], ["789", "inf", "True"]),
        ([789, float("-inf"), True], ["789", "-inf", "True"]),
        ([789, float("nan"), True], ["789", "nan", "True"]),
        ([789, "", True], ["789", "", "True"]),
        ((789, "", True), ["789", "", "True"]),
        ({789, "", True}, ignore_order_of_output_list(["789", "", "True"])),
        ([789, "Hello World!", True], ["789", "Hello World!", "True"]),
        ((789, "Hello World!", True), ["789", "Hello World!", "True"]),
        ({789, "Hello World!", True}, ignore_order_of_output_list(["789", "Hello World!", "True"])),
        ({789: "hello", "": "hello", True: theoretical_testutils.EmptyObject()}, ignore_order_of_output_list(["789", "", "True"])),
        ([789, ipaddress.ip_address("127.0.0.1"), ipaddress.ip_address("::1"), True], ["789", "127.0.0.1", "::1", "True"]),
        ([789, theoretical_testutils.EmptyObject(), True], InputDataTypeNotInAllowlistExc),
        ([ipaddress.ip_address("127.0.0.1"), ipaddress.ip_address("::1")], ["127.0.0.1", "::1"]),
        ([theoretical_testutils.EmptyObject()], InputDataTypeNotInAllowlistExc),
        ("123a456", ["1", "2", "3", "a", "4", "5", "6"]),
        ("-123", ["-", "1", "2", "3"]),
        ("123_000", ["1", "2", "3", "_", "0", "0", "0"]),
        ("hello", ["h", "e", "l", "l", "o"]),
        (None, InputDataNotConvertibleExc),
        (False, InputDataNotConvertibleExc),
        (True, InputDataNotConvertibleExc),
        (-123, InputDataNotConvertibleExc),
        (0, InputDataNotConvertibleExc),
        (123, InputDataNotConvertibleExc),
        (-123.5, InputDataNotConvertibleExc),
        (-0.0, InputDataNotConvertibleExc),
        (0.0, InputDataNotConvertibleExc),
        (123.5, InputDataNotConvertibleExc),
        (float("inf"), InputDataNotConvertibleExc),
        (float("nan"), InputDataNotConvertibleExc),
        (int, InputDataNotConvertibleExc),
        (theoretical_testutils.EmptyObject, InputDataNotConvertibleExc),
        (datetime.datetime.now(), InputDataNotConvertibleExc),
        (datetime.datetime.now().date(), InputDataNotConvertibleExc),
        (datetime.datetime.now().time(), InputDataNotConvertibleExc),
        (ipaddress.ip_address("127.0.0.1"), InputDataNotConvertibleExc),
        (ipaddress.ip_address("::1"), InputDataNotConvertibleExc),
        (ipaddress.ip_network("127.0.0.0/30"), ["127.0.0.0", "127.0.0.1", "127.0.0.2", "127.0.0.3"]),
        (ipaddress.ip_network("2001:db8::/126"), ["2001:db8::", "2001:db8::1", "2001:db8::2", "2001:db8::3"]),
        (urllib.parse.urlparse("https://www.google.cz/test?abc=def"), ["https", "www.google.cz", "/test", "", "abc=def", ""]),
        (uuid.UUID('{12345678-1234-5678-1234-567812345678}'), InputDataNotConvertibleExc),
        (theoretical_testutils.EmptyObject(), InputDataNotConvertibleExc),
        (IterableObject([1, "", 3]), ["1", "", "3"]),
        (IterableObject([1, "hello", 3]), ["1", "hello", "3"]),
        (IterableObject([1, theoretical_testutils.EmptyObject, 2]), InputDataTypeNotInAllowlistExc),
        (IterableObject([1, theoretical_testutils.EmptyObject(), 2]), InputDataTypeNotInAllowlistExc),
        (ExceptionRaisingIterableObject(raise_=True), InputDataNotConvertibleExc),
    )),
    (ListBlueprint(item_blueprint=StringBlueprint(), parsing_mode=ParsingMode.MODE_RATIONAL), (
        ([789, -123, 2.5, 4.775, "456", "\r\n-888_222   \t", True, False], ["789", "-123", "2.5", "4.775", "456", "\r\n-888_222   \t", "True", "False"]),
        ((789, -123, 2.5, 4.775, "456", "\r\n-888_222   \t", True, False), ["789", "-123", "2.5", "4.775", "456", "\r\n-888_222   \t", "True", "False"]),
        ({789, -123, 2.5, 4.775, "456", "\r\n-888_222   \t", True, False}, ignore_order_of_output_list(["789", "-123", "2.5", "4.775", "456", "\r\n-888_222   \t", "True", "False"])),
        (frozenset((789, -123, 2.5, 4.775, "456", "\r\n-888_222   \t", True, False)), ignore_order_of_output_list(["789", "-123", "2.5", "4.775", "456", "\r\n-888_222   \t", "True", "False"])),
        (
            {789: theoretical_testutils.EmptyObject(), -123: "hello", 2.5: "hello", 4.775: "hello", "456": "hello", "\r\n-888_222   \t": "hello", True: "hello", False: "hello"},
            InputDataTypeInBlocklistExc
        ),
        ([2.001, 2.499, 2.5, 2.501, 2.999, 0.0, -0.0], ["2.001", "2.499", "2.5", "2.501", "2.999", "0.0", "-0.0"]),
        ("1234567890", InputDataTypeInBlocklistExc),
        (b"\x00\x00\x00\x00", InputDataTypeInBlocklistExc),
        (b"abcdef", InputDataTypeInBlocklistExc),  # list(bytes) returns a list of integers (ASCII values)!
        (bytearray(b"abcdef"), InputDataTypeInBlocklistExc),  # list(bytes) returns a list of integers (ASCII values)!
        (range(5, 15), ["5", "6", "7", "8", "9", "10", "11", "12", "13", "14"]),
        (sorted((100, 5, 849, 2, -456, 999)), ["-456", "2", "5", "100", "849", "999"]),
        (sorted("18754522"), ["1", "2", "2", "4", "5", "5", "7", "8"]),
        (sorted(b"cabfdeee"), ["97", "98", "99", "100", "101", "101", "101", "102"]),
        (sorted(bytearray(b"cabfdeee")), ["97", "98", "99", "100", "101", "101", "101", "102"]),
        ((i * i for i in range(10)), ["0", "1", "4", "9", "16", "25", "36", "49", "64", "81"]),
        (map(lambda x: x + "000", ("1", "2", "3")), ["1000", "2000", "3000"]),
        (map(lambda x: x ** 2, range(5)), ["0", "1", "4", "9", "16"]),
        (filter(lambda x: len(x) > 1, ("1", "123", "", "t", "789456", "\r\n9\t")), ["123", "789456", "\r\n9\t"]),
        (IterableObject([]), []),
        (IterableObject(["-555", 2.999, True, "\v+123_000\f", 999]), ["-555", "2.999", "True", "\v+123_000\f", "999"]),
        (IterableObject({"-789": "HelloWorld!", False: theoretical_testutils.EmptyObject(), 5.5: "xyz"}), ignore_order_of_output_list(["-789", "False", "5.5"])),
        (IterableObject(range(1, 10, 2)), ["1", "3", "5", "7", "9"]),
        (IterableObject("886644"), ["8", "8", "6", "6", "4", "4"]),
        (IterableObject(b"abc"), ["97", "98", "99"]),
        (IterableObject(bytearray(b"abc")), ["97", "98", "99"]),
        (ExceptionRaisingIterableObject(raise_=False), ["-123"]),
        ([], []),
        (tuple(), []),
        (set(), []),
        (dict(), InputDataTypeInBlocklistExc),
        ("", InputDataTypeInBlocklistExc),
        (b"", InputDataTypeInBlocklistExc),
        (("abc" for _ in range(0)), []),
        (("abc" for _ in range(1)), ["abc"]),
        ((theoretical_testutils.EmptyObject() for _ in range(0)), []),
        ((theoretical_testutils.EmptyObject() for _ in range(1)), InputDataTypeNotInAllowlistExc),
        (map(lambda x: str(x) + "t", (1, 2, 3)), ["1t", "2t", "3t"]),
        (map(lambda _: theoretical_testutils.EmptyObject(), (1, 2, 3)), InputDataTypeNotInAllowlistExc),
        ([789, float("inf"), True], ["789", "inf", "True"]),
        ([789, float("-inf"), True], ["789", "-inf", "True"]),
        ([789, float("nan"), True], ["789", "nan", "True"]),
        ([789, "", True], ["789", "", "True"]),
        ((789, "", True), ["789", "", "True"]),
        ({789, "", True}, ignore_order_of_output_list(["789", "", "True"])),
        ([789, "Hello World!", True], ["789", "Hello World!", "True"]),
        ((789, "Hello World!", True), ["789", "Hello World!", "True"]),
        ({789, "Hello World!", True}, ignore_order_of_output_list(["789", "Hello World!", "True"])),
        ({789: "hello", "": "hello", True: theoretical_testutils.EmptyObject()}, InputDataTypeInBlocklistExc),
        ([789, ipaddress.ip_address("127.0.0.1"), ipaddress.ip_address("::1"), True], ["789", "127.0.0.1", "::1", "True"]),
        ([789, theoretical_testutils.EmptyObject(), True], InputDataTypeNotInAllowlistExc),
        ([ipaddress.ip_address("127.0.0.1"), ipaddress.ip_address("::1")], ["127.0.0.1", "::1"]),
        ([theoretical_testutils.EmptyObject()], InputDataTypeNotInAllowlistExc),
        ("123a456", InputDataTypeInBlocklistExc),
        ("-123", InputDataTypeInBlocklistExc),
        ("123_000", InputDataTypeInBlocklistExc),
        ("hello", InputDataTypeInBlocklistExc),
        (None, InputDataNotConvertibleExc),
        (False, InputDataNotConvertibleExc),
        (True, InputDataNotConvertibleExc),
        (-123, InputDataNotConvertibleExc),
        (0, InputDataNotConvertibleExc),
        (123, InputDataNotConvertibleExc),
        (-123.5, InputDataNotConvertibleExc),
        (-0.0, InputDataNotConvertibleExc),
        (0.0, InputDataNotConvertibleExc),
        (123.5, InputDataNotConvertibleExc),
        (float("inf"), InputDataNotConvertibleExc),
        (float("nan"), InputDataNotConvertibleExc),
        (int, InputDataNotConvertibleExc),
        (theoretical_testutils.EmptyObject, InputDataNotConvertibleExc),
        (datetime.datetime.now(), InputDataNotConvertibleExc),
        (datetime.datetime.now().date(), InputDataNotConvertibleExc),
        (datetime.datetime.now().time(), InputDataNotConvertibleExc),
        (ipaddress.ip_address("127.0.0.1"), InputDataNotConvertibleExc),
        (ipaddress.ip_address("::1"), InputDataNotConvertibleExc),
        (ipaddress.ip_network("127.0.0.0/30"), ["127.0.0.0", "127.0.0.1", "127.0.0.2", "127.0.0.3"]),
        (ipaddress.ip_network("2001:db8::/126"), ["2001:db8::", "2001:db8::1", "2001:db8::2", "2001:db8::3"]),
        (urllib.parse.urlparse("https://www.google.cz/test?abc=def"), ["https", "www.google.cz", "/test", "", "abc=def", ""]),
        (uuid.UUID('{12345678-1234-5678-1234-567812345678}'), InputDataNotConvertibleExc),
        (theoretical_testutils.EmptyObject(), InputDataNotConvertibleExc),
        (IterableObject([1, "", 3]), ["1", "", "3"]),
        (IterableObject([1, "hello", 3]), ["1", "hello", "3"]),
        (IterableObject([1, theoretical_testutils.EmptyObject, 2]), InputDataTypeNotInAllowlistExc),
        (IterableObject([1, theoretical_testutils.EmptyObject(), 2]), InputDataTypeNotInAllowlistExc),
        (ExceptionRaisingIterableObject(raise_=True), InputDataNotConvertibleExc),
    )),
    (ListBlueprint(item_blueprint=StringBlueprint(), parsing_mode=ParsingMode.MODE_STRICT), (
        ([789, -123, 2.5, 4.775, "456", "\r\n-888_222   \t", True, False], ["789", "-123", "2.5", "4.775", "456", "\r\n-888_222   \t", "True", "False"]),
        ((789, -123, 2.5, 4.775, "456", "\r\n-888_222   \t", True, False), ["789", "-123", "2.5", "4.775", "456", "\r\n-888_222   \t", "True", "False"]),
        ({789, -123, 2.5, 4.775, "456", "\r\n-888_222   \t", True, False}, ignore_order_of_output_list(["789", "-123", "2.5", "4.775", "456", "\r\n-888_222   \t", "True", "False"])),
        (frozenset((789, -123, 2.5, 4.775, "456", "\r\n-888_222   \t", True, False)), ignore_order_of_output_list(["789", "-123", "2.5", "4.775", "456", "\r\n-888_222   \t", "True", "False"])),
        (
            {789: theoretical_testutils.EmptyObject(), -123: "hello", 2.5: "hello", 4.775: "hello", "456": "hello", "\r\n-888_222   \t": "hello", True: "hello", False: "hello"},
            InputDataTypeNotInAllowlistExc
        ),
        ([2.001, 2.499, 2.5, 2.501, 2.999, 0.0, -0.0], ["2.001", "2.499", "2.5", "2.501", "2.999", "0.0", "-0.0"]),
        ("1234567890", InputDataTypeNotInAllowlistExc),
        (b"\x00\x00\x00\x00", InputDataTypeNotInAllowlistExc),
        (b"abcdef", InputDataTypeNotInAllowlistExc),  # list(bytes) returns a list of integers (ASCII values)!
        (bytearray(b"abcdef"), InputDataTypeNotInAllowlistExc),  # list(bytes) returns a list of integers (ASCII values)!
        (range(5, 15), InputDataTypeNotInAllowlistExc),
        (sorted((100, 5, 849, 2, -456, 999)), ["-456", "2", "5", "100", "849", "999"]),
        (sorted("18754522"), ["1", "2", "2", "4", "5", "5", "7", "8"]),
        (sorted(b"cabfdeee"), ["97", "98", "99", "100", "101", "101", "101", "102"]),
        (sorted(bytearray(b"cabfdeee")), ["97", "98", "99", "100", "101", "101", "101", "102"]),
        ((i * i for i in range(10)), InputDataTypeNotInAllowlistExc),
        (map(lambda x: x + "000", ("1", "2", "3")), InputDataTypeNotInAllowlistExc),
        (map(lambda x: x ** 2, range(5)), InputDataTypeNotInAllowlistExc),
        (filter(lambda x: len(x) > 1, ("1", "123", "", "t", "789456", "\r\n9\t")), InputDataTypeNotInAllowlistExc),
        (IterableObject([]), InputDataTypeNotInAllowlistExc),
        (IterableObject(["-555", 2.999, True, "\v+123_000\f", 999]), InputDataTypeNotInAllowlistExc),
        (IterableObject({"-789": "HelloWorld!", False: theoretical_testutils.EmptyObject(), 5.5: "xyz"}), InputDataTypeNotInAllowlistExc),
        (IterableObject(range(1, 10, 2)), InputDataTypeNotInAllowlistExc),
        (IterableObject("886644"), InputDataTypeNotInAllowlistExc),
        (IterableObject(b"abc"), InputDataTypeNotInAllowlistExc),
        (IterableObject(bytearray(b"abc")), InputDataTypeNotInAllowlistExc),
        (ExceptionRaisingIterableObject(raise_=False), InputDataTypeNotInAllowlistExc),
        ([], []),
        (tuple(), []),
        (set(), []),
        (dict(), InputDataTypeNotInAllowlistExc),
        ("", InputDataTypeNotInAllowlistExc),
        (b"", InputDataTypeNotInAllowlistExc),
        (("abc" for _ in range(0)), InputDataTypeNotInAllowlistExc),
        (("abc" for _ in range(1)), InputDataTypeNotInAllowlistExc),
        ((theoretical_testutils.EmptyObject() for _ in range(0)), InputDataTypeNotInAllowlistExc),
        ((theoretical_testutils.EmptyObject() for _ in range(1)), InputDataTypeNotInAllowlistExc),
        (map(lambda x: str(x) + "t", (1, 2, 3)), InputDataTypeNotInAllowlistExc),
        (map(lambda _: theoretical_testutils.EmptyObject(), (1, 2, 3)), InputDataTypeNotInAllowlistExc),
        ([789, float("inf"), True], ["789", "inf", "True"]),
        ([789, float("-inf"), True], ["789", "-inf", "True"]),
        ([789, float("nan"), True], ["789", "nan", "True"]),
        ([789, "", True], ["789", "", "True"]),
        ((789, "", True), ["789", "", "True"]),
        ({789, "", True}, ignore_order_of_output_list(["789", "", "True"])),
        ([789, "Hello World!", True], ["789", "Hello World!", "True"]),
        ((789, "Hello World!", True), ["789", "Hello World!", "True"]),
        ({789, "Hello World!", True}, ignore_order_of_output_list(["789", "Hello World!", "True"])),
        ({789: "hello", "": "hello", True: theoretical_testutils.EmptyObject()}, InputDataTypeNotInAllowlistExc),
        ([789, ipaddress.ip_address("127.0.0.1"), ipaddress.ip_address("::1"), True], ["789", "127.0.0.1", "::1", "True"]),
        ([789, theoretical_testutils.EmptyObject(), True], InputDataTypeNotInAllowlistExc),
        ([ipaddress.ip_address("127.0.0.1"), ipaddress.ip_address("::1")], ["127.0.0.1", "::1"]),
        ([theoretical_testutils.EmptyObject()], InputDataTypeNotInAllowlistExc),
        ("123a456", InputDataTypeNotInAllowlistExc),
        ("-123", InputDataTypeNotInAllowlistExc),
        ("123_000", InputDataTypeNotInAllowlistExc),
        ("hello", InputDataTypeNotInAllowlistExc),
        (None, InputDataTypeNotInAllowlistExc),
        (False, InputDataTypeNotInAllowlistExc),
        (True, InputDataTypeNotInAllowlistExc),
        (-123, InputDataTypeNotInAllowlistExc),
        (0, InputDataTypeNotInAllowlistExc),
        (123, InputDataTypeNotInAllowlistExc),
        (-123.5, InputDataTypeNotInAllowlistExc),
        (-0.0, InputDataTypeNotInAllowlistExc),
        (0.0, InputDataTypeNotInAllowlistExc),
        (123.5, InputDataTypeNotInAllowlistExc),
        (float("inf"), InputDataTypeNotInAllowlistExc),
        (float("nan"), InputDataTypeNotInAllowlistExc),
        (int, InputDataTypeNotInAllowlistExc),
        (theoretical_testutils.EmptyObject, InputDataTypeNotInAllowlistExc),
        (datetime.datetime.now(), InputDataTypeNotInAllowlistExc),
        (datetime.datetime.now().date(), InputDataTypeNotInAllowlistExc),
        (datetime.datetime.now().time(), InputDataTypeNotInAllowlistExc),
        (ipaddress.ip_address("127.0.0.1"), InputDataTypeNotInAllowlistExc),
        (ipaddress.ip_address("::1"), InputDataTypeNotInAllowlistExc),
        (ipaddress.ip_network("127.0.0.0/30"), InputDataTypeNotInAllowlistExc),
        (ipaddress.ip_network("2001:db8::/126"), InputDataTypeNotInAllowlistExc),
        (urllib.parse.urlparse("https://www.google.cz/test?abc=def"), ["https", "www.google.cz", "/test", "", "abc=def", ""]),  # ParseResult is a subclass of tuple!!!
        (uuid.UUID('{12345678-1234-5678-1234-567812345678}'), InputDataTypeNotInAllowlistExc),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc),
        (IterableObject([1, "", 3]), InputDataTypeNotInAllowlistExc),
        (IterableObject([1, "hello", 3]), InputDataTypeNotInAllowlistExc),
        (IterableObject([1, theoretical_testutils.EmptyObject, 2]), InputDataTypeNotInAllowlistExc),
        (IterableObject([1, theoretical_testutils.EmptyObject(), 2]), InputDataTypeNotInAllowlistExc),
        (ExceptionRaisingIterableObject(raise_=True), InputDataTypeNotInAllowlistExc),
    )),
    (ListBlueprint(item_blueprint=IntegerBlueprint(), filters=(ListDeduplicateItemsFilter(),)), (
        (["1", 2, 3.1], [1, 2, 3]),
        (range(10), [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
        (["1", True, 2.9, "\r\n2\t", "\v\f   3   ", 3], [1, 2, 3]),
        ((float(i % 2) for i in range(20)), [0, 1]),
        ([1, 2, 2, 2, 3, 3, 4], [1, 2, 3, 4]),
        (theoretical_testutils.EmptyObject(), InputDataNotConvertibleExc),
        ([theoretical_testutils.EmptyObject()], InputDataTypeNotInAllowlistExc),
    )),
    (ListBlueprint(item_blueprint=IntegerBlueprint(), filters=(ListSortFilter(None, reverse_order=False),)), (
        ([], []),
        ([123], [123]),
        ([100, True, -100, "\r\n000_3  ", 0, 2.999, 4, "6", 5], [-100, 0, 1, 2, 3, 4, 5, 6, 100]),
        (range(10, 0, -1), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
        ([1, 1, 2, 1, 3, 5, 4, 4, 5, 2, 3], [1, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5]),
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),
        ((str(i) for i in range(10)), [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
        (theoretical_testutils.EmptyObject(), InputDataNotConvertibleExc),
        ([theoretical_testutils.EmptyObject()], InputDataTypeNotInAllowlistExc),
    )),
    (ListBlueprint(item_blueprint=IntegerBlueprint(), filters=(ListSortFilter(None, reverse_order=True),)), (
        ([], []),
        ([123], [123]),
        ([100, True, -100, "\r\n000_3  ", 0, 2.999, 4, "6", 5], [100, 6, 5, 4, 3, 2, 1, 0, -100]),
        (range(10, 0, -1), [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]),
        ([1, 1, 2, 1, 3, 5, 4, 4, 5, 2, 3], [5, 5, 4, 4, 3, 3, 2, 2, 1, 1, 1]),
        ([1, 2, 3, 4, 5], [5, 4, 3, 2, 1]),
        ((str(i) for i in range(10)), [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]),
        (theoretical_testutils.EmptyObject(), InputDataNotConvertibleExc),
        ([theoretical_testutils.EmptyObject()], InputDataTypeNotInAllowlistExc),
    )),
    (ListBlueprint(item_blueprint=GenericBlueprint(), filters=(ListSortFilter(lambda item: item.get_id(), reverse_order=False),)), (
        ([], []),
        (
            [CustomTestListItem(3, "a"), CustomTestListItem(1, "c"), CustomTestListItem(2, "b")],
            [CustomTestListItem(1, "c"), CustomTestListItem(2, "b"), CustomTestListItem(3, "a")]
        ),
        (
            (CustomTestListItem(i, string.ascii_uppercase[-((i % 3) + 1)] * 3) for i in range(5)),
            [CustomTestListItem(0, "ZZZ"), CustomTestListItem(1, "YYY"), CustomTestListItem(2, "XXX"), CustomTestListItem(3, "ZZZ"), CustomTestListItem(4, "YYY")]
        ),
        (theoretical_testutils.EmptyObject(), InputDataNotConvertibleExc),
        ([theoretical_testutils.EmptyObject()], SortingFailedInFilterExc),
        ([theoretical_testutils.EmptyObject(), theoretical_testutils.EmptyObject(), theoretical_testutils.EmptyObject()], SortingFailedInFilterExc),
    )),
    (ListBlueprint(item_blueprint=GenericBlueprint(), filters=(ListSortFilter(lambda item: item.get_id(), reverse_order=True),)), (
        ([], []),
        (
            [CustomTestListItem(3, "a"), CustomTestListItem(1, "c"), CustomTestListItem(2, "b")],
            [CustomTestListItem(3, "a"), CustomTestListItem(2, "b"), CustomTestListItem(1, "c")]
        ),
        (
            (CustomTestListItem(i, string.ascii_uppercase[-((i % 3) + 1)] * 3) for i in range(5)),
            [CustomTestListItem(4, "YYY"), CustomTestListItem(3, "ZZZ"), CustomTestListItem(2, "XXX"), CustomTestListItem(1, "YYY"), CustomTestListItem(0, "ZZZ")]
        ),
        ([theoretical_testutils.EmptyObject()], SortingFailedInFilterExc),  # sorted()'s implementation detail - this raises exception there, but it does not below!
        ([theoretical_testutils.EmptyObject(), theoretical_testutils.EmptyObject(), theoretical_testutils.EmptyObject()], SortingFailedInFilterExc),
        (theoretical_testutils.EmptyObject(), InputDataNotConvertibleExc),
    )),
    (ListBlueprint(item_blueprint=GenericBlueprint(), filters=(ListSortFilter(),)), (
        ([], []),
        ([789], [789]),
        ([3, 1, 2], [1, 2, 3]),
        ([1, 3, 2.5, 2, 1.5, 3.5], [1, 1.5, 2, 2.5, 3, 3.5]),
        ([theoretical_testutils.EmptyObject()], [theoretical_testutils.EmptyObject()]),  # sorted()'s implementation detail - this doesn't raise exception there, but it does above!
        ([theoretical_testutils.EmptyObject(), theoretical_testutils.EmptyObject(), theoretical_testutils.EmptyObject()], SortingFailedInFilterExc),
        (theoretical_testutils.EmptyObject(), InputDataNotConvertibleExc),
    )),
    (ListBlueprint(item_blueprint=GenericBlueprint(), filters=(ListSortFilter(lambda item: theoretical_testutils.EmptyObject()),)), (
        ([], []),
        ([789], [789]),  # sorted()'s implementation detail - this doesn't raise exception there, but it does above!
        ([3, 1, 2], SortingFailedInFilterExc),
        ([1, 3, 2.5, 2, 1.5, 3.5], SortingFailedInFilterExc),
        ([theoretical_testutils.EmptyObject()], [theoretical_testutils.EmptyObject()]),  # sorted()'s implementation detail - this doesn't raise exception there, but it does above!
        ([theoretical_testutils.EmptyObject(), theoretical_testutils.EmptyObject(), theoretical_testutils.EmptyObject()], SortingFailedInFilterExc),
        (theoretical_testutils.EmptyObject(), InputDataNotConvertibleExc),
    )),
    (ListBlueprint(item_blueprint=GenericBlueprint(), filters=(ListSortFilter(lambda: 1),)), (  
        ([], []),
        ([789], SortingFailedInFilterExc),  # sorted()'s implementation detail - this raises exception there, but it doesn't above!
        ([3, 1, 2], SortingFailedInFilterExc),
        ([1, 3, 2.5, 2, 1.5, 3.5], SortingFailedInFilterExc),
        ([theoretical_testutils.EmptyObject()], SortingFailedInFilterExc),  # sorted()'s implementation detail - this raises exception there, but it doesn't above!
        ([theoretical_testutils.EmptyObject(), theoretical_testutils.EmptyObject(), theoretical_testutils.EmptyObject()], SortingFailedInFilterExc),
        (theoretical_testutils.EmptyObject(), InputDataNotConvertibleExc),
    )),
    (ListBlueprint(item_blueprint=GenericBlueprint(), filters=(ListSortFilter(exception_raising_comparison_key_extraction_function),)), (  
        ([], []),
        ([789], SortingFailedInFilterExc),  # sorted()'s implementation detail - this raises exception there, but it doesn't above!
        ([3, 1, 2], SortingFailedInFilterExc),
        ([1, 3, 2.5, 2, 1.5, 3.5], SortingFailedInFilterExc),
        ([theoretical_testutils.EmptyObject()], SortingFailedInFilterExc),  # sorted()'s implementation detail - this raises exception there, but it doesn't above!
        ([theoretical_testutils.EmptyObject(), theoretical_testutils.EmptyObject(), theoretical_testutils.EmptyObject()], SortingFailedInFilterExc),
        (theoretical_testutils.EmptyObject(), InputDataNotConvertibleExc),
    )),
    (ListBlueprint(item_blueprint=IntegerBlueprint(), validators=(SequenceContainsItemValidator(5, negate=False),)), (  
        ([True, "\r\n2   ", 3.9, 4, "\t     5\v \f  "], [1, 2, 3, 4, 5]),
        (range(10), [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
        ([False, False, 4, 5.5, "\r  5\v", 5, 777], [0, 0, 4, 5, 5, 5, 777]),
        ([True, 2, 3.8, "\n 4\t", "6", 789], DataValidationFailedExc),
        (filter(lambda x: (x % 5) != 0, range(15)), DataValidationFailedExc),
        ([1, 1, 2, 3, 4, 4, 4, 6, 6, 6, 777], DataValidationFailedExc),
        (theoretical_testutils.EmptyObject(), InputDataNotConvertibleExc),
        ([theoretical_testutils.EmptyObject()], InputDataTypeNotInAllowlistExc),
    )),
    (ListBlueprint(item_blueprint=IntegerBlueprint(), validators=(SequenceContainsItemValidator(5, negate=True),)), (
        ([True, "\r\n2   ", 3.9, 4, "\t     5\v \f  "], DataValidationFailedExc),
        (range(10), DataValidationFailedExc),
        ([False, False, 4, 5.5, "\r  5\v", 5, 777], DataValidationFailedExc),
        ([True, 2, 3.8, "\n 4\t", "6", 789], [1, 2, 3, 4, 6, 789]),
        (filter(lambda x: (x % 5) != 0, range(15)), [1, 2, 3, 4, 6, 7, 8, 9, 11, 12, 13, 14]),
        ([1, 1, 2, 3, 4, 4, 4, 6, 6, 6, 777], [1, 1, 2, 3, 4, 4, 4, 6, 6, 6, 777]),
        (theoretical_testutils.EmptyObject(), InputDataNotConvertibleExc),
        ([theoretical_testutils.EmptyObject()], InputDataTypeNotInAllowlistExc),
    )),
    (ListBlueprint(item_blueprint=IntegerBlueprint(), validators=(SequenceHasAllItemsUniqueValidator(),)), (  
        (["1", 2, 3.1], [1, 2, 3]),
        (range(10), [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
        (["1", True, 2.9, "\r\n2\t", "\v\f   3   ", 3], DataValidationFailedExc),
        ((float(i % 2) for i in range(20)), DataValidationFailedExc),
        ([1, 2, 2, 2, 3, 3, 4], DataValidationFailedExc),
        (theoretical_testutils.EmptyObject(), InputDataNotConvertibleExc),
        ([theoretical_testutils.EmptyObject()], InputDataTypeNotInAllowlistExc),
    )),
    (ListBlueprint(item_blueprint=IntegerBlueprint(), validators=(SequenceIsNotEmptyValidator(negate=False),)), (  
        ([True], [1]),
        ([True, 2.9, "3", 4, "\n\r 5\t   \v"], [1, 2, 3, 4, 5]),
        (range(1), [0]),
        (range(10), [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
        ([1, 2, 3], [1, 2, 3]),
        ([], DataValidationFailedExc),
        (range(0), DataValidationFailedExc),
        (filter(lambda x: x > 100, range(20)), DataValidationFailedExc),
        (theoretical_testutils.EmptyObject(), InputDataNotConvertibleExc),
        ([theoretical_testutils.EmptyObject()], InputDataTypeNotInAllowlistExc),
    )),
    (ListBlueprint(item_blueprint=IntegerBlueprint(), validators=(SequenceIsNotEmptyValidator(negate=True),)), (  
        ([True], DataValidationFailedExc),
        ([True, 2.9, "3", 4, "\n\r 5\t   \v"], DataValidationFailedExc),
        (range(1), DataValidationFailedExc),
        (range(10), DataValidationFailedExc),
        ([1, 2, 3], DataValidationFailedExc),
        ([], []),
        (range(0), []),
        (filter(lambda x: x > 100, range(20)), []),
        (theoretical_testutils.EmptyObject(), InputDataNotConvertibleExc),
        ([theoretical_testutils.EmptyObject()], InputDataTypeNotInAllowlistExc),
    )),
    (ListBlueprint(item_blueprint=IntegerBlueprint(), validators=(SequenceMaximumLengthValidator(3),)), (
        ([], []),
        (range(0), []),
        ([True], [1]),
        (range(1), [0]),
        ([True, 2.9], [1, 2]),
        (range(2), [0, 1]),
        ([True, 2.9, "\r\n003   \t"], [1, 2, 3]),
        (map(lambda x: float(x ** 2), range(3)), [0, 1, 4]),
        ([True, 2.9, "\r\n003   \t", 4], DataValidationFailedExc),
        (map(lambda x: float(x ** 2), range(4)), DataValidationFailedExc),
        ([True, 2.9, "\r\n003   \t", 4, "\v  000_005   "], DataValidationFailedExc),
        (map(lambda x: float(x ** 2), range(5)), DataValidationFailedExc),
        (range(10), DataValidationFailedExc),
        (map(lambda x: "\n\r000_000_000_" + str(x) + "    \f\f\v", range(10)), DataValidationFailedExc),
        (theoretical_testutils.EmptyObject(), InputDataNotConvertibleExc),
        ([theoretical_testutils.EmptyObject()], InputDataTypeNotInAllowlistExc),
    )),
    (ListBlueprint(item_blueprint=IntegerBlueprint(), validators=(SequenceMinimumLengthValidator(3),)), (
        ([], DataValidationFailedExc),
        (range(0), DataValidationFailedExc),
        ([True], DataValidationFailedExc),
        (range(1), DataValidationFailedExc),
        ([True, 2.9], DataValidationFailedExc),
        (range(2), DataValidationFailedExc),
        ([True, 2.9, "\r\n003   \t"], [1, 2, 3]),
        (map(lambda x: float(x ** 2), range(3)), [0, 1, 4]),
        ([True, 2.9, "\r\n003   \t", 4], [1, 2, 3, 4]),
        (map(lambda x: float(x ** 2), range(4)), [0, 1, 4, 9]),
        ([True, 2.9, "\r\n003   \t", 4, "\v  000_005   "], [1, 2, 3, 4, 5]),
        (map(lambda x: float(x ** 2), range(5)), [0, 1, 4, 9, 16]),
        (range(10), [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
        (map(lambda x: "\n\r000_000_000_" + str(x) + "    \f\f\v", range(10)), [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
        (theoretical_testutils.EmptyObject(), InputDataNotConvertibleExc),
        ([theoretical_testutils.EmptyObject()], InputDataTypeNotInAllowlistExc),
    )),
    (ListBlueprint(
        item_blueprint=ListBlueprint(item_blueprint=IntegerBlueprint())
    ), (
        (1, InputDataNotConvertibleExc),
        ([1, 2, 3], InputDataNotConvertibleExc),
        ([[1, 2, 3], [1, 2], 1], InputDataNotConvertibleExc),
        ([[1, 2, 3], [1, 2], [1]], [[1, 2, 3], [1, 2], [1]]),
        ([(1, 2, 3), (1, 2), (1,)], [[1, 2, 3], [1, 2], [1]]),
        (((1, 2, 3), (1, 2), (1,)), [[1, 2, 3], [1, 2], [1]]),
        ([], []),
        ((), []),
        ([[]], [[]]),
        ([()], [[]]),
        (([],), [[]]),
        (((),), [[]]),
        (theoretical_testutils.EmptyObject(), InputDataNotConvertibleExc),
        ([theoretical_testutils.EmptyObject()], InputDataNotConvertibleExc),
        ([[theoretical_testutils.EmptyObject()]], InputDataTypeNotInAllowlistExc),
    )),
    (ListBlueprint(
        # "Real use case" simulation - a list of IDs received from a client.
        item_blueprint=IntegerBlueprint(
            parsing_mode=ParsingMode.MODE_STRICT,
            validators=(IntegerIsPositiveValidator(), NumberMaximumValueValidator(2**31 - 1))
        ),
        filters=(ListDeduplicateItemsFilter(), ListSortFilter()),
        validators=(SequenceIsNotEmptyValidator(), SequenceMaximumLengthValidator(5)),  
        parsing_mode=ParsingMode.MODE_STRICT
    ), (
        (range(3), InputDataTypeNotInAllowlistExc),
        ((i ** 2 for i in range(4)), InputDataTypeNotInAllowlistExc),
        (map(lambda x: x ** 2, range(4)), InputDataTypeNotInAllowlistExc),
        ("123", InputDataTypeNotInAllowlistExc),
        (b'abcd', InputDataTypeNotInAllowlistExc),
        (bytearray(b'xyz'), InputDataTypeNotInAllowlistExc),
        (dict(), InputDataTypeNotInAllowlistExc),
        ({1: 2, 3: 4}, InputDataTypeNotInAllowlistExc),
        (123, InputDataTypeNotInAllowlistExc),
        (123.456, InputDataTypeNotInAllowlistExc),
        (True, InputDataTypeNotInAllowlistExc),
        (float("inf"), InputDataTypeNotInAllowlistExc),
        (float("nan"), InputDataTypeNotInAllowlistExc),
        (None, InputDataTypeNotInAllowlistExc),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc),
        (object(), InputDataTypeNotInAllowlistExc),
        ([1, 2.0, 3], InputDataTypeNotInAllowlistExc),
        ([1, "2", 3], InputDataTypeNotInAllowlistExc),
        ([1, None, 3], InputDataTypeNotInAllowlistExc),
        ([1, theoretical_testutils.EmptyObject(), 3], InputDataTypeNotInAllowlistExc),
        (["123"], InputDataTypeNotInAllowlistExc),
        ([None], InputDataTypeNotInAllowlistExc),
        ([[], []], InputDataTypeNotInAllowlistExc),
        ([{}, {}], InputDataTypeNotInAllowlistExc),
        ([theoretical_testutils.EmptyObject(), theoretical_testutils.EmptyObject()], InputDataTypeNotInAllowlistExc),
        ([1, 0, 2], DataValidationFailedExc),
        ([-100], DataValidationFailedExc),
        ([1, 2**31, 2], DataValidationFailedExc),
        ([2**64], DataValidationFailedExc),
        ([], DataValidationFailedExc),
        ([1, 2, 3, 4, 5, 6], DataValidationFailedExc),
        (list(range(10, 100)), DataValidationFailedExc),
        ([1, 2, 2, 3], [1, 2, 3]),
        ([1] * 50, [1]),
        ([1, 2, 3, 4, 5] * 20, [1, 2, 3, 4, 5]),
        ([3], [3]),
        ([5, 1, 2, 4, 3], [1, 2, 3, 4, 5]),
        ([3, 3, 1, 2, 1, 3, 2, 1, 1, 1, 2, 3, 2, 1, 1, 2, 3, 2], [1, 2, 3]),
        ((1, 2.0, 3), InputDataTypeNotInAllowlistExc),
        ((1, "2", 3), InputDataTypeNotInAllowlistExc),
        ((1, None, 3), InputDataTypeNotInAllowlistExc),
        ((1, theoretical_testutils.EmptyObject(), 3), InputDataTypeNotInAllowlistExc),
        (("123",), InputDataTypeNotInAllowlistExc),
        ((None,), InputDataTypeNotInAllowlistExc),
        (([], []), InputDataTypeNotInAllowlistExc),
        (({}, {}), InputDataTypeNotInAllowlistExc),
        ((theoretical_testutils.EmptyObject(), theoretical_testutils.EmptyObject()), InputDataTypeNotInAllowlistExc),
        ((1, 0, 2), DataValidationFailedExc),
        ((-100,), DataValidationFailedExc),
        ((1, 2**31, 2), DataValidationFailedExc),
        ((2**64,), DataValidationFailedExc),
        ((), DataValidationFailedExc),
        ((1, 2, 3, 4, 5, 6), DataValidationFailedExc),
        (tuple(range(10, 100)), DataValidationFailedExc),
        ((1, 2, 2, 3), [1, 2, 3]),
        ((1,) * 50, [1]),
        ((1, 2, 3, 4, 5) * 20, [1, 2, 3, 4, 5]),
        ((3,), [3]),
        ((5, 1, 2, 4, 3), [1, 2, 3, 4, 5]),
        ((3, 3, 1, 2, 1, 3, 2, 1, 1, 1, 2, 3, 2, 1, 1, 2, 3, 2), [1, 2, 3]),
        ({1, 2.0, 3}, InputDataTypeNotInAllowlistExc),
        ({1, "2", 3}, InputDataTypeNotInAllowlistExc),
        ({1, None, 3}, InputDataTypeNotInAllowlistExc),
        ({1, object(), 3}, InputDataTypeNotInAllowlistExc),
        ({"123"}, InputDataTypeNotInAllowlistExc),
        ({None}, InputDataTypeNotInAllowlistExc),
        ({tuple(), tuple()}, InputDataTypeNotInAllowlistExc),
        ({frozenset(), frozenset()}, InputDataTypeNotInAllowlistExc),
        ({object(), object()}, InputDataTypeNotInAllowlistExc),
        ({1, 0, 2}, DataValidationFailedExc),
        ({-100}, DataValidationFailedExc),
        ({1, 2**31, 2}, DataValidationFailedExc),
        ({2**64}, DataValidationFailedExc),
        (set(), DataValidationFailedExc),
        ({1, 2, 3, 4, 5, 6}, DataValidationFailedExc),
        (set(range(10, 100)), DataValidationFailedExc),
        ({1, 2, 2, 3}, [1, 2, 3]),
        ({3}, [3]),
        ({5, 1, 2, 4, 3}, [1, 2, 3, 4, 5]),
        ({3, 3, 1, 2, 1, 3, 2, 1, 1, 1, 2, 3, 2, 1, 1, 2, 3, 2}, [1, 2, 3]),
        (frozenset([1, 2.0, 3]), InputDataTypeNotInAllowlistExc),
        (frozenset([1, "2", 3]), InputDataTypeNotInAllowlistExc),
        (frozenset([1, None, 3]), InputDataTypeNotInAllowlistExc),
        (frozenset([1, object(), 3]), InputDataTypeNotInAllowlistExc),
        (frozenset(["123"]), InputDataTypeNotInAllowlistExc),
        (frozenset([None]), InputDataTypeNotInAllowlistExc),
        (frozenset([tuple(), tuple()]), InputDataTypeNotInAllowlistExc),
        (frozenset([frozenset(), frozenset()]), InputDataTypeNotInAllowlistExc),
        (frozenset([object(), object()]), InputDataTypeNotInAllowlistExc),
        (frozenset([1, 0, 2]), DataValidationFailedExc),
        (frozenset([-100]), DataValidationFailedExc),
        (frozenset([1, 2**31, 2]), DataValidationFailedExc),
        (frozenset([2**64]), DataValidationFailedExc),
        (frozenset(), DataValidationFailedExc),
        (frozenset([1, 2, 3, 4, 5, 6]), DataValidationFailedExc),
        (frozenset(range(10, 100)), DataValidationFailedExc),
        (frozenset([1, 2, 2, 3]), [1, 2, 3]),
        (frozenset([3]), [3]),
        (frozenset([5, 1, 2, 4, 3]), [1, 2, 3, 4, 5]),
        (frozenset([3, 3, 1, 2, 1, 3, 2, 1, 1, 1, 2, 3, 2, 1, 1, 2, 3, 2]), [1, 2, 3]),
    )),
)


@pytest.mark.parametrize(("blueprint", "input_", "output"), theoretical_testutils.test_function_parameter_generator(__LIST_BLUEPRINT_TEST_SUITE))
def test_list_blueprint(blueprint, input_, output):
    theoretical_testutils.perform_test(blueprint, input_, output)


def test_list_blueprint_default_parsing_mode():
    assert ListBlueprint(item_blueprint=IntegerBlueprint()).get_parsing_mode() == ParsingMode.MODE_RATIONAL


def test_list_blueprint_item_blueprint():
    item_bp = IntegerBlueprint()
    assert ListBlueprint(item_blueprint=item_bp).get_item_blueprint() is item_bp


def test_list_blueprint_filter_and_validator_sequences():
    filter_seq = (
        ListDeduplicateItemsFilter(),
        ListSortFilter()
    )
    validator_seq = (
        SequenceContainsItemValidator("???"),
        SequenceHasAllItemsUniqueValidator(),
        SequenceIsNotEmptyValidator(),
        SequenceMaximumLengthValidator(100),
        SequenceMinimumLengthValidator(50)
    )
    list_bp = ListBlueprint(GenericBlueprint(), filters=filter_seq, validators=validator_seq)

    assert (list_bp.get_filters() == filter_seq) and (list_bp.get_validators() == validator_seq)


def test_list_sort_filter_default_instance_attributes():
    instance = ListSortFilter()
    assert (instance.get_comparison_key_extraction_function() is None) and (instance.is_order_reversed() is False)


def test_list_sort_filter_instance_attributes():
    def __extraction_func(item):
        return item

    instance = ListSortFilter(comparison_key_extraction_function=__extraction_func, reverse_order=True)

    assert (instance.get_comparison_key_extraction_function() is __extraction_func) and (instance.is_order_reversed() is True)


def test_sequence_contains_item_validator_default_negation():
    assert SequenceContainsItemValidator("!!!").is_negated() is False


def test_sequence_contains_item_validator_checked_item():
    item = theoretical_testutils.EmptyObject()
    assert SequenceContainsItemValidator(item).get_checked_item() is item


def test_sequence_is_not_empty_validator_default_negation():
    assert SequenceIsNotEmptyValidator().is_negated() is False


@pytest.mark.parametrize("length", (0, 1, 100, 1000, 1_000_000, 1_000_000_000_000_000))
def test_sequence_maximum_length_validator_maximum_acceptable_length(length):
    assert SequenceMaximumLengthValidator(length).get_maximum_acceptable_length() == length


@pytest.mark.parametrize("length", (-1, -100, -100_000_000_000_000))
def test_sequence_maximum_length_validator_invalid_maximum_acceptable_length(length):
    with pytest.raises(InvalidValidatorConfigError):
        SequenceMaximumLengthValidator(length)


@pytest.mark.parametrize("length", (0, 1, 100, 1000, 1_000_000, 1_000_000_000_000_000))
def test_sequence_minimum_length_validator_minimum_acceptable_length(length):
    assert SequenceMinimumLengthValidator(length).get_minimum_acceptable_length() == length


@pytest.mark.parametrize("length", (-1, -100, -100_000_000_000_000))
def test_sequence_minimum_length_validator_invalid_minimum_acceptable_length(length):
    with pytest.raises(InvalidValidatorConfigError):
        SequenceMinimumLengthValidator(length)
