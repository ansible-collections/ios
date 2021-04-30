==================================
Cisco Ios Collection Release Notes
==================================

.. contents:: Topics

v2.1.0
======

Minor Changes
-------------
- Add support for ansible_network_resources key allows to fetch the available resources for a platform (https://github.com/ansible-collections/cisco.ios/pull/292).
- Add ios_route_maps Resource Module (https://github.com/ansible-collections/cisco.ios/pull/297).

Security Fixes
--------------
- To fix Cisco IOS no log issue and add ignore txt for 2.12 (https://github.com/ansible-collections/cisco.ios/pull/304).

Bugfixes
--------
- To fix the wrong arg being passed in acls template function (https://github.com/ansible-collections/cisco.ios/pull/305).

New Modules
-----------

- ios_route_maps - Manage the attributes of Route maps on Cisco IOS.

v2.0.1
======

Minor Changes
-------------
- Remove tests/sanity/requirements.txt (https://github.com/ansible-collections/cisco.ios/pull/261).

Bugfixes
--------
- Doc update to update users WRT to idempotence issue in ios_logging when logging is ON (https://github.com/ansible-collections/cisco.ios/pull/287).
- To fix ios_acls log and log_input params (https://github.com/ansible-collections/cisco.ios/pull/265).
- To add support for TwoGigabitEthernet interface option from IOS standpoint (https://github.com/ansible-collections/cisco.ios/pull/262).
- To fix ios_acls resource module acl_name traceback over some switches (https://github.com/ansible-collections/cisco.ios/pull/285).
- PR to fix ios_l2_interfaces issue where it wasn't working with range of vlans as expected (https://github.com/ansible-collections/cisco.ios/pull/264).
- To fix ios_acls Nonetype error when aces are empty (https://github.com/ansible-collections/cisco.ios/pull/260).
- To fix ios_vlans traceback error when empty line with just Ports information is available in config (https://github.com/ansible-collections/cisco.ios/pull/273).

v2.0.0
======

Major Changes
-------------

- Requires ansible.netcommon v2.0.0+ to support `ansible_network_single_user_mode` and `ansible_network_import_modules`.
- Please refer to ansible.netcommon `changelog <https://github.com/ansible-collections/ansible.netcommon/blob/main/changelogs/CHANGELOG.rst#ansible-netcommon-collection-release-notes>`_ for more details.

Minor Changes
-------------
- Add ios_bgp_address_family Resource Module. (https://github.com/ansible-collections/cisco.ios/pull/219).
- Adds support for `single_user_mode` command output caching. (https://github.com/ansible-collections/cisco.ios/pull/204).

Bugfixes
--------
- fix error when comparing two vlan using string instead of the int value (https://github.com/ansible-collections/cisco.ios/pull/249).
- To fix ios_acls parsed state example under module doc (https://github.com/ansible-collections/cisco.ios/pull/244).

New Modules
-----------
- ios_bgp_address_family - BGP Address Family resource module.

v1.3.0
======

Minor Changes
-------------

- Add ios_bgp_global module.

Bugfixes
--------
- IOS resource modules minor doc updates (https://github.com/ansible-collections/cisco.ios/pull/233).
- To fix ios_static_routes facts parsing in presence of interface (https://github.com/ansible-collections/cisco.ios/pull/225).
- Add support size and df_bit options for ios_ping (https://github.com/ansible-collections/cisco.ios/pull/228).
- IOS_CONFIG, incorrectly claims success when Command Rejected (https://github.com/ansible-collections/cisco.ios/pull/215).
- Update doc to clarify on input config pattern (https://github.com/ansible-collections/cisco.ios/pull/220).
- Updating ios acls module to use newer CLI RM approach to resolve all of the ACL related bugs (https://github.com/ansible-collections/cisco.ios/pull/211).

New Modules
-----------

- ios_bgp_global - BGP Global resource module

v1.2.1
======

Bugfixes
--------

- To fix ios_ospf_interfaces resource module authentication param behaviour (https://github.com/ansible-collections/cisco.ios/issues/209).
- Add version key to galaxy.yaml to work around ansible-galaxy bug.

v1.2.0
======

Minor Changes
-------------

- Add ios_ospf_interfaces module.

Bugfixes
--------

- To enable ios ospfv3 integration tests (https://github.com/ansible-collections/cisco.ios/pull/165).
- To fix ios_static_routes where interface ip route-cache config was being parsed and resulted traceback (https://github.com/ansible-collections/cisco.ios/pull/176).
- To fix IOS static routes idempotency issue coz of netmask to cidr conversion (https://github.com/ansible-collections/cisco.ios/pull/177).
- To fix ios_vlans traceback bug when the name had Remote in it and added unit TC for the module (https://github.com/ansible-collections/cisco.ios/pull/179).
- To fix the traceback issue for longer vlan name having more than 32 characters (https://github.com/ansible-collections/cisco.ios/pull/182).

New Modules
-----------

- ios_ospf_interfaces - OSPF Interfaces resource module

v1.1.0
======

Minor Changes
-------------

- Add ios_ospfv3 module.

Bugfixes
--------

- Fix element type of ios_command's command parameter (https://github.com/ansible-collections/cisco.ios/pull/151).
- Add support for interface type Virtual-Template (https://github.com/ansible-collections/cisco.ios/pull/154).
- Added support for interface Tunnel (https://github.com/ansible-collections/cisco.ios/pull/145).
- To fix the incorrect command displayed under ios_l3_interfaces resource module docs (https://github.com/ansible-collections/cisco.ios/pull/149).

New Modules
-----------

- ios_ospfv3 - OSPFv3 resource module

v1.0.3
======

Release Summary
---------------

- Releasing 1.0.3 with updated readme with changelog link, galaxy description, and bugfix.

Bugfixes
--------

- To fix the issue where ios acls was complaining in absence of protocol option value (https://github.com/ansible-collections/cisco.ios/pull/124).
- To fix IOS l2 interfaces for traceback error and merge operation not working as expected (https://github.com/ansible-collections/cisco.ios/pull/103).

v1.0.2
======

Release Summary
---------------

- Re-releasing 1.0.1 with updated changelog.

v1.0.1
======

Minor Changes
-------------

- Removes IOS sanity ignores and sync for argspec and docstring (https://github.com/ansible-collections/cisco.ios/pull/114).
- Updated docs.

Bugfixes
--------

- Make `src`, `backup` and `backup_options` in ios_config work when module alias is used (https://github.com/ansible-collections/cisco.ios/pull/107).


v1.0.0
======

New Plugins
-----------

Cliconf
~~~~~~~

- ios - Use ios cliconf to run command on Cisco IOS platform

New Modules
-----------

- ios_acl_interfaces - ACL interfaces resource module
- ios_acls - ACLs resource module
- ios_banner - Manage multiline banners on Cisco IOS devices
- ios_bgp - Configure global BGP protocol settings on Cisco IOS.
- ios_command - Run commands on remote devices running Cisco IOS
- ios_config - Manage Cisco IOS configuration sections
- ios_facts - Collect facts from remote devices running Cisco IOS
- ios_interface - (deprecated, removed after 2022-06-01) Manage Interface on Cisco IOS network devices
- ios_interfaces - Interfaces resource module
- ios_l2_interface - (deprecated, removed after 2022-06-01) Manage Layer-2 interface on Cisco IOS devices.
- ios_l2_interfaces - L2 interfaces resource module
- ios_l3_interface - (deprecated, removed after 2022-06-01) Manage Layer-3 interfaces on Cisco IOS network devices.
- ios_l3_interfaces - L3 interfaces resource module
- ios_lacp - LACP resource module
- ios_lacp_interfaces - LACP interfaces resource module
- ios_lag_interfaces - LAG interfaces resource module
- ios_linkagg - Manage link aggregation groups on Cisco IOS network devices
- ios_lldp - Manage LLDP configuration on Cisco IOS network devices.
- ios_lldp_global - LLDP resource module
- ios_lldp_interfaces - LLDP interfaces resource module
- ios_logging - Manage logging on network devices
- ios_ntp - Manages core NTP configuration.
- ios_ospfv2 - OSPFv2 resource module
- ios_ping - Tests reachability using ping from Cisco IOS network devices
- ios_static_route - (deprecated, removed after 2022-06-01) Manage static IP routes on Cisco IOS network devices
- ios_static_routes - Static routes resource module
- ios_system - Manage the system attributes on Cisco IOS devices
- ios_user - Manage the aggregate of local users on Cisco IOS device
- ios_vlan - (deprecated, removed after 2022-06-01) Manage VLANs on IOS network devices
- ios_vlans - VLANs resource module
- ios_vrf - Manage the collection of VRF definitions on Cisco IOS devices
