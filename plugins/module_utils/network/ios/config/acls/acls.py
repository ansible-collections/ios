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

        # if state is merged, merge want onto have and then compare
        if self.state == "merged":
            temp_have = copy.deepcopy(haved)
            temp = []
            temp_acls = {}

            for each in wantd:
                want_in_have = False
                for each_have in temp_have:
                    if each.get("afi") == each_have.get("afi"):
                        temp_acls["acls"] = []
                        for each_acls in each.get("acls"):
                            want_acls_in_have = False
                            for each_have_acls in each_have.get("acls"):
                                if each_acls["name"] == each_have_acls["name"]:
                                    aces = []
                                    if each_acls.get("aces"):
                                        for each_ace in each_acls["aces"]:
                                            each_ace_sequence = each_ace.get(
                                                "sequence"
                                            )
                                            if (
                                                each_ace_sequence
                                                and each_have_acls.get("aces")
                                            ):
                                                for (
                                                    each_have_ace
                                                ) in each_have_acls["aces"]:
                                                    if (
                                                        each_ace_sequence
                                                        == each_have_ace.get(
                                                            "sequence"
                                                        )
                                                    ):
                                                        aces.append(
                                                            dict(
                                                                dict_merge(
                                                                    each_have_ace,
                                                                    each_ace,
                                                                )
                                                            )
                                                        )
                                                        break
                                    if aces:
                                        temp_acls["acls"].append(
                                            {
                                                "aces": aces,
                                                "name": each_acls["name"],
                                            }
                                        )
                                    else:
                                        temp_acls["acls"].append(
                                            dict(
                                                dict_merge(
                                                    each_have_acls, each_acls
                                                )
                                            )
                                        )
                                    want_acls_in_have = True
                            if not want_acls_in_have:
                                temp_acls["acls"].append(each_acls)
                        temp_acls.update({"afi": each.get("afi")})
                        # temp.append(dict(dict_merge(each, each_have)))
                        temp.append(temp_acls)
                        want_in_have = True
                if not want_in_have:
                    temp.append(each)
            if temp:
                wantd = temp

        # if state is deleted, empty out wantd and set haved to wantd
        if self.state == "deleted":
            if wantd:
                for each_have in haved:
                    count = 0
                    for every_have in each_have.get("acls"):
                        del_want = False
                        for each_want in wantd:
                            want_acls = each_want.get("acls")
                            want_afi = each_want.get("afi")
                            if want_acls:
                                for every_want in each_want.get("acls"):
                                    if every_want.get(
                                        "name"
                                    ) == every_have.get("name"):
                                        del_want = True
                                        break
                            elif want_afi and want_afi == each_have["afi"]:
                                del_want = True
                        if not del_want:
                            del each_have.get("acls")[count]
                        count += 1
                wantd = {}
            for each in haved:
                for every_acls in each.get("acls"):
                    every_acls.update({"afi": each.get("afi")})
                    self.addcmd(every_acls, "acls_name", True)

        # remove superfluous config for overridden and deleted
        if self.state in ["overridden"] and wantd:
            for each_have in haved:
                count = 0
                for every_have in each_have.get("acls"):
                    del_want = False
                    for each_want in wantd:
                        for every_want in each_want.get("acls"):
                            if every_want.get("name") == every_have.get(
                                "name"
                            ):
                                del_want = True
                                break
                    if not del_want:
                        every_have.update({"afi": each_have.get("afi")})
                        self.addcmd(every_have, "acls_name", True)
                    count += 1

        for w in wantd:
            want_in_have = False
            if haved:
                for h in haved:
                    if w["afi"] == h["afi"]:
                        want_in_have = True
                        for e_w in w["acls"]:
                            set_want = True
                            for e_h in h["acls"]:
                                if e_w["name"] == e_h["name"]:
                                    e_w.update({"afi": w.get("afi")})
                                    e_h.update({"afi": h.get("afi")})
                                    self._compare(want=e_w, have=e_h)
                                    set_want = False
                                    break
                            if set_want:
                                e_w.update({"afi": w.get("afi")})
                                self._compare(want=e_w, have={})
            if not haved or not want_in_have:
                for e_w in w["acls"]:
                    e_w.update({"afi": w["afi"]})
                    self._compare(want=e_w, have={})

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
           populates the list of commands to be run by comparing
           the `want` and `have` data with the `parsers` defined
           for the Ospf_interfaces network resource.
        """
        parsers = ["aces"]

        if want.get("aces"):
            cmd_added = True
            for each in want.get("aces"):
                set_want = True
                if have.get("aces"):
                    for each_have in have.get("aces"):
                        if each.get("source") == each_have.get(
                            "source"
                        ) and each.get("destination") == each_have.get(
                            "destination"
                        ):
                            set_want = False
                            if each.get("sequence") and not each_have.get(
                                "sequence"
                            ):
                                each_have.update(
                                    {"sequence": each.get("sequence")}
                                )
                            elif not each.get("sequence") and each_have.get(
                                "sequence"
                            ):
                                each.update(
                                    {"sequence": each_have.get("sequence")}
                                )
                            if each.get("protocol") and not each_have.get(
                                "protocol"
                            ):
                                each_have.update(
                                    {"protocol": each.get("protocol")}
                                )
                            elif not each.get("protocol") and each_have.get(
                                "protocol"
                            ):
                                each.update(
                                    {"protocol": each_have.get("protocol")}
                                )
                            if each != each_have:
                                if cmd_added:
                                    self.addcmd(have, "acls_name", False)
                                    cmd_added = False
                                self.compare(
                                    parsers=parsers,
                                    want={"aces": each, "afi": want["afi"]},
                                    have={
                                        "aces": each_have,
                                        "afi": have["afi"],
                                    },
                                )
                        elif each.get("sequence") == each_have.get("sequence"):
                            if cmd_added:
                                self.addcmd(have, "acls_name", False)
                                cmd_added = False
                            self.compare(
                                parsers=parsers,
                                want={},
                                have={"aces": each_have, "afi": have["afi"]},
                            )
                            self.compare(
                                parsers=parsers,
                                want={"aces": each, "afi": want["afi"]},
                                have={},
                            )
                            set_want = False
                else:
                    if cmd_added:
                        self.addcmd(want, "acls_name", False)
                        cmd_added = False
                    self.compare(
                        parsers=parsers,
                        want={"aces": each, "afi": want["afi"]},
                        have=dict(),
                    )
                    set_want = False
                if set_want:
                    if cmd_added:
                        self.addcmd(want, "acls_name", False)
                        cmd_added = False
                    self.compare(
                        parsers=parsers,
                        want={"aces": each, "afi": want["afi"]},
                        have=dict(),
                    )
