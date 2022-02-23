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
from datalidator.blueprints.DefaultBlueprintWithModeSupportImplBase import DefaultBlueprintWithModeSupportImplBase
from datalidator.blueprints.ParsingMode import ParsingMode
from datalidator.filters.FilterIface import FilterIface
from datalidator.validators.ValidatorIface import ValidatorIface


__all__ = "BytesBlueprint",


class BytesBlueprint(DefaultBlueprintWithModeSupportImplBase[bytes]):
    """
    INPUT in loose mode:
    - any object except 'int' and 'float'

    INPUT in rational mode:
    - 'bytes' or 'bytearray' object
    - 'str' object

    INPUT in strict mode:
    - 'bytes' or 'bytearray' object

    OUTPUT:
    - 'bytes' object
    """

    __slots__ = "__string_encoding",

    # Passing an int to the bytes() function is always forbidden because it would introduce a very easily exploitable
    #  DoS vulnerability to the library (when an integer is passed to the bytes() function, a bytes object with
    #  n zero-initialized bytes is created - a huge enough integer can cause memory depletion).
    __LOOSE_MODE_DATA_TYPE_BLOCKLIST: Final[Tuple[Type, ...]] = (int, float)
    __RATIONAL_MODE_DATA_TYPE_ALLOWLIST: Final[Tuple[Type, ...]] = (bytes, bytearray, str)
    __STRICT_MODE_DATA_TYPE_ALLOWLIST: Final[Tuple[Type, ...]] = (bytes, bytearray)

    _DEFAULT_STRING_ENCODING: Final[str] = "utf-8"

    def __init__(self,
                 string_encoding: str = _DEFAULT_STRING_ENCODING,
                 filters: Sequence[FilterIface[bytes]] = (),
                 validators: Sequence[ValidatorIface[bytes]] = (),
                 parsing_mode: ParsingMode = DefaultBlueprintWithModeSupportImplBase._DEFAULT_PARSING_MODE,
                 tag: str = ""):
        DefaultBlueprintWithModeSupportImplBase.__init__(self, filters, validators, parsing_mode, tag)

        self.__string_encoding: Final[str] = string_encoding

    @classmethod
    @final
    def get_default_string_encoding(cls) -> str:
        return cls._DEFAULT_STRING_ENCODING

    @final
    def get_string_encoding(self) -> str:
        return self.__string_encoding

    def _get_allowed_output_data_types(self) -> Optional[Tuple[Type, ...]]:
        return bytes,

    def _parse_in_loose_mode(self, input_data: Any) -> bytes:
        return self._data_conversion_helper.convert_input_with_data_type_blocklist(
            self.__convert_input_data_to_bytes, self.__class__.__LOOSE_MODE_DATA_TYPE_BLOCKLIST, input_data
        )

    def _parse_in_rational_mode(self, input_data: Any) -> bytes:
        return self._data_conversion_helper.convert_input_with_data_type_allowlist(
            self.__convert_input_data_to_bytes, self.__class__.__RATIONAL_MODE_DATA_TYPE_ALLOWLIST, input_data
        )

    def _parse_in_strict_mode(self, input_data: Any) -> bytes:
        return self._data_conversion_helper.convert_input_with_data_type_allowlist(
            self.__convert_input_data_to_bytes, self.__class__.__STRICT_MODE_DATA_TYPE_ALLOWLIST, input_data
        )

    @final
    def __convert_input_data_to_bytes(self, input_data: Any) -> bytes:
        if isinstance(input_data, str):
            try:
                return input_data.encode(self.__string_encoding, "strict")
            except Exception:  # Can be UnicodeError, ...
                raise self._invalid_input_data_exc_factory.generate_input_data_not_convertible_exc((bytes,), input_data)

        try:
            return bytes(input_data)
        except Exception:  # Can be ValueError, ...
            raise self._invalid_input_data_exc_factory.generate_input_data_not_convertible_exc((bytes,), input_data)
