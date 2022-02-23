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
import re
from datalidator.blueprints.DefaultBlueprintWithStandardFeaturesImplBase import DefaultBlueprintWithStandardFeaturesImplBase


__all__ = "UnixFilesystemPathBlueprint",


class UnixFilesystemPathBlueprint(DefaultBlueprintWithStandardFeaturesImplBase[str]):
    """
    INPUT:
    - 'str' object considered a Unix filesystem path

    OUTPUT:
    - 'str' object considered a Unix filesystem path

    NOTE: This blueprint takes the input string, strips leading and trailing whitespace from it, reduces duplicate slash
     characters ('/') to one, and returns the resulting 'str' object. The input string must not be empty or contain a 
     NULL character ('\0').
    """

    __slots__ = ()

    def _get_allowed_output_data_types(self) -> Optional[Tuple[Type, ...]]:
        return str,

    def _parse(self, input_data: Any) -> str:
        return self._data_conversion_helper.convert_input_with_data_type_allowlist(
            self.__convert_string_to_fs_path_string, (str,), input_data
        )

    @final
    def __convert_string_to_fs_path_string(self, input_data: str) -> str:
        path = str(input_data)  # Possibly unsubclass the input string
        path = path.strip()  # In the vast majority of cases, having a whitespace at the beginning or end of a path is considered an error, even though it is technically possible

        if path == "":  # Empty strings are not valid filesystem paths
            raise self._invalid_input_data_exc_factory.generate_invalid_input_data_exc(
                "The supplied Unix filesystem path is empty!",
                input_data
            )

        if '\0' in path:
            raise self._invalid_input_data_exc_factory.generate_invalid_input_data_exc(
                "The supplied Unix filesystem path contains a '\\0' (NULL) character: {}".format(repr(path)),
                input_data
            )

        path = re.sub(r'/+', '/', path)  # Remove redundant slashes

        return path
