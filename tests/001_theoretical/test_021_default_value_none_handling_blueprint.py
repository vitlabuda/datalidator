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

from typing import Any
import theoretical_testutils
import pytest
import ipaddress
from datalidator.blueprints.ParsingMode import ParsingMode
from datalidator.blueprints.specialimpl.DefaultValueNoneHandlingBlueprint import DefaultValueNoneHandlingBlueprint
from datalidator.blueprints.impl.BooleanBlueprint import BooleanBlueprint
from datalidator.blueprints.impl.StringBlueprint import StringBlueprint
from datalidator.blueprints.impl.GenericBlueprint import GenericBlueprint
from datalidator.blueprints.exc.InputDataTypeNotInAllowlistExc import InputDataTypeNotInAllowlistExc
from datalidator.blueprints.exc.InputDataValueNotAllowedForDataTypeExc import InputDataValueNotAllowedForDataTypeExc


__DEFAULT_VALUE_NONE_HANDLING_BLUEPRINT = (
    (DefaultValueNoneHandlingBlueprint[bool](
        wrapped_blueprint=BooleanBlueprint(parsing_mode=ParsingMode.MODE_RATIONAL),
        default_value=True
    ), (
        (None, True),
        (True, True),
        (False, False),
        (0, False),
        (-1, InputDataValueNotAllowedForDataTypeExc),
        (0.0, False),
        (0.1, InputDataValueNotAllowedForDataTypeExc),
        ("true", True),
        ("false", False),
        ("\r\n   On \x85\u2029", True),
        ("\t\f\r   OFF\n\n", False),
        ("hello", InputDataValueNotAllowedForDataTypeExc),
        ("", InputDataValueNotAllowedForDataTypeExc),
        ("None", InputDataValueNotAllowedForDataTypeExc),
        (bool, InputDataTypeNotInAllowlistExc),
        (object(), InputDataTypeNotInAllowlistExc),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc),
    )),
    (DefaultValueNoneHandlingBlueprint[bool](
        wrapped_blueprint=BooleanBlueprint(parsing_mode=ParsingMode.MODE_RATIONAL),
        default_value=False
    ), (
        (None, False),
        (True, True),
        (False, False),
        (0, False),
        (-1, InputDataValueNotAllowedForDataTypeExc),
        (0.0, False),
        (0.1, InputDataValueNotAllowedForDataTypeExc),
        ("true", True),
        ("false", False),
        ("\r\n   On \x85\u2029", True),
        ("\t\f\r   OFF\n\n", False),
        ("hello", InputDataValueNotAllowedForDataTypeExc),
        ("", InputDataValueNotAllowedForDataTypeExc),
        ("None", InputDataValueNotAllowedForDataTypeExc),
        (bool, InputDataTypeNotInAllowlistExc),
        (object(), InputDataTypeNotInAllowlistExc),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc),
    )),
    (DefaultValueNoneHandlingBlueprint[str](
        wrapped_blueprint=StringBlueprint(parsing_mode=ParsingMode.MODE_STRICT),
        default_value="🤍"
    ), (
        (None, "🤍"),
        (True, InputDataTypeNotInAllowlistExc),
        (1, InputDataTypeNotInAllowlistExc),
        (1.5, InputDataTypeNotInAllowlistExc),
        (b'hello world', InputDataTypeNotInAllowlistExc),
        ("", ""),
        ("hello world", "hello world"),
        ("\n\r   Příliš žluťoučký\x00kůň\uffff  úpěl\aďábelské ódy.  \x85\u2029", "\n\r   Příliš žluťoučký\x00kůň\uffff  úpěl\aďábelské ódy.  \x85\u2029"),
        ("🤍", "🤍"),
        ("None", "None"),
        (str, InputDataTypeNotInAllowlistExc),
        (object(), InputDataTypeNotInAllowlistExc),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc),
    )),
    (DefaultValueNoneHandlingBlueprint[str](
        wrapped_blueprint=StringBlueprint(parsing_mode=ParsingMode.MODE_STRICT),
        default_value=""
    ), (
        (None, ""),
        (True, InputDataTypeNotInAllowlistExc),
        (1, InputDataTypeNotInAllowlistExc),
        (1.5, InputDataTypeNotInAllowlistExc),
        (b'hello world', InputDataTypeNotInAllowlistExc),
        ("", ""),
        ("hello world", "hello world"),
        ("\n\r   Příliš žluťoučký\x00kůň\uffff  úpěl\aďábelské ódy.  \x85\u2029", "\n\r   Příliš žluťoučký\x00kůň\uffff  úpěl\aďábelské ódy.  \x85\u2029"),
        ("🤍", "🤍"),
        ("None", "None"),
        (str, InputDataTypeNotInAllowlistExc),
        (object(), InputDataTypeNotInAllowlistExc),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc),
    )),
    (DefaultValueNoneHandlingBlueprint[Any](
        wrapped_blueprint=GenericBlueprint(),
        default_value=theoretical_testutils.EmptyObject()
    ), (
        (None, theoretical_testutils.EmptyObject()),
        (False, False),
        (1, 1),
        (1.5, 1.5),
        (float("-inf"), float("-inf")),
        ("hello world\r\n", "hello world\r\n"),
        ("🤍", "🤍"),
        ("None", "None"),
        (b'abc', b'abc'),
        (str, str),
        (object, object),
        (theoretical_testutils.EmptyObject(), theoretical_testutils.EmptyObject()),
    )),
    (DefaultValueNoneHandlingBlueprint[Any](
        wrapped_blueprint=GenericBlueprint(),
        default_value=ipaddress.ip_network("127.1.2.0/24")
    ), (
        (None, ipaddress.ip_network("127.1.2.0/24")),
        (False, False),
        (1, 1),
        (1.5, 1.5),
        (float("-inf"), float("-inf")),
        ("hello world\r\n", "hello world\r\n"),
        ("🤍", "🤍"),
        ("None", "None"),
        (b'abc', b'abc'),
        (str, str),
        (object, object),
        (theoretical_testutils.EmptyObject(), theoretical_testutils.EmptyObject()),
    )),
)


@pytest.mark.parametrize(("blueprint", "input_", "output"), theoretical_testutils.test_function_parameter_generator(__DEFAULT_VALUE_NONE_HANDLING_BLUEPRINT))
def test_default_value_none_handling_blueprint(blueprint, input_, output):
    theoretical_testutils.perform_test(blueprint, input_, output)


@pytest.mark.parametrize(("wrapped_bp", "default"), (  
        (StringBlueprint(), "hello"),
        (StringBlueprint(bytes_encoding="ascii", parsing_mode=ParsingMode.MODE_RATIONAL), ""),
        (BooleanBlueprint(parsing_mode=ParsingMode.MODE_LOOSE), False),
        (BooleanBlueprint(parsing_mode=ParsingMode.MODE_STRICT), True),
        (GenericBlueprint(), theoretical_testutils.EmptyObject()),
        (GenericBlueprint(), object()),
))
def test_default_value_none_handling_blueprint_instance_attributes(wrapped_bp, default):
    blueprint = DefaultValueNoneHandlingBlueprint(wrapped_blueprint=wrapped_bp, default_value=default)

    assert (blueprint.get_wrapped_blueprint() is wrapped_bp) and (blueprint.get_default_value() is default)
