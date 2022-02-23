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


import enum


__all__ = "ParsingMode",


class ParsingMode(enum.Enum):
    """
    Blueprints that are subclasses of the DefaultBlueprintWithModeSupportImplBase base class allow their users to
     change what input data are they able to parse and how they do it using a 'parsing mode' initializer argument.
     There are 3 parsing modes: loose, rational and strict. They behave differently across blueprints, but their
     general ideas are as follows:

    LOOSE MODE:
    In loose mode, there is usually very little to no restriction on input data types by the blueprint and the
     success of them getting parsed usually depends only on whether the underlying functions can deal with them.
    Keep in mind that in this mode, resulting output data might seem unrelated or unexpected in relation to input data
     (for example in StringBlueprint, where the input object is simply passed to the str() function, which might result
     in unexpected strings being returned).
    In most cases, this parsing mode is not very useful in practice.

    RATIONAL MODE (default):
    In rational mode, blueprints try to provide the most sensible output data in relation to input data. Therefore,
     they usually restrict the data types accepted on input to a reasonable set.
    In addition, some blueprints are programmed to handle some input values in a specific way or are programmed to be
     able to process only a small set of input values (for example BooleanBlueprint accepts only a small set of input
     strings such as "true", "yes", "false" or "no" in this mode). This behaviour is specific for this parsing mode
     only and is not present in the other two modes.
    This is the default parsing mode which is used unless you specify a different one when instantiating a blueprint.
    In practice, using this mode is usually the most reasonable option, as it can be used to parse structured data in
     both typed (e.g. JSON) and non-typed (e.g. INI) formats. For example, IntegerBlueprint can parse numeric strings
     to integers in this mode.

    STRICT MODE:
    In strict mode, the set of accepted input data types is usually very restricted and often contains only the output
     data type (e.g. StringBlueprint only accepts 'str' objects on input). Blueprints in this mode usually also try to
     avoid losing any information when parsing the input data (e.g. IntegerBlueprint does not accept 'float' objects on
     its input as the decimal part of the number would get lost).
    In practice, this mode may be used to parse structured data in typed formats (e.g. JSON) if the rules of rational
     mode were too loose for your use case.

    Blueprints bundled with this library that have the ability to make use of parsing modes have their behaviour under
     all the parsing modes properly documented in their docstrings. It is recommended to check the documentation when
     using such blueprint in order to decide which parsing mode is the best one for your use case.
    """

    __slots__ = ()

    MODE_LOOSE = 1
    MODE_RATIONAL = 2
    MODE_STRICT = 3

    # This is used only for testing - it should never be used in production!
    _MODE_INVALID = 4
