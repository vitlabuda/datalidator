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


from typing import final, Final, Any, Sequence, Generic, TypeVar
import abc
from datalidator.blueprints.DefaultBlueprintWithStandardFeaturesImplBase import DefaultBlueprintWithStandardFeaturesImplBase
from datalidator.blueprints.ParsingMode import ParsingMode
from datalidator.filters.FilterIface import FilterIface
from datalidator.validators.ValidatorIface import ValidatorIface
from datalidator.exc.err.ThisShouldNeverHappenError import ThisShouldNeverHappenError


__all__ = "DefaultBlueprintWithModeSupportImplBase", "DefaultBlueprintWithModeSupportImplBase_T"
DefaultBlueprintWithModeSupportImplBase_T = TypeVar("DefaultBlueprintWithModeSupportImplBase_T")


class DefaultBlueprintWithModeSupportImplBase(DefaultBlueprintWithStandardFeaturesImplBase[DefaultBlueprintWithModeSupportImplBase_T], Generic[DefaultBlueprintWithModeSupportImplBase_T], metaclass=abc.ABCMeta):
    """
    An extension class for DefaultBlueprintWithStandardFeaturesImplBase used by some of this library's built-in blueprints.

    It enables blueprints that extend this base class to make use of parsing modes. See the docstring of the ParsingMode
     class to learn what parsing modes are and how to use them.

    Refer to the class hierarchy document to find out which classes extend this base class.
    """

    __slots__ = "__parsing_mode",

    _DEFAULT_PARSING_MODE: Final[ParsingMode] = ParsingMode.MODE_RATIONAL

    def __init__(self,
                 filters: Sequence[FilterIface[DefaultBlueprintWithModeSupportImplBase_T]] = (),
                 validators: Sequence[ValidatorIface[DefaultBlueprintWithModeSupportImplBase_T]] = (),
                 parsing_mode: ParsingMode = _DEFAULT_PARSING_MODE,
                 tag: str = ""):
        DefaultBlueprintWithStandardFeaturesImplBase.__init__(self, filters, validators, tag)

        self.__parsing_mode: Final[ParsingMode] = parsing_mode

    @classmethod
    @final
    def get_default_parsing_mode(cls) -> ParsingMode:
        return cls._DEFAULT_PARSING_MODE

    @final
    def get_parsing_mode(self) -> ParsingMode:
        return self.__parsing_mode

    @final
    def _parse(self, input_data: Any) -> DefaultBlueprintWithModeSupportImplBase_T:
        parse_func_for_current_mode = ({
            ParsingMode.MODE_LOOSE: self._parse_in_loose_mode,
            ParsingMode.MODE_RATIONAL: self._parse_in_rational_mode,
            ParsingMode.MODE_STRICT: self._parse_in_strict_mode
        }.get(self.__parsing_mode, None))

        if parse_func_for_current_mode is None:
            # This can happen only if the library is used incorrectly (not according to type annotations in this case)
            raise ThisShouldNeverHappenError(
                "The supplied parsing mode (of type '{}') is invalid: {}".format(self.__parsing_mode.__class__.__name__, repr(self.__parsing_mode)),
                self._tag
            )

        return parse_func_for_current_mode(input_data)

    @abc.abstractmethod
    def _parse_in_loose_mode(self, input_data: Any) -> DefaultBlueprintWithModeSupportImplBase_T:
        """
        Converts untrusted (!) 'input_data' into output data of generic type 'VT' in an appropriate way, when the
         blueprint is in loose mode. See the docstring of the 'DefaultBlueprintWithStandardFeaturesImplBase._parse()'
         method for general rules of parsing input data and the docstring of the 'ParsingMode' class for information
         regarding parsing modes.

        :param input_data: The untrusted input data to be converted to output data.
        :return: The output data of generic type 'VT'.
        :raises DatalidatorExc: The superclass of all exceptions raised by this library.
        """

        raise NotImplementedError(DefaultBlueprintWithModeSupportImplBase._parse_in_loose_mode.__qualname__)

    @abc.abstractmethod
    def _parse_in_rational_mode(self, input_data: Any) -> DefaultBlueprintWithModeSupportImplBase_T:
        """
        Converts untrusted (!) 'input_data' into output data of generic type 'VT' in an appropriate way, when the
         blueprint is in rational mode. See the docstring of the 'DefaultBlueprintWithStandardFeaturesImplBase._parse()'
         method for general rules of parsing input data and the docstring of the 'ParsingMode' class for information
         regarding parsing modes.

        :param input_data: The untrusted input data to be converted to output data.
        :return: The output data of generic type 'VT'.
        :raises DatalidatorExc: The superclass of all exceptions raised by this library.
        """

        raise NotImplementedError(DefaultBlueprintWithModeSupportImplBase._parse_in_rational_mode.__qualname__)

    @abc.abstractmethod
    def _parse_in_strict_mode(self, input_data: Any) -> DefaultBlueprintWithModeSupportImplBase_T:
        """
        Converts untrusted (!) 'input_data' into output data of generic type 'VT' in an appropriate way, when the
         blueprint is in strict mode. See the docstring of the 'DefaultBlueprintWithStandardFeaturesImplBase._parse()'
         method for general rules of parsing input data and the docstring of the 'ParsingMode' class for information
         regarding parsing modes.

        :param input_data: The untrusted input data to be converted to output data.
        :return: The output data of generic type 'VT'.
        :raises DatalidatorExc: The superclass of all exceptions raised by this library.
        """

        raise NotImplementedError(DefaultBlueprintWithModeSupportImplBase._parse_in_strict_mode.__qualname__)
