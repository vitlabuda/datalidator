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
from datalidator.filters.exc.InputDatetimeObjectIsNaiveInFilterExc import InputDatetimeObjectIsNaiveInFilterExc


__all__ = "DatetimeChangeTimezoneFilter",


class DatetimeChangeTimezoneFilter(DefaultFilterImplBase[datetime.datetime]):
    """
    Adjusts aware input datetime objects to the new initializer-provided timezone information.
    Raises 'InputDatetimeObjectIsNaiveInFilterExc' when a naive datetime object is passed to this filter.
    """

    __slots__ = "__new_timezone",

    def __init__(self, new_timezone: datetime.tzinfo, tag: str = ""):
        DefaultFilterImplBase.__init__(self, tag)

        self.__new_timezone: Final[datetime.tzinfo] = new_timezone

    @final
    def get_new_timezone(self) -> datetime.tzinfo:
        return self.__new_timezone

    def _filter(self, data: datetime.datetime) -> datetime.datetime:
        if data.tzinfo is None:  # = If the input datetime.datetime object is naive
            raise InputDatetimeObjectIsNaiveInFilterExc(
                "Changing timezone in a naive datetime object is not possible, as such objects do not carry timezone information!",
                self._tag
            )

        return data.astimezone(self.__new_timezone)
