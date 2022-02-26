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

import locale
locale.setlocale(locale.LC_ALL, "C")  # Some of DatetimeBlueprint's functionality is locale-dependent under certain circumstances!

import theoretical_testutils
import pytest
import datetime
import zoneinfo
from datalidator.blueprints.ParsingMode import ParsingMode
from datalidator.blueprints.impl.DateBlueprint import DateBlueprint
from datalidator.blueprints.impl.DatetimeBlueprint import DatetimeBlueprint
from datalidator.blueprints.exc.InputDataNotConvertibleExc import InputDataNotConvertibleExc
from datalidator.blueprints.exc.InputDataTypeNotInAllowlistExc import InputDataTypeNotInAllowlistExc


current_datetime_naive = datetime.datetime.now()
current_datetime_aware = datetime.datetime.now(datetime.timezone.utc).astimezone(zoneinfo.ZoneInfo("Europe/Prague"))


__DATE_BLUEPRINT_TEST_SUITE = (
    (DateBlueprint(DatetimeBlueprint(parsing_mode=ParsingMode.MODE_LOOSE)), (
        (current_datetime_naive, current_datetime_naive.date()),
        (current_datetime_aware, current_datetime_aware.date()),
        (datetime.datetime(2016, 2, 29, 1, 20, 50), datetime.date(2016, 2, 29)),
        (datetime.datetime(2016, 2, 29, 1, 20, 50, tzinfo=datetime.timezone.utc), datetime.date(2016, 2, 29)),
        (datetime.datetime(2016, 2, 29, 1, 20, 50, tzinfo=zoneinfo.ZoneInfo("Europe/Prague")), datetime.date(2016, 2, 29)),
        (datetime.datetime(2016, 2, 29, 1, 20, 50, tzinfo=zoneinfo.ZoneInfo("America/New_York")), datetime.date(2016, 2, 29)),
        ("2020-12-15", datetime.date(2020, 12, 15)),
        ("2020-12-15T12:30:45", datetime.date(2020, 12, 15)),
        ("2020-12-15T12:30:45+04:00", datetime.date(2020, 12, 15)),
        ("2020-12-15T12:30:45-04:00", datetime.date(2020, 12, 15)),
        (datetime.date(2014, 2, 8), datetime.date(2014, 2, 8)),
        (datetime.date(2020, 2, 29), datetime.date(2020, 2, 29)),
        (datetime.time(15, 45, 50), datetime.date(1900, 1, 1)),
        ("", InputDataNotConvertibleExc),
        ("hello", InputDataNotConvertibleExc),
        (float("nan"), InputDataNotConvertibleExc),
        (None, InputDataTypeNotInAllowlistExc),
        (zoneinfo.ZoneInfo("Europe/Prague"), InputDataTypeNotInAllowlistExc),
        (datetime.datetime, InputDataTypeNotInAllowlistExc),
        (datetime.date, InputDataTypeNotInAllowlistExc),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc),
    )),
)


@pytest.mark.parametrize(("blueprint", "input_", "output"), theoretical_testutils.test_function_parameter_generator(__DATE_BLUEPRINT_TEST_SUITE))
def test_date_blueprint(blueprint, input_, output):
    theoretical_testutils.perform_test(blueprint, input_, output)


def test_date_blueprint_wrapped_blueprint_instance():
    instance = DatetimeBlueprint()
    assert DateBlueprint(instance).get_datetime_blueprint() is instance
