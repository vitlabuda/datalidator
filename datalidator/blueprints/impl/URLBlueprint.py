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


from typing import final, Any, Optional, Tuple, Type
import urllib.parse
from datalidator.blueprints.DefaultBlueprintWithStandardFeaturesImplBase import DefaultBlueprintWithStandardFeaturesImplBase


__all__ = "URLBlueprint",


class URLBlueprint(DefaultBlueprintWithStandardFeaturesImplBase[urllib.parse.ParseResult]):
    """
    INPUT:
    - 'urllib.parse.ParseResult' object (not 'urllib.parse.ParseResultBytes'!)
    - 'str' object containing an URL

    OUTPUT:
    - 'urllib.parse.ParseResult' object (as returned by urllib.parse.urlparse())
    """

    __slots__ = ()

    def _get_allowed_output_data_types(self) -> Optional[Tuple[Type, ...]]:
        return urllib.parse.ParseResult,

    def _parse(self, input_data: Any) -> urllib.parse.ParseResult:
        # The urllib.parse.urlparse() function does not accept urllib.parse.ParseResult objects.
        if isinstance(input_data, urllib.parse.ParseResult):
            # The parsed URL is "unparsed" back to string and then later parsed back to URL - this way, it is guaranteed
            #  that the returned object is not a subclass of ParseResult (e.g. ParseResultBytes). This behaviour is
            #  similar to passing a string to str()).
            try:
                input_data = urllib.parse.urlunparse(input_data)
            except Exception:
                raise self._invalid_input_data_exc_factory.generate_input_data_not_unsubclassable_exc(urllib.parse.ParseResult, input_data)

        # If a bytes() object is passed to the urllib.parse.urlparse() function, a urllib.parse.ParseResultBytes object
        #  is returned (and vice versa - when a ParseResultBytes object is unparsed, a bytes() object is returned).
        #  Even though the returned object is a subclass of urllib.parse.ParseResult, this behaviour is not wanted in
        #  the vast majority of cases, so it is disabled here.
        parse_result = self._data_conversion_helper.convert_input_with_data_type_allowlist(
            self.__convert_string_to_parse_result_object, (str,), input_data
        )

        # May raise InputDataNotConvertibleExc
        self.__check_data_types_of_parse_result_fields(parse_result, input_data)

        return parse_result

    @final
    def __convert_string_to_parse_result_object(self, input_data: str) -> urllib.parse.ParseResult:
        try:
            return urllib.parse.urlparse(url=input_data.strip(), scheme="", allow_fragments=True)
        except Exception:
            raise self._invalid_input_data_exc_factory.generate_input_data_not_convertible_exc((urllib.parse.ParseResult,), input_data)

    @final
    def __check_data_types_of_parse_result_fields(self, parse_result: urllib.parse.ParseResult, input_data: Any) -> None:
        # ParseResult is a 6-tuple
        for field in parse_result:
            if field.__class__ is not str:
                raise self._invalid_input_data_exc_factory.generate_input_data_not_convertible_exc((urllib.parse.ParseResult,), input_data)
