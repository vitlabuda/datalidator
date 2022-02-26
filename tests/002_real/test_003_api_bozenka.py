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


import os
import os.path
import sys
if "DATALIDATOR_TESTS_AUTOPATH" in os.environ:
    __TESTS_DIR = os.path.dirname(os.path.realpath(__file__))
    __MODULE_DIR = os.path.realpath(os.path.join(__TESTS_DIR, "../.."))
    if __TESTS_DIR not in sys.path:
        sys.path.insert(0, __TESTS_DIR)
    if __MODULE_DIR not in sys.path:
        sys.path.insert(0, __MODULE_DIR)

import real_testutils
import pytest
import datetime
from datalidator.blueprints.ParsingMode import ParsingMode
from datalidator.blueprints.impl.StringBlueprint import StringBlueprint
from datalidator.blueprints.impl.BooleanBlueprint import BooleanBlueprint
from datalidator.blueprints.impl.FloatBlueprint import FloatBlueprint
from datalidator.blueprints.impl.DatetimeBlueprint import DatetimeBlueprint
from datalidator.blueprints.impl.DateBlueprint import DateBlueprint
from datalidator.blueprints.impl.TimeBlueprint import TimeBlueprint
from datalidator.blueprints.impl.PredefinedDictionaryBlueprint import PredefinedDictionaryBlueprint
from datalidator.blueprints.specialimpl.JSONBlueprint import JSONBlueprint
from datalidator.blueprints.exc.InputDataNotConvertibleExc import InputDataNotConvertibleExc
from datalidator.filters.impl.StringUnicodeNormalizeFilter import StringUnicodeNormalizeFilter
from datalidator.validators.impl.NumberMinimumValueValidator import NumberMinimumValueValidator
from datalidator.validators.impl.NumberMaximumValueValidator import NumberMaximumValueValidator
from datalidator.validators.impl.SequenceIsNotEmptyValidator import SequenceIsNotEmptyValidator
from datalidator.validators.impl.SequenceMaximumLengthValidator import SequenceMaximumLengthValidator
from datalidator.validators.impl.StringContainsNoControlOrSeparatorCharactersValidator import StringContainsNoControlOrSeparatorCharactersValidator


__ESTIMATION_BLUEPRINT = PredefinedDictionaryBlueprint(
    dict_specification={
        "score": FloatBlueprint(
            validators=(
                NumberMinimumValueValidator(0.0),
                NumberMaximumValueValidator(100.0)
            ),
            parsing_mode=ParsingMode.MODE_RATIONAL,
            allow_ieee754_special_values=False
        ),
        "class": StringBlueprint(
            filters=(StringUnicodeNormalizeFilter(normal_form="NFKC"),),
            validators=(
                SequenceIsNotEmptyValidator(),
                SequenceMaximumLengthValidator(50),
                StringContainsNoControlOrSeparatorCharactersValidator(allowed_characters="")
            ),
            parsing_mode=ParsingMode.MODE_STRICT
        )
    },
    ignore_unspecified_keys_in_input=False
)


__BOZENKA_REPORT_DICT_SPECIFICATION = {
    "enabled": BooleanBlueprint(parsing_mode=ParsingMode.MODE_RATIONAL),
    "enabledFrom": TimeBlueprint(
        datetime_blueprint=DatetimeBlueprint(
            additional_datetime_string_formats=("%H:%M",),
            parsing_mode=ParsingMode.MODE_STRICT
        )
    ),
    "enabledTo": TimeBlueprint(
        datetime_blueprint=DatetimeBlueprint(
            additional_datetime_string_formats=("%H:%M",),
            parsing_mode=ParsingMode.MODE_STRICT
        )
    ),
    "date": DateBlueprint(
        datetime_blueprint=DatetimeBlueprint(
            additional_datetime_string_formats=("%d.%m. %Y",),
            parsing_mode=ParsingMode.MODE_STRICT
        )
    ),
    "time": TimeBlueprint(
        datetime_blueprint=DatetimeBlueprint(
            additional_datetime_string_formats=("%H:%M",),
            parsing_mode=ParsingMode.MODE_STRICT
        )
    ),
    "finalEstimation": __ESTIMATION_BLUEPRINT,
    "estimation1": __ESTIMATION_BLUEPRINT,
    "estimation2": __ESTIMATION_BLUEPRINT,
    "estimation3": __ESTIMATION_BLUEPRINT
}


def test_bozenka_api():
    response = real_testutils.make_api_request("https://bozenka.cloud/api.php")

    response_blueprint = JSONBlueprint(
        wrapped_blueprint=PredefinedDictionaryBlueprint(
            dict_specification=__BOZENKA_REPORT_DICT_SPECIFICATION,
            ignore_unspecified_keys_in_input=True
        )
    )

    bozenka_report = response_blueprint.use(response)
    assert bozenka_report.__class__ is dict
    assert bozenka_report["enabled"].__class__ is bool
    assert bozenka_report["enabledFrom"].__class__ is datetime.time
    assert bozenka_report["enabledTo"].__class__ is datetime.time
    assert bozenka_report["date"].__class__ is datetime.date
    assert bozenka_report["time"].__class__ is datetime.time
    for estimation_name in ("finalEstimation", "estimation1", "estimation2", "estimation3"):
        assert bozenka_report[estimation_name].__class__ is dict
        assert bozenka_report[estimation_name]["score"].__class__ is float
        assert bozenka_report[estimation_name]["class"].__class__ is str


def test_bozenka_api_with_invalid_blueprint():
    response = real_testutils.make_api_request("https://bozenka.cloud/api.php")

    response_blueprint = DatetimeBlueprint(parsing_mode=ParsingMode.MODE_STRICT)

    with pytest.raises(InputDataNotConvertibleExc):
        response_blueprint.use(response)
