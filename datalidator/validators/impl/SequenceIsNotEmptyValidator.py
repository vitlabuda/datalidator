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


from typing import final, Sequence, Mapping, Generic, TypeVar
from datalidator.validators.DefaultValidatorWithNegationSupportImplBase import DefaultValidatorWithNegationSupportImplBase


__all__ = "SequenceIsNotEmptyValidator", "SequenceIsNotEmptyValidator_T"
SequenceIsNotEmptyValidator_T = TypeVar("SequenceIsNotEmptyValidator_T", Sequence, Mapping, str)


class SequenceIsNotEmptyValidator(DefaultValidatorWithNegationSupportImplBase[SequenceIsNotEmptyValidator_T], Generic[SequenceIsNotEmptyValidator_T]):
    """
    POSITIVE VALIDATION (default; negate=False):
     The input sequence or mapping is valid if it is not empty.

    NEGATIVE VALIDATION (negate=True):
     The input sequence or mapping is valid if it is empty.

    NOTE: Strings are sequences as well. This validator can also be used on mappings (e.g. dictionaries).
    """

    __slots__ = ()

    def _validate_positively(self, data: SequenceIsNotEmptyValidator_T) -> None:  # Sequence is not empty? -> Valid
        if self.__is_sequence_empty(data):
            raise self._generate_data_validation_failed_exc("The input sequence is empty!")

    def _validate_negatively(self, data: SequenceIsNotEmptyValidator_T) -> None:  # Sequence is empty? -> Valid
        if self.__is_sequence_empty(data):
            return

        raise self._generate_data_validation_failed_exc("The input sequence is not empty!")

    @final
    def __is_sequence_empty(self, sequence: SequenceIsNotEmptyValidator_T) -> bool:
        return len(sequence) == 0
