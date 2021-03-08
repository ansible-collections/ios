#
# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.cisco.ios.tests.unit.compat.mock import patch
from ansible_collections.cisco.ios.plugins.modules import (
    ios_bgp_address_family,
)
from ansible_collections.cisco.ios.tests.unit.modules.utils import (
    set_module_args,
)
from .ios_module import TestIosModule, load_fixture


class TestIosBgpAddressFamilyModule(TestIosModule):
    module = ios_bgp_address_family

    def setUp(self):
        super(TestIosBgpAddressFamilyModule, self).setUp()

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
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.bgp_address_family.bgp_address_family."
            "Bgp_AddressFamilyFacts.get_bgp_address_family_data"
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosBgpAddressFamilyModule, self).tearDown()
        self.mock_get_resource_connection_config.stop()
        self.mock_get_resource_connection_facts.stop()
        self.mock_edit_config.stop()
        self.mock_get_config.stop()
        self.mock_load_config.stop()
        self.mock_execute_show_command.stop()

    def load_fixtures(self, commands=None):
        def load_from_file(*args, **kwargs):
            return load_fixture("ios_bgp_address_family.cfg")

        self.execute_show_command.side_effect = load_from_file

    def test_ios_bgp_address_family_merged(self):
        set_module_args(
            dict(
                config=dict(
                    as_number="65000",
                    address_family=[
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            vrf="blue",
                            aggregate_address=[
                                dict(
                                    address="192.0.3.1",
                                    netmask="255.255.255.255",
                                    as_confed_set=True,
                                )
                            ],
                            bgp=dict(
                                dampening=dict(
                                    penalty_half_time=10,
                                    reuse_route_val=10,
                                    suppress_route_val=10,
                                    max_suppress=10,
                                )
                            ),
                            neighbor=[
                                dict(
                                    address="198.51.100.1",
                                    remote_as=65100,
                                    route_map=[
                                        dict(
                                            name="test-route-out",
                                            out="true"
                                        ),
                                    ],
                                    prefix_list=[
                                        dict(
                                            name="AS65100-PREFIX-OUT",
                                            out="true"
                                        ),
                                    ]
                                )
                            ]
                        ),
                        dict(
                            afi="nsap",
                            bgp=dict(
                                aggregate_timer=20,
                                dmzlink_bw=True,
                                scan_time=10,
                            ),
                            default_metric=10,
                            network=[
                                dict(
                                    address="192.0.1.1", route_map="test_route"
                                )
                            ],
                        ),
                    ],
                ),
                state="merged",
            )
        )
        commands = [
            "router bgp 65000",
            "address-family ipv4 multicast vrf blue",
            "bgp dampening 10 10 10 10",
            "aggregate-address 192.0.3.1 255.255.255.255 as-confed-set",
            "address-family nsap",
            "bgp aggregate-timer 20",
            "bgp dmzlink-bw",
            "bgp scan-time 10",
            "neighbor 192.168.100.100 route-map test-route-out out"
            "network 192.0.1.1 route-map test_route",
            "default-metric 10",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_bgp_address_family_merged_idempotent(self):
        set_module_args(
            dict(
                config=dict(
                    as_number="65000",
                    address_family=[
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            vrf="blue",
                            aggregate_address=[
                                dict(
                                    address="192.0.2.1",
                                    netmask="255.255.255.255",
                                    as_confed_set=True,
                                )
                            ],
                            bgp=dict(
                                aggregate_timer=10,
                                dampening=dict(
                                    penalty_half_time=1,
                                    reuse_route_val=1,
                                    suppress_route_val=1,
                                    max_suppress=1,
                                ),
                                slow_peer=[
                                    dict(detection=dict(threshold=150))
                                ],
                            ),
                            neighbor=[
                                dict(
                                    activate=True,
                                    address="198.51.100.1",
                                    aigp=dict(
                                        send=dict(
                                            cost_community=dict(
                                                id=100,
                                                poi=dict(
                                                    igp_cost=True,
                                                    transitive=True,
                                                ),
                                            )
                                        )
                                    ),
                                    prefix_list=[
                                        dict(
                                            name="AS65100-PREFIX-OUT",
                                            out="true"
                                        ),
                                    ],
                                    slow_peer=[
                                        dict(detection=dict(threshold=150))
                                    ],
                                    remote_as=10,
                                    route_map=[
                                        dict(
                                            name="test-route", out=True
                                        )
                                    ],
                                    route_server_client=True,
                                )
                            ],
                            network=[
                                dict(
                                    address="198.51.110.10",
                                    mask="255.255.255.255",
                                    backdoor=True,
                                )
                            ],
                        ),
                        dict(
                            afi="ipv4",
                            safi="mdt",
                            bgp=dict(
                                dmzlink_bw=True,
                                dampening=dict(
                                    penalty_half_time=1,
                                    reuse_route_val=10,
                                    suppress_route_val=100,
                                    max_suppress=5,
                                ),
                                soft_reconfig_backup=True,
                            ),
                        ),
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            aggregate_address=[
                                dict(
                                    address="192.0.3.1",
                                    netmask="255.255.255.255",
                                    as_confed_set=True,
                                )
                            ],
                            default_metric=12,
                            distance=dict(external=10, internal=10, local=100),
                            network=[
                                dict(
                                    address="198.51.111.11",
                                    mask="255.255.255.255",
                                    route_map="test",
                                )
                            ],
                            table_map=dict(name="test_tableMap", filter=True),
                        ),
                    ],
                ),
                state="merged",
            )
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_bgp_address_family_replaced(self):
        set_module_args(
            dict(
                config=dict(
                    as_number="65000",
                    address_family=[
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            vrf="blue",
                            aggregate_address=[
                                dict(
                                    address="192.0.2.1",
                                    netmask="255.255.255.255",
                                    as_confed_set=True,
                                )
                            ],
                            bgp=dict(
                                aggregate_timer=10,
                                slow_peer=[
                                    dict(detection=dict(threshold=200))
                                ],
                            ),
                            redistribute=[dict(connected=dict(metric=10))],
                            neighbor=[
                                dict(
                                    address="198.51.110.1",
                                    activate=True,
                                    remote_as=200,
                                    route_map=[
                                        dict(
                                            name="test-replaced-route", out=True
                                        )
                                    ],
                                )
                            ],
                        )
                    ],
                ),
                state="replaced",
            )
        )
        commands = [
            "router bgp 65000",
            "address-family ipv4 multicast vrf blue",
            "no bgp dampening 1 1 1 1",
            "bgp slow-peer detection threshold 200",
            "no neighbor 198.51.100.1 activate",
            "no neighbor 198.51.100.1 remote-as 10",
            "no neighbor 198.51.100.1 aigp send cost-community 100 poi igp-cost transitive",
            "no neighbor 198.51.100.1 route-server-client",
            "no neighbor 198.51.100.1 slow-peer detection threshold 150",
            "no neighbor 198.51.100.1 route-map test-route out",
            "neighbor 198.51.110.1 activate",
            "neighbor 198.51.110.1 remote-as 200",
            "neighbor 198.51.110.1 route-map test-replaced-route out",
            "no network 198.51.110.10 mask 255.255.255.255 backdoor",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_bgp_address_family_replaced_idempotent(self):
        set_module_args(
            dict(
                config=dict(
                    as_number="65000",
                    address_family=[
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            vrf="blue",
                            aggregate_address=[
                                dict(
                                    address="192.0.2.1",
                                    netmask="255.255.255.255",
                                    as_confed_set=True,
                                )
                            ],
                            bgp=dict(
                                aggregate_timer=10,
                                dampening=dict(
                                    penalty_half_time=1,
                                    reuse_route_val=1,
                                    suppress_route_val=1,
                                    max_suppress=1,
                                ),
                                slow_peer=[
                                    dict(detection=dict(threshold=150))
                                ],
                            ),
                            neighbor=[
                                dict(
                                    activate=True,
                                    address="198.51.100.1",
                                    aigp=dict(
                                        send=dict(
                                            cost_community=dict(
                                                id=100,
                                                poi=dict(
                                                    igp_cost=True,
                                                    transitive=True,
                                                ),
                                            )
                                        )
                                    ),
                                    prefix_list=[
                                        dict(
                                            name="AS65100-PREFIX-OUT",
                                            out="true"
                                        ),
                                    ],
                                    slow_peer=[
                                        dict(detection=dict(threshold=150))
                                    ],
                                    remote_as=10,
                                    route_map=[
                                        dict(
                                            name="test-route", out=True
                                        )
                                    ],
                                    route_server_client=True,
                                )
                            ],
                            network=[
                                dict(
                                    address="198.51.110.10",
                                    mask="255.255.255.255",
                                    backdoor=True,
                                )
                            ],
                        ),
                        dict(
                            afi="ipv4",
                            safi="mdt",
                            bgp=dict(
                                dmzlink_bw=True,
                                dampening=dict(
                                    penalty_half_time=1,
                                    reuse_route_val=10,
                                    suppress_route_val=100,
                                    max_suppress=5,
                                ),
                                soft_reconfig_backup=True,
                            ),
                        ),
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            aggregate_address=[
                                dict(
                                    address="192.0.3.1",
                                    netmask="255.255.255.255",
                                    as_confed_set=True,
                                )
                            ],
                            default_metric=12,
                            distance=dict(external=10, internal=10, local=100),
                            network=[
                                dict(
                                    address="198.51.111.11",
                                    mask="255.255.255.255",
                                    route_map="test",
                                )
                            ],
                            table_map=dict(name="test_tableMap", filter=True),
                        ),
                    ],
                ),
                state="replaced",
            )
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_bgp_address_family_overridden_idempotent(self):
        set_module_args(
            dict(
                config=dict(
                    as_number="65000",
                    address_family=[
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            vrf="blue",
                            aggregate_address=[
                                dict(
                                    address="192.0.2.1",
                                    netmask="255.255.255.255",
                                    as_confed_set=True,
                                )
                            ],
                            bgp=dict(
                                aggregate_timer=10,
                                dampening=dict(
                                    penalty_half_time=1,
                                    reuse_route_val=1,
                                    suppress_route_val=1,
                                    max_suppress=1,
                                ),
                                slow_peer=[
                                    dict(detection=dict(threshold=150))
                                ],
                            ),
                            neighbor=[
                                dict(
                                    activate=True,
                                    address="198.51.100.1",
                                    aigp=dict(
                                        send=dict(
                                            cost_community=dict(
                                                id=100,
                                                poi=dict(
                                                    igp_cost=True,
                                                    transitive=True,
                                                ),
                                            )
                                        )
                                    ),
                                    prefix_list=[
                                        dict(
                                            name="AS65100-PREFIX-OUT",
                                            out="true"
                                        ),
                                    ],
                                    slow_peer=[
                                        dict(detection=dict(threshold=150))
                                    ],
                                    remote_as=10,
                                    route_map=[
                                        dict(
                                            name="test-route", out=True
                                        )
                                    ],
                                    route_server_client=True,
                                )
                            ],
                            network=[
                                dict(
                                    address="198.51.110.10",
                                    mask="255.255.255.255",
                                    backdoor=True,
                                )
                            ],
                        ),
                        dict(
                            afi="ipv4",
                            safi="mdt",
                            bgp=dict(
                                dmzlink_bw=True,
                                dampening=dict(
                                    penalty_half_time=1,
                                    reuse_route_val=10,
                                    suppress_route_val=100,
                                    max_suppress=5,
                                ),
                                soft_reconfig_backup=True,
                            ),
                        ),
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            aggregate_address=[
                                dict(
                                    address="192.0.3.1",
                                    netmask="255.255.255.255",
                                    as_confed_set=True,
                                )
                            ],
                            default_metric=12,
                            distance=dict(external=10, internal=10, local=100),
                            network=[
                                dict(
                                    address="198.51.111.11",
                                    mask="255.255.255.255",
                                    route_map="test",
                                )
                            ],
                            table_map=dict(name="test_tableMap", filter=True),
                        ),
                    ],
                ),
                state="overridden",
            )
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_bgp_address_family_deleted(self):
        set_module_args(dict(state="deleted"))
        commands = [
            "router bgp 65000",
            "no address-family ipv4 multicast vrf blue",
            "no address-family ipv4 mdt",
            "no address-family ipv4 multicast",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_bgp_address_family_delete_without_config(self):
        set_module_args(
            dict(
                config=dict(
                    as_number="65000",
                    address_family=[
                        dict(afi="ipv4", safi="multicast"),
                        dict(afi="ipv4", safi="mdt"),
                    ],
                ),
                state="deleted",
            )
        )
        commands = [
            "router bgp 65000",
            "no address-family ipv4 mdt",
            "no address-family ipv4 multicast",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_bgp_address_family_rendered(self):
        set_module_args(
            dict(
                config=dict(
                    as_number="65000",
                    address_family=[
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            vrf="blue",
                            aggregate_address=[
                                dict(
                                    address="192.0.2.1",
                                    netmask="255.255.255.255",
                                    as_confed_set=True,
                                )
                            ],
                            bgp=dict(
                                dampening=dict(
                                    penalty_half_time=1,
                                    reuse_route_val=1,
                                    suppress_route_val=1,
                                    max_suppress=1,
                                )
                            ),
                            neighbor=[
                                dict(
                                    activate=True,
                                    address="198.51.100.1",
                                    aigp=dict(
                                        send=dict(
                                            cost_community=dict(
                                                id=100,
                                                poi=dict(
                                                    igp_cost=True,
                                                    transitive=True,
                                                ),
                                            )
                                        )
                                    ),
                                    slow_peer=[
                                        dict(detection=dict(threshold=150))
                                    ],
                                    remote_as=10,
                                    route_map=[
                                        dict(
                                            name="test-route", out=True
                                        )
                                    ],
                                    route_server_client=True,
                                )
                            ],
                            network=[
                                dict(
                                    address="198.51.110.10",
                                    mask="255.255.255.255",
                                    backdoor=True,
                                )
                            ],
                        ),
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            aggregate_address=[
                                dict(
                                    address="192.0.3.1",
                                    netmask="255.255.255.255",
                                    as_confed_set=True,
                                )
                            ],
                            default_metric=12,
                            distance=dict(external=10, internal=10, local=100),
                            network=[
                                dict(
                                    address="198.51.111.11",
                                    mask="255.255.255.255",
                                    route_map="test",
                                )
                            ],
                            table_map=dict(name="test_tableMap", filter=True),
                        ),
                    ],
                ),
                state="rendered",
            )
        )
        commands = [
            "router bgp 65000",
            "address-family ipv4 multicast vrf blue",
            "bgp dampening 1 1 1 1",
            "neighbor 198.51.100.1 remote-as 10",
            "neighbor 198.51.100.1 activate",
            "neighbor 198.51.100.1 aigp send cost-community 100 poi igp-cost transitive",
            "neighbor 198.51.100.1 route-map test-route out",
            "neighbor 198.51.100.1 route-server-client",
            "neighbor 198.51.100.1 slow-peer detection threshold 150",
            "network 198.51.110.10 mask 255.255.255.255 backdoor",
            "aggregate-address 192.0.2.1 255.255.255.255 as-confed-set",
            "address-family ipv4 multicast",
            "network 198.51.111.11 mask 255.255.255.255 route-map test",
            "aggregate-address 192.0.3.1 255.255.255.255 as-confed-set",
            "default-metric 12",
            "distance bgp 10 10 100",
            "table-map test_tableMap filter",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["rendered"]), sorted(commands))

    def test_ios_bgp_address_family_parsed(self):
        set_module_args(
            dict(
                running_config="router bgp 65000\n address-family ipv4 multicast vrf blue\n bgp aggregate-timer 10\n bgp slow-peer detection threshold 150",
                state="parsed",
            )
        )
        result = self.execute_module(changed=False)
        parsed_list = {
            "address_family": [
                {
                    "afi": "ipv4",
                    "bgp": {
                        "aggregate_timer": 10,
                        "slow_peer": [{"detection": {"threshold": 150}}],
                    },
                    "safi": "multicast",
                    "vrf": "blue",
                }
            ],
            "as_number": "65000",
        }
        self.assertEqual(parsed_list, result["parsed"])
