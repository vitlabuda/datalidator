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


from typing import final, Final, Tuple
import unicodedata
from datalidator.filters.DefaultFilterImplBase import DefaultFilterImplBase
from datalidator.filters.exc.err.InvalidFilterConfigError import InvalidFilterConfigError


__all__ = "StringUnicodeNormalizeFilter",


class StringUnicodeNormalizeFilter(DefaultFilterImplBase[str]):
    """
    Normalizes Unicode input strings using the 'unicodedata.normalize()' function. See its documentation for more
     information: https://docs.python.org/3/library/unicodedata.html#unicodedata.normalize

    The normal form can be specified using the 'normal_form' initializer argument ('NFC' by default):
    - NFC:  ('ů', '…') -> ('ů', '…')
    - NFKC: ('ů', '…') -> ('ů', '.', '.', '.')
    - NFD:  ('ů', '…') -> ('u', '̊', '…')
    - NFKD: ('ů', '…') -> ('u', '̊', '.', '.', '.')
    See https://towardsdatascience.com/difference-between-nfd-nfc-nfkd-and-nfkc-explained-with-python-code-e2631f96ae6c
     for more information.
    """

    __slots__ = "__normal_form",

    __ALLOWED_NORMAL_FORMS: Final[Tuple[str, ...]] = ("NFC", "NFKC", "NFD", "NFKD")

    def __init__(self, normal_form: str = "NFC", tag: str = ""):
        DefaultFilterImplBase.__init__(self, tag)

        self.__normal_form: Final[str] = normal_form

        if self.__normal_form not in self.__class__.__ALLOWED_NORMAL_FORMS:
            raise InvalidFilterConfigError(
                "The normal form must be one of these: {}, not {}!".format(
                    repr(self.__class__.__ALLOWED_NORMAL_FORMS),
                    repr(self.__normal_form)
                ),
                self._tag
            )

    @final
    def get_normal_form(self) -> str:
        return self.__normal_form

    def _filter(self, data: str) -> str:
        return unicodedata.normalize(self.__normal_form, data)
