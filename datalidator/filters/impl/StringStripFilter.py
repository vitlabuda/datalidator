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


from typing import final, Final, Optional
from datalidator.filters.DefaultFilterImplBase import DefaultFilterImplBase
from datalidator.filters.exc.err.InvalidFilterConfigError import InvalidFilterConfigError


__all__ = "StringStripFilter",


class StringStripFilter(DefaultFilterImplBase[str]):
    """
    By default, strips whitespace characters from both the beginning and end of the input string.
    The behavior can be customized using the 'do_left_strip', 'do_right_strip' and 'stripped_characters' initializer arguments.
    """

    __slots__ = "__do_left_strip", "__do_right_strip", "__stripped_characters"

    def __init__(self,
                 do_left_strip: bool = True,
                 do_right_strip: bool = True,
                 stripped_characters: Optional[str] = None,
                 tag: str = ""):
        DefaultFilterImplBase.__init__(self, tag)

        self.__do_left_strip: Final[bool] = do_left_strip
        self.__do_right_strip: Final[bool] = do_right_strip
        self.__stripped_characters: Final[Optional[str]] = stripped_characters

        if (not self.__do_left_strip) and (not self.__do_right_strip):
            raise InvalidFilterConfigError("Neither left nor right strip is performed!", self._tag)

        if self.__stripped_characters == "":
            raise InvalidFilterConfigError("The supplied set of stripped characters is an empty string!", self._tag)

    @final
    def is_left_strip_performed(self) -> bool:
        return self.__do_left_strip

    @final
    def is_right_strip_performed(self) -> bool:
        return self.__do_right_strip

    @final
    def get_stripped_characters(self) -> Optional[str]:
        return self.__stripped_characters

    def _filter(self, data: str) -> str:
        if self.__do_left_strip:
            data = data.lstrip(self.__stripped_characters)

        if self.__do_right_strip:
            data = data.rstrip(self.__stripped_characters)

        return data
