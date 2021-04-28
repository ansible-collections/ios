#
# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The cisco.ios_prefix_lists config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""

from copy import deepcopy

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
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.prefix_lists import (
    Prefix_listsTemplate,
)
import q


class Prefix_lists(ResourceModule):
    """
    The cisco.ios_prefix_lists config class
    """

    def __init__(self, module):
        super(Prefix_lists, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="prefix_lists",
            tmplt=Prefix_listsTemplate(),
        )
        self.parsers = [
        ]

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
        q(self.want, self.have)
        wantd = {entry['afi']: entry for entry in self.want}
        haved = {entry['afi']: entry for entry in self.have}

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
                    self._compare(want={}, have=have)

        for k, want in iteritems(wantd):
            self._compare(want=want, have=haved.pop(k, {}))

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
           populates the list of commands to be run by comparing
           the `want` and `have` data with the `parsers` defined
           for the Prefix_lists network resource.
        """
        if want != have and self.state != "deleted":
            for k, v in iteritems(want['prefix_lists']):
                if have.get("prefix_lists"):
                    have_prefix = have["prefix_lists"].pop(k, {})
                    for key, val in iteritems(v):
                        have_prefix_param = have_prefix.pop(key, {})
                        if have_prefix_param and val != have_prefix_param:
                            if key == 'description':
                                self.compare(
                                    parsers=self.parsers,
                                    want={'afi': want['afi'], 'name': k, 'prefix_list': {key: val}},
                                    have={'afi': have['afi'], 'name': k, 'prefix_list': {key: have_prefix_param}},
                                )
                            else:
                                self.compare(
                                    parsers=self.parsers,
                                    want=dict(),
                                    have={'afi': have['afi'], 'name': k, 'prefix_list': have_prefix_param},
                                )
                                self.compare(
                                    parsers=self.parsers,
                                    want={'afi': want['afi'], 'name': k, 'prefix_list': val},
                                    have={'afi': have['afi'], 'name': k, 'prefix_list': have_prefix_param},
                                )
                        elif val and val != have_prefix_param:
                            if key == 'description':
                                self.compare(
                                    parsers=self.parsers,
                                    want={'afi': want['afi'], 'name': k, 'prefix_list': {key: val}},
                                    have=dict(),
                                )
                            else:
                                self.compare(
                                    parsers=self.parsers,
                                    want={'afi': want['afi'], 'name': k, 'prefix_list': val},
                                    have=dict(),
                                )

    def list_to_dict(self, param):
        if param:
            for key, val in iteritems(param):
                if val.get("prefix_lists"):
                    temp_prefix_list = {}
                    for each in val["prefix_lists"]:
                        temp_entries = dict()
                        for every in each['params']:
                            if every.get('description'):
                                temp_entries.update(every)
                            else:
                                temp_entries.update({str(every['sequence']): every})
                        temp_prefix_list.update({each['name']: temp_entries})
                    val['prefix_lists'] = temp_prefix_list
