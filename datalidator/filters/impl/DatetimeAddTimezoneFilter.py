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
import datetime
from datalidator.filters.DefaultFilterImplBase import DefaultFilterImplBase


__all__ = "DatetimeAddTimezoneFilter",


class DatetimeAddTimezoneFilter(DefaultFilterImplBase[datetime.datetime]):
    """
    Adds the initializer-provided timezone information to naive input datetime objects.
    Aware objects remain unmodified.
    """

    __slots__ = "__added_timezone",

    def __init__(self, added_timezone: datetime.tzinfo, tag: str = ""):
        DefaultFilterImplBase.__init__(self, tag)

        self.__added_timezone: Final[datetime.tzinfo] = added_timezone

    @final
    def get_added_timezone(self) -> datetime.tzinfo:
        return self.__added_timezone

    def _filter(self, data: datetime.datetime) -> datetime.datetime:
        if data.tzinfo is None:  # = If the input datetime.datetime object is naive
            data = data.replace(tzinfo=self.__added_timezone)

        return data
