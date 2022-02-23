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


from typing import final, Final, Any, Tuple, Type, Sequence, Optional
import math
from datalidator.blueprints.DefaultBlueprintWithModeSupportImplBase import DefaultBlueprintWithModeSupportImplBase
from datalidator.blueprints.ParsingMode import ParsingMode
from datalidator.filters.FilterIface import FilterIface
from datalidator.validators.ValidatorIface import ValidatorIface


__all__ = "FloatBlueprint",


class FloatBlueprint(DefaultBlueprintWithModeSupportImplBase[float]):
    """
    INPUT in loose mode:
    - any object that can be passed to float()

    INPUT in rational mode:
    - 'float' object
    - 'int' object
    - 'bool' object
    - 'str' object containing a numeric value

    INPUT in strict mode:
    - 'float' object
    - 'int' object

    OUTPUT:
    - 'float' object
    """

    __slots__ = "__allow_ieee754_special_values",

    # The rationality of 'bool' being converted to 'int' can be controversial
    __RATIONAL_MODE_DATA_TYPE_ALLOWLIST: Final[Tuple[Type, ...]] = (float, int, bool, str)
    __STRICT_MODE_DATA_TYPE_ALLOWLIST: Final[Tuple[Type, ...]] = (float,)

    def __init__(self,
                 allow_ieee754_special_values: bool = False,
                 filters: Sequence[FilterIface[float]] = (),
                 validators: Sequence[ValidatorIface[float]] = (),
                 parsing_mode: ParsingMode = DefaultBlueprintWithModeSupportImplBase._DEFAULT_PARSING_MODE,
                 tag: str = ""):
        DefaultBlueprintWithModeSupportImplBase.__init__(self, filters, validators, parsing_mode, tag)

        self.__allow_ieee754_special_values: Final[bool] = allow_ieee754_special_values

    @final
    def are_ieee754_special_values_allowed(self) -> bool:
        return self.__allow_ieee754_special_values

    def _get_allowed_output_data_types(self) -> Optional[Tuple[Type, ...]]:
        return float,

    def _parse_in_loose_mode(self, input_data: Any) -> float:
        return self.__convert_input_data_to_float(input_data)

    def _parse_in_rational_mode(self, input_data: Any) -> float:
        return self._data_conversion_helper.convert_input_with_data_type_allowlist(
            self.__convert_input_data_to_float, self.__class__.__RATIONAL_MODE_DATA_TYPE_ALLOWLIST, input_data
        )

    def _parse_in_strict_mode(self, input_data: Any) -> float:
        return self._data_conversion_helper.convert_input_with_data_type_allowlist(
            self.__convert_input_data_to_float, self.__class__.__STRICT_MODE_DATA_TYPE_ALLOWLIST, input_data
        )

    @final
    def __convert_input_data_to_float(self, input_data: Any) -> float:
        original_input_data = input_data  # The exceptions should get the unmodified input data, so they can be relevant
        if isinstance(input_data, str):
            input_data = input_data.replace(",", ".")  # In some countries, commas are used as decimal separators instead of dots

        try:
            # If a string is converted to float, initial and trailing whitespace is automatically stripped from it
            #  (standard behaviour of the float() class)
            # float() accepts strings containing integers (e.g. "4") too (important!)
            number = float(input_data)
        except Exception:  # Can be TypeError, ValueError, ...
            raise self._invalid_input_data_exc_factory.generate_input_data_not_convertible_exc((float,), original_input_data)

        # This check is not implemented as a validator, because a badly programmed filter (filters are executed before
        #  validators) could obtain an IEEE 754 special value and behave unexpectedly which could negatively affect a
        #  whole program's security, if an untrusted user input was parsed. Furthermore, and even more importantly,
        #  the following functionality would have to be implemented by both a filter ("normalizing" -0.0 to 0.0) and
        #  a validator (checking the finiteness of the float) which would be impractical.
        if not self.__allow_ieee754_special_values:
            if number == (-0.0):
                number = 0.0

            if not math.isfinite(number):
                raise self._invalid_input_data_exc_factory.generate_invalid_input_data_exc(
                    "The parsed float value is not finite: {}".format(number),
                    original_input_data
                )

        return number
