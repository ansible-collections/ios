#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for cisco.ios_prefix_lists
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
module: ios_prefix_lists
short_description: Prefix Lists resource module
description:
  - This module configures and manages the attributes of prefix list on Cisco IOS.
version_added: 2.2.0
author: Sumit Jaiswal (@justjais)
notes:
  - Tested against Cisco IOSv Version 15.2 on VIRL
  - This module works with connection C(network_cli).
    See L(IOS Platform Options,../network/user_guide/platform_ios.html)
options:
  config:
    description: A list of configurations for Prefix lists.
    type: list
    elements: dict
    suboptions:
      afi:
        description:
          - The Address Family Indicator (AFI) for the  prefix list.
        type: str
        choices:
          - ipv4
          - ipv6
      name:
        description: Name of a prefix-list
        type: str
      prefix_lists:
        description: List of Prefix-lists.
        type: list
        elements: dict
        suboptions:
          action:
            description: Specify packets to be rejected or forwarded
            type: str
            choices: ['deny', 'permit']
          sequence:
            description: sequence number of an entry
            type: int
          description:
            description:  Prefix-list specific description
            type: str
          address:
            description:
              - IP prefix <network>/<length>, e.g., A.B.C.D/nn
              - IPv6 prefix <network>/<length>, e.g., X:X:X:X::X/<0-128>
            type: str
          match:
            description: List of Prefix-lists.
            type: dict
            suboptions:
              ge:
                description: Minimum prefix length to be matched
                type: int
              le:
                description: Maximum prefix length to be matched
                type: int
  running_config:
    description:
    - This option is used only with state I(parsed).
    - The value of this option should be the output received from the IOS device by
      executing the command B(sh bgp).
    - The state I(parsed) reads the configuration from C(running_config) option and
      transforms it into Ansible structured data as per the resource module's argspec
      and the value is then returned in the I(parsed) key within the result.
    type: str
  state:
    description:
      - The state the configuration should be left in.
    type: str
    choices:
      - merged
      - replaced
      - overridden
      - deleted
      - gathered
      - parsed
      - rendered
    default: merged
required_if:
- ["state", "merged", ["config",]]
- ["state", "replaced", ["config",]]
- ["state", "overridden", ["config",]]
- ["state", "rendered", ["config",]]
- ["state", "parsed", ["running_config",]]
mutually_exclusive:
- ["config", "running_config"]
supports_check_mode: True
"""
EXAMPLES = """
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.prefix_lists.prefix_lists import (
    Prefix_listsArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.prefix_lists.prefix_lists import (
    Prefix_lists,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Prefix_listsArgs.argument_spec,
        mutually_exclusive=[["config", "running_config"]],
        required_if=[
            ["state", "merged", ["config"]],
            ["state", "replaced", ["config"]],
            ["state", "overridden", ["config"]],
            ["state", "rendered", ["config"]],
            ["state", "parsed", ["running_config"]],
        ],
        supports_check_mode=True,
    )

    result = Prefix_lists(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
