# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The Prefix_lists parser templates file. This contains 
a list of parser definitions and associated functions that 
facilitates both facts gathering and native command generation for 
the given network resource.
"""

import re
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network_template import (
    NetworkTemplate,
)

def _tmplt_set_prefix_lists(config_data):
    if 'prefix_list' in config_data:
        if config_data.get('afi') == 'ipv4':
            config_data['afi'] = 'ip'
        cmd = "{afi} prefix-list {name}".format(**config_data)
        if config_data['prefix_list'].get('description'):
            cmd += ' description {description}'.format(**config_data['prefix_list'])
        else:
            cmd += ' seq {sequence} {action} {prefix}'.format(**config_data['prefix_list'])
            if config_data['prefix_list'].get('ge'):
                cmd += ' ge {ge}'.format(**config_data['prefix_list'])
            if config_data['prefix_list'].get('le'):
                cmd += ' le {le}'.format(**config_data['prefix_list'])
        return cmd

class Prefix_listsTemplate(NetworkTemplate):
    def __init__(self, lines=None):
        super(Prefix_listsTemplate, self).__init__(lines=lines, tmplt=self)

    PARSERS = [
        {
            "name": "prefix_list",
            "getval": re.compile(
                r"""
                ^(?P<afi>ip|ipv6)*
                \s*prefix-list*
                \s*(?P<name>\S+)*
                \s*(?P<description>description\s\S.*)*                
                \s*(?P<sequence>seq\s\S+)*
                \s*(?P<action>deny|permit)*
                \s*(?P<address>(?:[0-9]{1,3}\.){3}[0-9]{1,3}/\d+|(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))/\d+)*
                \s*(?P<ge>ge\s\d+)*
                \s*(?P<le>le\s\d+)*
                $""", re.VERBOSE),
            "setval": _tmplt_set_prefix_lists,
            "result": {
                "{{ afi + '_' + name }}": {
                    "afi": "{{ 'ipv4' if afi is defined and afi=='ip' else 'ipv6' }}",
                    "prefix_lists": [
                        {
                            "name": "{{ name if name is defined }}",
                            "entries":
                                {
                                "description": "{{ description.split('description ')[1] if description is defined }}",
                                "sequence": "{{ sequence.split(' ')[1] if sequence is defined }}",
                                "action": "{{ action if action is defined }}",
                                "prefix": "{{ address if address is defined }}",
                                "ge": "{{ ge.split(' ')[1] if ge is defined }}",
                                "le": "{{ le.split(' ')[1] if le is defined }}",
                            }
                        },
                    ]
                }
            },
            "shared": True
        },
    ]
