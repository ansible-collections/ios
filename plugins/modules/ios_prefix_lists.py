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
        choices: ['ipv4', 'ipv6']
      prefix_lists:
        description: List of Prefix-lists.
        type: list
        elements: dict
        suboptions:
          name:
            description: Name of a prefix-list
            type: str
          entries:
            description: Prefix-lists supported entries.
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
              prefix:
                description:
                  - IPv4 prefix <network>/<length>, e.g., A.B.C.D/nn
                  - IPv6 prefix <network>/<length>, e.g., X:X:X:X::X/<0-128>
                type: str
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
      - The state the configuration should be left in
      - The states I(rendered), I(gathered) and I(parsed) does not perform any change
        on the device.
      - The state I(rendered) will transform the configuration in C(config) option to
        platform specific CLI commands which will be returned in the I(rendered) key
        within the result. For state I(rendered) active connection to remote host is
        not required.
      - The state I(gathered) will fetch the running configuration from device and transform
        it into structured data in the format as per the resource module argspec and
        the value is returned in the I(gathered) key within the result.
      - The state I(parsed) reads the configuration from C(running_config) option and
        transforms it into JSON format as per the resource module parameters and the
        value is returned in the I(parsed) key within the result. The value of C(running_config)
        option should be the same format as the output of command I(sh running-config
        | section ^ip prefix-list|^ipv6 prefix-list) executed on device. For state I(parsed) active
        connection to remote host is not required.
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
"""

EXAMPLES = """
# Using deleted by Name

# Before state:
# -------------
#
# router-ios#sh running-config | section ^ip prefix-list|^ipv6 prefix-list
# ip prefix-list 10 description this is test description
# ip prefix-list 10 seq 5 deny 1.0.0.0/8 le 15
# ip prefix-list 10 seq 10 deny 35.0.0.0/8 ge 10
# ip prefix-list 10 seq 15 deny 12.0.0.0/8 ge 15
# ip prefix-list 10 seq 20 deny 14.0.0.0/8 ge 20 le 21
# ip prefix-list test description this is test
# ip prefix-list test seq 50 deny 12.0.0.0/8 ge 15
# ip prefix-list test_prefix description this is for prefix-list
# ip prefix-list test_prefix seq 5 deny 35.0.0.0/8 ge 10 le 15
# ip prefix-list test_prefix seq 10 deny 35.0.0.0/8 ge 20
# ipv6 prefix-list test_ipv6 description this is ipv6 prefix-list
# ipv6 prefix-list test_ipv6 seq 10 deny 2001:DB8:0:4::/64 ge 80

- name: Delete provided Prefix lists config by Prefix name
  cisco.ios.ios_prefix_lists:
    config:
      - afi: ipv4
        prefix_lists:
          - name: 10
          - name: test_prefix
    state: deleted

#  Commands Fired:
#  ---------------
#
#  "commands": [
#         "no ip prefix-list 10",
#         "no ip prefix-list test_prefix"
#     ]

# After state:
# -------------
# router-ios#sh running-config | section ^ip prefix-list|^ipv6 prefix-list
# ip prefix-list test description this is test
# ip prefix-list test seq 50 deny 12.0.0.0/8 ge 15
# ipv6 prefix-list test_ipv6 description this is ipv6 prefix-list
# ipv6 prefix-list test_ipv6 seq 10 deny 2001:DB8:0:4::/64 ge 80

# Using deleted by AFI

# Before state:
# -------------
#
# router-ios#sh running-config | section ^ip prefix-list|^ipv6 prefix-list
# ip prefix-list 10 description this is test description
# ip prefix-list 10 seq 5 deny 1.0.0.0/8 le 15
# ip prefix-list 10 seq 10 deny 35.0.0.0/8 ge 10
# ip prefix-list 10 seq 15 deny 12.0.0.0/8 ge 15
# ip prefix-list 10 seq 20 deny 14.0.0.0/8 ge 20 le 21
# ip prefix-list test description this is test
# ip prefix-list test seq 50 deny 12.0.0.0/8 ge 15
# ip prefix-list test_prefix description this is for prefix-list
# ip prefix-list test_prefix seq 5 deny 35.0.0.0/8 ge 10 le 15
# ip prefix-list test_prefix seq 10 deny 35.0.0.0/8 ge 20
# ipv6 prefix-list test_ipv6 description this is ipv6 prefix-list
# ipv6 prefix-list test_ipv6 seq 10 deny 2001:DB8:0:4::/64 ge 80

- name: Delete provided Prefix lists config by AFI
  cisco.ios.ios_prefix_lists:
    config:
      - afi: ipv4
    state: deleted

#  Commands Fired:
#  ---------------
#
#  "commands": [
#         "no ip prefix-list test",
#         "no ip prefix-list 10",
#         "no ip prefix-list test_prefix"
#     ]

# After state:
# -------------
# router-ios#sh running-config | section ^ip prefix-list|^ipv6 prefix-list
# ipv6 prefix-list test_ipv6 description this is ipv6 prefix-list
# ipv6 prefix-list test_ipv6 seq 10 deny 2001:DB8:0:4::/64 ge 80

# Using deleted without any config passed (NOTE: This will delete all Prefix lists configuration from device)

# Before state:
# -------------
#
# router-ios#sh running-config | section ^ip prefix-list|^ipv6 prefix-list
# ip prefix-list 10 description this is test description
# ip prefix-list 10 seq 5 deny 1.0.0.0/8 le 15
# ip prefix-list 10 seq 10 deny 35.0.0.0/8 ge 10
# ip prefix-list 10 seq 15 deny 12.0.0.0/8 ge 15
# ip prefix-list 10 seq 20 deny 14.0.0.0/8 ge 20 le 21
# ip prefix-list test description this is test
# ip prefix-list test seq 50 deny 12.0.0.0/8 ge 15
# ip prefix-list test_prefix description this is for prefix-list
# ip prefix-list test_prefix seq 5 deny 35.0.0.0/8 ge 10 le 15
# ip prefix-list test_prefix seq 10 deny 35.0.0.0/8 ge 20
# ipv6 prefix-list test_ipv6 description this is ipv6 prefix-list
# ipv6 prefix-list test_ipv6 seq 10 deny 2001:DB8:0:4::/64 ge 80

- name: Delete all Prefix lists config
  cisco.ios.ios_prefix_lists:
    state: deleted

# Commands Fired:
# ---------------
#
#  "commands": [
#         "no ip prefix-list test",
#         "no ip prefix-list 10",
#         "no ip prefix-list test_prefix",
#         "no ipv6 prefix-list test_ipv6"
#     ]

# After state:
# -------------
# router-ios#sh running-config | section ^ip prefix-list|^ipv6 prefix-list
# router-ios#

# Using merged

# Before state:
# -------------
#
# router-ios#sh running-config | section ^ip prefix-list|^ipv6 prefix-list
# ipv6 prefix-list test_ipv6 description this is ipv6
# ipv6 prefix-list test_ipv6 seq 10 deny 2001:DB8:0:4::/64 ge 80

- name: Merge provided Prefix lists configuration
  cisco.ios.ios_prefix_lists:
    config:
      - afi: ipv4
        prefix_lists:
          - name: 10
            entries:
              - description: this is new merge test
              - action: deny
                prefix: 1.0.0.0/8
                le: 15
                sequence: 5
              - action: deny
                prefix: 35.0.0.0/8
                ge: 10
                sequence: 10
              - action: deny
                prefix: 12.0.0.0/8
                ge: 15
                sequence: 15
              - action: deny
                prefix: 14.0.0.0/8
                ge: 20
                le: 21
                sequence: 20
          - name: test
            entries:
              - description: this is merge test
              - action: deny
                prefix: 12.0.0.0/8
                ge: 15
                sequence: 50
          - name: test_prefix
            entries:
              - description: this is for prefix-list
              - action: deny
                prefix: 35.0.0.0/8
                ge: 10
                le: 15
                sequence: 5
              - action: deny
                prefix: 35.0.0.0/8
                ge: 20
                sequence: 10
      - afi: ipv6
        prefix_lists:
          - name: test_ipv6
            entries:
              - description: this is ipv6 merge test
              - action: deny
                prefix: 2001:DB8:0:4::/64
                ge: 80
                le: 100
                sequence: 10
    state: merged

#  Commands Fired:
#  ---------------
#
#   "commands": [
#         "ip prefix-list test description this is merge test",
#         "ip prefix-list test seq 50 deny 12.0.0.0/8 ge 15",
#         "ip prefix-list 10 seq 15 deny 12.0.0.0/8 ge 15",
#         "ip prefix-list 10 seq 10 deny 35.0.0.0/8 ge 10",
#         "ip prefix-list 10 seq 5 deny 1.0.0.0/8 le 15",
#         "ip prefix-list 10 description this is new merge test",
#         "ip prefix-list 10 seq 20 deny 14.0.0.0/8 ge 20 le 21",
#         "ip prefix-list test_prefix seq 10 deny 35.0.0.0/8 ge 20",
#         "ip prefix-list test_prefix seq 5 deny 35.0.0.0/8 ge 10 le 15",
#         "ip prefix-list test_prefix description this is for prefix-list",
#         "no ipv6 prefix-list test_ipv6 seq 10 deny 2001:DB8:0:4::/64 ge 80",
#         "ipv6 prefix-list test_ipv6 seq 10 deny 2001:DB8:0:4::/64 ge 80 le 100",
#         "ipv6 prefix-list test_ipv6 description this is ipv6 merge test"
#     ]

# After state:
# -------------
#
# router-ios#sh running-config | section ^ip prefix-list|^ipv6 prefix-list
# ip prefix-list 10 description this is new merge test
# ip prefix-list 10 seq 5 deny 1.0.0.0/8 le 15
# ip prefix-list 10 seq 10 deny 35.0.0.0/8 ge 10
# ip prefix-list 10 seq 15 deny 12.0.0.0/8 ge 15
# ip prefix-list 10 seq 20 deny 14.0.0.0/8 ge 20 le 21
# ip prefix-list test description this is merge test
# ip prefix-list test seq 50 deny 12.0.0.0/8 ge 15
# ip prefix-list test_prefix description this is for prefix-list
# ip prefix-list test_prefix seq 5 deny 35.0.0.0/8 ge 10 le 15
# ip prefix-list test_prefix seq 10 deny 35.0.0.0/8 ge 20
# ipv6 prefix-list test_ipv6 description this is ipv6 merge test
# ipv6 prefix-list test_ipv6 seq 10 deny 2001:DB8:0:4::/64 ge 80 le 100

# Using overridden

# Before state:
# -------------
#
# router-ios#sh running-config | section ^ip prefix-list|^ipv6 prefix-list
# ip prefix-list 10 description this is test description
# ip prefix-list 10 seq 5 deny 1.0.0.0/8 le 15
# ip prefix-list 10 seq 10 deny 35.0.0.0/8 ge 10
# ip prefix-list 10 seq 15 deny 12.0.0.0/8 ge 15
# ip prefix-list 10 seq 20 deny 14.0.0.0/8 ge 20 le 21
# ip prefix-list test description this is test
# ip prefix-list test seq 50 deny 12.0.0.0/8 ge 15
# ip prefix-list test_prefix description this is for prefix-list
# ip prefix-list test_prefix seq 5 deny 35.0.0.0/8 ge 10 le 15
# ip prefix-list test_prefix seq 10 deny 35.0.0.0/8 ge 20
# ipv6 prefix-list test_ipv6 description this is ipv6 prefix-list
# ipv6 prefix-list test_ipv6 seq 10 deny 2001:DB8:0:4::/64 ge 80

- name: Override provided Prefix lists configuration
  cisco.ios.ios_prefix_lists:
    config:
      - afi: ipv4
        prefix_lists:
          - name: 10
            entries:
              - description: this is override test
              - action: deny
                prefix: 12.0.0.0/8
                ge: 15
                sequence: 15
              - action: deny
                prefix: 14.0.0.0/8
                ge: 20
                le: 21
                sequence: 20
          - name: test_override
            entries:
              - description: this is override test
              - action: deny
                prefix: 35.0.0.0/8
                ge: 20
                sequence: 10
      - afi: ipv6
        prefix_lists:
          - name: test_ipv6
            entries:
              - description: this is ipv6 override test
              - action: deny
                prefix: 2001:DB8:0:4::/64
                ge: 80
                le: 100
                sequence: 10
    state: overridden

# Commands Fired:
# ---------------
#
#  "commands": [
#         "no ip prefix-list test",
#         "no ip prefix-list test_prefix",
#         "ip prefix-list 10 description this is override test",
#         "no ip prefix-list 10 seq 10 deny 35.0.0.0/8 ge 10",
#         "no ip prefix-list 10 seq 5 deny 1.0.0.0/8 le 15",
#         "ip prefix-list test_override seq 10 deny 35.0.0.0/8 ge 20",
#         "ip prefix-list test_override description this is override test",
#         "no ipv6 prefix-list test_ipv6 seq 10 deny 2001:DB8:0:4::/64 ge 80",
#         "ipv6 prefix-list test_ipv6 seq 10 deny 2001:DB8:0:4::/64 ge 80 le 100",
#         "ipv6 prefix-list test_ipv6 description this is ipv6 override test"
#     ]

# After state:
# -------------
#
# router-ios#sh running-config | section ^ip prefix-list|^ipv6 prefix-list
# ip prefix-list 10 description this is override test
# ip prefix-list 10 seq 15 deny 12.0.0.0/8 ge 15
# ip prefix-list 10 seq 20 deny 14.0.0.0/8 ge 20 le 21
# ip prefix-list test_override description this is override test
# ip prefix-list test_override seq 10 deny 35.0.0.0/8 ge 20
# ipv6 prefix-list test_ipv6 description this is ipv6 override test
# ipv6 prefix-list test_ipv6 seq 10 deny 2001:DB8:0:4::/64 ge 80 le 100

# Using replaced

# Before state:
# -------------
#
# router-ios#sh running-config | section ^ip prefix-list|^ipv6 prefix-list
# ip prefix-list 10 description this is test description
# ip prefix-list 10 seq 5 deny 1.0.0.0/8 le 15
# ip prefix-list 10 seq 10 deny 35.0.0.0/8 ge 10
# ip prefix-list 10 seq 15 deny 12.0.0.0/8 ge 15
# ip prefix-list 10 seq 20 deny 14.0.0.0/8 ge 20 le 21
# ip prefix-list test description this is test
# ip prefix-list test seq 50 deny 12.0.0.0/8 ge 15
# ip prefix-list test_prefix description this is for prefix-list
# ip prefix-list test_prefix seq 5 deny 35.0.0.0/8 ge 10 le 15
# ip prefix-list test_prefix seq 10 deny 35.0.0.0/8 ge 20
# ipv6 prefix-list test_ipv6 description this is ipv6 prefix-list
# ipv6 prefix-list test_ipv6 seq 10 deny 2001:DB8:0:4::/64 ge 80

- name: Replaced provided Prefix lists configuration
  cisco.ios.ios_prefix_lists:
    config:
      - afi: ipv4
        prefix_lists:
          - name: 10
            entries:
              - description: this is replace test
              - action: deny
                prefix: 12.0.0.0/8
                ge: 15
                sequence: 15
              - action: deny
                prefix: 14.0.0.0/8
                ge: 20
                le: 21
                sequence: 20
          - name: test_replace
            entries:
              - description: this is replace test
              - action: deny
                prefix: 35.0.0.0/8
                ge: 20
                sequence: 10
      - afi: ipv6
        prefix_lists:
          - name: test_ipv6
            entries:
              - description: this is ipv6 replace test
              - action: deny
                prefix: 2001:DB8:0:4::/64
                ge: 80
                le: 100
                sequence: 10
    state: replaced

# Commands Fired:
# ---------------
#  "commands": [
#         "ip prefix-list 10 description this is replace test",
#         "no ip prefix-list 10 seq 10 deny 35.0.0.0/8 ge 10",
#         "no ip prefix-list 10 seq 5 deny 1.0.0.0/8 le 15",
#         "ip prefix-list test_replace seq 10 deny 35.0.0.0/8 ge 20",
#         "ip prefix-list test_replace description this is replace test",
#         "no ipv6 prefix-list test_ipv6 seq 10 deny 2001:DB8:0:4::/64 ge 80",
#         "ipv6 prefix-list test_ipv6 seq 10 deny 2001:DB8:0:4::/64 ge 80 le 100",
#         "ipv6 prefix-list test_ipv6 description this is ipv6 replace test"
#     ]

# After state:
# -------------
#
# router-ios#sh running-config | section ^ip prefix-list|^ipv6 prefix-list
# ip prefix-list 10 description this is replace test
# ip prefix-list 10 seq 15 deny 12.0.0.0/8 ge 15
# ip prefix-list 10 seq 20 deny 14.0.0.0/8 ge 20 le 21
# ip prefix-list test description this is test
# ip prefix-list test seq 50 deny 12.0.0.0/8 ge 15
# ip prefix-list test_prefix description this is for prefix-list
# ip prefix-list test_prefix seq 5 deny 35.0.0.0/8 ge 10 le 15
# ip prefix-list test_prefix seq 10 deny 35.0.0.0/8 ge 20
# ip prefix-list test_replace description this is replace test
# ip prefix-list test_replace seq 10 deny 35.0.0.0/8 ge 20
# ipv6 prefix-list test_ipv6 description this is ipv6 replace test
# ipv6 prefix-list test_ipv6 seq 10 deny 2001:DB8:0:4::/64 ge 80 le 100

# Using Gathered

# Before state:
# -------------
#
# router-ios#sh running-config | section ^ip prefix-list|^ipv6 prefix-list
# ip prefix-list 10 description this is test description
# ip prefix-list 10 seq 5 deny 1.0.0.0/8 le 15
# ip prefix-list 10 seq 10 deny 35.0.0.0/8 ge 10
# ip prefix-list 10 seq 15 deny 12.0.0.0/8 ge 15
# ip prefix-list 10 seq 20 deny 14.0.0.0/8 ge 20 le 21
# ip prefix-list test description this is test
# ip prefix-list test seq 50 deny 12.0.0.0/8 ge 15
# ip prefix-list test_prefix description this is for prefix-list
# ip prefix-list test_prefix seq 5 deny 35.0.0.0/8 ge 10 le 15
# ip prefix-list test_prefix seq 10 deny 35.0.0.0/8 ge 20
# ipv6 prefix-list test_ipv6 description this is ipv6 prefix-list
# ipv6 prefix-list test_ipv6 seq 10 deny 2001:DB8:0:4::/64 ge 80

- name: Gather Prefix lists provided configurations
  cisco.ios.ios_prefix_lists:
    config:
    state: gathered

# Module Execution Result:
# ------------------------
#
# "gathered": [
#         {
#             "afi": "ipv4",
#             "prefix_lists": [
#                 {
#                     "entries": [
#                         {
#                             "description": "this is test description"
#                         },
#                         {
#                             "action": "deny",
#                             "le": 15,
#                             "prefix": "1.0.0.0/8",
#                             "sequence": 5
#                         },
#                         {
#                             "action": "deny",
#                             "ge": 10,
#                             "prefix": "35.0.0.0/8",
#                             "sequence": 10
#                         },
#                         {
#                             "action": "deny",
#                             "ge": 15,
#                             "prefix": "12.0.0.0/8",
#                             "sequence": 15
#                         },
#                         {
#                             "action": "deny",
#                             "ge": 20,
#                             "le": 21,
#                             "prefix": "14.0.0.0/8",
#                             "sequence": 20
#                         }
#                     ],
#                     "name": "10"
#                 },
#                 {
#                     "entries": [
#                         {
#                             "description": "this is test"
#                         },
#                         {
#                             "action": "deny",
#                             "ge": 15,
#                             "prefix": "12.0.0.0/8",
#                             "sequence": 50
#                         }
#                     ],
#                     "name": "test"
#                 },
#                 {
#                     "entries": [
#                         {
#                             "description": "this is for prefix-list"
#                         },
#                         {
#                             "action": "deny",
#                             "ge": 10,
#                             "le": 15,
#                             "prefix": "35.0.0.0/8",
#                             "sequence": 5
#                         },
#                         {
#                             "action": "deny",
#                             "ge": 20,
#                             "prefix": "35.0.0.0/8",
#                             "sequence": 10
#                         }
#                     ],
#                     "name": "test_prefix"
#                 }
#             ]
#         },
#         {
#             "afi": "ipv6",
#             "prefix_lists": [
#                 {
#                     "entries": [
#                         {
#                             "description": "this is ipv6 prefix-list"
#                         },
#                         {
#                             "action": "deny",
#                             "ge": 80,
#                             "prefix": "2001:DB8:0:4::/64",
#                             "sequence": 10
#                         }
#                     ],
#                     "name": "test_ipv6"
#                 }
#             ]
#         }
#     ]

# After state:
# ------------
#
# router-ios#sh running-config | section ^ip prefix-list|^ipv6 prefix-list
# ip prefix-list 10 description this is test description
# ip prefix-list 10 seq 5 deny 1.0.0.0/8 le 15
# ip prefix-list 10 seq 10 deny 35.0.0.0/8 ge 10
# ip prefix-list 10 seq 15 deny 12.0.0.0/8 ge 15
# ip prefix-list 10 seq 20 deny 14.0.0.0/8 ge 20 le 21
# ip prefix-list test description this is test
# ip prefix-list test seq 50 deny 12.0.0.0/8 ge 15
# ip prefix-list test_prefix description this is for prefix-list
# ip prefix-list test_prefix seq 5 deny 35.0.0.0/8 ge 10 le 15
# ip prefix-list test_prefix seq 10 deny 35.0.0.0/8 ge 20
# ipv6 prefix-list test_ipv6 description this is ipv6 prefix-list
# ipv6 prefix-list test_ipv6 seq 10 deny 2001:DB8:0:4::/64 ge 80

# Using Rendered

- name: Render the commands for provided  configuration
  cisco.ios.ios_prefix_lists:
    config:
      - afi: ipv4
        prefix_lists:
          - name: 10
            entries:
              - description: this is new merge test
              - action: deny
                prefix: 1.0.0.0/8
                le: 15
                sequence: 5
              - action: deny
                prefix: 35.0.0.0/8
                ge: 10
                sequence: 10
              - action: deny
                prefix: 12.0.0.0/8
                ge: 15
                sequence: 15
              - action: deny
                prefix: 14.0.0.0/8
                ge: 20
                le: 21
                sequence: 20
          - name: test
            entries:
              - description: this is merge test
              - action: deny
                prefix: 12.0.0.0/8
                ge: 15
                sequence: 50
          - name: test_prefix
            entries:
              - description: this is for prefix-list
              - action: deny
                prefix: 35.0.0.0/8
                ge: 10
                le: 15
                sequence: 5
              - action: deny
                prefix: 35.0.0.0/8
                ge: 20
                sequence: 10
      - afi: ipv6
        prefix_lists:
          - name: test_ipv6
            entries:
              - description: this is ipv6 merge test
              - action: deny
                prefix: 2001:DB8:0:4::/64
                ge: 80
                le: 100
                sequence: 10
    state: rendered

# Module Execution Result:
# ------------------------
#
#  "rendered": [
#         "ip prefix-list test description this is test",
#         "ip prefix-list test seq 50 deny 12.0.0.0/8 ge 15",
#         "ip prefix-list 10 seq 15 deny 12.0.0.0/8 ge 15",
#         "ip prefix-list 10 seq 10 deny 35.0.0.0/8 ge 10",
#         "ip prefix-list 10 seq 5 deny 1.0.0.0/8 le 15",
#         "ip prefix-list 10 description this is test description",
#         "ip prefix-list 10 seq 20 deny 14.0.0.0/8 ge 20 le 21",
#         "ip prefix-list test_prefix seq 10 deny 35.0.0.0/8 ge 20",
#         "ip prefix-list test_prefix seq 5 deny 35.0.0.0/8 ge 10 le 15",
#         "ip prefix-list test_prefix description this is for prefix-list",
#         "ipv6 prefix-list test_ipv6 seq 10 deny 2001:DB8:0:4::/64 ge 80 l2 100",
#         "ipv6 prefix-list test_ipv6 description this is ipv6 prefix-list"
#     ]

# Using Parsed

# File: parsed.cfg
# ----------------
#
# ip prefix-list 10 description this is test description
# ip prefix-list 10 seq 5 deny 1.0.0.0/8 le 15
# ip prefix-list 10 seq 10 deny 35.0.0.0/8 ge 10
# ip prefix-list 10 seq 15 deny 12.0.0.0/8 ge 15
# ip prefix-list 10 seq 20 deny 14.0.0.0/8 ge 20 le 21
# ip prefix-list test description this is test
# ip prefix-list test seq 50 deny 12.0.0.0/8 ge 15
# ip prefix-list test_prefix description this is for prefix-list
# ip prefix-list test_prefix seq 5 deny 35.0.0.0/8 ge 10 le 15
# ip prefix-list test_prefix seq 10 deny 35.0.0.0/8 ge 20
# ipv6 prefix-list test_ipv6 description this is ipv6 prefix-list
# ipv6 prefix-list test_ipv6 seq 10 deny 2001:DB8:0:4::/64 ge 80

- name: Parse the provided configuration with the existing running configuration
  cisco.ios.ios_prefix_lists:
    running_config: "{{ lookup('file', 'parsed.cfg') }}"
    state: parsed

# Module Execution Result:
# ------------------------
#
# "parsed": [
#         {
#             "afi": "ipv4",
#             "prefix_lists": [
#                 {
#                     "entries": [
#                         {
#                             "description": "this is test description"
#                         },
#                         {
#                             "action": "deny",
#                             "le": 15,
#                             "prefix": "1.0.0.0/8",
#                             "sequence": 5
#                         },
#                         {
#                             "action": "deny",
#                             "ge": 10,
#                             "prefix": "35.0.0.0/8",
#                             "sequence": 10
#                         },
#                         {
#                             "action": "deny",
#                             "ge": 15,
#                             "prefix": "12.0.0.0/8",
#                             "sequence": 15
#                         },
#                         {
#                             "action": "deny",
#                             "ge": 20,
#                             "le": 21,
#                             "prefix": "14.0.0.0/8",
#                             "sequence": 20
#                         }
#                     ],
#                     "name": "10"
#                 },
#                 {
#                     "entries": [
#                         {
#                             "description": "this is test"
#                         },
#                         {
#                             "action": "deny",
#                             "ge": 15,
#                             "prefix": "12.0.0.0/8",
#                             "sequence": 50
#                         }
#                     ],
#                     "name": "test"
#                 },
#                 {
#                     "entries": [
#                         {
#                             "description": "this is for prefix-list"
#                         },
#                         {
#                             "action": "deny",
#                             "ge": 10,
#                             "le": 15,
#                             "prefix": "35.0.0.0/8",
#                             "sequence": 5
#                         },
#                         {
#                             "action": "deny",
#                             "ge": 20,
#                             "prefix": "35.0.0.0/8",
#                             "sequence": 10
#                         }
#                     ],
#                     "name": "test_prefix"
#                 }
#             ]
#         },
#         {
#             "afi": "ipv6",
#             "prefix_lists": [
#                 {
#                     "entries": [
#                         {
#                             "description": "this is ipv6 prefix-list"
#                         },
#                         {
#                             "action": "deny",
#                             "ge": 80,
#                             "prefix": "2001:DB8:0:4::/64",
#                             "sequence": 10
#                         }
#                     ],
#                     "name": "test_ipv6"
#                 }
#             ]
#         }
#     ]
"""

RETURN = """
before:
  description: The configuration prior to the model invocation.
  returned: always
  sample: >
    The configuration returned will always be in the same format
     of the parameters above.
  type: list
after:
  description: The resulting configuration model invocation.
  returned: when changed
  sample: >
    The configuration returned will always be in the same format
     of the parameters above.
  type: list
commands:
  description: The set of commands pushed to the remote device.
  returned: always
  type: list
  sample: ['ip prefix-list 10 description this is test description', 'ip prefix-list 10 seq 5 deny 1.0.0.0/8 le 15']
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
