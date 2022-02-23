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


from typing import final, Final, Sequence, Tuple, Generic, TypeVar
from datalidator.filters.DefaultFilterImplBase import DefaultFilterImplBase
from datalidator.filters.exc.err.InvalidFilterConfigError import InvalidFilterConfigError


__all__ = "ReplacementMapFilter", "ReplacementMapFilter_T"
ReplacementMapFilter_T = TypeVar("ReplacementMapFilter_T")


class ReplacementMapFilter(DefaultFilterImplBase[ReplacementMapFilter_T], Generic[ReplacementMapFilter_T]):
    """
    If the input value is found in the first item of a tuple in the initializer-provided replacement map (= a sequence
     of such tuples), the second item of the same tuple is returned instead. Keep in mind that the replacement value is
     returned as it is; therefore, using this filter with mutable values is not recommended!
    Input values not found in the replacement map are returned as they are.

    NOTE: Input values are compared with the old values in the replacement map using the '==' operator.
    """

    __slots__ = "__replacement_map",

    def __init__(self, replacement_map: Sequence[Tuple[ReplacementMapFilter_T, ReplacementMapFilter_T]], tag: str = ""):
        DefaultFilterImplBase.__init__(self, tag)

        # Converting the sequence to tuple to prevent it from being (accidentally) modified from the outside.
        # The replacement map is not provided as a dictionary, because the replaced (old) value would have to be Hashable.
        self.__replacement_map: Final[Tuple[Tuple[ReplacementMapFilter_T, ReplacementMapFilter_T], ...]] = tuple(replacement_map)

        if len(self.__replacement_map) == 0:
            raise InvalidFilterConfigError("The replacement map is empty!", self._tag)

    @final
    def get_replacement_map(self) -> Sequence[Tuple[ReplacementMapFilter_T, ReplacementMapFilter_T]]:
        return self.__replacement_map  # An *immutable* sequence (tuple) is returned

    def _filter(self, data: ReplacementMapFilter_T) -> ReplacementMapFilter_T:
        for old_item, new_item in self.__replacement_map:
            if old_item == data:
                return new_item

        return data
