# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The cisco.ios bgp_global fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from copy import deepcopy
import re
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.bgp_global import (
    Bgp_globalTemplate,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.bgp_global.bgp_global import (
    Bgp_globalArgs,
)
from ansible.module_utils.connection import ConnectionError


class Bgp_globalFacts(object):
    """ The cisco.ios bgp_global facts class
    """

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Bgp_globalArgs.argument_spec
        spec = deepcopy(self.argument_spec)
        if subspec:
            if options:
                facts_argument_spec = spec[subspec][options]
            else:
                facts_argument_spec = spec[subspec]
        else:
            facts_argument_spec = spec

        self.generated_spec = utils.generate_dict(facts_argument_spec)

    def get_bgp_global_data(self, connection):
        try:
            return connection.get("sh running-config | section ^router bgp")
        except:
            if "Invalid input detected at" in e.message:
                data = connection.get("sh running-config | begin ^router bgp")
                return "\n".join(re.findall(r'router bgp.+?(?<=\n\!)$', data,re.M|re.S))
            else:
                raise

    def populate_facts(self, connection, ansible_facts, data=None):
        """ Populate the facts for Bgp_global network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}

        if not data:
            data = self.get_bgp_global_data(connection)

        # parse native config using the Bgp_global template
        bgp_global_parser = Bgp_globalTemplate(
            lines=data.splitlines(), module=self._module
        )
        objs = bgp_global_parser.parse()

        objs = utils.remove_empties(objs)
        if "neighbor" in objs:
            temp_neighbor = []
            temp = {}
            temp["address"] = None
            for each in objs["neighbor"]:
                if temp["address"] != each["address"]:
                    if temp["address"]:
                        temp_neighbor.append(temp)
                        temp = {}
                    temp["address"] = each.pop("address")
                    if each:
                        temp.update(each)
                else:
                    each.pop("address")
                    temp.update(each)
            if temp:
                temp_neighbor.append(temp)
            objs["neighbor"] = temp_neighbor
        if objs:
            ansible_facts["ansible_network_resources"].pop("bgp_global", None)

            params = utils.remove_empties(
                bgp_global_parser.validate_config(
                    self.argument_spec, {"config": objs}, redact=True
                )
            )
            facts["bgp_global"] = params["config"]
            ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
