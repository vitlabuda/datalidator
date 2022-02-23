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
from datalidator.blueprints.ParsingMode import ParsingMode
from datalidator.blueprints.impl.StringBlueprint import StringBlueprint
from datalidator.blueprints.impl.IntegerBlueprint import IntegerBlueprint
from datalidator.blueprints.impl.ObjectBlueprint import ObjectBlueprint
from datalidator.blueprints.impl.ListBlueprint import ListBlueprint
from datalidator.blueprints.specialimpl.JSONBlueprint import JSONBlueprint
from datalidator.blueprints.extras.ObjectModel import ObjectModel
from datalidator.blueprints.exc.InputDataTypeNotInAllowlistExc import InputDataTypeNotInAllowlistExc
from datalidator.blueprints.exc.InputDataNotConvertibleExc import InputDataNotConvertibleExc
from datalidator.filters.impl.StringStripFilter import StringStripFilter
from datalidator.filters.impl.StringDeduplicateWhitespaceFilter import StringDeduplicateWhitespaceFilter
from datalidator.filters.impl.StringUnicodeNormalizeFilter import StringUnicodeNormalizeFilter
from datalidator.filters.impl.ListSortFilter import ListSortFilter
from datalidator.validators.impl.IntegerIsPositiveValidator import IntegerIsPositiveValidator
from datalidator.validators.impl.NumberMaximumValueValidator import NumberMaximumValueValidator
from datalidator.validators.impl.SequenceIsNotEmptyValidator import SequenceIsNotEmptyValidator
from datalidator.validators.impl.SequenceMaximumLengthValidator import SequenceMaximumLengthValidator
from datalidator.validators.impl.StringContainsNoControlOrSeparatorCharactersValidator import StringContainsNoControlOrSeparatorCharactersValidator
from datalidator.validators.impl.StringMatchesRegexValidator import StringMatchesRegexValidator


class Comment(ObjectModel):
    postId = IntegerBlueprint(
        validators=(
            IntegerIsPositiveValidator(),
            NumberMaximumValueValidator(2**31 - 1)
        ),
        parsing_mode=ParsingMode.MODE_STRICT
    )

    id = IntegerBlueprint(
        validators=(
            IntegerIsPositiveValidator(),
            NumberMaximumValueValidator(2**31 - 1)
        ),
        parsing_mode=ParsingMode.MODE_STRICT
    )

    name = StringBlueprint(
        filters=(
            StringStripFilter(),
            StringDeduplicateWhitespaceFilter(),
            StringUnicodeNormalizeFilter()
        ),
        validators=(
            SequenceIsNotEmptyValidator(),
            SequenceMaximumLengthValidator(100),
            StringContainsNoControlOrSeparatorCharactersValidator(allowed_characters=" ")
        ),
        parsing_mode=ParsingMode.MODE_STRICT
    )

    email = StringBlueprint(
        filters=(
            StringStripFilter(),
        ),
        validators=(
            SequenceIsNotEmptyValidator(),
            SequenceMaximumLengthValidator(100),
            StringMatchesRegexValidator(regex_pattern=r'^[A-Za-z0-9._-]+@[A-Za-z0-9.-]+\.[A-Za-z]+\Z')
        ),
        parsing_mode=ParsingMode.MODE_STRICT
    )

    body = StringBlueprint(
        filters=(
            StringStripFilter(),
            StringDeduplicateWhitespaceFilter(),
            StringUnicodeNormalizeFilter()
        ),
        validators=(
            SequenceIsNotEmptyValidator(),
            SequenceMaximumLengthValidator(500),
            StringContainsNoControlOrSeparatorCharactersValidator(allowed_characters=" \n")
        ),
        parsing_mode=ParsingMode.MODE_STRICT
    )


def check_comment(comment: Comment) -> None:
    assert comment.__class__ is Comment
    assert comment.postId.__class__ is int
    assert comment.id.__class__ is int
    assert comment.name.__class__ is str
    assert comment.email.__class__ is str
    assert comment.body.__class__ is str


def test_jsonplaceholder_comments():
    response = real_testutils.make_api_request("https://jsonplaceholder.typicode.com/comments")

    response_blueprint = JSONBlueprint(
        wrapped_blueprint=ListBlueprint(
            item_blueprint=ObjectBlueprint(Comment, ignore_input_keys_which_are_not_in_model=False),
            filters=(
                ListSortFilter(comparison_key_extraction_function=lambda comment_instance: comment_instance.id, reverse_order=False),
            ),
            validators=(
                SequenceIsNotEmptyValidator(),
                SequenceMaximumLengthValidator(1000)
            )
        )
    )

    parsed_response = response_blueprint.use(response)
    assert parsed_response.__class__ is list
    for comment in parsed_response:
        check_comment(comment)


def test_jsonplaceholder_invalid_blueprint_for_comments():
    response = real_testutils.make_api_request("https://jsonplaceholder.typicode.com/comments")

    response_blueprint = JSONBlueprint(
        wrapped_blueprint=StringBlueprint(parsing_mode=ParsingMode.MODE_STRICT),
    )

    with pytest.raises(InputDataTypeNotInAllowlistExc):
        response_blueprint.use(response)


@pytest.mark.parametrize("comment_id", (1, 17, 100, 387, 499, 500))
def test_jsonplaceholder_single_comment(comment_id):
    response = real_testutils.make_api_request("https://jsonplaceholder.typicode.com/comments/{}".format(comment_id))

    response_blueprint = JSONBlueprint(
        wrapped_blueprint=ObjectBlueprint(Comment, ignore_input_keys_which_are_not_in_model=False)
    )

    comment = response_blueprint.use(response)
    check_comment(comment)
    assert comment.id == comment_id


@pytest.mark.parametrize("comment_id", (1, 17, 100, 387, 499, 500))
def test_jsonplaceholder_invalid_blueprint_for_single_comment(comment_id):
    response = real_testutils.make_api_request("https://jsonplaceholder.typicode.com/comments/{}".format(comment_id))

    response_blueprint = JSONBlueprint(
        wrapped_blueprint=IntegerBlueprint(parsing_mode=ParsingMode.MODE_LOOSE),
    )

    with pytest.raises(InputDataNotConvertibleExc):
        response_blueprint.use(response)
