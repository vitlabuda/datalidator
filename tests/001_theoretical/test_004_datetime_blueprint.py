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
import time
import ipaddress
from datalidator.blueprints.ParsingMode import ParsingMode
from datalidator.blueprints.impl.DatetimeBlueprint import DatetimeBlueprint
from datalidator.blueprints.exc.InputDataNotConvertibleExc import InputDataNotConvertibleExc
from datalidator.blueprints.exc.InputDataTypeNotInAllowlistExc import InputDataTypeNotInAllowlistExc
from datalidator.filters.impl.DatetimeAddTimezoneFilter import DatetimeAddTimezoneFilter
from datalidator.filters.impl.DatetimeChangeTimezoneFilter import DatetimeChangeTimezoneFilter
from datalidator.filters.exc.InputDatetimeObjectIsNaiveInFilterExc import InputDatetimeObjectIsNaiveInFilterExc
from datalidator.validators.impl.DatetimeIsAwareValidator import DatetimeIsAwareValidator
from datalidator.validators.impl.DatetimeNotAfterValidator import DatetimeNotAfterValidator
from datalidator.validators.impl.DatetimeNotBeforeValidator import DatetimeNotBeforeValidator
from datalidator.validators.exc.DataValidationFailedExc import DataValidationFailedExc
from datalidator.validators.exc.InputDatetimeObjectIsNaiveInValidatorExc import InputDatetimeObjectIsNaiveInValidatorExc
from datalidator.validators.exc.err.InvalidValidatorConfigError import InvalidValidatorConfigError


current_datetime_naive = datetime.datetime.now()
current_datetime_aware = datetime.datetime.now(datetime.timezone.utc).astimezone(zoneinfo.ZoneInfo("Europe/Prague"))
current_struct_time_utc = time.gmtime()
current_struct_time_localtime = time.localtime()


__DATETIME_BLUEPRINT_TEST_SUITE = (
    (DatetimeBlueprint(parsing_mode=ParsingMode.MODE_LOOSE), (
        (current_datetime_naive, lambda output: (output is not current_datetime_naive) and (output == current_datetime_naive)),
        (current_datetime_aware, lambda output: (output is not current_datetime_aware) and (output == current_datetime_aware)),
        (current_datetime_naive, lambda output: output != current_datetime_aware),
        (current_datetime_aware, lambda output: output != current_datetime_naive),
        (datetime.datetime(2020, 2, 29, 12, 40, 25), datetime.datetime(2020, 2, 29, 12, 40, 25)),
        (datetime.datetime(2020, 2, 29, 12, 40, 25), lambda output: output != datetime.datetime(2020, 2, 29, 12, 40, 25, tzinfo=datetime.timezone.utc)),
        (datetime.datetime(2020, 2, 29, 12, 40, 25, tzinfo=datetime.timezone.utc), lambda output: output != datetime.datetime(2020, 2, 29, 12, 40, 25)),
        (datetime.datetime(2020, 2, 29, 12, 40, 25, tzinfo=datetime.timezone.utc), datetime.datetime(2020, 2, 29, 12, 40, 25, tzinfo=datetime.timezone.utc)),
        (datetime.datetime(2020, 2, 29, 12, 40, 25), lambda output: output != datetime.datetime(2020, 2, 29, 12, 40, 25, tzinfo=zoneinfo.ZoneInfo("Europe/Prague"))),
        (datetime.datetime(2020, 2, 29, 12, 40, 25, tzinfo=zoneinfo.ZoneInfo("Europe/Prague")), lambda output: output != datetime.datetime(2020, 2, 29, 12, 40, 25)),
        (datetime.datetime(2020, 2, 29, 12, 40, 25, tzinfo=zoneinfo.ZoneInfo("Europe/Prague")), datetime.datetime(2020, 2, 29, 12, 40, 25, tzinfo=zoneinfo.ZoneInfo("Europe/Prague"))),
        (datetime.datetime(2020, 2, 29, 12, 40, 25, tzinfo=datetime.timezone.utc), lambda output: output != datetime.datetime(2020, 2, 29, 12, 40, 25, tzinfo=zoneinfo.ZoneInfo("America/New_York"))),
        (datetime.datetime(2020, 2, 29, 12, 40, 25, tzinfo=zoneinfo.ZoneInfo("Europe/Prague")), lambda output: output != datetime.datetime(2020, 2, 29, 12, 40, 25, tzinfo=zoneinfo.ZoneInfo("America/New_York"))),
        (datetime.datetime(1066, 10, 14, 15, 0, 0), datetime.datetime(1066, 10, 14, 15, 0, 0)),
        (datetime.datetime(8500, 10, 14, 15, 0, 0), datetime.datetime(8500, 10, 14, 15, 0, 0)),
        (datetime.datetime(1066, 10, 14, 15, 0, 0, tzinfo=datetime.timezone.utc), datetime.datetime(1066, 10, 14, 15, 0, 0, tzinfo=datetime.timezone.utc)),
        (datetime.datetime(8500, 10, 14, 15, 0, 0, tzinfo=datetime.timezone.utc), datetime.datetime(8500, 10, 14, 15, 0, 0, tzinfo=datetime.timezone.utc)),
        (current_struct_time_utc, datetime.datetime.fromtimestamp(time.mktime(current_struct_time_utc), tz=datetime.timezone.utc)),
        (current_struct_time_localtime, datetime.datetime.fromtimestamp(time.mktime(current_struct_time_localtime), tz=datetime.timezone.utc)),
        # Hardcoded time.struct_time objects cannot be tested reliably, because their conversion to datetime.datetime is timezone-dependent.
        (time.struct_time((2020, 1, 1, 1, 1, 1, 1, 1, 1)), lambda output: True),  # This just tests whether the blueprint did not raise an exception.
        (time.struct_time((8020, 1, 1, 1, 1, 1, 1, 1, 1)), lambda output: True),  # This just tests whether the blueprint did not raise an exception.
        (time.struct_time((1066, 1, 1, 1, 1, 1, 1, 1, 1)), InputDataNotConvertibleExc),
        (time.struct_time((150000000, 1, 1, 1, 1, 1, 1, 1, 1)), InputDataNotConvertibleExc),
        (time.struct_time((15000, 1, 1, 1, 1, 1, 1, 1, 1)), InputDataNotConvertibleExc),
        # https://docs.python.org/3/library/datetime.html#datetime.datetime.fromisoformat
        (current_datetime_naive.isoformat(), current_datetime_naive),
        (current_datetime_aware.isoformat(), current_datetime_aware),
        ("2022-01-08T18:38:54.648842", datetime.datetime(2022, 1, 8, 18, 38, 54, 648842)),
        ("2022-01-08x18:38:54.648842", datetime.datetime(2022, 1, 8, 18, 38, 54, 648842)),
        ("2022-01-08\x0018:38:54.648842", datetime.datetime(2022, 1, 8, 18, 38, 54, 648842)),
        ("2011-11", InputDataNotConvertibleExc),
        ("2011-11-04", datetime.datetime(2011, 11, 4, 0, 0, 0)),
        ("201-11-04", InputDataNotConvertibleExc),
        ("20111-11-04", InputDataNotConvertibleExc),
        ("2011-11-04 01", datetime.datetime(2011, 11, 4, 1, 0, 0)),
        ("2011-11-04 01:05", datetime.datetime(2011, 11, 4, 1, 5, 0)),
        ("2011-11-04 01:05:23", datetime.datetime(2011, 11, 4, 1, 5, 23)),
        ("2011-02-29 01:05:23", InputDataNotConvertibleExc),
        ("2012-02-29 01:05:23", datetime.datetime(2012, 2, 29, 1, 5, 23)),
        ("2011-13-01 10:05:50", InputDataNotConvertibleExc),
        ("2011-11-31 01:05:23", InputDataNotConvertibleExc),
        ("2011-01-01 24:05:23", InputDataNotConvertibleExc),
        ("2011-01-01 10:60:23", InputDataNotConvertibleExc),
        ("2011-01-01 10:05:60", InputDataNotConvertibleExc),
        ("\r\n2011-11-04 01:05:23\t", datetime.datetime(2011, 11, 4, 1, 5, 23)),
        ("     2011-11-04 01:05:23  ", datetime.datetime(2011, 11, 4, 1, 5, 23)),
        ("\x002011-11-04 01:05:23", InputDataNotConvertibleExc),
        ("2011-11-04 01:05\x00:23", InputDataNotConvertibleExc),
        ("2011-11-04 01:05:23\x00", datetime.datetime(2011, 11, 4, 1, 5, 23)),  # This works for some reason...
        ("2011-11-04 01:05:23\x00abc", InputDataNotConvertibleExc),  # ... and this does not.
        ("2011-11-04 01:05:23.28", InputDataNotConvertibleExc),
        ("2011-11-04 01:05:23.283", datetime.datetime(2011, 11, 4, 1, 5, 23, 283000)),
        ("2011-11-04 01:05:23.2839", InputDataNotConvertibleExc),
        ("2011-11-04 01:05:23.283999", datetime.datetime(2011, 11, 4, 1, 5, 23, 283999)),
        ("2011-11-04 01:05:23.2839999", InputDataNotConvertibleExc),
        ("2011-11-04+05:30", datetime.datetime(2011, 11, 4, 5, 30, 0)),  # The '+05:30' is not considered a timezone, but 'hour:minute'!!!
        ("2011-11-04 01:05:23+00:00", datetime.datetime(2011, 11, 4, 1, 5, 23, tzinfo=datetime.timezone.utc)),
        ("2011-11-04 01:05:23.283+00:00", datetime.datetime(2011, 11, 4, 1, 5, 23, 283000, tzinfo=datetime.timezone.utc)),
        ("2011-11-04 01:05:23.283999+00:00", datetime.datetime(2011, 11, 4, 1, 5, 23, 283999, tzinfo=datetime.timezone.utc)),
        ("2011-11-04 01:05:23-00:00", datetime.datetime(2011, 11, 4, 1, 5, 23, tzinfo=datetime.timezone.utc)),
        ("2011-11-04 01:05:23.283-00:00", datetime.datetime(2011, 11, 4, 1, 5, 23, 283000, tzinfo=datetime.timezone.utc)),
        ("2011-11-04 01:05:23.283999-00:00", datetime.datetime(2011, 11, 4, 1, 5, 23, 283999, tzinfo=datetime.timezone.utc)),
        ("2011-11-04 01:05:23+05:30", datetime.datetime(2011, 11, 4, 1, 5, 23, tzinfo=datetime.timezone(datetime.timedelta(seconds=19800)))),
        ("2011-11-04 01:05:23.283+05:30", datetime.datetime(2011, 11, 4, 1, 5, 23, 283000, tzinfo=datetime.timezone(datetime.timedelta(seconds=19800)))),
        ("2011-11-04 01:05:23.283999+05:30", datetime.datetime(2011, 11, 4, 1, 5, 23, 283999, tzinfo=datetime.timezone(datetime.timedelta(seconds=19800)))),
        ("2011-11-04 01:05:23-05:30", datetime.datetime(2011, 11, 4, 1, 5, 23, tzinfo=datetime.timezone(datetime.timedelta(seconds=-19800)))),
        ("2011-11-04 01:05:23.283-05:30", datetime.datetime(2011, 11, 4, 1, 5, 23, 283000, tzinfo=datetime.timezone(datetime.timedelta(seconds=-19800)))),
        ("2011-11-04 01:05:23.283999-05:30", datetime.datetime(2011, 11, 4, 1, 5, 23, 283999, tzinfo=datetime.timezone(datetime.timedelta(seconds=-19800)))),
        ("2011-11-04 01:05:23+05:30:10", datetime.datetime(2011, 11, 4, 1, 5, 23, tzinfo=datetime.timezone(datetime.timedelta(seconds=19810)))),
        ("2011-11-04 01:05:23.283+05:30:10.123", InputDataNotConvertibleExc),
        ("2011-11-04 01:05:23.283999+05:30:10.123456", datetime.datetime(2011, 11, 4, 1, 5, 23, 283999, tzinfo=datetime.timezone(datetime.timedelta(seconds=19810, microseconds=123456)))),
        ("2011-11-04 01:05:23-05:30:10", datetime.datetime(2011, 11, 4, 1, 5, 23, tzinfo=datetime.timezone(datetime.timedelta(seconds=-19810)))),
        ("2011-11-04 01:05:23.283-05:30:10.123", InputDataNotConvertibleExc),
        ("2011-11-04 01:05:23.283999-05:30:10.123456", datetime.datetime(2011, 11, 4, 1, 5, 23, 283999, tzinfo=datetime.timezone(datetime.timedelta(seconds=-19810, microseconds=-123456)))),
        ("15.02.2021 04:50:45", InputDataNotConvertibleExc),
        ("02/15/2021 04:50:45", InputDataNotConvertibleExc),
        ("02/15/2021 04:50 am", InputDataNotConvertibleExc),
        ("0", datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)),
        ("-0", datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)),
        ("\r\n0000  \t", datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)),
        ("0.0", datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)),
        ("-0.0", datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)),
        ("\r\n0000.000  \t", datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)),
        ("\x001204295445", InputDataNotConvertibleExc),
        ("1204295445", datetime.datetime(2008, 2, 29, 14, 30, 45, 0, tzinfo=datetime.timezone.utc)),
        ("1204295445.123", datetime.datetime(2008, 2, 29, 14, 30, 45, 123000, tzinfo=datetime.timezone.utc)),
        ("1204295445.123456", datetime.datetime(2008, 2, 29, 14, 30, 45, 123456, tzinfo=datetime.timezone.utc)),
        ("-5000000000", datetime.datetime(1811, 7, 23, 15, 6, 40, tzinfo=datetime.timezone.utc)),
        ("-5000000000.1", datetime.datetime(1811, 7, 23, 15, 6, 39, 900000, tzinfo=datetime.timezone.utc)),
        ("-100000000000.1", InputDataNotConvertibleExc),  # ValueError
        ("-100000000000000000", InputDataNotConvertibleExc),  # OSError
        ("-100000000000000000000", InputDataNotConvertibleExc),  # OverflowError
        ("100000000000", datetime.datetime(5138, 11, 16, 9, 46, 40, tzinfo=datetime.timezone.utc)),
        ("100000000000000.1", InputDataNotConvertibleExc),  # ValueError
        ("100000000000000000", InputDataNotConvertibleExc),  # OSError
        ("100000000000000000000", InputDataNotConvertibleExc),  # OverflowError
        ("", InputDataNotConvertibleExc),
        ("abcdefxyz", InputDataNotConvertibleExc),
        ("\x00", InputDataNotConvertibleExc),
        ("řeřicha", InputDataNotConvertibleExc),
        ("nan", InputDataNotConvertibleExc),
        ("-inf", InputDataNotConvertibleExc),
        (0, datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)),
        (-0, datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)),
        (0.0, datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)),
        (-0.0, datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)),
        (1204295445, datetime.datetime(2008, 2, 29, 14, 30, 45, 0, tzinfo=datetime.timezone.utc)),
        (1204295445.123, datetime.datetime(2008, 2, 29, 14, 30, 45, 123000, tzinfo=datetime.timezone.utc)),
        (1204295445.123456, datetime.datetime(2008, 2, 29, 14, 30, 45, 123456, tzinfo=datetime.timezone.utc)),
        (-5000000000, datetime.datetime(1811, 7, 23, 15, 6, 40, tzinfo=datetime.timezone.utc)),
        (-5000000000.1, datetime.datetime(1811, 7, 23, 15, 6, 39, 900000, tzinfo=datetime.timezone.utc)),
        (-100000000000.1, InputDataNotConvertibleExc),  # ValueError
        (-100000000000000000, InputDataNotConvertibleExc),  # OSError
        (-100000000000000000000, InputDataNotConvertibleExc),  # OverflowError
        (100000000000, datetime.datetime(5138, 11, 16, 9, 46, 40, tzinfo=datetime.timezone.utc)),
        (100000000000000.1, InputDataNotConvertibleExc),  # ValueError
        (100000000000000000, InputDataNotConvertibleExc),  # OSError
        (100000000000000000000, InputDataNotConvertibleExc),  # OverflowError
        (float("nan"), InputDataNotConvertibleExc),
        (float("-inf"), InputDataNotConvertibleExc),
        (datetime.date(100, 2, 2), datetime.datetime(100, 2, 2, 0, 0, 0)),
        (datetime.date(2012, 2, 29), datetime.datetime(2012, 2, 29, 0, 0, 0)),
        (datetime.date(8000, 2, 2), datetime.datetime(8000, 2, 2, 0, 0, 0)),
        (datetime.time(3, 59, 45), datetime.datetime(1900, 1, 1, 3, 59, 45)),
        (datetime.time(23, 59, 45), datetime.datetime(1900, 1, 1, 23, 59, 45)),
        (datetime.time(23, 59, 45, tzinfo=datetime.timezone.utc), datetime.datetime(1900, 1, 1, 23, 59, 45, tzinfo=datetime.timezone.utc)),
        (datetime.time(23, 59, 45), lambda output: output != datetime.datetime(1900, 1, 1, 23, 59, 45, tzinfo=datetime.timezone.utc)),
        (datetime.time(23, 59, 45, tzinfo=datetime.timezone.utc), lambda output: output != datetime.datetime(1900, 1, 1, 23, 59, 45)),
        (datetime.time(23, 59, 45, tzinfo=zoneinfo.ZoneInfo("Europe/Prague")), datetime.datetime(1900, 1, 1, 23, 59, 45, tzinfo=zoneinfo.ZoneInfo("Europe/Prague"))),
        (datetime.time(23, 59, 45), lambda output: output != datetime.datetime(1900, 1, 1, 23, 59, 45, tzinfo=zoneinfo.ZoneInfo("Europe/Prague"))),
        (datetime.time(23, 59, 45, tzinfo=zoneinfo.ZoneInfo("Europe/Prague")), lambda output: output != datetime.datetime(1900, 1, 1, 23, 59, 45)),
        (int, InputDataTypeNotInAllowlistExc),
        ([], InputDataTypeNotInAllowlistExc),
        ({}, InputDataTypeNotInAllowlistExc),
        (ipaddress.ip_address("127.0.0.1"), InputDataTypeNotInAllowlistExc),
        (ipaddress.ip_network("127.0.0.0/8"), InputDataTypeNotInAllowlistExc),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc)
    )),
    (DatetimeBlueprint(parsing_mode=ParsingMode.MODE_RATIONAL), (
        (current_datetime_naive, lambda output: (output is not current_datetime_naive) and (output == current_datetime_naive)),
        (current_datetime_aware, lambda output: (output is not current_datetime_aware) and (output == current_datetime_aware)),
        (current_datetime_naive, lambda output: output != current_datetime_aware),
        (current_datetime_aware, lambda output: output != current_datetime_naive),
        (datetime.datetime(2020, 2, 29, 12, 40, 25), datetime.datetime(2020, 2, 29, 12, 40, 25)),
        (datetime.datetime(2020, 2, 29, 12, 40, 25), lambda output: output != datetime.datetime(2020, 2, 29, 12, 40, 25, tzinfo=datetime.timezone.utc)),
        (datetime.datetime(2020, 2, 29, 12, 40, 25, tzinfo=datetime.timezone.utc), lambda output: output != datetime.datetime(2020, 2, 29, 12, 40, 25)),
        (datetime.datetime(2020, 2, 29, 12, 40, 25, tzinfo=datetime.timezone.utc), datetime.datetime(2020, 2, 29, 12, 40, 25, tzinfo=datetime.timezone.utc)),
        (datetime.datetime(2020, 2, 29, 12, 40, 25), lambda output: output != datetime.datetime(2020, 2, 29, 12, 40, 25, tzinfo=zoneinfo.ZoneInfo("Europe/Prague"))),
        (datetime.datetime(2020, 2, 29, 12, 40, 25, tzinfo=zoneinfo.ZoneInfo("Europe/Prague")), lambda output: output != datetime.datetime(2020, 2, 29, 12, 40, 25)),
        (datetime.datetime(2020, 2, 29, 12, 40, 25, tzinfo=zoneinfo.ZoneInfo("Europe/Prague")), datetime.datetime(2020, 2, 29, 12, 40, 25, tzinfo=zoneinfo.ZoneInfo("Europe/Prague"))),
        (datetime.datetime(2020, 2, 29, 12, 40, 25, tzinfo=datetime.timezone.utc), lambda output: output != datetime.datetime(2020, 2, 29, 12, 40, 25, tzinfo=zoneinfo.ZoneInfo("America/New_York"))),
        (datetime.datetime(2020, 2, 29, 12, 40, 25, tzinfo=zoneinfo.ZoneInfo("Europe/Prague")), lambda output: output != datetime.datetime(2020, 2, 29, 12, 40, 25, tzinfo=zoneinfo.ZoneInfo("America/New_York"))),
        (datetime.datetime(1066, 10, 14, 15, 0, 0), datetime.datetime(1066, 10, 14, 15, 0, 0)),
        (datetime.datetime(8500, 10, 14, 15, 0, 0), datetime.datetime(8500, 10, 14, 15, 0, 0)),
        (datetime.datetime(1066, 10, 14, 15, 0, 0, tzinfo=datetime.timezone.utc), datetime.datetime(1066, 10, 14, 15, 0, 0, tzinfo=datetime.timezone.utc)),
        (datetime.datetime(8500, 10, 14, 15, 0, 0, tzinfo=datetime.timezone.utc), datetime.datetime(8500, 10, 14, 15, 0, 0, tzinfo=datetime.timezone.utc)),
        (current_struct_time_utc, datetime.datetime.fromtimestamp(time.mktime(current_struct_time_utc), tz=datetime.timezone.utc)),
        (current_struct_time_localtime, datetime.datetime.fromtimestamp(time.mktime(current_struct_time_localtime), tz=datetime.timezone.utc)),
        # Hardcoded time.struct_time objects cannot be tested reliably, because their conversion to datetime.datetime is timezone-dependent.
        (time.struct_time((2020, 1, 1, 1, 1, 1, 1, 1, 1)), lambda output: True),  # This just tests whether the blueprint did not raise an exception.
        (time.struct_time((8020, 1, 1, 1, 1, 1, 1, 1, 1)), lambda output: True),  # This just tests whether the blueprint did not raise an exception.
        (time.struct_time((1066, 1, 1, 1, 1, 1, 1, 1, 1)), InputDataNotConvertibleExc),
        (time.struct_time((150000000, 1, 1, 1, 1, 1, 1, 1, 1)), InputDataNotConvertibleExc),
        (time.struct_time((15000, 1, 1, 1, 1, 1, 1, 1, 1)), InputDataNotConvertibleExc),
        # https://docs.python.org/3/library/datetime.html#datetime.datetime.fromisoformat
        (current_datetime_naive.isoformat(), current_datetime_naive),
        (current_datetime_aware.isoformat(), current_datetime_aware),
        ("2022-01-08T18:38:54.648842", datetime.datetime(2022, 1, 8, 18, 38, 54, 648842)),
        ("2022-01-08x18:38:54.648842", datetime.datetime(2022, 1, 8, 18, 38, 54, 648842)),
        ("2022-01-08\x0018:38:54.648842", datetime.datetime(2022, 1, 8, 18, 38, 54, 648842)),
        ("2011-11", InputDataNotConvertibleExc),
        ("2011-11-04", datetime.datetime(2011, 11, 4, 0, 0, 0)),
        ("201-11-04", InputDataNotConvertibleExc),
        ("20111-11-04", InputDataNotConvertibleExc),
        ("2011-11-04 01", datetime.datetime(2011, 11, 4, 1, 0, 0)),
        ("2011-11-04 01:05", datetime.datetime(2011, 11, 4, 1, 5, 0)),
        ("2011-11-04 01:05:23", datetime.datetime(2011, 11, 4, 1, 5, 23)),
        ("2011-02-29 01:05:23", InputDataNotConvertibleExc),
        ("2012-02-29 01:05:23", datetime.datetime(2012, 2, 29, 1, 5, 23)),
        ("2011-13-01 10:05:50", InputDataNotConvertibleExc),
        ("2011-11-31 01:05:23", InputDataNotConvertibleExc),
        ("2011-01-01 24:05:23", InputDataNotConvertibleExc),
        ("2011-01-01 10:60:23", InputDataNotConvertibleExc),
        ("2011-01-01 10:05:60", InputDataNotConvertibleExc),
        ("\r\n2011-11-04 01:05:23\t", datetime.datetime(2011, 11, 4, 1, 5, 23)),
        ("     2011-11-04 01:05:23  ", datetime.datetime(2011, 11, 4, 1, 5, 23)),
        ("\x002011-11-04 01:05:23", InputDataNotConvertibleExc),
        ("2011-11-04 01:05\x00:23", InputDataNotConvertibleExc),
        ("2011-11-04 01:05:23\x00", datetime.datetime(2011, 11, 4, 1, 5, 23)),  # This works for some reason...
        ("2011-11-04 01:05:23\x00abc", InputDataNotConvertibleExc),  # ... and this does not.
        ("2011-11-04 01:05:23.28", InputDataNotConvertibleExc),
        ("2011-11-04 01:05:23.283", datetime.datetime(2011, 11, 4, 1, 5, 23, 283000)),
        ("2011-11-04 01:05:23.2839", InputDataNotConvertibleExc),
        ("2011-11-04 01:05:23.283999", datetime.datetime(2011, 11, 4, 1, 5, 23, 283999)),
        ("2011-11-04 01:05:23.2839999", InputDataNotConvertibleExc),
        ("2011-11-04+05:30", datetime.datetime(2011, 11, 4, 5, 30, 0)),  # The '+05:30' is not considered a timezone, but 'hour:minute'!!!
        ("2011-11-04 01:05:23+00:00", datetime.datetime(2011, 11, 4, 1, 5, 23, tzinfo=datetime.timezone.utc)),
        ("2011-11-04 01:05:23.283+00:00", datetime.datetime(2011, 11, 4, 1, 5, 23, 283000, tzinfo=datetime.timezone.utc)),
        ("2011-11-04 01:05:23.283999+00:00", datetime.datetime(2011, 11, 4, 1, 5, 23, 283999, tzinfo=datetime.timezone.utc)),
        ("2011-11-04 01:05:23-00:00", datetime.datetime(2011, 11, 4, 1, 5, 23, tzinfo=datetime.timezone.utc)),
        ("2011-11-04 01:05:23.283-00:00", datetime.datetime(2011, 11, 4, 1, 5, 23, 283000, tzinfo=datetime.timezone.utc)),
        ("2011-11-04 01:05:23.283999-00:00", datetime.datetime(2011, 11, 4, 1, 5, 23, 283999, tzinfo=datetime.timezone.utc)),
        ("2011-11-04 01:05:23+05:30", datetime.datetime(2011, 11, 4, 1, 5, 23, tzinfo=datetime.timezone(datetime.timedelta(seconds=19800)))),
        ("2011-11-04 01:05:23.283+05:30", datetime.datetime(2011, 11, 4, 1, 5, 23, 283000, tzinfo=datetime.timezone(datetime.timedelta(seconds=19800)))),
        ("2011-11-04 01:05:23.283999+05:30", datetime.datetime(2011, 11, 4, 1, 5, 23, 283999, tzinfo=datetime.timezone(datetime.timedelta(seconds=19800)))),
        ("2011-11-04 01:05:23-05:30", datetime.datetime(2011, 11, 4, 1, 5, 23, tzinfo=datetime.timezone(datetime.timedelta(seconds=-19800)))),
        ("2011-11-04 01:05:23.283-05:30", datetime.datetime(2011, 11, 4, 1, 5, 23, 283000, tzinfo=datetime.timezone(datetime.timedelta(seconds=-19800)))),
        ("2011-11-04 01:05:23.283999-05:30", datetime.datetime(2011, 11, 4, 1, 5, 23, 283999, tzinfo=datetime.timezone(datetime.timedelta(seconds=-19800)))),
        ("2011-11-04 01:05:23+05:30:10", datetime.datetime(2011, 11, 4, 1, 5, 23, tzinfo=datetime.timezone(datetime.timedelta(seconds=19810)))),
        ("2011-11-04 01:05:23.283+05:30:10.123", InputDataNotConvertibleExc),
        ("2011-11-04 01:05:23.283999+05:30:10.123456", datetime.datetime(2011, 11, 4, 1, 5, 23, 283999, tzinfo=datetime.timezone(datetime.timedelta(seconds=19810, microseconds=123456)))),
        ("2011-11-04 01:05:23-05:30:10", datetime.datetime(2011, 11, 4, 1, 5, 23, tzinfo=datetime.timezone(datetime.timedelta(seconds=-19810)))),
        ("2011-11-04 01:05:23.283-05:30:10.123", InputDataNotConvertibleExc),
        ("2011-11-04 01:05:23.283999-05:30:10.123456", datetime.datetime(2011, 11, 4, 1, 5, 23, 283999, tzinfo=datetime.timezone(datetime.timedelta(seconds=-19810, microseconds=-123456)))),
        ("15.02.2021 04:50:45", InputDataNotConvertibleExc),
        ("02/15/2021 04:50:45", InputDataNotConvertibleExc),
        ("02/15/2021 04:50 am", InputDataNotConvertibleExc),
        ("0", datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)),
        ("-0", datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)),
        ("\r\n0000  \t", datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)),
        ("0.0", datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)),
        ("-0.0", datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)),
        ("\r\n0000.000  \t", datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)),
        ("\x001204295445", InputDataNotConvertibleExc),
        ("1204295445", datetime.datetime(2008, 2, 29, 14, 30, 45, 0, tzinfo=datetime.timezone.utc)),
        ("1204295445.123", datetime.datetime(2008, 2, 29, 14, 30, 45, 123000, tzinfo=datetime.timezone.utc)),
        ("1204295445.123456", datetime.datetime(2008, 2, 29, 14, 30, 45, 123456, tzinfo=datetime.timezone.utc)),
        ("-5000000000", datetime.datetime(1811, 7, 23, 15, 6, 40, tzinfo=datetime.timezone.utc)),
        ("-5000000000.1", datetime.datetime(1811, 7, 23, 15, 6, 39, 900000, tzinfo=datetime.timezone.utc)),
        ("-100000000000.1", InputDataNotConvertibleExc),  # ValueError
        ("-100000000000000000", InputDataNotConvertibleExc),  # OSError
        ("-100000000000000000000", InputDataNotConvertibleExc),  # OverflowError
        ("100000000000", datetime.datetime(5138, 11, 16, 9, 46, 40, tzinfo=datetime.timezone.utc)),
        ("100000000000000.1", InputDataNotConvertibleExc),  # ValueError
        ("100000000000000000", InputDataNotConvertibleExc),  # OSError
        ("100000000000000000000", InputDataNotConvertibleExc),  # OverflowError
        ("", InputDataNotConvertibleExc),
        ("abcdefxyz", InputDataNotConvertibleExc),
        ("\x00", InputDataNotConvertibleExc),
        ("řeřicha", InputDataNotConvertibleExc),
        ("nan", InputDataNotConvertibleExc),
        ("-inf", InputDataNotConvertibleExc),
        (0, datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)),
        (-0, datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)),
        (0.0, datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)),
        (-0.0, datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)),
        (1204295445, datetime.datetime(2008, 2, 29, 14, 30, 45, 0, tzinfo=datetime.timezone.utc)),
        (1204295445.123, datetime.datetime(2008, 2, 29, 14, 30, 45, 123000, tzinfo=datetime.timezone.utc)),
        (1204295445.123456, datetime.datetime(2008, 2, 29, 14, 30, 45, 123456, tzinfo=datetime.timezone.utc)),
        (-5000000000, datetime.datetime(1811, 7, 23, 15, 6, 40, tzinfo=datetime.timezone.utc)),
        (-5000000000.1, datetime.datetime(1811, 7, 23, 15, 6, 39, 900000, tzinfo=datetime.timezone.utc)),
        (-100000000000.1, InputDataNotConvertibleExc),  # ValueError
        (-100000000000000000, InputDataNotConvertibleExc),  # OSError
        (-100000000000000000000, InputDataNotConvertibleExc),  # OverflowError
        (100000000000, datetime.datetime(5138, 11, 16, 9, 46, 40, tzinfo=datetime.timezone.utc)),
        (100000000000000.1, InputDataNotConvertibleExc),  # ValueError
        (100000000000000000, InputDataNotConvertibleExc),  # OSError
        (100000000000000000000, InputDataNotConvertibleExc),  # OverflowError
        (float("nan"), InputDataNotConvertibleExc),
        (float("-inf"), InputDataNotConvertibleExc),
        (datetime.date(100, 2, 2), InputDataTypeNotInAllowlistExc),
        (datetime.date(2012, 2, 29), InputDataTypeNotInAllowlistExc),
        (datetime.date(8000, 2, 2), InputDataTypeNotInAllowlistExc),
        (datetime.time(3, 59, 45), InputDataTypeNotInAllowlistExc),
        (datetime.time(23, 59, 45), InputDataTypeNotInAllowlistExc),
        (datetime.time(23, 59, 45, tzinfo=datetime.timezone.utc), InputDataTypeNotInAllowlistExc),
        (datetime.time(23, 59, 45, tzinfo=zoneinfo.ZoneInfo("Europe/Prague")), InputDataTypeNotInAllowlistExc),
        (int, InputDataTypeNotInAllowlistExc),
        ([], InputDataTypeNotInAllowlistExc),
        ({}, InputDataTypeNotInAllowlistExc),
        (ipaddress.ip_address("127.0.0.1"), InputDataTypeNotInAllowlistExc),
        (ipaddress.ip_network("127.0.0.0/8"), InputDataTypeNotInAllowlistExc),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc)
    )),
    (DatetimeBlueprint(parsing_mode=ParsingMode.MODE_STRICT), (
        (current_datetime_naive, lambda output: (output is not current_datetime_naive) and (output == current_datetime_naive)),
        (current_datetime_aware, lambda output: (output is not current_datetime_aware) and (output == current_datetime_aware)),
        (current_datetime_naive, lambda output: output != current_datetime_aware),
        (current_datetime_aware, lambda output: output != current_datetime_naive),
        (datetime.datetime(2020, 2, 29, 12, 40, 25), datetime.datetime(2020, 2, 29, 12, 40, 25)),
        (datetime.datetime(2020, 2, 29, 12, 40, 25), lambda output: output != datetime.datetime(2020, 2, 29, 12, 40, 25, tzinfo=datetime.timezone.utc)),
        (datetime.datetime(2020, 2, 29, 12, 40, 25, tzinfo=datetime.timezone.utc), lambda output: output != datetime.datetime(2020, 2, 29, 12, 40, 25)),
        (datetime.datetime(2020, 2, 29, 12, 40, 25, tzinfo=datetime.timezone.utc), datetime.datetime(2020, 2, 29, 12, 40, 25, tzinfo=datetime.timezone.utc)),
        (datetime.datetime(2020, 2, 29, 12, 40, 25), lambda output: output != datetime.datetime(2020, 2, 29, 12, 40, 25, tzinfo=zoneinfo.ZoneInfo("Europe/Prague"))),
        (datetime.datetime(2020, 2, 29, 12, 40, 25, tzinfo=zoneinfo.ZoneInfo("Europe/Prague")), lambda output: output != datetime.datetime(2020, 2, 29, 12, 40, 25)),
        (datetime.datetime(2020, 2, 29, 12, 40, 25, tzinfo=zoneinfo.ZoneInfo("Europe/Prague")), datetime.datetime(2020, 2, 29, 12, 40, 25, tzinfo=zoneinfo.ZoneInfo("Europe/Prague"))),
        (datetime.datetime(2020, 2, 29, 12, 40, 25, tzinfo=datetime.timezone.utc), lambda output: output != datetime.datetime(2020, 2, 29, 12, 40, 25, tzinfo=zoneinfo.ZoneInfo("America/New_York"))),
        (datetime.datetime(2020, 2, 29, 12, 40, 25, tzinfo=zoneinfo.ZoneInfo("Europe/Prague")), lambda output: output != datetime.datetime(2020, 2, 29, 12, 40, 25, tzinfo=zoneinfo.ZoneInfo("America/New_York"))),
        (datetime.datetime(1066, 10, 14, 15, 0, 0), datetime.datetime(1066, 10, 14, 15, 0, 0)),
        (datetime.datetime(8500, 10, 14, 15, 0, 0), datetime.datetime(8500, 10, 14, 15, 0, 0)),
        (datetime.datetime(1066, 10, 14, 15, 0, 0, tzinfo=datetime.timezone.utc), datetime.datetime(1066, 10, 14, 15, 0, 0, tzinfo=datetime.timezone.utc)),
        (datetime.datetime(8500, 10, 14, 15, 0, 0, tzinfo=datetime.timezone.utc), datetime.datetime(8500, 10, 14, 15, 0, 0, tzinfo=datetime.timezone.utc)),
        (current_struct_time_utc, datetime.datetime.fromtimestamp(time.mktime(current_struct_time_utc), tz=datetime.timezone.utc)),
        (current_struct_time_localtime, datetime.datetime.fromtimestamp(time.mktime(current_struct_time_localtime), tz=datetime.timezone.utc)),
        # Hardcoded time.struct_time objects cannot be tested reliably, because their conversion to datetime.datetime is timezone-dependent.
        (time.struct_time((2020, 1, 1, 1, 1, 1, 1, 1, 1)), lambda output: True),  # This just tests whether the blueprint did not raise an exception.
        (time.struct_time((8020, 1, 1, 1, 1, 1, 1, 1, 1)), lambda output: True),  # This just tests whether the blueprint did not raise an exception.
        (time.struct_time((1066, 1, 1, 1, 1, 1, 1, 1, 1)), InputDataNotConvertibleExc),
        (time.struct_time((150000000, 1, 1, 1, 1, 1, 1, 1, 1)), InputDataNotConvertibleExc),
        (time.struct_time((15000, 1, 1, 1, 1, 1, 1, 1, 1)), InputDataNotConvertibleExc),
        # https://docs.python.org/3/library/datetime.html#datetime.datetime.fromisoformat
        (current_datetime_naive.isoformat(), current_datetime_naive),
        (current_datetime_aware.isoformat(), current_datetime_aware),
        ("2022-01-08T18:38:54.648842", datetime.datetime(2022, 1, 8, 18, 38, 54, 648842)),
        ("2022-01-08x18:38:54.648842", datetime.datetime(2022, 1, 8, 18, 38, 54, 648842)),
        ("2022-01-08\x0018:38:54.648842", datetime.datetime(2022, 1, 8, 18, 38, 54, 648842)),
        ("2011-11", InputDataNotConvertibleExc),
        ("2011-11-04", datetime.datetime(2011, 11, 4, 0, 0, 0)),
        ("201-11-04", InputDataNotConvertibleExc),
        ("20111-11-04", InputDataNotConvertibleExc),
        ("2011-11-04 01", datetime.datetime(2011, 11, 4, 1, 0, 0)),
        ("2011-11-04 01:05", datetime.datetime(2011, 11, 4, 1, 5, 0)),
        ("2011-11-04 01:05:23", datetime.datetime(2011, 11, 4, 1, 5, 23)),
        ("2011-02-29 01:05:23", InputDataNotConvertibleExc),
        ("2012-02-29 01:05:23", datetime.datetime(2012, 2, 29, 1, 5, 23)),
        ("2011-13-01 10:05:50", InputDataNotConvertibleExc),
        ("2011-11-31 01:05:23", InputDataNotConvertibleExc),
        ("2011-01-01 24:05:23", InputDataNotConvertibleExc),
        ("2011-01-01 10:60:23", InputDataNotConvertibleExc),
        ("2011-01-01 10:05:60", InputDataNotConvertibleExc),
        ("\r\n2011-11-04 01:05:23\t", datetime.datetime(2011, 11, 4, 1, 5, 23)),
        ("     2011-11-04 01:05:23  ", datetime.datetime(2011, 11, 4, 1, 5, 23)),
        ("\x002011-11-04 01:05:23", InputDataNotConvertibleExc),
        ("2011-11-04 01:05\x00:23", InputDataNotConvertibleExc),
        ("2011-11-04 01:05:23\x00", datetime.datetime(2011, 11, 4, 1, 5, 23)),  # This works for some reason...
        ("2011-11-04 01:05:23\x00abc", InputDataNotConvertibleExc),  # ... and this does not.
        ("2011-11-04 01:05:23.28", InputDataNotConvertibleExc),
        ("2011-11-04 01:05:23.283", datetime.datetime(2011, 11, 4, 1, 5, 23, 283000)),
        ("2011-11-04 01:05:23.2839", InputDataNotConvertibleExc),
        ("2011-11-04 01:05:23.283999", datetime.datetime(2011, 11, 4, 1, 5, 23, 283999)),
        ("2011-11-04 01:05:23.2839999", InputDataNotConvertibleExc),
        ("2011-11-04+05:30", datetime.datetime(2011, 11, 4, 5, 30, 0)),  # The '+05:30' is not considered a timezone, but 'hour:minute'!!!
        ("2011-11-04 01:05:23+00:00", datetime.datetime(2011, 11, 4, 1, 5, 23, tzinfo=datetime.timezone.utc)),
        ("2011-11-04 01:05:23.283+00:00", datetime.datetime(2011, 11, 4, 1, 5, 23, 283000, tzinfo=datetime.timezone.utc)),
        ("2011-11-04 01:05:23.283999+00:00", datetime.datetime(2011, 11, 4, 1, 5, 23, 283999, tzinfo=datetime.timezone.utc)),
        ("2011-11-04 01:05:23-00:00", datetime.datetime(2011, 11, 4, 1, 5, 23, tzinfo=datetime.timezone.utc)),
        ("2011-11-04 01:05:23.283-00:00", datetime.datetime(2011, 11, 4, 1, 5, 23, 283000, tzinfo=datetime.timezone.utc)),
        ("2011-11-04 01:05:23.283999-00:00", datetime.datetime(2011, 11, 4, 1, 5, 23, 283999, tzinfo=datetime.timezone.utc)),
        ("2011-11-04 01:05:23+05:30", datetime.datetime(2011, 11, 4, 1, 5, 23, tzinfo=datetime.timezone(datetime.timedelta(seconds=19800)))),
        ("2011-11-04 01:05:23.283+05:30", datetime.datetime(2011, 11, 4, 1, 5, 23, 283000, tzinfo=datetime.timezone(datetime.timedelta(seconds=19800)))),
        ("2011-11-04 01:05:23.283999+05:30", datetime.datetime(2011, 11, 4, 1, 5, 23, 283999, tzinfo=datetime.timezone(datetime.timedelta(seconds=19800)))),
        ("2011-11-04 01:05:23-05:30", datetime.datetime(2011, 11, 4, 1, 5, 23, tzinfo=datetime.timezone(datetime.timedelta(seconds=-19800)))),
        ("2011-11-04 01:05:23.283-05:30", datetime.datetime(2011, 11, 4, 1, 5, 23, 283000, tzinfo=datetime.timezone(datetime.timedelta(seconds=-19800)))),
        ("2011-11-04 01:05:23.283999-05:30", datetime.datetime(2011, 11, 4, 1, 5, 23, 283999, tzinfo=datetime.timezone(datetime.timedelta(seconds=-19800)))),
        ("2011-11-04 01:05:23+05:30:10", datetime.datetime(2011, 11, 4, 1, 5, 23, tzinfo=datetime.timezone(datetime.timedelta(seconds=19810)))),
        ("2011-11-04 01:05:23.283+05:30:10.123", InputDataNotConvertibleExc),
        ("2011-11-04 01:05:23.283999+05:30:10.123456", datetime.datetime(2011, 11, 4, 1, 5, 23, 283999, tzinfo=datetime.timezone(datetime.timedelta(seconds=19810, microseconds=123456)))),
        ("2011-11-04 01:05:23-05:30:10", datetime.datetime(2011, 11, 4, 1, 5, 23, tzinfo=datetime.timezone(datetime.timedelta(seconds=-19810)))),
        ("2011-11-04 01:05:23.283-05:30:10.123", InputDataNotConvertibleExc),
        ("2011-11-04 01:05:23.283999-05:30:10.123456", datetime.datetime(2011, 11, 4, 1, 5, 23, 283999, tzinfo=datetime.timezone(datetime.timedelta(seconds=-19810, microseconds=-123456)))),
        ("15.02.2021 04:50:45", InputDataNotConvertibleExc),
        ("02/15/2021 04:50:45", InputDataNotConvertibleExc),
        ("02/15/2021 04:50 am", InputDataNotConvertibleExc),
        ("0", InputDataNotConvertibleExc),
        ("-0", InputDataNotConvertibleExc),
        ("\r\n0000  \t", InputDataNotConvertibleExc),
        ("0.0", InputDataNotConvertibleExc),
        ("-0.0", InputDataNotConvertibleExc),
        ("\r\n0000.000  \t", InputDataNotConvertibleExc),
        ("\x001204295445", InputDataNotConvertibleExc),
        ("1204295445", InputDataNotConvertibleExc),
        ("1204295445.123", InputDataNotConvertibleExc),
        ("1204295445.123456", InputDataNotConvertibleExc),
        ("-5000000000", InputDataNotConvertibleExc),
        ("-5000000000.1", InputDataNotConvertibleExc),
        ("-100000000000.1", InputDataNotConvertibleExc),  # ValueError
        ("-100000000000000000", InputDataNotConvertibleExc),  # OSError
        ("-100000000000000000000", InputDataNotConvertibleExc),  # OverflowError
        ("100000000000", InputDataNotConvertibleExc),
        ("100000000000000.1", InputDataNotConvertibleExc),  # ValueError
        ("100000000000000000", InputDataNotConvertibleExc),  # OSError
        ("100000000000000000000", InputDataNotConvertibleExc),  # OverflowError
        ("", InputDataNotConvertibleExc),
        ("abcdefxyz", InputDataNotConvertibleExc),
        ("\x00", InputDataNotConvertibleExc),
        ("řeřicha", InputDataNotConvertibleExc),
        ("nan", InputDataNotConvertibleExc),
        ("-inf", InputDataNotConvertibleExc),
        (0, InputDataTypeNotInAllowlistExc),
        (-0, InputDataTypeNotInAllowlistExc),
        (0.0, InputDataTypeNotInAllowlistExc),
        (-0.0, InputDataTypeNotInAllowlistExc),
        (1204295445, InputDataTypeNotInAllowlistExc),
        (1204295445.123, InputDataTypeNotInAllowlistExc),
        (1204295445.123456, InputDataTypeNotInAllowlistExc),
        (-5000000000, InputDataTypeNotInAllowlistExc),
        (-5000000000.1, InputDataTypeNotInAllowlistExc),
        (-100000000000.1, InputDataTypeNotInAllowlistExc),  # ValueError
        (-100000000000000000, InputDataTypeNotInAllowlistExc),  # OSError
        (-100000000000000000000, InputDataTypeNotInAllowlistExc),  # OverflowError
        (100000000000, InputDataTypeNotInAllowlistExc),
        (100000000000000.1, InputDataTypeNotInAllowlistExc),  # ValueError
        (100000000000000000, InputDataTypeNotInAllowlistExc),  # OSError
        (100000000000000000000, InputDataTypeNotInAllowlistExc),  # OverflowError
        (float("nan"), InputDataTypeNotInAllowlistExc),
        (float("-inf"), InputDataTypeNotInAllowlistExc),
        (datetime.date(100, 2, 2), InputDataTypeNotInAllowlistExc),
        (datetime.date(2012, 2, 29), InputDataTypeNotInAllowlistExc),
        (datetime.date(8000, 2, 2), InputDataTypeNotInAllowlistExc),
        (datetime.time(3, 59, 45), InputDataTypeNotInAllowlistExc),
        (datetime.time(23, 59, 45), InputDataTypeNotInAllowlistExc),
        (datetime.time(23, 59, 45, tzinfo=datetime.timezone.utc), InputDataTypeNotInAllowlistExc),
        (datetime.time(23, 59, 45, tzinfo=zoneinfo.ZoneInfo("Europe/Prague")), InputDataTypeNotInAllowlistExc),
        (int, InputDataTypeNotInAllowlistExc),
        ([], InputDataTypeNotInAllowlistExc),
        ({}, InputDataTypeNotInAllowlistExc),
        (ipaddress.ip_address("127.0.0.1"), InputDataTypeNotInAllowlistExc),
        (ipaddress.ip_network("127.0.0.0/8"), InputDataTypeNotInAllowlistExc),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc)
    )),
    (DatetimeBlueprint(additional_datetime_string_formats=(
        "%d.%m.%Y %H:%M:%S",
        "%B %d, %Y %I:%M %p",  # Locale-dependent!
        "%a, %d %b %Y %H:%M:%S %Z"  # Locale-dependent!
    )), (
        ("0", datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)),
        ("-0", datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)),
        ("0.0", datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)),
        ("-0.0", datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)),
        ("\r\n29.02.2012 15:45:50  \t", datetime.datetime(2012, 2, 29, 15, 45, 50)),
        ("   29.02.2012 15:45:50    ", datetime.datetime(2012, 2, 29, 15, 45, 50)),
        ("29.02.2011 15:45:50", InputDataNotConvertibleExc),
        ("29.02.2012 15:45:50", datetime.datetime(2012, 2, 29, 15, 45, 50)),
        ("02.02.2012 05:45:50", datetime.datetime(2012, 2, 2, 5, 45, 50)),
        ("02.02.2012 5:45:50", datetime.datetime(2012, 2, 2, 5, 45, 50)),
        ("2.2.2012 05:45:50", datetime.datetime(2012, 2, 2, 5, 45, 50)),
        ("2.2.2012 5:45:50", datetime.datetime(2012, 2, 2, 5, 45, 50)),
        ("\x0029.02.2012 15:45:50", InputDataNotConvertibleExc),
        ("29.02.2012 15:45:50\x00", InputDataNotConvertibleExc),
        ("29.02.2012 15:45:50\x00abc", InputDataNotConvertibleExc),
        ("20.01.2011 15:45", InputDataNotConvertibleExc),
        ("20.01.2011T15:45:50", InputDataNotConvertibleExc),
        ("January 7, 2020 8:08 PM", datetime.datetime(2020, 1, 7, 20, 8, 0)),
        ("January 7, 2020 08:08 PM", datetime.datetime(2020, 1, 7, 20, 8, 0)),
        ("January 07, 2020 8:08 PM", datetime.datetime(2020, 1, 7, 20, 8, 0)),
        ("Yanuary 7, 2020 8:08 PM", InputDataNotConvertibleExc),
        ("January 7 2020 8:08 PM", InputDataNotConvertibleExc),
        ("January 7, 2020 8:08 XM", InputDataNotConvertibleExc),
        ("January 7, 2020 13:08 PM", InputDataNotConvertibleExc),
        ("February 29, 2021 8:08 PM", InputDataNotConvertibleExc),
        ("Sat, 08 Jan 2022 20:36:07 GMT", datetime.datetime(2022, 1, 8, 20, 36, 7)),  # Unfortunately, datetime.datetime.strptime() ignores timezone information...
        ("Sat, 08 Jan 2022 20:36:07 CET", datetime.datetime(2022, 1, 8, 20, 36, 7)),  # Unfortunately, datetime.datetime.strptime() ignores timezone information...
        ("Sat, 08 Jan 2022 20:36:07 KET", InputDataNotConvertibleExc),  # ... however, it detects the timezone string being invalid.
        ("Tue, 08 Jan 2022 20:36:07 GMT", datetime.datetime(2022, 1, 8, 20, 36, 7)),  # Day of week is ignored by datetime.datetime.strptime()...
        ("Kue, 08 Jan 2022 20:36:07 GMT", InputDataNotConvertibleExc),  # ... as long as it represents a valid weekday.
        ("Sat, 8 Jan 2022 20:36:07 GMT", datetime.datetime(2022, 1, 8, 20, 36, 7)),
        ("Sat, 8 Jan 2022 02:36:07 GMT", datetime.datetime(2022, 1, 8, 2, 36, 7)),
        ("Sat, 8 Jan 2022 2:36:07 GMT", datetime.datetime(2022, 1, 8, 2, 36, 7)),
        ("Sat, 29 Feb 2022 20:36:07 GMT", InputDataNotConvertibleExc),
        ("2011-11-04 01:05:23", datetime.datetime(2011, 11, 4, 1, 5, 23)),  # ISO format is accepted even if the instance has *additional* string formats...
        ("2011-11-04 01:05:23.283999+05:30:10.123456", datetime.datetime(2011, 11, 4, 1, 5, 23, 283999, tzinfo=datetime.timezone(datetime.timedelta(seconds=19810, microseconds=123456)))),  # ISO format is accepted even if the instance has *additional* string formats...
        ("", InputDataNotConvertibleExc),
        ("hello", InputDataNotConvertibleExc),
        ("\x00", InputDataNotConvertibleExc),
        ("Pepík", InputDataNotConvertibleExc)
    )),
    (DatetimeBlueprint(filters=(DatetimeAddTimezoneFilter(zoneinfo.ZoneInfo("Europe/Prague")),)), (
        (datetime.datetime(2020, 8, 20, 8, 20, 30), datetime.datetime(2020, 8, 20, 8, 20, 30, tzinfo=zoneinfo.ZoneInfo("Europe/Prague"))),
        (datetime.datetime(2020, 8, 20, 8, 20, 30, tzinfo=zoneinfo.ZoneInfo("Europe/Prague")), datetime.datetime(2020, 8, 20, 8, 20, 30, tzinfo=zoneinfo.ZoneInfo("Europe/Prague"))),
        (datetime.datetime(2020, 8, 20, 8, 20, 30, tzinfo=datetime.timezone.utc), datetime.datetime(2020, 8, 20, 8, 20, 30, tzinfo=datetime.timezone.utc)),
        (datetime.datetime(2020, 8, 20, 8, 20, 30, tzinfo=zoneinfo.ZoneInfo("America/New_York")), datetime.datetime(2020, 8, 20, 8, 20, 30, tzinfo=zoneinfo.ZoneInfo("America/New_York"))),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc)  # "Checks" if the blueprint is not affected by the filter
    )),
    (DatetimeBlueprint(filters=(DatetimeChangeTimezoneFilter(zoneinfo.ZoneInfo("Europe/Prague")),)), (
        (datetime.datetime(2020, 1, 30, 7, 30, 40), InputDatetimeObjectIsNaiveInFilterExc),
        (datetime.datetime(2020, 7, 30, 7, 30, 40), InputDatetimeObjectIsNaiveInFilterExc),
        (datetime.datetime(2020, 1, 30, 7, 30, 40, tzinfo=zoneinfo.ZoneInfo("Europe/Prague")), datetime.datetime(2020, 1, 30, 7, 30, 40, tzinfo=zoneinfo.ZoneInfo("Europe/Prague"))),
        (datetime.datetime(2020, 7, 30, 7, 30, 40, tzinfo=zoneinfo.ZoneInfo("Europe/Prague")), datetime.datetime(2020, 7, 30, 7, 30, 40, tzinfo=zoneinfo.ZoneInfo("Europe/Prague"))),
        (datetime.datetime(2020, 1, 30, 7, 30, 40, tzinfo=datetime.timezone.utc), datetime.datetime(2020, 1, 30, 8, 30, 40, tzinfo=zoneinfo.ZoneInfo("Europe/Prague"))),
        (datetime.datetime(2020, 7, 30, 7, 30, 40, tzinfo=datetime.timezone.utc), datetime.datetime(2020, 7, 30, 9, 30, 40, tzinfo=zoneinfo.ZoneInfo("Europe/Prague"))),  # DST active
        (datetime.datetime(2020, 1, 30, 7, 30, 40, tzinfo=zoneinfo.ZoneInfo("America/New_York")), datetime.datetime(2020, 1, 30, 13, 30, 40, tzinfo=zoneinfo.ZoneInfo("Europe/Prague"))),
        (datetime.datetime(2020, 7, 30, 7, 30, 40, tzinfo=zoneinfo.ZoneInfo("America/New_York")), datetime.datetime(2020, 7, 30, 13, 30, 40, tzinfo=zoneinfo.ZoneInfo("Europe/Prague"))),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc)  # "Checks" if the blueprint is not affected by the filter
    )),
    (DatetimeBlueprint(validators=(DatetimeIsAwareValidator(negate=False),)), (
        (datetime.datetime(2020, 6, 15, 10, 20, 30), DataValidationFailedExc),
        (datetime.datetime(2020, 6, 15, 10, 20, 30, tzinfo=datetime.timezone.utc), datetime.datetime(2020, 6, 15, 10, 20, 30, tzinfo=datetime.timezone.utc)),
        (datetime.datetime(2020, 6, 15, 10, 20, 30, tzinfo=zoneinfo.ZoneInfo("Europe/Prague")), datetime.datetime(2020, 6, 15, 10, 20, 30, tzinfo=zoneinfo.ZoneInfo("Europe/Prague"))),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc)  # "Checks" if the blueprint is not affected by the validator
    )),
    (DatetimeBlueprint(validators=(DatetimeIsAwareValidator(negate=True),)), (
        (datetime.datetime(2020, 6, 15, 10, 20, 30), datetime.datetime(2020, 6, 15, 10, 20, 30)),
        (datetime.datetime(2020, 6, 15, 10, 20, 30, tzinfo=datetime.timezone.utc), DataValidationFailedExc),
        (datetime.datetime(2020, 6, 15, 10, 20, 30, tzinfo=zoneinfo.ZoneInfo("Europe/Prague")), DataValidationFailedExc),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc)  # "Checks" if the blueprint is not affected by the validator
    )),
    (DatetimeBlueprint(validators=(DatetimeNotAfterValidator(datetime.datetime(2021, 7, 20, 8, 30, 40, tzinfo=zoneinfo.ZoneInfo("Europe/Prague"))),)), (
        (datetime.datetime(2021, 7, 20, 8, 30, 40), InputDatetimeObjectIsNaiveInValidatorExc),
        (datetime.datetime(1, 7, 20, 8, 30, 41, tzinfo=zoneinfo.ZoneInfo("Europe/Prague")), datetime.datetime(1, 7, 20, 8, 30, 41, tzinfo=zoneinfo.ZoneInfo("Europe/Prague"))),
        (datetime.datetime(2021, 7, 20, 8, 30, 39, tzinfo=zoneinfo.ZoneInfo("Europe/Prague")), datetime.datetime(2021, 7, 20, 8, 30, 39, tzinfo=zoneinfo.ZoneInfo("Europe/Prague"))),
        (datetime.datetime(2021, 7, 20, 8, 30, 40, tzinfo=zoneinfo.ZoneInfo("Europe/Prague")), datetime.datetime(2021, 7, 20, 8, 30, 40, tzinfo=zoneinfo.ZoneInfo("Europe/Prague"))),
        (datetime.datetime(2021, 7, 20, 8, 30, 41, tzinfo=zoneinfo.ZoneInfo("Europe/Prague")), DataValidationFailedExc),
        (datetime.datetime(9999, 7, 20, 8, 30, 39, tzinfo=zoneinfo.ZoneInfo("Europe/Prague")), DataValidationFailedExc),
        (datetime.datetime(1, 7, 20, 6, 30, 41, tzinfo=datetime.timezone.utc), datetime.datetime(1, 7, 20, 6, 30, 41, tzinfo=datetime.timezone.utc)),  # DST active
        (datetime.datetime(2021, 7, 20, 6, 30, 39, tzinfo=datetime.timezone.utc), datetime.datetime(2021, 7, 20, 6, 30, 39, tzinfo=datetime.timezone.utc)),  # DST active
        (datetime.datetime(2021, 7, 20, 6, 30, 40, tzinfo=datetime.timezone.utc), datetime.datetime(2021, 7, 20, 6, 30, 40, tzinfo=datetime.timezone.utc)),  # DST active
        (datetime.datetime(2021, 7, 20, 6, 30, 41, tzinfo=datetime.timezone.utc), DataValidationFailedExc),  # DST active
        (datetime.datetime(9999, 7, 20, 6, 30, 39, tzinfo=datetime.timezone.utc), DataValidationFailedExc),  # DST active
        (datetime.datetime(1, 7, 20, 2, 30, 41, tzinfo=zoneinfo.ZoneInfo("America/New_York")), datetime.datetime(1, 7, 20, 2, 30, 41, tzinfo=zoneinfo.ZoneInfo("America/New_York"))),
        (datetime.datetime(2021, 7, 20, 2, 30, 39, tzinfo=zoneinfo.ZoneInfo("America/New_York")), datetime.datetime(2021, 7, 20, 2, 30, 39, tzinfo=zoneinfo.ZoneInfo("America/New_York"))),
        (datetime.datetime(2021, 7, 20, 2, 30, 40, tzinfo=zoneinfo.ZoneInfo("America/New_York")), datetime.datetime(2021, 7, 20, 2, 30, 40, tzinfo=zoneinfo.ZoneInfo("America/New_York"))),
        (datetime.datetime(2021, 7, 20, 2, 30, 41, tzinfo=zoneinfo.ZoneInfo("America/New_York")), DataValidationFailedExc),
        (datetime.datetime(9999, 7, 20, 2, 30, 39, tzinfo=zoneinfo.ZoneInfo("America/New_York")), DataValidationFailedExc),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc)  # "Checks" if the blueprint is not affected by the validator
    )),
    (DatetimeBlueprint(validators=(DatetimeNotBeforeValidator(datetime.datetime(2021, 6, 10, 15, 20, 25, tzinfo=zoneinfo.ZoneInfo("Europe/Prague"))),)), (
        (datetime.datetime(2021, 6, 10, 15, 20, 25), InputDatetimeObjectIsNaiveInValidatorExc),
        (datetime.datetime(1, 6, 10, 15, 20, 26, tzinfo=zoneinfo.ZoneInfo("Europe/Prague")), DataValidationFailedExc),
        (datetime.datetime(2021, 6, 10, 15, 20, 24, tzinfo=zoneinfo.ZoneInfo("Europe/Prague")), DataValidationFailedExc),
        (datetime.datetime(2021, 6, 10, 15, 20, 25, tzinfo=zoneinfo.ZoneInfo("Europe/Prague")), datetime.datetime(2021, 6, 10, 15, 20, 25, tzinfo=zoneinfo.ZoneInfo("Europe/Prague"))),
        (datetime.datetime(2021, 6, 10, 15, 20, 26, tzinfo=zoneinfo.ZoneInfo("Europe/Prague")), datetime.datetime(2021, 6, 10, 15, 20, 26, tzinfo=zoneinfo.ZoneInfo("Europe/Prague"))),
        (datetime.datetime(9999, 6, 10, 15, 20, 24, tzinfo=zoneinfo.ZoneInfo("Europe/Prague")), datetime.datetime(9999, 6, 10, 15, 20, 24, tzinfo=zoneinfo.ZoneInfo("Europe/Prague"))),
        (datetime.datetime(1, 6, 10, 13, 20, 26, tzinfo=datetime.timezone.utc), DataValidationFailedExc),  # DST active
        (datetime.datetime(2021, 6, 10, 13, 20, 24, tzinfo=datetime.timezone.utc), DataValidationFailedExc),  # DST active
        (datetime.datetime(2021, 6, 10, 13, 20, 25, tzinfo=datetime.timezone.utc), datetime.datetime(2021, 6, 10, 13, 20, 25, tzinfo=datetime.timezone.utc)),  # DST active
        (datetime.datetime(2021, 6, 10, 13, 20, 26, tzinfo=datetime.timezone.utc), datetime.datetime(2021, 6, 10, 13, 20, 26, tzinfo=datetime.timezone.utc)),  # DST active
        (datetime.datetime(9999, 6, 10, 13, 20, 24, tzinfo=datetime.timezone.utc), datetime.datetime(9999, 6, 10, 13, 20, 24, tzinfo=datetime.timezone.utc)),  # DST active
        (datetime.datetime(1, 6, 10, 9, 20, 26, tzinfo=zoneinfo.ZoneInfo("America/New_York")), DataValidationFailedExc),
        (datetime.datetime(2021, 6, 10, 9, 20, 24, tzinfo=zoneinfo.ZoneInfo("America/New_York")), DataValidationFailedExc),
        (datetime.datetime(2021, 6, 10, 9, 20, 25, tzinfo=zoneinfo.ZoneInfo("America/New_York")), datetime.datetime(2021, 6, 10, 9, 20, 25, tzinfo=zoneinfo.ZoneInfo("America/New_York"))),
        (datetime.datetime(2021, 6, 10, 9, 20, 26, tzinfo=zoneinfo.ZoneInfo("America/New_York")), datetime.datetime(2021, 6, 10, 9, 20, 26, tzinfo=zoneinfo.ZoneInfo("America/New_York"))),
        (datetime.datetime(9999, 6, 10, 9, 20, 24, tzinfo=zoneinfo.ZoneInfo("America/New_York")), datetime.datetime(9999, 6, 10, 9, 20, 24, tzinfo=zoneinfo.ZoneInfo("America/New_York"))),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc)  # "Checks" if the blueprint is not affected by the validator
    )),
    (DatetimeBlueprint(
        filters=(
            DatetimeAddTimezoneFilter(datetime.timezone.utc),
            DatetimeChangeTimezoneFilter(zoneinfo.ZoneInfo("Europe/Prague"))
        ),
        validators=(
            DatetimeNotBeforeValidator(datetime.datetime(2015, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Prague"))),
            DatetimeNotAfterValidator(datetime.datetime(2025, 12, 31, 23, 59, 59, tzinfo=zoneinfo.ZoneInfo("Europe/Prague")))
        )
    ), (
        (datetime.datetime(2020, 6, 15, 12, 30, 40), datetime.datetime(2020, 6, 15, 14, 30, 40, tzinfo=zoneinfo.ZoneInfo("Europe/Prague"))),
        (datetime.datetime(2020, 6, 15, 12, 30, 40, tzinfo=datetime.timezone.utc), datetime.datetime(2020, 6, 15, 14, 30, 40, tzinfo=zoneinfo.ZoneInfo("Europe/Prague"))),  # DST active
        (datetime.datetime(2020, 6, 15, 12, 30, 40, tzinfo=zoneinfo.ZoneInfo("Europe/Prague")), datetime.datetime(2020, 6, 15, 12, 30, 40, tzinfo=zoneinfo.ZoneInfo("Europe/Prague"))),
        (datetime.datetime(2020, 6, 15, 12, 30, 40, tzinfo=zoneinfo.ZoneInfo("America/New_York")), datetime.datetime(2020, 6, 15, 18, 30, 40, tzinfo=zoneinfo.ZoneInfo("Europe/Prague"))),
        (datetime.datetime(2014, 12, 31, 23, 59, 59, tzinfo=zoneinfo.ZoneInfo("Europe/Prague")), DataValidationFailedExc),
        (datetime.datetime(2015, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Prague")), datetime.datetime(2015, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Prague"))),
        (datetime.datetime(2015, 1, 1, 0, 0, 1, tzinfo=zoneinfo.ZoneInfo("Europe/Prague")), datetime.datetime(2015, 1, 1, 0, 0, 1, tzinfo=zoneinfo.ZoneInfo("Europe/Prague"))),
        (datetime.datetime(2025, 12, 31, 23, 59, 58, tzinfo=zoneinfo.ZoneInfo("Europe/Prague")), datetime.datetime(2025, 12, 31, 23, 59, 58, tzinfo=zoneinfo.ZoneInfo("Europe/Prague"))),
        (datetime.datetime(2025, 12, 31, 23, 59, 59, tzinfo=zoneinfo.ZoneInfo("Europe/Prague")), datetime.datetime(2025, 12, 31, 23, 59, 59, tzinfo=zoneinfo.ZoneInfo("Europe/Prague"))),
        (datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Prague")), DataValidationFailedExc),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc)  # "Checks" if the blueprint is not affected by the validator
    ))
)


@pytest.mark.parametrize(("blueprint", "input_", "output"), theoretical_testutils.test_function_parameter_generator(__DATETIME_BLUEPRINT_TEST_SUITE))
def test_datetime_blueprint(blueprint, input_, output):
    theoretical_testutils.perform_test(blueprint, input_, output)


def test_datetime_blueprint_default_parsing_mode():
    assert DatetimeBlueprint().get_parsing_mode() == ParsingMode.MODE_RATIONAL


def test_datetime_blueprint_filter_and_validator_sequences():
    filter_sequence = (DatetimeAddTimezoneFilter(datetime.timezone.utc), DatetimeChangeTimezoneFilter(datetime.timezone.utc))
    validator_sequence = (
        DatetimeIsAwareValidator(),
        DatetimeNotBeforeValidator(datetime.datetime.now(tz=datetime.timezone.utc)),
        DatetimeNotAfterValidator(datetime.datetime.now(tz=datetime.timezone.utc))
    )
    blueprint = DatetimeBlueprint(filters=filter_sequence, validators=validator_sequence)

    assert (blueprint.get_filters() == filter_sequence) and (blueprint.get_validators() == validator_sequence)


def test_datetime_add_timezone_filter_added_timezone():
    assert DatetimeAddTimezoneFilter(zoneinfo.ZoneInfo("Europe/Prague")).get_added_timezone() == zoneinfo.ZoneInfo("Europe/Prague")


def test_datetime_change_timezone_filter_new_timezone():
    assert DatetimeChangeTimezoneFilter(zoneinfo.ZoneInfo("Europe/Prague")).get_new_timezone() == zoneinfo.ZoneInfo("Europe/Prague")


def test_datetime_is_aware_validator_default_negation():
    assert DatetimeIsAwareValidator().is_negated() is False


def test_datetime_not_after_validator_latest_acceptable_datetime():
    latest_acceptable_dt = datetime.datetime.now(tz=zoneinfo.ZoneInfo("Europe/Prague"))
    assert DatetimeNotAfterValidator(latest_acceptable_dt).get_latest_acceptable_datetime() == latest_acceptable_dt


def test_datetime_not_after_validator_naive_latest_acceptable_datetime():
    with pytest.raises(InvalidValidatorConfigError):
        DatetimeNotAfterValidator(datetime.datetime.now())


def test_datetime_not_before_validator_earliest_acceptable_datetime():
    earliest_acceptable_dt = datetime.datetime.now(tz=zoneinfo.ZoneInfo("Europe/Prague"))
    assert DatetimeNotBeforeValidator(earliest_acceptable_dt).get_earliest_acceptable_datetime() == earliest_acceptable_dt


def test_datetime_not_before_validator_naive_earliest_acceptable_datetime():
    with pytest.raises(InvalidValidatorConfigError):
        DatetimeNotBeforeValidator(datetime.datetime.now())
