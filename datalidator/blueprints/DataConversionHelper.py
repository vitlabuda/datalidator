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


from typing import Final, Generic, Callable, Any, Tuple, Type, Sequence, TypeVar
from datalidator.blueprints.exc.utils.InvalidInputDataExcFactory import InvalidInputDataExcFactory


__all__ = "DataConversionHelper", "DataConversionHelper_T"
DataConversionHelper_T = TypeVar("DataConversionHelper_T")


class DataConversionHelper(Generic[DataConversionHelper_T]):
    """
    A utility class offering methods that help with input data conversion in blueprints.
    """

    __slots__ = "_invalid_input_data_exc_factory",

    # All of this class's methods and instance variables are public or protected - feel free to extend this class.

    def __init__(self, invalid_input_data_exc_factory: InvalidInputDataExcFactory):
        self._invalid_input_data_exc_factory: Final[InvalidInputDataExcFactory] = invalid_input_data_exc_factory

    def convert_input_with_data_type_allowlist(self, converter_function: Callable[[Any], DataConversionHelper_T], data_type_allowlist: Tuple[Type, ...], input_data: Any) -> DataConversionHelper_T:
        """
        Passes 'input_data' to 'converter_function' only if their data type is in 'data_type_allowlist'.
        Otherwise, 'InputDataTypeNotInAllowlistExc' is raised.
        """

        if isinstance(input_data, data_type_allowlist):
            return converter_function(input_data)

        raise self._invalid_input_data_exc_factory.generate_input_data_type_not_in_allowlist_exc(data_type_allowlist, input_data)

    def convert_input_with_data_type_blocklist(self, converter_function: Callable[[Any], DataConversionHelper_T], data_type_blocklist: Tuple[Type, ...], input_data: Any) -> DataConversionHelper_T:
        """
        Passes 'input_data' to 'converter_function' only if their data type is not in 'data_type_blocklist'.
        Otherwise, 'InputDataTypeInBlocklistExc' is raised.
        """

        if isinstance(input_data, data_type_blocklist):
            raise self._invalid_input_data_exc_factory.generate_input_data_type_in_blocklist_exc(data_type_blocklist, input_data)

        return converter_function(input_data)

    def convert_input_using_per_data_type_converter_functions(self, type_converter_pairs: Sequence[Tuple[Tuple[Type, ...], Callable[[Any], DataConversionHelper_T]]], input_data: Any) -> DataConversionHelper_T:
        """
        This function accepts a sequence of type-converter pairs. Each pair is a two-tuple, whose first item is a tuple
         of data types (classes) and second item is a converter function for these data types.

        This function is useful when different types of input data have different methods of converting them to output
         data type in a blueprint.
        """

        for data_types, converter_function in type_converter_pairs:
            if isinstance(input_data, data_types):
                return converter_function(input_data)

        # If no suitable converter function is found for the input data, an exception is raised
        data_type_allowlist = []
        for data_types, _ in type_converter_pairs:
            data_type_allowlist += data_types

        raise self._invalid_input_data_exc_factory.generate_input_data_type_not_in_allowlist_exc(data_type_allowlist, input_data)
