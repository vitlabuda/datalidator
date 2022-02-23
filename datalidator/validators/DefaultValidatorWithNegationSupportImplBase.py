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


from typing import final, Final, Generic, TypeVar
import abc
from datalidator.validators.DefaultValidatorImplBase import DefaultValidatorImplBase


__all__ = "DefaultValidatorWithNegationSupportImplBase", "DefaultValidatorWithNegationSupportImplBase_T"
DefaultValidatorWithNegationSupportImplBase_T = TypeVar("DefaultValidatorWithNegationSupportImplBase_T")


class DefaultValidatorWithNegationSupportImplBase(DefaultValidatorImplBase[DefaultValidatorWithNegationSupportImplBase_T], Generic[DefaultValidatorWithNegationSupportImplBase_T], metaclass=abc.ABCMeta):
    """
    An extension class for DefaultValidatorImplBase used by some of this library's built-in validators.

    It provides this class's subclasses with a standard way of negating their validated condition. For example, the
     built-in StringContainsSubstringValidator considers the input string valid if it contains an initializer-provided
     substring by default. When negated (using an initializer argument), it considers the input string valid if it
     does NOT contain the substring.

    Built-in validators extending this base class have their behaviour properly documented in both validation modes.
     Refer to the class hierarchy document to find out which classes extend this class.
    """

    __slots__ = "__negate",

    def __init__(self, negate: bool = False, tag: str = ""):
        DefaultValidatorImplBase.__init__(self, tag)

        self.__negate: Final[bool] = negate

    @final
    def is_negated(self) -> bool:
        return self.__negate

    @final
    def _validate(self, data: DefaultValidatorWithNegationSupportImplBase_T) -> None:
        if self.__negate:
            return self._validate_negatively(data)

        return self._validate_positively(data)

    @abc.abstractmethod
    def _validate_positively(self, data: DefaultValidatorWithNegationSupportImplBase_T) -> None:
        """
        Checks whether 'data' meet the validator's default requirements. See this class's docstring for more information.

        :param data: The parsed data (i.e. NOT the untrusted input data!) to check.
        :raises DatalidatorExc: The superclass of all exceptions raised by this library.
        """

        raise NotImplementedError(DefaultValidatorWithNegationSupportImplBase._validate_positively.__qualname__)

    @abc.abstractmethod
    def _validate_negatively(self, data: DefaultValidatorWithNegationSupportImplBase_T) -> None:
        """
        Checks whether 'data' meet the validator's negated requirements. See this class's docstring for more information.

        :param data: The parsed data (i.e. NOT the untrusted input data!) to check.
        :raises DatalidatorExc: The superclass of all exceptions raised by this library.
        """

        raise NotImplementedError(DefaultValidatorWithNegationSupportImplBase._validate_negatively.__qualname__)
