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
from datalidator.filters.FilterIface import FilterIface
from datalidator.filters.exc.UnexpectedExceptionRaisedInFilterExc import UnexpectedExceptionRaisedInFilterExc


__all__ = "DefaultFilterImplBase", "DefaultFilterImplBase_T"
DefaultFilterImplBase_T = TypeVar("DefaultFilterImplBase_T")


class DefaultFilterImplBase(FilterIface[DefaultFilterImplBase_T], DefaultDatalidatorObjectImplBase, Generic[DefaultFilterImplBase_T], metaclass=abc.ABCMeta):
    """
    The default implementation of FilterIface.

    All filters that ship with this library are subclasses of this base class.
    When implementing your own filters, you may choose to either inherit from this class as well (this is the easier
     way) or implement FilterIface yourselves.
    """

    __slots__ = ()

    def __init__(self, tag: str = ""):
        DefaultDatalidatorObjectImplBase.__init__(self, tag)

    @final
    def filter(self, data: DefaultFilterImplBase_T) -> DefaultFilterImplBase_T:
        # For possible future expansion.
        return self.__filter_in_exception_handling_context(data)

    @final
    def __filter_in_exception_handling_context(self, data: DefaultFilterImplBase_T) -> DefaultFilterImplBase_T:
        try:
            return self._filter(data)
        except (DatalidatorExc, DatalidatorError) as e:
            raise e
        except Exception as f:
            raise UnexpectedExceptionRaisedInFilterExc("{}: {}".format(f.__class__.__name__, str(f)), self._tag, f)

    @abc.abstractmethod
    def _filter(self, data: DefaultFilterImplBase_T) -> DefaultFilterImplBase_T:
        """
        Filters 'data', i.e. modifies them in a way specific for each concrete filter class, and returns the result.
        The return value must be of the same type as the 'data' argument (not even its subclass)!

        This method is called by the @final filter() method which is reserved for possible future expansion.

        :param data: The parsed data (i.e. NOT the untrusted input data!) to filter.
        :return: The filtered data (must be of the same data type as the 'data' argument).
        :raises DatalidatorExc: The superclass of all exceptions raised by this library.
        """

        raise NotImplementedError(DefaultFilterImplBase._filter.__qualname__)
