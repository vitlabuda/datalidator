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


from typing import final, Final, Any, TypeVar, Generic
from datalidator.exc.DatalidatorExc import DatalidatorExc
from datalidator.blueprints.BlueprintIface import BlueprintIface
from datalidator.blueprints.DefaultBlueprintImplBase import DefaultBlueprintImplBase


__all__ = "ExceptionHandlingBlueprint", "ExceptionHandlingBlueprint_T"
ExceptionHandlingBlueprint_T = TypeVar("ExceptionHandlingBlueprint_T")


class ExceptionHandlingBlueprint(DefaultBlueprintImplBase[ExceptionHandlingBlueprint_T], Generic[ExceptionHandlingBlueprint_T]):  # DP: Decorator
    """
    If the initializer-provided 'wrapped_blueprint' raises 'DatalidatorExc' while dealing with the input data, the
     initializer-provided 'default_value' is returned.
    """

    __slots__ = "__wrapped_blueprint", "__default_value"

    def __init__(self, wrapped_blueprint: BlueprintIface[ExceptionHandlingBlueprint_T], default_value: ExceptionHandlingBlueprint_T, tag: str = ""):
        DefaultBlueprintImplBase.__init__(self, tag)

        self.__wrapped_blueprint: Final[BlueprintIface[ExceptionHandlingBlueprint_T]] = wrapped_blueprint
        self.__default_value: Final[ExceptionHandlingBlueprint_T] = default_value

    @final
    def get_wrapped_blueprint(self) -> BlueprintIface[ExceptionHandlingBlueprint_T]:
        return self.__wrapped_blueprint

    @final
    def get_default_value(self) -> ExceptionHandlingBlueprint_T:
        return self.__default_value

    def _use(self, input_data: Any) -> ExceptionHandlingBlueprint_T:
        try:
            return self.__wrapped_blueprint.use(input_data)
        except DatalidatorExc:
            return self.__default_value
