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


from typing import final, Any, Generic, TypeVar
import abc
from datalidator.DefaultDatalidatorObjectImplBase import DefaultDatalidatorObjectImplBase
from datalidator.exc.DatalidatorExc import DatalidatorExc
from datalidator.exc.err.DatalidatorError import DatalidatorError
from datalidator.blueprints.BlueprintIface import BlueprintIface
from datalidator.blueprints.exc.UnexpectedExceptionRaisedInBlueprintExc import UnexpectedExceptionRaisedInBlueprintExc


__all__ = "DefaultBlueprintImplBase", "DefaultBlueprintImplBase_T"
DefaultBlueprintImplBase_T = TypeVar("DefaultBlueprintImplBase_T")


class DefaultBlueprintImplBase(BlueprintIface[DefaultBlueprintImplBase_T], DefaultDatalidatorObjectImplBase, Generic[DefaultBlueprintImplBase_T], metaclass=abc.ABCMeta):
    """
    The default implementation of BlueprintIface.

    All blueprints that ship with this library are subclasses of this base class.
    When implementing your own blueprints, you may choose to either inherit from this class as well (this is the easier
     way) or implement BlueprintIface yourselves.
    """

    __slots__ = ()

    def __init__(self, tag: str = ""):
        DefaultDatalidatorObjectImplBase.__init__(self, tag)

    @final
    def use(self, input_data: Any) -> DefaultBlueprintImplBase_T:
        # For possible future expansion.
        return self.__use_in_exception_handling_context(input_data)

    @final
    def __use_in_exception_handling_context(self, input_data: Any) -> DefaultBlueprintImplBase_T:
        try:
            return self._use(input_data)
        except (DatalidatorExc, DatalidatorError) as e:
            raise e
        except Exception as f:
            raise UnexpectedExceptionRaisedInBlueprintExc("{}: {}".format(f.__class__.__name__, str(f)), self._tag, f)

    @abc.abstractmethod
    def _use(self, input_data: Any) -> DefaultBlueprintImplBase_T:
        """
        Converts untrusted (!) 'input_data' into output data of generic type 'VT' in an appropriate way, and if
         applicable, runs the output data through a user-provided sequence of filters and validators.

        If possible, the output should not be the same instance as input and the output's type should not be a subclass
         of the desired output type (to prevent subclasses which are not respecting Liskov substitution principle
         from being returned and then breaking the program which is using the blueprint).

        Since 'input_data' are untrusted and can be of any data type, blueprints should ensure that they can properly
         handle the data's unexpected behaviour. This includes being able to catch and handle unexpected exceptions.
         This method runs in a context where all exceptions other than 'DatalidatorExc' and its subclasses are caught
         and handled (by raising 'UnexpectedExceptionRaisedExc', a subclass of 'DatalidatorExc'). However, this
         behaviour should be considered only a last resort solution of the problem when everything else fails - if you
         expect that something may go wrong, you should handle it properly yourselves!

        :param input_data: The untrusted input data to be converted to output data (which can then be optionally filtered and validated).
        :return: The output data of generic type 'VT'.
        :raises DatalidatorExc: The superclass of all exceptions raised by this library.
        """

        raise NotImplementedError(DefaultBlueprintImplBase._use.__qualname__)
