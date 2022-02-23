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


from typing import final, Final, Sequence, Tuple, Generic, TypeVar
from datalidator.validators.DefaultValidatorImplBase import DefaultValidatorImplBase
from datalidator.validators.exc.err.InvalidValidatorConfigError import InvalidValidatorConfigError


__all__ = "AllowlistValidator", "AllowlistValidator_T"
AllowlistValidator_T = TypeVar("AllowlistValidator_T")


class AllowlistValidator(DefaultValidatorImplBase[AllowlistValidator_T], Generic[AllowlistValidator_T]):
    """
    The input is valid if its value is present in the initializer-provided allowlist.

    NOTE: The presence of input values in the allowlist is checked using the 'in' operator.
    """

    __slots__ = "__allowlist",

    def __init__(self, allowlist: Sequence[AllowlistValidator_T], tag: str = ""):
        DefaultValidatorImplBase.__init__(self, tag)

        # Converting the sequence to tuple to prevent it from being (accidentally) modified from the outside.
        self.__allowlist: Final[Tuple[AllowlistValidator_T, ...]] = tuple(allowlist)

        if len(self.__allowlist) == 0:
            raise InvalidValidatorConfigError("The allowlist is empty!", self._tag)

    @final
    def get_allowlist(self) -> Sequence[AllowlistValidator_T]:
        return self.__allowlist  # An *immutable* sequence (tuple) is returned

    def _validate(self, data: AllowlistValidator_T) -> None:
        if data in self.__allowlist:
            return

        raise self._generate_data_validation_failed_exc("The allowlist does not contain the input value: {}".format(repr(data)))
