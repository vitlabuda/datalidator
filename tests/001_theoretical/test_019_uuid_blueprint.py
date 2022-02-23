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
import uuid
import datetime
import ipaddress
import urllib.parse
from test_014_string_blueprint import StringableObject, ExceptionRaisingStringableObject
from datalidator.blueprints.impl.UUIDBlueprint import UUIDBlueprint
from datalidator.blueprints.exc.InputDataNotConvertibleExc import InputDataNotConvertibleExc
from datalidator.blueprints.exc.InputDataTypeNotInAllowlistExc import InputDataTypeNotInAllowlistExc


# NOTE: Some outputs might not seem "sane" when comparing them to input data.
#  However, the outputs are produced by underlying Python standard library functions which might have some quirks caused by their internal implementation.
#  As testing the standard library is obviously not the objective of this test, it does not matter - the important thing is that the tested blueprints, filters and validators themselves work fine.


__UUID_BLUEPRINT_TEST_SUITE = (
    (UUIDBlueprint(), (
        # The parsability of most of the tested values depends on uuid.UUID()'s internal implementation;
        #  therefore, some tests may start to fail after, for example, upgrading to a newer Python version.
        # (The reason for their presence is to ensure that the blueprint can deal with these "weird" inputs.)
        (uuid.UUID("12345678123456781234567812345678"), uuid.UUID("12345678-1234-5678-1234-567812345678")),
        (uuid.UUID("{12345678-1234-5678-1234-567812345678}"), uuid.UUID("12345678-1234-5678-1234-567812345678")),
        (uuid.UUID("12345678-1234-5678-1234-567812345678"), uuid.UUID("12345678-1234-5678-1234-567812345678")),
        (uuid.UUID("urn:uuid:12345678-1234-5678-1234-567812345678"), uuid.UUID("12345678-1234-5678-1234-567812345678")),
        (uuid.UUID("urn:uuid:12345678123456781234567812345678"), uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("12345678123456781234567812345678", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("{12345678-1234-5678-1234-567812345678}", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("{{12345678-1234-5678-1234-567812345678}}", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("{{12345678-1234-5678-1{234-567812345678}}", InputDataNotConvertibleExc),
        ("{{12345678-1234-5678-1}234-567812345678}}", InputDataNotConvertibleExc),
        ("{{12345678-1234-5678-1{}234-567812345678}}", InputDataNotConvertibleExc),
        ("{{}}}}}{}{}{}{}{}{}12345678-1234-5678-1234-567812345678}}}{{{}}{}{}{{", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("{{}}}}}{}{}{}{}{}{}12345678-----1--234----567--8----1234----56---78123---45678}}}{{{}}{}{}{{", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("12345678-1234-5678-1234-567812345678", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("---12345678-1234-5678-1234-567812345678--", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("12345678----1234-----5678----1234----567812345678", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("---12345678----1234-----5678----1234----567812345678--", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("---12---34----5678----1234-----5678----1234----56781234567-------------8--", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("-1-2-3-4-5-6-7-8-1-2-3-4-5-6-7-8-1-2-3-4-5-6-7-8-1-2-3-4-5-6-7-8-", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("{{{---12---34----5678----1234-----5678----1234----56781234567-------------8--}}}", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("{{{}}}{{}---12---34----5678----1234-----5678----1234----56781234567-------------8--}}}{{{}}}", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("urn:uuid:12345678123456781234567812345678", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("Urn:Uuid:12345678123456781234567812345678", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("URN:UUID:12345678123456781234567812345678", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("urn:uuid:{12345678-1234-5678-1234-567812345678}", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("urn:uuid:{{}}}12345678-1234-5678-1234-567812345678{{}}}}", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("urn:uuid:{{}}}---1234--56----78-12---34-56---78-12-34-56781234-5678----{{}}}}", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("urn:uuid:12345678-1234-5678-1234-567812345678", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("urn:uuid:----------12345678----1234-5678----1234--567812345678------", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("urn:uuid:urn:uuid:urn:uuid:urn:uuid:{urn:uuid:12345678-urn:uuid:1234-5678urn:uuid:-urn:uuid:1234-urn:uuid:56781234567urn:uuid:8}urn:uuid:", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("urn:uuid{12345678-1234-5678-1234-567812345678}", InputDataNotConvertibleExc),
        ("urnuuid:{12345678-1234-5678-1234-567812345678}", InputDataNotConvertibleExc),
        ("urnuuid{12345678-1234-5678-1234-567812345678}", InputDataNotConvertibleExc),
        ("urn:{12345678-1234-5678-1234-567812345678}", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("URN:{12345678-1234-5678-1234-567812345678}", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("URN:urn:{1urn:2345678-urn:1234urn:-5678urn:-urn:1234-urn:567812345678urn:}urn:urn:urn:", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("uuid:{12345678-1234-5678-1234-567812345678}", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("UUID:{12345678-1234-5678-1234-567812345678}", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("UUID:uuid:uuid:{uuid:uuid:12345678uuid:-1234uuid:-uuid:5678-uuid:1234uuid:-567812345678uuid:}uuid:", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("1", InputDataNotConvertibleExc),
        ("1234567812345678123456781234567", InputDataNotConvertibleExc),
        ("12345678123456781234567812345678", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("123456781234567812345678123456789", InputDataNotConvertibleExc),
        ("123456781234567812345678123456789123456789123456789123456789", InputDataNotConvertibleExc),
        ("12345678123456781234567812345678x", InputDataNotConvertibleExc),
        ("x12345678123456781234567812345678", InputDataNotConvertibleExc),
        ("123456781234567812345x67812345678", InputDataNotConvertibleExc),
        ("1234567812345678123456781234567x", InputDataNotConvertibleExc),
        ("x1234567812345678123456781234567", InputDataNotConvertibleExc),
        ("123456781234567812345x6781234567", InputDataNotConvertibleExc),
        ("12345678123456781234567812345678T", InputDataNotConvertibleExc),
        ("T12345678123456781234567812345678", InputDataNotConvertibleExc),
        ("123456781234567812345x67812345678", InputDataNotConvertibleExc),
        ("1234567812345678123456781234567T", InputDataNotConvertibleExc),
        ("T1234567812345678123456781234567", InputDataNotConvertibleExc),
        ("123456781234567812345T6781234567", InputDataNotConvertibleExc),
        ("12345678123456781234567812345678š", InputDataNotConvertibleExc),
        ("š12345678123456781234567812345678", InputDataNotConvertibleExc),
        ("123456781234567812345š67812345678", InputDataNotConvertibleExc),
        ("1234567812345678123456781234567š", InputDataNotConvertibleExc),
        ("š1234567812345678123456781234567", InputDataNotConvertibleExc),
        ("123456781234567812345š6781234567", InputDataNotConvertibleExc),
        ("12345678123456781234567812345678🤍", InputDataNotConvertibleExc),
        ("🤍12345678123456781234567812345678", InputDataNotConvertibleExc),
        ("123456781234567812345🤍67812345678", InputDataNotConvertibleExc),
        ("1234567812345678123456781234567🤍", InputDataNotConvertibleExc),
        ("🤍1234567812345678123456781234567", InputDataNotConvertibleExc),
        ("123456781234567812345🤍6781234567", InputDataNotConvertibleExc),
        ("12345678123456781234567812345678!", InputDataNotConvertibleExc),
        ("!12345678123456781234567812345678", InputDataNotConvertibleExc),
        ("123456781234567812345!67812345678", InputDataNotConvertibleExc),
        ("1234567812345678123456781234567!", InputDataNotConvertibleExc),
        ("!1234567812345678123456781234567", InputDataNotConvertibleExc),
        ("123456781234567812345!6781234567", InputDataNotConvertibleExc),
        ("12345678123456781234567812345678\uffff", InputDataNotConvertibleExc),
        ("\uffff12345678123456781234567812345678", InputDataNotConvertibleExc),
        ("123456781234567812345\uffff67812345678", InputDataNotConvertibleExc),
        ("1234567812345678123456781234567\uffff", InputDataNotConvertibleExc),
        ("\uffff1234567812345678123456781234567", InputDataNotConvertibleExc),
        ("123456781234567812345\uffff6781234567", InputDataNotConvertibleExc),
        ("12345678123456781234567812345678\x00", InputDataNotConvertibleExc),
        ("\x0012345678123456781234567812345678", InputDataNotConvertibleExc),
        ("123456781234567812345\x0067812345678", InputDataNotConvertibleExc),
        ("1234567812345678123456781234567\x00", InputDataNotConvertibleExc),
        ("\x001234567812345678123456781234567", InputDataNotConvertibleExc),
        ("123456781234567812345\x006781234567", InputDataNotConvertibleExc),
        ("12345678123456781234567812345678 ", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        (" 12345678123456781234567812345678",  uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("123456781234567812345 67812345678", InputDataNotConvertibleExc),
        ("1234567812345678123456781234567 ", InputDataNotConvertibleExc),
        (" 1234567812345678123456781234567", InputDataNotConvertibleExc),
        ("123456781234567812345 6781234567", InputDataNotConvertibleExc),
        ("12345678123456781234567812345678\u2028", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("\u202812345678123456781234567812345678",  uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("123456781234567812345\u202867812345678", InputDataNotConvertibleExc),
        ("1234567812345678123456781234567\u2028", InputDataNotConvertibleExc),
        ("\u20281234567812345678123456781234567", InputDataNotConvertibleExc),
        ("123456781234567812345\u20286781234567", InputDataNotConvertibleExc),
        ("12345678123456781234567812345678\n", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("\n12345678123456781234567812345678",  uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("123456781234567812345\n67812345678", InputDataNotConvertibleExc),
        ("1234567812345678123456781234567\n", InputDataNotConvertibleExc),
        ("\n1234567812345678123456781234567", InputDataNotConvertibleExc),
        ("123456781234567812345\n6781234567", InputDataNotConvertibleExc),
        ("12345678123456781234567812345678\x1d", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("\x1d12345678123456781234567812345678",  uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("123456781234567812345\x1d7812345678", InputDataNotConvertibleExc),
        ("1234567812345678123456781234567\x1d", InputDataNotConvertibleExc),
        ("\x1d1234567812345678123456781234567", InputDataNotConvertibleExc),
        ("123456781234567812345\x1d6781234567", InputDataNotConvertibleExc),
        ("abcdefabcdefabcdefabcdefabcdefab", uuid.UUID('abcdefab-cdef-abcd-efab-cdefabcdefab')),
        ("abcDEfabcdeFAbcdefabcdefABCdefAb", uuid.UUID('abcdefab-cdef-abcd-efab-cdefabcdefab')),
        ("ABCDEFABCDEFABCDEFABCDEFABCDEFAB", uuid.UUID('abcdefab-cdef-abcd-efab-cdefabcdefab')),
        ("urn:uuid:{{}}{{}{-----a---b-cdef-a-b-cd-efab-c----defa-bcde-f-a-bcde-f-ab-----{}}{}{{{}", uuid.UUID('abcdefab-cdef-abcd-efab-cdefabcdefab')),
        ("URN:UUID:{{}}{{}{-----a---b-cdef-a-b-cd-EFAB-C----DEFA-BCDE-f-a-bcde-f-ab-----{}}{}{{{}", uuid.UUID('abcdefab-cdef-abcd-efab-cdefabcdefab')),
        ("\n\r\t\u00a0  \u2009   \f 12345678123456781234567812345678\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("\n\r\t\u00a0  \u2009   \f {12345678-1234-5678-1234-567812345678}\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("\n\r\t\u00a0  \u2009   \f {{12345678-1234-5678-1234-567812345678}}\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("\n\r\t\u00a0  \u2009   \f {{12345678-1234-5678-1{234-567812345678}}\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f {{12345678-1234-5678-1}234-567812345678}}\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f {{12345678-1234-5678-1{}234-567812345678}}\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f {{}}}}}{}{}{}{}{}{}12345678-1234-5678-1234-567812345678}}}{{{}}{}{}{{\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("\n\r\t\u00a0  \u2009   \f {{}}}}}{}{}{}{}{}{}12345678-----1--234----567--8----1234----56---78123---45678}}}{{{}}{}{}{{\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("\n\r\t\u00a0  \u2009   \f 12345678-1234-5678-1234-567812345678\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("\n\r\t\u00a0  \u2009   \f ---12345678-1234-5678-1234-567812345678--\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("\n\r\t\u00a0  \u2009   \f 12345678----1234-----5678----1234----567812345678\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("\n\r\t\u00a0  \u2009   \f ---12345678----1234-----5678----1234----567812345678--\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("\n\r\t\u00a0  \u2009   \f ---12---34----5678----1234-----5678----1234----56781234567-------------8--\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("\n\r\t\u00a0  \u2009   \f -1-2-3-4-5-6-7-8-1-2-3-4-5-6-7-8-1-2-3-4-5-6-7-8-1-2-3-4-5-6-7-8-\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("\n\r\t\u00a0  \u2009   \f {{{---12---34----5678----1234-----5678----1234----56781234567-------------8--}}}\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("\n\r\t\u00a0  \u2009   \f {{{}}}{{}---12---34----5678----1234-----5678----1234----56781234567-------------8--}}}{{{}}}\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("\n\r\t\u00a0  \u2009   \f urn:uuid:12345678123456781234567812345678\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("\n\r\t\u00a0  \u2009   \f Urn:Uuid:12345678123456781234567812345678\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("\n\r\t\u00a0  \u2009   \f URN:UUID:12345678123456781234567812345678\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("\n\r\t\u00a0  \u2009   \f urn:uuid:{12345678-1234-5678-1234-567812345678}\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("\n\r\t\u00a0  \u2009   \f urn:uuid:{{}}}12345678-1234-5678-1234-567812345678{{}}}}\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("\n\r\t\u00a0  \u2009   \f urn:uuid:{{}}}---1234--56----78-12---34-56---78-12-34-56781234-5678----{{}}}}\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("\n\r\t\u00a0  \u2009   \f urn:uuid:12345678-1234-5678-1234-567812345678\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("\n\r\t\u00a0  \u2009   \f urn:uuid:----------12345678----1234-5678----1234--567812345678------\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("\n\r\t\u00a0  \u2009   \f urn:uuid:urn:uuid:urn:uuid:urn:uuid:{urn:uuid:12345678-urn:uuid:1234-5678urn:uuid:-urn:uuid:1234-urn:uuid:56781234567urn:uuid:8}urn:uuid:\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("\n\r\t\u00a0  \u2009   \f urn:uuid{12345678-1234-5678-1234-567812345678}\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f urnuuid:{12345678-1234-5678-1234-567812345678}\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f urnuuid{12345678-1234-5678-1234-567812345678}\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f urn:{12345678-1234-5678-1234-567812345678}\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("\n\r\t\u00a0  \u2009   \f URN:{12345678-1234-5678-1234-567812345678}\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("\n\r\t\u00a0  \u2009   \f URN:urn:{1urn:2345678-urn:1234urn:-5678urn:-urn:1234-urn:567812345678urn:}urn:urn:urn:\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("\n\r\t\u00a0  \u2009   \f uuid:{12345678-1234-5678-1234-567812345678}\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("\n\r\t\u00a0  \u2009   \f UUID:{12345678-1234-5678-1234-567812345678}\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("\n\r\t\u00a0  \u2009   \f UUID:uuid:uuid:{uuid:uuid:12345678uuid:-1234uuid:-uuid:5678-uuid:1234uuid:-567812345678uuid:}uuid:\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("\n\r\t\u00a0  \u2009   \f 1\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f 1234567812345678123456781234567\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f 12345678123456781234567812345678\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("\n\r\t\u00a0  \u2009   \f 123456781234567812345678123456789\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f 123456781234567812345678123456789123456789123456789123456789\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f 12345678123456781234567812345678x\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f x12345678123456781234567812345678\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f 123456781234567812345x67812345678\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f 1234567812345678123456781234567x\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f x1234567812345678123456781234567\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f 123456781234567812345x6781234567\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f 12345678123456781234567812345678T\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f T12345678123456781234567812345678\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f 123456781234567812345x67812345678\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f 1234567812345678123456781234567T\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f T1234567812345678123456781234567\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f 123456781234567812345T6781234567\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f 12345678123456781234567812345678š\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f š12345678123456781234567812345678\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f 123456781234567812345š67812345678\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f 1234567812345678123456781234567š\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f š1234567812345678123456781234567\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f 123456781234567812345š6781234567\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f 12345678123456781234567812345678🤍\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f 🤍12345678123456781234567812345678\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f 123456781234567812345🤍67812345678\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f 1234567812345678123456781234567🤍\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f 🤍1234567812345678123456781234567\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f 123456781234567812345🤍6781234567\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f 12345678123456781234567812345678!\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f !12345678123456781234567812345678\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f 123456781234567812345!67812345678\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f 1234567812345678123456781234567!\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f !1234567812345678123456781234567\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f 123456781234567812345!6781234567\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f 12345678123456781234567812345678\uffff\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f \uffff12345678123456781234567812345678\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f 123456781234567812345\uffff67812345678\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f 1234567812345678123456781234567\uffff\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f \uffff1234567812345678123456781234567\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f 123456781234567812345\uffff6781234567\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f 12345678123456781234567812345678\x00\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f \x0012345678123456781234567812345678\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f 123456781234567812345\x0067812345678\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f 1234567812345678123456781234567\x00\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f \x001234567812345678123456781234567\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f 123456781234567812345\x006781234567\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f 12345678123456781234567812345678 \x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("\n\r\t\u00a0  \u2009   \f  12345678123456781234567812345678\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ",  uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("\n\r\t\u00a0  \u2009   \f 123456781234567812345 67812345678\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f 1234567812345678123456781234567 \x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f  1234567812345678123456781234567\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f 123456781234567812345 6781234567\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f 12345678123456781234567812345678\u2028\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("\n\r\t\u00a0  \u2009   \f \u202812345678123456781234567812345678\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ",  uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("\n\r\t\u00a0  \u2009   \f 123456781234567812345\u202867812345678\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f 1234567812345678123456781234567\u2028\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f \u20281234567812345678123456781234567\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f 123456781234567812345\u20286781234567\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f 12345678123456781234567812345678\n\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("\n\r\t\u00a0  \u2009   \f \n12345678123456781234567812345678\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ",  uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("\n\r\t\u00a0  \u2009   \f 123456781234567812345\n67812345678\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f 1234567812345678123456781234567\n\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f \n1234567812345678123456781234567\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f 123456781234567812345\n6781234567\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f 12345678123456781234567812345678\x1d\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("\n\r\t\u00a0  \u2009   \f \x1d12345678123456781234567812345678\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ",  uuid.UUID("12345678-1234-5678-1234-567812345678")),
        ("\n\r\t\u00a0  \u2009   \f 123456781234567812345\x1d7812345678\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f 1234567812345678123456781234567\x1d\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f \x1d1234567812345678123456781234567\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f 123456781234567812345\x1d6781234567\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", InputDataNotConvertibleExc),
        ("\n\r\t\u00a0  \u2009   \f abcdefabcdefabcdefabcdefabcdefab\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", uuid.UUID('abcdefab-cdef-abcd-efab-cdefabcdefab')),
        ("\n\r\t\u00a0  \u2009   \f abcDEfabcdeFAbcdefabcdefABCdefAb\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", uuid.UUID('abcdefab-cdef-abcd-efab-cdefabcdefab')),
        ("\n\r\t\u00a0  \u2009   \f ABCDEFABCDEFABCDEFABCDEFABCDEFAB\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", uuid.UUID('abcdefab-cdef-abcd-efab-cdefabcdefab')),
        ("\n\r\t\u00a0  \u2009   \f urn:uuid:{{}}{{}{-----a---b-cdef-a-b-cd-efab-c----defa-bcde-f-a-bcde-f-ab-----{}}{}{{{}\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", uuid.UUID('abcdefab-cdef-abcd-efab-cdefabcdefab')),
        ("\n\r\t\u00a0  \u2009   \f URN:UUID:{{}}{{}{-----a---b-cdef-a-b-cd-EFAB-C----DEFA-BCDE-f-a-bcde-f-ab-----{}}{}{{{}\x85   \u202f\n\x1d\x1e\x1c\t\r\n\u2029\u2029\v\v\v   ", uuid.UUID('abcdefab-cdef-abcd-efab-cdefabcdefab')),
        (None, InputDataTypeNotInAllowlistExc),
        (True, InputDataTypeNotInAllowlistExc),
        (False, InputDataTypeNotInAllowlistExc),
        (-1, InputDataTypeNotInAllowlistExc),
        (0, InputDataTypeNotInAllowlistExc),
        (1, InputDataTypeNotInAllowlistExc),
        (-1.5, InputDataTypeNotInAllowlistExc),
        (-1.0, InputDataTypeNotInAllowlistExc),
        (-0.0, InputDataTypeNotInAllowlistExc),
        (0.0, InputDataTypeNotInAllowlistExc),
        (1.0, InputDataTypeNotInAllowlistExc),
        (1.5, InputDataTypeNotInAllowlistExc),
        (float("inf"), InputDataTypeNotInAllowlistExc),
        (float("nan"), InputDataTypeNotInAllowlistExc),
        (1+2j, InputDataTypeNotInAllowlistExc),
        (b'', InputDataTypeNotInAllowlistExc),
        (b'12345678-1234-5678-1234-567812345678', InputDataTypeNotInAllowlistExc),
        (b'12345678123456781234567812345678', InputDataTypeNotInAllowlistExc),
        (b'{12345678-1234-5678-1234-567812345678}', InputDataTypeNotInAllowlistExc),
        (bytearray(b''), InputDataTypeNotInAllowlistExc),
        (bytearray(b'12345678-1234-5678-1234-567812345678'), InputDataTypeNotInAllowlistExc),
        (bytearray(b'12345678123456781234567812345678'), InputDataTypeNotInAllowlistExc),
        (bytearray(b'{12345678-1234-5678-1234-567812345678}'), InputDataTypeNotInAllowlistExc),
        ([], InputDataTypeNotInAllowlistExc),
        (["12345678-1234-5678-1234-567812345678"], InputDataTypeNotInAllowlistExc),
        ({}, InputDataTypeNotInAllowlistExc),
        ({"12345678-1234-5678-1234-567812345678": "12345678-1234-5678-1234-567812345678"}, InputDataTypeNotInAllowlistExc),
        (str, InputDataTypeNotInAllowlistExc),
        (theoretical_testutils.EmptyObject, InputDataTypeNotInAllowlistExc),
        (datetime.datetime.now(), InputDataTypeNotInAllowlistExc),
        (datetime.datetime.now().date(), InputDataTypeNotInAllowlistExc),
        (datetime.datetime.now().time(), InputDataTypeNotInAllowlistExc),
        (ipaddress.ip_address("127.7.8.9"), InputDataTypeNotInAllowlistExc),
        (ipaddress.ip_address("::1"), InputDataTypeNotInAllowlistExc),
        (ipaddress.ip_network("127.0.0.0/8"), InputDataTypeNotInAllowlistExc),
        (ipaddress.ip_network("2001:db8::/64"), InputDataTypeNotInAllowlistExc),
        (urllib.parse.urlparse("12345678-1234-5678-1234-567812345678"), InputDataTypeNotInAllowlistExc),
        (theoretical_testutils.EmptyObject(), InputDataTypeNotInAllowlistExc),
        (theoretical_testutils.TestException(), InputDataTypeNotInAllowlistExc),
        (object(), InputDataTypeNotInAllowlistExc),
        (StringableObject("12345678-1234-5678-1234-567812345678"), InputDataTypeNotInAllowlistExc),
        (StringableObject("12345678123456781234567812345678"), InputDataTypeNotInAllowlistExc),
        (StringableObject("{12345678-1234-5678-1234-567812345678}"), InputDataTypeNotInAllowlistExc),
        (StringableObject(None), InputDataTypeNotInAllowlistExc),
        (StringableObject(theoretical_testutils.EmptyObject()), InputDataTypeNotInAllowlistExc),
        (ExceptionRaisingStringableObject(), InputDataTypeNotInAllowlistExc),
    )),
)


@pytest.mark.parametrize(("blueprint", "input_", "output"), theoretical_testutils.test_function_parameter_generator(__UUID_BLUEPRINT_TEST_SUITE))
def test_uuid_blueprint(blueprint, input_, output):
    theoretical_testutils.perform_test(blueprint, input_, output)
