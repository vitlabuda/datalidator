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


from typing import TypeVar, Generic, Any
import abc
from datalidator.DatalidatorObjectIface import DatalidatorObjectIface


__all__ = "BlueprintIface", "BlueprintIface_T"
BlueprintIface_T = TypeVar("BlueprintIface_T")


class BlueprintIface(DatalidatorObjectIface, Generic[BlueprintIface_T], metaclass=abc.ABCMeta):
    """
    The interface of all blueprints.

    The purpose of blueprints is to safely and reliably parse untrusted input data to a specific blueprint's output
     data type and raise an appropriate exception if it is not possible (i.e. blueprints must be able to react to input
     data of any type and value without getting into an unexpected state under regular conditions). If applicable,
     blueprints should also be capable of running the parsed data through filters and validators.

    Blueprints MUST be thread-safe and SHOULD be immutable (i.e. it should not be possible to *knowingly* change the
     internal state of a blueprint instance after its initialization).
    """

    __slots__ = ()

    @abc.abstractmethod
    def use(self, input_data: Any) -> BlueprintIface_T:
        """
        Converts untrusted (!) 'input_data' into output data of generic type 'VT' in an appropriate way, and if
         applicable, runs the output data through a user-provided sequence of filters and validators.

        If possible, the output should not be the same instance as input and the output's type should not be a subclass
         of the desired output type (to prevent subclasses which are not respecting Liskov substitution principle
         from being returned and then breaking the program which is using the blueprint).

        Since 'input_data' are untrusted and can be of any data type, blueprints should ensure that they can properly
         handle the data's unexpected behaviour. This includes being able to catch and handle unexpected exceptions
         ('DefaultBlueprintImplBase' already does this, but it should be considered only a last resort solution - if
         you expect that something may go wrong, you should handle it properly yourselves!).

        :param input_data: The untrusted input data to be converted to output data (which can then be optionally filtered and validated).
        :return: The output data of generic type 'VT'.
        :raises DatalidatorExc: The superclass of all exceptions raised by this library.
        """

        raise NotImplementedError(BlueprintIface.use.__qualname__)
