<!--
Copyright (c) 2022 Vít Labuda. All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
following conditions are met:
 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following
    disclaimer.
 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
    following disclaimer in the documentation and/or other materials provided with the distribution.
 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
    products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
-->


# Datalidator Exception Hierarchy
This document contains the hierarchy of this library's built-in exceptions and errors.

---

## Exceptions
- **DatalidatorExc** *([datalidator.exc.DatalidatorExc](../datalidator/exc/DatalidatorExc.py))*
    - **ValidatorExc** *([datalidator.validators.exc.ValidatorExc](../datalidator/validators/exc/ValidatorExc.py))*
        - **DataValidationFailedExc** *([datalidator.validators.exc.DataValidationFailedExc](../datalidator/validators/exc/DataValidationFailedExc.py))*
        - **RegexFailedInValidatorExc** *([datalidator.validators.exc.RegexFailedInValidatorExc](../datalidator/validators/exc/RegexFailedInValidatorExc.py))*
        - **InputDatetimeObjectIsNaiveInValidatorExc** *([datalidator.validators.exc.InputDatetimeObjectIsNaiveInValidatorExc](../datalidator/validators/exc/InputDatetimeObjectIsNaiveInValidatorExc.py))*
        - **UnexpectedExceptionRaisedInValidatorExc** *([datalidator.validators.exc.UnexpectedExceptionRaisedInValidatorExc](../datalidator/validators/exc/UnexpectedExceptionRaisedInValidatorExc.py))*
    - **FilterExc** *([datalidator.filters.exc.FilterExc](../datalidator/filters/exc/FilterExc.py))*
        - **RegexFailedInFilterExc** *([datalidator.filters.exc.RegexFailedInFilterExc](../datalidator/filters/exc/RegexFailedInFilterExc.py))*
        - **InputDatetimeObjectIsNaiveInFilterExc** *([datalidator.filters.exc.InputDatetimeObjectIsNaiveInFilterExc](../datalidator/filters/exc/InputDatetimeObjectIsNaiveInFilterExc.py))*
        - **UnexpectedExceptionRaisedInFilterExc** *([datalidator.filters.exc.UnexpectedExceptionRaisedInFilterExc](../datalidator/filters/exc/UnexpectedExceptionRaisedInFilterExc.py))*
        - **SortingFailedInFilterExc** *([datalidator.filters.exc.SortingFailedInFilterExc](../datalidator/filters/exc/SortingFailedInFilterExc.py))*
    - **BlueprintExc** *([datalidator.blueprints.exc.BlueprintExc](../datalidator/blueprints/exc/BlueprintExc.py))*
        - **InvalidInputDataExc** *([datalidator.blueprints.exc.InvalidInputDataExc](../datalidator/blueprints/exc/InvalidInputDataExc.py))*
            - **InputDataTypeNotInAllowlistExc** *([datalidator.blueprints.exc.InputDataTypeNotInAllowlistExc](../datalidator/blueprints/exc/InputDataTypeNotInAllowlistExc.py))*
            - **InputDataNotConvertibleExc** *([datalidator.blueprints.exc.InputDataNotConvertibleExc](../datalidator/blueprints/exc/InputDataNotConvertibleExc.py))*
            - **InputDataValueNotAllowedForDataTypeExc** *([datalidator.blueprints.exc.InputDataValueNotAllowedForDataTypeExc](../datalidator/blueprints/exc/InputDataValueNotAllowedForDataTypeExc.py))*
            - **InputDataNotUnsubclassableExc** *([datalidator.blueprints.exc.InputDataNotUnsubclassableExc](../datalidator/blueprints/exc/InputDataNotUnsubclassableExc.py))*
            - **InputDataTypeInBlocklistExc** *([datalidator.blueprints.exc.InputDataTypeInBlocklistExc](../datalidator/blueprints/exc/InputDataTypeInBlocklistExc.py))*
        - **UnexpectedOutputDataTypeExc** *([datalidator.blueprints.exc.UnexpectedOutputDataTypeExc](../datalidator/blueprints/exc/UnexpectedOutputDataTypeExc.py))*
        - **UnexpectedExceptionRaisedInBlueprintExc** *([datalidator.blueprints.exc.UnexpectedExceptionRaisedInBlueprintExc](../datalidator/blueprints/exc/UnexpectedExceptionRaisedInBlueprintExc.py))*
    

## Errors
- **DatalidatorError** *([datalidator.exc.err.DatalidatorError](../datalidator/exc/err/DatalidatorError.py))*
    - **ThisShouldNeverHappenError** *([datalidator.exc.err.ThisShouldNeverHappenError](../datalidator/exc/err/ThisShouldNeverHappenError.py))*
    - **ValidatorError** *([datalidator.validators.exc.err.ValidatorError](../datalidator/validators/exc/err/ValidatorError.py))*
        - **InvalidValidatorConfigError** *([datalidator.validators.exc.err.InvalidValidatorConfigError](../datalidator/validators/exc/err/InvalidValidatorConfigError.py))*
            - **RegexCompilationFailedInValidatorError** *([datalidator.validators.exc.err.RegexCompilationFailedInValidatorError](../datalidator/validators/exc/err/RegexCompilationFailedInValidatorError.py))*
    - **FilterError** *([datalidator.filters.exc.err.FilterError](../datalidator/filters/exc/err/FilterError.py))*
        - **InvalidFilterConfigError** *([datalidator.filters.exc.err.InvalidFilterConfigError](../datalidator/filters/exc/err/InvalidFilterConfigError.py))*
            - **RegexCompilationFailedInFilterError** *([datalidator.filters.exc.err.RegexCompilationFailedInFilterError](../datalidator/filters/exc/err/RegexCompilationFailedInFilterError.py))*
    - **BlueprintError** *([datalidator.blueprints.exc.err.BlueprintError](../datalidator/blueprints/exc/err/BlueprintError.py))*
        - **InvalidBlueprintConfigError** *([datalidator.blueprints.exc.err.InvalidBlueprintConfigError](../datalidator/blueprints/exc/err/InvalidBlueprintConfigError.py))*
