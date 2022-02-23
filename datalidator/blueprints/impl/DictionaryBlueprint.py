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


from typing import final, Final, Dict, Generic, Any, Sequence, Hashable, Optional, Tuple, Type, TypeVar
from datalidator.blueprints.BlueprintIface import BlueprintIface
from datalidator.blueprints.DefaultBlueprintWithStandardFeaturesImplBase import DefaultBlueprintWithStandardFeaturesImplBase
from datalidator.filters.FilterIface import FilterIface
from datalidator.validators.ValidatorIface import ValidatorIface


__all__ = "DictionaryBlueprint", "DictionaryBlueprint_KT", "DictionaryBlueprint_VT"
DictionaryBlueprint_KT = TypeVar("DictionaryBlueprint_KT")
DictionaryBlueprint_VT = TypeVar("DictionaryBlueprint_VT")


class DictionaryBlueprint(DefaultBlueprintWithStandardFeaturesImplBase[Dict[DictionaryBlueprint_KT, DictionaryBlueprint_VT]], Generic[DictionaryBlueprint_KT, DictionaryBlueprint_VT]):
    """
    INPUT:
    - any object convertible to 'dict'

    OUTPUT:
    - 'dict' object containing keys and values ran through the initializer-provided 'key_blueprint' and 'value_blueprint' objects

    NOTE: This blueprint takes the input data, converts them to a 'dict' object, runs its keys and values through
     the 'key_blueprint' and 'value_blueprint' objects that have been passed to this object's initializer before,
     and returns the resulting 'dict' object.
    """

    __slots__ = "__key_blueprint", "__value_blueprint"

    # Dictionary is a specific-enough type, so there is very little chance that any input data would cause an
    #  "irrational" output. Therefore, there is no need for parsing modes support.

    def __init__(self,
                 key_blueprint: BlueprintIface[DictionaryBlueprint_KT],
                 value_blueprint: BlueprintIface[DictionaryBlueprint_VT],
                 filters: Sequence[FilterIface[Dict[DictionaryBlueprint_KT, DictionaryBlueprint_VT]]] = (),
                 validators: Sequence[ValidatorIface[Dict[DictionaryBlueprint_KT, DictionaryBlueprint_VT]]] = (),
                 tag: str = ""):
        DefaultBlueprintWithStandardFeaturesImplBase.__init__(self, filters, validators, tag)

        self.__key_blueprint: Final[BlueprintIface[DictionaryBlueprint_KT]] = key_blueprint
        self.__value_blueprint: Final[BlueprintIface[DictionaryBlueprint_VT]] = value_blueprint

    @final
    def get_key_blueprint(self) -> BlueprintIface[DictionaryBlueprint_KT]:
        return self.__key_blueprint

    @final
    def get_value_blueprint(self) -> BlueprintIface[DictionaryBlueprint_VT]:
        return self.__value_blueprint

    def _get_allowed_output_data_types(self) -> Optional[Tuple[Type, ...]]:
        return dict,

    def _parse(self, input_data: Any) -> Dict[DictionaryBlueprint_KT, DictionaryBlueprint_VT]:
        dict_from_input_data = self.__convert_input_data_to_dict(input_data)

        # Writing this as dict comprehension is quite unclear
        output_dict = {}
        for input_key, input_value in dict_from_input_data.items():
            blueprinted_key = self.__run_dict_key_through_blueprint(input_key, input_data)
            blueprinted_value = self.__run_dict_value_through_blueprint(input_value)

            output_dict[blueprinted_key] = blueprinted_value

        return output_dict

    @final
    def __convert_input_data_to_dict(self, input_data: Any) -> Dict[Hashable, Any]:
        try:
            return dict(input_data)
        except Exception:
            raise self._invalid_input_data_exc_factory.generate_input_data_not_convertible_exc((dict,), input_data)

    @final
    def __run_dict_key_through_blueprint(self, input_key: Hashable, input_data: Any) -> DictionaryBlueprint_KT:
        blueprinted_key = self.__key_blueprint.use(input_key)  # Recursive behaviour

        # The output of the key blueprint is used as the resulting dictionary's key, so it must be hashable. This check
        #  of hashability is not necessary there (the dictionary, of course, checks it itself), but it allows us to
        #  raise an exception with an user-readable error message.
        try:
            hash(blueprinted_key)
        except Exception:  # Can be TypeError, ...
            raise self._invalid_input_data_exc_factory.generate_invalid_input_data_exc(
                "The output (of type '{}') of the key blueprint ('{}') must be hashable: {}".format(
                    self._invalid_input_data_exc_factory.__class__.get_class_name(blueprinted_key),
                    self._invalid_input_data_exc_factory.__class__.get_class_name(self.__key_blueprint),
                    repr(blueprinted_key)
                ),
                input_data
            )

        return blueprinted_key

    @final
    def __run_dict_value_through_blueprint(self, input_value: Any) -> DictionaryBlueprint_VT:
        # For possible future expansion & code consistency.
        return self.__value_blueprint.use(input_value)  # Recursive behaviour
