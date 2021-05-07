#
# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.cisco.ios.tests.unit.compat.mock import patch
from ansible_collections.cisco.ios.plugins.modules import ios_prefix_lists
from ansible_collections.cisco.ios.tests.unit.modules.utils import (
    set_module_args,
)
from .ios_module import TestIosModule, load_fixture


class TestIosPrefixListsModule(TestIosModule):
    module = ios_prefix_lists

    def setUp(self):
        super(TestIosPrefixListsModule, self).setUp()

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
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.prefix_lists.prefix_lists."
            "Prefix_listsFacts.get_prefix_list_data"
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosPrefixListsModule, self).tearDown()
        self.mock_get_resource_connection_config.stop()
        self.mock_get_resource_connection_facts.stop()
        self.mock_edit_config.stop()
        self.mock_get_config.stop()
        self.mock_load_config.stop()
        self.mock_execute_show_command.stop()

    def load_fixtures(self, commands=None):
        def load_from_file(*args, **kwargs):
            return load_fixture("ios_prefix_lists.cfg")

        self.execute_show_command.side_effect = load_from_file

    def test_ios_prefix_lists_merged(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        afi="ipv4",
                        prefix_lists=[
                            dict(
                                entries=[
                                    dict(description="this is merge test"),
                                    dict(
                                        action="deny",
                                        ge=10,
                                        le=15,
                                        prefix="25.0.0.0/8",
                                        sequence=25,
                                    ),
                                ],
                                name="10",
                            ),
                            dict(
                                entries=[
                                    dict(
                                        description="this is for prefix-list"
                                    ),
                                    dict(
                                        action="deny",
                                        ge=10,
                                        le=15,
                                        prefix="35.0.0.0/8",
                                        sequence=5,
                                    ),
                                    dict(
                                        action="deny",
                                        ge=20,
                                        prefix="35.0.0.0/8",
                                        sequence=10,
                                    ),
                                ],
                                name="test_prefix",
                            ),
                        ],
                    ),
                    dict(
                        afi="ipv6",
                        prefix_lists=[
                            dict(
                                entries=[
                                    dict(
                                        description="this is merged ipv6 prefix-list"
                                    ),
                                    dict(
                                        action="deny",
                                        ge=80,
                                        le=100,
                                        prefix="2001:DB8:0:4::/64",
                                        sequence=10,
                                    ),
                                ],
                                name="test_ipv6",
                            )
                        ],
                    ),
                ],
                state="merged",
            )
        )
        commands = [
            "ip prefix-list 10 description this is merge test",
            "ip prefix-list 10 seq 25 deny 25.0.0.0/8 ge 10 le 15",
            "ipv6 prefix-list test_ipv6 description this is merged ipv6 prefix-list",
            "no ipv6 prefix-list test_ipv6 seq 10 deny 2001:DB8:0:4::/64 ge 80",
            "ipv6 prefix-list test_ipv6 seq 10 deny 2001:DB8:0:4::/64 ge 80 le 100",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_prefix_lists_merged_idempotent(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        afi="ipv4",
                        prefix_lists=[
                            dict(
                                entries=[
                                    dict(
                                        description="this is test description"
                                    ),
                                    dict(
                                        action="deny",
                                        le=15,
                                        prefix="1.0.0.0/8",
                                        sequence=5,
                                    ),
                                    dict(
                                        action="deny",
                                        ge=10,
                                        prefix="35.0.0.0/8",
                                        sequence=10,
                                    ),
                                    dict(
                                        action="deny",
                                        ge=15,
                                        prefix="12.0.0.0/8",
                                        sequence=15,
                                    ),
                                    dict(
                                        action="deny",
                                        ge=20,
                                        le=21,
                                        prefix="14.0.0.0/8",
                                        sequence=20,
                                    ),
                                ],
                                name="10",
                            ),
                            dict(
                                entries=[
                                    dict(description="this is test"),
                                    dict(
                                        action="deny",
                                        ge=15,
                                        prefix="12.0.0.0/8",
                                        sequence=50,
                                    ),
                                ],
                                name="test",
                            ),
                            dict(
                                entries=[
                                    dict(
                                        description="this is for prefix-list"
                                    ),
                                    dict(
                                        action="deny",
                                        ge=10,
                                        le=15,
                                        prefix="35.0.0.0/8",
                                        sequence=5,
                                    ),
                                    dict(
                                        action="deny",
                                        ge=20,
                                        prefix="35.0.0.0/8",
                                        sequence=10,
                                    ),
                                ],
                                name="test_prefix",
                            ),
                        ],
                    ),
                    dict(
                        afi="ipv6",
                        prefix_lists=[
                            dict(
                                entries=[
                                    dict(
                                        description="this is ipv6 prefix-list"
                                    ),
                                    dict(
                                        action="deny",
                                        ge=80,
                                        prefix="2001:DB8:0:4::/64",
                                        sequence=10,
                                    ),
                                ],
                                name="test_ipv6",
                            )
                        ],
                    ),
                ],
                state="merged",
            )
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_prefix_lists_replaced(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        afi="ipv4",
                        prefix_lists=[
                            dict(
                                entries=[
                                    dict(description="this is replace test"),
                                    dict(
                                        action="deny",
                                        ge=15,
                                        prefix="12.0.0.0/8",
                                        sequence=15,
                                    ),
                                    dict(
                                        action="deny",
                                        ge=20,
                                        le=21,
                                        prefix="14.0.0.0/8",
                                        sequence=20,
                                    ),
                                ],
                                name="10",
                            ),
                            dict(
                                entries=[
                                    dict(description="this is replace test"),
                                    dict(
                                        action="deny",
                                        ge=20,
                                        prefix="35.0.0.0/8",
                                        sequence=10,
                                    ),
                                ],
                                name="test_replace",
                            ),
                        ],
                    ),
                    dict(
                        afi="ipv6",
                        prefix_lists=[
                            dict(
                                entries=[
                                    dict(
                                        description="this is ipv6 replace test"
                                    ),
                                    dict(
                                        action="deny",
                                        ge=80,
                                        le=100,
                                        prefix="2001:DB8:0:4::/64",
                                        sequence=10,
                                    ),
                                ],
                                name="test_ipv6",
                            )
                        ],
                    ),
                ],
                state="replaced",
            )
        )
        commands = [
            "ip prefix-list 10 description this is replace test",
            "no ip prefix-list 10 seq 10 deny 35.0.0.0/8 ge 10",
            "no ip prefix-list 10 seq 5 deny 1.0.0.0/8 le 15",
            "ip prefix-list test_replace seq 10 deny 35.0.0.0/8 ge 20",
            "ip prefix-list test_replace description this is replace test",
            "no ipv6 prefix-list test_ipv6 seq 10 deny 2001:DB8:0:4::/64 ge 80",
            "ipv6 prefix-list test_ipv6 seq 10 deny 2001:DB8:0:4::/64 ge 80 le 100",
            "ipv6 prefix-list test_ipv6 description this is ipv6 replace test",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_prefix_lists_replaced_idempotent(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        afi="ipv4",
                        prefix_lists=[
                            dict(
                                entries=[
                                    dict(
                                        description="this is test description"
                                    ),
                                    dict(
                                        action="deny",
                                        le=15,
                                        prefix="1.0.0.0/8",
                                        sequence=5,
                                    ),
                                    dict(
                                        action="deny",
                                        ge=10,
                                        prefix="35.0.0.0/8",
                                        sequence=10,
                                    ),
                                    dict(
                                        action="deny",
                                        ge=15,
                                        prefix="12.0.0.0/8",
                                        sequence=15,
                                    ),
                                    dict(
                                        action="deny",
                                        ge=20,
                                        le=21,
                                        prefix="14.0.0.0/8",
                                        sequence=20,
                                    ),
                                ],
                                name="10",
                            ),
                            dict(
                                entries=[
                                    dict(description="this is test"),
                                    dict(
                                        action="deny",
                                        ge=15,
                                        prefix="12.0.0.0/8",
                                        sequence=50,
                                    ),
                                ],
                                name="test",
                            ),
                            dict(
                                entries=[
                                    dict(
                                        description="this is for prefix-list"
                                    ),
                                    dict(
                                        action="deny",
                                        ge=10,
                                        le=15,
                                        prefix="35.0.0.0/8",
                                        sequence=5,
                                    ),
                                    dict(
                                        action="deny",
                                        ge=20,
                                        prefix="35.0.0.0/8",
                                        sequence=10,
                                    ),
                                ],
                                name="test_prefix",
                            ),
                        ],
                    ),
                    dict(
                        afi="ipv6",
                        prefix_lists=[
                            dict(
                                entries=[
                                    dict(
                                        description="this is ipv6 prefix-list"
                                    ),
                                    dict(
                                        action="deny",
                                        ge=80,
                                        prefix="2001:DB8:0:4::/64",
                                        sequence=10,
                                    ),
                                ],
                                name="test_ipv6",
                            )
                        ],
                    ),
                ],
                state="merged",
            )
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_prefix_lists_overridden(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        afi="ipv4",
                        prefix_lists=[
                            dict(
                                entries=[
                                    dict(description="this is override test"),
                                    dict(
                                        action="deny",
                                        ge=15,
                                        prefix="12.0.0.0/8",
                                        sequence=15,
                                    ),
                                    dict(
                                        action="deny",
                                        ge=20,
                                        le=21,
                                        prefix="14.0.0.0/8",
                                        sequence=20,
                                    ),
                                ],
                                name="10",
                            ),
                            dict(
                                entries=[
                                    dict(description="this is override test"),
                                    dict(
                                        action="deny",
                                        ge=20,
                                        prefix="35.0.0.0/8",
                                        sequence=10,
                                    ),
                                ],
                                name="test_override",
                            ),
                        ],
                    ),
                    dict(
                        afi="ipv6",
                        prefix_lists=[
                            dict(
                                entries=[
                                    dict(
                                        description="this is ipv6 override test"
                                    ),
                                    dict(
                                        action="deny",
                                        ge=80,
                                        le=100,
                                        prefix="2001:DB8:0:4::/64",
                                        sequence=10,
                                    ),
                                ],
                                name="test_ipv6",
                            )
                        ],
                    ),
                ],
                state="overridden",
            )
        )
        commands = [
            "no ip prefix-list test",
            "no ip prefix-list test_prefix",
            "ip prefix-list 10 description this is override test",
            "no ip prefix-list 10 seq 10 deny 35.0.0.0/8 ge 10",
            "no ip prefix-list 10 seq 5 deny 1.0.0.0/8 le 15",
            "ip prefix-list test_override seq 10 deny 35.0.0.0/8 ge 20",
            "ip prefix-list test_override description this is override test",
            "no ipv6 prefix-list test_ipv6 seq 10 deny 2001:DB8:0:4::/64 ge 80",
            "ipv6 prefix-list test_ipv6 seq 10 deny 2001:DB8:0:4::/64 ge 80 le 100",
            "ipv6 prefix-list test_ipv6 description this is ipv6 override test",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_prefix_lists_overridden_idempotent(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        afi="ipv4",
                        prefix_lists=[
                            dict(
                                entries=[
                                    dict(
                                        description="this is test description"
                                    ),
                                    dict(
                                        action="deny",
                                        le=15,
                                        prefix="1.0.0.0/8",
                                        sequence=5,
                                    ),
                                    dict(
                                        action="deny",
                                        ge=10,
                                        prefix="35.0.0.0/8",
                                        sequence=10,
                                    ),
                                    dict(
                                        action="deny",
                                        ge=15,
                                        prefix="12.0.0.0/8",
                                        sequence=15,
                                    ),
                                    dict(
                                        action="deny",
                                        ge=20,
                                        le=21,
                                        prefix="14.0.0.0/8",
                                        sequence=20,
                                    ),
                                ],
                                name="10",
                            ),
                            dict(
                                entries=[
                                    dict(description="this is test"),
                                    dict(
                                        action="deny",
                                        ge=15,
                                        prefix="12.0.0.0/8",
                                        sequence=50,
                                    ),
                                ],
                                name="test",
                            ),
                            dict(
                                entries=[
                                    dict(
                                        description="this is for prefix-list"
                                    ),
                                    dict(
                                        action="deny",
                                        ge=10,
                                        le=15,
                                        prefix="35.0.0.0/8",
                                        sequence=5,
                                    ),
                                    dict(
                                        action="deny",
                                        ge=20,
                                        prefix="35.0.0.0/8",
                                        sequence=10,
                                    ),
                                ],
                                name="test_prefix",
                            ),
                        ],
                    ),
                    dict(
                        afi="ipv6",
                        prefix_lists=[
                            dict(
                                entries=[
                                    dict(
                                        description="this is ipv6 prefix-list"
                                    ),
                                    dict(
                                        action="deny",
                                        ge=80,
                                        prefix="2001:DB8:0:4::/64",
                                        sequence=10,
                                    ),
                                ],
                                name="test_ipv6",
                            )
                        ],
                    ),
                ],
                state="merged",
            )
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_prefix_lists_deleted_by_afi(self):
        set_module_args(dict(config=[dict(afi="ipv4")], state="deleted"))
        commands = [
            "no ip prefix-list test",
            "no ip prefix-list 10",
            "no ip prefix-list test_prefix",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_prefix_lists_delete_without_config(self):
        set_module_args(dict(state="deleted"))
        commands = [
            "no ip prefix-list test",
            "no ip prefix-list 10",
            "no ip prefix-list test_prefix",
            "no ipv6 prefix-list test_ipv6",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_prefix_lists_rendered(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        afi="ipv4",
                        prefix_lists=[
                            dict(
                                entries=[
                                    dict(description="this is merge test"),
                                    dict(
                                        action="deny",
                                        ge=10,
                                        le=15,
                                        prefix="25.0.0.0/8",
                                        sequence=25,
                                    ),
                                ],
                                name="10",
                            ),
                            dict(
                                entries=[
                                    dict(
                                        description="this is for prefix-list"
                                    ),
                                    dict(
                                        action="deny",
                                        ge=10,
                                        le=15,
                                        prefix="35.0.0.0/8",
                                        sequence=5,
                                    ),
                                    dict(
                                        action="deny",
                                        ge=20,
                                        prefix="35.0.0.0/8",
                                        sequence=10,
                                    ),
                                ],
                                name="test_prefix",
                            ),
                        ],
                    ),
                    dict(
                        afi="ipv6",
                        prefix_lists=[
                            dict(
                                entries=[
                                    dict(
                                        description="this is ipv6 prefix-list"
                                    ),
                                    dict(
                                        action="deny",
                                        ge=80,
                                        le=100,
                                        prefix="2001:DB8:0:4::/64",
                                        sequence=10,
                                    ),
                                ],
                                name="test_ipv6",
                            )
                        ],
                    ),
                ],
                state="rendered",
            )
        )
        commands = [
            "ip prefix-list 10 description this is merge test",
            "ip prefix-list 10 seq 25 deny 25.0.0.0/8 ge 10 le 15",
            "ip prefix-list test_prefix description this is for prefix-list",
            "ip prefix-list test_prefix seq 5 deny 35.0.0.0/8 ge 10 le 15",
            "ip prefix-list test_prefix seq 10 deny 35.0.0.0/8 ge 20",
            "ipv6 prefix-list test_ipv6 description this is ipv6 prefix-list",
            "ipv6 prefix-list test_ipv6 seq 10 deny 2001:DB8:0:4::/64 ge 80 le 100",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["rendered"]), sorted(commands))
