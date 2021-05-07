#
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The ios_acls class
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to it's desired end-state is
created
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import copy
from ansible.module_utils.six import iteritems
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.facts import (
    Facts,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.acls import (
    AclsTemplate,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.resource_module import (
    ResourceModule,
)


class Acls(ResourceModule):
    """
    The ios_acls class
    """

    gather_subset = ["!all", "!min"]

    gather_network_resources = ["acls"]

    parsers = ["aces"]

    def __init__(self, module):
        super(Acls, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="acls",
            tmplt=AclsTemplate(),
        )

    def execute_module(self):
        """ Execute the module

        :rtype: A dictionary
        :returns: The result from moduel execution
        """
        self.gen_config()
        self.run_commands()
        return self.result

    def gen_config(self):
        """ Select the appropriate function based on the state provided
        :rtype: A list
        :returns: the commands necessary to migrate the current configuration
        to the desired configuration
        """

        if self.want:
            wantd = self.want
        else:
            wantd = {}
        if self.have:
            haved = self.have
        else:
            haved = {}

        haved = self.list_to_dict(haved)
        self.update_sequence_in_want(wantd, haved)
        wantd = self.list_to_dict(wantd)

        # if state is merged, merge want onto have and then compare
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        # if state is deleted, empty out wantd and set haved to wantd
        if self.state == "deleted":
            for k, v in iteritems(haved):
                afi = k
                afi_want = wantd.get(k)
                if (afi_want and not afi_want.get("acls")) or not wantd:
                    for key, val in iteritems(v["acls"]):
                        val.update({"afi": afi, "name": key})
                        self.addcmd(val, "acls_name", True)
                elif afi_want:
                    for key, val in iteritems(v["acls"]):
                        want_acl = afi_want["acls"].get(key)
                        if want_acl:
                            val.update({"afi": afi, "name": key})
                            self.addcmd(val, "acls_name", True)

        # remove superfluous config for overridden and deleted
        if self.state == "overridden":
            for k, v in iteritems(haved):
                afi = k
                afi_want = wantd.get(k)
                for key, val in iteritems(v["acls"]):
                    if afi_want:
                        acls_want = afi_want["acls"].get(key, {})
                        if not acls_want:
                            val.update({"afi": afi, "name": key})
                            self.addcmd(val, "acls_name", True)
                    else:
                        val.update({"afi": afi, "name": key})
                        self.addcmd(val, "acls_name", True)

        for k, want in iteritems(wantd):
            want.update({"afi": k})
            self._compare(want=want, have=haved.pop(k, {}))

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
           populates the list of commands to be run by comparing
           the `want` and `have` data with the `parsers` defined
           for the acls network resource.
        """

        if want != have and self.state != "deleted":
            if want.get("acls"):
                afi = want["afi"]
                for k, v in iteritems(want["acls"]):
                    if have.get("acls") and k in have["acls"]:
                        cmd_len = len(self.commands)
                        have_acl = have["acls"].pop(k, {})
                        if have_acl:
                            for key, val in iteritems(v.get("aces")):
                                have_ace = have_acl["aces"].pop(key, {})
                                if val.get("protocol_options"):
                                    if not val.get("protocol") and (
                                        list(val.get("protocol_options"))[0]
                                        == have_ace.get("protocol")
                                    ):
                                        have_ace.pop("protocol")
                                if have_ace and val != have_ace:
                                    self.compare(
                                        parsers=self.parsers,
                                        want=dict(),
                                        have={"aces": have_ace, "afi": afi},
                                    )
                                    self.compare(
                                        parsers=self.parsers,
                                        want={
                                            "aces": val,
                                            "afi": afi,
                                            "acl_type": v.get("acl_type"),
                                        },
                                        have={"aces": have_ace, "afi": afi},
                                    )
                                elif not have_ace:
                                    self.compare(
                                        parsers=self.parsers,
                                        want={"aces": val, "afi": afi},
                                        have=dict(),
                                    )
                        if (
                            self.state == "overridden"
                            or self.state == "replaced"
                        ):
                            if have_acl.get("aces"):
                                for key, val in iteritems(have_acl["aces"]):
                                    self.compare(
                                        parsers=self.parsers,
                                        want=dict(),
                                        have={"aces": val, "afi": afi},
                                    )
                        if cmd_len != len(self.commands):
                            command = self.acl_name_config_cmd(
                                name=k, afi=afi, acl_type=v.get("acl_type")
                            )
                            self.commands.insert(cmd_len, command)
                    else:
                        cmd_len = len(self.commands)
                        for key, val in iteritems(v.get("aces")):
                            self.compare(
                                parsers=self.parsers,
                                want={
                                    "aces": val,
                                    "afi": afi,
                                    "acl_type": v.get("acl_type"),
                                },
                                have=dict(),
                            )
                        if cmd_len != self.commands:
                            command = self.acl_name_config_cmd(
                                name=k, afi=afi, acl_type=v.get("acl_type")
                            )
                            self.commands.insert(cmd_len, command)

    def update_sequence_in_want(self, want, have):
        if (want and not have) or (not want and have):
            return want
        else:
            temp_acl = {}
            count = 0
            for each in want:
                if each.get("acls"):
                    have_each = have.get(each["afi"])
                    temp_acl["acls"] = []
                    for acl in each["acls"]:
                        temp_ace = []
                        have_aces = None
                        if have_each:
                            have_acls = have_each.get("acls")
                        if acl.get("aces"):
                            if have_acls:
                                have_aces = have_acls.get(acl["name"])
                            for every in acl["aces"]:
                                if every.get("sequence"):
                                    temp_ace.append(every)
                                else:
                                    if have_aces:
                                        for key, val in iteritems(
                                            have_aces["aces"]
                                        ):
                                            temp = copy.copy(val)
                                            seq = temp.pop("sequence")
                                            protocol = (
                                                temp.pop("protocol")
                                                if temp.get("protocol")
                                                else None
                                            )
                                            if temp == every:
                                                if protocol:
                                                    every.update(
                                                        {
                                                            "protocol": protocol,
                                                            "sequence": seq,
                                                        }
                                                    )
                                                else:
                                                    every.update(
                                                        {"sequence": seq}
                                                    )
                                                temp_ace.append(every)
                                    else:
                                        temp_ace.append(every)
                        if have_aces:
                            aces = {
                                "aces": temp_ace,
                                "acl_type": have_aces.get("acl_type"),
                                "name": acl["name"],
                            }
                        elif acl.get("acl_type"):
                            aces = {
                                "aces": temp_ace,
                                "acl_type": acl["acl_type"],
                                "name": acl["name"],
                            }
                        else:
                            aces = {"aces": temp_ace, "name": acl["name"]}
                        temp_acl["acls"].append(aces)
                temp_acl.update({"afi": each["afi"]})
                want[count] = copy.copy(temp_acl)
                count += 1

    def acl_name_config_cmd(self, name, afi, acl_type):
        if afi == "ipv4":
            if not acl_type:
                try:
                    acl_id = int(name)
                    if not acl_type:
                        if acl_id >= 1 and acl_id <= 99:
                            acl_type = "standard"
                        if acl_id >= 100 and acl_id <= 199:
                            acl_type = "extended"
                except ValueError:
                    acl_type = "extended"
            command = "ip access-list {0} {1}".format(acl_type, name)
        elif afi == "ipv6":
            command = "ipv6 access-list {0}".format(name)
        return command

    def list_to_dict(self, param):
        if param:
            temp = {}
            for each in param:
                temp_acls = {}
                if each.get("acls"):
                    acls = each.get("acls")
                    for every in acls:
                        acl_name = every.get("name")
                        temp_aces = {}
                        aces = every.get("aces")
                        if aces:
                            count = 0
                            for ace in aces:
                                seq = (
                                    ace["sequence"]
                                    if ace.get("sequence")
                                    else count
                                )
                                temp_aces.update(
                                    {acl_name + "_" + str(seq): ace}
                                )
                                count += 1
                        if every.get("acl_type"):
                            temp_acls.update(
                                {
                                    acl_name: {
                                        "aces": temp_aces,
                                        "acl_type": every["acl_type"],
                                    }
                                }
                            )
                        else:
                            temp_acls.update({acl_name: {"aces": temp_aces}})
                each["acls"] = temp_acls
                temp.update({each["afi"]: {"acls": temp_acls}})
            return temp
        else:
            return dict()
