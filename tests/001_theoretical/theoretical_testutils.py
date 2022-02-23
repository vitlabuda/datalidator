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


import inspect
import pytest


class EmptyObject:
    __slots__ = ()

    def __init__(self):
        pass

    def __eq__(self, other):
        return isinstance(other, self.__class__)


class TestException(Exception):
    pass


def test_function_parameter_generator(test_suite):
    for blueprint, tested_values in test_suite:
        if inspect.isgeneratorfunction(tested_values):
            tested_values = tested_values()

        for input_, output in tested_values:
            yield blueprint, input_, output


def perform_test(blueprint, input_, output, compare_using_is: bool = False):
    if isinstance(output, type) and issubclass(output, BaseException):
        with pytest.raises(output):
            blueprint.use(input_)
    elif inspect.isfunction(output):
        assert output(blueprint.use(input_))
    elif compare_using_is:
        assert blueprint.use(input_) is output
    else:
        assert blueprint.use(input_) == output
