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


from typing import final, Final, Any, Tuple, Optional, Type
from datalidator.blueprints.DefaultBlueprintWithModeSupportImplBase import DefaultBlueprintWithModeSupportImplBase


__all__ = "BooleanBlueprint",


class BooleanBlueprint(DefaultBlueprintWithModeSupportImplBase[bool]):
    """
    INPUT in loose mode:
    - any object that can be passed to bool()
    * there is no special handling for some values as in rational mode

    INPUT in rational mode:
    - 'bool' object
    - 'int' object with one of the following values: 0, 1
    - 'float' object with one of the following values: 0.0, 1.0
    - 'str' object with one of the following values (case-insensitive): '1', 'yes', 'y', 'true', 'on', '0', 'no', 'n', 'false', 'off'

    INPUT in strict mode:
    - 'bool' object

    OUTPUT:
    - 'bool' object
    """

    __slots__ = ()

    __TRUE_STRINGS: Final[Tuple[str, ...]] = ("1", "yes", "y", "true", "on")  # Must be lowercase only!
    __FALSE_STRINGS: Final[Tuple[str, ...]] = ("0", "no", "n", "false", "off")  # Must be lowercase only!

    def _get_allowed_output_data_types(self) -> Optional[Tuple[Type, ...]]:
        return bool,

    def _parse_in_loose_mode(self, input_data: Any) -> bool:
        return self.__perform_generic_conversion_to_bool(input_data)

    def _parse_in_rational_mode(self, input_data: Any) -> bool:
        return self._data_conversion_helper.convert_input_using_per_data_type_converter_functions(
            (
                ((bool,), self.__perform_generic_conversion_to_bool),
                ((int,), self.__convert_int_to_bool_rationally),
                ((float,), self.__convert_float_to_bool_rationally),
                ((str,), self.__convert_str_to_bool_rationally)
            ),
            input_data
        )

    def _parse_in_strict_mode(self, input_data: Any) -> bool:
        return self._data_conversion_helper.convert_input_with_data_type_allowlist(
            self.__perform_generic_conversion_to_bool, (bool,), input_data
        )

    @final
    def __perform_generic_conversion_to_bool(self, input_data: Any) -> bool:
        try:
            return bool(input_data)  # /Any/ object can be turned into a boolean
        except Exception:
            raise self._invalid_input_data_exc_factory.generate_input_data_not_convertible_exc((bool,), input_data)

    @final
    def __convert_int_to_bool_rationally(self, input_data: int) -> bool:
        if input_data == 1:
            return True

        if input_data == 0:
            return False

        raise self._invalid_input_data_exc_factory.generate_input_data_value_not_allowed_for_data_type_exc(int, (1, 0), input_data)

    @final
    def __convert_float_to_bool_rationally(self, input_data: float) -> bool:
        if input_data == 1.0:
            return True

        if input_data == 0.0:
            return False

        raise self._invalid_input_data_exc_factory.generate_input_data_value_not_allowed_for_data_type_exc(float, (1.0, 0.0), input_data)

    @final
    def __convert_str_to_bool_rationally(self, input_data: str) -> bool:
        canonicalized_string = input_data.strip().lower()
        if canonicalized_string in self.__class__.__TRUE_STRINGS:
            return True

        if canonicalized_string in self.__class__.__FALSE_STRINGS:
            return False

        raise self._invalid_input_data_exc_factory.generate_input_data_value_not_allowed_for_data_type_exc(
            str, (self.__class__.__TRUE_STRINGS + self.__class__.__FALSE_STRINGS), input_data
        )
