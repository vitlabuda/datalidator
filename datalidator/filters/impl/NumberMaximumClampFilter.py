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


from typing import final, Final, Generic, TypeVar
import math
from datalidator.filters.DefaultFilterImplBase import DefaultFilterImplBase
from datalidator.filters.exc.err.InvalidFilterConfigError import InvalidFilterConfigError


__all__ = "NumberMaximumClampFilter", "NumberMaximumClampFilter_Number"
NumberMaximumClampFilter_Number = TypeVar("NumberMaximumClampFilter_Number", int, float)


class NumberMaximumClampFilter(DefaultFilterImplBase[NumberMaximumClampFilter_Number], Generic[NumberMaximumClampFilter_Number]):
    """
    Clamps the input number to the initializer-provided maximum value.
    """

    __slots__ = "__maximum_value",

    def __init__(self, maximum_value: NumberMaximumClampFilter_Number, tag: str = ""):
        DefaultFilterImplBase.__init__(self, tag)

        self.__maximum_value: Final[NumberMaximumClampFilter_Number] = maximum_value

        if not math.isfinite(self.__maximum_value):
            raise InvalidFilterConfigError("The maximum value must be a finite number: {}".format(repr(self.__maximum_value)), self._tag)

    @final
    def get_maximum_value(self) -> NumberMaximumClampFilter_Number:
        return self.__maximum_value

    def _filter(self, data: NumberMaximumClampFilter_Number) -> NumberMaximumClampFilter_Number:
        return min(data, self.__maximum_value)
