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
from datalidator.validators.DefaultValidatorWithNegationSupportImplBase import DefaultValidatorWithNegationSupportImplBase
from datalidator.validators.exc.err.InvalidValidatorConfigError import InvalidValidatorConfigError


__all__ = "StringContainsSubstringValidator",


class StringContainsSubstringValidator(DefaultValidatorWithNegationSupportImplBase[str]):
    """
    POSITIVE VALIDATION (default; negate=False):
     The input string is valid if it contains the initializer-provided 'checked_substring'.

    NEGATIVE VALIDATION (negate=True):
     The input string is valid if it does not contain the initializer-provided 'checked_substring'.
    """

    __slots__ = "__checked_substring", "__perform_check_case_sensitively"

    def __init__(self,
                 checked_substring: str,
                 perform_check_case_sensitively: bool = True,
                 negate: bool = False,
                 tag: str = ""):
        DefaultValidatorWithNegationSupportImplBase.__init__(self, negate, tag)

        self.__checked_substring: Final[str] = checked_substring
        self.__perform_check_case_sensitively: Final[bool] = perform_check_case_sensitively

        if self.__checked_substring == "":
            raise InvalidValidatorConfigError("The supplied checked substring is empty!", self._tag)

    @final
    def get_checked_substring(self) -> str:
        return self.__checked_substring

    @final
    def is_check_performed_case_sensitively(self) -> bool:
        return self.__perform_check_case_sensitively

    def _validate_positively(self, data: str) -> None:  # Contains substring? -> Valid
        if self.__does_string_contain_substring(data):
            return

        raise self._generate_data_validation_failed_exc(
            "The substring ({}) is not present within the input string: {}".format(
                repr(self.__checked_substring),
                repr(data)
            )
        )

    def _validate_negatively(self, data: str) -> None:  # Does not contain substring? -> Valid
        if self.__does_string_contain_substring(data):
            raise self._generate_data_validation_failed_exc(
                "The substring ({}) is present within the input string: {}".format(
                    repr(self.__checked_substring),
                    repr(data)
                )
            )

    @final
    def __does_string_contain_substring(self, string: str) -> bool:
        if self.__perform_check_case_sensitively:
            return self.__checked_substring in string

        return self.__checked_substring.lower() in string.lower()
