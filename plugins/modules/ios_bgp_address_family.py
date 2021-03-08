#!/usr/bin/python
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#
"""
The module file for ios_bgp_address_family
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = """
module: ios_bgp_address_family
short_description: BGP Address family resource module
description: This module configures and manages the attributes of bgp address family on Cisco IOS.
version_added: 1.2.0
author: Sumit Jaiswal (@justjais)
notes:
- Tested against Cisco IOSv Version 15.2 on VIRL
options:
  config:
    description: A list of configurations for bgp address family.
    type: dict
    suboptions:
      as_number:
        description: Autonomous system number.
        type: str
      address_family:
        description: A list of configurations for bgp address family.
        type: list
        elements: dict
        suboptions:
          afi:
            description: Address Family
            type: str
            choices: ['ipv4', 'ipv6', 'l2vpn', 'nsap', 'rtfilter', 'vpnv4', 'vpnv6']
          safi:
            description: Address Family modifier
            type: str
            choices: ['flowspec', 'mdt', 'multicast', 'mvpn', 'evpn', 'unicast']
          vrf:
            description: Specify parameters for a VPN Routing/Forwarding instance
            type: str
          aggregate_address:
            description: Configure BGP aggregate entries
            type: list
            elements: dict
            suboptions:
              address:
                description: Aggregate address(A.B.C.D)
                type: str
              netmask:
                description: Aggregate mask(A.B.C.D)
                type: str
              advertise_map:
                description: Set condition to advertise attribute
                type: str
              as_confed_set:
                description: Generate AS confed set path information
                type: bool
              as_set:
                description: Generate AS set path information
                type: bool
              attribute_map:
                description: Set attributes of aggregate
                type: str
              summary_only:
                description: Filter more specific routes from updates
                type: bool
              suppress_map:
                description: Conditionally filter more specific routes from updates
                type: str
          auto_summary:
            description: Enable automatic network number summarization
            type: bool
          bgp:
            description: Configure BGP aggregate entries
            type: dict
            suboptions:
              additional_paths:
                description: Additional paths in the BGP table
                type: dict
                suboptions:
                  receive:
                    description: Receive additional paths from neighbors
                    type: bool
                  select:
                    description: Selection criteria to pick the paths
                    type: dict
                    suboptions:
                      all:
                        description: Select all available paths
                        type: bool
                      best:
                        description: Select best N paths (2-3).
                        type: int
                      group_best:
                        description: Select group-best path
                        type: bool
                  send:
                    description: Send additional paths to neighbors
                    type: bool
              aggregate_timer:
                description:
                  - Configure Aggregation Timer
                  - Please refer vendor documentation for valid values
                type: int
              dampening:
                description: Enable route-flap dampening
                type: dict
                suboptions:
                  penalty_half_time:
                    description:
                      - Half-life time for the penalty
                      - Please refer vendor documentation for valid values
                    type: int
                  reuse_route_val:
                    description:
                      - Value to start reusing a route
                      - Please refer vendor documentation for valid values
                    type: int
                  suppress_route_val:
                    description:
                      - Value to start suppressing a route
                      - Please refer vendor documentation for valid values
                    type: int
                  max_suppress:
                    description:
                      - Maximum duration to suppress a stable route
                      - Please refer vendor documentation for valid values
                    type: int
                  route_map:
                    description: Route-map to specify criteria for dampening
                    type: str
              dmzlink_bw:
                description: Use DMZ Link Bandwidth as weight for BGP multipaths
                type: bool
              nexthop:
                description: Nexthop tracking commands
                type: dict
                suboptions:
                  route_map:
                    description: Route map for valid nexthops
                    type: str
                  trigger:
                    description: Nexthop triggering
                    type: dict
                    suboptions:
                      delay:
                        description:
                          - Set the delay to tigger nexthop tracking
                          - Please refer vendor documentation for valid values
                        type: int
                      enable:
                        description: Enable nexthop tracking
                        type: bool
              redistribute_internal:
                description: Allow redistribution of iBGP into IGPs (dangerous)
                type: bool
              route_map:
                description:
                  - route-map control commands
                  - Have route-map set commands take priority over BGP commands such as next-hop unchanged
                type: bool
              scan_time:
                description:
                  - Configure background scanner interval
                  - Please refer vendor documentation for valid values
                type: int
              slow_peer:
                description: Nexthop triggering
                type: list
                elements: dict
                suboptions:
                  detection:
                    description: Slow-peer detection
                    type: dict
                    suboptions:
                      enable:
                        description: Enable slow-peer detection
                        type: bool
                      threshold:
                        description:
                          - Set the slow-peer detection threshold
                          - Threshold value (seconds)
                          - Please refer vendor documentation for valid values
                        type: int
                  split_update_group:
                    description: Configure slow-peer split-update-group
                    type: dict
                    suboptions:
                      dynamic:
                        description: Dynamically split the slow peer to slow-update group
                        type: bool
                      permanent:
                        description: Keep the slow-peer permanently in slow-update group
                        type: bool
              soft_reconfig_backup:
                description: Use soft-reconfiguration inbound only when route-refresh is not negotiated
                type: bool
              update_group:
                description:
                  - Manage peers in bgp update groups
                  - Split update groups based on Policy
                  - Keep peers with as-override in different update groups
                type: bool
          default:
            description: Set a command to its defaults
            type: bool
          default_information:
            description:
              - Distribution of default information
              - Distribute default route
            type: bool
          default_metric:
            description: Set metric of redistributed routes
            type: int
          distance:
            description: Define an administrative distance
            type: dict
            suboptions:
              external:
                description: Distance for routes external to the AS
                type: int
              internal:
                description: Distance for routes internal to the AS
                type: int
              local:
                description: Distance for local routes
                type: int
          neighbor:
            description: Specify a neighbor router
            type: list
            elements: dict
            suboptions:
              address:
                description: Neighbor address (A.B.C.D)
                type: str
              tag:
                description: Neighbor tag
                type: str
              ipv6_adddress:
                description: Neighbor ipv6 address (X:X:X:X::X)
                type: str
              activate:
                description: Enable the Address Family for this Neighbor
                type: bool
              additional_paths:
                description: Negotiate additional paths capabilities with this neighbor
                type: dict
                suboptions:
                  disable:
                    description: Disable additional paths for this neighbor
                    type: bool
                  receive:
                    description: Receive additional paths from neighbors
                    type: bool
                  send:
                    description: Send additional paths to this neighbor
                    type: bool
              advertise:
                description:
                  - Advertise to this neighbor
                  - Advertise additional paths
                type: dict
                suboptions:
                  all:
                    description: Select all available paths
                    type: bool
                  best:
                    description: Select best N paths (2-3).
                    type: int
                  group_best:
                    description: Select group-best path
                    type: bool
              advertise_map:
                description: specify route-map for conditional advertisement
                type: dict
                suboptions:
                  name:
                    description: advertise route-map name
                    type: str
                  exist_map:
                    description:
                      - advertise prefix only if prefix is in the condition exists
                      - condition route-map name
                    type: str
                  non_exist_map:
                    description:
                      - advertise prefix only if prefix in the condition does not exist
                      - condition route-map name
                    type: str
              advertisement_interval:
                description: Minimum interval between sending BGP routing updates
                type: int
              aigp:
                description: Enable a AIGP on neighbor
                type: dict
                suboptions:
                  enable:
                    description: Enable a AIGP on neighbor
                    type: str
                  send:
                    description: Cost community or MED carrying AIGP VALUE
                    type: dict
                    suboptions:
                      cost_community:
                        description: Cost extended community carrying AIGP Value
                        type: dict
                        suboptions:
                          id:
                            description:
                              - Community ID
                              - Please refer vendor documentation for valid values
                            type: int
                          poi:
                            description: Point of Insertion
                            type: dict
                            suboptions:
                              igp_cost:
                                description:  Point of Insertion After IGP
                                type: bool
                              pre_bestpath:
                                description: Point of Insertion At Beginning
                                type: bool
                              transitive:
                                description: Cost community is Transitive
                                type: bool
                      med:
                        description: Med carrying AIGP Value
                        type: bool
              allow_policy:
                description: Enable the policy support for this IBGP Neighbor
                type: bool
              allowas_in:
                description:
                  - Accept as-path with my AS present in it
                  - Please refer vendor documentation for valid values
                type: int
              as_override:
                description: Override matching AS-number while sending update
                type: dict
                suboptions:
                  set:
                    description: Enable AS override
                    type: bool
                  split_horizon:
                    description: Maintain Split Horizon while sending update
                    type: bool
              bmp_activate:
                description: Activate the BMP monitoring for a BGP peer
                type: dict
                suboptions:
                  all:
                    description: Activate BMP monitoring for all servers
                    type: bool
                  server:
                    description:
                      - Activate BMP for server
                      - BMP Server Number
                      - Please refer vendor documentation for valid values
                    type: int
              capability:
                description:
                  - Advertise capability to the peer
                  - Advertise ORF capability to the peer
                  - Advertise prefixlist ORF capability to this neighbor
                type: dict
                suboptions:
                  both:
                    description: Capability to SEND and RECEIVE the ORF to/from this neighbor
                    type: bool
                  receive:
                    description: Capability to RECEIVE the ORF from this neighbor
                    type: bool
                  send:
                    description: Capability to SEND the ORF to this neighbor
                    type: bool
              cluster_id:
                description:
                  - Configure Route-Reflector Cluster-id (peers may reset)
                  - Route-Reflector Cluster-id as 32 bit quantity, or
                    Route-Reflector Cluster-id in IP address format (A.B.C.D)
                type: str
              default_originate:
                description: Originate default route to this neighbor
                type: dict
                suboptions:
                  set:
                    description: Set default route to this neighbor
                    type: bool
                  route_map:
                    description: Route-map to specify criteria to originate default
                    type: str
              description:
                description: Neighbor specific description
                type: str
              disable_connected_check:
                description: one-hop away EBGP peer using loopback address
                type: bool
              distribute_list:
                description: Filter updates to/from this neighbor
                type: dict
                suboptions:
                  acl:
                    description: ACL id/name
                    type: str
                  in:
                    description: Filter incoming updates
                    type: bool
                  out:
                    description: Filter outgoing updates
                    type: bool
              dmzlink_bw:
                description: Propagate the DMZ link bandwidth
                type: bool
              ebgp_multihop:
                description: Allow EBGP neighbors not on directly connected networks
                type: dict
                suboptions:
                  enable:
                    description: Allow EBGP neighbors not on directly connected networks
                    type: bool
                  hop_count:
                    description:
                      - Maximum hop count
                      - Please refer vendor documentation for valid values
                    type: int
              fall_over:
                description: Session fall on peer route lost
                type: dict
                suboptions:
                  bfd:
                    description: Use BFD to detect failure
                    type: dict
                    suboptions:
                      set:
                        description: set bfd
                        type: bool
                      multi_hop:
                        description: Force BFD multi-hop to detect failure
                        type: bool
                      single_hop:
                        description: Force BFD single-hop to detect failure
                        type: bool
                  route_map:
                    description: Route map for peer route
                    type: str
              filter_list:
                description: Establish BGP filters
                type: dict
                suboptions:
                  as_path_acl:
                    description:
                      - AS path access list
                      - Please refer vendor documentation for valid values
                    type: int
                  in:
                    description: Filter incoming updates
                    type: bool
                  out:
                    description: Filter outgoing updates
                    type: bool
              ha_mode:
                description: high availability mode
                type: dict
                suboptions:
                  set:
                    description: set ha-mode and graceful-restart for this peer
                    type: bool
                  disable:
                    description: disable graceful-restart
                    type: bool
              inherit:
                description:
                  - Inherit a template
                  - Inherit a peer-policy template
                type: str
              internal_vpn_client:
                description: Stack iBGP-CE Neighbor Path in ATTR_SET for vpn update
                type: bool
              local_as:
                description: Specify a local-as number
                type: dict
                suboptions:
                  set:
                    description: set local-as number
                    type: bool
                  number:
                    description:
                      - AS number used as local AS
                      - Please refer vendor documentation for valid values
                    type: int
                  dual_as:
                    description: Accept either real AS or local AS from the ebgp peer
                    type: bool
                  no_prepend:
                    description: Do not prepend local-as to updates from ebgp peers
                    type: dict
                    suboptions:
                      set:
                        description: Set prepend
                        type: bool
                      replace_as:
                        description: Replace real AS with local AS in the EBGP updates
                        type: bool
              log_neighbor_changes:
                description: Log neighbor up/down and reset reason
                type: dict
                suboptions:
                  set:
                    description: set Log neighbor up/down and reset
                    type: bool
                  disable:
                    description: disable Log neighbor up/down and reset
                    type: bool
              maximum_prefix:
                description: Establish BGP filters
                type: dict
                suboptions:
                  number:
                    description:
                      - maximum no. of prefix limit
                      - Please refer vendor documentation for valid values
                    type: int
                  threshold_value:
                    description:
                      - Threshold value (%) at which to generate a warning msg
                      - Please refer vendor documentation for valid values
                    type: int
                  restart:
                    description: Restart bgp connection after limit is exceeded
                    type: int
                  warning_only:
                    description: Only give warning message when limit is exceeded
                    type: bool
              next_hop_self:
                description: Disable the next hop calculation for this neighbor
                type: bool
              next_hop_unchanged:
                description: Propagate next hop unchanged for iBGP paths to this neighbor
                type: bool
              password:
                description: Set a password
                type: str
              path_attribute:
                description: BGP optional attribute filtering
                type: dict
                suboptions:
                  discard:
                    description: Discard matching path-attribute for this neighbor
                    type: dict
                    suboptions:
                      type:
                        description:
                          - path attribute type
                          - Please refer vendor documentation for valid values
                        type: int
                      range:
                        description: path attribute range
                        type: dict
                        suboptions:
                          start:
                            description:
                              - path attribute range start value
                              - Please refer vendor documentation for valid values
                            type: int
                          end:
                            description:
                              - path attribute range end value
                              - Please refer vendor documentation for valid values
                            type: int
                      in:
                        description: Perform inbound path-attribute filtering
                        type: bool
                  treat_as_withdraw:
                    description: Treat-as-withdraw matching path-attribute for this neighbor
                    type: dict
                    suboptions:
                      type:
                        description:
                          - path attribute type
                          - Please refer vendor documentation for valid values
                        type: int
                      range:
                        description: path attribute range
                        type: dict
                        suboptions:
                          start:
                            description:
                              - path attribute range start value
                              - Please refer vendor documentation for valid values
                            type: int
                          end:
                            description:
                              - path attribute range end value
                              - Please refer vendor documentation for valid values
                            type: int
                      in:
                        description: Perform inbound path-attribute filtering
                        type: bool
              peer_group:
                description: Member of the peer-group
                type: bool
              prefix_list:
                description: Filter updates to/from this neighbor
                type: list
                elements: dict
                suboptions:
                  name:
                    description: Name of a prefix list
                    type: str
                  in:
                    description: Filter incoming updates
                    type: bool
                  out:
                    description: Filter outgoing updates
                    type: bool
              remote_as:
                description:
                  - Specify a BGP neighbor
                  - AS of remote neighbor
                type: int
              remove_private_as:
                description: Remove private AS number from outbound updates
                type: dict
                suboptions:
                  set:
                    description: Remove private AS number from outbound updates
                    type: bool
                  all:
                    description: Remove all private AS numbers
                    type: bool
                  replace_as:
                    description: Replace all private AS numbers with local AS
                    type: bool
              route_map:
                description: Apply route map to neighbor
                type: list
                elements: dict
                suboptions:
                  name:
                    description: Name of route map
                    type: str
                  in:
                    description: Apply map to incoming routes
                    type: bool
                  out:
                    description: Apply map to outbound routes
                    type: bool
              route_reflector_client:
                description: Configure a neighbor as Route Reflector client
                type: bool
              route_server_client:
                description: Configure a neighbor as Route Server client
                type: bool
              send_community:
                description: Send Community attribute to this neighbor
                type: dict
                suboptions:
                  both:
                    description: Send Standard and Extended Community attributes
                    type: bool
                  extended:
                    description: Send Extended Community attribute
                    type: bool
                  standard:
                    description: Send Standard Community attribute
                    type: bool
              shutdown:
                description: Administratively shut down this neighbor
                type: dict
                suboptions:
                  set:
                    description: shut down
                    type: bool
                  graceful:
                    description:
                      - Gracefully shut down this neighbor
                      - time in seconds
                      - Please refer vendor documentation for valid values
                    type: int
              slow_peer:
                description: Configure slow-peer
                type: list
                elements: dict
                suboptions:
                  detection:
                    description: Configure slow-peer
                    type: dict
                    suboptions:
                      enable:
                        description: Enable slow-peer detection
                        type: bool
                      disable:
                        description: Disable slow-peer detection
                        type: bool
                      threshold:
                        description: Set the slow-peer detection threshold
                        type: int
                  split_update_group:
                    description: Configure slow-peer
                    type: dict
                    suboptions:
                      dynamic:
                        description: Configure slow-peer
                        type: dict
                        suboptions:
                          enable:
                            description: Configure slow-peer
                            type: bool
                          disable:
                            description: Configure slow-peer
                            type: bool
                          permanent:
                            description: Configure slow-peer
                            type: bool
                      static:
                        description: Configure slow-peer
                        type: bool
              soft_reconfiguration:
                description:
                  - Per neighbor soft reconfiguration
                  - Allow inbound soft reconfiguration for this neighbor
                type: bool
              soo:
                description: Site-of-Origin extended community
                type: str
              timers:
                description: BGP per neighbor timers
                type: dict
                suboptions:
                  interval:
                    description: Keepalive interval
                    type: int
                  holdtime:
                    description: Holdtime
                    type: int
                  min_holdtime:
                    description: Minimum hold time from neighbor
                    type: int
              transport:
                description: Transport options
                type: dict
                suboptions:
                  connection_mode:
                    description: Specify passive or active connection
                    type: dict
                    suboptions:
                      active:
                        description: Actively establish the TCP session
                        type: bool
                      passive:
                        description: Passively establish the TCP session
                        type: bool
                  multi_session:
                    description: Use Multi-session for transport
                    type: bool
                  path_mtu_discovery:
                    description: Use transport path MTU discovery
                    type: dict
                    suboptions:
                      set:
                        description: Use path MTU discovery
                        type: bool
                      disable:
                        description: disable
                        type: bool
              ttl_security:
                description:
                  - BGP ttl security check
                  - maximum number of hops
                  - Please refer vendor documentation for valid values
                type: int
              unsuppress_map:
                description: Route-map to selectively unsuppress suppressed routes
                type: str
              version:
                description:
                  - Set the BGP version to match a neighbor
                  - Neighbor's BGP version
                  - Please refer vendor documentation for valid values
                type: int
              weight:
                description: Set default weight for routes from this neighbor
                type: int
          network:
            description: Specify a network to announce via BGP
            type: list
            elements: dict
            suboptions:
              address:
                description: Network number (A.B.C.D)
                type: str
              mask:
                description: Network mask (A.B.C.D)
                type: str
              backdoor:
                description: Specify a BGP backdoor route
                type: bool
              route_map:
                description: Route-map to modify the attributes
                type: str
          redistribute:
            description: Redistribute information from another routing protocol
            type: list
            elements: dict
            suboptions:
              application:
                description: Application
                type: dict
                suboptions:
                  name:
                    description: Application name
                    type: str
                  metric:
                    description: Metric for redistributed routes
                    type: int
                  route_map:
                    description: Route map reference
                    type: str
              bgp:
                description: Border Gateway Protocol (BGP)
                type: dict
                suboptions:
                  as_number:
                    description: Autonomous system number
                    type: str
                  metric:
                    description: Metric for redistributed routes
                    type: int
                  route_map:
                    description: Route map reference
                    type: str
              connected:
                description: Connected
                type: dict
                suboptions:
                  metric:
                    description: Metric for redistributed routes
                    type: int
                  route_map:
                    description: Route map reference
                    type: str
              eigrp:
                description: Enhanced Interior Gateway Routing Protocol (EIGRP)
                type: dict
                suboptions:
                  as_number:
                    description: Autonomous system number
                    type: str
                  metric:
                    description: Metric for redistributed routes
                    type: int
                  route_map:
                    description: Route map reference
                    type: str
              isis:
                description: ISO IS-IS
                type: dict
                suboptions:
                  area_tag:
                    description: ISO routing area tag
                    type: str
                  clns:
                    description: Redistribution of OSI dynamic routes
                    type: bool
                  ip:
                    description: Redistribution of IP dynamic routes
                    type: bool
                  metric:
                    description: Metric for redistributed routes
                    type: int
                  route_map:
                    description: Route map reference
                    type: str
              iso_igrp:
                description: IGRP for OSI networks
                type: dict
                suboptions:
                  area_tag:
                    description: ISO routing area tag
                    type: str
                  route_map:
                    description: Route map reference
                    type: str
              lisp:
                description: Locator ID Separation Protocol (LISP)
                type: dict
                suboptions:
                  metric:
                    description: Metric for redistributed routes
                    type: int
                  route_map:
                    description: Route map reference
                    type: str
              mobile:
                description: Mobile routes
                type: dict
                suboptions:
                  metric:
                    description: Metric for redistributed routes
                    type: int
                  route_map:
                    description: Route map reference
                    type: str
              odr:
                description: On Demand stub Routes
                type: dict
                suboptions:
                  metric:
                    description: Metric for redistributed routes
                    type: int
                  route_map:
                    description: Route map reference
                    type: str
              ospf:
                description: Open Shortest Path First (OSPF)
                type: dict
                suboptions:
                  process_id:
                    description: Process ID
                    type: int
                  match:
                    description: On Demand stub Routes
                    type: dict
                    suboptions:
                      external:
                        description: Redistribute OSPF external routes
                        type: bool
                      internal:
                        description: Redistribute OSPF internal routes
                        type: bool
                      nssa_external:
                        description: Redistribute OSPF NSSA external routes
                        type: bool
                      type_1:
                        description: Redistribute NSSA external type 1 routes
                        type: bool
                      type_2:
                        description: Redistribute NSSA external type 2 routes
                        type: bool
                  metric:
                    description: Metric for redistributed routes
                    type: int
                  route_map:
                    description: Route map reference
                    type: str
                  vrf:
                    description: VPN Routing/Forwarding Instance
                    type: str
              ospfv3:
                description: OSPFv3
                type: dict
                suboptions:
                  process_id:
                    description: Process ID
                    type: int
                  match:
                    description: On Demand stub Routes
                    type: dict
                    suboptions:
                      external:
                        description: Redistribute OSPF external routes
                        type: bool
                      internal:
                        description: Redistribute OSPF internal routes
                        type: bool
                      nssa_external:
                        description: Redistribute OSPF NSSA external routes
                        type: bool
                      type_1:
                        description: Redistribute NSSA external type 1 routes
                        type: bool
                      type_2:
                        description: Redistribute NSSA external type 2 routes
                        type: bool
                  metric:
                    description: Metric for redistributed routes
                    type: int
                  route_map:
                    description: Route map reference
                    type: str
              rip:
                description: Routing Information Protocol (RIP)
                type: dict
                suboptions:
                  metric:
                    description: Metric for redistributed routes
                    type: int
                  route_map:
                    description: Route map reference
                    type: str
              static:
                description: Static routes
                type: dict
                suboptions:
                  clns:
                    description: Redistribution of OSI static routes
                    type: bool
                  ip:
                    description: Redistribution of IP static routes
                    type: bool
                  metric:
                    description: Metric for redistributed routes
                    type: int
                  route_map:
                    description: Route map reference
                    type: str
              vrf:
                description: Specify a source VRF
                type: dict
                suboptions:
                  name:
                    description: Source VRF name
                    type: str
                  global:
                    description: global VRF
                    type: bool
          snmp:
            description: Modify snmp parameters
            type: dict
            suboptions:
              context:
                description:
                  - Configure a SNMP context
                  - Context Name
                type: dict
                suboptions:
                  name:
                    description: Context Name
                    type: str
                  community:
                    description: Configure a SNMP v2c Community string and access privs
                    type: dict
                    suboptions:
                      snmp_community:
                        description: SNMP community string
                        type: str
                      acl:
                        description:
                          - Standard IP accesslist allowing access with this community string
                          - Expanded IP accesslist allowing access with this community string
                          - Access-list name
                        type: str
                      ipv6:
                        description:
                          - Specify IPv6 Named Access-List
                          - IPv6 Access-list name
                        type: str
                      ro:
                        description: Read-only access with this community string
                        type: bool
                      rw:
                        description: Read-write access with this community string
                        type: bool
                  user:
                    description: Configure a SNMP v3 user
                    type: dict
                    suboptions:
                      name:
                        description: SNMP community string
                        type: str
                      access:
                        description: specify an access-list associated with this group
                        type: dict
                        suboptions:
                          acl:
                            description: SNMP community string
                            type: str
                          ipv6:
                            description:
                              - Specify IPv6 Named Access-List
                              - IPv6 Access-list name
                            type: str
                      auth:
                        description: authentication parameters for the user
                        type: dict
                        suboptions:
                          md5:
                            description:
                              - Use HMAC MD5 algorithm for authentication
                              - authentication password for user
                            type: str
                          sha:
                            description:
                              - Use HMAC SHA algorithm for authentication
                              - authentication password for user
                            type: str
                      priv:
                        description: encryption parameters for the user
                        type: dict
                        suboptions:
                          des:
                            description: Use 56 bit DES algorithm for encryption
                            type: str
                      credential:
                        description: If the user password is already configured and saved
                        type: bool
                      encrypted:
                        description: specifying passwords as MD5 or SHA digests
                        type: bool
          table_map:
            description: Map external entry attributes into routing table
            type: dict
            suboptions:
              name:
                description: route-map name
                type: str
              filter:
                description: Selective route download
                type: bool
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the IOS
        device by executing the command B(sh running-config | section ^router bgp).
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
    - rendered
    - parsed
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
        option should be the same format as the output of command I(show running-config
        | include ip route|ipv6 route) executed on device. For state I(parsed) active
        connection to remote host is not required.
    type: str
"""

EXAMPLES = """

# Using merged

# Before state:
# -------------
#
# vios#sh running-config | section ^router bgp
# router bgp 65000
#  bgp log-neighbor-changes
#  bgp nopeerup-delay cold-boot 20

- name: Merge provided configuration with device configuration
  cisco.ios.ios_bgp_address_family:
    config:
      as_number: 65000
      address_family:
        - afi: ipv4
          safi: multicast
          vrf: blue
          aggregate_address:
            - address: 192.0.2.1
              netmask: 255.255.255.255
              as_confed_set: true
          bgp:
            aggregate_timer: 10
            dampening:
              penalty_half_time: 1
              reuse_route_val: 1
              suppress_route_val: 1
              max_suppress: 1
            slow_peer:
              - detection:
                  threshold: 150
          neighbor:
            - address: 198.51.100.1
              aigp:
                send:
                  cost_community:
                    id: 100
                    poi:
                      igp_cost: true
                      transitive: true
              slow_peer:
                - detection:
                    threshold: 150
              remote_as: 10
              route_map:
                name: test-route
                out: true
              route_server_client: true
          network:
            - address: 198.51.110.10
              mask: 255.255.255.255
              backdoor: true
          snmp:
            context:
              name: snmp_con
              community:
                snmp_community: community
                ro: true
                acl: 10
        - afi: ipv4
          safi: mdt
          bgp:
            dmzlink_bw: true
            dampening:
              penalty_half_time: 1
              reuse_route_val: 10
              suppress_route_val: 100
              max_suppress: 5
            soft_reconfig_backup: true
        - afi: ipv4
          safi: multicast
          aggregate_address:
            - address: 192.0.3.1
              netmask: 255.255.255.255
              as_confed_set: true
          default_metric: 12
          distance:
            external: 10
            internal: 10
            local: 100
          network:
            - address: 198.51.111.11
              mask: 255.255.255.255
              route_map: test
          table_map:
            name: test_tableMap
            filter: true
    state: merged

# Commands fired:
# ---------------
# "commands": [
#     "router bgp 65000",
#     "address-family ipv4 multicast vrf blue",
#     "bgp aggregate-timer 10",
#     "bgp slow-peer detection threshold 150",
#     "bgp dampening 1 1 1 1",
#     "neighbor 198.51.100.1 remote-as 10",
#     "neighbor 198.51.100.1 aigp send cost-community 100 poi igp-cost transitive",
#     "neighbor 198.51.100.1 route-map test-route out",
#     "neighbor 198.51.100.1 route-server-client",
#     "neighbor 198.51.100.1 slow-peer detection threshold 150",
#     "network 198.51.110.10 mask 255.255.255.255 backdoor",
#     "snmp context snnmp_con_1 community community ro 10",
#     "aggregate-address 192.0.2.1 255.255.255.255 as-confed-set",
#     "exit-address-family",
#     "address-family ipv4 mdt",
#     "bgp dmzlink-bw",
#     "bgp dampening 1 10 100 5",
#     "bgp soft-reconfig-backup",
#     "exit-address-family",
#     "address-family ipv4 multicast",
#     "network 1.1.1.1 mask 255.255.255.255 route-map test",
#     "aggregate-address 192.0.3.1 255.255.255.255 as-confed-set",
#     "default-metric 12",
#     "distance bgp 10 10 100",
#     "table-map test_tableMap filter"
#     "exit-address-family",
# ]

# After state:
# ------------
#
# vios#sh running-config | section ^router bgp
# router bgp 65000
#  bgp log-neighbor-changes
#  bgp nopeerup-delay cold-boot 20
#  !
#  address-family ipv4 multicast
#   table-map test_tableMap filter
#   network 1.1.1.1 mask 255.255.255.255 route-map test
#   aggregate-address 192.0.3.1 255.255.255.255 as-confed-set
#   default-metric 12
#   distance bgp 10 10 100
#  exit-address-family
#  !
#  address-family ipv4 mdt
#   bgp dampening 1 10 100 5
#   bgp dmzlink-bw
#   bgp soft-reconfig-backup
#  exit-address-family
#  !
#  address-family ipv4 multicast vrf blue
#   bgp aggregate-timer 10
#   bgp slow-peer detection threshold 150
#   bgp dampening 1 1 1 1
#   network 198.51.110.10 mask 255.255.255.255 backdoor
#   aggregate-address 192.0.2.1 255.255.255.255 as-confed-set
#   neighbor 198.51.100.1 remote-as 10
#   neighbor 198.51.100.1 activate
#   neighbor 198.51.100.1 aigp send cost-community 100 poi igp-cost transitive
#   neighbor 198.51.100.1 route-server-client
#   neighbor 198.51.100.1 slow-peer detection threshold 150
#   neighbor 198.51.100.1 route-map test-route out
#  exit-address-family

# Using replaced

# Before state:
# -------------
#
# vios#sh running-config | section ^router bgp
# router bgp 65000
#  bgp log-neighbor-changes
#  bgp nopeerup-delay cold-boot 20
#  !
#  address-family ipv4 multicast
#   table-map test_tableMap filter
#   network 1.1.1.1 mask 255.255.255.255 route-map test
#   aggregate-address 192.0.3.1 255.255.255.255 as-confed-set
#   default-metric 12
#   distance bgp 10 10 100
#  exit-address-family
#  !
#  address-family ipv4 mdt
#   bgp dampening 1 10 100 5
#   bgp dmzlink-bw
#   bgp soft-reconfig-backup
#  exit-address-family
#  !
#  address-family ipv4 multicast vrf blue
#   bgp aggregate-timer 10
#   bgp slow-peer detection threshold 150
#   bgp dampening 1 1 1 1
#   network 198.51.110.10 mask 255.255.255.255 backdoor
#   aggregate-address 192.0.2.1 255.255.255.255 as-confed-set
#   neighbor 198.51.100.1 remote-as 10
#   neighbor 198.51.100.1 activate
#   neighbor 198.51.100.1 aigp send cost-community 100 poi igp-cost transitive
#   neighbor 198.51.100.1 route-server-client
#   neighbor 198.51.100.1 slow-peer detection threshold 150
#   neighbor 198.51.100.1 route-map test-route out
#  exit-address-family

- name: Replaces device configuration of listed AF BGP with provided configuration
  cisco.ios.ios_bgp_address_family:
    config:
      as_number: 65000
      address_family:
        - afi: ipv4
          safi: multicast
          vrf: blue
          aggregate_address:
            - address: 192.0.2.1
              netmask: 255.255.255.255
              as_confed_set: true
          bgp:
            aggregate_timer: 10
            dampening:
              penalty_half_time: 1
              reuse_route_val: 1
              suppress_route_val: 1
              max_suppress: 1
            slow_peer:
              - detection:
                  threshold: 150
          neighbor:
            - address: 198.51.110.1
              activate: true
              aigp:
                send:
                  cost_community:
                    id: 200
                    poi:
                      igp_cost: true
                      transitive: true
              slow_peer:
                - detection:
                    threshold: 150
              remote_as: 10
              route_map:
                name: test-replaced-route
                out: true
              route_server_client: true
          network:
            - address: 198.51.110.10
              mask: 255.255.255.255
              backdoor: true
        - afi: ipv4
          safi: multicast
          bgp:
            aggregate_timer: 10
            dampening:
              penalty_half_time: 10
              reuse_route_val: 10
              suppress_route_val: 10
              max_suppress: 10
            slow_peer:
              - detection:
                  threshold: 200
          network:
            - address: 192.0.2.1
              mask: 255.255.255.255
              route_map: test
    state: replaced

# Commands fired:
# ---------------
# "commands": [
#         "router bgp 65000",
#         "address-family ipv4 multicast vrf blue",
#         "neighbor 198.51.110.1 remote-as 10",
#         "neighbor 198.51.110.1 activate",
#         "neighbor 198.51.110.1 aigp send cost-community 200 poi igp-cost transitive",
#         "neighbor 198.51.110.1 route-map test-replaced-route out",
#         "neighbor 198.51.110.1 route-server-client",
#         "neighbor 198.51.110.1 slow-peer detection threshold 150",
#         "no neighbor 198.51.100.1 remote-as 10",
#         "no neighbor 198.51.100.1 activate",
#         "no neighbor 198.51.100.1 aigp send cost-community 100 poi igp-cost transitive",
#         "no neighbor 198.51.100.1 route-map test-route out",
#         "no neighbor 198.51.100.1 route-server-client",
#         "no neighbor 198.51.100.1 slow-peer detection threshold 150",
#         "exit-address-family",
#         "address-family ipv4 multicast",
#         "bgp aggregate-timer 10",
#         "bgp slow-peer detection threshold 200",
#         "bgp dampening 10 10 10 10",
#         "network 192.0.2.1 mask 255.255.255.255 route-map test",
#         "no network 1.1.1.1 mask 255.255.255.255 route-map test",
#         "no aggregate-address 192.0.3.1 255.255.255.255 as-confed-set",
#         "no default-metric 12",
#         "no distance bgp 10 10 100",
#         "no table-map test_tableMap filter"
#         "exit-address-family",
#     ]

# After state:
# -------------
#
# vios#sh running-config | section ^router bgp
# router bgp 65000
#  bgp log-neighbor-changes
#  bgp nopeerup-delay cold-boot 20
#  !
#  address-family ipv4 multicast
#   bgp aggregate-timer 10
#   bgp slow-peer detection threshold 200
#   bgp dampening 10 10 10 10
#   network 192.0.2.1 mask 255.255.255.255 route-map test
#  exit-address-family
#  !
#  address-family ipv4 mdt
#   bgp dampening 1 10 100 5
#   bgp dmzlink-bw
#   bgp soft-reconfig-backup
#  exit-address-family
#  !
#  address-family ipv4 multicast vrf blue
#   bgp aggregate-timer 10
#   bgp slow-peer detection threshold 150
#   bgp dampening 1 1 1 1
#   network 198.51.110.10 mask 255.255.255.255 backdoor
#   aggregate-address 192.0.2.1 255.255.255.255 as-confed-set
#   neighbor 198.51.110.1 remote-as 10
#   neighbor 198.51.110.1 activate
#   neighbor 198.51.110.1 aigp send cost-community 200 poi igp-cost transitive
#   neighbor 198.51.110.1 route-server-client
#   neighbor 198.51.110.1 slow-peer detection threshold 150
#   neighbor 198.51.110.1 route-map test-replaced-route out
#  exit-address-family

# Using overridden

# Before state:
# -------------
#
# vios#sh running-config | section ^router bgp
# router bgp 65000
#  bgp log-neighbor-changes
#  bgp nopeerup-delay cold-boot 20
#  !
#  address-family ipv4 multicast
#   table-map test_tableMap filter
#   network 1.1.1.1 mask 255.255.255.255 route-map test
#   aggregate-address 192.0.3.1 255.255.255.255 as-confed-set
#   default-metric 12
#   distance bgp 10 10 100
#  exit-address-family
#  !
#  address-family ipv4 mdt
#   bgp dampening 1 10 100 5
#   bgp dmzlink-bw
#   bgp soft-reconfig-backup
#  exit-address-family
#  !
#  address-family ipv4 multicast vrf blue
#   bgp aggregate-timer 10
#   bgp slow-peer detection threshold 150
#   bgp dampening 1 1 1 1
#   network 198.51.110.10 mask 255.255.255.255 backdoor
#   aggregate-address 192.0.2.1 255.255.255.255 as-confed-set
#   neighbor 198.51.100.1 remote-as 10
#   neighbor 198.51.100.1 activate
#   neighbor 198.51.100.1 aigp send cost-community 100 poi igp-cost transitive
#   neighbor 198.51.100.1 route-server-client
#   neighbor 198.51.100.1 slow-peer detection threshold 150
#   neighbor 198.51.100.1 route-map test-route out
#  exit-address-family

- name: Override device configuration of all AF BGP with provided configuration
  cisco.ios.ios_bgp_address_family:
    config:
      as_number: 65000
      address_family:
        - afi: ipv4
          safi: multicast
          vrf: blue
          aggregate_address:
            - address: 192.0.2.1
              netmask: 255.255.255.255
              as_confed_set: true
          bgp:
            aggregate_timer: 10
            dampening:
              penalty_half_time: 10
              reuse_route_val: 10
              suppress_route_val: 100
              max_suppress: 50
            slow_peer:
              - detection:
                  threshold: 150
          neighbor:
            - address: 198.51.110.1
              activate: true
              log_neighbor_changes:
                disable: true
              maximum_prefix:
                number: 1
                threshold_value: 10
                restart: 100
              slow_peer:
                - detection:
                    threshold: 150
              remote_as: 100
              route_map:
                name: test-override-route
                out: true
              route_server_client: true
              version: 4
          network:
            - address: 198.51.110.10
              mask: 255.255.255.255
              backdoor: true
        - afi: ipv6
          safi: multicast
          default_information: true
          bgp:
            aggregate_timer: 10
            dampening:
              penalty_half_time: 10
              reuse_route_val: 10
              suppress_route_val: 10
              max_suppress: 10
            slow_peer:
              - detection:
                  threshold: 200
          network:
            - address: 2001:DB8:0:3::/64
              route_map: test_ipv6
    state: overridden

# Commands fired:
# ---------------
# "commands": [
#       "router bgp 65000",
#       "no address-family ipv4 multicast",
#       "no address-family ipv4 mdt",
#       "address-family ipv4 multicast vrf blue",
#       "bgp aggregate-timer 10",
#       "bgp slow-peer detection threshold 150",
#       "bgp dampening 10 10 100 50",
#       "neighbor 198.51.110.1 remote-as 100",
#       "neighbor 198.51.110.1 activate",
#       "neighbor 198.51.110.1 log-neighbor-changes disable",
#       "neighbor 198.51.110.1 maximum-prefix 1 10 restart 100",
#       "neighbor 198.51.110.1 route-map test-override-route out",
#       "neighbor 198.51.110.1 route-server-client",
#       "neighbor 198.51.110.1 version 4",
#       "neighbor 198.51.110.1 slow-peer detection threshold 150",
#       "network 198.51.110.10 mask 255.255.255.255 backdoor",
#       "aggregate-address 192.0.2.1 255.255.255.255 as-confed-set",
#       "exit-address-family",
#       "address-family ipv6 multicast",
#       "bgp aggregate-timer 10",
#       "bgp slow-peer detection threshold 200",
#       "bgp dampening 10 10 10 10",
#       "network 2001:DB8:0:3::/64 route-map test_ipv6"
#       "exit-address-family",
#   ]

# After state:
# -------------
#
# vios#sh running-config | section ^router bgp
# router bgp 65000
#  bgp log-neighbor-changes
#  bgp nopeerup-delay cold-boot 20
#  bgp nopeerup-delay post-boot 10
#  bgp bestpath med confed
#  snmp context snnmp_con_1 community community RO 10
#  neighbor 192.0.2.1 remote-as 100
#  neighbor 192.0.2.1 description replace neighbor
#  neighbor 198.51.100.1 remote-as 10
#  !
#  address-family ipv6 multicast
#   bgp aggregate-timer 10
#   bgp slow-peer detection threshold 200
#   bgp dampening 10 10 10 10
#   network 2001:DB8:0:3::/64 route-map test_ipv6
#  exit-address-family
#  !
#  address-family ipv4 multicast vrf blue
#   bgp aggregate-timer 10
#   bgp slow-peer detection threshold 150
#   bgp dampening 10 10 100 50
#   network 198.51.110.10 mask 255.255.255.255 backdoor
#   aggregate-address 192.0.2.1 255.255.255.255 as-confed-set
#   neighbor 198.51.110.1 remote-as 100
#   neighbor 198.51.110.1 log-neighbor-changes disable
#   neighbor 198.51.110.1 version 4
#   neighbor 198.51.110.1 activate
#   neighbor 198.51.110.1 route-server-client
#   neighbor 198.51.110.1 slow-peer detection threshold 150
#   neighbor 198.51.110.1 route-map test-override-route out
#   neighbor 198.51.110.1 maximum-prefix 1 10 restart 100
#  exit-address-family

# Using Deleted

# Before state:
# -------------
#
# vios#sh running-config | section ^router bgp
# router bgp 65000
#  bgp log-neighbor-changes
#  bgp nopeerup-delay cold-boot 20
#  !
#  address-family ipv4 multicast
#   table-map test_tableMap filter
#   network 1.1.1.1 mask 255.255.255.255 route-map test
#   aggregate-address 192.0.3.1 255.255.255.255 as-confed-set
#   default-metric 12
#   distance bgp 10 10 100
#  exit-address-family
#  !
#  address-family ipv4 mdt
#   bgp dampening 1 10 100 5
#   bgp dmzlink-bw
#   bgp soft-reconfig-backup
#  exit-address-family
#  !
#  address-family ipv4 multicast vrf blue
#   bgp aggregate-timer 10
#   bgp slow-peer detection threshold 150
#   bgp dampening 1 1 1 1
#   network 198.51.110.10 mask 255.255.255.255 backdoor
#   aggregate-address 192.0.2.1 255.255.255.255 as-confed-set
#   neighbor 198.51.100.1 remote-as 10
#   neighbor 198.51.100.1 activate
#   neighbor 198.51.100.1 aigp send cost-community 100 poi igp-cost transitive
#   neighbor 198.51.100.1 route-server-client
#   neighbor 198.51.100.1 slow-peer detection threshold 150
#   neighbor 198.51.100.1 route-map test-route out
#  exit-address-family

- name: "Delete AF BGP (Note: This won't delete the all configured AF BGP)"
  cisco.ios.ios_bgp_address_family:
    config:
      as_number: 65000
      address_family:
        - afi: ipv4
          safi: multicast
        - afi: ipv4
          safi: mdt
    state: deleted

# Commands fired:
# ---------------
# "commands": [
#       "router bgp 65000",
#       "no address-family ipv4 multicast",
#       "no address-family ipv4 mdt"
#   ]

# After state:
# -------------
#
# vios#sh running-config | section ^router bg
# router bgp 65000
#  bgp log-neighbor-changes
#  bgp nopeerup-delay cold-boot 20
#  !
#  address-family ipv4 multicast vrf blue
#   bgp aggregate-timer 10
#   bgp slow-peer detection threshold 150
#   bgp dampening 1 1 1 1
#   network 198.51.110.10 mask 255.255.255.255 backdoor
#   aggregate-address 192.0.2.1 255.255.255.255 as-confed-set
#   neighbor 198.51.100.1 remote-as 10
#   neighbor 198.51.100.1 activate
#   neighbor 198.51.100.1 aigp send cost-community 100 poi igp-cost transitive
#   neighbor 198.51.100.1 route-server-client
#   neighbor 198.51.100.1 slow-peer detection threshold 150
#   neighbor 198.51.100.1 route-map test-route out
#  exit-address-family

# Using Deleted without any config passed
#"(NOTE: This will delete all of configured AF BGP)"

# Before state:
# -------------
#
# vios#sh running-config | section ^router bgp
# router bgp 65000
#  bgp log-neighbor-changes
#  bgp nopeerup-delay cold-boot 20
#  !
#  address-family ipv4 multicast
#   table-map test_tableMap filter
#   network 1.1.1.1 mask 255.255.255.255 route-map test
#   aggregate-address 192.0.3.1 255.255.255.255 as-confed-set
#   default-metric 12
#   distance bgp 10 10 100
#  exit-address-family
#  !
#  address-family ipv4 mdt
#   bgp dampening 1 10 100 5
#   bgp dmzlink-bw
#   bgp soft-reconfig-backup
#  exit-address-family
#  !
#  address-family ipv4 multicast vrf blue
#   bgp aggregate-timer 10
#   bgp slow-peer detection threshold 150
#   bgp dampening 1 1 1 1
#   network 198.51.110.10 mask 255.255.255.255 backdoor
#   aggregate-address 192.0.2.1 255.255.255.255 as-confed-set
#   neighbor 198.51.100.1 remote-as 10
#   neighbor 198.51.100.1 activate
#   neighbor 198.51.100.1 aigp send cost-community 100 poi igp-cost transitive
#   neighbor 198.51.100.1 route-server-client
#   neighbor 198.51.100.1 slow-peer detection threshold 150
#   neighbor 198.51.100.1 route-map test-route out
#  exit-address-family

- name: 'Delete ALL of configured AF BGP (Note: This WILL delete the all configured
    AF BGP)'
  cisco.ios.ios_bgp_address_family:
    state: deleted

# Commands fired:
# ---------------
# "commands": [
#       "router bgp 65000",
#       "no address-family ipv4 multicast vrf blue",
#       "no address-family ipv4 multicast",
#       "no address-family ipv4 mdt"
#   ]

# After state:
# -------------
#
# vios#sh running-config | section ^router bgp
# router bgp 65000
#  bgp log-neighbor-changes
#  bgp nopeerup-delay cold-boot 20

# Using Gathered
# Before state:
# -------------
#
# vios#sh running-config | section ^router bgp

- name: Gather listed AF BGP with provided configurations
  cisco.ios.ios_bgp_address_family:
    config:
    state: gathered

# Module Execution Result:
# ------------------------
#
# "gathered": {
#       "address_family": [
#           {
#               "afi": "ipv4",
#               "aggregate_address": [{
#                   "address": "192.0.2.1",
#                   "as_confed_set": true,
#                   "netmask": "255.255.255.255"
#               }],
#               "bgp": {
#                   "aggregate_timer": 10,
#                   "dampening": {
#                       "max_suppress": 1,
#                       "penalty_half_time": 1,
#                       "reuse_route_val": 1,
#                       "suppress_route_val": 1
#                   },
#                   "slow_peer": [
#                       {
#                           "detection": {
#                               "threshold": 150
#                           }
#                       }
#                   ]
#               },
#               "neighbor": [
#                   {
#                       "activate": true,
#                       "address": "198.51.100.1",
#                       "aigp": {
#                           "send": {
#                               "cost_community": {
#                                   "id": 100,
#                                   "poi": {
#                                       "igp_cost": true,
#                                       "transitive": true
#                                   }
#                               }
#                           }
#                       },
#                       "remote_as": 10,
#                       "route_map": {
#                           "name": "test-route",
#                           "out": true
#                       },
#                       "route_server_client": true,
#                       "slow_peer": [
#                           {
#                               "detection": {
#                                   "threshold": 150
#                               }
#                           }
#                       ]
#                   }
#               ],
#               "network": [
#                   {
#                       "address": "198.51.110.10",
#                       "backdoor": true,
#                       "mask": "255.255.255.255"
#                   }
#               ],
#               "safi": "multicast",
#               "snmp": {
#                   "context": {
#                       "community": {
#                           "acl": "10",
#                           "ro": true,
#                           "snmp_community": "community"
#                       },
#                       "name": "snnmp_con_1"
#                   }
#               },
#               "vrf": "blue"
#           },
#           {
#               "afi": "ipv4",
#               "aggregate_address": [{
#                   "address": "192.0.3.1",
#                   "as_confed_set": true,
#                   "netmask": "255.255.255.255"
#               }],
#               "default_metric": 12,
#               "distance": {
#                   "external": 10,
#                   "internal": 10,
#                   "local": 100
#               },
#               "network": [
#                   {
#                       "address": "1.1.1.1",
#                       "mask": "255.255.255.255",
#                       "route_map": "test"
#                   }
#               ],
#               "safi": "multicast",
#               "table_map": {
#                   "filter": true,
#                   "name": "test_tableMap"
#               }
#           },
#           {
#               "afi": "ipv4",
#               "bgp": {
#                   "dampening": {
#                       "max_suppress": 5,
#                       "penalty_half_time": 1,
#                       "reuse_route_val": 10,
#                       "suppress_route_val": 100
#                   },
#                   "dmzlink_bw": true,
#                   "soft_reconfig_backup": true
#               },
#               "safi": "mdt"
#           }
#       ],
#       "as_number": "65000"
#   }

# Using Rendered

- name: Rendered the provided configuration with the exisiting running configuration
  cisco.ios.ios_bgp_address_family:
    config:
      as_number: 65000
      address_family:
        - afi: ipv4
          safi: multicast
          vrf: blue
          aggregate_address:
            - address: 192.0.2.1
              netmask: 255.255.255.255
              as_confed_set: true
          bgp:
            aggregate_timer: 10
            dampening:
              penalty_half_time: 1
              reuse_route_val: 1
              suppress_route_val: 1
              max_suppress: 1
            slow_peer:
              - detection:
                  threshold: 150
          neighbor:
            - address: 198.51.100.1
              aigp:
                send:
                  cost_community:
                    id: 100
                    poi:
                      igp_cost: true
                      transitive: true
              slow_peer:
                - detection:
                    threshold: 150
              remote_as: 10
              route_map:
                name: test-route
                out: true
              route_server_client: true
          network:
            - address: 198.51.110.10
              mask: 255.255.255.255
              backdoor: true
          snmp:
            context:
              name: snmp_con
              community:
                snmp_community: community
                ro: true
                acl: 10
        - afi: ipv4
          safi: mdt
          bgp:
            dmzlink_bw: true
            dampening:
              penalty_half_time: 1
              reuse_route_val: 10
              suppress_route_val: 100
              max_suppress: 5
            soft_reconfig_backup: true
    state: rendered

# Module Execution Result:
# ------------------------
#
# "rendered": [
#     "router bgp 65000",
#     "address-family ipv4 multicast vrf blue",
#     "bgp aggregate-timer 10",
#     "bgp slow-peer detection threshold 150",
#     "bgp dampening 1 1 1 1",
#     "neighbor 198.51.100.1 remote-as 10",
#     "neighbor 198.51.100.1 aigp send cost-community 100 poi igp-cost transitive",
#     "neighbor 198.51.100.1 route-map test-route out",
#     "neighbor 198.51.100.1 route-server-client",
#     "neighbor 198.51.100.1 slow-peer detection threshold 150",
#     "network 198.51.110.10 mask 255.255.255.255 backdoor",
#     "snmp context snnmp_con_1 community community ro 10",
#     "aggregate-address 192.0.2.1 255.255.255.255 as-confed-set",
#     "exit-address-family",
#     "address-family ipv4 mdt",
#     "bgp dmzlink-bw",
#     "bgp dampening 1 10 100 5",
#     "bgp soft-reconfig-backup"
#     "exit-address-family",
# ]

# Using Parsed

# File: parsed.cfg
# ----------------
# router bgp 65000
#  bgp log-neighbor-changes
#  bgp nopeerup-delay cold-boot 20
#  !
#  address-family ipv4 multicast
#   table-map test_tableMap filter
#   network 1.1.1.1 mask 255.255.255.255 route-map test
#   aggregate-address 192.0.3.1 255.255.255.255 as-confed-set
#   default-metric 12
#   distance bgp 10 10 100
#  exit-address-family
#  !
#  address-family ipv4 mdt
#   bgp dampening 1 10 100 5
#   bgp dmzlink-bw
#   bgp soft-reconfig-backup
#  exit-address-family
#  !

- name: Parse the commands for provided configuration
  cisco.ios.ios_bgp_address_family:
    running_config: "{{ lookup('file', 'parsed.cfg') }}"
    state: parsed

# Module Execution Result:
# ------------------------
#
# "parsed": {
#       "address_family": [
#           {
#               "afi": "ipv4",
#               "aggregate_address": [{
#                   "address": "192.0.3.1",
#                   "as_confed_set": true,
#                   "netmask": "255.255.255.255"
#               }],
#               "default_metric": 12,
#               "distance": {
#                   "external": 10,
#                   "internal": 10,
#                   "local": 100
#               },
#               "network": [
#                   {
#                       "address": "1.1.1.1",
#                       "mask": "255.255.255.255",
#                       "route_map": "test"
#                   }
#               ],
#               "safi": "multicast",
#               "table_map": {
#                   "filter": true,
#                   "name": "test_tableMap"
#               }
#           },
#           {
#               "afi": "ipv4",
#               "bgp": {
#                   "dampening": {
#                       "max_suppress": 5,
#                       "penalty_half_time": 1,
#                       "reuse_route_val": 10,
#                       "suppress_route_val": 100
#                   },
#                   "dmzlink_bw": true,
#                   "soft_reconfig_backup": true
#               },
#               "safi": "mdt"
#           }
#       ],
#       "as_number": "65000"
#   }

"""

RETURN = """
before:
  description: The configuration as structured data prior to module invocation.
  returned: always
  type: list
  sample: The configuration returned will always be in the same format of the parameters above.
after:
  description: The configuration as structured data after module completion.
  returned: when changed
  type: list
  sample: The configuration returned will always be in the same format of the parameters above.
commands:
  description: The set of commands pushed to the remote device
  returned: always
  type: list
  sample: [
    "router bgp 65000",
    "address-family ipv4 multicast",
    "table-map test_tableMap filter",
    "network 1.1.1.1 mask 255.255.255.255 route-map test",
    "aggregate-address 192.0.3.1 255.255.255.255 as-confed-set",
  ]
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.bgp_address_family.bgp_address_family import (
    Bgp_AddressFamilyArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.bgp_address_family.bgp_address_family import (
    Bgp_AddressFamily,
)


def main():
    """
    Main entry point for module execution
    :returns: the result form module invocation
    """
    required_if = [
        ("state", "merged", ("config",)),
        ("state", "replaced", ("config",)),
        ("state", "overridden", ("config",)),
        ("state", "rendered", ("config",)),
        ("state", "parsed", ("running_config",)),
    ]
    mutually_exclusive = [("config", "running_config")]
    module = AnsibleModule(
        argument_spec=Bgp_AddressFamilyArgs.argument_spec,
        required_if=required_if,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True,
    )
    result = Bgp_AddressFamily(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
