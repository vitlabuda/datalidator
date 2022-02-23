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


from typing import final, Final, Optional, Any, List, Generic, Callable, TypeVar
from datalidator.filters.DefaultFilterImplBase import DefaultFilterImplBase
from datalidator.filters.exc.SortingFailedInFilterExc import SortingFailedInFilterExc


__all__ = "ListSortFilter", "ListSortFilter_T"
ListSortFilter_T = TypeVar("ListSortFilter_T")


class ListSortFilter(DefaultFilterImplBase[List[ListSortFilter_T]], Generic[ListSortFilter_T]):
    """
    Returns a new list which contains the input list's items in a sorted order.
    It uses the built-in sorted() function; therefore, the input list remains unmodified.
    """

    __slots__ = "__comparison_key_extraction_function", "__reverse_order"

    def __init__(self, comparison_key_extraction_function: Optional[Callable[[ListSortFilter_T], Any]] = None, reverse_order: bool = False, tag: str = ""):
        DefaultFilterImplBase.__init__(self, tag)

        # Used by the sorted() function.
        self.__comparison_key_extraction_function: Final[Optional[Callable[[ListSortFilter_T], Any]]] = comparison_key_extraction_function
        self.__reverse_order: Final[bool] = reverse_order

    @final
    def get_comparison_key_extraction_function(self) -> Optional[Callable[[ListSortFilter_T], Any]]:
        return self.__comparison_key_extraction_function

    @final
    def is_order_reversed(self) -> bool:
        return self.__reverse_order

    def _filter(self, data: List[ListSortFilter_T]) -> List[ListSortFilter_T]:
        try:
            return sorted(data, key=self.__comparison_key_extraction_function, reverse=self.__reverse_order)
        except Exception as e:
            raise SortingFailedInFilterExc("An exception occurred while sorting the input list!", self._tag, e)
