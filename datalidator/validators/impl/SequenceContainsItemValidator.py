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


from typing import final, Final, Sequence, TypeVar
from datalidator.validators.DefaultValidatorWithNegationSupportImplBase import DefaultValidatorWithNegationSupportImplBase


__all__ = "SequenceContainsItemValidator", "SequenceContainsItemValidator_T"
SequenceContainsItemValidator_T = TypeVar("SequenceContainsItemValidator_T")


class SequenceContainsItemValidator(DefaultValidatorWithNegationSupportImplBase[Sequence[SequenceContainsItemValidator_T]]):
    """
    POSITIVE VALIDATION (default; negate=False):
     The input sequence is valid if it contains the initializer-provided 'checked_item'.

    NEGATIVE VALIDATION (negate=True):
     The input sequence is valid if it does not contain the initializer-provided 'checked_item'.
    """

    __slots__ = "__checked_item",

    def __init__(self, checked_item: SequenceContainsItemValidator_T, negate: bool = False, tag: str = ""):
        DefaultValidatorWithNegationSupportImplBase.__init__(self, negate, tag)

        self.__checked_item: Final[SequenceContainsItemValidator_T] = checked_item

    @final
    def get_checked_item(self) -> SequenceContainsItemValidator_T:
        return self.__checked_item

    def _validate_positively(self, data: Sequence[SequenceContainsItemValidator_T]) -> None:  # Sequence contains item? -> Valid
        if self.__does_sequence_contain_item(data):
            return

        raise self._generate_data_validation_failed_exc("The item is not present in the input sequence: {}".format(repr(self.__checked_item)))

    def _validate_negatively(self, data: Sequence[SequenceContainsItemValidator_T]) -> None:  # Sequence does not contain item? -> Valid
        if self.__does_sequence_contain_item(data):
            raise self._generate_data_validation_failed_exc("The item is present in the input sequence: {}".format(repr(self.__checked_item)))

    @final
    def __does_sequence_contain_item(self, sequence: Sequence[SequenceContainsItemValidator_T]) -> bool:
        return self.__checked_item in sequence
