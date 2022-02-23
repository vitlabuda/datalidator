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


import abc
from datalidator.exc.utils.OriginatorTagCarrierMixin import OriginatorTagCarrierMixin


__all__ = "DatalidatorExc",


class DatalidatorExc(Exception, OriginatorTagCarrierMixin, metaclass=abc.ABCMeta):
    """
    A superclass of all exceptions raised by Datalidator.
    Never raised directly - only its subclasses are raised.

    One should catch exceptions that inherit from this class in the vast majority of cases because they can commonly
     occur even when one is using the library in a completely correct way - for example when invalid input data are
     passed to a blueprint's use() method (which is something that will happen if this library is used to handle
     untrusted user input in any way).
    """

    def __init__(self, error_message: str, originator_tag: str):  # = The error message is mandatory
        Exception.__init__(self, error_message)
        OriginatorTagCarrierMixin.__init__(self, originator_tag)
