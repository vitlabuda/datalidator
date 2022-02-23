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


from typing import final, Final, Union, Callable
import re
from datalidator.filters.DefaultFilterImplBase import DefaultFilterImplBase
from datalidator.filters.exc.RegexFailedInFilterExc import RegexFailedInFilterExc
from datalidator.filters.exc.err.InvalidFilterConfigError import InvalidFilterConfigError
from datalidator.filters.exc.err.RegexCompilationFailedInFilterError import RegexCompilationFailedInFilterError


__all__ = "StringRegexReplaceFilter",


class StringRegexReplaceFilter(DefaultFilterImplBase[str]):
    """
    Applies the re.sub() function to the input string.
    """

    __slots__ = "__regex_pattern", "__replacement", "__max_replacement_count", "__regex_compile_flags", "__complied_regex"

    def __init__(self,
                 regex_pattern: str,
                 replacement: Union[str, Callable[[re.Match], str]],
                 max_replacement_count: int = 0,
                 regex_compile_flags: int = 0,
                 tag: str = ""):
        DefaultFilterImplBase.__init__(self, tag)

        self.__regex_pattern: Final[str] = regex_pattern
        self.__replacement: Final[Union[str, Callable[[re.Match], str]]] = replacement
        self.__max_replacement_count: Final[int] = max_replacement_count
        self.__regex_compile_flags: Final[int] = regex_compile_flags

        if self.__max_replacement_count < 0:
            raise InvalidFilterConfigError(
                "The supplied maximum replacement count is invalid: {}".format(self.__max_replacement_count),
                self._tag
            )

        try:
            self.__complied_regex: Final[re.Pattern] = re.compile(self.__regex_pattern, self.__regex_compile_flags)
        except Exception as e:
            raise RegexCompilationFailedInFilterError(
                "The supplied regex pattern and/or flags cannot be compiled: {}".format(str(e)),
                self._tag, e
            )

    @final
    def get_regex_pattern(self) -> str:
        return self.__regex_pattern

    @final
    def get_replacement(self) -> Union[str, Callable[[re.Match], str]]:
        return self.__replacement

    @final
    def get_max_replacement_count(self) -> int:
        return self.__max_replacement_count

    @final
    def get_regex_compile_flags(self) -> int:
        return self.__regex_compile_flags

    def _filter(self, data: str) -> str:
        try:
            return self.__complied_regex.sub(self.__replacement, data, self.__max_replacement_count)
        except Exception as e:
            raise RegexFailedInFilterExc(
                "An exception occurred while using the precompiled regex object to replace a substring in the input string!",
                self._tag, e
            )
