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


from typing import final, Final, Any, Optional, Tuple, Type, TypeVar, Generic
import json
from datalidator.blueprints.BlueprintIface import BlueprintIface
from datalidator.blueprints.DefaultBlueprintWithStandardFeaturesImplBase import DefaultBlueprintWithStandardFeaturesImplBase


__all__ = "JSONBlueprint", "JSONBlueprint_T"
JSONBlueprint_T = TypeVar("JSONBlueprint_T")


class JSONBlueprint(DefaultBlueprintWithStandardFeaturesImplBase[JSONBlueprint_T], Generic[JSONBlueprint_T]):  # DP: Decorator
    """
    INPUT:
    - 'str' object containing a JSON document

    OUTPUT:
    - the value returned by the initializer-provided 'wrapped_blueprint'

    NOTE: The input JSON string is deserialized using json.loads(), the deserialized data is passed into the
     initializer-provided 'wrapped_blueprint' and its return value is returned.
    """

    __slots__ = "__wrapped_blueprint",

    def __init__(self, wrapped_blueprint: BlueprintIface[JSONBlueprint_T], tag: str = ""):
        # Passing filters and validators to this blueprint would not make sense, as this blueprint returns the data
        #  returned by the wrapped blueprint without any modification; therefore, the filters and validators within
        #  the wrapped blueprint can safely be used.
        # I am aware that by doing this, I am not respecting the abstraction a little, as I am not using one of the main
        #  features of the DefaultBlueprintImplBase class - the ability to use filters and validators. However, I still
        #  decided to do it like this, because I am using other important features of the aforementioned superclass
        #  (such its InvalidInputDataExcFactory and DataConversionHelper instances) and splitting them to a different
        #  subclass/mixin would be unnecessary for this one "special implementation".
        DefaultBlueprintWithStandardFeaturesImplBase.__init__(self, (), (), tag)

        self.__wrapped_blueprint: Final[BlueprintIface[JSONBlueprint_T]] = wrapped_blueprint

    @final
    def get_wrapped_blueprint(self) -> BlueprintIface[JSONBlueprint_T]:
        return self.__wrapped_blueprint

    def _get_allowed_output_data_types(self) -> Optional[Tuple[Type, ...]]:
        return None

    def _parse(self, input_data: Any) -> JSONBlueprint_T:
        return self._data_conversion_helper.convert_input_with_data_type_allowlist(
            self.__parse_str, (str,), input_data
        )

    @final
    def __parse_str(self, input_data: str) -> JSONBlueprint_T:
        try:
            deserialized_json = json.loads(input_data.strip())
        except Exception:
            raise self._invalid_input_data_exc_factory.generate_invalid_input_data_exc("The supplied string does not contain valid JSON data!", input_data)

        return self.__wrapped_blueprint.use(deserialized_json)
