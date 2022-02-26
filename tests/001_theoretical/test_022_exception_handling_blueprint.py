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

from typing import List
import theoretical_testutils
import pytest
import re
import datetime
from datalidator.blueprints.ParsingMode import ParsingMode
from datalidator.blueprints.specialimpl.ExceptionHandlingBlueprint import ExceptionHandlingBlueprint
from datalidator.blueprints.impl.StringBlueprint import StringBlueprint
from datalidator.blueprints.impl.ListBlueprint import ListBlueprint
from datalidator.blueprints.impl.BooleanBlueprint import BooleanBlueprint
from datalidator.blueprints.impl.GenericBlueprint import GenericBlueprint
from datalidator.filters.impl.StringRegexReplaceFilter import StringRegexReplaceFilter
from datalidator.validators.impl.AllowlistValidator import AllowlistValidator


__EXCEPTION_HANDLING_BLUEPRINT_TEST_SUITE = (
    (ExceptionHandlingBlueprint[str](
        wrapped_blueprint=StringBlueprint(parsing_mode=ParsingMode.MODE_STRICT),
        default_value="řeřicha\r\n"
    ), (
        # InputDataTypeNotInAllowlistExc
        ("", ""),
        ("abc", "abc"),
        ("řeřicha\r\n", "řeřicha\r\n"),
        ("hello world\r\n", "hello world\r\n"),
        ("hello🤍world", "hello🤍world"),
        ("hello\x00world\n", "hello\x00world\n"),
        (None, "řeřicha\r\n"),
        (True, "řeřicha\r\n"),
        (1, "řeřicha\r\n"),
        (1.5, "řeřicha\r\n"),
        (1+5j, "řeřicha\r\n"),
        (datetime.datetime.now(), "řeřicha\r\n"),
        (b'', "řeřicha\r\n"),
        (b'hello world', "řeřicha\r\n"),
        (str, "řeřicha\r\n"),
        (object(), "řeřicha\r\n"),
        (theoretical_testutils.EmptyObject(), "řeřicha\r\n"),
    )),
    (ExceptionHandlingBlueprint[List[bool]](
        wrapped_blueprint=ListBlueprint(
            item_blueprint=BooleanBlueprint(parsing_mode=ParsingMode.MODE_RATIONAL),
            parsing_mode=ParsingMode.MODE_RATIONAL
        ),
        default_value=[True, False, True]
    ), (
        # InputDataNotConvertibleExc & InputDataTypeInBlocklistExc & InputDataValueNotAllowedForDataTypeExc & InputDataTypeNotInAllowlistExc
        (None, [True, False, True]),
        (False, [True, False, True]),
        (1, [True, False, True]),
        (1.5, [True, False, True]),
        ("", [True, False, True]),
        ("abc", [True, False, True]),
        (b"", [True, False, True]),
        (b"abc", [True, False, True]),
        (dict(), [True, False, True]),
        ({True: False, False: True}, [True, False, True]),
        (["false", "", "off"], [True, False, True]),
        (["false", "\x00", "off"], [True, False, True]),
        (["false", "hello", "off"], [True, False, True]),
        (["false", bool, "off"], [True, False, True]),
        (["false", object(), "off"], [True, False, True]),
        (["false", theoretical_testutils.EmptyObject(), "off"], [True, False, True]),
        (["false"], [False]),
        ([1, 1.0, "false", True], [True, True, False, True]),
        ([1, 1.0, "false", True, "\r\n   FALse \x85\u2029   \t  "], [True, True, False, True, False]),
        ([0.0, 1, 1.0, "false", True, "\r\n   FALse \x85\u2029   \t  "], [False, True, True, False, True, False]),
        (list, [True, False, True]),
        (object(), [True, False, True]),
        (theoretical_testutils.EmptyObject(), [True, False, True]),
    )),
    (ExceptionHandlingBlueprint[str](
        wrapped_blueprint=StringBlueprint(
            filters=(StringRegexReplaceFilter(r'abc', lambda x: theoretical_testutils.EmptyObject(), regex_compile_flags=re.IGNORECASE),),  # noqa
            parsing_mode=ParsingMode.MODE_STRICT
        ),
        default_value="\x00🤍"
    ), (
        # InputDataTypeNotInAllowlistExc & RegexFailedInFilterExc
        ("", ""),
        ("hello world", "hello world"),
        ("hello\x00🤍world", "hello\x00🤍world"),
        ("řeřicha\r\n", "řeřicha\r\n"),
        ("hello abc world", "\x00🤍"),
        ("HELLO\tABC\uffffWORLD", "\x00🤍"),
        ("Abc Abc", "\x00🤍"),
        ("aBC aBC", "\x00🤍"),
        (None, "\x00🤍"),
        (1, "\x00🤍"),
        (1.5, "\x00🤍"),
        (1+2j, "\x00🤍"),
        ([], "\x00🤍"),
        (str, "\x00🤍"),
        (object(), "\x00🤍"),
        (theoretical_testutils.EmptyObject(), "\x00🤍"),
    )),
    (ExceptionHandlingBlueprint[str](
        wrapped_blueprint=StringBlueprint(
            validators=(AllowlistValidator(["", "False", "hello", "\x00", "hello 🤍"]),),
            parsing_mode=ParsingMode.MODE_LOOSE
        ),
        default_value="hello"
    ), (
        # DataValidationFailedExc
        (None, "hello"),
        (True, "hello"),
        (False, "False"),
        (1, "hello"),
        (1.5, "hello"),
        (1+2j, "hello"),
        ([], "hello"),
        ("", ""),
        ("False", "False"),
        ("hello", "hello"),
        ("\x00", "\x00"),
        ("\x00 ", "hello"),
        (" \x00", "hello"),
        ("\x00\x00", "hello"),
        ("hello 🤍", "hello 🤍"),
        ("abc", "hello"),
        ("řeřicha", "hello"),
        ("Příliš žluťoučký kůň", "hello"),
        ("\uffff", "hello"),
        (str, "hello"),
        (object(), "hello"),
        (theoretical_testutils.EmptyObject(), "hello"),
    )),
)


@pytest.mark.parametrize(("blueprint", "input_", "output"), theoretical_testutils.test_function_parameter_generator(__EXCEPTION_HANDLING_BLUEPRINT_TEST_SUITE))
def test_exception_handling_blueprint(blueprint, input_, output):
    theoretical_testutils.perform_test(blueprint, input_, output)


@pytest.mark.parametrize(("wrapped_bp", "default"), (  
        (StringBlueprint(), "hello"),
        (StringBlueprint(bytes_encoding="ascii", parsing_mode=ParsingMode.MODE_RATIONAL), ""),
        (BooleanBlueprint(parsing_mode=ParsingMode.MODE_LOOSE), False),
        (BooleanBlueprint(parsing_mode=ParsingMode.MODE_STRICT), True),
        (GenericBlueprint(), theoretical_testutils.EmptyObject()),
        (GenericBlueprint(), object()),
))
def test_exception_handling_blueprint_instance_attributes(wrapped_bp, default):
    blueprint = ExceptionHandlingBlueprint(wrapped_blueprint=wrapped_bp, default_value=default)

    assert (blueprint.get_wrapped_blueprint() is wrapped_bp) and (blueprint.get_default_value() is default)
