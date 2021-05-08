# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The Logging_global parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network_template import (
    NetworkTemplate,
)


def tmplt_host(config_data):
    cmd = "logging host"
    verb = config_data.get("hosts")
    changed = True
    if verb.get("transport"):
        changed = False
    if verb:
        if verb.get("hostname"):
            cmd += " {hostname}".format(hostname=verb["hostname"])
        if verb.get("ipv6"):
            cmd += " ipv6 {ipv6}".format(ipv6=verb["ipv6"])
        if verb.get("vrf"):
            cmd += " vrf {vrf}".format(vrf=verb["vrf"])
        if verb.get("filtered"):
            cmd += " {filtered}".format(filtered="filtered")
            changed = True
        if verb.get("xml"):
            cmd += " {xml}".format(xml="xml")
            changed = True
        if verb.get("session_id"):
            session_id = verb.get("session_id")
            changed = True
            if session_id.get("text"):
                cmd += " session-id string {text}".format(
                    text=session_id["text"]
                )
            elif session_id.get("tag"):
                cmd += " session-id {tag}".format(tag=session_id["tag"])
        if verb.get("stream"):
            cmd += " stream {stream}".format(stream=verb["stream"])
            changed = True
        if verb.get("sequence_num_session"):
            cmd += " {sequence_num_session}".format(
                sequence_num_session="sequence-num-session"
            )
            changed = True
        if verb.get("discriminator"):
            cmd += " discriminator {discriminator}".format(
                discriminator=verb["discriminator"]
            )
            changed = True
    if not changed:
        cmd = None
    return cmd


def tmplt_host_transport(config_data):
    cmd = "logging host"
    verb = config_data.get("hosts")

    if verb.get("hostname"):
        cmd += " {hostname}".format(hostname=verb["hostname"])
    if verb.get("ipv6"):
        cmd += " ipv6 {ipv6}".format(ipv6=verb["ipv6"])
    if verb.get("vrf"):
        cmd += " vrf {vrf}".format(vrf=verb["vrf"])
    if verb.get("transport"):
        transport_type = verb.get("transport")
        prot = None
        if transport_type.get("udp"):
            cmd += " transport {prot}".format(prot="udp")
            prot = "udp"
        elif transport_type.get("tcp"):
            cmd += " transport {prot}".format(prot="tcp")
            prot = "tcp"

        if prot:
            verb = transport_type.get(prot)

            if verb.get("port"):
                cmd += " port {port}".format(port=verb["port"])
            if verb.get("audit"):
                cmd += " {audit}".format(audit="audit")
            if verb.get("xml"):
                cmd += " {xml}".format(xml="xml")
            if verb.get("filtered"):
                cmd += " {filtered}".format(filtered="filtered")
            if verb.get("discriminator"):
                cmd += " discriminator {discriminator}".format(
                    discriminator=verb["discriminator"]
                )
            if verb.get("stream"):
                cmd += " stream {stream}".format(stream=verb["stream"])
            if verb.get("session_id"):
                session_id = verb.get("session_id")
                if session_id.get("text"):
                    cmd += " session-id string {text}".format(
                        text=session_id["text"]
                    )
                elif session_id.get("tag"):
                    cmd += " session-id {tag}".format(tag=session_id["tag"])
            if verb.get("sequence_num_session"):
                cmd += " {sequence_num_session}".format(
                    sequence_num_session="sequence-num-session"
                )
    return cmd


def tmplt_host_del(config_data):
    cmd = "logging host"
    verb = config_data.get("hosts")
    if verb.get("hostname"):
        cmd += " {hostname}".format(hostname=verb["hostname"])
    if verb.get("ipv6"):
        cmd += " ipv6 {ipv6}".format(ipv6=verb["ipv6"])
    if verb.get("transport"):
        cmd = None
    return cmd


def tmplt_host_transport_del(config_data):
    cmd = "logging host"
    verb = config_data.get("hosts")
    if verb.get("hostname"):
        cmd += " {hostname}".format(hostname=verb["hostname"])
    if verb.get("ipv6"):
        cmd += " ipv6 {ipv6}".format(ipv6=verb["ipv6"])
    return cmd


def tmplt_buffered(config_data):
    return tmplt_common(config_data.get("buffered"), "logging buffered")


def tmplt_history(config_data):
    return tmplt_common(config_data.get("history"), "logging history")


def tmplt_console(config_data):
    return tmplt_common(config_data.get("console"), "logging console")


def tmplt_monitor(config_data):
    return tmplt_common(config_data.get("monitor"), "logging monitor")


def tmplt_origin_id(config_data):
    return tmplt_common(config_data.get("origin_id"), "logging origin-id")


def tmplt_queue_limit(config_data):
    return tmplt_common(config_data.get("queue_limit"), "logging queue-limit")


def tmplt_rate_limit(config_data):
    return tmplt_common(config_data.get("rate_limit"), "logging rate-limit")


def tmplt_reload(config_data):
    return tmplt_common(config_data.get("reload"), "logging reload")


def tmplt_message_counter(verb):
    cmd = "logging message-counter"

    if verb.get("message_counter"):
        cmd += " {message_counter}".format(
            message_counter=verb["message_counter"]
        )
    return cmd


def tmplt_filter(config_data):
    cmd = "logging filter"
    verb = config_data.get("filter")

    if verb.get("url"):
        cmd += " {url}".format(url=verb["url"])
    if verb.get("order"):
        cmd += " {order}".format(order=verb["order"])
    if verb.get("args"):
        cmd += " args {args}".format(args=verb["args"])
    return cmd


def tmplt_source_interface(config_data):
    cmd = "logging source-interface"
    verb = config_data.get("source_interface")

    if verb.get("interface"):
        cmd += " {interface}".format(interface=verb["interface"])
    if verb.get("vrf"):
        cmd += " vrf {vrf}".format(vrf=verb["vrf"])
    return cmd


def tmplt_common(verb, cmd):
    if verb:
        if verb.get("all"):
            cmd += " {all}".format(all="all")
        if verb.get("console"):
            cmd += " {console}".format(console="console")
        if verb.get("message_limit"):
            cmd += " message-limit {message_limit}".format(
                message_limit=verb["message_limit"]
            )
        if verb.get("discriminator"):
            cmd += " discriminator {discriminator}".format(
                discriminator=verb.get("discriminator")
            )
        if verb.get("filtered"):
            cmd += " {filtered}".format(filtered="filtered")
        if verb.get("xml"):
            cmd += " {xml}".format(xml="xml")
        if verb.get("size"):
            cmd += " {size}".format(size=verb["size"])
        if verb.get("severity"):
            cmd += " {severity}".format(severity=verb["severity"])
        if verb.get("except_severity"):
            cmd += " except {exceptSev}".format(
                exceptSev=verb["except_severity"]
            )
        if verb.get("tag"):
            cmd += " {tag}".format(tag=verb["tag"])
        if verb.get("text"):
            cmd += " string {tag}".format(tag=verb["text"])
        if verb.get("esm"):
            cmd += " esm {tag}".format(tag=verb["esm"])
        if verb.get("trap"):
            cmd += " trap {tag}".format(tag=verb["trap"])
    return cmd


def tmplt_persistent(config_data):
    cmd = "logging persistent"
    verb = config_data.get("persistent")

    if verb.get("url"):
        cmd += " url {url}".format(url=verb["url"])
    if verb.get("size"):
        cmd += " size {size}".format(size=verb["size"])
    if verb.get("filesize"):
        cmd += " filesize {filesize}".format(filesize=verb["filesize"])
    if verb.get("batch"):
        cmd += " batch {batch}".format(batch=verb["batch"])
    if verb.get("threshold"):
        cmd += " threshold {threshold}".format(threshold=verb["threshold"])
    if verb.get("immediate"):
        cmd += " {immediate}".format(immediate="immediate")
    if verb.get("protected"):
        cmd += " {protected}".format(protected="protected")
    if verb.get("notify"):
        cmd += " {notify}".format(notify="notify")
    return cmd


class Logging_globalTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Logging_globalTemplate, self).__init__(
            lines=lines, tmplt=self, module=module
        )

    # fmt: off
    PARSERS = [
        {
            "name": "hosts",
            "getval": re.compile(
                r"""
                ^logging\shost
                (\s(?P<hostname>\S+))?
                (\sipv6\s(?P<ipv6>\S+))?
                (\svrf\s(?P<vrf>\w+))?
                (\s(?P<filtered>filtered))?
                (\s(?P<xml>xml))?
                (\sstream\s(?P<stream>\d+))?
                (\s(?P<session_id>session-id))?
                (\s(?P<tag>hostname|ipv4|ipv6))?
                (\sstring\s(?P<text>\w+))?
                (\s(?P<sequence_num_session>sequence-num-session))?
                (\sdiscriminator\s(?P<discriminator>.+$))?
                $""", re.VERBOSE),
            "setval": tmplt_host,
            "remval": tmplt_host_del,
            "result": {
                "{{ hostname if hostname is defined else ipv6 }}": {
                    "hosts": [{
                        "hostname": "{{ hostname }}",
                        "ipv6": "{{ ipv6 }}",
                        "discriminator": "{{ discriminator }}",
                        "vrf": "{{ vrf }}",
                        "xml": "{{ True if xml is defined }}",
                        "filtered": "{{ True if filtered is defined }}",
                        "sequence_num_session": "{{ True if sequence_num_session is defined }}",
                        "stream": "{{ stream }}",
                        "session_id": {
                            "tag": "{{ tag }}",
                            "text": "{{ text }}",
                        }
                    }]
                }
            },
        },
        {
            "name": "hosts.transport",
            "getval": re.compile(
                r"""
                ^logging\shost
                (\s(?P<hostname>\S+))?
                (\sipv6\s(?P<ipv6>\S+))?
                (\svrf\s(?P<vrf>\w+))?
                (\stransport\s(?P<transport>tcp|udp))?
                (\sport\s(?P<port>[1-9][0-9]*))?
                (\s(?P<audit>audit))?
                (\s(?P<xml>xml))?
                (\s(?P<filtered>filtered))?
                (\sdiscriminator\s(?P<discriminator>.+$))?
                (\sstream\s(?P<stream>\d+))?
                (\s(?P<session_id>session-id))?
                (\s(?P<tag>hostname|ipv4|ipv6))?
                (\sstring\s(?P<text>\w+))?
                (\s(?P<sequence_num_session>sequence-num-session))?
                $""", re.VERBOSE),
            "setval": tmplt_host_transport,
            "remval": tmplt_host_transport_del,
            "result": {
                "{{ hostname if hostname is defined else ipv6 }}": {
                    "hosts": [{
                        "hostname": "{{ hostname }}",
                        "ipv6": "{{ ipv6 }}",
                        "vrf": "{{ vrf if transport is defined }}",
                        "transport": {
                            "{{ transport }}": {
                                "audit": "{{ True if audit is defined }}",
                                "sequence_num_session": "{{ True if sequence_num_session is defined }}",
                                "xml": "{{ True if xml is defined }}",
                                "discriminator": "{{ discriminator }}",
                                "port": "{{ port }}",
                                "session_id": {
                                    "tag": "{{ tag }}",
                                    "text": "{{ text }}",
                                },
                                "filtered": "{{ True if filtered is defined }}",
                                "stream": "{{ stream }}",
                            }
                        }
                    }]
                }
            },
        },
        {
            "name": "buffered",
            "getval": re.compile(
                r"""
                ^logging\sbuffered
                (\sdiscriminator\s(?P<sdiscriminator>.+))?
                (\s(?P<filtered>filtered))?
                (\s(?P<xml>xml))?
                (\s(?P<size>[1-9][0-9]*))?
                (\s(?P<severity>alerts|critical|debugging|emergencies|errors|informational|notifications|warnings))?
                $""", re.VERBOSE),
            "setval": tmplt_buffered,
            "result": {
                "logging": {
                    "buffered": {
                        "filtered": "{{ True if filtered is defined }}",
                        "xml": "{{ True if xml is defined }}",
                        "severity": "{{ severity }}",
                        "size": "{{ size }}",
                        "discriminator": "{{ discriminator }}",
                    }
                }
            },
        },
        {
            "name": "buginf",
            "getval": re.compile(
                r"""
                ^logging\s(?P<buginf>buginf)
                $""", re.VERBOSE),
            "setval": "logging buginf",
            "result": {
                "logging": {
                    "buginf": "{{ True if buginf is defined }}"
                }
            },
        },
        {
            "name": "cns_events",
            "getval": re.compile(
                r"""
                ^logging\scns-events
                (\s(?P<severity>alerts|critical|debugging|emergencies|errors|informational|notifications|warnings))?
                $""", re.VERBOSE),
            "setval": "logging cns-events {{ cns_events }}",
            "result": {
                "logging": {
                    "cns_events": "{{ severity }}"
                }
            },
        },
        {
            "name": "console",
            "getval": re.compile(
                r"""
                ^logging\sconsole
                (\s(?P<filtered>filtered))?
                (\s(?P<xml>xml))?
                (\s(?P<severity>alerts|critical|debugging|emergencies|errors|informational|notifications|warnings|guaranteed$))?
                (\s(?P<discriminator>discriminator\s.+$))?
                $""", re.VERBOSE),
            "setval": tmplt_console,
            "result": {
                "logging": {
                    "console": {
                        "severity": "{{ severity }}",
                        "discriminator": "{{ discriminator }}",
                        "filtered": "{{ True if filtered is defined }}",
                        "xml": "{{ True if xml is defined }}",
                    }
                }
            },
        },
        {
            "name": "count",
            "getval": re.compile(
                r"""
                ^logging\s(?P<count>count)
                $""", re.VERBOSE),
            "setval": "logging count",
            "result": {
                "logging": {
                    "count": "{{ True if count is defined }}"
                }
            },
        },
        {
            "name": "delimiter",
            "getval": re.compile(
                r"""
                ^logging\sdelimiter\s(?P<tcp>tcp)
                $""", re.VERBOSE),
            "setval": "logging delimiter tcp",
            "result": {
                "logging": {
                    "delimiter": {
                        "tcp": "{{ True if tcp is defined }}"
                    }
                }
            },
        },
        {
            "name": "discriminator",
            "getval": re.compile(
                r"""
                ^logging\sdiscriminator\s(?P<discriminator>.+$)
                $""", re.VERBOSE),
            "setval": "logging discriminator {{ discriminator }}",
            "result": {
                "logging": {
                    "discriminator": ["{{ discriminator }}", ]
                }
            },
        },
        {
            "name": "dmvpn",
            "getval": re.compile(
                r"""
                ^logging\sdmvpn\srate-limit
                (\s(?P<rate>\d+))?
                $""", re.VERBOSE),
            "setval": "logging dmvpn rate-limit {{ dmvpn.rate_limit }}",
            "result": {
                "logging": {
                    "dmvpn": {
                        "rate_limit": "{{ rate }}",
                    }
                }
            },
        },
        {
            "name": "esm",
            "getval": re.compile(
                r"""
                ^logging\sesm\s(?P<config>config)
                $""", re.VERBOSE),
            "setval": "logging esm config",
            "result": {
                "logging": {
                    "esm": {
                        "config": "{{ True if config is defined }}"
                    }
                }
            },
        },
        {
            "name": "exception",
            "getval": re.compile(
                r"""
                ^logging\sexception
                \s(?P<exception>[1-9][0-9]*)
                $""", re.VERBOSE),
            "setval": "logging exception {{ exception }}",
            "result": {
                "logging": {
                    "exception": "{{ exception }}"
                }
            },
        },
        {
            "name": "facility",
            "getval": re.compile(
                r"""
                ^logging\sfacility
                \s(?P<facility>auth|cron|daemon|kern|local0|local1|local2|local3|local4|local5|local6|local7|lpr|mail|news|sys10|sys11|sys12|sys13|sys14|sys9|syslog|user|uucp)
                $""", re.VERBOSE),
            "setval": "logging facility {{ facility }}",
            "result": {
                "logging": {
                    "facility": "{{ facility }}"
                }
            },
        },
        {
            "name": "filter",
            "getval": re.compile(
                r"""
                ^logging\sfilter
                (\s(?P<url>\S+))?
                (\s(?P<order>\d+))?
                (\sargs\s(?P<args>.+$))?
                $""", re.VERBOSE),
            "setval": tmplt_filter,
            "result": {
                "logging": {
                    "filter": [{
                        "url": "{{ url }}",
                        "order": "{{ order }}",
                        "args": "{{ args }}",
                    }]
                }
            },
        },
        {
            "name": "history",
            "getval": re.compile(
                r"""
                ^logging\shistory
                (\s(?P<size>\d+))?
                (\s(?P<severity>alerts|critical|debugging|emergencies|errors|informational|notifications|warnings))?
                $""", re.VERBOSE),
            "setval": tmplt_history,
            "result": {
                "logging": {
                    "history": {
                        "severity": "{{ severity }}",
                        "size": "{{ size }}",
                    }
                }
            },
        },
        {
            "name": "message_counter",
            "getval": re.compile(
                r"""
                ^logging\smessage-counter
                \s(?P<counter>log|debug|syslog)
                $""", re.VERBOSE),
            "setval": tmplt_message_counter,
            "result": {
                "logging": {
                    "message_counter": ["{{ counter }}", ]
                }
            },
        },
        {
            "name": "monitor",
            "getval": re.compile(
                r"""
                ^logging\smonitor
                (\s(?P<filtered>filtered))?
                (\s(?P<xml>xml))?
                (\s(?P<severity>alerts|critical|debugging|emergencies|errors|informational|notifications|warnings))?
                (\s(?P<discriminator>discriminator\s.+$))?
                $""", re.VERBOSE),
            "setval": tmplt_monitor,
            "result": {
                "logging": {
                    "monitor": {
                        "filtered": "{{ True if filtered is defined }}",
                        "xml": "{{ True if xml is defined }}",
                        "severity": "{{ severity }}",
                        "discriminator": "{{ discriminator }}",
                    }
                }
            },
        },
        {
            "name": "logging_on",
            "getval": re.compile(
                r"""
                ((?P<negate>no))?
                ((\s|^))?logging
                (\s(?P<on>on))?
                $""", re.VERBOSE),
            "setval": "{{ 'no ' if logging_on == 'disable' }}logging on",
            "remval": "logging on",
            "result": {
                "logging": {
                    "logging_on": "{{ 'disable' if negate is defined else 'enable' }}",
                }
            },
        },
        {
            "name": "origin_id",
            "getval": re.compile(
                r"""
                ^logging\sorigin-id
                (\s(?P<tag>hostname|ip|ipv6))?
                (\sstring\s(?P<text>.+$))?
                $""", re.VERBOSE),
            "setval": tmplt_origin_id,
            "result": {
                "logging": {
                    "origin_id": {
                        "tag": "{{ tag }}",
                        "text": "{{ text }}",
                    }
                }
            },
        },
        {
            "name": "persistent",
            "getval": re.compile(
                r"""
                ^logging\spersistent
                (\surl\s(?P<url>\S+))?
                (\ssize\s(?P<size>[1-9][0-9]*))?
                (\sfilesize\s(?P<filesize>[1-9][0-9]*))?
                (\sbatch\s(?P<batch>[1-9][0-9]*))?
                (\sthreshold\s(?P<threshold>[1-9][0-9]*))?
                (\s(?P<immediate>immediate))?
                (\s(?P<protected>protected))?
                (\s(?P<notify>notify))?
                $""", re.VERBOSE),
            "setval": tmplt_persistent,
            "result": {
                "logging": {
                    "persistent": {
                        "batch": "{{ batch }}",
                        "filesize": "{{ filesize }}",
                        "immediate": "{{ True if immediate is defined }}",
                        "notify": "{{ True if notify is defined }}",
                        "protected": "{{ True if protected is defined }}",
                        "size": "{{ size }}",
                        "threshold": "{{ threshold }}",
                        "url": "{{ url }}",
                    }
                }
            },
        },
        {
            "name": "policy_firewall",
            "getval": re.compile(
                r"""
                ^logging\spolicy-firewall
                (\srate-limit\s(?P<rate>[1-9][0-9]*))?
                $""", re.VERBOSE),
            "setval": "logging policy-firewall rate-limit {{ policy_firewall.rate_limit }}",
            "result": {
                "logging": {
                    "policy_firewall": {
                        "rate_limit": "{{ rate }}",
                    }
                }
            },
        },
        {
            "name": "queue_limit",
            "getval": re.compile(
                r"""
                ^logging\squeue-limit
                (\s(?P<size>[1-9][0-9]*))?
                (\sesm\s(?P<esm>[1-9][0-9]*))?
                (\strap\s(?P<trap>[1-9][0-9]*))?
                $""", re.VERBOSE),
            "setval": tmplt_queue_limit,
            "result": {
                "logging": {
                    "queue_limit": {
                        "size": "{{ size }}",
                        "esm": "{{ esm }}",
                        "trap": "{{ trap }}",
                    }
                }
            },
        },
        {
            "name": "rate_limit",
            "getval": re.compile(
                r"""
                ^logging\srate-limit
                (\s(?P<option>all|console))?
                (\s(?P<size>[1-9][0-9]*))?
                (\sexcept\s(?P<except_severity>alerts|critical|debugging|emergencies|errors|informational|notifications|warnings))?
                $""", re.VERBOSE),
            "setval": tmplt_rate_limit,
            "result": {
                "logging": {
                    "rate_limit": {
                        "size": "{{ size }}",
                        "all": "{{ True if option == 'all' }}",
                        "console": "{{ True if option == 'console' }}",
                        "except_severity": "{{ except_severity }}",
                    }
                }
            },
        },
        {
            "name": "reload",
            "getval": re.compile(
                r"""
                ^logging
                (\s(?P<reload>reload))?
                (\smessage-limit\s(?P<message_limit>[1-9][0-9]*))?
                (\s(?P<severity>alerts|critical|debugging|emergencies|errors|informational|notifications|warnings))?
                $""", re.VERBOSE),
            "setval": tmplt_reload,
            "result": {
                "logging": {
                    "reload": {
                        "severity": "{{ severity }}",
                        "message_limit": "{{ message_limit }}",
                    }
                }
            },
        },
        {
            "name": "server_arp",
            "getval": re.compile(
                r"""
                ^logging
                \s(?P<server_arp>server-arp)
                $""", re.VERBOSE),
            "setval": "logging server-arp",
            "result": {
                "logging": {
                    "server_arp": "{{ True if server_arp is defined }}"
                }
            },
        },
        {
            "name": "snmp_trap",
            "getval": re.compile(
                r"""
                ^logging\ssnmp-trap
                (\s(?P<severity>alerts|critical|debugging|emergencies|errors|informational|notifications|warnings))?
                $""", re.VERBOSE),
            "setval": "logging snmp-trap {{ snmp_trap }}",
            "result": {
                "logging": {
                    "snmp_trap": ["{{ severity }}", ]
                }
            },
        },
        {
            "name": "source_interface",
            "getval": re.compile(
                r"""
                ^logging\ssource-interface
                (\s(?P<interface>\S+))?
                (\svrf\s(?P<vrf>\S+))?
                $""", re.VERBOSE),
            "setval": tmplt_source_interface,
            "result": {
                "logging": {
                    "source_interface": [{
                        "interface": "{{ interface }}",
                        "vrf": "{{ vrf }}",
                    }]
                }
            },
        },
        {
            "name": "trap",
            "getval": re.compile(
                r"""
                ^logging\strap
                \s(?P<severity>alerts|critical|debugging|emergencies|errors|informational|notifications|warnings)
                $""", re.VERBOSE),
            "setval": "logging trap {{ trap }}",
            "result": {
                "logging": {
                    "trap": "{{ severity }}",
                }
            },
        },
        {
            "name": "userinfo",
            "getval": re.compile(
                r"""
                ^logging\s(?P<userinfo>userinfo)
                $""", re.VERBOSE),
            "setval": "logging userinfo",
            "result": {
                "logging": {
                    "userinfo": "{{ True if userinfo is defined }}"
                }
            },
        },
    ]
    # fmt: on
