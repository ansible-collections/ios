#
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The ios_l3_interfaces class
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to it's desired end-state is
created
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.utils.utils import (
    validate_n_expand_ipv4,
    validate_ipv6,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.resource_module import (
    ResourceModule,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.facts import (
    Facts,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.l3_interfaces import (
    L3_InterfacesTemplate,
)


class L3_Interfaces(ResourceModule):
    """
    The ios_l3_interfaces class
    """

    gather_subset = ["!all", "!min"]

    parsers = ["ipv4", "ipv6"]

    def __init__(self, module):
        super(L3_Interfaces, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="l3_interfaces",
            tmplt=L3_InterfacesTemplate(),
        )

    def execute_module(self):
        """ Execute the module

        :rtype: A dictionary
        :returns: The result from module execution
        """
        if self.state not in ["parsed", "gathered"]:
            self.generate_commands()
            self.run_commands()
        return self.result

    def generate_commands(self):
        """ Generate configuration commands to send based on
            want, have and desired state.
        """
        if self.want:
            wantd = {}
            for each in self.want:
                wantd.update({each["name"]: each})
        else:
            wantd = {}
        if self.have:
            haved = {}
            for each in self.have:
                haved.update({each["name"]: each})
        else:
            haved = {}

        for each in wantd, haved:
            self.list_to_dict(each)

        # if state is merged, merge want onto have and then compare
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        # if state is deleted, limit the have to anything in want
        # set want to nothing
        if self.state == "deleted":
            temp = {}
            for k, v in iteritems(haved):
                if k in wantd or not wantd:
                    temp.update({k: v})
            haved = temp
            wantd = {}

        # delete processes first so we do run into "more than one" errors
        if self.state in ["overridden", "deleted"]:
            for k, have in iteritems(haved):
                if k not in wantd and (have.get("ipv4") or have.get("ipv6")):
                    self.addcmd(have, "name", False)
                    self.delete_l3_attributes(have)

        for k, want in iteritems(wantd):
            self._compare(want=want, have=haved.pop(k, {}))

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
           populates the list of commands to be run by comparing
           the `want` and `have` data with the `parsers` defined
           for the Bgp_address_family network resource.
        """
        if want != have and self.state != "deleted":
            self.addcmd(want or have, "name", False)
            if want.get("ipv4"):
                for k, v in iteritems(want["ipv4"]):
                    if have.get("ipv4") and have["ipv4"].get(k):
                        h_val = have["ipv4"].pop(k)
                        if v["address"] != "dhcp":
                            v["address"] = validate_n_expand_ipv4(
                                self._module, v
                            )
                            h_val["address"] = validate_n_expand_ipv4(
                                self._module, h_val
                            )
                        self.compare(
                            self.parsers,
                            want={"ipv4": v},
                            have={"ipv4": h_val},
                        )
                    else:
                        if v["address"] != "dhcp":
                            v["address"] = validate_n_expand_ipv4(
                                self._module, v
                            )
                        self.compare(
                            self.parsers, want={"ipv4": v}, have=dict()
                        )
            elif want.get("ipv6"):
                for k, v in iteritems(want["ipv6"]):
                    if have.get("ipv6") and have["ipv6"].get(k):
                        h_val = have["ipv6"].pop(k)
                        if "/" in v["address"] and "/" in h_val["address"]:
                            validate_ipv6(v["address"], self._module)
                            validate_ipv6(h_val["address"], self._module)
                        self.compare(
                            self.parsers,
                            want={"ipv6": v},
                            have={"ipv6": h_val},
                        )
                    else:
                        if "/" in v["address"]:
                            validate_ipv6(v["address"], self._module)
                        self.compare(
                            self.parsers, want={"ipv6": v}, have=dict()
                        )
        if self.state == "replaced" or self.state == "overridden":
            self.delete_l3_attributes(have)

    def delete_l3_attributes(self, have):
        if have.get("ipv4"):
            for k, v in iteritems(have["ipv4"]):
                if v["address"] != "dhcp":
                    v["address"] = validate_n_expand_ipv4(self._module, v)
                self.compare(
                    parsers=self.parsers, want=dict(), have={"ipv4": v}
                )
        elif have.get("ipv6"):
            for k, v in iteritems(have["ipv6"]):
                self.compare(
                    parsers=self.parsers, want=dict(), have={"ipv6": v}
                )

    def list_to_dict(self, param):
        if param:
            for key, val in iteritems(param):
                if "ipv4" in val:
                    temp = {}
                    for each in val["ipv4"]:
                        temp.update({each["address"]: each})
                    val["ipv4"] = temp
                if "ipv6" in val:
                    temp = {}
                    for each in val["ipv6"]:
                        temp.update({each["address"]: each})
                    val["ipv6"] = temp
