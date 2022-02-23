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
from datalidator.validators.DefaultValidatorImplBase import DefaultValidatorImplBase
from datalidator.validators.exc.InputDatetimeObjectIsNaiveInValidatorExc import InputDatetimeObjectIsNaiveInValidatorExc
from datalidator.validators.exc.err.InvalidValidatorConfigError import InvalidValidatorConfigError


__all__ = "DatetimeNotBeforeValidator",


class DatetimeNotBeforeValidator(DefaultValidatorImplBase[datetime.datetime]):
    """
    The input datetime object is valid if the time it represents is chronologically not before the time represented by
     the initializer-provided 'earliest_acceptable_datetime' object.

    Note: Both the input datetime object and the earliest acceptable datetime object must be aware!
    """

    __slots__ = "__earliest_acceptable_datetime",

    def __init__(self, earliest_acceptable_datetime: datetime.datetime, tag: str = ""):
        DefaultValidatorImplBase.__init__(self, tag)

        self.__earliest_acceptable_datetime: Final[datetime.datetime] = earliest_acceptable_datetime

        if self.__earliest_acceptable_datetime.tzinfo is None:
            raise InvalidValidatorConfigError("The supplied earliest acceptable datetime object is naive!", self._tag)

    @final
    def get_earliest_acceptable_datetime(self) -> datetime.datetime:
        return self.__earliest_acceptable_datetime

    def _validate(self, data: datetime.datetime) -> None:
        if data.tzinfo is None:
            raise InputDatetimeObjectIsNaiveInValidatorExc("The input datetime object is naive!", self._tag)

        if data < self.__earliest_acceptable_datetime:
            raise self._generate_data_validation_failed_exc(
                "The input datetime object ({}) represents an earlier time than the earliest acceptable time ({})!".format(str(data), str(self.__earliest_acceptable_datetime))
            )
