#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_logging_global
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
module: ios_logging_global
version_added: 2.1.0
short_description: Manages logging attributes of Cisco IOS network devices
description: This module manages the logging attributes of Cisco IOS network devices
author: Sagar Paul (@KB-perByte)
notes:
  - Tested against Cisco IOSv Version 15.2 on VIRL
  - This module works with connection C(network_cli).
    See L(IOS Platform Options,../network/user_guide/platform_ios.html)
  - The Configuration defaults of the Cisco IOS network devices
    are not subjected to idempotency causes
options:
  config:
    description: A list containing dictionary of logging options
    type: list
    elements: dict
    suboptions:
      buffered:
        description: Set buffered logging parameters
        type: dict
        suboptions:
          size: &size
            description: Logging buffer size
            type: int
          severity: &severity
            description: Logging severity level
            type: str
            choices: &severity_subgroup
              - alerts
              - critical
              - debugging
              - emergencies
              - errors
              - informational
              - notifications
              - warnings
          discriminator: &discriminator
            description: Establish MD-Buffer association
            type: str
          filtered: &filtered
            description: Enable filtered logging
            type: bool
          xml: &xml
            description: Enable logging in XML to XML logging buffer
            type: bool
      buginf:
        description: Enable buginf logging for debugging
        type: bool
      cns_events:
        description: Set CNS Event logging level
        type: str
        choices: *severity_subgroup
      console:
        description: Set console logging parameters
        type: dict
        suboptions:
          severity:
            description: Logging severity level
            type: str
            choices: ["alerts","critical","debugging","emergencies","errors","informational","notifications","warnings","guaranteed"]
          discriminator: *discriminator
          filtered: *filtered
          xml: *xml
      count:
        description: Count every log message and timestamp last occurance
        type: bool
      delimiter:
        description: Append delimiter to syslog messages
        type: dict
        suboptions:
          tcp:
            description: Append delimiter to syslog messages over TCP
            type: bool
      discriminator:
        description: Create or modify a message discriminator
        type: list
        elements: str
      dmvpn:
        description: DMVPN Configuration
        type: dict
        suboptions:
          rate_limit: &rate_limit
            description: rate in messages/minute, default is 600 messages/minute (1-10000)
            type: int
      esm:
        description: Set ESM filter restrictions
        type: dict
        suboptions:
          config:
            description: Permit/Deny configuration changes from ESM filters
            type: bool
      exception:
        description: Limit size of exception flush output (4096-2147483647)
        type: int
      facility:
        description: Facility parameter for syslog messages
        type: str
        choices:
          - auth
          - cron
          - daemon
          - kern
          - local0
          - local1
          - local2
          - local3
          - local4
          - local5
          - local6
          - local7
          - lpr
          - mail
          - news
          - sys10
          - sys11
          - sys12
          - sys13
          - sys14
          - sys9
          - syslog
          - user
          - uucp
      filter:
        description: Specify logging filter
        type: list
        elements: dict
        suboptions:
          url:
            description: Filter Uniform Resource Locator
            type: str
          order:
            description: Order of filter execution
            type: int
          args:
            description: Arguments passed to filter module.
            type: str
      history:
        description: Configure syslog history table
        type: dict
        suboptions:
          size: *size
          severity: *severity
      hosts:
        description: Set syslog server IP address and parameters
        type: list
        elements: dict
        suboptions:
          discriminator: *discriminator
          filtered: *filtered
          sequence_num_session: &sequence_num_session
            description: Include session sequence number tag in syslog message
            type: bool
          session_id: &session_id
            description: Specify syslog message session ID tagging
            type: dict
            suboptions: &session_id_suboptions
              tag:
                description: Include hostname in session ID tag
                type: str
                choices: ["hostname","ipv4","ipv6"]
              text:
                description: Include custom string in session ID tag
                type: str
          stream: &stream
            description: This server should only receive messages from a numbered stream
            type: int
          transport: &transport
            description: Specify the transport protocol (default=UDP)
            type: dict
            suboptions:
              tcp:
                description: Transport Control Protocol
                type: dict
                suboptions:
                  audit:
                    description: Set this host for IOS firewall audit logging
                    type: bool
                  discriminator: *discriminator
                  stream: *stream
                  filtered: *filtered
                  port:
                    description: Specify the TCP port number (default=601) (1 - 65535)
                    type: int
                  sequence_num_session: *sequence_num_session
                  session_id: *session_id
                  xml: *xml
              udp:
                description: User Datagram Protocol
                type: dict
                suboptions:
                  discriminator: *discriminator
                  stream: *stream
                  filtered: *filtered
                  port:
                    description: Specify the TCP port number (default=601) (1 - 65535)
                    type: int
                  sequence_num_session: *sequence_num_session
                  session_id: *session_id
                  xml: *xml
          vrf:
            description: Set VRF option
            type: str
          xml: *xml
          ipv6:
            description: Configure IPv6 syslog server
            type: str
          hostname:
            description: IP address of the syslog server
            type: str
      message_counter:
        description: Configure log message to include certain counter value
        type: list
        elements: str
        choices: ["log", "debug", "syslog"]
      monitor:
        description: Set terminal line (monitor) logging parameters
        type: dict
        suboptions:
          severity: *severity
          discriminator: *discriminator
          filtered: *filtered
          xml: *xml
      logging_on:
        description: Enable logging to all enabled destinations
        type: str
        choices: ["enable", "disable"]
      origin_id:
        description: Add origin ID to syslog messages
        type: dict
        suboptions:
          tag:
            description: Include hostname in session ID tag
            type: str
            choices: ["hostname","ip","ipv6"]
          text:
            description: Include custom string in session ID tag
            type: str
      persistent:
        description: Set persistent logging parameters
        type: dict
        suboptions:
          batch:
            description: Set batch size for writing to persistent storage (4096-2142715904)
            type: int
          filesize:
            description: Set size of individual log files (4096-2142715904)
            type: int
          immediate:
            description: Write log entry to storage immediately (no buffering).
            type: bool
          notify:
            description: Notify when show logging [persistent] is activated.
            type: bool
          protected:
            description: Eliminates manipulation on logging-persistent files.
            type: bool
          size:
            description: Set disk space for writing log messages (4096-2142715904)
            type: int
          threshold:
            description: Set threshold for logging persistent
            type: int
          url:
            description: URL to store logging messages
            type: str
      policy_firewall:
        description: Firewall configuration
        type: dict
        suboptions:
          rate_limit:
            description: (0-3600) value in seconds, default is 30 Sec.
            type: int
      queue_limit:
        description: Set logger message queue size
        type: dict
        suboptions:
          size:
            description: (100-2147483647) set new queue size
            type: int
          esm:
            description: (100-2147483647) set new queue size
            type: int
          trap:
            description: (100-2147483647) set new queue size
            type: int
      rate_limit:
        description: Set messages per second limit
        type: dict
        suboptions:
          size: &rate_limit_size
            description: (1-10000) message per second
            type: int
            required: True
          all:
            description: (1-10000) message per second
            type: bool
          console:
            description: (1-10000) message per second
            type: bool
          except_severity:
            description: Messages of this severity or higher
            type: str
            choices: *severity_subgroup
      reload:
        description: Set reload logging level
        type: dict
        suboptions:
          severity: *severity
          message_limit:
            description: Number of messages (1-4294967295>)
            type: int
      server_arp:
        description: Enable sending ARP requests for syslog servers when first configured
        type: bool
      snmp_trap:
        description: Set syslog level for sending snmp trap
        type: list
        elements: str
        choices: *severity_subgroup
      source_interface:
        description: Specify interface for source address in logging transactions
        type: list
        elements: dict
        suboptions:
          interface:
            description: Interface name with number
            type: str
          vrf:
            description: VPN Routing/Forwarding intstance name
            type: str
      trap:
        description: Set syslog server logging level
        type: str
        choices: *severity_subgroup
      userinfo:
        description: Enable logging of user info on privileged mode enabling
        type: bool
  running_config:
      description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the IOS device by
        executing the command B(show running-config | include logging).
      - The state I(parsed) reads the configuration from C(running_config) option and
        transforms it into Ansible structured data as per the resource module's argspec
        and the value is then returned in the I(parsed) key within the result.
      type: str
  state:
    choices:
    - merged
    - replaced
    - overridden
    - deleted
    - gathered
    - parsed
    - rendered
    default: merged
    description:
    - The state the configuration should be left in
    type: str
"""
EXAMPLES = """
# Using state: merged

# Before state:
# -------------

# router-ios#show running-config | section logging
# no logging exception
# no logging buffered
# no logging reload
# no logging rate-limit
# no logging console
# no logging monitor
# no logging cns-events
# no logging trap

- name: Apply the provided configuration
  cisco.ios.ios_logging_global:
    config:
      - buffered:
          severity: notifications
          size: 5099
          xml: True
      - console:
          severity: critical
          xml: True
      - facility: local5
      - hosts:
        - hostname: 10.0.1.12
        - hostname: 10.0.1.11
          xml: True
        - hostname: 10.0.1.10
          filtered: True
          stream: 10
        - hostname: 10.0.1.13
          transport:
            tcp:
              port: 514
      - monitor:
          severity: warnings
      - message_counter: log
      - snmp_trap:
        - errors
      - trap: errors
      - userinfo: True
      - policy_firewall:
          rate_limit: 10
      - logging_on: True
      - exception: 4099
      - dmvpn:
          rate_limit: 10
      - cns_events: warnings
    state: merged

# Commands Fired:
# ---------------

# "commands": [
#       "logging buffered xml 5099 notifications",
#       "logging cns-events warnings",
#       "logging console xml critical",
#       "logging dmvpn rate-limit 10",
#       "logging exception 4099",
#       "logging facility local5",
#       "logging monitor warnings",
#       "logging on",
#       "logging policy-firewall rate-limit 10",
#       "logging trap errors",
#       "logging userinfo",
#       "logging host 10.0.1.12",
#       "logging host 10.0.1.10 filtered stream 10",
#       "logging host 10.0.1.13 transport tcp port 514",
#       "logging message-counter log",
#       "logging snmp-trap errors",
#       "logging host 10.0.1.11 xml"
#     ],


# After state:
# ------------

# router-ios#show running-config | section logging
# logging exception 4099
# logging message-counter log
# logging userinfo
# logging buffered xml 5099 notifications
# no logging reload
# no logging rate-limit
# logging console xml critical
# logging monitor warnings
# logging cns-events warnings
# logging policy-firewall rate-limit 10
# logging dmvpn rate-limit 10
# logging trap errors
# logging facility local5
# logging snmp-trap errors
# logging snmp-trap warnings
# logging host 10.0.1.13 transport tcp port 514
# logging host 10.0.1.11 xml
# logging host 10.0.1.12
# logging host 10.0.1.10 filtered stream 10

# Using state: deleted

# Before state:
# -------------

# router-ios#show running-config | section logging
# logging exception 4099
# logging message-counter log
# logging userinfo
# logging buffered xml 5099 notifications
# no logging reload
# no logging rate-limit
# logging console xml critical
# logging monitor warnings
# logging cns-events warnings
# logging policy-firewall rate-limit 10
# logging dmvpn rate-limit 10
# logging trap errors
# logging facility local5
# logging snmp-trap errors
# logging snmp-trap warnings
# logging host 10.0.1.13 transport tcp port 514
# logging host 10.0.1.11 xml
# logging host 10.0.1.12
# logging host 10.0.1.10 filtered stream 10

- name: Remove as per the provided configuration
  cisco.ios.ios_logging_global:
    config:
      - snmp_trap:
          - errors
          - warnings
      - hosts:
          - hostname: 10.0.1.11
    state: deleted

# Commands Fired:
# ---------------

# "commands": [
#         "no logging snmp-trap errors",
#         "no logging snmp-trap warnings",
#         "no logging host 10.0.1.11"
#     ],

# After state:
# ------------

# router-ios#show running-config | section logging
# logging exception 4099
# logging message-counter log
# logging userinfo
# logging buffered xml 5099 notifications
# no logging reload
# no logging rate-limit
# logging console xml critical
# logging monitor warnings
# logging cns-events warnings
# logging policy-firewall rate-limit 10
# logging dmvpn rate-limit 10
# logging trap errors
# logging facility local5
# logging host 10.0.1.13 transport tcp port 514
# logging host 10.0.1.12
# logging host 10.0.1.10 filtered stream 10

# Using state: overridden

# Before state:
# -------------

# router-ios#show running-config | section logging
# logging exception 4099
# logging message-counter log
# logging userinfo
# logging buffered 6000 critical
# no logging reload
# no logging rate-limit
# logging console xml critical
# logging monitor warnings
# logging cns-events warnings
# logging policy-firewall rate-limit 10
# logging dmvpn rate-limit 10
# logging trap errors
# logging facility local6
# logging host 10.0.1.13 transport tcp port 514
# logging host 10.0.1.12
# logging host 10.0.1.10 filtered stream 10
# logging host 10.0.1.25 filtered

- name: Override commands with provided configuration
  cisco.ios.ios_logging_global:
    config:
      - buffered:
          severity: critical
          size: 6000
      - facility: local6
      - hosts:
          - hostname: 10.0.1.25
            filtered: True
    state: overridden

# Commands Fired:
# ---------------
# "commands": [
#         "no logging message-counter log",
#         "no logging host 10.0.1.12",
#         "no logging host 10.0.1.10",
#         "no logging host 10.0.1.13",
#         "no logging exception 4099",
#         "no logging userinfo",
#         "no logging console xml critical",
#         "no logging monitor warnings",
#         "no logging cns-events warnings",
#         "no logging policy-firewall rate-limit 10",
#         "no logging dmvpn rate-limit 10",
#         "no logging trap errors"
#     ],

# After state:
# ------------

# router-ios#show running-config | section logging
# no logging exception
# logging buffered 6000 critical
# no logging reload
# no logging rate-limit
# no logging console
# no logging monitor
# no logging cns-events
# no logging trap
# logging facility local6
# logging host 10.0.1.25 filtered

# Using state: gathered

# Before state:
# -------------

# router-ios#show running-config | section logging
# logging exception 4099
# logging message-counter log
# logging userinfo
# logging buffered xml 5099 notifications
# no logging reload
# no logging rate-limit
# logging console xml critical
# logging monitor warnings
# logging cns-events warnings
# logging policy-firewall rate-limit 10
# logging dmvpn rate-limit 10
# logging trap errors
# logging facility local5
# logging snmp-trap errors
# logging host 10.0.1.13 transport tcp port 514
# logging host 10.0.1.11 xml
# logging host 10.0.1.12
# logging host 10.0.1.10 filtered stream 10
# logging host 10.0.1.25 filtered

- name: Gather listed logging config
  cisco.ios.ios_logging_global:
    config:
    state: gathered

# Module Execution Result:
# ------------------------

# "gathered": [
#     {
#         "buffered": {
#             "severity": "notifications",
#             "size": 5099,
#             "xml": true
#         },
#         "cns_events": "warnings",
#         "console": {
#             "severity": "critical",
#             "xml": true
#         },
#         "dmvpn": {
#             "rate_limit": 10
#         },
#         "exception": 4099,
#         "facility": "local5",
#         "message_counter": [
#             "log"
#         ],
#         "monitor": {
#             "severity": "warnings"
#         },
#         "policy_firewall": {
#             "rate_limit": 10
#         },
#         "snmp_trap": [
#             "errors"
#         ],
#         "trap": "errors",
#         "userinfo": true
#     },
#     {
#         "host": [
#             {
#                 "hostname": "10.0.1.11",
#                 "xml": true
#             },
#             {
#                 "hostname": "10.0.1.12"
#             },
#             {
#                 "filtered": true,
#                 "hostname": "10.0.1.10",
#                 "stream": 10
#             },
#             {
#                 "filtered": true,
#                 "hostname": "10.0.1.25"
#             }
#         ]
#     }
# ],

# After state:
# -------------

# router-ios#show running-config | section logging
# logging exception 4099
# logging message-counter log
# logging userinfo
# logging buffered xml 5099 notifications
# no logging reload
# no logging rate-limit
# logging console xml critical
# logging monitor warnings
# logging cns-events warnings
# logging policy-firewall rate-limit 10
# logging dmvpn rate-limit 10
# logging trap errors
# logging facility local5
# logging snmp-trap errors
# logging host 10.0.1.13 transport tcp port 514
# logging host 10.0.1.11 xml
# logging host 10.0.1.12
# logging host 10.0.1.10 filtered stream 10
# logging host 10.0.1.25 filtered

# Using state: rendered

- name: Render the commands for provided configuration
  cisco.ios.ios_logging_global:
    config:
      - buffered:
          severity: notifications
          size: 5099
          xml: True
      - console:
          severity: critical
          xml: True
      - facility: local5
      - hosts:
        - hostname: 10.0.1.12
        - hostname: 10.0.1.11
          xml: True
        - hostname: 10.0.1.10
          filtered: True
          stream: 10
        - hostname: 10.0.1.13
          transport:
            tcp:
              port: 514
      - monitor:
          severity: warnings
      - message_counter: log
      - snmp_trap: errors
      - trap: errors
      - userinfo: True
      - policy_firewall:
          rate_limit: 10
      - logging_on: True
      - exception: 10
      - dmvpn:
          rate_limit: 10
      - cns_events: warnings
    state: rendered

# Module Execution Result:
# ------------------------

# "rendered": [
#     "logging host 10.0.1.12",
#     "logging host 10.0.1.11 xml",
#     "logging host 10.0.1.10 filtered stream 10",
#     "logging host 10.0.1.13 transport tcp port 514",
#     "logging message-counter log",
#     "logging snmp-trap errors",
#     "logging buffered xml 5099 notifications",
#     "logging console xml critical",
#     "logging facility local5",
#     "logging monitor warnings",
#     "logging trap errors",
#     "logging userinfo",
#     "logging policy-firewall rate-limit 10",
#     "logging on",
#     "logging exception 10",
#     "logging dmvpn rate-limit 10",
#     "logging cns-events warnings"
#     ]

# Using state: parsed

# File: parsed.cfg
# ----------------

# logging on
# logging count
# logging userinfo
# logging trap errors
# logging reload alerts
# logging host 10.0.1.1
# logging exception 4099
# logging history alerts
# logging facility local5
# logging snmp-trap errors
# logging monitor warnings
# logging origin-id hostname
# logging host 10.0.1.11 xml
# logging cns-events warnings
# logging dmvpn rate-limit 10
# logging message-counter log
# logging console xml critical
# logging message-counter debug
# logging persistent batch 4444
# logging host 10.0.1.25 filtered
# logging source-interface GBit1/0
# logging source-interface CTunnel2
# logging policy-firewall rate-limit 10
# logging buffered xml 5099 notifications
# logging rate-limit all 2 except warnings
# logging host 10.0.1.10 filtered stream 10
# logging host 10.0.1.13 transport tcp port 514
# logging discriminator msglog01 severity includes 5
# logging filter tftp://10.0.2.18/ESM/elate.tcl args TESTInst2
# logging filter tftp://10.0.2.14/ESM/escalate.tcl args TESTInst

- name: Parse the provided configuration with the existing running configuration
  cisco.ios.ios_logging_global:
    running_config: "{{ lookup('file', 'parsed.cfg') }}"
    state: parsed

# Module Execution Result:
# ------------------------

# "parsed": [
#         {
#             "buffered": {
#                 "severity": "notifications",
#                 "size": 5099,
#                 "xml": true
#             },
#             "cns_events": "warnings",
#             "console": {
#                 "severity": "critical",
#                 "xml": true
#             },
#             "count": true,
#             "discriminator": [
#                 "msglog01 severity includes 5"
#             ],
#             "dmvpn": {
#                 "rate_limit": 10
#             },
#             "exception": 4099,
#             "facility": "local5",
#             "filter": [
#                 {
#                     "args": "TESTInst2 ",
#                     "url": "tftp://10.0.2.18/ESM/elate.tcl"
#                 },
#                 {
#                     "args": "TESTInst",
#                     "url": "tftp://10.0.2.14/ESM/escalate.tcl"
#                 }
#             ],
#             "history": {
#                 "severity": "alerts"
#             },
#             "logging_on": true,
#             "message_counter": [
#                 "debug",
#                 "log"
#             ],
#             "monitor": {
#                 "severity": "warnings"
#             },
#             "origin_id": {
#                 "tag": "hostname"
#             },
#             "persistent": {
#                 "batch": 4444
#             },
#             "policy_firewall": {
#                 "rate_limit": 10
#             },
#             "rate_limit": {
#                 "all": true,
#                 "except_severity": "warnings",
#                 "size": 2
#             },
#             "reload": {
#                 "severity": "alerts"
#             },
#             "snmp_trap": [
#                 "errors"
#             ],
#             "source_interface": [
#                 {
#                     "interface": "GBit1/0"
#                 },
#                 {
#                     "interface": "CTunnel2"
#                 }
#             ],
#             "trap": "errors",
#             "userinfo": true
#         },
#         {
#             "hosts": [
#                 {
#                     "hostname": "10.0.1.1"
#                 },
#                 {
#                     "hostname": "10.0.1.11",
#                     "xml": true
#                 },
#                 {
#                     "filtered": true,
#                     "hostname": "10.0.1.25"
#                 },
#                 {
#                     "filtered": true,
#                     "hostname": "10.0.1.10",
#                     "stream": 10
#                 }
#             ]
#         }
#     ]
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.logging_global.logging_global import (
    Logging_globalArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.logging_global.logging_global import (
    Logging_global,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Logging_globalArgs.argument_spec,
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

    result = Logging_global(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
