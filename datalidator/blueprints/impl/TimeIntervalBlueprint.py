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


from typing import final, Final, Any, Union, Dict, Tuple, Optional, Sequence, Type
import math
import re
from datalidator.blueprints.DefaultBlueprintWithStandardFeaturesImplBase import DefaultBlueprintWithStandardFeaturesImplBase


__all__ = "TimeIntervalBlueprint",


class TimeIntervalBlueprint(DefaultBlueprintWithStandardFeaturesImplBase[float]):
    """
    INPUT:
    - 'int' or 'float' object with a non-negative value
    - 'str' object with a non-negative numeric value or a time interval string (see below)

    OUTPUT:
    - 'float' object with a non-negative value representing seconds

    TIME INTERVAL STRING FORMAT:
    A time interval string consists of one or more non-duplicate whitespace-separated tokens in the following format:
     ([0-9]+(y|year|years))? ([0-9]+(d|day|days))? ([0-9]+(h|hour|hours))? ([0-9]+(min|minute|minutes))? ([0-9]+(s|second|seconds))? ([0-9]+(ms|millisecond|milliseconds))?
    Keep in mind that the tokens must be ordered from the most significant (years) to the least significant (milliseconds).
    Examples:
    - '1y 7d 23h 10min 1s 50ms'
    - '1year 7days 23hours 10minutes 1second 50milliseconds'
    - '10min'
    - '0s'
    - '23h 500ms'
    Note: A year is always considered to be 365 days.

    NOTE: This blueprint is useful, for example, when one needs to provide time intervals in an app's settings for
     things like connection timeout, login token validity duration, password validity duration, etc.
    """

    __slots__ = ()

    # THIS DICTIONARY MUST NOT BE MUTATED!!!
    __FORMATTED_STRING_UNIT_SPECIFIERS: Final[Dict[str, Tuple[float, Optional[int]]]] = {
        # unit:lowercase_str -> (multiplier:float, max_value:int/None)

        # Millisecond
        "ms": (0.001, 999),
        "millisecond": (0.001, 999),
        "milliseconds": (0.001, 999),

        # Second
        "s": (1., 59),
        "second": (1., 59),
        "seconds": (1., 59),

        # Minute
        "min": (60., 59),
        "minute": (60., 59),
        "minutes": (60., 59),

        # Hour
        "h": (3600., 23),
        "hour": (3600., 23),
        "hours": (3600., 23),

        # Day
        "d": (86400., 364),
        "day": (86400., 364),
        "days": (86400., 364),

        # Month is not there, because it is ambiguous as a unit (1 month = 28/29/30/31 days)
        # Year (= 365 days)
        "y": (31536000., None),
        "year": (31536000., None),
        "years": (31536000., None)
    }

    def _get_allowed_output_data_types(self) -> Optional[Tuple[Type, ...]]:
        return float,

    # Can parse: number of seconds as int, float or str; human-readable string (e.g. "7d 23h 10min 1s 50ms")
    def _parse(self, input_data: Any) -> float:
        numeric_interval = self._data_conversion_helper.convert_input_using_per_data_type_converter_functions(
            (
                ((str,), self.__convert_str_to_interval),
                ((int, float), self.__convert_number_to_interval)
            ),
            input_data
        )

        return self.__check_output_interval(numeric_interval, input_data)

    @final
    def __convert_str_to_interval(self, input_data: str) -> float:
        try:
            numeric_interval = float(input_data)
        except Exception:  # noqa; Can be ValueError, ...
            pass
        else:
            # In the first version of the library, this call is unnecessary, but it is possible that the called method
            #  will be extended in the future.
            return self.__convert_number_to_interval(numeric_interval)

        return self.__convert_formatted_interval_string_to_interval(input_data)

    @final
    def __convert_formatted_interval_string_to_interval(self, input_data: str) -> float:
        tokens = self.__tokenize_interval_string(input_data)
        numeric_interval = 0.0

        # itertools.reduce() could also be used here
        for quantity, multiplier in tokens:
            numeric_interval += (quantity * multiplier)

        return numeric_interval

    @final
    def __tokenize_interval_string(self, input_data: str) -> Sequence[Tuple[int, float]]:  # (quantity:int, multiplier:float)
        # Canonicalize & split the string into tokens
        string_tokens = input_data.lower().split()  # str.split() removes unnecessary whitespace automatically
        if len(string_tokens) == 0:
            raise self._invalid_input_data_exc_factory.generate_invalid_input_data_exc("The supplied time interval string is empty!", input_data)

        # Parse the tokens
        parsed_tokens = tuple(self.__parse_interval_string_token(string_token, input_data) for string_token in string_tokens)

        # Check if the units are ordered correctly - from the most significant to the least significant
        last_seen_multiplier = 0.0
        for _, multiplier in reversed(parsed_tokens):
            if multiplier <= last_seen_multiplier:
                raise self._invalid_input_data_exc_factory.generate_invalid_input_data_exc(
                    "The units in the supplied time interval string are not ordered correctly - from the most significant to the least significant, or are duplicate: {}".format(repr(input_data)),
                    input_data
                )

            last_seen_multiplier = multiplier

        return parsed_tokens

    @final
    def __parse_interval_string_token(self, token: str, input_data: str) -> Tuple[int, float]:  # (quantity:int, multiplier:float)
        # Parse the token
        match_result = re.match(r'^([0-9]+)([a-z]+)\Z', token)
        if match_result is None:
            raise self._invalid_input_data_exc_factory.generate_invalid_input_data_exc(
                "The following token of the supplied time interval string is invalid: {}".format(repr(token)),
                input_data
            )

        quantity = int(match_result[1])  # The regex guarantees that this integer is not negative
        unit = match_result[2]

        # Get an appropriate unit specification
        try:
            multiplier, max_value = self.__class__.__FORMATTED_STRING_UNIT_SPECIFIERS[unit]
        except KeyError:
            raise self._invalid_input_data_exc_factory.generate_invalid_input_data_exc(
                "The unit in the following token of the supplied time interval string is invalid: {}".format(repr(token)),
                input_data
            )

        # Check if the quantity does not exceed its maximum allowed value (if there is any)
        if (max_value is not None) and (quantity > max_value):
            raise self._invalid_input_data_exc_factory.generate_invalid_input_data_exc(
                "The quantity in the following token of the supplied time interval string is exceeding its maximum allowed value ({}): {}".format(
                    max_value, repr(token)
                ),
                input_data
            )

        return quantity, multiplier

    @final
    def __convert_number_to_interval(self, input_data: Union[int, float]) -> float:
        return float(input_data)

    @final
    def __check_output_interval(self, output_interval: float, input_data: Any) -> float:
        if not math.isfinite(output_interval):
            raise self._invalid_input_data_exc_factory.generate_invalid_input_data_exc(
                "The resulting time interval float is not finite: {}".format(output_interval),
                input_data
            )

        if output_interval == (-0.0):
            output_interval = 0.0

        if output_interval < 0.0:
            raise self._invalid_input_data_exc_factory.generate_invalid_input_data_exc(
                "The resulting time interval float must not be negative: {}".format(output_interval),
                input_data
            )

        return output_interval
