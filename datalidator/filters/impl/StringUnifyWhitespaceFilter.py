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
import re
from datalidator.filters.DefaultFilterImplBase import DefaultFilterImplBase
from datalidator.filters.impl.StringRegexReplaceFilter import StringRegexReplaceFilter
from datalidator.filters.exc.err.InvalidFilterConfigError import InvalidFilterConfigError


__all__ = "StringUnifyWhitespaceFilter",


class StringUnifyWhitespaceFilter(DefaultFilterImplBase[str]):
    """
    Replaces all whitespace characters in the input string with the initializer-provided 'replacement_whitespace'.
    """

    __slots__ = "__replacement_whitespace", "__regex_replacement_filter"

    def __init__(self, replacement_whitespace: str = " ", tag: str = ""):
        DefaultFilterImplBase.__init__(self, tag)

        self.__replacement_whitespace: Final[str] = replacement_whitespace

        if not re.match(r'^\s\Z', self.__replacement_whitespace):
            raise InvalidFilterConfigError(
                "The supplied replacement whitespace character is not valid: {}".format(repr(self.__replacement_whitespace)),
                self._tag
            )

        self.__regex_replacement_filter: Final[StringRegexReplaceFilter] = StringRegexReplaceFilter(
            regex_pattern=r'\s',
            replacement=self.__replacement_whitespace,
            max_replacement_count=0,
            regex_compile_flags=0,
            tag=self._tag
        )

    @final
    def get_replacement_whitespace(self) -> str:
        return self.__replacement_whitespace

    def _filter(self, data: str) -> str:
        return self.__regex_replacement_filter.filter(data)
