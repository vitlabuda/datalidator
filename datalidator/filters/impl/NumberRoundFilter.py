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
from datalidator.filters.DefaultFilterImplBase import DefaultFilterImplBase


__all__ = "NumberRoundFilter", "NumberRoundFilter_Number"
NumberRoundFilter_Number = TypeVar("NumberRoundFilter_Number", int, float)


class NumberRoundFilter(DefaultFilterImplBase[NumberRoundFilter_Number], Generic[NumberRoundFilter_Number]):
    """
    Rounds the input number to the initializer-provided number of decimal places using the built-in round() function.
    """

    __slots__ = "__decimal_places",

    def __init__(self, decimal_places: int = 0, tag: str = ""):
        DefaultFilterImplBase.__init__(self, tag)

        self.__decimal_places: Final[int] = decimal_places

    @final
    def get_decimal_places(self) -> int:
        return self.__decimal_places

    def _filter(self, data: NumberRoundFilter_Number) -> NumberRoundFilter_Number:
        # The round() function always returns a number of the same type as the input number, but only if the second
        #  argument (decimal places) is provided!

        return round(data, self.__decimal_places)
