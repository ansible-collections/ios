#
# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.cisco.ios.tests.unit.compat.mock import patch
from ansible_collections.cisco.ios.plugins.modules import ios_route_maps
from ansible_collections.cisco.ios.tests.unit.modules.utils import (
    set_module_args,
)
from .ios_module import TestIosModule, load_fixture


class TestIosRouteMapsModule(TestIosModule):
    module = ios_route_maps

    def setUp(self):
        super(TestIosRouteMapsModule, self).setUp()

        self.mock_get_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network.Config.get_config"
        )
        self.get_config = self.mock_get_config.start()

        self.mock_load_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network.Config.load_config"
        )
        self.load_config = self.mock_load_config.start()

        self.mock_get_resource_connection_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.cfg.base."
            "get_resource_connection"
        )
        self.get_resource_connection_config = (
            self.mock_get_resource_connection_config.start()
        )

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection"
        )
        self.get_resource_connection_facts = (
            self.mock_get_resource_connection_facts.start()
        )

        self.mock_edit_config = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.providers.providers.CliProvider.edit_config"
        )
        self.edit_config = self.mock_edit_config.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.route_maps.route_maps."
            "Route_mapsFacts.get_route_maps_data"
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosRouteMapsModule, self).tearDown()
        self.mock_get_resource_connection_config.stop()
        self.mock_get_resource_connection_facts.stop()
        self.mock_edit_config.stop()
        self.mock_get_config.stop()
        self.mock_load_config.stop()
        self.mock_execute_show_command.stop()

    def load_fixtures(self, commands=None):
        def load_from_file(*args, **kwargs):
            return load_fixture("ios_route_maps.cfg")

        self.execute_show_command.side_effect = load_from_file

    def test_ios_route_maps_merged(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        entries=[
                            dict(
                                action="deny",
                                continue_entry=dict(entry_sequence=20),
                                description="this is merge test",
                                match=dict(
                                    additional_paths=dict(all=True),
                                    as_path=dict(acls=[100, 120]),
                                    clns=dict(address="test_osi"),
                                    community=dict(
                                        exact_match=True, name=["new_merge"]
                                    ),
                                    ip=dict(address=dict(acls=[10, 100])),
                                    length=dict(maximum=50000, minimum=5000),
                                    mpls_label=True,
                                    policy_lists=["ip_policy"],
                                    route_type=dict(
                                        external=dict(type_1=True),
                                        nssa_external=dict(type_1=True),
                                    ),
                                ),
                                set=dict(
                                    dampening=dict(
                                        penalty_half_time=10,
                                        reuse_route_val=100,
                                        suppress_route_val=100,
                                        max_suppress=10,
                                    ),
                                    extcomm_list="test_excomm",
                                    extcommunity=dict(
                                        vpn_distinguisher=dict(
                                            address="192.0.2.1:12"
                                        )
                                    ),
                                    ip=dict(
                                        address="192.0.2.1",
                                        df=1,
                                        next_hop=dict(
                                            recursive=dict(
                                                global_route=True,
                                                address="198.51.110.1",
                                            ),
                                            verify_availability=dict(
                                                address="198.51.111.1",
                                                sequence=100,
                                                track=10,
                                            ),
                                        ),
                                        precedence=dict(critical=True),
                                    ),
                                    traffic_index=10,
                                    weight=100,
                                ),
                                sequence=10,
                            )
                        ],
                        route_map="test_1",
                    ),
                    dict(
                        entries=[
                            dict(
                                action="deny",
                                match=dict(
                                    ipv6=dict(
                                        address=dict(acl="test_ip_acl"),
                                        next_hop=dict(prefix_list="test_new"),
                                        route_source=dict(acl="route_src_acl"),
                                    ),
                                    security_group=dict(source=[10, 20]),
                                    local_preference=dict(value=[55, 105]),
                                    mpls_label=True,
                                ),
                                sequence=10,
                            )
                        ],
                        route_map="test_2",
                    ),
                ],
                state="merged",
            )
        )
        commands = [
            "route-map test_1 deny 10",
            "continue 20",
            "description this is merge test",
            "match community 100 99 new_merge test_1 test_2 exact-match",
            "match length 5000 50000",
            "set dampening 10 100 100 10",
            "set extcomm-list test_excomm delete",
            "set extcommunity vpn-distinguisher 192.0.2.1:12",
            "set ip address prefix-list 192.0.2.1",
            "set ip df 1",
            "set ip next-hop verify-availability 198.51.111.1 100 track 10",
            "set ip next-hop recursive global 198.51.110.1",
            "set ip precedence critical",
            "set weight 100",
            "set traffic-index 10",
            "route-map test_2 deny 10",
            "match ipv6 address test_ip_acl",
            "match ipv6 next-hop prefix-list test_new",
            "match ipv6 route-source route_src_acl",
            "match security-group source tag 10 20",
            "match local-preference 105 55",
            "match mpls-label",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_route_maps_merged_idempotent(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        entries=[
                            dict(
                                action="deny",
                                continue_entry=dict(entry_sequence=100),
                                description="this is test",
                                match=dict(
                                    additional_paths=dict(all=True),
                                    as_path=dict(acls=[100, 120]),
                                    clns=dict(address="test_osi"),
                                    community=dict(
                                        exact_match=True,
                                        name=["99", "100", "test_1", "test_2"],
                                    ),
                                    extcommunity=["110", "130"],
                                    interfaces=["GigabitEthernet0/1"],
                                    ip=dict(address=dict(acls=[10, 100])),
                                    ipv6=dict(
                                        route_source=dict(acl="test_ipv6")
                                    ),
                                    length=dict(maximum=10000, minimum=1000),
                                    local_preference=dict(value=[100]),
                                    mdt_group=dict(acls=["25", "30"]),
                                    metric=dict(external=True, value=100),
                                    mpls_label=True,
                                    policy_lists=["ip_policy"],
                                    route_type=dict(
                                        external=dict(type_1=True),
                                        nssa_external=dict(type_1=True),
                                    ),
                                    rpki=dict(invalid=True),
                                    security_group=dict(destination=[100]),
                                    tag=dict(tag_list=["test_tag"]),
                                    track=100,
                                ),
                                sequence=10,
                            ),
                            dict(
                                action="deny",
                                sequence=20,
                                set=dict(
                                    aigp_metric=dict(value=1000),
                                    as_path=dict(prepend=dict(last_as=10)),
                                    automatic_tag=True,
                                    clns="11.1111",
                                    comm_list="test_comm",
                                    community=dict(
                                        additive=True, internet=True
                                    ),
                                    dampening=dict(
                                        penalty_half_time=10,
                                        reuse_route_val=100,
                                        suppress_route_val=100,
                                        max_suppress=10,
                                    ),
                                    extcomm_list="test_excomm",
                                    extcommunity=dict(
                                        vpn_distinguisher=dict(
                                            address="192.0.2.1:12"
                                        )
                                    ),
                                    global_route=True,
                                    interfaces=[
                                        "GigabitEthernet0/2",
                                        "GigabitEthernet0/1",
                                    ],
                                    level=dict(level_1_2=True),
                                    lisp="test_lisp",
                                    local_preference=100,
                                    metric=dict(
                                        deviation="plus", metric_value=100
                                    ),
                                    metric_type=dict(type_1=True),
                                    mpls_label=True,
                                    origin=dict(igp=True),
                                    tag=50529027,
                                    traffic_index=10,
                                    weight=100,
                                ),
                            ),
                        ],
                        route_map="test_1",
                    )
                ],
                state="merged",
            )
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_route_maps_replaced(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        entries=[
                            dict(
                                action="deny",
                                continue_entry=dict(entry_sequence=20),
                                description="this is replace test",
                                match=dict(
                                    additional_paths=dict(all=True),
                                    as_path=dict(acls=[100, 120]),
                                    clns=dict(address="test_osi"),
                                    community=dict(
                                        exact_match=True, name=["new_replace"]
                                    ),
                                    ip=dict(address=dict(acls=[10, 100])),
                                    length=dict(maximum=50000, minimum=5000),
                                    mpls_label=True,
                                    policy_lists=["ip_policy"],
                                    route_type=dict(
                                        external=dict(type_1=True),
                                        nssa_external=dict(type_1=True),
                                    ),
                                ),
                                set=dict(
                                    dampening=dict(
                                        penalty_half_time=10,
                                        reuse_route_val=100,
                                        suppress_route_val=100,
                                        max_suppress=10,
                                    ),
                                    extcomm_list="test_excomm",
                                    extcommunity=dict(
                                        vpn_distinguisher=dict(
                                            address="192.0.2.1:12"
                                        )
                                    ),
                                    ip=dict(
                                        address="192.0.2.1",
                                        df=1,
                                        next_hop=dict(
                                            recursive=dict(
                                                global_route=True,
                                                address="198.51.110.1",
                                            ),
                                            verify_availability=dict(
                                                address="198.51.111.1",
                                                sequence=100,
                                                track=10,
                                            ),
                                        ),
                                        precedence=dict(critical=True),
                                    ),
                                    traffic_index=10,
                                    weight=100,
                                ),
                                sequence=10,
                            )
                        ],
                        route_map="test_1",
                    ),
                    dict(
                        entries=[
                            dict(
                                action="deny",
                                match=dict(
                                    ipv6=dict(
                                        address=dict(acl="test_ip_acl"),
                                        next_hop=dict(prefix_list="test_new"),
                                        route_source=dict(acl="route_src_acl"),
                                    ),
                                    security_group=dict(source=[10, 20]),
                                    local_preference=dict(value=[55, 105]),
                                    mpls_label=True,
                                ),
                                sequence=10,
                            )
                        ],
                        route_map="test_2",
                    ),
                ],
                state="replaced",
            )
        )
        commands = [
            "route-map test_1 deny 10",
            "no description this is test",
            "continue 20",
            "description this is replace test",
            "match community new_replace exact-match",
            "match length 5000 50000",
            "no match mdt-group 25 30",
            "no match extcommunity 110 130",
            "no match interface GigabitEthernet0/1",
            "no match ipv6 route-source test_ipv6",
            "no match local-preference 100",
            "no match rpki invalid",
            "no match metric external 100",
            "no match source-protocol ospfv3 10000 static",
            "no match track 100",
            "no match tag list test_tag",
            "set dampening 10 100 100 10",
            "set extcomm-list test_excomm delete",
            "set extcommunity vpn-distinguisher 192.0.2.1:12",
            "set ip address prefix-list 192.0.2.1",
            "set ip df 1",
            "set ip next-hop recursive global 198.51.110.1",
            "set ip next-hop verify-availability 198.51.111.1 100 track 10",
            "set ip precedence critical",
            "set traffic-index 10",
            "set weight 100",
            "no route-map test_1 deny 20",
            "route-map test_2 deny 10",
            "match ipv6 address test_ip_acl",
            "match ipv6 next-hop prefix-list test_new",
            "match ipv6 route-source route_src_acl",
            "match security-group source tag 10 20",
            "match local-preference 105 55",
            "match mpls-label",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_route_maps_replaced_idempotent(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        entries=[
                            dict(
                                action="deny",
                                continue_entry=dict(entry_sequence=100),
                                description="this is test",
                                match=dict(
                                    additional_paths=dict(all=True),
                                    as_path=dict(acls=[100, 120]),
                                    clns=dict(address="test_osi"),
                                    community=dict(
                                        exact_match=True,
                                        name=["99", "100", "test_1", "test_2"],
                                    ),
                                    extcommunity=["110", "130"],
                                    interfaces=["GigabitEthernet0/1"],
                                    ip=dict(address=dict(acls=[10, 100])),
                                    ipv6=dict(
                                        route_source=dict(acl="test_ipv6")
                                    ),
                                    length=dict(maximum=10000, minimum=1000),
                                    local_preference=dict(value=[100]),
                                    mdt_group=dict(acls=["25", "30"]),
                                    metric=dict(external=True, value=100),
                                    mpls_label=True,
                                    policy_lists=["ip_policy"],
                                    route_type=dict(
                                        external=dict(type_1=True),
                                        nssa_external=dict(type_1=True),
                                    ),
                                    rpki=dict(invalid=True),
                                    security_group=dict(destination=[100]),
                                    source_protocol=dict(
                                        ospfv3=10000, static=True
                                    ),
                                    tag=dict(tag_list=["test_tag"]),
                                    track=100,
                                ),
                                sequence=10,
                            ),
                            dict(
                                action="deny",
                                sequence=20,
                                set=dict(
                                    aigp_metric=dict(value=1000),
                                    as_path=dict(prepend=dict(last_as=10)),
                                    automatic_tag=True,
                                    clns="11.1111",
                                    comm_list="test_comm",
                                    community=dict(
                                        additive=True, internet=True
                                    ),
                                    dampening=dict(
                                        penalty_half_time=10,
                                        reuse_route_val=100,
                                        suppress_route_val=100,
                                        max_suppress=10,
                                    ),
                                    extcomm_list="test_excomm",
                                    extcommunity=dict(
                                        vpn_distinguisher=dict(
                                            address="192.0.2.1:12"
                                        )
                                    ),
                                    global_route=True,
                                    interfaces=[
                                        "GigabitEthernet0/2",
                                        "GigabitEthernet0/1",
                                    ],
                                    level=dict(level_1_2=True),
                                    lisp="test_lisp",
                                    local_preference=100,
                                    metric=dict(
                                        deviation="plus", metric_value=100
                                    ),
                                    metric_type=dict(type_1=True),
                                    mpls_label=True,
                                    origin=dict(igp=True),
                                    tag=50529027,
                                    traffic_index=10,
                                    weight=100,
                                ),
                            ),
                        ],
                        route_map="test_1",
                    )
                ],
                state="replaced",
            )
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_route_maps_overridden(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        entries=[
                            dict(
                                action="deny",
                                continue_entry=dict(entry_sequence=20),
                                description="this is override test",
                                match=dict(
                                    additional_paths=dict(all=True),
                                    as_path=dict(acls=[100, 120]),
                                    clns=dict(address="test_osi"),
                                    community=dict(
                                        exact_match=True, name=["new_override"]
                                    ),
                                    ip=dict(address=dict(acls=[10, 100])),
                                    length=dict(maximum=50000, minimum=5000),
                                    mpls_label=True,
                                    policy_lists=["ip_policy"],
                                    route_type=dict(
                                        external=dict(type_1=True),
                                        nssa_external=dict(type_1=True),
                                    ),
                                ),
                                set=dict(
                                    dampening=dict(
                                        penalty_half_time=10,
                                        reuse_route_val=100,
                                        suppress_route_val=100,
                                        max_suppress=10,
                                    ),
                                    extcomm_list="test_excomm",
                                    extcommunity=dict(
                                        vpn_distinguisher=dict(
                                            address="192.0.2.1:12"
                                        )
                                    ),
                                    ip=dict(
                                        address="192.0.2.1",
                                        df=1,
                                        next_hop=dict(
                                            recursive=dict(
                                                global_route=True,
                                                address="198.51.110.1",
                                            ),
                                            verify_availability=dict(
                                                address="198.51.111.1",
                                                sequence=100,
                                                track=10,
                                            ),
                                        ),
                                        precedence=dict(critical=True),
                                    ),
                                    traffic_index=10,
                                    weight=100,
                                ),
                                sequence=10,
                            )
                        ],
                        route_map="test_1",
                    ),
                    dict(
                        entries=[
                            dict(
                                action="deny",
                                match=dict(
                                    ipv6=dict(
                                        address=dict(acl="test_ip_acl"),
                                        next_hop=dict(prefix_list="test_new"),
                                        route_source=dict(acl="route_src_acl"),
                                    ),
                                    security_group=dict(source=[10, 20]),
                                    local_preference=dict(value=[55, 105]),
                                    mpls_label=True,
                                ),
                                sequence=10,
                            )
                        ],
                        route_map="test_2",
                    ),
                ],
                state="overridden",
            )
        )
        commands = [
            "route-map test_1 deny 10",
            "no description this is test",
            "continue 20",
            "description this is override test",
            "match community new_override exact-match",
            "match length 5000 50000",
            "no match mdt-group 25 30",
            "no match extcommunity 110 130",
            "no match interface GigabitEthernet0/1",
            "no match ipv6 route-source test_ipv6",
            "no match local-preference 100",
            "no match rpki invalid",
            "no match metric external 100",
            "no match source-protocol ospfv3 10000 static",
            "no match track 100",
            "no match tag list test_tag",
            "set dampening 10 100 100 10",
            "set extcomm-list test_excomm delete",
            "set extcommunity vpn-distinguisher 192.0.2.1:12",
            "set ip address prefix-list 192.0.2.1",
            "set ip df 1",
            "set ip next-hop recursive global 198.51.110.1",
            "set ip next-hop verify-availability 198.51.111.1 100 track 10",
            "set ip precedence critical",
            "set traffic-index 10",
            "set weight 100",
            "no route-map test_1 deny 20",
            "route-map test_2 deny 10",
            "match ipv6 address test_ip_acl",
            "match ipv6 next-hop prefix-list test_new",
            "match ipv6 route-source route_src_acl",
            "match security-group source tag 10 20",
            "match local-preference 105 55",
            "match mpls-label",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_route_maps_overridden_idempotent(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        entries=[
                            dict(
                                action="deny",
                                continue_entry=dict(entry_sequence=100),
                                description="this is test",
                                match=dict(
                                    additional_paths=dict(all=True),
                                    as_path=dict(acls=[100, 120]),
                                    clns=dict(address="test_osi"),
                                    community=dict(
                                        exact_match=True,
                                        name=["99", "100", "test_1", "test_2"],
                                    ),
                                    extcommunity=["110", "130"],
                                    interfaces=["GigabitEthernet0/1"],
                                    ip=dict(address=dict(acls=[10, 100])),
                                    ipv6=dict(
                                        route_source=dict(acl="test_ipv6")
                                    ),
                                    length=dict(maximum=10000, minimum=1000),
                                    local_preference=dict(value=[100]),
                                    mdt_group=dict(acls=["25", "30"]),
                                    metric=dict(external=True, value=100),
                                    mpls_label=True,
                                    policy_lists=["ip_policy"],
                                    route_type=dict(
                                        external=dict(type_1=True),
                                        nssa_external=dict(type_1=True),
                                    ),
                                    rpki=dict(invalid=True),
                                    security_group=dict(destination=[100]),
                                    source_protocol=dict(
                                        ospfv3=10000, static=True
                                    ),
                                    tag=dict(tag_list=["test_tag"]),
                                    track=100,
                                ),
                                sequence=10,
                            ),
                            dict(
                                action="deny",
                                sequence=20,
                                set=dict(
                                    aigp_metric=dict(value=1000),
                                    as_path=dict(prepend=dict(last_as=10)),
                                    automatic_tag=True,
                                    clns="11.1111",
                                    comm_list="test_comm",
                                    community=dict(
                                        additive=True, internet=True
                                    ),
                                    dampening=dict(
                                        penalty_half_time=10,
                                        reuse_route_val=100,
                                        suppress_route_val=100,
                                        max_suppress=10,
                                    ),
                                    extcomm_list="test_excomm",
                                    extcommunity=dict(
                                        vpn_distinguisher=dict(
                                            address="192.0.2.1:12"
                                        )
                                    ),
                                    global_route=True,
                                    interfaces=[
                                        "GigabitEthernet0/2",
                                        "GigabitEthernet0/1",
                                    ],
                                    level=dict(level_1_2=True),
                                    lisp="test_lisp",
                                    local_preference=100,
                                    metric=dict(
                                        deviation="plus", metric_value=100
                                    ),
                                    metric_type=dict(type_1=True),
                                    mpls_label=True,
                                    origin=dict(igp=True),
                                    tag=50529027,
                                    traffic_index=10,
                                    weight=100,
                                ),
                            ),
                        ],
                        route_map="test_1",
                    )
                ],
                state="overridden",
            )
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_route_maps_deleted(self):
        set_module_args(
            dict(config=[dict(route_map="test_1")], state="deleted")
        )
        commands = ["no route-map test_1"]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_route_maps_delete_without_config(self):
        set_module_args(dict(state="deleted"))
        commands = ["no route-map test_1"]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_route_maps_rendered(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        entries=[
                            dict(
                                action="deny",
                                continue_entry=dict(entry_sequence=100),
                                description="this is test",
                                match=dict(
                                    additional_paths=dict(all=True),
                                    as_path=dict(acls=[100, 120]),
                                    clns=dict(address="test_osi"),
                                    community=dict(
                                        exact_match=True,
                                        name=["99", "100", "test_1", "test_2"],
                                    ),
                                    extcommunity=["110", "130"],
                                    interfaces=[
                                        "GigabitEthernet0/1",
                                        "GigabitEthernet0/2",
                                    ],
                                    ip=dict(address=dict(acls=[10, 100])),
                                    ipv6=dict(
                                        route_source=dict(acl="test_ipv6")
                                    ),
                                    length=dict(maximum=10000, minimum=1000),
                                    local_preference=dict(value=[100]),
                                    mdt_group=dict(acls=["25", "30"]),
                                    metric=dict(external=True, value=100),
                                    mpls_label=True,
                                    policy_lists=["ip_policy"],
                                    route_type=dict(
                                        external=dict(type_1=True),
                                        nssa_external=dict(type_1=True),
                                    ),
                                    rpki=dict(invalid=True),
                                    security_group=dict(destination=[100]),
                                    source_protocol=dict(
                                        ospfv3=10000, static=True
                                    ),
                                    tag=dict(tag_list=["test_tag"]),
                                    track=100,
                                ),
                                sequence=10,
                            ),
                            dict(
                                action="deny",
                                sequence=20,
                                set=dict(
                                    aigp_metric=dict(value=1000),
                                    as_path=dict(prepend=dict(last_as=10)),
                                    automatic_tag=True,
                                    clns="11.1111",
                                    comm_list="test_comm",
                                    community=dict(
                                        additive=True, internet=True
                                    ),
                                    dampening=dict(
                                        penalty_half_time=10,
                                        reuse_route_val=100,
                                        suppress_route_val=100,
                                        max_suppress=10,
                                    ),
                                    extcomm_list="test_excomm",
                                    extcommunity=dict(
                                        vpn_distinguisher=dict(
                                            address="192.0.2.1:12"
                                        )
                                    ),
                                    global_route=True,
                                    interfaces=[
                                        "GigabitEthernet0/2",
                                        "GigabitEthernet0/1",
                                    ],
                                    level=dict(level_1_2=True),
                                    lisp="test_lisp",
                                    local_preference=100,
                                    metric=dict(
                                        deviation="plus", metric_value=100
                                    ),
                                    metric_type=dict(type_1=True),
                                    mpls_label=True,
                                    origin=dict(igp=True),
                                    tag=50529027,
                                    traffic_index=10,
                                    weight=100,
                                ),
                            ),
                        ],
                        route_map="test_1",
                    )
                ],
                state="rendered",
            )
        )
        commands = [
            "route-map test_1 deny 10",
            "continue 100",
            "description this is test",
            "match additional-paths advertise-set all",
            "match as-path 100 120",
            "match clns address test_osi",
            "match mdt-group 25 30",
            "match community 100 99 test_1 test_2 exact-match",
            "match extcommunity 110 130",
            "match interface GigabitEthernet0/1 GigabitEthernet0/2",
            "match ip address 10 100",
            "match ipv6 route-source test_ipv6",
            "match length 1000 10000",
            "match local-preference 100",
            "match mpls-label",
            "match policy-list ip_policy",
            "match rpki invalid",
            "match route-type external type-1",
            "match metric external 100",
            "match source-protocol ospfv3 10000 static",
            "match track 100",
            "match tag list test_tag",
            "route-map test_1 deny 20",
            "set aigp-metric 1000",
            "set as-path prepend last-as 10",
            "set automatic-tag",
            "set clns next-hop 11.1111",
            "set comm-list test_comm delete",
            "set community additive internet",
            "set dampening 10 100 100 10",
            "set extcomm-list test_excomm delete",
            "set extcommunity vpn-distinguisher 192.0.2.1:12",
            "set weight 100",
            "set lisp locator-set test_lisp",
            "set interface GigabitEthernet0/1 GigabitEthernet0/2",
            "set tag 50529027",
            "set local-preference 100",
            "set mpls-label",
            "set metric-type type-1",
            "set traffic-index 10",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["rendered"]), sorted(commands))
