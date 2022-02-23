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


from typing import final, Final, Union, Any, Tuple, Type, Sequence, Optional
import ipaddress
from datalidator.blueprints.DefaultBlueprintWithModeSupportImplBase import DefaultBlueprintWithModeSupportImplBase
from datalidator.blueprints.ParsingMode import ParsingMode
from datalidator.filters.FilterIface import FilterIface
from datalidator.validators.ValidatorIface import ValidatorIface


__all__ = "IPNetworkBlueprint",


class IPNetworkBlueprint(DefaultBlueprintWithModeSupportImplBase[Union[ipaddress.IPv4Network, ipaddress.IPv6Network]]):
    """
    INPUT in loose mode:
    - any object that can be passed to ipaddress.ip_network()

    INPUT in rational mode:
    - 'ipaddress.IPv4Network' object
    - 'ipaddress.IPv6Network' object
    - 'str' object containing a string representation of an IPv4/IPv6 network (e.g. '127.0.0.0/8')

    INPUT in strict mode:
    - 'ipaddress.IPv4Network' object
    - 'ipaddress.IPv6Network' object

    OUTPUT:
    - either an 'ipaddress.IPv4Network' or 'ipaddress.IPv6Network' object, depending on which IP family the input data represented
    """

    __slots__ = "__ignore_set_host_bits",

    __RATIONAL_MODE_DATA_TYPE_ALLOWLIST: Final[Tuple[Type, ...]] = (ipaddress.IPv4Network, ipaddress.IPv6Network, str)
    __STRICT_MODE_DATA_TYPE_ALLOWLIST: Final[Tuple[Type, ...]] = (ipaddress.IPv4Network, ipaddress.IPv6Network)

    def __init__(self,
                 ignore_set_host_bits: bool = False,
                 filters: Sequence[FilterIface[Union[ipaddress.IPv4Network, ipaddress.IPv6Network]]] = (),
                 validators: Sequence[ValidatorIface[Union[ipaddress.IPv4Network, ipaddress.IPv6Network]]] = (),
                 parsing_mode: ParsingMode = DefaultBlueprintWithModeSupportImplBase._DEFAULT_PARSING_MODE,
                 tag: str = ""):
        DefaultBlueprintWithModeSupportImplBase.__init__(self, filters, validators, parsing_mode, tag)

        self.__ignore_set_host_bits: Final[bool] = ignore_set_host_bits

    @final
    def are_set_host_bits_ignored(self) -> bool:
        return self.__ignore_set_host_bits

    def _get_allowed_output_data_types(self) -> Optional[Tuple[Type, ...]]:
        return ipaddress.IPv4Network, ipaddress.IPv6Network

    def _parse_in_loose_mode(self, input_data: Any) -> Union[ipaddress.IPv4Network, ipaddress.IPv6Network]:
        return self.__convert_input_data_to_ip_network_object(input_data)

    def _parse_in_rational_mode(self, input_data: Any) -> Union[ipaddress.IPv4Network, ipaddress.IPv6Network]:
        return self._data_conversion_helper.convert_input_with_data_type_allowlist(
            self.__convert_input_data_to_ip_network_object_with_additional_checks,
            self.__class__.__RATIONAL_MODE_DATA_TYPE_ALLOWLIST,
            input_data
        )

    def _parse_in_strict_mode(self, input_data: Any) -> Union[ipaddress.IPv4Network, ipaddress.IPv6Network]:
        return self._data_conversion_helper.convert_input_with_data_type_allowlist(
            self.__convert_input_data_to_ip_network_object_with_additional_checks,
            self.__class__.__STRICT_MODE_DATA_TYPE_ALLOWLIST,
            input_data
        )

    # In contrast to the __convert_input_data_to_ip_network_object() method, this method contains some additional checks
    #  which are required in rational and strict mode.
    @final
    def __convert_input_data_to_ip_network_object_with_additional_checks(self, input_data: Any) -> Union[ipaddress.IPv4Network, ipaddress.IPv6Network]:
        # The ipaddress.ip_network() function accepts plain IP addresses, from which it makes /32 (IPv4) or /128 (IPv6)
        #  networks. Since this behaviour can be considered unexpected, it is prevented by this check:
        if isinstance(input_data, str) and ("/" not in input_data):
            raise self._invalid_input_data_exc_factory.generate_invalid_input_data_exc(
                "A '/' character is not present in the supplied string representation of an IP network: {}".format(repr(input_data)),
                input_data
            )

        return self.__convert_input_data_to_ip_network_object(input_data)

    # This method is called in loose mode or after the additional checks
    #  (in the __convert_input_data_to_ip_network_object_with_additional_checks() method) were performed.
    @final
    def __convert_input_data_to_ip_network_object(self, input_data: Any) -> Union[ipaddress.IPv4Network, ipaddress.IPv6Network]:
        # The documentation of ipaddress.IPv4Network and ipaddress.IPv6Network states the following:
        # "If strict is True and host bits are set in the supplied address, then ValueError is raised. Otherwise, the
        #  host bits are masked out to determine the appropriate network address."
        ip_network_strict_mode = not self.__ignore_set_host_bits

        original_input_data = input_data
        if isinstance(input_data, str):
            input_data = input_data.strip()

        try:
            # The documentation states that the ipaddress.ip_network() function returns either an ipaddress.IPv4Network
            #  or ipaddress.IPv6Network object.
            return ipaddress.ip_network(input_data, strict=ip_network_strict_mode)
        except Exception:
            raise self._invalid_input_data_exc_factory.generate_input_data_not_convertible_exc(
                (ipaddress.IPv4Network, ipaddress.IPv6Network), original_input_data
            )
