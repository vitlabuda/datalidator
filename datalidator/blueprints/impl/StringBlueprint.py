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


from typing import final, Final, Any, Sequence, Union, Optional, Tuple, Type
import datetime
import ipaddress
import urllib.parse
import uuid
from datalidator.exc.err.ThisShouldNeverHappenError import ThisShouldNeverHappenError
from datalidator.blueprints.DefaultBlueprintWithModeSupportImplBase import DefaultBlueprintWithModeSupportImplBase
from datalidator.blueprints.ParsingMode import ParsingMode
from datalidator.filters.FilterIface import FilterIface
from datalidator.validators.ValidatorIface import ValidatorIface


__all__ = "StringBlueprint",


class StringBlueprint(DefaultBlueprintWithModeSupportImplBase[str]):
    """
    INPUT in loose mode:
    - any object that can be passed to str()
    * there is no special handling for some data types as in rational mode (e.g. datetime.datetime, urllib.parse.ParseResult)

    INPUT in rational mode:
    - 'None'
    - 'str' object
    - 'bool' object
    - 'int' object
    - 'float' object
    - 'complex' object
    - 'ipaddress.IPv4Address' object
    - 'ipaddress.IPv6Address' object
    - 'ipaddress.IPv4Network' object
    - 'ipaddress.IPv6Network' object
    - 'uuid.UUID' object
    - 'bytes' or 'bytearray' object whose contents are encoded using the initializer-provided 'bytes_encoding'
    - 'urllib.parse.ParseResult' object (not 'urllib.parse.ParseResultBytes'!)
    - 'datetime.datetime' object (converted to a string formatted either as ISO 8601 or as the initializer-provided 'datetime_string_format' using strftime())
    - 'datetime.date' object (converted to a string formatted either as ISO 8601 or as the initializer-provided 'date_string_format' using strftime())
    - 'datetime.time' object (converted to a string formatted either as ISO 8601 or as the initializer-provided 'time_string_format' using strftime())

    INPUT in strict mode:
    - 'str' object

    OUTPUT:
    - 'str' object
    """

    __slots__ = "__bytes_encoding", "__datetime_string_format", "__date_string_format", "__time_string_format"

    _DEFAULT_BYTES_ENCODING: Final[str] = "utf-8"

    def __init__(self,
                 bytes_encoding: str = _DEFAULT_BYTES_ENCODING,
                 datetime_string_format: Optional[str] = None,  # If None, the ISO 8601 format will is used
                 date_string_format: Optional[str] = None,  # If None, the ISO 8601 format will is used
                 time_string_format: Optional[str] = None,  # If None, the ISO 8601 format will is used
                 filters: Sequence[FilterIface[str]] = (),
                 validators: Sequence[ValidatorIface[str]] = (),
                 parsing_mode: ParsingMode = DefaultBlueprintWithModeSupportImplBase._DEFAULT_PARSING_MODE,
                 tag: str = ""):
        DefaultBlueprintWithModeSupportImplBase.__init__(self, filters, validators, parsing_mode, tag)

        self.__bytes_encoding: Final[str] = bytes_encoding
        self.__datetime_string_format: Final[Optional[str]] = datetime_string_format
        self.__date_string_format: Final[Optional[str]] = date_string_format
        self.__time_string_format: Final[Optional[str]] = time_string_format

    @classmethod
    @final
    def get_default_bytes_encoding(cls) -> str:
        return cls._DEFAULT_BYTES_ENCODING

    @final
    def get_bytes_encoding(self) -> str:
        return self.__bytes_encoding

    @final
    def get_datetime_string_format(self) -> Optional[str]:
        return self.__datetime_string_format

    @final
    def get_date_string_format(self) -> Optional[str]:
        return self.__date_string_format

    @final
    def get_time_string_format(self) -> Optional[str]:
        return self.__time_string_format

    def _get_allowed_output_data_types(self) -> Optional[Tuple[Type, ...]]:
        return str,

    def _parse_in_loose_mode(self, input_data: Any) -> str:
        return self.__perform_generic_conversion_to_str(input_data)

    def _parse_in_rational_mode(self, input_data: Any) -> str:
        return self._data_conversion_helper.convert_input_using_per_data_type_converter_functions(
            (
                ((urllib.parse.ParseResult,), self.__convert_parsed_url_to_str),
                ((datetime.datetime, datetime.date, datetime.time), self.__convert_datetime_like_object_to_str),
                ((bytes, bytearray), self.__convert_bytes_to_str),
                ((type(None), str, bool, int, float, complex, ipaddress.IPv4Address, ipaddress.IPv6Address, ipaddress.IPv4Network, ipaddress.IPv6Network, uuid.UUID), self.__perform_generic_conversion_to_str),
            ),
            input_data
        )

    def _parse_in_strict_mode(self, input_data: Any) -> str:
        return self._data_conversion_helper.convert_input_with_data_type_allowlist(
            self.__perform_generic_conversion_to_str, (str,), input_data
        )

    @final
    def __perform_generic_conversion_to_str(self, input_data: Any) -> str:
        try:
            return str(input_data)  # /Any/ object can be turned into a string
        except Exception:
            raise self._invalid_input_data_exc_factory.generate_input_data_not_convertible_exc((str,), input_data)

    @final
    def __convert_bytes_to_str(self, input_data: Union[bytes, bytearray]) -> str:
        try:
            return input_data.decode(self.__bytes_encoding, "strict")
        except Exception:
            raise self._invalid_input_data_exc_factory.generate_input_data_not_convertible_exc((str,), input_data)

    @final
    def __convert_datetime_like_object_to_str(self, input_data: Union[datetime.datetime, datetime.date, datetime.time]) -> str:
        # "if-elif cascade" must be used due to the need of using isinstance() (a simple dict() mapping or similar methods would not be able to detect subclasses)
        if isinstance(input_data, datetime.datetime):  # datetime.datetime is a subclass of datetime.date, so it must be checked prior to datetime.date!
            string_format = self.__datetime_string_format
        elif isinstance(input_data, datetime.date):
            string_format = self.__date_string_format
        elif isinstance(input_data, datetime.time):
            string_format = self.__time_string_format
        else:
            # This should never happen, as the convert_input_using_per_data_type_converter_functions() function is used to call this method.
            raise ThisShouldNeverHappenError(
                "The data type of the '{}' method's input data must be one of these: {}, not '{}'!".format(
                    self.__convert_datetime_like_object_to_str.__name__,
                    self._invalid_input_data_exc_factory.__class__.get_single_string_representation_of_class_names((datetime.datetime, datetime.date, datetime.time)),
                    self._invalid_input_data_exc_factory.__class__.get_class_name(input_data)
                ),
                self._tag
            )

        try:
            if string_format is None:
                return input_data.isoformat()

            return input_data.strftime(string_format)

        except Exception:
            raise self._invalid_input_data_exc_factory.generate_input_data_not_convertible_exc((str,), input_data)

    @final
    def __convert_parsed_url_to_str(self, input_data: urllib.parse.ParseResult) -> str:
        try:
            output_string = urllib.parse.urlunparse(input_data)
        except Exception:
            raise self._invalid_input_data_exc_factory.generate_input_data_not_convertible_exc((str,), input_data)

        if isinstance(output_string, str):
            return str(output_string)  # Possibly unsubclass the output string

        # urllib.parse.ParseResultBytes is a subclass of ParseResult, and when passed to urlunparse(), it returns a bytes object!
        raise self._invalid_input_data_exc_factory.generate_input_data_not_convertible_exc((str,), input_data)
