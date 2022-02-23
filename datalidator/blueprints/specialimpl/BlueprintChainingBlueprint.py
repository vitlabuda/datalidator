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


from typing import final, Final, Any, Sequence, Tuple
from datalidator.blueprints.BlueprintIface import BlueprintIface
from datalidator.blueprints.DefaultBlueprintImplBase import DefaultBlueprintImplBase
from datalidator.blueprints.exc.err.InvalidBlueprintConfigError import InvalidBlueprintConfigError


__all__ = "BlueprintChainingBlueprint",


class BlueprintChainingBlueprint(DefaultBlueprintImplBase[Any]):
    """
    The input data are passed into the first blueprint of the initializer-provided 'blueprint_chain', its output is
     passed into the second blueprint in the chain and so on. The output of the last blueprint in the chain is returned.

    The blueprint chain must contain at least one blueprint.
    """

    __slots__ = "__blueprint_chain",

    def __init__(self, blueprint_chain: Sequence[BlueprintIface[Any]], tag: str = ""):
        DefaultBlueprintImplBase.__init__(self, tag)

        self.__blueprint_chain: Final[Tuple[BlueprintIface[Any], ...]] = tuple(blueprint_chain)

        if len(self.__blueprint_chain) == 0:
            raise InvalidBlueprintConfigError("The blueprint chain is empty!", self._tag)

    @final
    def get_blueprint_chain(self) -> Sequence[BlueprintIface[Any]]:
        return self.__blueprint_chain  # An *immutable* sequence (tuple) is returned

    def _use(self, input_data: Any) -> Any:
        for blueprint in self.__blueprint_chain:
            input_data = blueprint.use(input_data)

        return input_data
