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


from typing import final, Final, Generic, TypeVar
import math
from datalidator.validators.DefaultValidatorImplBase import DefaultValidatorImplBase
from datalidator.validators.exc.err.InvalidValidatorConfigError import InvalidValidatorConfigError


__all__ = "NumberMinimumValueValidator", "NumberMinimumValueValidator_Number"
NumberMinimumValueValidator_Number = TypeVar("NumberMinimumValueValidator_Number", int, float)


class NumberMinimumValueValidator(DefaultValidatorImplBase[NumberMinimumValueValidator_Number], Generic[NumberMinimumValueValidator_Number]):
    """
    The input number is valid if it is not less than the initializer-provided 'minimum_acceptable_number'.
    """

    __slots__ = "__minimum_acceptable_number",

    def __init__(self, minimum_acceptable_number: NumberMinimumValueValidator_Number, tag: str = ""):
        DefaultValidatorImplBase.__init__(self, tag)

        self.__minimum_acceptable_number: Final[NumberMinimumValueValidator_Number] = minimum_acceptable_number

        if not math.isfinite(self.__minimum_acceptable_number):
            raise InvalidValidatorConfigError("The minimum acceptable number must be finite: {}".format(repr(self.__minimum_acceptable_number)), self._tag)

    @final
    def get_minimum_acceptable_number(self) -> NumberMinimumValueValidator_Number:
        return self.__minimum_acceptable_number

    def _validate(self, data: NumberMinimumValueValidator_Number) -> None:
        if data < self.__minimum_acceptable_number:
            raise self._generate_data_validation_failed_exc(
                "The input number ({}) is smaller than the minimum acceptable number ({})!".format(data, self.__minimum_acceptable_number)
            )
