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


from typing import final, Generic, TypeVar
import abc
from datalidator.DefaultDatalidatorObjectImplBase import DefaultDatalidatorObjectImplBase
from datalidator.exc.DatalidatorExc import DatalidatorExc
from datalidator.exc.err.DatalidatorError import DatalidatorError
from datalidator.validators.ValidatorIface import ValidatorIface
from datalidator.validators.exc.DataValidationFailedExc import DataValidationFailedExc
from datalidator.validators.exc.UnexpectedExceptionRaisedInValidatorExc import UnexpectedExceptionRaisedInValidatorExc


__all__ = "DefaultValidatorImplBase", "DefaultValidatorImplBase_T"
DefaultValidatorImplBase_T = TypeVar("DefaultValidatorImplBase_T")


class DefaultValidatorImplBase(ValidatorIface[DefaultValidatorImplBase_T], DefaultDatalidatorObjectImplBase, Generic[DefaultValidatorImplBase_T], metaclass=abc.ABCMeta):
    """
    The default implementation of ValidatorIface.

    All validators that ship with this library are subclasses of this base class.
    When implementing your own validators, you may choose to either inherit from this class as well (this is the easier
     way) or implement ValidatorIface yourselves.
    """

    __slots__ = ()

    def __init__(self, tag: str = ""):
        DefaultDatalidatorObjectImplBase.__init__(self, tag)

    @final
    def validate(self, data: DefaultValidatorImplBase_T) -> None:
        # For possible future expansion.
        return self.__validate_in_exception_handling_context(data)

    @final
    def __validate_in_exception_handling_context(self, data: DefaultValidatorImplBase_T) -> None:
        try:
            return self._validate(data)
        except (DatalidatorExc, DatalidatorError) as e:
            raise e
        except Exception as f:
            raise UnexpectedExceptionRaisedInValidatorExc("{}: {}".format(f.__class__.__name__, str(f)), self._tag, f)

    @abc.abstractmethod
    def _validate(self, data: DefaultValidatorImplBase_T) -> None:
        """
        Checks whether 'data' meet the validator's requirements. If not, 'DataValidationFailedExc' must get raised (the
         '_generate_data_validation_failed_exc()' method of this class should be used to instantiate it), but in the
         vast majority of cases, you should catch its base superclass, 'DatalidatorExc', because other exceptions
         extending the superclass may get raised as well (for example when the validation process fails). See the
         exception hierarchy document for more information.

        This method is called by the @final validate() method which is reserved for possible future expansion.

        :param data: The parsed data (i.e. NOT the untrusted input data!) to check.
        :raises DatalidatorExc: The superclass of all exceptions raised by this library.
        """

        raise NotImplementedError(DefaultValidatorImplBase._validate.__qualname__)

    @final
    def _generate_data_validation_failed_exc(self, error_message: str) -> DataValidationFailedExc:  # DP: Factory
        return DataValidationFailedExc(error_message, self._tag)
