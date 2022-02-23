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
from datalidator.DatalidatorConstants import DatalidatorConstants
from datalidator.filters.DefaultFilterImplBase import DefaultFilterImplBase
from datalidator.filters.impl.StringRegexReplaceFilter import StringRegexReplaceFilter
from datalidator.filters.exc.err.InvalidFilterConfigError import InvalidFilterConfigError


__all__ = "StringUnifyNewlinesFilter",


class StringUnifyNewlinesFilter(DefaultFilterImplBase[str]):
    """
    Replaces all newline characters and sequences (including, but not limited to '\r', '\n' and '\r\n') in the input
     string with the initializer-provided 'replacement_newline'.
    """

    __slots__ = "__replacement_newline", "__regex_replace_filter"

    def __init__(self, replacement_newline: str = "\n", tag: str = ""):
        DefaultFilterImplBase.__init__(self, tag)

        self.__replacement_newline: Final[str] = replacement_newline

        if self.__replacement_newline not in DatalidatorConstants.NEWLINE_SEQUENCES:
            raise InvalidFilterConfigError(
                "The replacement newline string must be one of these: {}, not {}!".format(
                    repr(DatalidatorConstants.NEWLINE_SEQUENCES),
                    repr(self.__replacement_newline)
                ),
                self._tag
            )

        regex = "|".join(DatalidatorConstants.NEWLINE_SEQUENCES)
        self.__regex_replace_filter: Final[StringRegexReplaceFilter] = StringRegexReplaceFilter(
            regex_pattern=regex,
            replacement=self.__replacement_newline,
            max_replacement_count=0,
            regex_compile_flags=0,
            tag=self._tag
        )

    @final
    def get_replacement_newline(self) -> str:
        return self.__replacement_newline

    def _filter(self, data: str) -> str:
        return self.__regex_replace_filter.filter(data)
