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


import os.path
import sys
__TESTS_DIR = os.path.dirname(os.path.realpath(__file__))  
__MODULE_DIR = os.path.realpath(os.path.join(__TESTS_DIR, "../.."))  
if __TESTS_DIR not in sys.path:  
    sys.path.insert(0, __TESTS_DIR)  
if __MODULE_DIR not in sys.path:  
    sys.path.insert(0, __MODULE_DIR)  

import theoretical_testutils
import pytest
import datetime
import zoneinfo
from datalidator.blueprints.ParsingMode import ParsingMode
from datalidator.blueprints.impl.DatetimeBlueprint import DatetimeBlueprint
from datalidator.blueprints.impl.TimeBlueprint import TimeBlueprint
from datalidator.blueprints.exc.InputDataNotConvertibleExc import InputDataNotConvertibleExc
from datalidator.blueprints.exc.InputDataTypeNotInAllowlistExc import InputDataTypeNotInAllowlistExc


current_datetime_naive = datetime.datetime.now()
current_datetime_aware = datetime.datetime.now(datetime.timezone.utc).astimezone(zoneinfo.ZoneInfo("Europe/Prague"))


__TIME_BLUEPRINT_TEST_SUITE = (
    (TimeBlueprint(DatetimeBlueprint(
        additional_datetime_string_formats=("%H:%M:%S",),
        parsing_mode=ParsingMode.MODE_LOOSE
    )), (
        # https://docs.python.org/3/library/datetime.html#datetime.datetime.time
        (current_datetime_naive, current_datetime_naive.time()),
        (current_datetime_aware, current_datetime_aware.time()),
        (datetime.datetime(2012, 2, 29, 6, 50, 20), datetime.time(6, 50, 20)),
        (datetime.datetime(2012, 2, 29, 22, 25, 45), datetime.time(22, 25, 45)),
        (datetime.datetime(2012, 2, 29, 22, 25, 45, 777888), datetime.time(22, 25, 45, 777888)),
        (datetime.datetime(2012, 2, 29, 6, 50, 20, tzinfo=datetime.timezone.utc), datetime.time(6, 50, 20, tzinfo=None)),
        (datetime.datetime(2012, 2, 29, 22, 25, 45, tzinfo=datetime.timezone.utc), datetime.time(22, 25, 45, tzinfo=None)),
        (datetime.datetime(2012, 2, 29, 22, 25, 45, 777888, tzinfo=datetime.timezone.utc), datetime.time(22, 25, 45, 777888, tzinfo=None)),
        (datetime.datetime(2012, 2, 29, 6, 50, 20, tzinfo=zoneinfo.ZoneInfo("Europe/Prague")), datetime.time(6, 50, 20, tzinfo=None)),
        (datetime.datetime(2012, 2, 29, 22, 25, 45, tzinfo=zoneinfo.ZoneInfo("Europe/Prague")), datetime.time(22, 25, 45, tzinfo=None)),
        (datetime.datetime(2012, 2, 29, 22, 25, 45, 777888, tzinfo=zoneinfo.ZoneInfo("Europe/Prague")), datetime.time(22, 25, 45, 777888, tzinfo=None)),
        (datetime.datetime(2012, 2, 29, 6, 50, 20, tzinfo=zoneinfo.ZoneInfo("America/New_York")), datetime.time(6, 50, 20, tzinfo=None)),
        (datetime.datetime(2012, 2, 29, 22, 25, 45, tzinfo=zoneinfo.ZoneInfo("America/New_York")), datetime.time(22, 25, 45, tzinfo=None)),
        (datetime.datetime(2012, 2, 29, 22, 25, 45, 777888, tzinfo=zoneinfo.ZoneInfo("America/New_York")), datetime.time(22, 25, 45, 777888, tzinfo=None)),
        ("2024-02-05", datetime.time(0, 0, 0)),
        ("2024-02-05T02:35:05", datetime.time(2, 35, 5)),
        ("2024-02-05T02:35:05.445566", datetime.time(2, 35, 5, 445566)),
        ("2024-02-05T02:35:05.445566+05:00", datetime.time(2, 35, 5, 445566, tzinfo=None)),
        ("2024-02-05T02:35:05.445566-05:00", datetime.time(2, 35, 5, 445566, tzinfo=None)),
        ("2024-02-05T19:35:05", datetime.time(19, 35, 5)),
        ("2024-02-05T19:35:05.445566", datetime.time(19, 35, 5, 445566)),
        ("2024-02-05T19:35:05.445566+05:00", datetime.time(19, 35, 5, 445566, tzinfo=None)),
        ("2024-02-05T19:35:05.445566-05:00", datetime.time(19, 35, 5, 445566, tzinfo=None)),
        ("08:25:40", datetime.time(8, 25, 40)),
        ("17:59:01", datetime.time(17, 59, 1)),
        (datetime.time(8, 30, 59), datetime.time(8, 30, 59)),
        (datetime.time(8, 30, 59, 889911), datetime.time(8, 30, 59, 889911)),
        (datetime.time(8, 30, 59, 889911, tzinfo=datetime.timezone.utc), datetime.time(8, 30, 59, 889911, tzinfo=None)),
        (datetime.time(8, 30, 59, 889911, tzinfo=zoneinfo.ZoneInfo("Europe/Prague")), datetime.time(8, 30, 59, 889911, tzinfo=None)),
        (datetime.time(8, 30, 59, 889911, tzinfo=zoneinfo.ZoneInfo("America/New_York")), datetime.time(8, 30, 59, 889911, tzinfo=None)),
        (datetime.date(2020, 2, 29), datetime.time(0, 0, 0)),
        (datetime.date(2050, 6, 25), datetime.time(0, 0, 0)),
        ("", InputDataNotConvertibleExc),
        ("hello", InputDataNotConvertibleExc),
        (float("nan"), InputDataNotConvertibleExc),
        (None, InputDataTypeNotInAllowlistExc),
        (zoneinfo.ZoneInfo("Europe/Prague"), InputDataTypeNotInAllowlistExc),
        (datetime.datetime, InputDataTypeNotInAllowlistExc),
        (datetime.time, InputDataTypeNotInAllowlistExc),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc),
    )),
)


@pytest.mark.parametrize(("blueprint", "input_", "output"), theoretical_testutils.test_function_parameter_generator(__TIME_BLUEPRINT_TEST_SUITE))
def test_time_blueprint(blueprint, input_, output):
    theoretical_testutils.perform_test(blueprint, input_, output)


def test_time_blueprint_wrapped_blueprint_instance():
    instance = DatetimeBlueprint()
    assert TimeBlueprint(instance).get_datetime_blueprint() is instance
