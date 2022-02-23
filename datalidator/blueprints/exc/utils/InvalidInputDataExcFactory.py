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


from typing import Final, Sequence, Any, KeysView, ValuesView, Union
from datalidator.blueprints.exc.InvalidInputDataExc import InvalidInputDataExc
from datalidator.blueprints.exc.InputDataTypeNotInAllowlistExc import InputDataTypeNotInAllowlistExc
from datalidator.blueprints.exc.InputDataTypeInBlocklistExc import InputDataTypeInBlocklistExc
from datalidator.blueprints.exc.InputDataNotConvertibleExc import InputDataNotConvertibleExc
from datalidator.blueprints.exc.InputDataValueNotAllowedForDataTypeExc import InputDataValueNotAllowedForDataTypeExc
from datalidator.blueprints.exc.InputDataNotUnsubclassableExc import InputDataNotUnsubclassableExc


__all__ = "InvalidInputDataExcFactory",


class InvalidInputDataExcFactory:  # DP: Factory
    """
    A utility class that generates common instances of 'InvalidInputDataExc' exception and its subclasses.
    """

    # All of this class's methods and instance variables are public or protected - feel free to extend this class.

    __slots__ = "_originator_tag",

    def __init__(self, originator_tag: str):
        self._originator_tag: Final[str] = originator_tag

    def generate_invalid_input_data_exc(self, error_message: str, input_data: Any) -> InvalidInputDataExc:
        return InvalidInputDataExc(error_message, self._originator_tag, input_data)

    def generate_input_data_type_not_in_allowlist_exc(self, data_type_allowlist: Sequence[Any], input_data: Any) -> InvalidInputDataExc:
        if len(data_type_allowlist) == 1:
            error_message = "The input data must be of type '{}', not '{}'!".format(
                self.__class__.get_class_name(data_type_allowlist[0]),
                self.__class__.get_class_name(input_data)
            )
        else:
            error_message = "The input data must be of one of these types: {}, not '{}'!".format(
                self.__class__.get_single_string_representation_of_class_names(data_type_allowlist),
                self.__class__.get_class_name(input_data)
            )

        return InputDataTypeNotInAllowlistExc(error_message, self._originator_tag, input_data)

    def generate_input_data_type_in_blocklist_exc(self, data_type_blocklist: Sequence[Any], input_data: Any) -> InvalidInputDataExc:
        if len(data_type_blocklist) == 1:
            # The data type is taken from the blocklist because the type of the input data can be a subclass of the forbidden type
            error_message = "The input data must not be of type '{}'!".format(self.__class__.get_class_name(data_type_blocklist[0]))
        else:
            error_message = "The input data (of type '{}') must not be of these types: {}!".format(
                self.__class__.get_class_name(input_data),
                self.__class__.get_single_string_representation_of_class_names(data_type_blocklist)
            )

        return InputDataTypeInBlocklistExc(error_message, self._originator_tag, input_data)

    def generate_input_data_not_convertible_exc(self, converted_to: Sequence[Any], input_data: Any) -> InvalidInputDataExc:
        # Raised (mostly) in response to a "type cast" failure.
        if len(converted_to) == 1:
            error_message = "The input data (of type '{}') are not convertible to '{}': {}".format(
                self.__class__.get_class_name(input_data),
                self.__class__.get_class_name(converted_to[0]),
                repr(input_data)
            )
        else:
            error_message = "The input data (of type '{}': {}) are not convertible to at least one of these types: {}".format(
                self.__class__.get_class_name(input_data),
                repr(input_data),
                self.__class__.get_single_string_representation_of_class_names(converted_to)
            )

        return InputDataNotConvertibleExc(error_message, self._originator_tag, input_data)

    def generate_input_data_value_not_allowed_for_data_type_exc(self, data_type: Any, allowed_values: Sequence[Any], input_data: Any) -> InvalidInputDataExc:
        # The data type is passed manually because the type of the input data can be a subclass of the type for which
        #  there are allowed values
        error_message = "If the input data are of type '{}', their value must be one of these: {}, not {}!".format(
            self.__class__.get_class_name(data_type),
            self.__class__.get_single_string_representation_of_values(allowed_values),
            repr(input_data)
        )

        return InputDataValueNotAllowedForDataTypeExc(error_message, self._originator_tag, input_data)

    def generate_input_data_not_unsubclassable_exc(self, unsubclassed_to: Any, input_data: Any) -> InvalidInputDataExc:
        error_message = "The input data of type '{input_data_class_name}' (a subclass of '{subclass_name}') could not be unsubclassed to '{subclass_name}'!".format(
            input_data_class_name=self.__class__.get_class_name(input_data),
            subclass_name=self.__class__.get_class_name(unsubclassed_to)
        )

        return InputDataNotUnsubclassableExc(error_message, self._originator_tag, input_data)

    # The following methods can be used from the outside when their output is used in an error message passed to the
    #  generate_generic_exc() method of this class.
    @classmethod
    def get_class_name(cls, object_: Any) -> str:
        if not isinstance(object_, type):
            object_ = object_.__class__

        return object_.__name__  # Used in error messages.

    @classmethod
    def get_single_string_representation_of_class_names(cls, objects: Sequence[Any]) -> str:
        class_names = tuple(cls.get_class_name(object_) for object_ in objects)

        return repr(class_names)  # Used in error messages - the reason why a repr() is returned instead of the plain tuple.

    @classmethod
    def get_single_string_representation_of_values(cls, objects: Union[Sequence[Any], KeysView, ValuesView]) -> str:
        # The objects returned by dict.keys() and dict.values() do not work with the Sequence type annotation.

        return repr(tuple(objects))  # Used in error messages.
