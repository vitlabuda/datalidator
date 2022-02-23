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

from typing import Any, Final
import theoretical_testutils
import pytest
from datalidator.blueprints.DefaultBlueprintImplBase import DefaultBlueprintImplBase
from datalidator.blueprints.impl.GenericBlueprint import GenericBlueprint
from datalidator.blueprints.exc.UnexpectedExceptionRaisedInBlueprintExc import UnexpectedExceptionRaisedInBlueprintExc
from datalidator.filters.DefaultFilterImplBase import DefaultFilterImplBase
from datalidator.filters.exc.UnexpectedExceptionRaisedInFilterExc import UnexpectedExceptionRaisedInFilterExc
from datalidator.validators.DefaultValidatorImplBase import DefaultValidatorImplBase
from datalidator.validators.exc.UnexpectedExceptionRaisedInValidatorExc import UnexpectedExceptionRaisedInValidatorExc


class UnexpectedException(Exception):
    pass


class UnexpectedArithmeticError(ArithmeticError):
    pass


class UnexpectedKeyError(KeyError):
    pass


class UnexpectedOSError(OSError):
    pass


class UnexpectedRuntimeError(RuntimeError):
    pass


class UnexpectedTypeError(TypeError):
    pass


class UnexpectedValueError(ValueError):
    pass


__EXCEPTION_CLASSES = (
    Exception,
    ArithmeticError,
    FloatingPointError,
    OverflowError,
    ZeroDivisionError,
    AssertionError,
    AttributeError,
    BufferError,
    EOFError,
    ImportError,
    ModuleNotFoundError,
    LookupError,
    IndexError,
    KeyError,
    MemoryError,
    NameError,
    UnboundLocalError,
    OSError,
    BlockingIOError,
    ChildProcessError,
    ConnectionError,
    BrokenPipeError,
    ConnectionAbortedError,
    ConnectionRefusedError,
    ConnectionResetError,
    FileExistsError,
    FileNotFoundError,
    InterruptedError,
    IsADirectoryError,
    NotADirectoryError,
    PermissionError,
    ProcessLookupError,
    TimeoutError,
    ReferenceError,
    RuntimeError,
    NotImplementedError,
    RecursionError,
    SyntaxError,
    IndentationError,
    TabError,
    SystemError,
    TypeError,
    ValueError,
    UnicodeError,
    UnexpectedException,
    UnexpectedArithmeticError,
    UnexpectedKeyError,
    UnexpectedOSError,
    UnexpectedRuntimeError,
    UnexpectedTypeError,
    UnexpectedValueError,
    theoretical_testutils.TestException,
)


class UnexpectedExceptionRaisingBlueprint(DefaultBlueprintImplBase[Any]):
    def __init__(self, raised_exception: Exception):
        DefaultBlueprintImplBase.__init__(self)

        self.__raised_exception: Final[Exception] = raised_exception

    def _use(self, input_data: Any) -> Any:
        raise self.__raised_exception


class UnexpectedExceptionRaisingFilter(DefaultFilterImplBase[Any]):
    def __init__(self, raised_exception: Exception):
        DefaultFilterImplBase.__init__(self)

        self.__raised_exception: Final[Exception] = raised_exception

    def _filter(self, data: Any) -> Any:
        raise self.__raised_exception


class UnexpectedExceptionRaisingValidator(DefaultValidatorImplBase[Any]):
    def __init__(self, raised_exception: Exception):
        DefaultValidatorImplBase.__init__(self)

        self.__raised_exception: Final[Exception] = raised_exception

    def _validate(self, data: Any) -> None:
        raise self.__raised_exception


def blueprint_test_function_parameter_generator(exception_classes):
    for exception_class in exception_classes:
        yield UnexpectedExceptionRaisingBlueprint(raised_exception=exception_class())


def filter_test_function_parameter_generator(exception_classes):
    for exception_class in exception_classes:
        yield GenericBlueprint(filters=(UnexpectedExceptionRaisingFilter(raised_exception=exception_class()),))


def validator_test_function_parameter_generator(exception_classes):
    for exception_class in exception_classes:
        yield GenericBlueprint(validators=(UnexpectedExceptionRaisingValidator(raised_exception=exception_class()),))


@pytest.mark.parametrize("blueprint", blueprint_test_function_parameter_generator(__EXCEPTION_CLASSES))
def test_unexpected_exception_raised_in_blueprint(blueprint):
    with pytest.raises(UnexpectedExceptionRaisedInBlueprintExc):
        blueprint.use(theoretical_testutils.EmptyObject())


@pytest.mark.parametrize("blueprint_with_filter", filter_test_function_parameter_generator(__EXCEPTION_CLASSES))
def test_unexpected_exception_raised_in_filter(blueprint_with_filter):
    with pytest.raises(UnexpectedExceptionRaisedInFilterExc):
        blueprint_with_filter.use(theoretical_testutils.EmptyObject())


@pytest.mark.parametrize("blueprint_with_validator", validator_test_function_parameter_generator(__EXCEPTION_CLASSES))
def test_unexpected_exception_raised_in_validator(blueprint_with_validator):
    with pytest.raises(UnexpectedExceptionRaisedInValidatorExc):
        blueprint_with_validator.use(theoretical_testutils.EmptyObject())
