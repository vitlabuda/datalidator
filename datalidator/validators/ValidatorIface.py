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


from typing import Generic, TypeVar
import abc
from datalidator.DatalidatorObjectIface import DatalidatorObjectIface


__all__ = "ValidatorIface", "ValidatorIface_T"
ValidatorIface_T = TypeVar("ValidatorIface_T")


class ValidatorIface(DatalidatorObjectIface, Generic[ValidatorIface_T], metaclass=abc.ABCMeta):
    """
    The interface of all validators.

    The purpose of validators is to check whether data already parsed by a blueprint and optionally filtered by
     "zero or more" filters (i.e. NOT the untrusted input data!) meet certain requirements and if not, raise an
     'DataValidationFailedExc'.

    Validators MUST be thread-safe and SHOULD be immutable (i.e. it should not be possible to *knowingly* change the
     internal state of a validator instance after its initialization).
    """

    __slots__ = ()

    @abc.abstractmethod
    def validate(self, data: ValidatorIface_T) -> None:
        """
        Checks whether 'data' meet the validator's requirements. If not, 'DataValidationFailedExc' gets raised, but in
         the vast majority of cases, you should catch its base superclass, 'DatalidatorExc', because other exceptions
         extending the superclass may get raised as well (for example when the validation process fails). See the
         exception hierarchy document for more information.

        :param data: The parsed data (i.e. NOT the untrusted input data!) to check.
        :raises DatalidatorExc: The superclass of all exceptions raised by this library.
        """

        raise NotImplementedError(ValidatorIface.validate.__qualname__)
