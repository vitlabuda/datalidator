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


from typing import final, Final, Any, List, Sequence, Tuple, Type, Optional, Generic, TypeVar
import collections.abc
from datalidator.blueprints.BlueprintIface import BlueprintIface
from datalidator.blueprints.DefaultBlueprintWithModeSupportImplBase import DefaultBlueprintWithModeSupportImplBase
from datalidator.blueprints.ParsingMode import ParsingMode
from datalidator.filters.FilterIface import FilterIface
from datalidator.validators.ValidatorIface import ValidatorIface


__all__ = "ListBlueprint", "ListBlueprint_T"
ListBlueprint_T = TypeVar("ListBlueprint_T")


class ListBlueprint(DefaultBlueprintWithModeSupportImplBase[List[ListBlueprint_T]], Generic[ListBlueprint_T]):
    """
    INPUT in loose mode:
    - any object that can be passed to list()

    INPUT in rational mode:
    - any object that can be passed to list() except mappings (e.g. 'dict'), 'str', 'bytes' and 'bytearray'

    INPUT in strict mode:
    - 'list' object
    - 'tuple' object
    - 'set' object
    - 'frozenset' object

    OUTPUT:
    - 'list' object whose items were run through the initializer-provided 'item_blueprint' object

    NOTE: This blueprint takes the input data, converts them to a 'list' object, runs its items through the
     'item_blueprint' object that has been passed to this object's initializer before, and returns the resulting
     'list' object.
    """

    __slots__ = "__item_blueprint",

    # Those input data types are disallowed in rational mode because converting them to list might produce "irrational"
    #  results (e.g. a mapping passed to this blueprint would produce a list of its keys - most people would not expect
    #  such behaviour)
    __RATIONAL_MODE_DATA_TYPE_BLOCKLIST: Final[Tuple[Type, ...]] = (collections.abc.Mapping, str, bytes, bytearray)
    __STRICT_MODE_DATA_TYPE_ALLOWLIST: Final[Tuple[Type, ...]] = (list, tuple, set, frozenset)

    def __init__(self,
                 item_blueprint: BlueprintIface[ListBlueprint_T],
                 filters: Sequence[FilterIface[List[ListBlueprint_T]]] = (),
                 validators: Sequence[ValidatorIface[List[ListBlueprint_T]]] = (),
                 parsing_mode: ParsingMode = DefaultBlueprintWithModeSupportImplBase._DEFAULT_PARSING_MODE,
                 tag: str = ""):
        DefaultBlueprintWithModeSupportImplBase.__init__(self, filters, validators, parsing_mode, tag)

        self.__item_blueprint: Final[BlueprintIface[ListBlueprint_T]] = item_blueprint

    @final
    def get_item_blueprint(self) -> BlueprintIface[ListBlueprint_T]:
        return self.__item_blueprint

    def _get_allowed_output_data_types(self) -> Optional[Tuple[Type, ...]]:
        return list,

    def _parse_in_loose_mode(self, input_data: Any) -> List[ListBlueprint_T]:
        return self.__convert_input_data_to_list(input_data)

    def _parse_in_rational_mode(self, input_data: Any) -> List[ListBlueprint_T]:
        return self._data_conversion_helper.convert_input_with_data_type_blocklist(
            self.__convert_input_data_to_list, self.__class__.__RATIONAL_MODE_DATA_TYPE_BLOCKLIST, input_data
        )

    def _parse_in_strict_mode(self, input_data: Any) -> List[ListBlueprint_T]:
        return self._data_conversion_helper.convert_input_with_data_type_allowlist(
            self.__convert_input_data_to_list, self.__class__.__STRICT_MODE_DATA_TYPE_ALLOWLIST, input_data
        )

    @final
    def __convert_input_data_to_list(self, input_data: Any) -> List[ListBlueprint_T]:
        # Convert the input data to list before iterating through it (to be able to reasonably catch exceptions related
        #  to invalid input data)
        try:
            list_from_input_data = list(input_data)
        except Exception:
            raise self._invalid_input_data_exc_factory.generate_input_data_not_convertible_exc((list,), input_data)

        # Apply the blueprint passed to the initializer to each item of the list -> recursive behaviour
        return [self.__item_blueprint.use(item) for item in list_from_input_data]
