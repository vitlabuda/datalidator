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


from typing import final, Final, Sequence, Tuple, Any, Optional, Type, Generic, TypeVar
import abc
from datalidator.blueprints.DefaultBlueprintImplBase import DefaultBlueprintImplBase
from datalidator.blueprints.DataConversionHelper import DataConversionHelper
from datalidator.blueprints.exc.utils.InvalidInputDataExcFactory import InvalidInputDataExcFactory
from datalidator.blueprints.exc.UnexpectedOutputDataTypeExc import UnexpectedOutputDataTypeExc
from datalidator.filters.FilterIface import FilterIface
from datalidator.validators.ValidatorIface import ValidatorIface


__all__ = "DefaultBlueprintWithStandardFeaturesImplBase", "DefaultBlueprintWithStandardFeaturesImplBase_T"
DefaultBlueprintWithStandardFeaturesImplBase_T = TypeVar("DefaultBlueprintWithStandardFeaturesImplBase_T")


class DefaultBlueprintWithStandardFeaturesImplBase(DefaultBlueprintImplBase[DefaultBlueprintWithStandardFeaturesImplBase_T], Generic[DefaultBlueprintWithStandardFeaturesImplBase_T], metaclass=abc.ABCMeta):
    """
    An extension class of DefaultBlueprintImplBase used by most of this library's built-in blueprints.

    It contains standard functionality that most blueprints need to have. This includes the ability to run parsed data
     through user-provided sequences of filters and validators, the optional last-resort safety check of output data
     type and instances of InvalidInputDataExcFactory and DataConversionHelper classes to simplify the input data
     parsing process.

    Refer to the class hierarchy document to find out which classes extend this base class.
    """

    __slots__ = "__filters", "__validators", "_invalid_input_data_exc_factory", "_data_conversion_helper"

    def __init__(self,
                 filters: Sequence[FilterIface[DefaultBlueprintWithStandardFeaturesImplBase_T]] = (),
                 validators: Sequence[ValidatorIface[DefaultBlueprintWithStandardFeaturesImplBase_T]] = (),
                 tag: str = ""):
        DefaultBlueprintImplBase.__init__(self, tag)

        # Converting the filter and validator sequences to tuples prevents them from being (accidentally) mutated from
        #  the outside. The filters and validators themselves should prevent their mutation too.
        self.__filters: Final[Tuple[FilterIface[DefaultBlueprintWithStandardFeaturesImplBase_T], ...]] = tuple(filters)
        self.__validators: Final[Tuple[ValidatorIface[DefaultBlueprintWithStandardFeaturesImplBase_T], ...]] = tuple(validators)

        # The majority of this class's subclasses use these helpers. There are classes that do not use them
        #  (e.g. GenericBlueprint), but it is way easier to instantiate these helpers for all of this class's instances
        #  instead of implementing them as some kind of "optional features" (I tried implementing some of the features
        #  using mixins and the resulting code ended up being pretty unclear).
        self._invalid_input_data_exc_factory: Final[InvalidInputDataExcFactory] = InvalidInputDataExcFactory(self._tag)
        self._data_conversion_helper: Final[DataConversionHelper[DefaultBlueprintWithStandardFeaturesImplBase_T]] = DataConversionHelper[DefaultBlueprintWithStandardFeaturesImplBase_T](self._invalid_input_data_exc_factory)

    @final
    def get_filters(self) -> Sequence[FilterIface[DefaultBlueprintWithStandardFeaturesImplBase_T]]:
        return self.__filters  # An *immutable* sequence (tuple) is returned

    @final
    def get_validators(self) -> Sequence[ValidatorIface[DefaultBlueprintWithStandardFeaturesImplBase_T]]:
        return self.__validators  # An *immutable* sequence (tuple) is returned

    @final
    def _use(self, input_data: Any) -> DefaultBlueprintWithStandardFeaturesImplBase_T:  # DP: Template method
        # Allowed data types fetched once and saved here to prevent them from changing between the two calls of __check_allowed_output_data_types()
        allowed_output_data_types = self._get_allowed_output_data_types()

        # --- PARSE ---
        output_data = self._parse(input_data)
        self.__check_allowed_output_data_types(allowed_output_data_types, output_data)  # Raises an UnexpectedOutputDataTypeExc if the output data type is invalid

        # --- FILTER ---
        output_data = self.__filter(output_data, allowed_output_data_types)

        # --- VALIDATE ---
        self.__validate(output_data)

        # --- (RETURN) ---
        self.__check_allowed_output_data_types(allowed_output_data_types, output_data)  # Raises an UnexpectedOutputDataTypeExc if the output data type is invalid
        return output_data

    @abc.abstractmethod
    def _get_allowed_output_data_types(self) -> Optional[Tuple[Type, ...]]:
        """
        Blueprints that are subclasses of this base class can choose to have the data type of their output value checked.

        If this method returns a tuple of classes (data types), the check is performed: if the output value's type is
         present in the returned tuple, the check passes; otherwise, 'UnexpectedOutputDataTypeExc' (a subclass of
         'DatalidatorExc') gets raised. Keep in mind that the check does not pass if the output value's type is a
         subclass of a class present in the tuple (this behaviour is completely intentional - it prevents subclasses
         which are not respecting Liskov substitution principle from being returned and then breaking the program
         which is using the blueprint). To turn off the check, return 'None' from this method; however, it is
         recommended to let the check happen if possible.

        WARNING: This functionality should be considered as only a last-resort safety check (as per the rules of
         defensive programming) and should not be relied upon! Blueprints and filters must not produce output data of
         incorrect data types in any case and this check's purpose is to prevent the program using this library from
         receiving output data of invalid type from the blueprint when it is programmed incorrectly!

        :return: Either 'None' (to turn off the check) or a tuple of allowed types (classes) of output data.
        """

        raise NotImplementedError(DefaultBlueprintWithStandardFeaturesImplBase._get_allowed_output_data_types.__qualname__)

    @abc.abstractmethod
    def _parse(self, input_data: Any) -> DefaultBlueprintWithStandardFeaturesImplBase_T:
        """
        Converts untrusted (!) 'input_data' into output data of generic type 'VT' in an appropriate way.

        If possible, the output should not be the same instance as input and the output's type should not be a subclass
         of the desired output type (to prevent subclasses which are not respecting Liskov substitution principle
         from being returned and then breaking the program which is using the blueprint; also see the docstring of this
         class's '_get_allowed_output_data_types()' method).

        Since 'input_data' are untrusted and can be of any data type, it should be ensured that their unexpected
         behaviour is properly handled. Even though this method runs in a context where all exceptions other than
         'DatalidatorExc' and its subclasses are caught and handled (by raising 'UnexpectedExceptionRaisedExc', a
         subclass of 'DatalidatorExc'), this behaviour should be considered only a last resort solution of the problem
         when everything else fails - if you expect that something may go wrong, you should handle it yourselves!

        If the input data are invalid in some way, you should raise an 'InvalidInputDataExc' or one of its subclasses
         (even though any subclass of 'DatalidatorExc' can safely be raised), for whose creation you should use this
         class's instance of 'InvalidInputDataExcFactory' (self._invalid_input_data_exc_factory), and for some very
         common tasks such as checking whether a data type is present in a type allowlist, this class's instance of
         'DataConversionHelper' may be used.

        :param input_data: The untrusted input data to be converted to output data.
        :return: The output data of generic type 'VT'.
        :raises DatalidatorExc: The superclass of all exceptions raised by this library.
        """

        raise NotImplementedError(DefaultBlueprintWithStandardFeaturesImplBase._parse.__qualname__)

    @final
    def __check_allowed_output_data_types(self, allowed_output_data_types: Optional[Tuple[Type, ...]], output_data: DefaultBlueprintWithStandardFeaturesImplBase_T) -> None:
        if allowed_output_data_types is None:  # = If the blueprint does not want to check its output data type:
            return

        for allowed_type in allowed_output_data_types:
            if output_data.__class__ is allowed_type:  # = If the output data type is exactly (not a subclass of) one of the allowed output data types:
                return

        raise UnexpectedOutputDataTypeExc(
            "The exact output data type of {} must be one of these: {}, not {}!".format(
                self._invalid_input_data_exc_factory.__class__.get_class_name(self),
                self._invalid_input_data_exc_factory.__class__.get_single_string_representation_of_class_names(allowed_output_data_types),
                self._invalid_input_data_exc_factory.__class__.get_class_name(output_data)
            ),
            self._tag
        )

    @final
    def __filter(self, output_data: DefaultBlueprintWithStandardFeaturesImplBase_T, allowed_output_data_types: Optional[Tuple[Type, ...]]) -> DefaultBlueprintWithStandardFeaturesImplBase_T:
        for filter_ in self.__filters:
            output_data = filter_.filter(output_data)
            self.__check_allowed_output_data_types(allowed_output_data_types, output_data)  # Raises an UnexpectedOutputDataTypeExc if the output data type is invalid

        return output_data

    @final
    def __validate(self, output_data: DefaultBlueprintWithStandardFeaturesImplBase_T) -> None:
        for validator in self.__validators:
            validator.validate(output_data)
