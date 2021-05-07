# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The acls parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""
import re
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network_template import (
    NetworkTemplate,
)


def _tmplt_l3_interfaces(config_data):
    if config_data.get("ipv4"):
        cmd = "ip address {address}".format(**config_data["ipv4"])
        if config_data["ipv4"].get("secondary"):
            cmd += " secondary"
        if config_data["ipv4"].get("dhcp_client"):
            cmd += " client-id GigabitEthernet 0/{dhcp_client}".format(
                **config_data["ipv4"]
            )
        if config_data["ipv4"].get("dhcp_hostname"):
            cmd += " hostname {dhcp_hostname}".format(**config_data["ipv4"])
    elif config_data.get("ipv6"):
        cmd = "ipv6 address {address}".format(**config_data["ipv6"])
    return cmd


class L3_InterfacesTemplate(NetworkTemplate):
    def __init__(self, lines=None):
        super(L3_InterfacesTemplate, self).__init__(lines=lines, tmplt=self)

    PARSERS = [
        {
            "name": "name",
            "getval": re.compile(
                r"""^interface*
                    \s*(?P<name>\S+)
                    *$""",
                re.VERBOSE,
            ),
            "compval": "name",
            "setval": "interface {{ name }}",
            "result": {"{{ name }}": {"name": "{{ name }}"}},
            "shared": True,
        },
        {
            "name": "ipv4",
            "getval": re.compile(
                r"""\s+ip\saddress*
                    \s*(?P<ipv4>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\ssecondary|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})*
                    \s*(?P<ipv4_dhcp>dhcp\sclient-id\s\S+\shostname\s\S+|dhcp\sclient-id\s\S+|dhcp\shostname\s\S+|dhcp)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_l3_interfaces,
            "compval": "ipv4",
            "result": {
                "{{ name }}": {
                    "ipv4": [
                        {
                            "address": "{{ ipv4.split(' ')[0] if ipv4 is defined }}",
                            "netmask": "{{ ipv4.split(' ')[1] if ipv4 is defined }}",
                            "secondary": "{{ True if ipv4 is defined and 'secondary' in ipv4 }}",
                            "dhcp_client": "{{ ipv4_dhcp.split('/')[1].split(' ')[0] if ipv4_dhcp is defined and 'client-id' in ipv4_dhcp }}",
                            "dhcp_hostname": "{{ ipv4_dhcp.split('hostname ')[1] if ipv4_dhcp is defined and 'hostname' in ipv4_dhcp }}",
                        }
                    ]
                }
            },
        },
        {
            "name": "ipv6",
            "getval": re.compile(
                r"""\s+ipv6\saddress*
                    \s*((?P<ipv6>(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))\S+))
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_l3_interfaces,
            "compval": "ipv6",
            "result": {"{{ name }}": {"ipv6": [{"address": "{{ ipv6 }}"}]}},
        },
    ]
