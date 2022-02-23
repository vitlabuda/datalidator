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

import real_testutils
import pytest
import datetime
import urllib.parse
from datalidator.blueprints.ParsingMode import ParsingMode
from datalidator.blueprints.impl.StringBlueprint import StringBlueprint
from datalidator.blueprints.impl.IntegerBlueprint import IntegerBlueprint
from datalidator.blueprints.impl.URLBlueprint import URLBlueprint
from datalidator.blueprints.impl.DatetimeBlueprint import DatetimeBlueprint
from datalidator.blueprints.impl.ObjectBlueprint import ObjectBlueprint
from datalidator.blueprints.specialimpl.NoneHandlingBlueprint import NoneHandlingBlueprint
from datalidator.blueprints.specialimpl.BlueprintChainingBlueprint import BlueprintChainingBlueprint
from datalidator.blueprints.specialimpl.JSONBlueprint import JSONBlueprint
from datalidator.blueprints.extras.ObjectModel import ObjectModel
from datalidator.blueprints.exc.InputDataNotConvertibleExc import InputDataNotConvertibleExc
from datalidator.filters.impl.StringStripFilter import StringStripFilter
from datalidator.filters.impl.StringDeduplicateWhitespaceFilter import StringDeduplicateWhitespaceFilter
from datalidator.filters.impl.StringUnicodeNormalizeFilter import StringUnicodeNormalizeFilter
from datalidator.filters.impl.StringReplaceFilter import StringReplaceFilter
from datalidator.filters.impl.DatetimeChangeTimezoneFilter import DatetimeChangeTimezoneFilter
from datalidator.validators.impl.IntegerIsPositiveValidator import IntegerIsPositiveValidator
from datalidator.validators.impl.IntegerIsZeroOrPositiveValidator import IntegerIsZeroOrPositiveValidator
from datalidator.validators.impl.SequenceIsNotEmptyValidator import SequenceIsNotEmptyValidator
from datalidator.validators.impl.SequenceMaximumLengthValidator import SequenceMaximumLengthValidator
from datalidator.validators.impl.StringMatchesRegexValidator import StringMatchesRegexValidator
from datalidator.validators.impl.StringContainsNoControlOrSeparatorCharactersValidator import StringContainsNoControlOrSeparatorCharactersValidator
from datalidator.validators.impl.DatetimeIsAwareValidator import DatetimeIsAwareValidator


__TESTED_USERNAMES = (
    "vitlabuda",
    "torvalds",
    "gregkh",
)


class User(ObjectModel):
    id = IntegerBlueprint(
        validators=(IntegerIsPositiveValidator(),),
        parsing_mode=ParsingMode.MODE_STRICT
    )

    login = StringBlueprint(
        validators=(StringMatchesRegexValidator(r'^[0-9a-zA-Z_-]{1,100}\Z'),),
        parsing_mode=ParsingMode.MODE_STRICT
    )

    html_url = URLBlueprint()

    repos_url = URLBlueprint()

    name = StringBlueprint(
        filters=(
            StringStripFilter(),
            StringDeduplicateWhitespaceFilter(),
            StringUnicodeNormalizeFilter(normal_form="NFKC")
        ),
        validators=(
            StringContainsNoControlOrSeparatorCharactersValidator(allowed_characters=" "),
            StringMatchesRegexValidator(r'^[\w-]{1,50} [\w-]{1,50}\Z'),
            StringMatchesRegexValidator(r'[0-9_]', negate=True)
        ),
        parsing_mode=ParsingMode.MODE_STRICT
    )

    email = NoneHandlingBlueprint(
        wrapped_blueprint=StringBlueprint(
            filters=(StringStripFilter(),),
            validators=(
                SequenceIsNotEmptyValidator(),
                SequenceMaximumLengthValidator(128),
                StringMatchesRegexValidator(r'^[A-Za-z0-9._-]+@[A-Za-z0-9.-]+\.[A-Za-z]+\Z'),
            ),
            parsing_mode=ParsingMode.MODE_STRICT
        )
    )

    public_repos = IntegerBlueprint(
        validators=(IntegerIsZeroOrPositiveValidator(),),
        parsing_mode=ParsingMode.MODE_STRICT
    )

    public_gists = IntegerBlueprint(
        validators=(IntegerIsZeroOrPositiveValidator(),),
        parsing_mode=ParsingMode.MODE_STRICT
    )

    followers = IntegerBlueprint(
        validators=(IntegerIsZeroOrPositiveValidator(),),
        parsing_mode=ParsingMode.MODE_STRICT
    )

    following = IntegerBlueprint(
        validators=(IntegerIsZeroOrPositiveValidator(),),
        parsing_mode=ParsingMode.MODE_STRICT
    )

    created_at = BlueprintChainingBlueprint(blueprint_chain=[
        StringBlueprint(
            filters=(StringReplaceFilter("Z", "+00:00"),),
            parsing_mode=ParsingMode.MODE_STRICT
        ),
        DatetimeBlueprint(
            validators=(DatetimeIsAwareValidator(),),
            parsing_mode=ParsingMode.MODE_STRICT
        ),
        DatetimeBlueprint(
            filters=(DatetimeChangeTimezoneFilter(new_timezone=datetime.timezone.utc),),
            parsing_mode=ParsingMode.MODE_STRICT
        )
    ])


@pytest.mark.parametrize("username", __TESTED_USERNAMES)
def test_github_user(username):
    response = real_testutils.make_api_request("https://api.github.com/users/{}".format(username))

    response_blueprint = JSONBlueprint(
        wrapped_blueprint=ObjectBlueprint(User, ignore_input_keys_which_are_not_in_model=True)
    )

    user_info: User = response_blueprint.use(response)
    assert user_info.__class__ is User
    assert user_info.id.__class__ is int
    assert user_info.login.__class__ is str
    assert user_info.login == username
    assert user_info.html_url.__class__ is urllib.parse.ParseResult
    assert username in urllib.parse.urlunparse(user_info.html_url)  # noqa
    assert user_info.repos_url.__class__ is urllib.parse.ParseResult
    assert username in urllib.parse.urlunparse(user_info.repos_url)   # noqa
    assert user_info.name.__class__ is str
    assert (user_info.email is None) or (user_info.email.__class__ is str)
    assert user_info.public_repos.__class__ is int
    assert user_info.public_gists.__class__ is int
    assert user_info.followers.__class__ is int
    assert user_info.following.__class__ is int
    assert user_info.created_at.__class__ is datetime.datetime


@pytest.mark.parametrize("username", __TESTED_USERNAMES)
def test_github_invalid_blueprint_for_user(username):
    response = real_testutils.make_api_request("https://api.github.com/users/{}".format(username))

    response_blueprint = IntegerBlueprint(parsing_mode=ParsingMode.MODE_RATIONAL)

    with pytest.raises(InputDataNotConvertibleExc):
        response_blueprint.use(response)
