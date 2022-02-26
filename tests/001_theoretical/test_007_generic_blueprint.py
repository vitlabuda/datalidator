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

import theoretical_testutils
import pytest
import datetime
import ipaddress
import urllib.parse
import uuid
from datalidator.blueprints.impl.GenericBlueprint import GenericBlueprint


class CustomObject:
    def __init__(self, initial: int):
        self.__initial: int = initial

    def get(self) -> int:
        return self.__initial


__TESTED_INSTANCES = (
    False,
    None,
    123,
    123.456,
    "random string",
    b'random bytes',
    [],
    {},
    datetime.datetime.now(),
    datetime.datetime.now().date(),
    datetime.datetime.now().time(),
    ipaddress.ip_address("127.0.0.1"),
    ipaddress.ip_address("::1"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("2001:db8::/32"),
    urllib.parse.urlparse("https://www.google.cz/test?abc=def"),
    uuid.UUID('{12345678-1234-5678-1234-567812345678}'),
    theoretical_testutils.EmptyObject(),
    CustomObject(554)
)


__GENERIC_BLUEPRINT_TEST_SUITE = (
    (GenericBlueprint(), tuple((instance, instance) for instance in __TESTED_INSTANCES)),
)


@pytest.mark.parametrize(("blueprint", "input_", "output"), theoretical_testutils.test_function_parameter_generator(__GENERIC_BLUEPRINT_TEST_SUITE))
def test_generic_blueprint(blueprint, input_, output):
    theoretical_testutils.perform_test(blueprint, input_, output, compare_using_is=True)
