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


from typing import final, Final, Dict, Any, Hashable, Sequence, Union, Optional, Tuple, Type
from datalidator.blueprints.BlueprintIface import BlueprintIface
from datalidator.blueprints.DefaultBlueprintWithStandardFeaturesImplBase import DefaultBlueprintWithStandardFeaturesImplBase
from datalidator.blueprints.extras.OptionalItemIface import OptionalItemIface
from datalidator.filters.FilterIface import FilterIface
from datalidator.validators.ValidatorIface import ValidatorIface


__all__ = "PredefinedDictionaryBlueprint",


class PredefinedDictionaryBlueprint(DefaultBlueprintWithStandardFeaturesImplBase[Dict[Hashable, Any]]):
    """
    INPUT:
    - any object convertible to 'dict' whose items conform to the initializer-provided 'dict_specification'

    OUTPUT:
    - 'dict' object with heterogeneous items that were run through blueprints in the initializer-provided 'dict_specification'

    NOTE: See this library's examples for usage information.
    """

    __slots__ = "__dict_specification", "__ignore_unspecified_keys_in_input"

    def __init__(self,
                 dict_specification: Dict[Hashable, Union[BlueprintIface[Any], OptionalItemIface[Any]]],
                 ignore_unspecified_keys_in_input: bool = True,
                 filters: Sequence[FilterIface[Dict[Hashable, Any]]] = (),
                 validators: Sequence[ValidatorIface[Dict[Hashable, Any]]] = (),
                 tag: str = ""):
        DefaultBlueprintWithStandardFeaturesImplBase.__init__(self, filters, validators, tag)

        self.__dict_specification: Final[Dict[Hashable, Union[BlueprintIface[Any], OptionalItemIface[Any]]]] = dict_specification.copy()
        self.__ignore_unspecified_keys_in_input: Final[bool] = ignore_unspecified_keys_in_input

    @final
    def get_dict_specification(self) -> Dict[Hashable, Union[BlueprintIface[Any], OptionalItemIface[Any]]]:
        return self.__dict_specification.copy()

    @final
    def are_unspecified_keys_in_input_ignored(self) -> bool:
        return self.__ignore_unspecified_keys_in_input

    def _get_allowed_output_data_types(self) -> Optional[Tuple[Type, ...]]:
        return dict,

    def _parse(self, input_data: Any) -> Dict[Hashable, Any]:
        dict_from_input_data = self.__convert_input_data_to_dict(input_data)

        # The keys which are present in the dict specification are removed from the input dictionary, if they are found there!
        # This behaviour is made use of when checking whether there are unspecified keys in the input dictionary.
        parsed_data = self.__handle_input_data_according_to_specification(dict_from_input_data, input_data)

        # Check if there are unspecified keys in the input dictionary, if required:
        if not self.__ignore_unspecified_keys_in_input and len(dict_from_input_data) != 0:
            raise self._invalid_input_data_exc_factory.generate_invalid_input_data_exc(
                "There are keys in the input dictionary which are not specified in the dictionary specification: {}".format(
                    self._invalid_input_data_exc_factory.__class__.get_single_string_representation_of_values(dict_from_input_data.keys())
                ),
                input_data
            )

        return parsed_data

    @final
    def __convert_input_data_to_dict(self, input_data: Any) -> Dict[Hashable, Any]:
        try:
            return dict(input_data)  # This newly created dictionary is mutated later!
        except Exception:
            raise self._invalid_input_data_exc_factory.generate_input_data_not_convertible_exc((dict,), input_data)

    @final
    def __handle_input_data_according_to_specification(self, dict_from_input_data: Dict[Hashable, Any], input_data: Any) -> Dict[Hashable, Any]:
        output_dict = {}

        for key, specification in self.__dict_specification.items():
            if isinstance(specification, OptionalItemIface):
                output_value = self.__handle_optional_item_from_input_data(key, specification, dict_from_input_data)
            else:
                output_value = self.__handle_mandatory_item_from_input_data(key, specification, dict_from_input_data, input_data)

            output_dict[key] = output_value

        return output_dict

    @final
    def __handle_optional_item_from_input_data(self, key: Hashable, specification: OptionalItemIface, dict_from_input_data: Dict[Hashable, Any]) -> Any:
        try:
            raw_input_value = dict_from_input_data.pop(key)  # The key is removed from the input dictionary, if it is found there.
        except KeyError:
            return specification.get_default_value()
        else:
            return specification.get_wrapped_blueprint().use(raw_input_value)

    @final
    def __handle_mandatory_item_from_input_data(self, key: Hashable, specification: BlueprintIface[Any], dict_from_input_data: Dict[Hashable, Any], input_data: Any) -> Any:
        try:
            raw_input_value = dict_from_input_data.pop(key)  # The key is removed from the input dictionary, if it is found there.
        except KeyError:
            raise self._invalid_input_data_exc_factory.generate_invalid_input_data_exc(
                "The input dictionary does not contain the following mandatory key: {}".format(repr(key)),
                input_data
            )
        else:
            return specification.use(raw_input_value)
