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


from typing import final, Final
from datalidator.filters.DefaultFilterImplBase import DefaultFilterImplBase
from datalidator.filters.exc.err.InvalidFilterConfigError import InvalidFilterConfigError


__all__ = "StringReplaceFilter",


class StringReplaceFilter(DefaultFilterImplBase[str]):
    """
    Replaces occurrences of the initializer-provided 'old_substring' with 'new_substring' in the input string.
    """

    __slots__ = "__old_substring", "__new_substring", "__max_replacement_count"

    def __init__(self,
                 old_substring: str,
                 new_substring: str,
                 max_replacement_count: int = -1,
                 tag: str = ""):
        DefaultFilterImplBase.__init__(self, tag)

        self.__old_substring: Final[str] = old_substring
        self.__new_substring: Final[str] = new_substring
        self.__max_replacement_count: Final[int] = max_replacement_count

        if self.__old_substring == "":
            raise InvalidFilterConfigError("The supplied old substring is empty!", self._tag)

        if (self.__max_replacement_count < -1) or (self.__max_replacement_count == 0):
            raise InvalidFilterConfigError(
                "The supplied maximum replacement count is invalid: {}".format(self.__max_replacement_count),
                self._tag
            )

    @final
    def get_old_substring(self) -> str:
        return self.__old_substring

    @final
    def get_new_substring(self) -> str:
        return self.__new_substring

    @final
    def get_max_replacement_count(self) -> int:
        return self.__max_replacement_count

    def _filter(self, data: str) -> str:
        return data.replace(self.__old_substring, self.__new_substring, self.__max_replacement_count)
