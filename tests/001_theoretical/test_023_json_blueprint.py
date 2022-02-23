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

from typing import Any, List
import theoretical_testutils
import pytest
from datalidator.blueprints.ParsingMode import ParsingMode
from datalidator.blueprints.specialimpl.JSONBlueprint import JSONBlueprint
from datalidator.blueprints.impl.StringBlueprint import StringBlueprint
from datalidator.blueprints.impl.IntegerBlueprint import IntegerBlueprint
from datalidator.blueprints.impl.BooleanBlueprint import BooleanBlueprint
from datalidator.blueprints.impl.GenericBlueprint import GenericBlueprint
from datalidator.blueprints.impl.ListBlueprint import ListBlueprint
from datalidator.blueprints.impl.ObjectBlueprint import ObjectBlueprint
from datalidator.blueprints.extras.ObjectModel import ObjectModel
from datalidator.blueprints.exc.InvalidInputDataExc import InvalidInputDataExc
from datalidator.blueprints.exc.InputDataTypeNotInAllowlistExc import InputDataTypeNotInAllowlistExc
from datalidator.blueprints.exc.InputDataNotConvertibleExc import InputDataNotConvertibleExc
from datalidator.blueprints.exc.InputDataValueNotAllowedForDataTypeExc import InputDataValueNotAllowedForDataTypeExc
from datalidator.filters.impl.StringStripFilter import StringStripFilter
from datalidator.filters.impl.StringUnicodeNormalizeFilter import StringUnicodeNormalizeFilter
from datalidator.validators.impl.StringMatchesRegexValidator import StringMatchesRegexValidator
from datalidator.validators.impl.NumberMinimumValueValidator import NumberMinimumValueValidator
from datalidator.validators.impl.NumberMaximumValueValidator import NumberMaximumValueValidator
from datalidator.validators.exc.DataValidationFailedExc import DataValidationFailedExc


class JSONTestObjectModel(ObjectModel):
    username = StringBlueprint(
        filters=(StringStripFilter(), StringUnicodeNormalizeFilter(normal_form="NFKC")),
        validators=(StringMatchesRegexValidator(r'^[a-z0-9]{3,15}\Z'),),
        parsing_mode=ParsingMode.MODE_STRICT
    )
    age = IntegerBlueprint(
        validators=(NumberMinimumValueValidator(13), NumberMaximumValueValidator(100)),
        parsing_mode=ParsingMode.MODE_STRICT
    )


__JSON_BLUEPRINT_TEST_SUITE = (
    (JSONBlueprint[Any](
        wrapped_blueprint=GenericBlueprint()
    ), (
        ("", InvalidInputDataExc),
        ("hello", InvalidInputDataExc),
        ("hello\x00", InvalidInputDataExc),
        ("hello world", InvalidInputDataExc),
        ("hello world\r\n", InvalidInputDataExc),
        ("hello\r\nworld", InvalidInputDataExc),
        ("hello\x00world\r\n", InvalidInputDataExc),
        ("řeřicha", InvalidInputDataExc),
        ("řeřicha\r\n", InvalidInputDataExc),
        ("řeř\r\nicha", InvalidInputDataExc),
        ("řeř\x00icha", InvalidInputDataExc),
        ("🤍", InvalidInputDataExc),
        ("🤍\r\n", InvalidInputDataExc),
        ("🤍\x00", InvalidInputDataExc),
        ("\x00🤍", InvalidInputDataExc),
        ("null", None),
        ("Null", InvalidInputDataExc),
        ("NULL", InvalidInputDataExc),
        ("true", True),
        ("True", InvalidInputDataExc),
        ("TRUE", InvalidInputDataExc),
        ("false", False),
        ("False", InvalidInputDataExc),
        ("FALSE", InvalidInputDataExc),
        ("123", 123),
        ("-123", -123),
        ("123.0", 123.0),
        ("-123.0", -123.0),
        ("Infinity", float("inf")),  # This is not portable!
        ("infinity", InvalidInputDataExc),
        ("-Infinity", float("-inf")),  # This is not portable!
        ("-infinity", InvalidInputDataExc),
        ("NaN", lambda output: str(output) == "nan"),  # This is not portable!
        ("nan", InvalidInputDataExc),
        ('""', ""),
        ('"abc"', "abc"),
        ('"hello\\tworld\\r\\n"', "hello\tworld\r\n"),
        ('"hello\\t\\u0000world\\r\\n"', "hello\t\x00world\r\n"),
        ('"\\f\\u000b   hello\\t\\u0000world\\r\\n"', "\f\v   hello\t\x00world\r\n"),
        ('"\\"\\"\\"\'\'\\"\\"\'\\"\\"\'\\""', '"""\'\'""\'""\'"'),
        (
            '[1, 2.5, true, "abc", null, "hello\\tworld\\r\\n"]',
            [1, 2.5, True, "abc", None, "hello\tworld\r\n"]
        ),
        (
            '{"true": false, "some_value": null, "1.5": -123, "float": 123.5, "hello world": "\\u0159e\\u0159icha", "test\\u0000\\t key": "hello \\ud83e\\udd0d!", "   ascii\\uffffstring \\t\\n": "value", "": ""}',
            {"true": False, "some_value": None, "1.5": -123, "float": 123.5, "hello world": "řeřicha", "test\x00\t key": "hello 🤍!", "   ascii\uffffstring \t\n": "value", "": ""}
        ),
        (
            '[{}, {"a": 123, "b": true}, null, [1, 2.5], "test"]',
            [{}, {"a": 123, "b": True}, None, [1, 2.5], "test"]
        ),
        (
            '{"hello": [true, false, "123   "], "value": null, "test\\r\\n": 132.5, "object": {"a": null, "b": "c"}}',
            {"hello": [True, False, "123   "], "value": None, "test\r\n": 132.5, "object": {"a": None, "b": "c"}}
        ),
        ("\t\r\u2029\x85   \t   \x1c   ", InvalidInputDataExc),
        ("\t\r\u2029\x85   \t   \x1c   hello", InvalidInputDataExc),
        ("\t\r\u2029\x85   \t   \x1c   hello\x00", InvalidInputDataExc),
        ("\t\r\u2029\x85   \t   \x1c   hello world", InvalidInputDataExc),
        ("\t\r\u2029\x85   \t   \x1c   hello world\r\n", InvalidInputDataExc),
        ("\t\r\u2029\x85   \t   \x1c   hello\r\nworld", InvalidInputDataExc),
        ("\t\r\u2029\x85   \t   \x1c   hello\x00world\r\n", InvalidInputDataExc),
        ("\t\r\u2029\x85   \t   \x1c   řeřicha", InvalidInputDataExc),
        ("\t\r\u2029\x85   \t   \x1c   řeřicha\r\n", InvalidInputDataExc),
        ("\t\r\u2029\x85   \t   \x1c   řeř\r\nicha", InvalidInputDataExc),
        ("\t\r\u2029\x85   \t   \x1c   řeř\x00icha", InvalidInputDataExc),
        ("\t\r\u2029\x85   \t   \x1c   🤍", InvalidInputDataExc),
        ("\t\r\u2029\x85   \t   \x1c   🤍\r\n", InvalidInputDataExc),
        ("\t\r\u2029\x85   \t   \x1c   🤍\x00", InvalidInputDataExc),
        ("\t\r\u2029\x85   \t   \x1c   \x00🤍", InvalidInputDataExc),
        ("\t\r\u2029\x85   \t   \x1c   null", None),
        ("\t\r\u2029\x85   \t   \x1c   Null", InvalidInputDataExc),
        ("\t\r\u2029\x85   \t   \x1c   NULL", InvalidInputDataExc),
        ("\t\r\u2029\x85   \t   \x1c   true", True),
        ("\t\r\u2029\x85   \t   \x1c   True", InvalidInputDataExc),
        ("\t\r\u2029\x85   \t   \x1c   TRUE", InvalidInputDataExc),
        ("\t\r\u2029\x85   \t   \x1c   false", False),
        ("\t\r\u2029\x85   \t   \x1c   False", InvalidInputDataExc),
        ("\t\r\u2029\x85   \t   \x1c   FALSE", InvalidInputDataExc),
        ("\t\r\u2029\x85   \t   \x1c   123", 123),
        ("\t\r\u2029\x85   \t   \x1c   -123", -123),
        ("\t\r\u2029\x85   \t   \x1c   123.0", 123.0),
        ("\t\r\u2029\x85   \t   \x1c   -123.0", -123.0),
        ("\t\r\u2029\x85   \t   \x1c   Infinity", float("inf")),  # This is not portable!
        ("\t\r\u2029\x85   \t   \x1c   infinity", InvalidInputDataExc),
        ("\t\r\u2029\x85   \t   \x1c   -Infinity", float("-inf")),  # This is not portable!
        ("\t\r\u2029\x85   \t   \x1c   -infinity", InvalidInputDataExc),
        ("\t\r\u2029\x85   \t   \x1c   NaN", lambda output: str(output) == "nan"),  # This is not portable!
        ("\t\r\u2029\x85   \t   \x1c   nan", InvalidInputDataExc),
        ('\t\r\u2029\x85   \t   \x1c   ""', ""),
        ('\t\r\u2029\x85   \t   \x1c   "abc"', "abc"),
        ('\t\r\u2029\x85   \t   \x1c   "hello\\tworld\\r\\n"', "hello\tworld\r\n"),
        ('\t\r\u2029\x85   \t   \x1c   "hello\\t\\u0000world\\r\\n"', "hello\t\x00world\r\n"),
        ('\t\r\u2029\x85   \t   \x1c   "\\f\\u000b   hello\\t\\u0000world\\r\\n"', "\f\v   hello\t\x00world\r\n"),
        ('\t\r\u2029\x85   \t   \x1c   "\\"\\"\\"\'\'\\"\\"\'\\"\\"\'\\""', '"""\'\'""\'""\'"'),
        (
            '\x1c\x1e    \t\x85 \u2029\u2028   [1, 2.5, true, "abc", null, "hello\\tworld\\r\\n"]\v\f\f\r\n\r\r\n\n\n   ',
            [1, 2.5, True, "abc", None, "hello\tworld\r\n"]
        ),
        (
            '\x1c\x1e    \t\x85 \u2029\u2028   {"true": false, "some_value": null, "1.5": -123, "float": 123.5, "hello world": "\\u0159e\\u0159icha", "test\\u0000\\t key": "hello \\ud83e\\udd0d!", "   ascii\\uffffstring \\t\\n": "value", "": ""}\v\f\f\r\n\r\r\n\n\n   ',
            {"true": False, "some_value": None, "1.5": -123, "float": 123.5, "hello world": "řeřicha", "test\x00\t key": "hello 🤍!", "   ascii\uffffstring \t\n": "value", "": ""}
        ),
        (
            '\x1c\x1e    \t\x85 \u2029\u2028   [{}, {"a": 123, "b": true}, null, [1, 2.5], "test"]\v\f\f\r\n\r\r\n\n\n   ',
            [{}, {"a": 123, "b": True}, None, [1, 2.5], "test"]
        ),
        (
            '\x1c\x1e    \t\x85 \u2029\u2028   {"hello": [true, false, "123   "], "value": null, "test\\r\\n": 132.5, "object": {"a": null, "b": "c"}}\v\f\f\r\n\r\r\n\n\n   ',
            {"hello": [True, False, "123   "], "value": None, "test\r\n": 132.5, "object": {"a": None, "b": "c"}}
        ),
        (None, InputDataTypeNotInAllowlistExc),
        (False, InputDataTypeNotInAllowlistExc),
        (True, InputDataTypeNotInAllowlistExc),
        (1, InputDataTypeNotInAllowlistExc),
        (0, InputDataTypeNotInAllowlistExc),
        (1.5, InputDataTypeNotInAllowlistExc),
        (0.5, InputDataTypeNotInAllowlistExc),
        (1+2j, InputDataTypeNotInAllowlistExc),
        ([], InputDataTypeNotInAllowlistExc),
        (["abc"], InputDataTypeNotInAllowlistExc),
        ({}, InputDataTypeNotInAllowlistExc),
        ({"abc": "def"}, InputDataTypeNotInAllowlistExc),
        (b'', InputDataTypeNotInAllowlistExc),
        (b'hello', InputDataTypeNotInAllowlistExc),
        (bytearray(b''), InputDataTypeNotInAllowlistExc),
        (bytearray(b'hello'), InputDataTypeNotInAllowlistExc),
        (str, InputDataTypeNotInAllowlistExc),
        (object(), InputDataTypeNotInAllowlistExc),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc),
    )),
    (JSONBlueprint[bool](
        wrapped_blueprint=BooleanBlueprint(parsing_mode=ParsingMode.MODE_RATIONAL)
    ), (
        ("true", True),
        ("false", False),
        ("null", InputDataTypeNotInAllowlistExc),
        ("[]", InputDataTypeNotInAllowlistExc),
        ("{}", InputDataTypeNotInAllowlistExc),
        ("1.0", True),
        ("0.0", False),
        ("1.5", InputDataValueNotAllowedForDataTypeExc),
        ("0.5", InputDataValueNotAllowedForDataTypeExc),
        ("1", True),
        ("0", False),
        ("2", InputDataValueNotAllowedForDataTypeExc),
        ('""', InputDataValueNotAllowedForDataTypeExc),
        ('"hello"', InputDataValueNotAllowedForDataTypeExc),
        ('"TRUE"', True),
        ('"Yes\\r"', True),
        ('"  \\n  TRUE \\t"', True),
        ('"  \\t  no\\r\\n"', False),
        ('"  \\t  oFF\\r\\n"', False),
        ('"  \\t  \\u0000oFF\\r\\n"', InputDataValueNotAllowedForDataTypeExc),
        ('\r\n   \t\u2029   "\\t  TRUE  \\n"  \x1d\x1c \x85', True),
        ("", InvalidInputDataExc),
        ("hello", InvalidInputDataExc),
        ("he\x00llo", InvalidInputDataExc),
        ('"', InvalidInputDataExc),
        ('"""', InvalidInputDataExc),
        (None, InputDataTypeNotInAllowlistExc),
        ([], InputDataTypeNotInAllowlistExc),
        (str, InputDataTypeNotInAllowlistExc),
        (object(), InputDataTypeNotInAllowlistExc),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc),
    )),
    (JSONBlueprint[List[int]](
        wrapped_blueprint=ListBlueprint(
            item_blueprint=IntegerBlueprint(parsing_mode=ParsingMode.MODE_RATIONAL),  
            parsing_mode=ParsingMode.MODE_STRICT
        ),
    ), (
        ("true", InputDataTypeNotInAllowlistExc),
        ("null", InputDataTypeNotInAllowlistExc),
        ("{}", InputDataTypeNotInAllowlistExc),
        ("5", InputDataTypeNotInAllowlistExc),
        ('""', InputDataTypeNotInAllowlistExc),
        ('"hello"', InputDataTypeNotInAllowlistExc),
        ('[true, "\\r   10_000  \\t\\n", "", 2.9, 8, "-789000"]', InputDataNotConvertibleExc),
        ('[true, "\\r   10_000  \\t\\n", "hello", 2.9, 8, "-789000"]', InputDataNotConvertibleExc),
        ('[true, "\\r   10_000  \\t\\n", [], 2.9, 8, "-789000"]', InputDataTypeNotInAllowlistExc),
        ('[true, "\\r   10_000  \\t\\n", {}, 2.9, 8, "-789000"]', InputDataTypeNotInAllowlistExc),
        ('[true, "\\r   10_000  \\t\\n", null, 2.9, 8, "-789000"]', InputDataTypeNotInAllowlistExc),
        ('[]', []),
        ('[1, 2, -3, 4]', [1, 2, -3, 4]),
        ('[true, "\\r   10_000  \\t\\n", 2.9, 8, "-789000"]', [1, 10000, 2, 8, -789000]),
        ('\t\f\v\u2028    [] \x1c\x1d   ', []),
        ('\t\f\v\u2028    [1, 2, -3, 4] \x1c\x1d   ', [1, 2, -3, 4]),
        ('\t\f\v\u2028    [true, "\\r   10_000  \\t\\n", 2.9, 8, "-789000"] \x1c\x1d   ', [1, 10000, 2, 8, -789000]),
        ("", InvalidInputDataExc),
        ("hello", InvalidInputDataExc),
        ("he\x00llo", InvalidInputDataExc),
        ('"', InvalidInputDataExc),
        ('"""', InvalidInputDataExc),
        (None, InputDataTypeNotInAllowlistExc),
        ([], InputDataTypeNotInAllowlistExc),
        (str, InputDataTypeNotInAllowlistExc),
        (object(), InputDataTypeNotInAllowlistExc),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc),
    )),
    (JSONBlueprint[ObjectModel](
        wrapped_blueprint=ObjectBlueprint(
            object_model=JSONTestObjectModel,
            ignore_input_keys_which_are_not_in_model=False
        ),
    ), (
        ("true", InputDataNotConvertibleExc),
        ("null", InputDataNotConvertibleExc),
        ("5", InputDataNotConvertibleExc),
        ("5.8", InputDataNotConvertibleExc),
        ('""', InvalidInputDataExc),
        ('"\\uffff"', InvalidInputDataExc),
        ('"hello"', InputDataNotConvertibleExc),
        ('[]', InvalidInputDataExc),
        ('[1]', InputDataNotConvertibleExc),
        ('[1, 2]', InputDataNotConvertibleExc),
        ('{"username": "john01", "age": 15}', JSONTestObjectModel(username="john01", age=15)),
        ('{"username": "\\r\\n\\u2028   john01 \\t   \\u2029\\t\\n\\r", "age": 15}', JSONTestObjectModel(username="john01", age=15)),
        ('{"username": "ｊｏｈｎ０１", "age": 15}', JSONTestObjectModel(username="john01", age=15)),
        ('{"username": "\\uff4a\\uff4f\\uff48\\uff4e\\uff10\\uff11", "age": 15}', JSONTestObjectModel(username="john01", age=15)),
        ('[["username", "john01"], ["age", 15]]', JSONTestObjectModel(username="john01", age=15)),
        ('[["username", "\\r\\n\\u2028   john01 \\t   \\u2029\\t\\n\\r"], ["age", 15]]', JSONTestObjectModel(username="john01", age=15)),
        ('[["username", "ｊｏｈｎ０１"], ["age", 15]]', JSONTestObjectModel(username="john01", age=15)),
        ('[["username", "\\uff4a\\uff4f\\uff48\\uff4e\\uff10\\uff11"], ["age", 15]]', JSONTestObjectModel(username="john01", age=15)),
        ('{"username": "", "age": 15}', DataValidationFailedExc),
        ('[["username", ""], ["age", 15]]', DataValidationFailedExc),
        ('{"username": "ab", "age": 15}', DataValidationFailedExc),
        ('[["username", "ab"], ["age", 15]]', DataValidationFailedExc),
        ('{"username": "abc", "age": 15}', JSONTestObjectModel(username="abc", age=15)),
        ('[["username", "abc"], ["age", 15]]', JSONTestObjectModel(username="abc", age=15)),
        ('{"username": "abcdefghij", "age": 15}', JSONTestObjectModel(username="abcdefghij", age=15)),
        ('[["username", "abcdefghij"], ["age", 15]]', JSONTestObjectModel(username="abcdefghij", age=15)),
        ('{"username": "abcdefghijklmno", "age": 15}', JSONTestObjectModel(username="abcdefghijklmno", age=15)),
        ('[["username", "abcdefghijklmno"], ["age", 15]]', JSONTestObjectModel(username="abcdefghijklmno", age=15)),
        ('{"username": "abcdefghijklmnop", "age": 15}', DataValidationFailedExc),
        ('[["username", "abcdefghijklmnop"], ["age", 15]]', DataValidationFailedExc),
        ('{"username": "abcdefghijklmnop1234567890", "age": 15}', DataValidationFailedExc),
        ('[["username", "abcdefghijklmnop1234567890"], ["age", 15]]', DataValidationFailedExc),
        ('{"username": "John01", "age": 15}', DataValidationFailedExc),
        ('[["username", "John01"], ["age", 15]]', DataValidationFailedExc),
        ('{"username": "JOHN01", "age": 15}', DataValidationFailedExc),
        ('[["username", "JOHN01"], ["age", 15]]', DataValidationFailedExc),
        ('{"username": "johnŠ01", "age": 15}', DataValidationFailedExc),
        ('[["username", "johnŠ01"], ["age", 15]]', DataValidationFailedExc),
        ('{"username": "john\\u015901", "age": 15}', DataValidationFailedExc),
        ('[["username", "john\\u015901"], ["age", 15]]', DataValidationFailedExc),
        ('{"username": "john🤍01", "age": 15}', DataValidationFailedExc),
        ('[["username", "john🤍01"], ["age", 15]]', DataValidationFailedExc),
        ('{"username": "john\\ud83e\\udd0d01", "age": 15}', DataValidationFailedExc),
        ('[["username", "john\\ud83e\\udd0d01"], ["age", 15]]', DataValidationFailedExc),
        ('{"username": "john\\n01", "age": 15}', DataValidationFailedExc),
        ('[["username", "john\\n01"], ["age", 15]]', DataValidationFailedExc),
        ('{"username": "john\\u000001", "age": 15}', DataValidationFailedExc),
        ('[["username", "john\\u000001"], ["age", 15]]', DataValidationFailedExc),
        ('{"username": "john!01", "age": 15}', DataValidationFailedExc),
        ('[["username", "john!01"], ["age", 15]]', DataValidationFailedExc),
        ('{"username": "john.01", "age": 15}', DataValidationFailedExc),
        ('[["username", "john.01"], ["age", 15]]', DataValidationFailedExc),
        ('{"username": "john 01", "age": 15}', DataValidationFailedExc),
        ('[["username", "john 01"], ["age", 15]]', DataValidationFailedExc),
        ('{"username": "john\\t01", "age": 15}', DataValidationFailedExc),
        ('[["username", "john\\t01"], ["age", 15]]', DataValidationFailedExc),
        ('{"username": null, "age": 15}', InputDataTypeNotInAllowlistExc),
        ('[["username", null], ["age", 15]]', InputDataTypeNotInAllowlistExc),
        ('{"username": true, "age": 15}', InputDataTypeNotInAllowlistExc),
        ('[["username", true], ["age", 15]]', InputDataTypeNotInAllowlistExc),
        ('{"username": 7, "age": 15}', InputDataTypeNotInAllowlistExc),
        ('[["username", 7], ["age", 15]]', InputDataTypeNotInAllowlistExc),
        ('{"username": 5.5, "age": 15}', InputDataTypeNotInAllowlistExc),
        ('[["username", 5.5], ["age", 15]]', InputDataTypeNotInAllowlistExc),
        ('{"username": [], "age": 15}', InputDataTypeNotInAllowlistExc),
        ('[["username", []], ["age", 15]]', InputDataTypeNotInAllowlistExc),
        ('{"username": ["test"], "age": 15}', InputDataTypeNotInAllowlistExc),
        ('[["username", ["test"]], ["age", 15]]', InputDataTypeNotInAllowlistExc),
        ('{"username": {}, "age": 15}', InputDataTypeNotInAllowlistExc),
        ('[["username", {}], ["age", 15]]', InputDataTypeNotInAllowlistExc),
        ('{"username": {"test": "test"}, "age": 15}', InputDataTypeNotInAllowlistExc),
        ('[["username", {"test": "test"}], ["age", 15]]', InputDataTypeNotInAllowlistExc),
        ('{"username": "john01", "age": 0}', DataValidationFailedExc),
        ('[["username", "john01"], ["age", 0]]', DataValidationFailedExc),
        ('{"username": "john01", "age": 12}', DataValidationFailedExc),
        ('[["username", "john01"], ["age", 12]]', DataValidationFailedExc),
        ('{"username": "john01", "age": 13}', JSONTestObjectModel(username="john01", age=13)),
        ('[["username", "john01"], ["age", 13]]', JSONTestObjectModel(username="john01", age=13)),
        ('{"username": "john01", "age": 50}', JSONTestObjectModel(username="john01", age=50)),
        ('[["username", "john01"], ["age", 50]]', JSONTestObjectModel(username="john01", age=50)),
        ('{"username": "john01", "age": 100}', JSONTestObjectModel(username="john01", age=100)),
        ('[["username", "john01"], ["age", 100]]', JSONTestObjectModel(username="john01", age=100)),
        ('{"username": "john01", "age": 101}', DataValidationFailedExc),
        ('[["username", "john01"], ["age", 101]]', DataValidationFailedExc),
        ('{"username": "john01", "age": 100000000}', DataValidationFailedExc),
        ('[["username", "john01"], ["age", 100000000]]', DataValidationFailedExc),
        ('{"username": "john01", "age": null}', InputDataTypeNotInAllowlistExc),
        ('[["username", "john01"], ["age", null]]', InputDataTypeNotInAllowlistExc),
        ('{"username": "john01", "age": true}', DataValidationFailedExc),  # For historic reasons, 'bool' is a subclass of 'int'.
        ('[["username", "john01"], ["age", true]]', DataValidationFailedExc),  # For historic reasons, 'bool' is a subclass of 'int'.
        ('{"username": "john01", "age": 20.0}', InputDataTypeNotInAllowlistExc),
        ('[["username", "john01"], ["age", 20.0]]', InputDataTypeNotInAllowlistExc),
        ('{"username": "john01", "age": 20.9}', InputDataTypeNotInAllowlistExc),
        ('[["username", "john01"], ["age", 20.9]]', InputDataTypeNotInAllowlistExc),
        ('{"username": "john01", "age": "hello"}', InputDataTypeNotInAllowlistExc),
        ('[["username", "john01"], ["age", "hello"]]', InputDataTypeNotInAllowlistExc),
        ('{"username": "john01", "age": "20"}', InputDataTypeNotInAllowlistExc),
        ('[["username", "john01"], ["age", "20"]]', InputDataTypeNotInAllowlistExc),
        ('{"username": "john01", "age": []}', InputDataTypeNotInAllowlistExc),
        ('[["username", "john01"], ["age", []]]', InputDataTypeNotInAllowlistExc),
        ('{"username": "john01", "age": [20]}', InputDataTypeNotInAllowlistExc),
        ('[["username", "john01"], ["age", [20]]]', InputDataTypeNotInAllowlistExc),
        ('{"username": "john01", "age": {}}', InputDataTypeNotInAllowlistExc),
        ('[["username", "john01"], ["age", {}]]', InputDataTypeNotInAllowlistExc),
        ('{"username": "john01", "age": {"20": 20}}', InputDataTypeNotInAllowlistExc),
        ('[["username", "john01"], ["age", {"20": 20}]]', InputDataTypeNotInAllowlistExc),
        ('{"username": "john01", "age": 15, "extra": "field"}', InvalidInputDataExc),
        ('[["username", "john01"], ["age", 15], ["extra: "field"]]', InvalidInputDataExc),
        ('[["username", "john01", "abc"], ["age", 15]]', InputDataNotConvertibleExc),
        ('[["username", "john01"], ["age", 15, 16]]', InputDataNotConvertibleExc),
        ('[["username"], ["age", 15]]', InputDataNotConvertibleExc),
        ('[["username", "john01"], ["age"]]', InputDataNotConvertibleExc),
        ('[["username", "john01"], [], ["age", 15]]', InputDataNotConvertibleExc),
        ('[["username", "john01"], ["key"], ["age", 15]]', InputDataNotConvertibleExc),
        ('[["username", "john01"], ["key", "value"], ["age", 15]]', InvalidInputDataExc),
        ('[["username", "john01"], ["key", "value", "123"], ["age", 15]]', InputDataNotConvertibleExc),
        ('{"username": "john01"}', InvalidInputDataExc),
        ('[["username", "john01"]]', InvalidInputDataExc),
        ('{"age": 15}', InvalidInputDataExc),
        ('[["age", 15]]', InvalidInputDataExc),
        ('{}', InvalidInputDataExc),
        ('[]', InvalidInputDataExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": "john01", "age": 15}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', JSONTestObjectModel(username="john01", age=15)),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": "\\r\\n\\u2028   john01 \\t   \\u2029\\t\\n\\r", "age": 15}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', JSONTestObjectModel(username="john01", age=15)),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": "ｊｏｈｎ０１", "age": 15}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', JSONTestObjectModel(username="john01", age=15)),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": "\\uff4a\\uff4f\\uff48\\uff4e\\uff10\\uff11", "age": 15}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', JSONTestObjectModel(username="john01", age=15)),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", "john01"], ["age", 15]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', JSONTestObjectModel(username="john01", age=15)),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", "\\r\\n\\u2028   john01 \\t   \\u2029\\t\\n\\r"], ["age", 15]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', JSONTestObjectModel(username="john01", age=15)),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", "ｊｏｈｎ０１"], ["age", 15]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', JSONTestObjectModel(username="john01", age=15)),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", "\\uff4a\\uff4f\\uff48\\uff4e\\uff10\\uff11"], ["age", 15]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', JSONTestObjectModel(username="john01", age=15)),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": "", "age": 15}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', DataValidationFailedExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", ""], ["age", 15]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', DataValidationFailedExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": "ab", "age": 15}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', DataValidationFailedExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", "ab"], ["age", 15]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', DataValidationFailedExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": "abc", "age": 15}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', JSONTestObjectModel(username="abc", age=15)),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", "abc"], ["age", 15]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', JSONTestObjectModel(username="abc", age=15)),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": "abcdefghij", "age": 15}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', JSONTestObjectModel(username="abcdefghij", age=15)),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", "abcdefghij"], ["age", 15]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', JSONTestObjectModel(username="abcdefghij", age=15)),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": "abcdefghijklmno", "age": 15}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', JSONTestObjectModel(username="abcdefghijklmno", age=15)),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", "abcdefghijklmno"], ["age", 15]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', JSONTestObjectModel(username="abcdefghijklmno", age=15)),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": "abcdefghijklmnop", "age": 15}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', DataValidationFailedExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", "abcdefghijklmnop"], ["age", 15]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', DataValidationFailedExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": "abcdefghijklmnop1234567890", "age": 15}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', DataValidationFailedExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", "abcdefghijklmnop1234567890"], ["age", 15]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', DataValidationFailedExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": "John01", "age": 15}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', DataValidationFailedExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", "John01"], ["age", 15]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', DataValidationFailedExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": "JOHN01", "age": 15}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', DataValidationFailedExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", "JOHN01"], ["age", 15]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', DataValidationFailedExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": "johnŠ01", "age": 15}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', DataValidationFailedExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", "johnŠ01"], ["age", 15]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', DataValidationFailedExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": "john\\u015901", "age": 15}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', DataValidationFailedExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", "john\\u015901"], ["age", 15]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', DataValidationFailedExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": "john🤍01", "age": 15}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', DataValidationFailedExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", "john🤍01"], ["age", 15]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', DataValidationFailedExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": "john\\ud83e\\udd0d01", "age": 15}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', DataValidationFailedExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", "john\\ud83e\\udd0d01"], ["age", 15]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', DataValidationFailedExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": "john\\n01", "age": 15}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', DataValidationFailedExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", "john\\n01"], ["age", 15]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', DataValidationFailedExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": "john\\u000001", "age": 15}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', DataValidationFailedExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", "john\\u000001"], ["age", 15]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', DataValidationFailedExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": "john!01", "age": 15}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', DataValidationFailedExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", "john!01"], ["age", 15]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', DataValidationFailedExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": "john.01", "age": 15}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', DataValidationFailedExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", "john.01"], ["age", 15]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', DataValidationFailedExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": "john 01", "age": 15}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', DataValidationFailedExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", "john 01"], ["age", 15]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', DataValidationFailedExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": "john\\t01", "age": 15}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', DataValidationFailedExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", "john\\t01"], ["age", 15]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', DataValidationFailedExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": null, "age": 15}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InputDataTypeNotInAllowlistExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", null], ["age", 15]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InputDataTypeNotInAllowlistExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": true, "age": 15}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InputDataTypeNotInAllowlistExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", true], ["age", 15]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InputDataTypeNotInAllowlistExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": 7, "age": 15}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InputDataTypeNotInAllowlistExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", 7], ["age", 15]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InputDataTypeNotInAllowlistExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": 5.5, "age": 15}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InputDataTypeNotInAllowlistExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", 5.5], ["age", 15]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InputDataTypeNotInAllowlistExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": [], "age": 15}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InputDataTypeNotInAllowlistExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", []], ["age", 15]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InputDataTypeNotInAllowlistExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": ["test"], "age": 15}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InputDataTypeNotInAllowlistExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", ["test"]], ["age", 15]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InputDataTypeNotInAllowlistExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": {}, "age": 15}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InputDataTypeNotInAllowlistExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", {}], ["age", 15]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InputDataTypeNotInAllowlistExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": {"test": "test"}, "age": 15}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InputDataTypeNotInAllowlistExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", {"test": "test"}], ["age", 15]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InputDataTypeNotInAllowlistExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": "john01", "age": 0}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', DataValidationFailedExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", "john01"], ["age", 0]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', DataValidationFailedExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": "john01", "age": 12}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', DataValidationFailedExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", "john01"], ["age", 12]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', DataValidationFailedExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": "john01", "age": 13}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', JSONTestObjectModel(username="john01", age=13)),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", "john01"], ["age", 13]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', JSONTestObjectModel(username="john01", age=13)),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": "john01", "age": 50}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', JSONTestObjectModel(username="john01", age=50)),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", "john01"], ["age", 50]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', JSONTestObjectModel(username="john01", age=50)),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": "john01", "age": 100}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', JSONTestObjectModel(username="john01", age=100)),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", "john01"], ["age", 100]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', JSONTestObjectModel(username="john01", age=100)),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": "john01", "age": 101}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', DataValidationFailedExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", "john01"], ["age", 101]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', DataValidationFailedExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": "john01", "age": 100000000}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', DataValidationFailedExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", "john01"], ["age", 100000000]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', DataValidationFailedExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": "john01", "age": null}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InputDataTypeNotInAllowlistExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", "john01"], ["age", null]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InputDataTypeNotInAllowlistExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": "john01", "age": true}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', DataValidationFailedExc),  # For historic reasons, 'bool' is a subclass of 'int'.
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", "john01"], ["age", true]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', DataValidationFailedExc),  # For historic reasons, 'bool' is a subclass of 'int'.
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": "john01", "age": 20.0}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InputDataTypeNotInAllowlistExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", "john01"], ["age", 20.0]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InputDataTypeNotInAllowlistExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": "john01", "age": 20.9}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InputDataTypeNotInAllowlistExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", "john01"], ["age", 20.9]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InputDataTypeNotInAllowlistExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": "john01", "age": "hello"}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InputDataTypeNotInAllowlistExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", "john01"], ["age", "hello"]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InputDataTypeNotInAllowlistExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": "john01", "age": "20"}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InputDataTypeNotInAllowlistExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", "john01"], ["age", "20"]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InputDataTypeNotInAllowlistExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": "john01", "age": []}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InputDataTypeNotInAllowlistExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", "john01"], ["age", []]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InputDataTypeNotInAllowlistExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": "john01", "age": [20]}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InputDataTypeNotInAllowlistExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", "john01"], ["age", [20]]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InputDataTypeNotInAllowlistExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": "john01", "age": {}}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InputDataTypeNotInAllowlistExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", "john01"], ["age", {}]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InputDataTypeNotInAllowlistExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": "john01", "age": {"20": 20}}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InputDataTypeNotInAllowlistExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", "john01"], ["age", {"20": 20}]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InputDataTypeNotInAllowlistExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": "john01", "age": 15, "extra": "field"}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InvalidInputDataExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", "john01"], ["age", 15], ["extra: "field"]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InvalidInputDataExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", "john01", "abc"], ["age", 15]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InputDataNotConvertibleExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", "john01"], ["age", 15, 16]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InputDataNotConvertibleExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username"], ["age", 15]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InputDataNotConvertibleExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", "john01"], ["age"]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InputDataNotConvertibleExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", "john01"], [], ["age", 15]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InputDataNotConvertibleExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", "john01"], ["key"], ["age", 15]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InputDataNotConvertibleExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", "john01"], ["key", "value"], ["age", 15]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InvalidInputDataExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", "john01"], ["key", "value", "123"], ["age", 15]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InputDataNotConvertibleExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"username": "john01"}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InvalidInputDataExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["username", "john01"]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InvalidInputDataExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {"age": 15}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InvalidInputDataExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  [["age", 15]]  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InvalidInputDataExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  {}  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InvalidInputDataExc),
        ('\n\n\t    \x85\x1d\r\n\r   \u2029\u2028  []  \x1c\x1e\x85\n\n   \t\n   \u2029  ', InvalidInputDataExc),
        ("", InvalidInputDataExc),
        ("hello", InvalidInputDataExc),
        ("he\x00llo", InvalidInputDataExc),
        ('"', InvalidInputDataExc),
        ('"""', InvalidInputDataExc),
        (None, InputDataTypeNotInAllowlistExc),
        ([], InputDataTypeNotInAllowlistExc),
        (str, InputDataTypeNotInAllowlistExc),
        (object(), InputDataTypeNotInAllowlistExc),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc),
    )),
)


@pytest.mark.parametrize(("blueprint", "input_", "output"), theoretical_testutils.test_function_parameter_generator(__JSON_BLUEPRINT_TEST_SUITE))
def test_json_blueprint(blueprint, input_, output):
    theoretical_testutils.perform_test(blueprint, input_, output)


@pytest.mark.parametrize("wrapped_bp", (
    StringBlueprint(bytes_encoding="windows-1250", datetime_string_format="%d.%m.%Y %H:%M:%S", parsing_mode=ParsingMode.MODE_RATIONAL),
    IntegerBlueprint(parsing_mode=ParsingMode.MODE_STRICT),
    BooleanBlueprint(parsing_mode=ParsingMode.MODE_LOOSE),
    GenericBlueprint(),
))
def test_json_blueprint_wrapped_blueprint(wrapped_bp):
    assert JSONBlueprint(wrapped_blueprint=wrapped_bp).get_wrapped_blueprint() is wrapped_bp
