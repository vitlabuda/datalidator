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


import os
import os.path
import sys
if "DATALIDATOR_TESTS_AUTOPATH" in os.environ:
    __TESTS_DIR = os.path.dirname(os.path.realpath(__file__))
    __MODULE_DIR = os.path.realpath(os.path.join(__TESTS_DIR, "../.."))
    if __TESTS_DIR not in sys.path:
        sys.path.insert(0, __TESTS_DIR)
    if __MODULE_DIR not in sys.path:
        sys.path.insert(0, __MODULE_DIR)

import pytest
import configparser
import ipaddress
from datalidator.blueprints.ParsingMode import ParsingMode
from datalidator.blueprints.impl.StringBlueprint import StringBlueprint
from datalidator.blueprints.impl.IntegerBlueprint import IntegerBlueprint
from datalidator.blueprints.impl.BooleanBlueprint import BooleanBlueprint
from datalidator.blueprints.impl.IPAddressBlueprint import IPAddressBlueprint
from datalidator.blueprints.impl.UnixFilesystemPathBlueprint import UnixFilesystemPathBlueprint
from datalidator.blueprints.impl.ObjectBlueprint import ObjectBlueprint
from datalidator.blueprints.impl.ListBlueprint import ListBlueprint
from datalidator.blueprints.specialimpl.JSONBlueprint import JSONBlueprint
from datalidator.blueprints.extras.ObjectModel import ObjectModel
from datalidator.blueprints.exc.InputDataValueNotAllowedForDataTypeExc import InputDataValueNotAllowedForDataTypeExc
from datalidator.filters.impl.StringStripFilter import StringStripFilter
from datalidator.filters.impl.UnixFilesystemPathAddTrailingSlashFilter import UnixFilesystemPathAddTrailingSlashFilter
from datalidator.filters.impl.UnixFilesystemPathStripTrailingSlashesFilter import UnixFilesystemPathStripTrailingSlashesFilter
from datalidator.filters.impl.ListDeduplicateItemsFilter import ListDeduplicateItemsFilter
from datalidator.validators.impl.AllowlistValidator import AllowlistValidator
from datalidator.validators.impl.IntegerIsPositiveValidator import IntegerIsPositiveValidator
from datalidator.validators.impl.NumberMinimumValueValidator import NumberMinimumValueValidator
from datalidator.validators.impl.NumberMaximumValueValidator import NumberMaximumValueValidator
from datalidator.validators.impl.StringMatchesRegexValidator import StringMatchesRegexValidator
from datalidator.validators.impl.IPAddressIsIPv4Validator import IPAddressIsIPv4Validator
from datalidator.validators.impl.IPAddressIsIPv6Validator import IPAddressIsIPv6Validator
from datalidator.validators.impl.IPAddressIsLoopbackValidator import IPAddressIsLoopbackValidator
from datalidator.validators.impl.IPAddressIsMulticastValidator import IPAddressIsMulticastValidator


__NAT64_INI_CONFIG = r"""
[Program]
daemonize = no
translator_threads = 4
chroot_dir = /root/nat64-chroot/
working_dir = /
pid_file = /nat64.pid
must_run_as_root = yes
privilege_drop_user = nat64usr
privilege_drop_group = nat64grp

[Logging]
destinations = ["stderr", "logfile", "syslog"]
syslog_ident = nat64
log_file = /nat64.log
log_debug_msgs = yes

[TUN]
dev_name = nat64
dev_path = /dev/net/tun
persistent = no

[Network]
prefix = 64:ff9b::
xlat_ipv4 = 192.168.64.1
xlat_ipv6 = 2001:db8:6464::1
icmp_respond_to_pings = yes
packet_tos_tc_4to6 = yes
packet_tos_tc_6to4 = yes
packet_ipv4_check_options = yes
# fragmentation modes: forbid-silent forbid passthrough
fragmentation_mode = passthrough
mtu_out_v4 = 1500
mtu_out_v6 = 1500
"""


__NAT64_JSON_CONFIG = r"""
{
  "Program": {
    "daemonize": "no",
    "translator_threads": "4",
    "chroot_dir": "/root/nat64-chroot/",
    "working_dir": "/",
    "pid_file": "/nat64.pid",
    "must_run_as_root": "yes",
    "privilege_drop_user": "nat64usr",
    "privilege_drop_group": "nat64grp"
  },
  "Logging": {
    "destinations": "[\"stderr\", \"logfile\", \"syslog\"]",
    "syslog_ident": "nat64",
    "log_file": "/nat64.log",
    "log_debug_msgs": "yes"
  },
  "TUN": {
    "dev_name": "nat64",
    "dev_path": "/dev/net/tun",
    "persistent": "no"
  },
  "Network": {
    "prefix": "64:ff9b::",
    "xlat_ipv4": "192.168.64.1",
    "xlat_ipv6": "2001:db8:6464::1",
    "icmp_respond_to_pings": "yes",
    "packet_tos_tc_4to6": "yes",
    "packet_tos_tc_6to4": "yes",
    "packet_ipv4_check_options": "yes",
    "fragmentation_mode": "passthrough",
    "mtu_out_v4": "1500",
    "mtu_out_v6": "1500"
  }
}
"""


class ProgramConfigSection(ObjectModel):
    daemonize = BooleanBlueprint(
        parsing_mode=ParsingMode.MODE_RATIONAL
    )
    translator_threads = IntegerBlueprint(
        validators=(IntegerIsPositiveValidator(), NumberMaximumValueValidator(256)),
        parsing_mode=ParsingMode.MODE_RATIONAL
    )
    chroot_dir = UnixFilesystemPathBlueprint(
        filters=(UnixFilesystemPathAddTrailingSlashFilter(),)
    )
    working_dir = UnixFilesystemPathBlueprint(
        filters=(UnixFilesystemPathAddTrailingSlashFilter(),)
    )
    pid_file = UnixFilesystemPathBlueprint(
        filters=(UnixFilesystemPathStripTrailingSlashesFilter(),)
    )
    must_run_as_root = BooleanBlueprint(
        parsing_mode=ParsingMode.MODE_RATIONAL
    )
    privilege_drop_user = StringBlueprint(
        filters=(StringStripFilter(),),
        validators=(StringMatchesRegexValidator(r'^[a-z][0-9a-z-]{0,31}\Z'),),
        parsing_mode=ParsingMode.MODE_RATIONAL
    )
    privilege_drop_group = StringBlueprint(
        filters=(StringStripFilter(),),
        validators=(StringMatchesRegexValidator(r'^[a-z][0-9a-z-]{0,31}\Z'),),
        parsing_mode=ParsingMode.MODE_RATIONAL
    )


class LoggingConfigSection(ObjectModel):
    destinations = JSONBlueprint(
        wrapped_blueprint=ListBlueprint(
            item_blueprint=StringBlueprint(
                validators=(AllowlistValidator(allowlist=["stderr", "logfile", "syslog"]),),
                parsing_mode=ParsingMode.MODE_STRICT
            ),
            filters=(ListDeduplicateItemsFilter(),),
            parsing_mode=ParsingMode.MODE_STRICT
        ),
    )
    syslog_ident = StringBlueprint(
        filters=(StringStripFilter(),),
        validators=(StringMatchesRegexValidator(r'^[a-z][0-9a-z-]{0,31}\Z'),),
        parsing_mode=ParsingMode.MODE_RATIONAL
    )
    log_file = UnixFilesystemPathBlueprint(
        filters=(UnixFilesystemPathStripTrailingSlashesFilter(),)
    )
    log_debug_msgs = BooleanBlueprint(parsing_mode=ParsingMode.MODE_RATIONAL)


class TUNConfigSection(ObjectModel):
    dev_name = StringBlueprint(
        filters=(StringStripFilter(),),
        validators=(StringMatchesRegexValidator(r'^[a-z][0-9a-z-]{0,31}\Z'),),
        parsing_mode=ParsingMode.MODE_RATIONAL
    )
    dev_path = UnixFilesystemPathBlueprint(
        filters=(UnixFilesystemPathStripTrailingSlashesFilter(),)
    )
    persistent = BooleanBlueprint(parsing_mode=ParsingMode.MODE_RATIONAL)


class NetworkConfigSection(ObjectModel):
    prefix = IPAddressBlueprint(
        validators=(
            IPAddressIsIPv6Validator(),
            IPAddressIsLoopbackValidator(negate=True),
            IPAddressIsMulticastValidator(negate=True)
        ),
        parsing_mode=ParsingMode.MODE_RATIONAL
    )
    xlat_ipv4 = IPAddressBlueprint(
        validators=(
            IPAddressIsIPv4Validator(),
            IPAddressIsLoopbackValidator(negate=True),
            IPAddressIsMulticastValidator(negate=True)
        ),
        parsing_mode=ParsingMode.MODE_RATIONAL
    )
    xlat_ipv6 = IPAddressBlueprint(
        validators=(
            IPAddressIsIPv6Validator(),
            IPAddressIsLoopbackValidator(negate=True),
            IPAddressIsMulticastValidator(negate=True)
        ),
        parsing_mode=ParsingMode.MODE_RATIONAL
    )
    icmp_respond_to_pings = BooleanBlueprint(
        parsing_mode=ParsingMode.MODE_RATIONAL
    )
    packet_tos_tc_4to6 = BooleanBlueprint(
        parsing_mode=ParsingMode.MODE_RATIONAL
    )
    packet_tos_tc_6to4 = BooleanBlueprint(
        parsing_mode=ParsingMode.MODE_RATIONAL
    )
    packet_ipv4_check_options = BooleanBlueprint(
        parsing_mode=ParsingMode.MODE_RATIONAL
    )
    fragmentation_mode = StringBlueprint(
        filters=(StringStripFilter(),),
        validators=(AllowlistValidator(allowlist=["forbid-silent", "forbid", "passthrough"]),),
        parsing_mode=ParsingMode.MODE_RATIONAL
    )
    mtu_out_v4 = IntegerBlueprint(
        validators=(NumberMinimumValueValidator(68), NumberMaximumValueValidator(65535)),
        parsing_mode=ParsingMode.MODE_RATIONAL
    )
    mtu_out_v6 = IntegerBlueprint(
        validators=(NumberMinimumValueValidator(1280), NumberMaximumValueValidator(65535)),
        parsing_mode=ParsingMode.MODE_RATIONAL
    )


class NAT64Config(ObjectModel):
    Program = ObjectBlueprint(ProgramConfigSection, ignore_input_keys_which_are_not_in_model=False)
    Logging = ObjectBlueprint(LoggingConfigSection, ignore_input_keys_which_are_not_in_model=False)
    TUN = ObjectBlueprint(TUNConfigSection, ignore_input_keys_which_are_not_in_model=False)
    Network = ObjectBlueprint(NetworkConfigSection, ignore_input_keys_which_are_not_in_model=False)


def check_nat64_config(nat64_config):
    expected_nat64_config = NAT64Config(
        Program=ProgramConfigSection(
            daemonize=False,
            translator_threads=4,
            chroot_dir="/root/nat64-chroot/",
            working_dir="/",
            pid_file="/nat64.pid",
            must_run_as_root=True,
            privilege_drop_user="nat64usr",
            privilege_drop_group="nat64grp"
        ),
        Logging=LoggingConfigSection(
            destinations=["stderr", "logfile", "syslog"],
            syslog_ident="nat64",
            log_file="/nat64.log",
            log_debug_msgs=True
        ),
        TUN=TUNConfigSection(
            dev_name="nat64",
            dev_path="/dev/net/tun",
            persistent=False
        ),
        Network=NetworkConfigSection(
            prefix=ipaddress.IPv6Address("64:ff9b::"),
            xlat_ipv4=ipaddress.IPv4Address("192.168.64.1"),
            xlat_ipv6=ipaddress.IPv6Address("2001:db8:6464::1"),
            icmp_respond_to_pings=True,
            packet_tos_tc_4to6=True,
            packet_tos_tc_6to4=True,
            packet_ipv4_check_options=True,
            fragmentation_mode="passthrough",
            mtu_out_v4=1500,
            mtu_out_v6=1500
        )
    )

    assert nat64_config.__class__ is NAT64Config
    assert nat64_config == expected_nat64_config


def test_nat64_ini_config():
    parser = configparser.ConfigParser()  # configparser.ConfigParser() is a mapping
    parser.read_string(__NAT64_INI_CONFIG)

    config_blueprint = ObjectBlueprint(NAT64Config, ignore_input_keys_which_are_not_in_model=True)

    nat64_config = config_blueprint.use(parser)
    check_nat64_config(nat64_config)


def test_nat64_json_config():
    config_blueprint = JSONBlueprint(
        wrapped_blueprint=ObjectBlueprint(NAT64Config, ignore_input_keys_which_are_not_in_model=False)
    )

    nat64_config = config_blueprint.use(__NAT64_JSON_CONFIG)
    check_nat64_config(nat64_config)


@pytest.mark.parametrize("config_string", (__NAT64_INI_CONFIG, __NAT64_JSON_CONFIG))
def test_nat64_config_with_invalid_blueprint(config_string):
    config_blueprint = BooleanBlueprint(parsing_mode=ParsingMode.MODE_RATIONAL)

    with pytest.raises(InputDataValueNotAllowedForDataTypeExc):
        config_blueprint.use(config_string)
