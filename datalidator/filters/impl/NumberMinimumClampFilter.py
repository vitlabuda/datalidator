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


__all__ = "NumberMinimumClampFilter", "NumberMinimumClampFilter_Number"
NumberMinimumClampFilter_Number = TypeVar("NumberMinimumClampFilter_Number", int, float)


class NumberMinimumClampFilter(DefaultFilterImplBase[NumberMinimumClampFilter_Number], Generic[NumberMinimumClampFilter_Number]):
    """
    Clamps the input number to the initializer-provided minimum value.
    """

    __slots__ = "__minimum_value",

    def __init__(self, minimum_value: NumberMinimumClampFilter_Number, tag: str = ""):
        DefaultFilterImplBase.__init__(self, tag)

        self.__minimum_value: Final[NumberMinimumClampFilter_Number] = minimum_value

        if not math.isfinite(self.__minimum_value):
            raise InvalidFilterConfigError("The minimum value must be a finite number: {}".format(repr(self.__minimum_value)), self._tag)

    @final
    def get_minimum_value(self) -> NumberMinimumClampFilter_Number:
        return self.__minimum_value

    def _filter(self, data: NumberMinimumClampFilter_Number) -> NumberMinimumClampFilter_Number:
        return max(data, self.__minimum_value)
