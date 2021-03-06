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


from typing import final, Final, Sequence, Mapping, Generic, TypeVar
from datalidator.validators.DefaultValidatorImplBase import DefaultValidatorImplBase
from datalidator.validators.exc.err.InvalidValidatorConfigError import InvalidValidatorConfigError


__all__ = "SequenceMaximumLengthValidator", "SequenceMaximumLengthValidator_T"
SequenceMaximumLengthValidator_T = TypeVar("SequenceMaximumLengthValidator_T", Sequence, Mapping, str)


class SequenceMaximumLengthValidator(DefaultValidatorImplBase[SequenceMaximumLengthValidator_T], Generic[SequenceMaximumLengthValidator_T]):
    """
    The input sequence or mapping is valid if its length is not more than the initializer-provided 'maximum_acceptable_length'.

    NOTE: Strings are sequences as well. This validator can also be used on mappings (e.g. dictionaries).
    """

    __slots__ = "__maximum_acceptable_length",

    def __init__(self, maximum_acceptable_length: int, tag: str = ""):
        DefaultValidatorImplBase.__init__(self, tag)

        self.__maximum_acceptable_length: Final[int] = maximum_acceptable_length

        if self.__maximum_acceptable_length < 0:
            raise InvalidValidatorConfigError("The maximum acceptable length is negative: {}".format(self.__maximum_acceptable_length), self._tag)

    @final
    def get_maximum_acceptable_length(self) -> int:
        return self.__maximum_acceptable_length

    def _validate(self, data: SequenceMaximumLengthValidator_T) -> None:
        sequence_length = len(data)

        if sequence_length > self.__maximum_acceptable_length:
            raise self._generate_data_validation_failed_exc(
                "The input sequence's length ({}) is bigger than the maximum acceptable length ({})!".format(sequence_length, self.__maximum_acceptable_length)
            )
