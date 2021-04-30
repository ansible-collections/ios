#
# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The cisco.ios_route_maps config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.resource_module import (
    ResourceModule,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.facts import (
    Facts,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.route_maps import (
    Route_mapsTemplate,
)


class Route_maps(ResourceModule):
    """
    The cisco.ios_route_maps config class
    """

    parsers = ["continue_entry", "description"]

    def __init__(self, module):
        super(Route_maps, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="route_maps",
            tmplt=Route_mapsTemplate(),
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
            wantd = {(entry["route_map"]): entry for entry in self.want}
        else:
            wantd = {}
        if self.have:
            haved = {(entry["route_map"]): entry for entry in self.have}
        else:
            haved = {}

        # Convert each of config list to dict
        for each in wantd, haved:
            self.list_to_dict(each)

        # if state is merged, merge want onto have and then compare
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        # if state is deleted, empty out wantd and set haved to wantd
        if self.state == "deleted":
            haved = {
                k: v for k, v in iteritems(haved) if k in wantd or not wantd
            }
            wantd = {}

        # remove superfluous config for overridden and deleted
        if self.state in ["overridden", "deleted"]:
            for k, have in iteritems(haved):
                if k not in wantd:
                    route_map_cmd = "no route-map {route_map}".format(**have)
                    self.commands.append(route_map_cmd)

        for k, want in iteritems(wantd):
            self._compare(want=want, have=haved.pop(k, {}))

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
           populates the list of commands to be run by comparing
           the `want` and `have` data with the `parsers` defined
           for the Route_maps network resource.
        """
        if want != have and self.state != "deleted":
            self.entries_compare(want, have)

    def entries_compare(self, want, have):
        if want.get("entries"):
            cmd_len = len(self.commands)
            if have.get("entries"):
                for k, v in iteritems(want["entries"]):
                    have_entry = have["entries"].pop(k, {})
                    if have_entry and want["entries"][k] != have_entry:
                        # description gets merged with existing description, so explicit delete is required
                        # replaced and overridden state
                        if (
                            (
                                self.state == "replaced"
                                or self.state == "overridden"
                            )
                            and have_entry.get("description")
                            and have_entry.get("description")
                            != want["entries"][k].get("description")
                        ):
                            self.compare(
                                parsers=["description"],
                                want=dict(),
                                have=have_entry,
                            )
                        self.compare(
                            parsers=self.parsers,
                            want=want["entries"][k],
                            have=have_entry,
                        )
                        have_match = have_entry.get("match")
                        want_match = v.get("match")
                        if have_match and want_match:
                            self.list_type_compare(
                                "match", want=want_match, have=have_match
                            )
                        elif not have_match and want_match:
                            self.list_type_compare(
                                "match", want=want_match, have=dict()
                            )
                        have_set = have_entry.get("set")
                        want_set = v.get("set")
                        if have_set and want_set:
                            self.list_type_compare(
                                "set", want=want_set, have=have_set
                            )
                        elif not have_set and want_set:
                            self.list_type_compare(
                                "set", want=want_set, have=dict()
                            )
                    if cmd_len != len(self.commands):
                        route_map_cmd = "route-map {route_map}".format(**want)
                        if want["entries"][k].get("action"):
                            route_map_cmd += " {action}".format(
                                **want["entries"][k]
                            )
                        if want["entries"][k].get("sequence"):
                            route_map_cmd += " {sequence}".format(
                                **want["entries"][k]
                            )
                        self.commands.insert(cmd_len, route_map_cmd)
                        cmd_len = len(self.commands)
            else:
                for k, v in iteritems(want["entries"]):
                    self.compare(
                        parsers=self.parsers,
                        want=want["entries"][k],
                        have=dict(),
                    )
                    want_match = v.get("match")
                    if want_match:
                        self.list_type_compare(
                            "match", want=want_match, have=dict()
                        )
                    want_set = v.get("set")
                    if want_set:
                        self.list_type_compare(
                            "set", want=want_set, have=dict()
                        )
                    if cmd_len != len(self.commands):
                        route_map_cmd = "route-map {route_map}".format(**want)
                        if want["entries"][k].get("action"):
                            route_map_cmd += " {action}".format(
                                **want["entries"][k]
                            )
                        if want["entries"][k].get("sequence"):
                            route_map_cmd += " {sequence}".format(
                                **want["entries"][k]
                            )
                        self.commands.insert(cmd_len, route_map_cmd)
                        cmd_len = len(self.commands)
        if (
            self.state == "replaced" or self.state == "overridden"
        ) and have.get("entries"):
            cmd_len = len(self.commands)
            for k, v in iteritems(have["entries"]):
                route_map_cmd = "no route-map {route_map}".format(**have)
                if have["entries"][k].get("action"):
                    route_map_cmd += " {action}".format(**have["entries"][k])
                if have["entries"][k].get("sequence"):
                    route_map_cmd += " {sequence}".format(**have["entries"][k])
                self.commands.insert(cmd_len, route_map_cmd)

    def list_type_compare(self, compare_type, want, have):
        parsers = [
            "{0}".format(compare_type),
            "{0}.ip".format(compare_type),
            "{0}.ipv6".format(compare_type),
        ]
        for k, v in iteritems(want):
            have_v = have.pop(k, {})
            if v != have_v and k not in ["ip", "ipv6", "action", "sequence"]:
                if have_v:
                    self.compare(
                        parsers=parsers,
                        want={compare_type: {k: v}},
                        have={compare_type: {k: have_v}},
                    )
                else:
                    self.compare(
                        parsers=parsers,
                        want={compare_type: {k: v}},
                        have=dict(),
                    )
            if k in ["ip", "ipv6"]:
                for key, val in iteritems(v):
                    have_val = have_v.pop(key, {})
                    if val != have_val:
                        if have_val:
                            if (
                                self.state == "overridden"
                                or self.state == "replaced"
                            ):
                                self.compare(
                                    parsers=parsers,
                                    want=dict(),
                                    have={compare_type: {k: {key: have_val}}},
                                )
                            self.compare(
                                parsers=parsers,
                                want={compare_type: {k: {key: val}}},
                                have={compare_type: {k: {key: have_val}}},
                            )
                        else:
                            self.compare(
                                parsers=parsers,
                                want={compare_type: {k: {key: val}}},
                                have=dict(),
                            )
                if (
                    self.state == "overridden" or self.state == "replaced"
                ) and have_v:
                    for key, val in iteritems(have_v):
                        self.compare(
                            parsers=parsers,
                            want=dict(),
                            have={compare_type: {k: {key: val}}},
                        )
        if have and (self.state == "replaced" or self.state == "overridden"):
            for k, v in iteritems(have):
                if k in ["ip", "ipv6"]:
                    for key, val in iteritems(v):
                        if key and val:
                            self.compare(
                                parsers=parsers,
                                want=dict(),
                                have={compare_type: {k: {key: val}}},
                            )
                else:
                    self.compare(
                        parsers=parsers,
                        want=dict(),
                        have={compare_type: {k: v}},
                    )

    def list_to_dict(self, param):
        if param:

            def convert_to_dict(inner_match, key):
                temp = dict()
                for each in inner_match:
                    temp.update({key + "_" + str(each): each})
                return dict(sorted(temp.items(), key=lambda x: x[1]))

            for key, val in iteritems(param):
                temp_entries = dict()
                if val.get("entries"):
                    for every in val["entries"]:
                        match = every.get("match")
                        if match:
                            if match.get("as_path") and match.get(
                                "as_path"
                            ).get("acls"):
                                match["as_path"]["acls"] = convert_to_dict(
                                    match["as_path"]["acls"], "acl"
                                )
                            if match.get("community") and match.get(
                                "community"
                            ).get("name"):
                                match["community"]["name"] = convert_to_dict(
                                    match["community"]["name"], "name"
                                )
                            if match.get("extcommunity"):
                                match["extcommunity"] = convert_to_dict(
                                    match["extcommunity"], "num"
                                )
                            if match.get("interfaces"):
                                match["interfaces"] = convert_to_dict(
                                    match["interfaces"], "interface"
                                )
                            if match.get("ip"):
                                for each_ip_param in [
                                    "address",
                                    "flowspec",
                                    "next_hop",
                                    "redistribution_source",
                                    "route_source",
                                ]:
                                    if match["ip"].get(each_ip_param):
                                        if match["ip"][each_ip_param].get(
                                            "acls"
                                        ):
                                            match["ip"][each_ip_param][
                                                "acls"
                                            ] = convert_to_dict(
                                                match["ip"][each_ip_param][
                                                    "acls"
                                                ],
                                                "acl",
                                            )
                                        elif match["ip"][each_ip_param].get(
                                            "prefix_lists"
                                        ):
                                            match["ip"][each_ip_param][
                                                "prefix_lists"
                                            ] = convert_to_dict(
                                                match["ip"][each_ip_param][
                                                    "prefix_lists"
                                                ],
                                                "prefix_list",
                                            )
                            if match.get("local_preference") and match.get(
                                "local_preference"
                            ).get("value"):
                                match["local_preference"][
                                    "value"
                                ] = convert_to_dict(
                                    match["local_preference"]["value"], "value"
                                )
                            if match.get("mdt_group") and match.get(
                                "mdt_group"
                            ).get("acls"):
                                match["mdt_group"]["acls"] = convert_to_dict(
                                    match["mdt_group"]["acls"], "acl"
                                )
                            if match.get("policy_lists"):
                                match["policy_lists"] = convert_to_dict(
                                    match["policy_lists"], "policy"
                                )
                            if match.get("security_group"):
                                for each_sg_param in ["source", "destination"]:
                                    if match.get("security_group").get(
                                        each_sg_param
                                    ):
                                        match["security_group"][
                                            each_sg_param
                                        ] = convert_to_dict(
                                            match["security_group"][
                                                each_sg_param
                                            ],
                                            each_sg_param,
                                        )
                        set = every.get("set")
                        if set:
                            if set.get("interfaces"):
                                set["interfaces"] = convert_to_dict(
                                    set["interfaces"], "interface"
                                )
                        action = every.get("action")
                        sequence = every.get("sequence")
                        temp_entries.update(
                            {action + "_" + str(sequence): every}
                        )
                    val["entries"] = temp_entries
