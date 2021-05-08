#
# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from textwrap import dedent
from ansible_collections.cisco.ios.tests.unit.compat.mock import patch
from ansible_collections.cisco.ios.plugins.modules import ios_logging_global
from ansible_collections.cisco.ios.tests.unit.modules.utils import (
    set_module_args,
)
from .ios_module import TestIosModule


class TestIosLoggingGlobalModule(TestIosModule):
    module = ios_logging_global

    def setUp(self):
        super(TestIosLoggingGlobalModule, self).setUp()

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
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.logging_global.logging_global."
            "Logging_globalFacts.get_logging_data"
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosLoggingGlobalModule, self).tearDown()
        self.mock_get_resource_connection_config.stop()
        self.mock_get_resource_connection_facts.stop()
        self.mock_edit_config.stop()
        self.mock_get_config.stop()
        self.mock_load_config.stop()
        self.mock_execute_show_command.stop()
        self.allCommands = [
            "logging on",
            "logging buffered xml 5099 notifications",
            "logging buginf",
            "logging cns-events warnings",
            "logging console xml critical",
            "logging count",
            "logging delimiter tcp",
            "logging discriminator msglog01 severity includes 5",
            "logging dmvpn rate-limit 10",
            "logging esm config",
            "logging exception 4099",
            "logging facility local5",
            "logging filter tftp://172.16.2.18/ESM/elate.tcl args TESTInst2",
            "logging filter tftp://172.16.2.14/ESM/escalate.tcl args TESTInst",
            "logging history alerts",
            "logging host 172.16.1.1",
            "logging host 172.16.1.11 xml",
            "logging host 172.16.1.25 filtered",
            "logging host 172.16.1.10 filtered stream 10",
            "logging host 172.16.1.13 transport tcp port 514",
            "logging message-counter log",
            "logging message-counter debug",
            "logging monitor warnings",
            "logging origin-id hostname",
            "logging persistent batch 4444",
            "logging policy-firewall rate-limit 10",
            "logging queue-limit esm 150",
            "logging rate-limit all 2",
            "logging reload alerts",
            "logging server-arp",
            "logging snmp-trap errors",
            "logging source-interface GBit1/0",
            "logging source-interface CTunnel2",
            "logging trap errors",
            "logging userinfo",
        ]

    def test_ios_logging_global_merged_idempotent(self):
        """
        passing all commands as have and expecting [] commands
        """
        self.execute_show_command.return_value = dedent(
            """\
            logging on
            logging count
            logging buginf
            logging userinfo
            logging esm config
            logging server-arp
            logging trap errors
            logging delimiter tcp
            logging reload alerts
            logging host 172.16.1.1
            logging exception 4099
            logging history alerts
            logging facility local5
            logging snmp-trap errors
            logging monitor warnings
            logging origin-id hostname
            logging host 172.16.1.11 xml
            logging cns-events warnings
            logging queue-limit esm 150
            logging dmvpn rate-limit 10
            logging message-counter log
            logging console xml critical
            logging message-counter debug
            logging persistent batch 4444
            logging host 172.16.1.25 filtered
            logging source-interface GBit1/0
            logging source-interface CTunnel2
            logging policy-firewall rate-limit 10
            logging buffered xml 5099 notifications
            logging rate-limit all 2 except warnings
            logging host 172.16.1.10 filtered stream 10
            logging host 172.16.1.13 transport tcp port 514
            logging discriminator msglog01 severity includes 5
            logging filter tftp://172.16.2.18/ESM/elate.tcl args TESTInst2
            logging filter tftp://172.16.2.14/ESM/escalate.tcl args TESTInst
            """
        )
        playbook = dict(
            config=[
                dict(logging_on="enable"),
                dict(
                    buffered=dict(
                        size=5099, severity="notifications", xml=True
                    )
                ),
                dict(buginf=True),
                dict(cns_events="warnings"),
                dict(console=dict(severity="critical", xml=True)),
                dict(count=True),
                dict(delimiter=dict(tcp=True)),
                dict(discriminator=["msglog01 severity includes 5"]),
                dict(dmvpn=dict(rate_limit=10)),
                dict(esm=dict(config=True)),
                dict(exception=4099),
                dict(facility="local5"),
                dict(
                    filter=[
                        dict(
                            url="tftp://172.16.2.18/ESM/elate.tcl",
                            args="TESTInst2",
                        ),
                        dict(
                            url="tftp://172.16.2.14/ESM/escalate.tcl",
                            args="TESTInst",
                        ),
                    ]
                ),
                dict(history=dict(severity="alerts")),
                dict(
                    hosts=[
                        dict(hostname="172.16.1.1"),
                        dict(hostname="172.16.1.11", xml=True),
                        dict(hostname="172.16.1.25", filtered=True),
                        dict(hostname="172.16.1.10", stream=10, filtered=True),
                        dict(
                            hostname="172.16.1.13",
                            transport=dict(tcp=dict(port=514)),
                        ),
                    ]
                ),
                dict(message_counter=["log", "debug"]),
                dict(monitor=dict(severity="warnings")),
                dict(origin_id=dict(tag="hostname")),
                dict(persistent=dict(batch=4444)),
                dict(policy_firewall=dict(rate_limit=10)),
                dict(queue_limit=dict(esm=150)),
                dict(
                    rate_limit=dict(
                        all=True, size=2, except_severity="warnings"
                    )
                ),
                dict(reload=dict(severity="alerts")),
                dict(server_arp=True),
                dict(snmp_trap=["errors"]),
                dict(
                    source_interface=[
                        dict(interface="GBit1/0"),
                        dict(interface="CTunnel2"),
                    ]
                ),
                dict(trap="errors"),
                dict(userinfo=True),
            ]
        )
        merged = []
        playbook["state"] = "merged"
        set_module_args(playbook)
        result = self.execute_module()

        self.maxDiff = None
        self.assertEqual(sorted(result["commands"]), sorted(merged))

    def test_ios_logging_global_deleted(self):
        self.execute_show_command.return_value = dedent(
            """\
            logging on
            logging count
            logging buginf
            logging buffered xml 5099 notifications
            logging console xml critical
            logging delimiter tcp
            logging dmvpn rate-limit 10
            logging esm config
            logging exception 4099
            logging facility local5
            logging history alerts
            logging monitor warnings
            logging origin-id hostname
            logging persistent batch 4444
            logging policy-firewall rate-limit 10
            logging queue-limit esm 150
            logging rate-limit all 2 except warnings
            logging server-arp
            logging reload alerts
            logging userinfo
            logging trap errors
            """
        )
        playbook = dict(
            config=[
                dict(logging_on="enable"),
                dict(count=True),
                dict(
                    buffered=dict(
                        size=5099, severity="notifications", xml=True
                    )
                ),
                dict(buginf=True),
                dict(console=dict(severity="critical", xml=True)),
                dict(delimiter=dict(tcp=True)),
                dict(dmvpn=dict(rate_limit=10)),
                dict(esm=dict(config=True)),
                dict(exception=4099),
                dict(facility="local5"),
                dict(history=dict(severity="alerts")),
                dict(monitor=dict(severity="warnings")),
                dict(origin_id=dict(tag="hostname")),
                dict(persistent=dict(batch=4444)),
                dict(policy_firewall=dict(rate_limit=10)),
                dict(queue_limit=dict(esm=150)),
                dict(
                    rate_limit=dict(
                        all=True, size=2, except_severity="warnings"
                    )
                ),
                dict(reload=dict(severity="alerts")),
                dict(server_arp=True),
                dict(trap="errors"),
                dict(userinfo=True),
            ]
        )
        deleted = [
            "no logging on",
            "no logging count",
            "no logging buginf",
            "no logging buffered xml 5099 notifications",
            "no logging console xml critical",
            "no logging delimiter tcp",
            "no logging dmvpn rate-limit 10",
            "no logging esm config",
            "no logging exception 4099",
            "no logging facility local5",
            "no logging history alerts",
            "no logging monitor warnings",
            "no logging origin-id hostname",
            "no logging persistent batch 4444",
            "no logging policy-firewall rate-limit 10",
            "no logging queue-limit esm 150",
            "no logging rate-limit all 2 except warnings",
            "no logging server-arp",
            "no logging reload alerts",
            "no logging userinfo",
            "no logging trap errors",
        ]
        playbook["state"] = "deleted"
        set_module_args(playbook)
        result = self.execute_module(changed=True)

        self.maxDiff = None
        self.assertEqual(sorted(result["commands"]), sorted(deleted))

    def test_ios_logging_global_deleted_list(self):
        self.execute_show_command.return_value = dedent(
            """\
            logging discriminator msglog01 severity includes 5
            logging filter tftp://172.16.2.18/ESM/elate.tcl args TESTInst2
            logging filter tftp://172.16.2.14/ESM/escalate.tcl args TESTInst
            logging host 172.16.1.1
            logging host 172.16.1.11 xml
            logging host 172.16.1.25 filtered
            logging host 172.16.1.10 filtered stream 10
            logging host 172.16.1.13 transport tcp port 514
            logging message-counter log
            logging message-counter debug
            logging snmp-trap errors
            logging source-interface GBit1/0
            logging source-interface CTunnel2
            """
        )
        playbook = dict(
            config=[
                dict(discriminator=["msglog01 severity includes 5"]),
                dict(
                    filter=[
                        dict(
                            url="tftp://172.16.2.18/ESM/elate.tcl",
                            args="TESTInst2",
                        ),
                        dict(
                            url="tftp://172.16.2.14/ESM/escalate.tcl",
                            args="TESTInst",
                        ),
                    ]
                ),
                dict(
                    hosts=[
                        dict(hostname="172.16.1.1"),
                        dict(hostname="172.16.1.11", xml=True),
                        dict(hostname="172.16.1.25", filtered=True),
                        dict(hostname="172.16.1.10", stream=10, filtered=True),
                        dict(
                            hostname="172.16.1.13",
                            transport=dict(tcp=dict(port=514)),
                        ),
                    ]
                ),
                dict(message_counter=["log", "debug"]),
                dict(snmp_trap=["errors"]),
                dict(
                    source_interface=[
                        dict(interface="GBit1/0"),
                        dict(interface="CTunnel2"),
                    ]
                ),
            ]
        )
        deleted = [
            "no logging discriminator msglog01 severity includes 5",
            "no logging filter tftp://172.16.2.18/ESM/elate.tcl args TESTInst2",
            "no logging filter tftp://172.16.2.14/ESM/escalate.tcl args TESTInst",
            "no logging host 172.16.1.1",
            "no logging host 172.16.1.11",
            "no logging host 172.16.1.25",
            "no logging host 172.16.1.10",
            "no logging host 172.16.1.13",
            "no logging message-counter log",
            "no logging message-counter debug",
            "no logging snmp-trap errors",
            "no logging source-interface GBit1/0",
            "no logging source-interface CTunnel2",
        ]
        playbook["state"] = "deleted"
        set_module_args(playbook)
        result = self.execute_module(changed=True)
        self.maxDiff = None
        self.assertEqual(sorted(result["commands"]), sorted(deleted))

    def test_ios_logging_global_overridden(self):
        self.execute_show_command.return_value = dedent(
            """\
            logging on
            logging count
            logging buginf
            logging buffered xml 5099 notifications
            logging console xml critical
            logging delimiter tcp
            logging dmvpn rate-limit 10
            logging esm config
            logging exception 4099
            logging facility local5
            logging history alerts
            logging monitor warnings
            logging origin-id hostname
            logging persistent batch 4444
            logging policy-firewall rate-limit 10
            logging queue-limit esm 150
            logging rate-limit all 2 except warnings
            logging server-arp
            logging reload alerts
            logging userinfo
            logging trap errors
            """
        )
        playbook = dict(
            config=[
                dict(discriminator=["msglog01 severity includes 5"]),
                dict(
                    filter=[
                        dict(
                            url="tftp://172.16.2.18/ESM/elate.tcl",
                            args="TESTInst2",
                        ),
                        dict(
                            url="tftp://172.16.2.14/ESM/escalate.tcl",
                            args="TESTInst",
                        ),
                    ]
                ),
                dict(
                    hosts=[
                        dict(hostname="172.16.1.1"),
                        dict(hostname="172.16.1.11", xml=True),
                        dict(hostname="172.16.1.25", filtered=True),
                        dict(hostname="172.16.1.10", stream=10, filtered=True),
                        dict(
                            hostname="172.16.1.13",
                            transport=dict(tcp=dict(port=514)),
                        ),
                    ]
                ),
                dict(message_counter=["log", "debug"]),
                dict(snmp_trap=["errors"]),
                dict(
                    source_interface=[
                        dict(interface="GBit1/0"),
                        dict(interface="CTunnel2"),
                    ]
                ),
            ]
        )
        overridden = [
            "no logging on",
            "no logging count",
            "no logging buginf",
            "no logging buffered xml 5099 notifications",
            "no logging console xml critical",
            "no logging delimiter tcp",
            "no logging dmvpn rate-limit 10",
            "no logging esm config",
            "no logging exception 4099",
            "no logging facility local5",
            "no logging history alerts",
            "no logging monitor warnings",
            "no logging origin-id hostname",
            "no logging persistent batch 4444",
            "no logging policy-firewall rate-limit 10",
            "no logging queue-limit esm 150",
            "no logging rate-limit all 2 except warnings",
            "no logging server-arp",
            "no logging reload alerts",
            "no logging userinfo",
            "no logging trap errors",
            "logging discriminator msglog01 severity includes 5",
            "logging filter tftp://172.16.2.18/ESM/elate.tcl args TESTInst2",
            "logging filter tftp://172.16.2.14/ESM/escalate.tcl args TESTInst",
            "logging host 172.16.1.1",
            "logging host 172.16.1.11 xml",
            "logging host 172.16.1.25 filtered",
            "logging host 172.16.1.10 filtered stream 10",
            "logging host 172.16.1.13 transport tcp port 514",
            "logging message-counter log",
            "logging message-counter debug",
            "logging snmp-trap errors",
            "logging source-interface GBit1/0",
            "logging source-interface CTunnel2",
        ]
        playbook["state"] = "overridden"
        set_module_args(playbook)
        result = self.execute_module(changed=True)
        self.maxDiff = None
        self.assertEqual(sorted(result["commands"]), sorted(overridden))

    def test_ios_logging_global_merged(self):
        self.execute_show_command.return_value = dedent(
            """\
            logging host 172.16.1.1
            """
        )
        playbook = dict(
            config=[
                dict(
                    hosts=[
                        dict(
                            hostname="172.16.2.15",
                            session_id=dict(text="Test"),
                        ),
                        dict(
                            ipv6="2001:0db8:85a3:0000:0000:8a2e:0370:7304",
                            discriminator="msglog01 severity includes 5",
                        ),
                        dict(
                            ipv6="2001:0db8:85a3:0000:0000:8a2e:0370:7314",
                            sequence_num_session=True,
                        ),
                        dict(
                            ipv6="2001:0db8:85a3:0000:0000:8a2e:0370:7324",
                            vrf="vpn1",
                        ),
                        dict(
                            ipv6="2001:0db8:85a3:0000:0000:8a2e:0370:7334",
                            stream=10,
                            filtered=True,
                        ),
                        dict(
                            ipv6="2001:0db8:85a3:0000:0000:8a2e:0370:7344",
                            session_id=dict(tag="ipv4"),
                        ),
                        dict(
                            ipv6="2001:0db8:85a3:0000:0000:8a2e:0370:7354",
                            transport=dict(tcp=dict(port=514, xml=True)),
                        ),
                        dict(
                            ipv6="2001:0db8:85a3:0000:0000:8a2e:0370:7374",
                            vrf="Apn2",
                            transport=dict(
                                udp=dict(
                                    discriminator="msglog01 severity includes 5"
                                )
                            ),
                        ),
                        dict(
                            ipv6="2001:0db8:85a3:0000:0000:8a2e:0370:7384",
                            transport=dict(
                                udp=dict(sequence_num_session=True)
                            ),
                        ),
                        dict(
                            ipv6="2001:0db8:85a3:0000:0000:8a2e:0370:7364",
                            transport=dict(
                                tcp=dict(
                                    audit=True,
                                    filtered=True,
                                    stream=10,
                                    session_id=dict(text="Test"),
                                )
                            ),
                        ),
                    ]
                )
            ]
        )
        merged = [
            "logging host 172.16.2.15 session-id string Test",
            "logging host ipv6 2001:0db8:85a3:0000:0000:8a2e:0370:7304 discriminator msglog01 severity includes 5",
            "logging host ipv6 2001:0db8:85a3:0000:0000:8a2e:0370:7314 sequence-num-session",
            "logging host ipv6 2001:0db8:85a3:0000:0000:8a2e:0370:7324 vrf vpn1",
            "logging host ipv6 2001:0db8:85a3:0000:0000:8a2e:0370:7334 filtered stream 10",
            "logging host ipv6 2001:0db8:85a3:0000:0000:8a2e:0370:7344 session-id ipv4",
            "logging host ipv6 2001:0db8:85a3:0000:0000:8a2e:0370:7354 transport tcp port 514 xml",
            "logging host ipv6 2001:0db8:85a3:0000:0000:8a2e:0370:7364 transport tcp audit filtered stream 10 session-id string Test",
            "logging host ipv6 2001:0db8:85a3:0000:0000:8a2e:0370:7374 vrf Apn2 transport udp discriminator msglog01 severity includes 5",
            "logging host ipv6 2001:0db8:85a3:0000:0000:8a2e:0370:7384 transport udp sequence-num-session",
        ]
        playbook["state"] = "merged"
        set_module_args(playbook)
        result = self.execute_module(changed=True)

        self.maxDiff = None
        self.assertEqual(sorted(result["commands"]), sorted(merged))

    def test_ios_logging_global_parsed(self):
        set_module_args(
            dict(
                running_config=dedent(
                    """\
                    logging on
                    logging buffered xml 5099 notifications
                    logging buginf
                    logging cns-events warnings
                    logging console xml critical
                    logging count
                    logging delimiter tcp
                    """
                ),
                state="parsed",
            )
        )
        parsed = [
            dict(
                logging_on="enable",
                buffered=dict(size=5099, severity="notifications", xml=True),
                buginf=True,
                cns_events="warnings",
                console=dict(severity="critical", xml=True),
                count=True,
                delimiter=dict(tcp=True),
            )
        ]
        result = self.execute_module(changed=False)

        self.maxDiff = None
        self.assertEqual(sorted(result["parsed"][0]), sorted(parsed[0]))

    def test_ios_logging_global_gathered(self):
        self.execute_show_command.return_value = dedent(
            """\
            logging persistent notify
            """
        )
        set_module_args(dict(state="gathered"))
        gathered = [dict(persistent=dict(notify=True))]
        result = self.execute_module(changed=False)

        self.maxDiff = None
        self.assertEqual(sorted(result["gathered"]), sorted(gathered))

    def test_ios_logging_global_gathered_host(self):
        self.execute_show_command.return_value = dedent(
            """\
            logging host 172.16.1.1 vrf vpn1 transport tcp audit
            """
        )
        set_module_args(dict(state="gathered"))
        gathered = [
            dict(
                hosts=[
                    dict(
                        hostname="172.16.1.1",
                        vrf="vpn1",
                        transport=dict(tcp=dict(audit=True)),
                    )
                ]
            )
        ]
        result = self.execute_module(changed=False)

        self.maxDiff = None
        self.assertEqual(sorted(result["gathered"]), sorted(gathered))

    def test_ios_logging_global_rendered(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        rate_limit=dict(
                            console=True, size=2, except_severity="warnings"
                        )
                    ),
                    dict(reload=dict(message_limit=10, severity="alerts")),
                    dict(
                        persistent=dict(
                            url="flash0:172.16.0.1",
                            threshold=2,
                            immediate=True,
                            protected=True,
                            notify=True,
                        )
                    ),
                    dict(queue_limit=dict(trap=1000)),
                    dict(
                        buffered=dict(
                            discriminator="notifications", filtered=True
                        )
                    ),
                    dict(
                        hosts=[
                            dict(
                                ipv6="2001:0db8:85a3:0000:0000:8a2e:0370:7364",
                                transport=dict(
                                    tcp=dict(session_id=dict(tag="hostname"))
                                ),
                            )
                        ]
                    ),
                ],
                state="rendered",
            )
        )
        rendered = [
            "logging reload message-limit 10 alerts",
            "logging rate-limit console 2 except warnings",
            "logging buffered discriminator notifications filtered",
            "logging persistent url flash0:172.16.0.1 threshold 2 immediate protected notify",
            "logging queue-limit trap 1000",
            "logging host ipv6 2001:0db8:85a3:0000:0000:8a2e:0370:7364 transport tcp session-id hostname",
        ]
        result = self.execute_module(changed=False)
        self.maxDiff = None
        self.assertEqual(sorted(result["rendered"]), sorted(rendered))

    def test_ios_logging_global_deleted_empty(self):
        self.execute_show_command.return_value = dedent(
            """\
            logging rate-limit all 2 except warnings
            logging server-arp
            logging origin-id string Test
            logging reload alerts
            logging userinfo
            logging trap errors
            logging host ipv6 2001:0db8:85a3:0000:0000:8a2e:0370:7324
            logging persistent size 1000 filesize 1000
            logging source-interface Gbit0/1 vrf vpn1
            logging filter flash:172.16.1.1 1 args Test
            """
        )
        playbook = dict(config=[])
        deleted = [
            "no logging rate-limit all 2 except warnings",
            "no logging server-arp",
            "no logging origin-id string Test",
            "no logging reload alerts",
            "no logging userinfo",
            "no logging trap errors",
            "no logging host ipv6 2001:0db8:85a3:0000:0000:8a2e:0370:7324",
            "no logging persistent size 1000 filesize 1000",
            "no logging source-interface Gbit0/1 vrf vpn1",
            "no logging filter flash:172.16.1.1 1 args Test",
        ]
        playbook["state"] = "deleted"
        set_module_args(playbook)
        result = self.execute_module(changed=True)

        self.maxDiff = None
        self.assertEqual(sorted(result["commands"]), sorted(deleted))

    def test_ios_logging_global_replaced(self):
        self.execute_show_command.return_value = dedent(
            """\
            logging host 172.16.1.1
            """
        )
        playbook = dict(
            config=[
                dict(
                    hosts=[
                        dict(
                            hostname="172.16.2.15",
                            session_id=dict(text="Test"),
                        )
                    ]
                )
            ]
        )
        merged = [
            "no logging host 172.16.1.1",
            "logging host 172.16.2.15 session-id string Test",
        ]
        playbook["state"] = "replaced"
        set_module_args(playbook)
        result = self.execute_module(changed=True)

        self.maxDiff = None
        self.assertEqual(sorted(result["commands"]), sorted(merged))
