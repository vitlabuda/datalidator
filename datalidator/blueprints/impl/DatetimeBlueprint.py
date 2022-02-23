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


from typing import final, Final, Any, Sequence, Tuple, Union, Optional, Type
import datetime
import time
import math
from datalidator.blueprints.DefaultBlueprintWithModeSupportImplBase import DefaultBlueprintWithModeSupportImplBase
from datalidator.blueprints.ParsingMode import ParsingMode
from datalidator.filters.FilterIface import FilterIface
from datalidator.validators.ValidatorIface import ValidatorIface


__all__ = "DatetimeBlueprint",


class DatetimeBlueprint(DefaultBlueprintWithModeSupportImplBase[datetime.datetime]):
    """
    INPUT in loose mode:
    - 'datetime.datetime' object
    - 'time.struct_time' object (the returned 'datetime.datetime' object always has the UTC timezone)
    - 'str' object containing a number (considered as Unix timestamp) or formatted either as ISO 8601 (see NOTE!) or as any of the additional strptime() formats passed to the initializer
    - 'int' or 'float' object (considered as Unix timestamp; the returned 'datetime.datetime' object always has the UTC timezone)
    - 'datetime.date' object
    - 'datetime.time' object

    INPUT in rational mode:
    - 'datetime.datetime' object
    - 'time.struct_time' object (the returned 'datetime.datetime' object always has the UTC timezone)
    - 'str' object containing a number (considered as Unix timestamp) or formatted either as ISO 8601 (see NOTE!) or as any of the additional strptime() formats passed to the initializer
    - 'int' or 'float' object (considered as Unix timestamp; the returned 'datetime.datetime' object always has the UTC timezone)

    INPUT in strict mode:
    - 'datetime.datetime' object
    - 'time.struct_time' object (the returned 'datetime.datetime' object always has the UTC timezone)
    - 'str' object formatted either as ISO 8601 (see NOTE!) or as any of the additional strptime() formats passed to the initializer

    OUTPUT:
    - 'datetime.datetime' object

    NOTE: Keep in mind that the initializer-provided 'additional_datetime_string_formats' might be locale-dependent!
    NOTE: By "ISO 8601 strings", strings that are accepted by datetime.fromisoformat() are meant; therefore, not all
     ISO 8601 formats can be parsed: https://docs.python.org/3/library/datetime.html#datetime.datetime.fromisoformat
    """

    __slots__ = "__additional_datetime_string_formats",

    # I am aware that the parsing modes scheme does not fit this blueprint that well (e.g. converting Unix time
    #  [= a plain number] to datetime could be considered irrational in some cases). If it causes problems, I might
    #  change this behaviour in the future.

    __DATE_TO_DATETIME_TIME_TO_COMBINE: Final[datetime.time] = datetime.time(hour=0, minute=0, second=0)
    __TIME_TO_DATETIME_DATE_TO_COMBINE: Final[datetime.date] = datetime.date(year=1900, month=1, day=1)

    def __init__(self,
                 additional_datetime_string_formats: Sequence[str] = (),  # The format specifiers might be locale-dependent!
                 filters: Sequence[FilterIface[datetime.datetime]] = (),
                 validators: Sequence[ValidatorIface[datetime.datetime]] = (),
                 parsing_mode: ParsingMode = DefaultBlueprintWithModeSupportImplBase._DEFAULT_PARSING_MODE,
                 tag: str = ""):
        DefaultBlueprintWithModeSupportImplBase.__init__(self, filters, validators, parsing_mode, tag)

        # Both input datetime strings and datetime string formats are stripped of leading and trailing whitespace.
        self.__additional_datetime_string_formats: Final[Tuple[str, ...]] = tuple(format_string.strip() for format_string in additional_datetime_string_formats)

    @final
    def get_additional_datetime_string_formats(self) -> Sequence[str]:
        return self.__additional_datetime_string_formats  # An *immutable* sequence (tuple) is returned

    def _get_allowed_output_data_types(self) -> Optional[Tuple[Type, ...]]:
        return datetime.datetime,

    # Can convert: datetime.datetime, time.struct_time, formatted datetime str, Unix timestamp as int/float/str, datetime.date, datetime.time
    def _parse_in_loose_mode(self, input_data: Any) -> datetime.datetime:
        return self._data_conversion_helper.convert_input_using_per_data_type_converter_functions(
            (
                ((datetime.datetime,), self.__convert_datetime_to_datetime),  # datetime.datetime is a subclass of datetime.date, so it must be checked prior to datetime.date!
                ((time.struct_time,), self.__convert_struct_time_to_datetime),
                ((str,), self.__convert_any_valid_str_to_datetime),  # The string can either contain a Unix timestamp, or a formatted datetime.
                ((int, float), self.__convert_numeric_unix_timestamp_to_datetime),
                ((datetime.date,), self.__convert_date_to_datetime),
                ((datetime.time,), self.__convert_time_to_datetime)
            ),
            input_data
        )

    # Can convert: datetime.datetime, time.struct_time, formatted datetime str, Unix timestamp as int/float/str
    def _parse_in_rational_mode(self, input_data: Any) -> datetime.datetime:
        return self._data_conversion_helper.convert_input_using_per_data_type_converter_functions(
            (
                ((datetime.datetime,), self.__convert_datetime_to_datetime),
                ((time.struct_time,), self.__convert_struct_time_to_datetime),
                ((str,), self.__convert_any_valid_str_to_datetime),  # The string can either contain a Unix timestamp, or a formatted datetime.
                ((int, float), self.__convert_numeric_unix_timestamp_to_datetime)
            ),
            input_data
        )

    # Can convert: datetime.datetime, time.struct_time, formatted datetime str
    def _parse_in_strict_mode(self, input_data: Any) -> datetime.datetime:
        return self._data_conversion_helper.convert_input_using_per_data_type_converter_functions(
            (
                ((datetime.datetime,), self.__convert_datetime_to_datetime),
                ((time.struct_time,), self.__convert_struct_time_to_datetime),
                ((str,), self.__convert_formatted_str_to_datetime)
            ),
            input_data
        )

    @final
    def __convert_datetime_to_datetime(self, input_data: datetime.datetime) -> datetime.datetime:
        # One of this library's basic principles is that the built-in blueprints only return data that are instances of
        #  their output data type and not of the type's subclasses! This serves as a protection against subclasses that
        #  break Liskov substitution principle - remember, the blueprints should be able to deal with any untrusted
        #  input data!
        new_datetime = input_data.replace()  # Give the potential subclass a chance to return an instance of the base class
        if new_datetime.__class__ is datetime.datetime:
            return new_datetime

        raise self._invalid_input_data_exc_factory.generate_input_data_not_unsubclassable_exc(datetime.datetime, input_data)

    @final
    def __convert_struct_time_to_datetime(self, input_data: time.struct_time) -> datetime.datetime:
        try:
            unix_timestamp = time.mktime(input_data)

            return datetime.datetime.fromtimestamp(unix_timestamp, tz=datetime.timezone.utc)
        except Exception:  # Can be OverflowError, ...
            raise self._invalid_input_data_exc_factory.generate_input_data_not_convertible_exc((datetime.datetime,), input_data)

    @final
    def __convert_any_valid_str_to_datetime(self, input_data: str) -> datetime.datetime:
        try:
            numeric_unix_timestamp = float(input_data)
        except Exception:  # noqa; Can be ValueError, ...
            pass
        else:
            # If the input string can be converted to a float, it is considered a Unix timestamp.
            return self.__convert_numeric_unix_timestamp_to_datetime(numeric_unix_timestamp)

        # Otherwise, treat the input string as a formatted datetime string.
        return self.__convert_formatted_str_to_datetime(input_data)

    @final
    def __convert_formatted_str_to_datetime(self, input_data: str) -> datetime.datetime:
        # datetime.datetime methods do not automatically strip whitespace from input strings (as float() or int() does)
        stripped_input_string = input_data.strip()

        try:
            return datetime.datetime.fromisoformat(stripped_input_string)
        except Exception:  # noqa; Can be ValueError, ...
            pass

        # If the input string is not ISO-formatted, try parsing it using the additional datetime string formats...
        for additional_string_format in self.__additional_datetime_string_formats:
            try:
                # Both input datetime strings and datetime string formats are stripped of leading and trailing whitespace.
                return datetime.datetime.strptime(stripped_input_string, additional_string_format)
            except Exception:  # noqa; Can be ValueError, ...
                pass

        raise self._invalid_input_data_exc_factory.generate_input_data_not_convertible_exc((datetime.datetime,), input_data)

    @final
    def __convert_numeric_unix_timestamp_to_datetime(self, input_data: Union[int, float]) -> datetime.datetime:
        if not math.isfinite(input_data):  # See code comments in FloatBlueprint for more information
            raise self._invalid_input_data_exc_factory.generate_input_data_not_convertible_exc((datetime.datetime,), input_data)

        if input_data == (-0.0):  # See code comments in FloatBlueprint for more information
            input_data = 0.0

        try:
            return datetime.datetime.fromtimestamp(input_data, tz=datetime.timezone.utc)
        except Exception:
            raise self._invalid_input_data_exc_factory.generate_input_data_not_convertible_exc((datetime.datetime,), input_data)

    @final
    def __convert_date_to_datetime(self, input_data: datetime.date) -> datetime.datetime:
        try:
            return datetime.datetime.combine(input_data, self.__class__.__DATE_TO_DATETIME_TIME_TO_COMBINE)
        except Exception:
            raise self._invalid_input_data_exc_factory.generate_input_data_not_convertible_exc((datetime.datetime,), input_data)

    @final
    def __convert_time_to_datetime(self, input_data: datetime.time) -> datetime.datetime:
        try:
            return datetime.datetime.combine(self.__class__.__TIME_TO_DATETIME_DATE_TO_COMBINE, input_data)
        except Exception:
            raise self._invalid_input_data_exc_factory.generate_input_data_not_convertible_exc((datetime.datetime,), input_data)
