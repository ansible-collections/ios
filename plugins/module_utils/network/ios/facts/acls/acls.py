# pylint: skip-file
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The ios_acls fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type


from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.acls.acls import (
    AclsArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.acls import (
    AclsTemplate,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network_template import (
    NetworkTemplate,
)


class AclsFacts(object):
    """ The ios_acls fact class
    """

    def __init__(self, module, subspec="config", options="options"):

        self._module = module
        self.argument_spec = AclsArgs.argument_spec

    def get_acl_data(self, connection):
        # Get the access-lists from the ios router
        return connection.get("sh access-list")

    def populate_facts(self, connection, ansible_facts, data=None):
        """ Populate the facts for acls
        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf
        :rtype: dictionary
        :returns: facts
        """

        if not data:
            data = self.get_acl_data(connection)

        rmmod = NetworkTemplate(lines=data.splitlines(), tmplt=AclsTemplate())
        current = rmmod.parse()

        temp_v4 = []
        temp_v6 = []
        if current.get("acls"):
            for k, v in iteritems(current.get("acls")):
                if v.get("afi") == "ipv4":
                    del v["afi"]
                    temp_v4.append(v)
                elif v.get("afi") == "ipv6":
                    del v["afi"]
                    temp_v6.append(v)
            temp_v4 = sorted(temp_v4, key=lambda i: str(i["name"]))
            temp_v6 = sorted(temp_v6, key=lambda i: str(i["name"]))
            for each in temp_v4:
                aces_ipv4 = each.get("aces")
                if aces_ipv4:
                    for each_ace in each.get("aces"):
                        if each["acl_type"] == "standard":
                            each_ace["source"] = each_ace.pop("std_source")
                        if each_ace.get("icmp_igmp_tcp_protocol"):
                            each_ace["protocol_options"] = {
                                each_ace["protocol"]: {
                                    each_ace.pop(
                                        "icmp_igmp_tcp_protocol"
                                    ).replace("-", "_"): True
                                }
                            }
                        if each_ace.get("std_source") == {}:
                            del each_ace["std_source"]
            for each in temp_v6:
                aces_ipv6 = each.get("aces")
                if aces_ipv6:
                    for each_ace in each.get("aces"):
                        if each_ace.get("std_source") == {}:
                            del each_ace["std_source"]
                        if each_ace.get("icmp_igmp_tcp_protocol"):
                            each_ace["protocol_options"] = {
                                each_ace["protocol"]: {
                                    each_ace.pop(
                                        "icmp_igmp_tcp_protocol"
                                    ).replace("-", "_"): True
                                }
                            }

        objs = []
        if temp_v4:
            objs.append({"afi": "ipv4", "acls": temp_v4})
        if temp_v6:
            objs.append({"afi": "ipv6", "acls": temp_v6})

        facts = {}
        if objs:
            facts["acls"] = []
            params = utils.validate_config(
                self.argument_spec, {"config": objs}
            )
            for cfg in params["config"]:
                facts["acls"].append(utils.remove_empties(cfg))
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
