#
# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.cisco.ios.tests.unit.compat.mock import patch
from ansible_collections.cisco.ios.plugins.modules import ios_l3_interfaces
from ansible_collections.cisco.ios.tests.unit.modules.utils import (
    set_module_args,
)
from .ios_module import TestIosModule, load_fixture


class TestIosL3InterfacesModule(TestIosModule):
    module = ios_l3_interfaces

    def setUp(self):
        super(TestIosL3InterfacesModule, self).setUp()

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
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.facts.facts."
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
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.l3_interfaces.l3_interfaces."
            "L3_InterfacesFacts.get_l3_interfaces_data"
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosL3InterfacesModule, self).tearDown()
        self.mock_get_resource_connection_config.stop()
        self.mock_get_resource_connection_facts.stop()
        self.mock_edit_config.stop()
        self.mock_get_config.stop()
        self.mock_load_config.stop()
        self.mock_execute_show_command.stop()

    def load_fixtures(self, commands=None):
        def load_from_file(*args, **kwargs):
            return load_fixture("ios_l3_interfaces.cfg")

        self.execute_show_command.side_effect = load_from_file

    def test_ios_l3_interfaces_merged(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="loopback888", ipv4=[dict(address="192.0.3.1/24")]
                    ),
                    dict(
                        name="loopback100", ipv4=[dict(address="192.0.1.1/24")]
                    ),
                    dict(
                        name="GigabitEthernet0/1",
                        ipv4=[dict(address="198.51.100.2/24", secondary=True)],
                        ipv6=[dict(address="autoconfig")],
                    ),
                    dict(
                        name="GigabitEthernet0/2",
                        ipv6=[dict(address="2001:DB8:0:1::/64")],
                    ),
                ],
                state="merged",
            )
        )
        commands = [
            "interface loopback888",
            "ip address 192.0.3.1 255.255.255.0",
            "interface loopback100",
            "ip address 192.0.1.1 255.255.255.0",
            "interface GigabitEthernet0/1",
            "ip address 198.51.100.2 255.255.255.0 secondary",
            "ipv6 address autoconfig",
            "interface GigabitEthernet0/2",
            "ipv6 address 2001:DB8:0:1::/64",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_l3_interfaces_merged_idempotent(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Loopback888", ipv4=[dict(address="192.0.1.1/24")]
                    ),
                    dict(
                        name="GigabitEthernet0/1",
                        ipv4=[dict(address="192.0.2.1/24")],
                        ipv6=[dict(address="2001:db8:0:3::/64")],
                    ),
                    dict(
                        name="GigabitEthernet0/2",
                        ipv4=[
                            dict(address="198.51.100.1/24"),
                            dict(address="198.51.100.2/24", secondary=True),
                        ],
                    ),
                ],
                state="merged",
            )
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_l3_interfaces_replaced(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="GigabitEthernet0/2",
                        ipv4=[dict(address="192.0.2.1/24")],
                    ),
                    dict(
                        name="GigabitEthernet0/3",
                        ipv4=[
                            dict(
                                address="dhcp",
                                dhcp_client=2,
                                dhcp_hostname="test.com",
                            )
                        ],
                    ),
                    dict(
                        name="GigabitEthernet0/3.100",
                        ipv4=[dict(address="198.51.100.3/24", secondary=True)],
                    ),
                ],
                state="replaced",
            )
        )
        commands = [
            "interface GigabitEthernet0/2",
            "ip address 192.0.2.1 255.255.255.0",
            "interface GigabitEthernet0/3.100",
            "ip address 198.51.100.3 255.255.255.0 secondary",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_l3_interfaces_replaced_idempotent(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Loopback888", ipv4=[dict(address="192.0.1.1/24")]
                    ),
                    dict(
                        name="GigabitEthernet0/1",
                        ipv4=[dict(address="192.0.2.1/24")],
                        ipv6=[dict(address="2001:db8:0:3::/64")],
                    ),
                    dict(
                        name="GigabitEthernet0/2",
                        ipv4=[
                            dict(address="198.51.100.1/24"),
                            dict(address="198.51.100.2/24", secondary=True),
                        ],
                    ),
                ],
                state="replaced",
            )
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_l3_interfaces_overridden(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="GigabitEthernet0/2",
                        ipv4=[dict(address="192.0.2.1/24")],
                    )
                ],
                state="overridden",
            )
        )
        commands = [
            "interface loopback888",
            "no ip address",
            "interface GigabitEthernet0/1",
            "no ip address",
            "no ipv6 address",
            "interface GigabitEthernet0/2",
            "ip address 192.0.2.1 255.255.255.0",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_l3_interfaces_overridden_idempotent(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Loopback888", ipv4=[dict(address="192.0.1.1/24")]
                    ),
                    dict(
                        name="GigabitEthernet0/1",
                        ipv4=[dict(address="192.0.2.1/24")],
                        ipv6=[dict(address="2001:db8:0:3::/64")],
                    ),
                    dict(
                        name="GigabitEthernet0/2",
                        ipv4=[
                            dict(address="198.51.100.1/24"),
                            dict(address="198.51.100.2/24", secondary=True),
                        ],
                    ),
                ],
                state="overridden",
            )
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_l3_interfaces_deleted_interface(self):
        set_module_args(
            dict(config=[dict(name="GigabitEthernet0/1")], state="deleted")
        )
        commands = [
            "interface GigabitEthernet0/1",
            "no ip address",
            "no ipv6 address",
        ]
        self.execute_module(changed=True, commands=commands)

    def test_ios_l3_interfaces_deleted_all(self):
        set_module_args(dict(config=[], state="deleted"))
        commands = [
            "interface loopback888",
            "no ip address",
            "interface GigabitEthernet0/1",
            "no ip address",
            "no ipv6 address",
            "interface GigabitEthernet0/2",
            "no ip address",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_l3_interfaces_parsed(self):
        set_module_args(
            dict(
                running_config="interface GigabitEthernet0/1\nip address 192.0.2.1/24\nipv6 address 2001:db8:0:3::/64",
                state="parsed",
            )
        )
        result = self.execute_module(changed=False)
        parsed_list = [
            {
                "ipv4": [{"address": "192.0.2.1/24"}],
                "ipv6": [{"address": "2001:db8:0:3::/64"}],
                "name": "GigabitEthernet0/1",
            }
        ]
        self.assertEqual(parsed_list, result["parsed"])

    def test_ios_l3_interfaces_rendered(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="loopback888", ipv4=[dict(address="192.0.3.1/24")]
                    ),
                    dict(
                        name="GigabitEthernet0/1",
                        ipv4=[
                            dict(address="198.51.100.1/24"),
                            dict(address="198.51.100.2/24", secondary=True),
                        ],
                    ),
                    dict(
                        name="GigabitEthernet0/2",
                        ipv6=[dict(address="2001:DB8:0:1::/64")],
                    ),
                ],
                state="rendered",
            )
        )
        commands = [
            "interface loopback888",
            "ip address 192.0.3.1 255.255.255.0",
            "interface GigabitEthernet0/1",
            "ip address 198.51.100.1 255.255.255.0",
            "ip address 198.51.100.2 255.255.255.0 secondary",
            "interface GigabitEthernet0/2",
            "ipv6 address 2001:DB8:0:1::/64",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(result["rendered"], commands)
