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


from typing import Final
from datalidator.filters.DefaultFilterImplBase import DefaultFilterImplBase
from datalidator.filters.impl.StringRegexReplaceFilter import StringRegexReplaceFilter


__all__ = "StringDeduplicateWhitespaceFilter",


class StringDeduplicateWhitespaceFilter(DefaultFilterImplBase[str]):
    """
    Reduces all groups of consecutive whitespace characters in the input string to one such whitespace.
    """

    __slots__ = "__regex_replacement_filter",

    def __init__(self, tag: str = ""):
        DefaultFilterImplBase.__init__(self, tag)

        self.__regex_replacement_filter: Final[StringRegexReplaceFilter] = StringRegexReplaceFilter(
            regex_pattern=r'(\s)+',
            replacement=r'\1',
            max_replacement_count=0,
            regex_compile_flags=0,
            tag=self._tag
        )

    def _filter(self, data: str) -> str:
        return self.__regex_replacement_filter.filter(data)
