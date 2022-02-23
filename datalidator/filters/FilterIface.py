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


__all__ = "FilterIface", "FilterIface_T"
FilterIface_T = TypeVar("FilterIface_T")


class FilterIface(DatalidatorObjectIface, Generic[FilterIface_T], metaclass=abc.ABCMeta):
    """
    The interface of all filters.

    The purpose of filters is to modify data already parsed by a blueprint (i.e. NOT the untrusted input data!) in some
     way without changing their data type.

    Filters MUST be thread-safe and SHOULD be immutable (i.e. it should not be possible to *knowingly* change the
     internal state of a filter instance after its initialization).
    """

    __slots__ = ()

    @abc.abstractmethod
    def filter(self, data: FilterIface_T) -> FilterIface_T:
        """
        Filters 'data', i.e. modifies them in a way specific for each concrete filter class, and returns the result.
        The return value must be of the same type as the 'data' argument (not even its subclass)!

        :param data: The parsed data (i.e. NOT the untrusted input data!) to filter.
        :return: The filtered data (must be of the same data type as the 'data' argument).
        :raises DatalidatorExc: The superclass of all exceptions raised by this library.
        """

        raise NotImplementedError(FilterIface.filter.__qualname__)
