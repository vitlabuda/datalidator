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
import re
from datalidator.validators.DefaultValidatorWithNegationSupportImplBase import DefaultValidatorWithNegationSupportImplBase
from datalidator.validators.exc.RegexFailedInValidatorExc import RegexFailedInValidatorExc
from datalidator.validators.exc.err.RegexCompilationFailedInValidatorError import RegexCompilationFailedInValidatorError


__all__ = "StringMatchesRegexValidator",


class StringMatchesRegexValidator(DefaultValidatorWithNegationSupportImplBase[str]):
    """
    POSITIVE VALIDATION (default; negate=False):
     The input string is valid if it matches the initializer-provided regex.

    NEGATIVE VALIDATION (negate=True):
     The input string is valid if it does not match the initializer-provided regex.
    """

    __slots__ = "__regex_pattern", "__regex_compile_flags", "__compiled_regex"

    def __init__(self,
                 regex_pattern: str,
                 regex_compile_flags: int = 0,
                 negate: bool = False,
                 tag: str = ""):
        DefaultValidatorWithNegationSupportImplBase.__init__(self, negate, tag)

        self.__regex_pattern: Final[str] = regex_pattern
        self.__regex_compile_flags: Final[int] = regex_compile_flags

        try:
            self.__compiled_regex: Final[re.Pattern] = re.compile(self.__regex_pattern, self.__regex_compile_flags)
        except Exception as e:
            raise RegexCompilationFailedInValidatorError(
                "The supplied regex pattern and/or flags cannot be compiled: {}".format(str(e)),
                self._tag, e
            )

    @final
    def get_regex_pattern(self) -> str:
        return self.__regex_pattern

    @final
    def get_regex_compile_flags(self) -> int:
        return self.__regex_compile_flags

    def _validate_positively(self, data: str) -> None:  # String matches the regex? -> Valid
        if self.__does_string_match_regex(data):
            return

        raise self._generate_data_validation_failed_exc("The regex does not match the input string: {}".format(repr(data)))

    def _validate_negatively(self, data: str) -> None:  # String does not match the regex? -> Valid
        if self.__does_string_match_regex(data):
            raise self._generate_data_validation_failed_exc("The regex matches the input string: {}".format(repr(data)))

    @final
    def __does_string_match_regex(self, string: str) -> bool:
        try:
            # https://docs.python.org/3/library/re.html#search-vs-match
            #  "Python offers two different primitive operations based on regular expressions: re.match() checks for a
            #  match only at the beginning of the string, while re.search() checks for a match anywhere in the string
            #  (this is what Perl does by default)."

            return bool(self.__compiled_regex.search(string))
        except Exception as e:
            raise RegexFailedInValidatorExc(
                "An exception occurred while using the precompiled regex object to match the input string!",
                self._tag, e
            )
