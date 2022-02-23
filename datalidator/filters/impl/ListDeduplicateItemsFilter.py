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


from typing import List, Generic, TypeVar
from datalidator.filters.DefaultFilterImplBase import DefaultFilterImplBase


__all__ = "ListDeduplicateItemsFilter", "ListDeduplicateItemsFilter_T"
ListDeduplicateItemsFilter_T = TypeVar("ListDeduplicateItemsFilter_T")


class ListDeduplicateItemsFilter(DefaultFilterImplBase[List[ListDeduplicateItemsFilter_T]], Generic[ListDeduplicateItemsFilter_T]):
    """
    Returns a new list with unique values from the input list (= duplicate values are reduced to one such value).
    The input list remains unmodified.
    """

    __slots__ = ()

    def _filter(self, data: List[ListDeduplicateItemsFilter_T]) -> List[ListDeduplicateItemsFilter_T]:
        # Converting the input list to set and then back to list would not be possible in all cases, because the items
        #  would have to be Hashable!

        deduplicated_list = []

        for item in data:
            if item not in deduplicated_list:
                deduplicated_list.append(item)

        return deduplicated_list
