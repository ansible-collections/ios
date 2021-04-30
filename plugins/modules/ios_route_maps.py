#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for cisco.ios_route_maps
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
module: ios_route_maps
short_description: Route maps resource module
description:
  - This module configures and manages the attributes of Route maps on Cisco IOS.
version_added: 2.1.0
author: Sumit Jaiswal (@justjais)
notes:
  - Tested against Cisco IOSv Version 15.2 on VIRL
  - This module works with connection C(network_cli).
    See L(IOS Platform Options,../network/user_guide/platform_ios.html)
options:
  config:
    description: A list of configurations for Route maps.
    type: list
    elements: dict
    suboptions:
      route_map:
        description: Route map tag/name
        type: str
      entries:
        description: A list of configurations entries for Route maps.
        type: list
        elements: dict
        suboptions:
          sequence:
            description:
              - Sequence to insert to/delete from existing route-map entry
              - Please refer vendor documentation for valid values
            type: int
          action:
            description: Route map set operations
            type: str
            choices: ['deny', 'permit']
          continue_entry:
            description: Continue on a different entry within the route-map
            type: dict
            suboptions:
              set:
                description: Set continue
                type: bool
              entry_sequence:
                description:
                  - Route-map entry sequence number
                  - Please refer vendor documentation for valid values
                type: int
          description:
            description: Route-map comment
            type: str
          match:
            description: Match values from routing table
            type: dict
            suboptions:
              additional_paths:
                description:
                  - BGP Add-Path match policie
                  - BGP Add-Path advertise-set policy
                type: dict
                suboptions:
                  all:
                    description: BGP Add-Path advertise all paths
                    type: bool
                  best:
                    description: BGP Add-Path advertise best n paths (1-3)
                    type: int
                  best_range:
                    description: BGP Add-Path advertise best paths (range m to n)
                    type: dict
                    suboptions:
                      lower_limit:
                        description: BGP Add-Path best paths to advertise (lower limit) (1-3)
                        type: int
                      upper_limit:
                        description: BGP Add-Path best paths to advertise (upper limit) (1-3)
                        type: int
                  group_best:
                    description: BGP Add-Path advertise group-best path
                    type: bool
              as_path:
                description: Match BGP AS path list
                type: dict
                suboptions:
                  set:
                    description: Set AS path list
                    type: bool
                  acls:
                    description:
                      - AS path access-list
                      - Please refer vendor documentation for valid values
                    type: list
                    elements: int
              clns:
                description: CLNS information
                type: dict
                suboptions:
                  address:
                    description: Match address of route or match packet
                    type: str
                  next_hop:
                    description: Match next-hop address of route
                    type: str
                  route_source:
                    description: Match advertising source address of route
                    type: str
              community:
                description: Match BGP community list
                type: dict
                suboptions:
                  name:
                    description:
                      - Community-list number/Community-list name
                      - Please refer vendor documentation for valid values
                    type: list
                    elements: str
                  exact_match:
                    description: Do exact matching of communities
                    type: bool
              extcommunity:
                description:
                  - Match BGP/VPN extended community list
                  - Extended community-list number
                  - Please refer vendor documentation for valid values
                type: list
                elements: str
              interfaces:
                description: Match first hop interface of route
                type: list
                elements: str
              ip:
                description: IP specific information
                type: dict
                suboptions:
                  address:
                    description: Match address of route or match packet
                    type: dict
                    suboptions:
                      acls: &acls
                        description:
                          - Match entries of acl
                          - IP acl name/number
                          - Please refer vendor documentation for valid values
                        type: list
                        elements: str
                      prefix_lists: &prefix_lists
                        description:
                          - Match entries of prefix-lists
                          - IP prefix-list name
                        type: list
                        elements: str
                  flowspec:
                    description: Match src/dest prefix component of flowspec prefix
                    type: dict
                    suboptions:
                      dest_pfx:
                        description: Match dest prefix component of flowspec prefix
                        type: bool
                      src_pfx:
                        description: Match source prefix component of flowspec prefix
                        type: bool
                      acls: *acls
                      prefix_lists: *prefix_lists
                  next_hop:
                    description: Match next-hop address of route
                    type: dict
                    suboptions:
                      set:
                        description: Set next-hop address
                        type: bool
                      acls: *acls
                      prefix_lists: *prefix_lists
                  redistribution_source:
                    description: route redistribution source (EIGRP only)
                    type: dict
                    suboptions:
                      set:
                        description: Set redistribution-source
                        type: bool
                      acls: *acls
                      prefix_lists: *prefix_lists
                  route_source:
                    description: Match advertising source address of route
                    type: dict
                    suboptions:
                      set:
                        description: Set redistribution-source
                        type: bool
                      redistribution_source:
                        description: route redistribution source (EIGRP only)
                        type: bool
                      acls: *acls
                      prefix_lists: *prefix_lists
              ipv6:
                description: IPv6 specific information
                type: dict
                suboptions:
                  address:
                    type: dict
                    description: Match address of route or match packet
                    suboptions:
                      acl:
                        description: IPv6 access-list name
                        type: str
                      prefix_list:
                        description: IPv6 prefix-list name
                        type: str
                  flowspec:
                    description: Match next-hop address of route
                    type: dict
                    suboptions:
                      dest_pfx:
                        description: Match dest prefix component of flowspec prefix
                        type: bool
                      src_pfx:
                        description: Match source prefix component of flowspec prefix
                        type: bool
                      acl:
                        description: IPv6 access-list name
                        type: str
                      prefix_list:
                        description: IPv6 prefix-list name
                        type: str
                  next_hop:
                    description: Match next-hop address of route
                    type: dict
                    suboptions:
                      acl:
                        description: IPv6 access-list name
                        type: str
                      prefix_list:
                        description: IPv6 prefix-list name
                        type: str
                  route_source:
                    description: Match advertising source address of route
                    type: dict
                    suboptions:
                      acl:
                        description: IPv6 access-list name
                        type: str
                      prefix_list:
                        description: IPv6 prefix-list name
                        type: str
              length:
                description: Packet length
                type: dict
                suboptions:
                  minimum:
                    description:
                      - Minimum packet length
                      - Please refer vendor documentation for valid values
                    type: int
                  maximum:
                    description:
                      - Maximum packet length
                      - Please refer vendor documentation for valid values
                    type: int
              local_preference:
                description: Local preference for route
                type: dict
                suboptions:
                  set:
                    description: Set the Local preference for route
                    type: bool
                  value:
                    description:
                      - Local preference value
                      - Please refer vendor documentation for valid values
                    type: list
                    elements: str
              mdt_group:
                description: Match routes corresponding to MDT group
                type: dict
                suboptions:
                  set:
                    description: Set and Match routes corresponding to MDT group
                    type: bool
                  acls:
                    description:
                      - IP access-list number/IP standard access-list name
                      - Please refer vendor documentation for valid values
                    type: list
                    elements: str
              metric:
                description: Match metric of route
                type: dict
                suboptions:
                  value:
                    description:
                      - Metric value
                      - Please refer vendor documentation for valid values
                    type: int
                  external:
                    description: Match route using external protocol metric
                    type: bool
                  deviation:
                    description: Deviation option to match metric in a range
                    type: bool
                  deviation_value:
                    description:
                      - deviation value, 500 +- 10 creates the range 490 - 510
                      - Please refer vendor documentation for valid values
                    type: int
              mpls_label:
                description: Match routes which have MPLS labels
                type: bool
              policy_lists:
                description: Match IP policy list
                type: list
                elements: str
              route_type:
                description: Match route-type of route
                type: dict
                suboptions:
                  external:
                    description: external route (BGP, EIGRP and OSPF type 1/2)
                    type: dict
                    suboptions:
                      set:
                        description: Set external route
                        type: bool
                      type_1:
                        description: OSPF external type 1 route
                        type: bool
                      type_2:
                        description: OSPF external type 2 route
                        type: bool
                  internal:
                    description: internal route (including OSPF intra/inter area)
                    type: bool
                  level_1:
                    description: IS-IS level-1 route
                    type: bool
                  level_2:
                    description: IS-IS level-2 route
                    type: bool
                  local:
                    description: locally generated route
                    type: bool
                  nssa_external:
                    description: nssa-external route (OSPF type 1/2)
                    type: dict
                    suboptions:
                      set:
                        description: Set nssa-external route
                        type: bool
                      type_1:
                        description: OSPF external type 1 route
                        type: bool
                      type_2:
                        description: OSPF external type 2 route
                        type: bool
              rpki:
                description: Match RPKI state of route
                type: dict
                suboptions:
                  invalid:
                    description: RPKI Invalid State
                    type: bool
                  not_found:
                    description: RPKI Not Found State
                    type: bool
                  valid:
                    description: RPKI Valid State
                    type: bool
              security_group:
                description: Security Group
                type: dict
                suboptions:
                  source:
                    description:
                      - Source Security Group, source Security tag
                      - Please refer vendor documentation for valid values
                    type: list
                    elements: int
                  destination:
                    description:
                      - Destination Security Group, destination Security tag
                      - Please refer vendor documentation for valid values
                    type: list
                    elements: int
              source_protocol:
                description: Match source-protocol of route
                type: dict
                suboptions:
                  bgp:
                    description:
                      - Border Gateway Protocol (BGP)
                      - Autonomous system number
                      - Please refer vendor documentation for valid values
                    type: str
                  connected:
                    description: Connected
                    type: bool
                  eigrp:
                    description:
                      - Enhanced Interior Gateway Routing Protocol (EIGRP)
                      - Autonomous system number
                      - Please refer vendor documentation for valid values
                    type: int
                  isis:
                    description: ISO IS-IS
                    type: bool
                  lisp:
                    description: Locator ID Separation Protocol (LISP)
                    type: bool
                  mobile:
                    description: Mobile routes
                    type: bool
                  ospf:
                    description:
                      - Open Shortest Path First (OSPF) Process ID
                      - Please refer vendor documentation for valid values
                    type: int
                  ospfv3:
                    description:
                      - OSPFv3 Process ID
                      - Please refer vendor documentation for valid values
                    type: int
                  rip:
                    description: Routing Information Protocol (RIP)
                    type: bool
                  static:
                    description: Static routes
                    type: bool
              tag:
                description: Match tag of route
                type: dict
                suboptions:
                  value:
                    description: Tag value/Tag in Dotted Decimal eg, 10.10.10.10
                    type: list
                    elements: str
                  tag_list:
                    description: Route Tag List/Tag list name
                    type: list
                    elements: str
              track:
                description: tracking object
                type: int
          set:
            description: Match source-protocol of route
            type: dict
            suboptions:
              aigp_metric:
                description: accumulated metric value
                type: dict
                suboptions:
                  value:
                    description: manual value
                    type: int
                  igp_metric:
                    description: metric value from rib
                    type: bool
              as_path:
                description: Prepend string for a BGP AS-path attribute
                type: dict
                suboptions:
                  prepend:
                    description: Prepend to the as-path
                    type: dict
                    suboptions:
                      as_number:
                        description:
                          - AS number
                          - Please refer vendor documentation for valid values
                        type: list
                        elements: str
                      last_as:
                        description:
                          - Prepend last AS to the as-path
                          - Number of last-AS prepends
                          - Please refer vendor documentation for valid values
                        type: int
                  tag:
                    description: Set the tag as an AS-path attribute
                    type: bool
              automatic_tag:
                description: Automatically compute TAG value
                type: bool
              clns:
                description:
                  - OSI summary address
                  - Next hop address
                  - CLNS summary prefix
                type: str
              comm_list:
                description:
                  - set BGP community list (for deletion)
                  - Community-list name/number
                  - Delete matching communities
                type: str
              community:
                description: BGP community attribute
                type: dict
                suboptions:
                  number:
                    description:
                      - community number
                      - community number in aa:nn format
                      - Please refer vendor documentation for valid values
                    type: str
                  additive:
                    description: Add to the existing community
                    type: bool
                  gshut:
                    description: Graceful Shutdown (well-known community)
                    type: bool
                  internet:
                    description: Internet (well-known community)
                    type: bool
                  local_as:
                    description: Do not send outside local AS (well-known community)
                    type: bool
                  no_advertise:
                    description: Do not advertise to any peer (well-known community)
                    type: bool
                  no_export:
                    description: Do not export to next AS (well-known community)
                    type: bool
                  none:
                    description: No community attribute
                    type: bool
              dampening:
                description: Set BGP route flap dampening parameters
                type: dict
                suboptions:
                  penalty_half_time:
                    description:
                      - half-life time for the penalty
                      - Please refer vendor documentation for valid values
                    type: int
                  reuse_route_val:
                    description:
                      - Penalty to start reusing a route
                      - Please refer vendor documentation for valid values
                    type: int
                  suppress_route_val:
                    description:
                      - Penalty to start suppressing a route
                      - Please refer vendor documentation for valid values
                    type: int
                  max_suppress:
                    description:
                      - Maximum duration to suppress a stable route
                      - Please refer vendor documentation for valid values
                    type: int
              default:
                description:
                  - Set default information
                  - Default output interface
                type: str
              extcomm_list:
                description:
                  - Set BGP/VPN extended community list (for deletion)
                  - Extended community-list number/name
                  - Delete matching extended communities
                type: str
              extcommunity:
                description: BGP extended community attribute
                type: dict
                suboptions:
                  cost:
                    description: Cost extended community
                    type: dict
                    suboptions:
                      id:
                        description:
                          - Community ID
                          - Please refer vendor documentation for valid values
                        type: str
                      cost_value:
                        description:
                          - Cost Value (No-preference Cost = 2147483647)
                          - Please refer vendor documentation for valid values
                        type: int
                      igp:
                        description: Compare following IGP cost comparison
                        type: bool
                      pre_bestpath:
                        description: Compare before all other steps in bestpath calculation
                        type: bool
                  rt:
                    description: Route Target extended community
                    type: dict
                    suboptions:
                      address:
                        description: VPN extended community
                        type: str
                      range:
                        description: Specify a range of extended community
                        type: dict
                        suboptions:
                          lower_limit:
                            description: VPN extended community
                            type: str
                          upper_limit:
                            description: VPN extended community
                            type: str
                      additive:
                        description: Add to the existing extcommunity
                        type: bool
                  soo:
                    description: Site-of-Origin extended community
                    type: str
                  vpn_distinguisher:
                    description: VPN Distinguisher
                    type: dict
                    suboptions:
                      address:
                        description: VPN extended community
                        type: str
                      range:
                        description: Specify a range of extended community
                        type: dict
                        suboptions:
                          lower_limit:
                            description: VPN extended community
                            type: str
                          upper_limit:
                            description: VPN extended community
                            type: str
                      additive:
                        description: Add to the existing extcommunity
                        type: bool
              global_route:
                description: Set to global routing table
                type: bool
              interfaces:
                description: Output interface
                type: list
                elements: str
              ip:
                description: IP specific information
                type: dict
                suboptions:
                  address:
                    description:
                      - Specify IP address
                      - Prefix-list name to set ip address
                    type: str
                  df:
                    description: Set DF bit
                    choices: [0, 1]
                    type: int
                  global_route:
                    description: global routing table
                    type: dict
                    suboptions:
                      address:
                        description: IP address of next hop
                        type: str
                      verify_availability:
                        description: Verify if nexthop is reachable
                        type: dict
                        suboptions:
                          address:
                            description: IP address of next hop
                            type: str
                          sequence:
                            description:
                              - Sequence to insert into next-hop list
                              - Please refer vendor documentation for valid values
                            type: int
                          track:
                            description:
                              - Set the next hop depending on the state of a tracked object
                              - tracked object number
                              - Please refer vendor documentation for valid values
                            type: int
                  next_hop:
                    description: Next hop address
                    type: dict
                    suboptions:
                      address:
                        description: IP address of next hop
                        type: str
                      dynamic:
                        description:
                          - application dynamically sets next hop
                          - DHCP learned next hop
                        type: bool
                      encapsulate:
                        description:
                          - Encapsulation profile for VPN nexthop
                          - L3VPN
                          - Encapsulation profile name
                        type: str
                      peer_address:
                        description: Use peer address (for BGP only)
                        type: bool
                      recursive:
                        description: Recursive next-hop
                        type: dict
                        suboptions:
                          global_route:
                            description: global routing table
                            type: bool
                          vrf:
                            description: VRF
                            type: str
                          address:
                            description: IP address of recursive next hop
                            type: str
                      self:
                        description: Use self address (for BGP only)
                        type: bool
                      verify_availability:
                        description: Verify if nexthop is reachable
                        type: dict
                        suboptions:
                          set:
                            description: Set and Verify if nexthop is reachable
                            type: bool
                          address:
                            description: IP address of next hop
                            type: str
                          sequence:
                            description:
                              - Sequence to insert into next-hop list
                              - Please refer vendor documentation for valid values
                            type: int
                          track:
                            description:
                              - Set the next hop depending on the state of a tracked object
                              - tracked object number
                              - Please refer vendor documentation for valid values
                            type: int
                  precedence:
                    description: Set precedence field
                    type: dict
                    suboptions:
                      set:
                        description: Just set precedence field
                        type: bool
                      critical:
                        description: Set critical precedence (5)
                        type: bool
                      flash:
                        description: Set flash precedence (3)
                        type: bool
                      flash_override:
                        description: Set flash override precedence (4)
                        type: bool
                      immediate:
                        description: Set immediate precedence (2)
                        type: bool
                      internet:
                        description: Set internetwork control precedence (6)
                        type: bool
                      network:
                        description: Set network control precedence (7)
                        type: bool
                      priority:
                        description: Set priority precedence (1)
                        type: bool
                      routine:
                        description: Set routine precedence (0)
                        type: bool
                  qos_group:
                    description:
                      - Set QOS Group ID
                      - Please refer vendor documentation for valid values
                    type: int
                  tos:
                    description: Set type of service field
                    type: dict
                    suboptions:
                      set:
                        description: Just set type of service field
                        type: bool
                      max_reliability:
                        description: Set max reliable TOS (2)
                        type: bool
                      max_throughput:
                        description: Set max throughput TOS (4)
                        type: bool
                      min_delay:
                        description: Set min delay TOS (8)
                        type: bool
                      min_monetary_cost:
                        description: Set min monetary cost TOS (1)
                        type: bool
                      normal:
                        description: Set normal TOS (0)
                        type: bool
                  vrf:
                    description: VRF
                    type: dict
                    suboptions:
                      name:
                        description: VRF name
                        type: str
                      address:
                        description: IP address of next hop
                        type: str
                      verify_availability:
                        description: Verify if nexthop is reachable
                        type: dict
                        suboptions:
                          set:
                            description: Set and Verify if nexthop is reachable
                            type: bool
                          address:
                            description: IP address of next hop
                            type: str
                          sequence:
                            description:
                              - Sequence to insert into next-hop list
                              - Please refer vendor documentation for valid values
                            type: int
                          track:
                            description:
                              - Set the next hop depending on the state of a tracked object
                              - tracked object number
                              - Please refer vendor documentation for valid values
                            type: int
              ipv6:
                description: IPv6 specific information
                type: dict
                suboptions:
                  address:
                    description:
                      - IPv6 address
                      - IPv6 prefix-list
                    type: str
                  default:
                    description: Set default information
                    type: bool
                  global_route:
                    description: global routing table
                    type: dict
                    suboptions:
                      address:
                        description: Next hop address (X:X:X:X::X)
                        type: str
                      verify_availability:
                        description: Verify if nexthop is reachable
                        type: dict
                        suboptions:
                          address:
                            description: Next hop address (X:X:X:X::X)
                            type: str
                          sequence:
                            description:
                              - Sequence to insert into next-hop list
                              - Please refer vendor documentation for valid values
                            type: int
                          track:
                            description:
                              - Set the next hop depending on the state of a tracked object
                              - tracked object number
                              - Please refer vendor documentation for valid values
                            type: int
                  next_hop:
                    description: IPv6 Next hop
                    type: dict
                    suboptions:
                      address:
                        description: Next hop address (X:X:X:X::X)
                        type: str
                      encapsulate:
                        description:
                          - Encapsulation profile for VPN nexthop
                          - L3VPN
                          - Encapsulation profile name
                        type: str
                      peer_address:
                        description: Use peer address (for BGP only)
                        type: bool
                      recursive:
                        description:
                          - Recursive next-hop
                          - IPv6 address of recursive next-hop
                        type: str
                  precedence:
                    description:
                      - Set precedence field
                      - Precedence value
                      - Please refer vendor documentation for valid values
                    type: int
                  vrf:
                    description: VRF name
                    type: dict
                    suboptions:
                      name:
                        description: VRF name
                        type: str
                      verify_availability:
                        description: Verify if nexthop is reachable
                        type: dict
                        suboptions:
                          address:
                            description: IPv6 address of next hop
                            type: str
                          sequence:
                            description:
                              - Sequence to insert into next-hop list
                              - Please refer vendor documentation for valid values
                            type: int
                          track:
                            description:
                              - Set the next hop depending on the state of a tracked object
                              - tracked object number
                              - Please refer vendor documentation for valid values
                            type: int
              level:
                description: Where to import route
                type: dict
                suboptions:
                  level_1:
                    description: Import into a level-1 area
                    type: bool
                  level_1_2:
                    description: Import into level-1 and level-2
                    type: bool
                  level_2:
                    description: Import into level-2 sub-domain
                    type: bool
                  nssa_only:
                    description: Import only into OSPF NSSA areas and don't propagate
                    type: bool
              lisp:
                description:
                  - Locator ID Separation Protocol specific information
                  - Specify a locator-set to use in LISP route-import
                  - The name of the locator set
                type: str
              local_preference:
                description:
                  - BGP local preference path attribute
                  - Please refer vendor documentation for valid values
                type: int
              metric:
                description: Metric value for destination routing protocol
                type: dict
                suboptions:
                  deviation:
                    description: Add or subtract metric
                    choices: ['plus', 'minus']
                    type: str
                  metric_value:
                    description:
                      - Metric value or Bandwidth in Kbits per second
                      - Please refer vendor documentation for valid values
                    type: int
                  eigrp_delay:
                    description:
                      - EIGRP delay metric, in 10 microsecond units
                      - Please refer vendor documentation for valid values
                    type: int
                  metric_reliability:
                    description:
                      - EIGRP reliability metric where 255 is 100 reliable
                      - Please refer vendor documentation for valid values
                    type: int
                  metric_bandwidth:
                    description:
                      - EIGRP Effective bandwidth metric (Loading) where 255 is 100 loaded
                      - Please refer vendor documentation for valid values
                    type: int
                  mtu:
                    description:
                      - EIGRP MTU of the path
                      - Please refer vendor documentation for valid values
                    type: int
              metric_type:
                description: Type of metric for destination routing protocol
                type: dict
                suboptions:
                  external:
                    description: IS-IS external metric
                    type: bool
                  internal:
                    description: IS-IS internal metric or Use IGP metric as the MED for BGP
                    type: bool
                  type_1:
                    description: OSPF external type 1 metric
                    type: bool
                  type_2:
                    description: OSPF external type 2 metric
                    type: bool
              mpls_label:
                description: Set MPLS label for prefix
                type: bool
              origin:
                description: BGP origin code
                type: dict
                suboptions:
                  igp:
                    description: local IGP
                    type: bool
                  incomplete:
                    description: unknown heritage
                    type: bool
              tag:
                description:
                  - Tag value for destination routing protocol
                  - Tag value A.B.C.D(dotted decimal format)/Tag value
                type: str
              traffic_index:
                description:
                  - BGP traffic classification number for accounting
                  - Please refer vendor documentation for valid values
                type: int
              vrf:
                description:
                  - Define VRF name
                  - VPN Routing/Forwarding instance name
                type: str
              weight:
                description:
                  - BGP weight for routing table
                  - Please refer vendor documentation for valid values
                type: int
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the IOS
        device by executing the command B(sh running-config | section ^route-map).
      - The state I(parsed) reads the configuration from C(running_config)
        option and transforms it into Ansible structured data as per the
        resource module's argspec and the value is then returned in the
        I(parsed) key within the result.
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
        | section ^route-map) executed on device. For state I(parsed) active
        connection to remote host is not required.
    type: str
"""

EXAMPLES = """

# Using deleted

# Before state:
# -------------
#
# router-ios#sh running-config | section ^route-map
# route-map test_1 deny 10
#  description this is test route
#  match ip next-hop prefix-list test_2_new test_1_new
#  match ip route-source 10
#  match security-group source tag 10 20
#  match local-preference 100 50
#  match mpls-label
# route-map test_1 deny 20
#  match track  105
#  match tag list test_match_tag
#  match route-type level-1
#  match additional-paths advertise-set all group-best
#  match as-path 200 100
#  match ipv6 address test_acl_20
#  continue 100
# route-map test_2 deny 10
#  match security-group source tag 10 20
#  match local-preference 55 105
#  match mpls-label
#  match ipv6 address test_ip_acl
#  match ipv6 next-hop prefix-list test_new
#  match ipv6 route-source route_src_acl
#  set automatic-tag
#  set ip precedence critical
#  set ip address prefix-list 192.0.2.1
#  set aigp-metric 100
#  set extcommunity cost pre-bestpath 10 100
#  set ip df 1
#  set ip next-hop verify-availability 198.51.111.1 100 track 10
#  set ip next-hop recursive global 198.51.110.1

- name: Delete provided Route maps config
  cisco.ios.ios_route_maps:
    config:
      - route_map: test_1
    state: deleted

#  Commands Fired:
#  ---------------
#
#  "commands": [
#         "no route-map test_1"
#     ]

# After state:
# -------------
# router-ios#sh running-config | section ^route-map
# route-map test_2 deny 10
#  match security-group source tag 10 20
#  match local-preference 55 105
#  match mpls-label
#  match ipv6 address test_ip_acl
#  match ipv6 next-hop prefix-list test_new
#  match ipv6 route-source route_src_acl
#  set automatic-tag
#  set ip precedence critical
#  set ip address prefix-list 192.0.2.1
#  set aigp-metric 100
#  set extcommunity cost pre-bestpath 10 100
#  set ip df 1
#  set ip next-hop verify-availability 198.51.111.1 100 track 10
#  set ip next-hop recursive global 198.51.110.1

# Using deleted without any config passed (NOTE: This will delete all Route maps configuration from device)

# Before state:
# -------------
#
# router-ios#sh running-config | section ^route-map
# route-map test_1 deny 10
#  description this is test route
#  match ip next-hop prefix-list test_2_new test_1_new
#  match ip route-source 10
#  match security-group source tag 10 20
#  match local-preference 100 50
#  match mpls-label
# route-map test_1 deny 20
#  match track  105
#  match tag list test_match_tag
#  match route-type level-1
#  match additional-paths advertise-set all group-best
#  match as-path 200 100
#  match ipv6 address test_acl_20
#  continue 100
# route-map test_2 deny 10
#  match security-group source tag 10 20
#  match local-preference 55 105
#  match mpls-label
#  match ipv6 address test_ip_acl
#  match ipv6 next-hop prefix-list test_new
#  match ipv6 route-source route_src_acl
#  set automatic-tag
#  set ip precedence critical
#  set ip address prefix-list 192.0.2.1
#  set aigp-metric 100
#  set extcommunity cost pre-bestpath 10 100
#  set ip df 1
#  set ip next-hop verify-availability 198.51.111.1 100 track 10
#  set ip next-hop recursive global 198.51.110.1

- name: Delete all Route maps config
  cisco.ios.ios_route_maps:
    state: deleted

# Commands Fired:
# ---------------
#
#  "commands": [
#         "no route-map test_1",
#         "no route-map test_2"
#     ]

# After state:
# -------------
# router-ios#sh running-config | section ^route-map
# router-ios#

# Using merged

# Before state:
# -------------
#
# router-ios#sh running-config | section ^route-map
# router-ios#

- name: Merge provided Route maps configuration
  cisco.ios.ios_route_maps:
    config:
      - route_map: test_1
        entries:
          - sequence: 10
            action: deny
            description: this is test route
            match:
              ip:
                next_hop:
                  prefix_lists:
                    - test_1_new
                    - test_2_new
                route_source:
                  acls:
                    - 10
              security_group:
                source:
                  - 10
                  - 20
              local_preference:
                value:
                  - 50
                  - 100
              mpls_label: true
          - sequence: 20
            action: deny
            continue_entry:
              entry_sequence: 100
            match:
              additional_paths:
                all: true
                group_best: true
              as_path:
                acls:
                  - 100
                  - 200
              ipv6:
                address:
                  acl: test_acl_20
              route_type:
                level_1: true
              tag:
                tag_list:
                  - test_match_tag
              track: 105
      - route_map: test_2
        entries:
          - sequence: 10
            action: deny
            match:
              ipv6:
                address:
                  acl: test_ip_acl
                next_hop:
                  prefix_list: test_new
                route_source:
                  acl: route_src_acl
              security_group:
                source:
                  - 10
                  - 20
              local_preference:
                value:
                  - 55
                  - 105
              mpls_label: true
            set:
              aigp_metric:
                value: 100
              automatic_tag: true
              extcommunity:
                cost:
                  id: 10
                  cost_value: 100
                  pre_bestpath: true
              ip:
                address: 192.0.2.1
                df: 1
                next_hop:
                  recursive:
                    global_route: true
                    address: 198.51.110.1
                  verify_availability:
                    address: 198.51.111.1
                    sequence: 100
                    track: 10
                precedence:
                  critical: true
    state: merged

#  Commands Fired:
#  ---------------
#
#   "commands": [
#      "route-map test_2 deny 10",
#      "match security-group source tag 10 20",
#      "match local-preference 55 105",
#      "match mpls-label",
#      "match ipv6 next-hop prefix-list test_new",
#      "match ipv6 route-source route_src_acl",
#      "match ipv6 address test_ip_acl",
#      "set extcommunity cost pre-bestpath 10 100",
#      "set ip df 1",
#      "set ip next-hop recursive global 198.51.110.1",
#      "set ip next-hop verify-availability 198.51.111.1 100 track 10",
#      "set ip precedence critical",
#      "set ip address prefix-list 192.0.2.1",
#      "set automatic-tag",
#      "set aigp-metric 100",
#      "route-map test_1 deny 20",
#      "continue 100",
#      "match track 105",
#      "match tag list test_match_tag",
#      "match ipv6 address test_acl_20",
#      "match route-type level-1",
#      "match as-path 200 100",
#      "match additional-paths advertise-set all group-best",
#      "route-map test_1 deny 10",
#      "description this is test route",
#      "match security-group source tag 10 20",
#      "match ip next-hop prefix-list test_2_new test_1_new",
#      "match ip route-source 10",
#      "match local-preference 100 50",
#      "match mpls-label"
#     ]

# After state:
# -------------
#
# router-ios#sh running-config | section ^route-map
# route-map test_1 deny 10
#  description this is test route
#  match ip next-hop prefix-list test_2_new test_1_new
#  match ip route-source 10
#  match security-group source tag 10 20
#  match local-preference 100 50
#  match mpls-label
# route-map test_1 deny 20
#  match track  105
#  match tag list test_match_tag
#  match route-type level-1
#  match additional-paths advertise-set all group-best
#  match as-path 200 100
#  match ipv6 address test_acl_20
#  continue 100
# route-map test_2 deny 10
#  match security-group source tag 10 20
#  match local-preference 55 105
#  match mpls-label
#  match ipv6 address test_ip_acl
#  match ipv6 next-hop prefix-list test_new
#  match ipv6 route-source route_src_acl
#  set automatic-tag
#  set ip precedence critical
#  set ip address prefix-list 192.0.2.1
#  set aigp-metric 100
#  set extcommunity cost pre-bestpath 10 100
#  set ip df 1
#  set ip next-hop verify-availability 198.51.111.1 100 track 10
#  set ip next-hop recursive global 198.51.110.1

# Using overridden

# Before state:
# -------------
#
# router-ios#sh running-config | section ^route-map
# route-map test_1 deny 10
#  description this is test route
#  match ip next-hop prefix-list test_2_new test_1_new
#  match ip route-source 10
#  match security-group source tag 10 20
#  match local-preference 100 50
#  match mpls-label
# route-map test_1 deny 20
#  match track  105
#  match tag list test_match_tag
#  match route-type level-1
#  match additional-paths advertise-set all group-best
#  match as-path 200 100
#  match ipv6 address test_acl_20
#  continue 100
# route-map test_2 deny 10
#  match security-group source tag 10 20
#  match local-preference 55 105
#  match mpls-label
#  match ipv6 address test_ip_acl
#  match ipv6 next-hop prefix-list test_new
#  match ipv6 route-source route_src_acl
#  set automatic-tag
#  set ip precedence critical
#  set ip address prefix-list 192.0.2.1
#  set aigp-metric 100
#  set extcommunity cost pre-bestpath 10 100
#  set ip df 1
#  set ip next-hop verify-availability 198.51.111.1 100 track 10
#  set ip next-hop recursive global 198.51.110.1

- name: Override provided Route maps configuration
  cisco.ios.ios_route_maps:
    config:
      - route_map: test_1
        entries:
          - sequence: 10
            action: deny
            description: this is override route
            match:
              ip:
                next_hop:
                  acls:
                    - 10
                    - test1_acl
                flowspec:
                  dest_pfx: true
                  acls:
                    - test_acl_1
                    - test_acl_2
              length:
                minimum: 10
                maximum: 100
              metric:
                value: 10
                external: true
              security_group:
                source:
                  - 10
                  - 20
              mpls_label: true
            set:
              extcommunity:
                vpn_distinguisher:
                  address: 192.0.2.1:12
                  additive: true
              metric:
                metric_value: 100
                deviation: plus
                eigrp_delay: 100
                metric_reliability: 10
                metric_bandwidth: 20
                mtu: 30
      - route_map: test_override
        entries:
          - sequence: 10
            action: deny
            match:
              ipv6:
                address:
                  acl: test_acl
                next_hop:
                  prefix_list: test_new
                route_source:
                  acl: route_src_acl
              security_group:
                source:
                  - 15
                  - 20
              local_preference:
                value:
                  - 105
                  - 110
              mpls_label: true
            set:
              aigp_metric:
                value: 100
              automatic_tag: true
              extcommunity:
                cost:
                  id: 10
                  cost_value: 100
                  pre_bestpath: true
              ip:
                address: 192.0.2.1
                df: 1
                next_hop:
                  recursive:
                    global_route: true
                    address: 198.110.51.1
                  verify_availability:
                    address: 198.110.51.2
                    sequence: 100
                    track: 10
                precedence:
                  critical: true
    state: overridden

# Commands Fired:
# ---------------
#
#  "commands": [
#         "no route-map test_2",
#         "route-map test_override deny 10",
#         "match security-group source tag 15 20",
#         "match local-preference 110 105",
#         "match mpls-label",
#         "match ipv6 next-hop prefix-list test_new",
#         "match ipv6 route-source route_src_acl",
#         "match ipv6 address test_acl",
#         "set extcommunity cost pre-bestpath 10 100",
#         "set ip df 1",
#         "set ip next-hop recursive global 198.110.51.1",
#         "set ip next-hop verify-availability 198.110.51.2 100 track 10",
#         "set ip precedence critical",
#         "set ip address prefix-list 192.0.2.1",
#         "set automatic-tag",
#         "set aigp-metric 100",
#         "route-map test_1 deny 10",
#         "no description this is test route",
#         "description this is override route",
#         "match ip flowspec dest-pfx test_acl_1 test_acl_2",
#         "no match ip next-hop prefix-list test_2_new test_1_new",
#         "match ip next-hop test1_acl 10",
#         "no match ip route-source 10",
#         "match metric external 10",
#         "match length 10 100",
#         "no match local-preference 100 50",
#         "set extcommunity vpn-distinguisher 192.0.2.1:12 additive",
#         "set metric 100 +100 10 20 30",
#         "no route-map test_1 deny 20"
#     ]

# After state:
# -------------
#
# router-ios#sh running-config | section ^route-map
# route-map test_override deny 10
#  match security-group source tag 15 20
#  match local-preference 110 105
#  match mpls-label
#  match ipv6 address test_acl
#  match ipv6 next-hop prefix-list test_new
#  match ipv6 route-source route_src_acl
#  set automatic-tag
#  set ip precedence critical
#  set ip address prefix-list 192.0.2.1
#  set aigp-metric 100
#  set extcommunity cost pre-bestpath 10 100
#  set ip df 1
#  set ip next-hop verify-availability 198.110.51.2 100 track 10
#  set ip next-hop recursive global 198.110.51.1
# route-map test_1 deny 10
#  description this is override route
#  match ip flowspec dest-pfx test_acl_1 test_acl_2
#  match ip next-hop test1_acl 10
#  match security-group source tag 10 20
#  match metric external 10
#  match mpls-label
#  match length 10 100
#  set metric 100 +100 10 20 30
#  set extcommunity vpn-distinguisher 192.0.2.1:12 additive

# Using replaced

# Before state:
# -------------
#
# router-ios#sh running-config | section ^route-map
# route-map test_1 deny 10
#  description this is test route
#  match ip next-hop prefix-list test_2_new test_1_new
#  match ip route-source 10
#  match security-group source tag 10 20
#  match local-preference 100 50
#  match mpls-label
# route-map test_1 deny 20
#  match track  105
#  match tag list test_match_tag
#  match route-type level-1
#  match additional-paths advertise-set all group-best
#  match as-path 200 100
#  match ipv6 address test_acl_20
#  continue 100
# route-map test_2 deny 10
#  match security-group source tag 10 20
#  match local-preference 55 105
#  match mpls-label
#  match ipv6 address test_ip_acl
#  match ipv6 next-hop prefix-list test_new
#  match ipv6 route-source route_src_acl
#  set automatic-tag
#  set ip precedence critical
#  set ip address prefix-list 192.0.2.1
#  set aigp-metric 100
#  set extcommunity cost pre-bestpath 10 100
#  set ip df 1
#  set ip next-hop verify-availability 198.51.111.1 100 track 10
#  set ip next-hop recursive global 198.51.110.1

- name: Replaced provided Route maps configuration
  cisco.ios.ios_route_maps:
    config:
      - route_map: test_1
        entries:
          - sequence: 10
            action: deny
            description: this is replaced route
            match:
              ip:
                next_hop:
                  acls:
                    - 10
                    - test1_acl
                flowspec:
                  dest_pfx: true
                  acls:
                    - test_acl_1
                    - test_acl_2
              length:
                minimum: 10
                maximum: 100
              metric:
                value: 10
                external: true
              security_group:
                source:
                  - 10
                  - 20
              mpls_label: true
            set:
              extcommunity:
                vpn_distinguisher:
                  address: 192.0.2.1:12
                  additive: true
              metric:
                metric_value: 100
                deviation: plus
                eigrp_delay: 100
                metric_reliability: 10
                metric_bandwidth: 20
                mtu: 30
      - route_map: test_replaced
        entries:
          - sequence: 10
            action: deny
            match:
              ipv6:
                address:
                  acl: test_acl
                next_hop:
                  prefix_list: test_new
                route_source:
                  acl: route_src_acl
              security_group:
                source:
                  - 15
                  - 20
              local_preference:
                value:
                  - 105
                  - 110
              mpls_label: true
            set:
              aigp_metric:
                value: 100
              automatic_tag: true
              extcommunity:
                cost:
                  id: 10
                  cost_value: 100
                  pre_bestpath: true
              ip:
                address: 192.0.2.1
                df: 1
                next_hop:
                  recursive:
                    global_route: true
                    address: 198.110.51.1
                  verify_availability:
                    address: 198.110.51.2
                    sequence: 100
                    track: 10
                precedence:
                  critical: true
    state: replaced

# Commands Fired:
# ---------------
#  "commands": [
#         "route-map test_replaced deny 10",
#         "match security-group source tag 15 20",
#         "match local-preference 110 105",
#         "match mpls-label",
#         "match ipv6 next-hop prefix-list test_new",
#         "match ipv6 route-source route_src_acl",
#         "match ipv6 address test_acl",
#         "set extcommunity cost pre-bestpath 10 100",
#         "set ip df 1",
#         "set ip next-hop recursive global 198.110.51.1",
#         "set ip next-hop verify-availability 198.110.51.2 100 track 10",
#         "set ip precedence critical",
#         "set ip address prefix-list 192.0.2.1",
#         "set automatic-tag",
#         "set aigp-metric 100",
#         "route-map test_1 deny 10",
#         "no description this is test route",
#         "description this is replaced route",
#         "match ip flowspec dest-pfx test_acl_1 test_acl_2",
#         "no match ip next-hop prefix-list test_2_new test_1_new",
#         "match ip next-hop test1_acl 10",
#         "no match ip route-source 10",
#         "match metric external 10",
#         "match length 10 100",
#         "no match local-preference 100 50",
#         "set extcommunity vpn-distinguisher 192.0.2.1:12 additive",
#         "set metric 100 +100 10 20 30",
#         "no route-map test_1 deny 20"
#     ]

# After state:
# -------------
#
# router-ios#sh running-config | section ^route-map
# route-map test_replaced deny 10
#  match security-group source tag 15 20
#  match local-preference 110 105
#  match mpls-label
#  match ipv6 address test_acl
#  match ipv6 next-hop prefix-list test_new
#  match ipv6 route-source route_src_acl
#  set automatic-tag
#  set ip precedence critical
#  set ip address prefix-list 192.0.2.1
#  set aigp-metric 100
#  set extcommunity cost pre-bestpath 10 100
#  set ip df 1
#  set ip next-hop verify-availability 198.110.51.2 100 track 10
#  set ip next-hop recursive global 198.110.51.1
# route-map test_1 deny 10
#  description this is replaced route
#  match ip flowspec dest-pfx test_acl_1 test_acl_2
#  match ip next-hop test1_acl 10
#  match security-group source tag 10 20
#  match metric external 10
#  match mpls-label
#  match length 10 100
#  set metric 100 +100 10 20 30
#  set extcommunity vpn-distinguisher 192.0.2.1:12 additive
# route-map test_2 deny 10
#  match security-group source tag 10 20
#  match local-preference 55 105
#  match mpls-label
#  match ipv6 address test_ip_acl
#  match ipv6 next-hop prefix-list test_new
#  match ipv6 route-source route_src_acl
#  set automatic-tag
#  set ip precedence critical
#  set ip address prefix-list 192.0.2.1
#  set aigp-metric 100
#  set extcommunity cost pre-bestpath 10 100
#  set ip df 1
#  set ip next-hop verify-availability 198.51.111.1 100 track 10
#  set ip next-hop recursive global 198.51.110.1

# Using Gathered

# Before state:
# -------------
#
# router-ios#sh running-config | section ^route-map
# route-map test_1 deny 10
#  description this is test route
#  match ip next-hop prefix-list test_2_new test_1_new
#  match ip route-source 10
#  match security-group source tag 10 20
#  match local-preference 100 50
#  match mpls-label
# route-map test_1 deny 20
#  match track  105
#  match tag list test_match_tag
#  match route-type level-1
#  match additional-paths advertise-set all group-best
#  match as-path 200 100
#  match ipv6 address test_acl_20
#  continue 100
# route-map test_2 deny 10
#  match security-group source tag 10 20
#  match local-preference 55 105
#  match mpls-label
#  match ipv6 address test_ip_acl
#  match ipv6 next-hop prefix-list test_new
#  match ipv6 route-source route_src_acl
#  set automatic-tag
#  set ip precedence critical
#  set ip address prefix-list 192.0.2.1
#  set aigp-metric 100
#  set extcommunity cost pre-bestpath 10 100
#  set ip df 1
#  set ip next-hop verify-availability 198.51.111.1 100 track 10
#  set ip next-hop recursive global 198.51.110.1

- name: Gather Route maps provided configurations
  cisco.ios.ios_route_maps:
    config:
    state: gathered

# Module Execution Result:
# ------------------------
#
# "gathered": [
#         {
#             "entries": [
#                 {
#                     "action": "deny",
#                     "description": "this is test route",
#                     "match": {
#                         "ip": {
#                             "next_hop": {
#                                 "prefix_lists": [
#                                     "test_2_new",
#                                     "test_1_new"
#                                 ]
#                             },
#                             "route_source": {
#                                 "acls": [
#                                     "10"
#                                 ]
#                             }
#                         },
#                         "local_preference": {
#                             "value": [
#                                 "100",
#                                 "50"
#                             ]
#                         },
#                         "mpls_label": true,
#                         "security_group": {
#                             "source": [
#                                 10,
#                                 20
#                             ]
#                         }
#                     },
#                     "sequence": 10
#                 },
#                 {
#                     "action": "deny",
#                     "continue_entry": {
#                         "entry_sequence": 100
#                     },
#                     "match": {
#                         "additional_paths": {
#                             "all": true,
#                             "group_best": true
#                         },
#                         "as_path": {
#                             "acls": [
#                                 200,
#                                 100
#                             ]
#                         },
#                         "ipv6": {
#                             "address": {
#                                 "acl": "test_acl_20"
#                             }
#                         },
#                         "route_type": {
#                             "external": {
#                                 "set": true
#                             },
#                             "level_1": true,
#                             "nssa_external": {
#                                 "set": true
#                             }
#                         },
#                         "tag": {
#                             "tag_list": [
#                                 "test_match_tag"
#                             ]
#                         },
#                         "track": 105
#                     },
#                     "sequence": 20
#                 }
#             ],
#             "route_map": "test_1"
#         },
#         {
#             "entries": [
#                 {
#                     "action": "deny",
#                     "match": {
#                         "ipv6": {
#                             "address": {
#                                 "acl": "test_ip_acl"
#                             },
#                             "next_hop": {
#                                 "prefix_list": "test_new"
#                             },
#                             "route_source": {
#                                 "acl": "route_src_acl"
#                             }
#                         },
#                         "local_preference": {
#                             "value": [
#                                 "55",
#                                 "105"
#                             ]
#                         },
#                         "mpls_label": true,
#                         "security_group": {
#                             "source": [
#                                 10,
#                                 20
#                             ]
#                         }
#                     },
#                     "sequence": 10,
#                     "set": {
#                         "aigp_metric": {
#                             "value": 100
#                         },
#                         "automatic_tag": true,
#                         "extcommunity": {
#                             "cost": {
#                                 "cost_value": 100,
#                                 "id": "10",
#                                 "pre_bestpath": true
#                             }
#                         },
#                         "ip": {
#                             "address": "192.0.2.1",
#                             "df": 1,
#                             "next_hop": {
#                                 "recursive": {
#                                     "address": "198.51.110.1",
#                                     "global_route": true
#                                 },
#                                 "verify_availability": {
#                                     "address": "198.51.111.1",
#                                     "sequence": 100,
#                                     "track": 10
#                                 }
#                             },
#                             "precedence": {
#                                 "critical": true
#                             }
#                         }
#                     }
#                 }
#             ],
#             "route_map": "test_2"
#         }
#     ]

# After state:
# ------------
#
# router-ios#sh running-config | section ^route-map
# route-map test_1 deny 10
#  description this is test route
#  match ip next-hop prefix-list test_2_new test_1_new
#  match ip route-source 10
#  match security-group source tag 10 20
#  match local-preference 100 50
#  match mpls-label
# route-map test_1 deny 20
#  match track  105
#  match tag list test_match_tag
#  match route-type level-1
#  match additional-paths advertise-set all group-best
#  match as-path 200 100
#  match ipv6 address test_acl_20
#  continue 100
# route-map test_2 deny 10
#  match security-group source tag 10 20
#  match local-preference 55 105
#  match mpls-label
#  match ipv6 address test_ip_acl
#  match ipv6 next-hop prefix-list test_new
#  match ipv6 route-source route_src_acl
#  set automatic-tag
#  set ip precedence critical
#  set ip address prefix-list 192.0.2.1
#  set aigp-metric 100
#  set extcommunity cost pre-bestpath 10 100
#  set ip df 1
#  set ip next-hop verify-availability 198.51.111.1 100 track 10
#  set ip next-hop recursive global 198.51.110.1

# Using Rendered

- name: Render the commands for provided  configuration
  cisco.ios.ios_route_maps:
    config:
      - route_map: test_1
        entries:
          - sequence: 10
            action: deny
            description: this is test route
            match:
              ip:
                next_hop:
                  prefix_lists:
                    - test_1_new
                    - test_2_new
                route_source:
                  acls:
                    - 10
              security_group:
                source:
                  - 10
                  - 20
              local_preference:
                value:
                  - 50
                  - 100
              mpls_label: true
          - sequence: 20
            action: deny
            continue_entry:
              entry_sequence: 100
            match:
              additional_paths:
                all: true
                group_best: true
              as_path:
                acls:
                  - 100
                  - 200
              ipv6:
                address:
                  acl: test_acl_20
              route_type:
                level_1: true
              tag:
                tag_list:
                  - test_match_tag
              track: 105
      - route_map: test_2
        entries:
          - sequence: 10
            action: deny
            match:
              ipv6:
                address:
                  acl: test_ip_acl
                next_hop:
                  prefix_list: test_new
                route_source:
                  acl: route_src_acl
              security_group:
                source:
                  - 10
                  - 20
              local_preference:
                value:
                  - 55
                  - 105
              mpls_label: true
            set:
              aigp_metric:
                value: 100
              automatic_tag: true
              extcommunity:
                cost:
                  id: 10
                  cost_value: 100
                  pre_bestpath: true
              ip:
                address: 192.0.2.1
                df: 1
                next_hop:
                  recursive:
                    global_route: true
                    address: 198.51.110.1
                  verify_availability:
                    address: 198.51.111.1
                    sequence: 100
                    track: 10
                precedence:
                  critical: true
    state: rendered

# Module Execution Result:
# ------------------------
#
#  "rendered": [
#      "route-map test_2 deny 10",
#      "match security-group source tag 10 20",
#      "match local-preference 55 105",
#      "match mpls-label",
#      "match ipv6 next-hop prefix-list test_new",
#      "match ipv6 route-source route_src_acl",
#      "match ipv6 address test_ip_acl",
#      "set extcommunity cost pre-bestpath 10 100",
#      "set ip df 1",
#      "set ip next-hop recursive global 198.51.110.1",
#      "set ip next-hop verify-availability 198.51.111.1 100 track 10",
#      "set ip precedence critical",
#      "set ip address prefix-list 192.0.2.1",
#      "set automatic-tag",
#      "set aigp-metric 100",
#      "route-map test_1 deny 20",
#      "continue 100",
#      "match track 105",
#      "match tag list test_match_tag",
#      "match ipv6 address test_acl_20",
#      "match route-type level-1",
#      "match as-path 200 100",
#      "match additional-paths advertise-set all group-best",
#      "route-map test_1 deny 10",
#      "description this is test route",
#      "match security-group source tag 10 20",
#      "match ip next-hop prefix-list test_2_new test_1_new",
#      "match ip route-source 10",
#      "match local-preference 100 50",
#      "match mpls-label"
#     ]

# Using Parsed

# File: parsed.cfg
# ----------------
#
# route-map test_1 deny 10
#  description this is test route
#  match ip next-hop prefix-list test_2_new test_1_new
#  match ip route-source 10
#  match security-group source tag 10 20
#  match local-preference 100 50
#  match mpls-label
# route-map test_1 deny 20
#  match track  105
#  match tag list test_match_tag
#  match route-type level-1
#  match additional-paths advertise-set all group-best
#  match as-path 200 100
#  match ipv6 address test_acl_20
#  continue 100
# route-map test_2 deny 10
#  match security-group source tag 10 20
#  match local-preference 55 105
#  match mpls-label
#  match ipv6 address test_ip_acl
#  match ipv6 next-hop prefix-list test_new
#  match ipv6 route-source route_src_acl
#  set automatic-tag
#  set ip precedence critical
#  set ip address prefix-list 192.0.2.1
#  set aigp-metric 100
#  set extcommunity cost pre-bestpath 10 100
#  set ip df 1
#  set ip next-hop verify-availability 198.51.111.1 100 track 10
#  set ip next-hop recursive global 198.51.110.1

- name: Parse the provided configuration with the existing running configuration
  cisco.ios.ios_route_maps:
    running_config: "{{ lookup('file', 'parsed.cfg') }}"
    state: parsed

# Module Execution Result:
# ------------------------
#
# "parsed": [
#         {
#             "entries": [
#                 {
#                     "action": "deny",
#                     "description": "this is test route",
#                     "match": {
#                         "ip": {
#                             "next_hop": {
#                                 "prefix_lists": [
#                                     "test_2_new",
#                                     "test_1_new"
#                                 ]
#                             },
#                             "route_source": {
#                                 "acls": [
#                                     "10"
#                                 ]
#                             }
#                         },
#                         "local_preference": {
#                             "value": [
#                                 "100",
#                                 "50"
#                             ]
#                         },
#                         "mpls_label": true,
#                         "security_group": {
#                             "source": [
#                                 10,
#                                 20
#                             ]
#                         }
#                     },
#                     "sequence": 10
#                 },
#                 {
#                     "action": "deny",
#                     "continue_entry": {
#                         "entry_sequence": 100
#                     },
#                     "match": {
#                         "additional_paths": {
#                             "all": true,
#                             "group_best": true
#                         },
#                         "as_path": {
#                             "acls": [
#                                 200,
#                                 100
#                             ]
#                         },
#                         "ipv6": {
#                             "address": {
#                                 "acl": "test_acl_20"
#                             }
#                         },
#                         "route_type": {
#                             "external": {
#                                 "set": true
#                             },
#                             "level_1": true,
#                             "nssa_external": {
#                                 "set": true
#                             }
#                         },
#                         "tag": {
#                             "tag_list": [
#                                 "test_match_tag"
#                             ]
#                         },
#                         "track": 105
#                     },
#                     "sequence": 20
#                 }
#             ],
#             "route_map": "test_1"
#         },
#         {
#             "entries": [
#                 {
#                     "action": "deny",
#                     "match": {
#                         "ipv6": {
#                             "address": {
#                                 "acl": "test_ip_acl"
#                             },
#                             "next_hop": {
#                                 "prefix_list": "test_new"
#                             },
#                             "route_source": {
#                                 "acl": "route_src_acl"
#                             }
#                         },
#                         "local_preference": {
#                             "value": [
#                                 "55",
#                                 "105"
#                             ]
#                         },
#                         "mpls_label": true,
#                         "security_group": {
#                             "source": [
#                                 10,
#                                 20
#                             ]
#                         }
#                     },
#                     "sequence": 10,
#                     "set": {
#                         "aigp_metric": {
#                             "value": 100
#                         },
#                         "automatic_tag": true,
#                         "extcommunity": {
#                             "cost": {
#                                 "cost_value": 100,
#                                 "id": "10",
#                                 "pre_bestpath": true
#                             }
#                         },
#                         "ip": {
#                             "address": "192.0.2.1",
#                             "df": 1,
#                             "next_hop": {
#                                 "recursive": {
#                                     "address": "198.51.110.1",
#                                     "global_route": true
#                                 },
#                                 "verify_availability": {
#                                     "address": "198.51.111.1",
#                                     "sequence": 100,
#                                     "track": 10
#                                 }
#                             },
#                             "precedence": {
#                                 "critical": true
#                             }
#                         }
#                     }
#                 }
#             ],
#             "route_map": "test_2"
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
  sample: ['route-map test_1 deny 10', 'description this is test route', 'match ip route-source 10', 'match track  105']
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.route_maps.route_maps import (
    Route_mapsArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.route_maps.route_maps import (
    Route_maps,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Route_mapsArgs.argument_spec,
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

    result = Route_maps(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
