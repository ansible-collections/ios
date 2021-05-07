#
# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The cisco.ios_bgp_address_family config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.resource_module import (
    ResourceModule,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.facts import (
    Facts,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.bgp_address_family import (
    Bgp_AddressFamilyTemplate,
)
#import q

class Bgp_AddressFamily(ResourceModule):
    """
    The cisco.ios_bgp_address_family config class
    """

    gather_subset = ["!all", "!min"]

    parsers = [
        "as_number",
        "afi",
        "default",
        "default_metric",
        "distance",
        "table_map",
    ]

    def __init__(self, module):
        super(Bgp_AddressFamily, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="bgp_address_family",
            tmplt=Bgp_AddressFamilyTemplate(),
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
            wantd = {self.want["as_number"]: self.want}
        else:
            wantd = dict()
        if self.have:
            haved = {self.have["as_number"]: self.have}
        else:
            haved = dict()
        #q(wantd, haved)
        for each in wantd, haved:
            self.list_to_dict(each)

        # if state is merged, merge want onto have and then compare
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)
            if len(wantd) > 1:
                self._module.fail_json(
                    msg="BGP is already running. Only one BGP instance is allowed per device."
                )
        # if state is deleted, empty out wantd and set haved to wantd
        if self.state == "deleted":
            as_number = None
            if wantd:
                temp = dict()
                for key, val in iteritems(haved):
                    as_number = key
                    if wantd.get(key):
                        for k, v in iteritems(val.get("address_family")):
                            w = wantd[key].get("address_family")
                            if k in w:
                                temp.update({k: v})
                    val["address_family"] = temp
            elif haved:
                as_number = list(haved)[0]
                temp = {}
                for k, v in iteritems(haved):
                    if not wantd:
                        temp.update({k: v})
                haved = temp
            wantd = dict()
            for k, have in iteritems(haved):
                if k not in wantd:
                    self._compare(want=wantd, have=have, as_number=as_number)

        # remove superfluous config for overridden
        if self.state == "overridden":
            for key, have in iteritems(haved):
                if wantd.get(key):
                    for k, v in iteritems(have.get("address_family")):
                        w = wantd[key].get("address_family")
                        if k not in w:
                            self._compare(
                                want=dict(),
                                have={"address_family": {k: v}},
                                as_number=key,
                            )

        for k, want in iteritems(wantd):
            self._compare(want=want, have=haved.pop(k, dict()), as_number=k)
        # q(self.commands)
        # self.commands = []

    def _compare(self, want, have, as_number):
        """Leverages the base class `compare()` method and
           populates the list of commands to be run by comparing
           the `want` and `have` data with the `parsers` defined
           for the Bgp_address_family network resource.
        """
        if want != have and self.state != "deleted":
            self._compare_af(want, have)
        elif self.state == "deleted":
            self._delete_af(have)

        if self.commands and "router bgp" not in self.commands[0]:
            self.commands.insert(0, "router bgp {0}".format(as_number))

    def _compare_af(self, want, have):
        w = want.get("address_family", dict())
        h = have.get("address_family", dict())

        for key, val in iteritems(w):
            cmd_len = len(self.commands)
            if h.get(key):
                h_key = h.get(key)
            else:
                h_key = dict()
            if val != h_key:
                self._aggregate_address_af_config_compare(val, have=h_key)
                self._bgp_af_config_compare(val, have=h_key)
                self._compare_neighbor(val, have=h_key)
                self._compare_network(val, have=h_key)
                self._compare_snmp(val, have=h_key)
                self.compare(
                    parsers=self.parsers, want=val, have=h.pop(key, dict())
                )
            if cmd_len != len(self.commands):
                af_cmd = "address-family {afi}".format(**val)
                if val.get("safi"):
                    af_cmd += " {safi}".format(**val)
                if val.get("vrf"):
                    af_cmd += " vrf {vrf}".format(**val)
                self.commands.insert(cmd_len, af_cmd)
        if not w and self.state == "overridden":
            self._delete_af(have)

    def _aggregate_address_af_config_compare(self, want, have):
        parsers = ["aggregate_address"]
        w_aggregate_address = want.get("aggregate_address", {})
        if have:
            h_aggregate_address = have.get("aggregate_address", {})
        else:
            h_aggregate_address = {}
        for key, val in iteritems(w_aggregate_address):
            if h_aggregate_address and h_aggregate_address.get(key):
                self.compare(
                    parsers=parsers,
                    want={"aggregate_address": val},
                    have={"aggregate_address": h_aggregate_address.pop(key)},
                )
            else:
                self.compare(
                    parsers=parsers,
                    want={"aggregate_address": val},
                    have=dict(),
                )
        if self.state == "replaced" or self.state == "overridden":
            if h_aggregate_address:
                for key, val in iteritems(h_aggregate_address):
                    self.compare(
                        parsers=parsers,
                        want=dict(),
                        have={"aggregate_address": val},
                    )
            elif have.get("aggregate_address"):
                for key, val in iteritems(have.pop("aggregate_address")):
                    self.compare(
                        parsers=parsers,
                        want=dict(),
                        have={"aggregate_address": val},
                    )

    def _bgp_af_config_compare(self, want, have):
        parsers = [
            "bgp.additional_paths",
            "bgp.dampening",
            "bgp.config",
            "bgp.slow_peer",
        ]
        w_bgp = want.get("bgp", dict())
        if have:
            h_bgp = have.get("bgp", dict())
        else:
            h_bgp = dict()
        for key, val in iteritems(w_bgp):
            if h_bgp and h_bgp.get(key):
                self.compare(
                    parsers=parsers,
                    want={"bgp": {key: val}},
                    have={"bgp": {key: h_bgp.pop(key)}},
                )
            else:
                self.compare(
                    parsers=parsers, want={"bgp": {key: val}}, have=dict()
                )
        if self.state == "replaced" or self.state == "overridden":
            if h_bgp:
                for key, val in iteritems(h_bgp):
                    self.compare(
                        parsers=parsers, want=dict(), have={"bgp": {key: val}}
                    )
            elif have.get("bgp"):
                for key, val in iteritems(have.pop("bgp")):
                    self.compare(
                        parsers=parsers, want=dict(), have={"bgp": {key: val}}
                    )

    def _compare_neighbor(self, want, have):
        parsers = [
            "neighbor",
            "neighbor.prefix_list",
            "neighbor.route_map",
            "neighbor.slow_peer"
        ]
        neighbor_key = ['address', 'ipv6_address', 'tag']
        w = want.get("neighbor", {}) if want else {}
        if have:
            h = have.get("neighbor", {})
        else:
            h = {}
        for key, val in iteritems(w):
            if h and h.get(key):
                neighbor_tag = [each for each in neighbor_key if each in val][0]
                for k, v in iteritems(val):
                    if h[key].get(k) and k not in neighbor_key:
                        if k in ['prefix_list', 'route_map']:
                            for k_param, v_param in iteritems(val[k]):
                                self.compare(
                                    parsers=parsers,
                                    want={"neighbor": {neighbor_tag: val[neighbor_tag], k: v_param}},
                                    have={"neighbor": {neighbor_tag: val[neighbor_tag], k: h[key][k].pop(k_param, {})}},
                                )
                        else:
                            self.compare(
                                parsers=parsers,
                                want={"neighbor": {neighbor_tag: val[neighbor_tag], k: v}},
                                have={"neighbor": {neighbor_tag: val[neighbor_tag], k: h[key].pop(k, {})}},
                            )
                    elif k not in neighbor_key:
                        if k in ['prefix_list', 'route_map']:
                            for k_param, v_param in iteritems(val[k]):
                                self.compare(
                                    parsers=parsers,
                                    want={"neighbor": {neighbor_tag: val[neighbor_tag], k: v_param}},
                                    have=dict(),
                                )
                        else:
                            self.compare(
                                parsers=parsers,
                                want={"neighbor": {neighbor_tag: val[neighbor_tag], k: v}},
                                have=dict(),
                            )
            else:
                for param in ['prefix_list', 'route_map']:
                    if param in val:
                        for k_param, v_param in iteritems(val[param]):
                            self.compare(
                                parsers=parsers,
                                want={"neighbor": {'address': val['address'], param: v_param}},
                                have=dict(),
                            )
                        val.pop(param)
                self.compare(
                    parsers=parsers,
                    want={"neighbor": val},
                    have=dict(),
                )
        if self.state == "replaced" or self.state == "overridden":
            for key, val in iteritems(h):
                self.compare(
                    parsers=parsers, want=dict(), have={"neighbor": val}
                )
            count = 0
            remote = None
            activate = None
            for each in self.commands:
                if "no" in each and "remote-as" in each:
                    remote = count
                if "no" in each and "activate" in each:
                    activate = count
                count += 1
            if activate and activate > remote:
                if count > 0 or "activate" in self.commands[activate]:
                    self.commands.append(self.commands.pop(activate))
            if remote and activate > remote:
                if count > 0 or "remote-as" in self.commands[remote]:
                    self.commands.append(self.commands.pop(remote))

    def _compare_network(self, want, have):
        parsers = ["network"]
        w = want.get("network", dict())
        h = have.get("network", dict())
        for key, val in iteritems(w):
            if h and h.get(key):
                h_network = h.pop(key)
                if h_network != val:
                    self.compare(
                        parsers=parsers,
                        want={"network": val},
                        have={"network": val},
                    )
            else:
                self.compare(
                    parsers=parsers, want={"network": val}, have=dict()
                )
        if self.state == "replaced" or self.state == "overridden":
            for key, val in iteritems(h):
                self.compare(
                    parsers=parsers, want=dict(), have={"network": val}
                )

    def _compare_snmp(self, want, have):
        parsers = ["snmp"]
        w = want.get("snmp", dict())
        h = have.get("snmp", dict())
        if w:
            for key, val in iteritems(w["context"]):
                if h:
                    h_snmp_param = h["context"].pop(key)
                    if h_snmp_param and key != "name":
                        self.compare(
                            parsers=parsers,
                            want={
                                "snmp": {
                                    key: val,
                                    "name": w["context"]["name"],
                                }
                            },
                            have={
                                "snmp": {
                                    key: h_snmp_param,
                                    "name": w["context"]["name"],
                                }
                            },
                        )
                elif key == "community" or key == "user":
                    self.compare(
                        parsers=parsers,
                        want={
                            "snmp": {key: val, "name": w["context"]["name"]}
                        },
                        have=dict(),
                    )
        elif h and self.state == "replaced" or self.state == "overridden":
            for key, val in iteritems(h):
                self.compare(
                    parsers=parsers,
                    want=dict(),
                    have={"snmp": {key: val, "name": h["context"]["name"]}},
                )

    def _delete_af(self, have):
        h = have.get("address_family", dict())
        for key, val in iteritems(h):
            if "safi" in val and "vrf" in val:
                cmd = "no address-family {afi} {safi} vrf {vrf}".format(**val)
            elif "safi" in val:
                cmd = "no address-family {afi} {safi}".format(**val)
            else:
                cmd = "no address-family {afi}".format(**val)
            self.commands.append(cmd)

    def list_to_dict(self, param):
        if param:
            for key, val in iteritems(param):
                if val.get("address_family"):
                    temp = {}
                    for each in val.get("address_family", []):
                        temp.update(
                            {
                                each["afi"]
                                + "_"
                                + each.get("safi", "")
                                + "_"
                                + each.get("vrf", ""): each
                            }
                        )
                    val["address_family"] = temp
                    self.list_to_dict(val["address_family"])
                if "aggregate_address" in val:
                    temp = {}
                    for each in val["aggregate_address"]:
                        temp.update({each["address"]: each})
                    val["aggregate_address"] = temp
                if "bgp" in val and "slow_peer" in val["bgp"]:
                    temp = {}
                    for each in val["bgp"]["slow_peer"]:
                        temp.update({list(each)[0]: each[list(each)[0]]})
                    val["bgp"]["slow_peer"] = temp
                if "neighbor" in val:
                    for each in val["neighbor"]:
                        if each.get('prefix_list'):
                            temp = {}
                            for every in each["prefix_list"]:
                                temp.update({every['name']: every})
                            each["prefix_list"] = temp
                        if each.get('route_map'):
                            temp = {}
                            for every in each["route_map"]:
                                temp.update({every['name']: every})
                            each["route_map"] = temp
                        if each.get('slow_peer'):
                            each["slow_peer"] = {list(every)[0]: every[list(every)[0]] for every in each["slow_peer"]}
                    val["neighbor"] = {
                        each.get("address") or each.get("ipv6_address") or each.get("tag"): each for each in val.get("neighbor", [])
                    }
                if "network" in val:
                    temp = {}
                    for each in val.get("network", []):
                        temp.update({each["address"]: each})
                    val["network"] = temp
