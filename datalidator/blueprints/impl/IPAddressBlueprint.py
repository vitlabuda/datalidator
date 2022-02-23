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


from typing import final, Final, Tuple, Union, Any, Type, Optional
import ipaddress
from datalidator.blueprints.DefaultBlueprintWithModeSupportImplBase import DefaultBlueprintWithModeSupportImplBase


__all__ = "IPAddressBlueprint",


class IPAddressBlueprint(DefaultBlueprintWithModeSupportImplBase[Union[ipaddress.IPv4Address, ipaddress.IPv6Address]]):
    """
    INPUT in loose mode:
    - any object that can be passed to ipaddress.ip_address()

    INPUT in rational mode:
    - 'ipaddress.IPv4Address' object
    - 'ipaddress.IPv6Address' object
    - 'str' object containing a string representation of an IPv4/IPv6 address

    INPUT in strict mode:
    - 'ipaddress.IPv4Address' object
    - 'ipaddress.IPv6Address' object

    OUTPUT:
    - either an 'ipaddress.IPv4Address' or 'ipaddress.IPv6Address' object, depending on which IP family the input data represented
    """

    __slots__ = ()

    __RATIONAL_MODE_DATA_TYPE_ALLOWLIST: Final[Tuple[Type, ...]] = (ipaddress.IPv4Address, ipaddress.IPv6Address, str)
    __STRICT_MODE_DATA_TYPE_ALLOWLIST: Final[Tuple[Type, ...]] = (ipaddress.IPv4Address, ipaddress.IPv6Address)

    def _get_allowed_output_data_types(self) -> Optional[Tuple[Type, ...]]:
        return ipaddress.IPv4Address, ipaddress.IPv6Address

    def _parse_in_loose_mode(self, input_data: Any) -> Union[ipaddress.IPv4Address, ipaddress.IPv6Address]:
        return self.__convert_input_data_to_ip_address_object(input_data)

    def _parse_in_rational_mode(self, input_data: Any) -> Union[ipaddress.IPv4Address, ipaddress.IPv6Address]:
        return self._data_conversion_helper.convert_input_with_data_type_allowlist(
            self.__convert_input_data_to_ip_address_object, self.__class__.__RATIONAL_MODE_DATA_TYPE_ALLOWLIST, input_data
        )

    def _parse_in_strict_mode(self, input_data: Any) -> Union[ipaddress.IPv4Address, ipaddress.IPv6Address]:
        return self._data_conversion_helper.convert_input_with_data_type_allowlist(
            self.__convert_input_data_to_ip_address_object, self.__class__.__STRICT_MODE_DATA_TYPE_ALLOWLIST, input_data
        )

    @final
    def __convert_input_data_to_ip_address_object(self, input_data: Any) -> Union[ipaddress.IPv4Address, ipaddress.IPv6Address]:
        original_input_data = input_data
        if isinstance(input_data, str):
            input_data = input_data.strip()

        try:
            # The documentation states that the ipaddress.ip_address() function returns either an ipaddress.IPv4Address
            #  or ipaddress.IPv6Address object.
            return ipaddress.ip_address(input_data)
        except Exception:
            raise self._invalid_input_data_exc_factory.generate_input_data_not_convertible_exc(
                (ipaddress.IPv4Address, ipaddress.IPv6Address), original_input_data
            )
