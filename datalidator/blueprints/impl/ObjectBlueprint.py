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


from typing import final, Final, Any, Sequence, Type, Dict, Hashable, Union, Optional, Tuple
from datalidator.blueprints.BlueprintIface import BlueprintIface
from datalidator.blueprints.DefaultBlueprintWithStandardFeaturesImplBase import DefaultBlueprintWithStandardFeaturesImplBase
from datalidator.blueprints.extras.ObjectModel import ObjectModel
from datalidator.blueprints.extras.OptionalItemIface import OptionalItemIface
from datalidator.blueprints.impl.PredefinedDictionaryBlueprint import PredefinedDictionaryBlueprint
from datalidator.blueprints.exc.err.InvalidBlueprintConfigError import InvalidBlueprintConfigError
from datalidator.filters.FilterIface import FilterIface
from datalidator.validators.ValidatorIface import ValidatorIface


__all__ = "ObjectBlueprint",


class ObjectBlueprint(DefaultBlueprintWithStandardFeaturesImplBase[ObjectModel]):
    """
    INPUT:
    - any object convertible to 'dict' whose items conform to the initializer-provided 'object_model'

    OUTPUT:
    - an instance of the initializer-provided subclass of 'ObjectModel'

    NOTE: See this library's examples for usage information.
    """

    __slots__ = "__object_model", "__ignore_input_keys_which_are_not_in_model", "__predefined_dictionary_blueprint"

    def __init__(self,
                 object_model: Type[ObjectModel],
                 ignore_input_keys_which_are_not_in_model: bool = True,
                 filters: Sequence[FilterIface[ObjectModel]] = (),
                 validators: Sequence[ValidatorIface[ObjectModel]] = (),
                 tag: str = ""):
        DefaultBlueprintWithStandardFeaturesImplBase.__init__(self, filters, validators, tag)

        self.__object_model: Final[Type[ObjectModel]] = object_model
        self.__ignore_input_keys_which_are_not_in_model: Final[bool] = ignore_input_keys_which_are_not_in_model

        # The ObjectBlueprint is a wrapper class which delegates most of its functionality to a PredefinedDictionaryBlueprint.
        self.__predefined_dictionary_blueprint: Final[PredefinedDictionaryBlueprint] = PredefinedDictionaryBlueprint(
            dict_specification=self.__generate_dict_specification_from_object_model(object_model),
            ignore_unspecified_keys_in_input=ignore_input_keys_which_are_not_in_model,
            filters=(),  # Even if some default filters were added to the blueprint, they would not be used in this case.
            validators=(),  # Even if some default validators were added to the blueprint, they would not be used in this case.
            tag=self._tag
        )

    @final
    def __generate_dict_specification_from_object_model(self, object_model: Type[ObjectModel]) -> Dict[Hashable, Union[BlueprintIface[Any], OptionalItemIface[Any]]]:
        dict_specification = {}

        for property_name, property_value in object_model.__dict__.items():
            if property_name.startswith("_") or not isinstance(property_value, (BlueprintIface, OptionalItemIface)):
                continue

            dict_specification[property_name] = property_value

        if len(dict_specification) == 0:
            # It does not matter whether the object model has no blueprints in it to this class. The error is raised here
            #  to inform the user that the blueprints probably were not declared or were declared incorrectly.
            raise InvalidBlueprintConfigError(
                "The supplied object model (of type '{}') does not contain any blueprints!".format(object_model.__name__),
                self._tag
            )

        return dict_specification

    @final
    def get_object_model(self) -> Type[ObjectModel]:
        return self.__object_model

    @final
    def are_input_keys_which_are_not_in_model_ignored(self) -> bool:
        return self.__ignore_input_keys_which_are_not_in_model

    def _get_allowed_output_data_types(self) -> Optional[Tuple[Type, ...]]:
        # An instance of the initializer-provided *subclass of* ObjectModel is returned by this blueprint; therefore, the check would not pass
        return None

    def _parse(self, input_data: Any) -> ObjectModel:
        parsed_dict = self.__predefined_dictionary_blueprint.use(input_data)

        return self.__object_model(**parsed_dict)
