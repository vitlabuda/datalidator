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


from typing import final, Union
import ipaddress
from datalidator.validators.DefaultValidatorWithNegationSupportImplBase import DefaultValidatorWithNegationSupportImplBase


__all__ = "IPAddressIsMulticastValidator",


class IPAddressIsMulticastValidator(DefaultValidatorWithNegationSupportImplBase[Union[ipaddress.IPv4Address, ipaddress.IPv6Address]]):
    """
    POSITIVE VALIDATION (default; negate=False):
     The input IPv4/IPv6 address is valid if it belongs to the multicast address space.

    NEGATIVE VALIDATION (negate=True):
     The input IPv4/IPv6 address is valid if it does not belong to the multicast address space.

    NOTE: The IPv4Address/IPv6Address's 'is_multicast' property is used to determine whether the input IP address is multicast or not.
    """

    # Despite the fact that some IP address validators are very similar to each other, I still decided to implement
    #  them in separate classes because this way, they are easier to use (there is no need for an enum etc.), even
    #  though the DRY principle is not being strictly followed.

    __slots__ = ()

    def _validate_positively(self, data: Union[ipaddress.IPv4Address, ipaddress.IPv6Address]) -> None:  # IP is multicast? -> Valid
        if self.__is_ip_address_multicast(data):
            return

        raise self._generate_data_validation_failed_exc("The input IP address is not a multicast address: {}".format(str(data)))

    def _validate_negatively(self, data: Union[ipaddress.IPv4Address, ipaddress.IPv6Address]) -> None:  # IP is not multicast? -> Valid
        if self.__is_ip_address_multicast(data):
            raise self._generate_data_validation_failed_exc("The input IP address is a multicast address: {}".format(str(data)))

    @final
    def __is_ip_address_multicast(self, ip_address: Union[ipaddress.IPv4Address, ipaddress.IPv6Address]) -> bool:
        return ip_address.is_multicast
