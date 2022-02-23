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
import uuid
from datalidator.blueprints.DefaultBlueprintWithStandardFeaturesImplBase import DefaultBlueprintWithStandardFeaturesImplBase


__all__ = "UUIDBlueprint",


class UUIDBlueprint(DefaultBlueprintWithStandardFeaturesImplBase[uuid.UUID]):
    """
    INPUT:
    - 'uuid.UUID' object
    - 'str' object containing a properly formatted UUID string: https://docs.python.org/3/library/uuid.html#uuid.UUID

    OUTPUT:
    - 'uuid.UUID' object
    """

    __slots__ = ()

    def _get_allowed_output_data_types(self) -> Optional[Tuple[Type, ...]]:
        return uuid.UUID,

    def _parse(self, input_data: Any) -> uuid.UUID:
        # This is a very similar procedure to the one in URLBlueprint.
        if isinstance(input_data, uuid.UUID):
            try:
                input_data = str(input_data)
            except Exception:
                raise self._invalid_input_data_exc_factory.generate_input_data_not_unsubclassable_exc(uuid.UUID, input_data)

        return self._data_conversion_helper.convert_input_with_data_type_allowlist(
            self.__convert_string_to_uuid_object, (str,), input_data
        )

    @final
    def __convert_string_to_uuid_object(self, input_data: str) -> uuid.UUID:
        try:
            return uuid.UUID(hex=input_data.strip().lower())
        except Exception:
            raise self._invalid_input_data_exc_factory.generate_input_data_not_convertible_exc((uuid.UUID,), input_data)
