# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The Bgp_address_family parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network_template import (
    NetworkTemplate,
)


def _tmplt_af(config_data):
    if "address_family" in config_data:
        cmd = "address-family {{ afi }}".format(
            **config_data["address_family"]
        )
        if config_data["address_family"].get("safi"):
            cmd += " {{ safi }}".format(**config_data["address_family"])
        if config_data["address_family"].get("vrf"):
            cmd += " vrf {{ vrf }}".format(**config_data["address_family"])
        return cmd


def _tmplt_af_aggregate_address(config_data):
    if "aggregate_address" in config_data:
        cmd = "aggregate-address {address} {netmask}".format(
            **config_data["aggregate_address"]
        )
        if "advertise_map" in config_data["aggregate_address"]:
            cmd += " advertise-map {advertise_map}".format(
                **config_data["aggregate_address"]
            )
        if "as_confed_set" in config_data["aggregate_address"]:
            cmd += " as-confed-set"
        if "as_set" in config_data["aggregate_address"]:
            cmd += " as-set"
        if "attribute_map" in config_data["aggregate_address"]:
            cmd += " attribute-map {attribute_map}".format(
                **config_data["aggregate_address"]
            )
        if "summary_only" in config_data["aggregate_address"]:
            cmd += " summary-only"
        if "suppress_map" in config_data["aggregate_address"]:
            cmd += " suppress-map {suppress_map}".format(
                **config_data["aggregate_address"]
            )

        return cmd


def _tmplt_bgp_af_additional_paths(config_data):
    if "bgp" in config_data:
        if "additional_paths" in config_data["bgp"]:
            cmd = "bgp additional-paths"
            if "install" in config_data["bgp"]["additional_paths"]:
                cmd += " install"
            elif "select" in config_data["bgp"]["additional_paths"]:
                cmd += " select"
                if "all" in config_data["bgp"]["additional_paths"]["select"]:
                    cmd += " all"
                elif (
                    "best" in config_data["bgp"]["additional_paths"]["select"]
                ):
                    cmd += " best {best}".format(
                        **config_data["bgp"]["additional_paths"]["select"]
                    )
                elif (
                    "best_external"
                    in config_data["bgp"]["additional_paths"]["select"]
                ):
                    cmd += " best-external"
                elif (
                    "group_best"
                    in config_data["bgp"]["additional_paths"]["select"]
                ):
                    cmd += " group-best"
            if "receive" in config_data["bgp"]["additional_paths"]:
                cmd += " receive"
            if "send" in config_data["bgp"]["additional_paths"]:
                cmd += " send"
            return cmd


def _tmplt_bgp_af_config(config_data):
    if "bgp" in config_data:
        cmd = []
        if config_data["bgp"].get("aggregate_timer"):
            cmd.append(
                "bgp aggregate-timer {aggregate_timer}".format(
                    **config_data["bgp"]
                )
            )
        if config_data["bgp"].get("dmzlink_bw"):
            cmd.append("bgp dmzlink-bw")
        if "nexthop" in config_data["bgp"]:
            command = "bgp nexthop"
            if "route_map" in config_data["bgp"]["nexthop"]:
                command += " route-map {route_map}".format(
                    **config_data["bgp"]["nexthop"]
                )
            elif "trigger" in config_data["bgp"]["nexthop"]:
                if config_data["bgp"]["nexthop"]["trigger"].get("delay"):
                    command += " trigger delay {delay}".format(
                        **config_data["bgp"]["nexthop"]["trigger"]
                    )
                elif config_data["bgp"]["nexthop"]["trigger"].get("delay"):
                    command += " trigger enable"
            cmd.append(command)
        if config_data["bgp"].get("redistribute_internal"):
            cmd.append("bgp redistribute-internal")
        if config_data["bgp"].get("route_map"):
            cmd.append("bgp route-map priority")
        if config_data["bgp"].get("scan_time"):
            cmd.append(
                "bgp scan-time {scan_time}".format(**config_data["bgp"])
            )
        if config_data["bgp"].get("soft_reconfig_backup"):
            cmd.append("bgp soft-reconfig-backup")
        if config_data["bgp"].get("update_group"):
            cmd.append("bgp update-group split as-override")
        return cmd


def _tmplt_bgp_af_dampening(config_data):
    if "bgp" in config_data and "dampening" in config_data["bgp"]:
        if config_data["bgp"]["dampening"].get("penalty_half_time"):
            command = "bgp dampening {penalty_half_time}".format(
                **config_data["bgp"]["dampening"]
            )
            if config_data["bgp"]["dampening"].get("reuse_route_val"):
                command += " {reuse_route_val}".format(
                    **config_data["bgp"]["dampening"]
                )
            if config_data["bgp"]["dampening"].get("suppress_route_val"):
                command += " {suppress_route_val}".format(
                    **config_data["bgp"]["dampening"]
                )
            if config_data["bgp"]["dampening"].get("max_suppress"):
                command += " {max_suppress}".format(
                    **config_data["bgp"]["dampening"]
                )
        elif config_data["bgp"]["dampening"].get("route_map"):
            command = "bgp dampening {route_map}".format(
                **config_data["bgp"]["dampening"]
            )
        return command


def _tmplt_bgp_af_slow_peer(config_data):
    if "bgp" in config_data and "slow_peer" in config_data["bgp"]:
        if "slow_peer" in config_data["bgp"]:
            cmd = "bgp slow-peer"
            if "detection" in config_data["bgp"]["slow_peer"]:
                cmd += " detection"
                if "threshold" in config_data["bgp"]["slow_peer"]["detection"]:
                    cmd += " threshold {threshold}".format(
                        **config_data["bgp"]["slow_peer"]["detection"]
                    )
            elif "split_update_group" in config_data["bgp"]["slow_peer"]:
                cmd += " split-update-group"
                if (
                    "dynamic"
                    in config_data["bgp"]["slow_peer"]["split_update_group"]
                ):
                    cmd += " dynamic"
                    if (
                        "permanent"
                        in config_data["bgp"]["slow_peer"][
                            "split_update_group"
                        ]
                    ):
                        cmd += " permanent {permanent}".format(
                            **config_data["bgp"]["slow_peer"][
                                "split_update_group"
                            ]
                        )
        return cmd


def _tmplt_af_distance(config_data):
    if config_data.get("distance"):
        cmd = "distance bgp {external} {internal} {local}".format(
            **config_data["distance"]
        )
        return cmd


def _tmplt_af_neighbor(config_data):
    if "neighbor" in config_data:
        commands = []
        cmd = "neighbor"
        # for each in list(config_data["neighbor"]):
        if "address" in config_data["neighbor"]:
            cmd += " {address}".format(**config_data["neighbor"])
        elif "tag" in config_data["neighbor"]:
            cmd += " {tag}".format(**config_data["neighbor"])
        elif "ipv6_adddress" in config_data["neighbor"]:
            cmd += " {ipv6_adddress}".format(**config_data["neighbor"])
        if "peer_group" in config_data["neighbor"]:
            commands.append(
                "{0} peer-group {peer_group}".format(
                    cmd, **config_data["neighbor"]
                )
            )
        if "remote_as" in config_data["neighbor"]:
            commands.append(
                "{0} remote-as {remote_as}".format(
                    cmd, **config_data["neighbor"]
                )
            )
        if "activate" in config_data["neighbor"]:
            commands.append("{0} activate".format(cmd))
        if "additional_paths" in config_data["neighbor"]:
            self_cmd = "{0} additional-paths".format(cmd)
            if "disable" in config_data["neighbor"]["additional_paths"]:
                self_cmd += " disable"
            elif "receive" in config_data["neighbor"]["additional_paths"]:
                self_cmd += " receive"
            elif "send" in config_data["neighbor"]["additional_paths"]:
                self_cmd += " send"
            commands.append(self_cmd)
        if "advertise" in config_data["neighbor"]:
            self_cmd = "{0} advertise".format(cmd)
            if "additional_paths" in config_data["neighbor"]["advertise"]:
                self_cmd += " additional-paths"
                if (
                    "all"
                    in config_data["neighbor"]["advertise"]["additional_paths"]
                ):
                    self_cmd += " all"
                elif (
                    "best"
                    in config_data["neighbor"]["advertise"]["additional_paths"]
                ):
                    self_cmd += " best {best}".format(
                        **config_data["neighbor"]["advertise"][
                            "additional_paths"
                        ]
                    )
                elif (
                    "group_best"
                    in config_data["neighbor"]["advertise"]["additional_paths"]
                ):
                    self_cmd += " group-best"
            elif "best_external" in config_data["neighbor"]["advertise"]:
                self_cmd += " best-external"
            elif "diverse_path" in config_data["neighbor"]["advertise"]:
                self_cmd += "diverse-path"
                if (
                    "backup"
                    in config_data["neighbor"]["advertise"]["diverse_path"]
                ):
                    self_cmd += " backup"
                elif (
                    "mpath"
                    in config_data["neighbor"]["advertise"]["diverse_path"]
                ):
                    self_cmd += " mpath"
            commands.append(self_cmd)
        if config_data["neighbor"].get("advertise_map"):
            self_cmd = "{0} advertise-map {name}".format(
                cmd, **config_data["neighbor"]["advertise_map"]
            )
            if "exist_map" in config_data["neighbor"]["advertise_map"]:
                self_cmd += " exist-map {exist_map}".format(
                    **config_data["neighbor"]["advertise_map"]
                )
            elif "non_exist_map" in config_data["neighbor"]["advertise_map"]:
                self_cmd += " exist-map {non_exist_map}".format(
                    **config_data["neighbor"]["advertise_map"]
                )
            commands.append(self_cmd)
        if config_data["neighbor"].get("advertisement_interval"):
            commands.append(
                "{0} advertisement-interval {advertisement_interval}".format(
                    cmd, **config_data["neighbor"]
                )
            )
        if config_data["neighbor"].get("aigp"):
            self_cmd = "{0} aigp".format(cmd)
            if config_data["neighbor"]["aigp"].get("send"):
                self_cmd += " send"
                if config_data["neighbor"]["aigp"]["send"].get(
                    "cost_community"
                ):
                    self_cmd += " cost-community {id}".format(
                        **config_data["neighbor"]["aigp"]["send"][
                            "cost_community"
                        ]
                    )
                    if config_data["neighbor"]["aigp"]["send"][
                        "cost_community"
                    ].get("poi"):
                        self_cmd += " poi"
                        if config_data["neighbor"]["aigp"]["send"][
                            "cost_community"
                        ]["poi"].get("igp_cost"):
                            self_cmd += " igp-cost"
                        if config_data["neighbor"]["aigp"]["send"][
                            "cost_community"
                        ]["poi"].get("pre_bestpath"):
                            self_cmd += " pre-bestpath"
                        if config_data["neighbor"]["aigp"]["send"][
                            "cost_community"
                        ]["poi"].get("transitive"):
                            self_cmd += " transitive"
                if config_data["neighbor"]["aigp"]["send"].get("med"):
                    self_cmd += " med"
            commands.append(self_cmd)
        if config_data["neighbor"].get("allow_policy"):
            commands.append("{0} allow-policy".format(cmd))
        if config_data["neighbor"].get("allowas_in"):
            commands.append(
                "{0} allowas-in {allowas_in}".format(
                    cmd, **config_data["neighbor"]
                )
            )
        if config_data["neighbor"].get("as_override"):
            commands.append("{0} as-override".format(cmd))
        if "bmp_activate" in config_data["neighbor"]:
            self_cmd = "{0} bmp-activate".format(cmd)
            if config_data["neighbor"]["bmp_activate"].get("all"):
                self_cmd += " all"
            if "server" in config_data["neighbor"]["bmp_activate"]:
                self_cmd += " server {server}".format(
                    **config_data["neighbor"]["bmp_activate"]
                )
            commands.append(self_cmd)
        if "capability" in config_data["neighbor"]:
            self_cmd = "{0} capability".format(cmd)
            if config_data["neighbor"]["capability"].get("both"):
                self_cmd += " both"
            elif config_data["neighbor"]["capability"].get("receive"):
                self_cmd += " receive"
            elif config_data["neighbor"]["capability"].get("send"):
                self_cmd += " send"
            commands.append(self_cmd)
        if config_data["neighbor"].get("cluster_id"):
            commands.append(
                "{0} cluster-id {cluster_id}".format(
                    cmd, **config_data["neighbor"]
                )
            )
        if "default_originate" in config_data["neighbor"]:
            self_cmd = "{0} default-originate".format(cmd)
            if config_data["neighbor"]["default_originate"].get("route_map"):
                self_cmd += " route-map {route_map}".format(
                    **config_data["neighbor"]["default_originate"]
                )
            commands.append(self_cmd)
        if "description" in config_data["neighbor"]:
            commands.append(
                "{0} description {description}".format(
                    cmd, **config_data["neighbor"]
                )
            )
        if config_data["neighbor"].get("disable_connected_check"):
            commands.append("{0} disable-connected-check".format(cmd))
        if "distribute_list" in config_data["neighbor"]:
            self_cmd = "{0} distribute-list".format(cmd)
            if "acl" in config_data["neighbor"]["distribute_list"]:
                self_cmd += " {acl}".format(
                    **config_data["neighbor"]["distribute_list"]
                )
            if config_data["neighbor"]["distribute_list"].get("in"):
                self_cmd += " in"
            elif config_data["neighbor"]["distribute_list"].get("out"):
                self_cmd += " out"
            commands.append(self_cmd)
        if config_data["neighbor"].get("dmzlink_bw"):
            commands.append("{0} dmzlink-bw".format(cmd))
        if "ebgp_multihop" in config_data["neighbor"]:
            self_cmd = "{0} ebgp-multihop".format(cmd)
            if "hop_count" in config_data["neighbor"]["ebgp_multihop"]:
                self_cmd += " {hop_count}".format(
                    **config_data["neighbor"]["ebgp_multihop"]
                )
            commands.append(self_cmd)
        if "fall_over" in config_data["neighbor"]:
            self_cmd = "{0} fall-over".format(cmd)
            if "bfd" in config_data["neighbor"]["fall_over"]:
                self_cmd += " bfd"
                if config_data["neighbor"]["fall_over"]["bfd"].get(
                    "multi_hop"
                ):
                    self_cmd += " multi-hop"
                elif config_data["neighbor"]["fall_over"]["bfd"].get(
                    "single_hop"
                ):
                    self_cmd += " single-hop"
            elif "route_map" in config_data["neighbor"]["fall_over"]:
                self_cmd += " {route_map}".format(
                    **config_data["neighbor"]["route_map"]
                )
            commands.append(self_cmd)
        if "filter_list" in config_data["neighbor"]:
            self_cmd = "{0} filter-list".format(cmd)
            if "path_acl" in config_data["neighbor"]["filter_list"]:
                self_cmd += " {path_acl}".format(
                    **config_data["neighbor"]["filter_list"]
                )
            if config_data["neighbor"]["filter_list"].get("in"):
                self_cmd += " in"
            elif config_data["neighbor"]["filter_list"].get("out"):
                self_cmd += " out"
            commands.append(self_cmd)
        if "ha_mode" in config_data["neighbor"]:
            self_cmd = "{0} ha-mode".format(cmd)
            if config_data["neighbor"]["ha_mode"].get("disable"):
                self_cmd += " disable"
            commands.append(self_cmd)
        if "inherit" in config_data["neighbor"]:
            self_cmd = "{0} inherit {inherit}".format(
                cmd, **config_data["neighbor"]
            )
            commands.append(self_cmd)
        if config_data["neighbor"].get("local_as"):
            self_cmd = "{0} local-as".format(cmd)
            if "number" in config_data["neighbor"]["local_as"]:
                self_cmd += " {number}".format(
                    **config_data["neighbor"]["local_as"]
                )
            if config_data["neighbor"]["local_as"].get("dual_as"):
                self_cmd += " dual-as"
            elif config_data["neighbor"]["local_as"].get("no_prepend"):
                self_cmd += " no-prepend"
                if config_data["neighbor"]["local_as"]["no_prepend"]:
                    self_cmd += " replace-as"
            commands.append(self_cmd)
        if "log_neighbor_changes" in config_data["neighbor"]:
            self_cmd = "{0} log-neighbor-changes".format(cmd)
            if config_data["neighbor"]["log_neighbor_changes"].get("disable"):
                self_cmd += " disable"
            commands.append(self_cmd)
        if "maximum_prefix" in config_data["neighbor"]:
            self_cmd = "{0} maximum-prefix".format(cmd)
            if "number" in config_data["neighbor"]["maximum_prefix"]:
                self_cmd += " {number}".format(
                    **config_data["neighbor"]["maximum_prefix"]
                )
            if "threshold_value" in config_data["neighbor"]["maximum_prefix"]:
                self_cmd += " {threshold_value}".format(
                    **config_data["neighbor"]["maximum_prefix"]
                )
            if config_data["neighbor"]["maximum_prefix"].get("restart"):
                self_cmd += " restart {restart}".format(
                    **config_data["neighbor"]["maximum_prefix"]
                )
            elif config_data["neighbor"]["filter_list"].get("warning_only"):
                self_cmd += " warning-only"
            commands.append(self_cmd)
        if "next_hop_self" in config_data["neighbor"]:
            self_cmd = "{0} next-hop-self".format(cmd)
            if config_data["neighbor"]["next_hop_self"].get("all"):
                self_cmd += " all"
            commands.append(self_cmd)
        if "next_hop_unchanged" in config_data["neighbor"]:
            self_cmd = "{0} next-hop-unchanged".format(cmd)
            if config_data["neighbor"]["next_hop_unchanged"].get("allpaths"):
                self_cmd += " allpaths"
            commands.append(self_cmd)
        if "prefix_list" in config_data["neighbor"]:
            self_cmd = "{0} prefix-list {name}".format(
                cmd, **config_data["neighbor"]["prefix_list"]
            )
            if config_data["neighbor"]["prefix_list"].get("in"):
                self_cmd += " in"
            elif config_data["neighbor"]["prefix_list"].get("out"):
                self_cmd += " out"
            commands.append(self_cmd)
        if "peer_group" in config_data["neighbor"]:
            commands.append(
                "{0} peer-group {peer_group}".format(
                    cmd, **config_data["neighbor"]
                )
            )
        if "remove_private_as" in config_data["neighbor"]:
            self_cmd = "{0} remove-private-as".format(cmd)
            if config_data["neighbor"]["remove_private_as"].get("all"):
                self_cmd += " all"
            elif config_data["neighbor"]["remove_private_as"].get(
                "replace_as"
            ):
                self_cmd += " replace_as"
            commands.append(self_cmd)
        if "route_map" in config_data["neighbor"]:
            self_cmd = "{0} route-map".format(cmd)
            if "name" in config_data["neighbor"]["route_map"]:
                self_cmd += " {name}".format(
                    **config_data["neighbor"]["route_map"]
                )
            if "in" in config_data["neighbor"]["route_map"]:
                self_cmd += " in"
            elif "out" in config_data["neighbor"]["route_map"]:
                self_cmd += " out"
            commands.append(self_cmd)
        if "route_reflector_client" in config_data["neighbor"]:
            commands.append("{0} route-reflector-client".format(cmd))
        if "route_server_client" in config_data["neighbor"]:
            self_cmd = "{0} route-server-client".format(cmd)
            if "context" in config_data["neighbor"]["route_map"]:
                self_cmd += " context {context}".format(
                    **config_data["neighbor"]["route_server_client"]
                )
            commands.append(self_cmd)
        if "send_community" in config_data["neighbor"]:
            self_cmd = "{0} send-community".format(cmd)
            if config_data["neighbor"]["send_community"].get("both"):
                self_cmd += " both"
            elif config_data["neighbor"]["send_community"].get("extended"):
                self_cmd += " extended"
            elif config_data["neighbor"]["send_community"].get("standard"):
                self_cmd += " standard"
            commands.append(self_cmd)
        if "soft_reconfiguration" in config_data["neighbor"]:
            commands.append("{0} soft-reconfiguration".format(cmd))
        if "soo" in config_data["neighbor"]:
            commands.append(
                "{0} soo {soo}".format(cmd, **config_data["neighbor"])
            )
        if "unsuppress_map" in config_data["neighbor"]:
            commands.append(
                "{0} unsuppress-map {unsuppress_map}".format(
                    cmd, **config_data["neighbor"]
                )
            )
        if "version" in config_data["neighbor"]:
            commands.append(
                "{0} version {version}".format(cmd, **config_data["neighbor"])
            )
        if "weight" in config_data["neighbor"]:
            commands.append(
                "{0} weight {weight}".format(cmd, **config_data["neighbor"])
            )
        return commands


def _tmplt_neighbor_af_slow_peer(config_data):
    if "neighbor" in config_data and "slow_peer" in config_data["neighbor"]:
        if "slow_peer" in config_data["neighbor"]:
            cmd = "neighbor {address} slow-peer".format(
                **config_data["neighbor"]
            )
            if "detection" in config_data["neighbor"]["slow_peer"]:
                cmd += " detection"
                if (
                    "disable"
                    in config_data["neighbor"]["slow_peer"]["detection"]
                ):
                    cmd += " disable"
                elif (
                    "threshold"
                    in config_data["neighbor"]["slow_peer"]["detection"]
                ):
                    cmd += " threshold {threshold}".format(
                        **config_data["neighbor"]["slow_peer"]["detection"]
                    )
            elif "split_update_group" in config_data["neighbor"]["slow_peer"]:
                cmd += " split-update-group"
                if (
                    "dynamic"
                    in config_data["neighbor"]["slow_peer"][
                        "split_update_group"
                    ]
                ):
                    cmd += " dynamic"
                    if (
                        "disable"
                        in config_data["neighbor"]["slow_peer"][
                            "split_update_group"
                        ]["dynamic"]
                    ):
                        cmd += " disable"
                    elif (
                        "permanent"
                        in config_data["neighbor"]["slow_peer"][
                            "split_update_group"
                        ]["dynamic"]
                    ):
                        cmd += " permanent"
                elif (
                    "static"
                    in config_data["neighbor"]["slow_peer"][
                        "split_update_group"
                    ]
                ):
                    cmd += " static"
        return cmd


def _tmplt_af_network(config_data):
    if "network" in config_data:
        cmd = "network {address}".format(**config_data["network"])
        if "mask" in config_data["network"]:
            cmd += " mask {mask}".format(**config_data["network"])
        if "backdoor" in config_data["network"]:
            cmd += " backdoor"
        if "route_map" in config_data["network"]:
            cmd += " route-map {route_map}".format(**config_data["network"])
        return cmd


def _tmplt_af_snmp(config_data):
    if "snmp" in config_data:
        cmd = "snmp context {name}".format(**config_data["snmp"])
        if config_data["snmp"].get("community"):
            cmd += " community {snmp_community}".format(
                **config_data["snmp"]["community"]
            )
            if config_data["snmp"]["community"].get("ro"):
                cmd += " ro"
            elif config_data["snmp"]["community"].get("rw"):
                cmd += " rw"
            if config_data["snmp"]["community"].get("acl"):
                cmd += " {acl}".format(**config_data["snmp"]["community"])
            elif config_data["snmp"]["community"].get("ipv6"):
                cmd += " ipv6 {ipv6}".format(
                    **config_data["snmp"]["community"]
                )
        if config_data["snmp"].get("user"):
            cmd += " user {name}".format(**config_data["snmp"]["user"])
            if config_data["snmp"]["user"].get("credential"):
                cmd += " credential"
            elif config_data["snmp"]["user"].get("encrypted"):
                cmd += " encrypted"
            if config_data["snmp"]["user"].get("auth"):
                cmd += " auth"
                if config_data["snmp"]["user"]["auth"].get("md5"):
                    cmd += " md5 {md5}".format(
                        **config_data["snmp"]["user"]["auth"]
                    )
                elif config_data["snmp"]["user"]["auth"].get("sha"):
                    cmd += " sha {sha}".format(
                        **config_data["snmp"]["user"]["auth"]
                    )
            if config_data["snmp"]["user"].get("access"):
                cmd += " access"
                if config_data["snmp"]["user"]["access"].get("acl"):
                    cmd += " {acl}".format(
                        **config_data["snmp"]["user"]["access"]
                    )
                elif config_data["snmp"]["user"]["access"].get("ipv6"):
                    cmd += " ipv6 {ipv6}".format(
                        **config_data["snmp"]["user"]["access"]
                    )
            if config_data["snmp"]["user"].get("priv"):
                cmd += " priv"
                if config_data["snmp"]["user"]["priv"].get("3des"):
                    cmd += " 3des {3des}".format(
                        **config_data["snmp"]["user"]["priv"]
                    )
                elif config_data["snmp"]["user"]["priv"].get("des"):
                    cmd += " des {des}".format(
                        **config_data["snmp"]["user"]["priv"]
                    )
                elif config_data["snmp"]["user"]["priv"].get("aes"):
                    cmd += " aes"
                    if config_data["snmp"]["user"]["priv"]["aes"].get("128"):
                        cmd += " 128 {128}".format(
                            **config_data["snmp"]["user"]["priv"]["aes"]
                        )
                    if config_data["snmp"]["user"]["priv"]["aes"].get("192"):
                        cmd += " 192 {192}".format(
                            **config_data["snmp"]["user"]["priv"]["aes"]
                        )
                    if config_data["snmp"]["user"]["priv"]["aes"].get("256"):
                        cmd += " 256 {256}".format(
                            **config_data["snmp"]["user"]["priv"]["aes"]
                        )
        return cmd


def _tmplt_af_table_map(config_data):
    if "table_map" in config_data:
        cmd = "table-map {name}".format(**config_data["table_map"])
        if config_data["table_map"].get("filter"):
            cmd += " filter"
        return cmd


class Bgp_AddressFamilyTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Bgp_AddressFamilyTemplate, self).__init__(
            lines=lines, tmplt=self, module=module
        )

    PARSERS = [
        {
            "name": "as_number",
            "getval": re.compile(
                r"""^router*
                    \s*bgp*
                    \s*(?P<as_number>\d+)*
                    $""",
                re.VERBOSE,
            ),
            "compval": "as_number",
            "setval": "router bgp {{ as_number }}",
            "result": {"as_number": "{{ as_number }}"},
            "shared": True,
        },
        {
            "name": "afi",
            "getval": re.compile(
                r"""\s*address-family*
                    \s*(?P<afi>ipv4|ipv6|l2vpn|nsap|rtfilter|vpnv4|vpnv6)*
                    \s*(?P<safi>flowspec|mdt|multicast|mvpn|unicast|evpn|vpls)*
                    \s*(?P<vrf>vrf\s\S+)*
                    $""",
                re.VERBOSE,
            ),
            "compval": "afi",
            "setval": _tmplt_af,
            "result": {
                "address_family": {
                    "{{ afi + '_' + safi|d() + '_' + vrf|d() }}": {
                        "afi": "{{ afi }}",
                        "safi": "{{ safi }}",
                        "vrf": "{{ vrf.split('vrf ')[1] if vrf is defined }}",
                    }
                }
            },
            "shared": True,
        },
        {
            "name": "aggregate_address",
            "getval": re.compile(
                r"""\s*aggregate-address*
                    \s*(?P<address>(?:[0-9]{1,3}\.){3}[0-9]{1,3}\s(?:[0-9]{1,3}\.){3}[0-9]{1,3})*
                    \s*(?P<as_confed_set>as-confed-set)*
                    \s*(?P<as_set>as-set)*
                    \s*(?P<route_map>route-map\s\S+)*
                    \s*(?P<summary_only>summary-only)*
                    \s*(?P<attribute_map>attribute-map\s\S+)*
                    \s*(?P<advertise_map>advertise-map\s\S+)*
                    \s*(?P<suppress_map>suppress-map\s\S+)*
                    $""",
                re.VERBOSE,
            ),
            "compval": "aggregate_address",
            "setval": _tmplt_af_aggregate_address,
            "result": {
                "address_family": {
                    "{{ afi|d() + '_' + safi|d() + '_' + vrf|d() }}": {
                        "aggregate_address": [
                            {
                                "address": "{{ address.split(' ')[0] }}",
                                "netmask": "{{ address.split(' ')[1] }}",
                                "advertise_map": "{{ advertise_map.split('advertise-map ')[1] if advertise_map is defined }}",
                                "as_confed_set": "{{ True if as_confed_set is defined }}",
                                "as_set": "{{ True if as_set is defined }}",
                                "attribute_map": "{{ attribute_map.split('attribute-map ')[1] if attribute_map is defined }}",
                                "summary_only": "{{ True if summary_only is defined }}",
                                "suppress_map": "{{ suppress_map.split('suppress-map ')[1] if suppress_map is defined }}",
                            }
                        ]
                    }
                }
            },
        },
        {
            "name": "bgp.additional_paths",
            "getval": re.compile(
                r"""\s*bgp*
                    \s*additional-paths*
                    \s*(?P<receive>receive)*
                    \s*(?P<select>select)*
                    \s*(?P<select_all>all)*
                    \s*(?P<select_backup>backup)*
                    \s*(?P<select_best>best\s\d)*
                    \s*(?P<select_group_best>group-best)*
                    \s*(?P<send>send)*
                    $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_bgp_af_additional_paths,
            "result": {
                "address_family": {
                    "{{ afi|d() + '_' + safi|d() + '_' + vrf|d() }}": {
                        "bgp": {
                            "additional_paths": {
                                "receive": "{{ True if receive is defined }}",
                                "select": {
                                    "all": "{{ True if select_all is defined }}",
                                    "backup": "{{ True if select_backup is defined }}",
                                    "best": "{{ select_best.split('best ')[1] if select_best is defined }}",
                                    "group_best": "{{ True if select_group_best is defined }}",
                                },
                                "send": "{{ True if send is defined }}",
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "bgp.config",
            "getval": re.compile(
                r"""\s*bgp*
                    \s*(?P<aggregate_timer>aggregate-timer\s\d+)*
                    \s*(?P<dmzlink_bw>dmzlink-bw)*
                    \s*(?P<nexthop>nexthop\s(route-map\s\S+|trigger\s(delay\s\d+|enable)))*
                    \s*(?P<redistribute_internal>redistribute-internal)*
                    \s*(?P<route_map>route-map\spriority)*
                    \s*(?P<scan_time>scan-time\s\d+)*
                    \s*(?P<soft_reconfig_backup>soft-reconfig-backup)*
                    \s*(?P<update_group>update-group\ssplit\sas-override)*
                    $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_bgp_af_config,
            "compval": "bgp",
            "result": {
                "address_family": {
                    "{{ afi|d() + '_' + safi|d() + '_' + vrf|d() }}": {
                        "bgp": {
                            "aggregate_timer": "{{ aggregate_timer.split('aggregate-timer ')[1] if aggregate_timer is defined }}",
                            "dmzlink_bw": "{{ True if dmzlink_bw is defined }}",
                            "nexthop": {
                                "route_map": "{{ nexthop.split('route-map ')[1] if nexthop is defined and 'route-map' in nexthop }}",
                                "trigger": {
                                    "delay": "{{ nexthop.split('delay ')[1] if nexthop is defined and 'delay' in nexthop }}",
                                    "enable": "{{ True if nexthop is defined and 'enable' in nexthop }}",
                                },
                            },
                            "redistribute_internal": "{{ True if redistribute_internal is defined }}",
                            "route_map": "{{ True if route_map is defined }}",
                            "scan_time": "{{ scan_time.split('scan-time ')[1] if scan_time is defined }}",
                            "soft_reconfig_backup": "{{ True if soft_reconfig_backup is defined }}",
                            "update_group": "{{ True if update_group is defined }}",
                        }
                    }
                }
            },
        },
        {
            "name": "bgp.dampening",
            "getval": re.compile(
                r"""\s*bgp*
                    \s*dampening*
                    \s*(?P<penalty_half_time>\d+)*
                    \s*(?P<reuse_route_val>\d+)*
                    \s*(?P<suppress_route_val>\d+)*
                    \s*(?P<max_suppress>\d+)*
                    \s*(?P<route_map>\S+)*
                    $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_bgp_af_dampening,
            "result": {
                "address_family": {
                    "{{ afi|d() + '_' + safi|d() + '_' + vrf|d() }}": {
                        "bgp": {
                            "dampening": {
                                "penalty_half_time": "{{ penalty_half_time if penalty_half_time is defined }}",
                                "reuse_route_val": "{{ reuse_route_val if penalty_half_time is defined }}",
                                "suppress_route_val": "{{ suppress_route_val if penalty_half_time is defined }}",
                                "max_suppress": "{{ max_suppress if penalty_half_time is defined }}",
                                "route_map": "{{ dampening.split('route-map ')[1] if dampening is defined and 'route-map' in dampening }}",
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "bgp.slow_peer",
            "getval": re.compile(
                r"""\s*bgp*
                    \s*(?P<slow_peer>slow-peer((\sdetection\sthreshold\s\d+|\sdetection)|(\ssplit-update-group\sdynamic\spermanent|\ssplit-update-group\sdynamic)))*
                    $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_bgp_af_slow_peer,
            "compval": "bgp",
            "result": {
                "address_family": {
                    "{{ afi|d() + '_' + safi|d() + '_' + vrf|d() }}": {
                        "bgp": {
                            "slow_peer": [
                                {
                                    "detection": {
                                        "set": "{{ True if slow_peer is defined and 'detection' in slow_peer and 'threshold' not in slow_peer }}",
                                        "threshold": "{{ slow_peer.split('threshold ')[1] if slow_peer is defined and 'threshold' in slow_peer }}",
                                    },
                                    "split_update_group": {
                                        "dynamic": "{{ True if slow_peer is defined and 'split-update-group' in slow_peer and\
                                            'dynamic' in slow_peer }}",
                                        "permanent": "{{ True if slow_peer is defined and 'split-update-group' in slow_peer and\
                                            'permanent' in slow_peer }}",
                                    },
                                }
                            ]
                        }
                    }
                }
            },
        },
        {
            "name": "default",
            "getval": re.compile(
                r"""\s*(?P<default>default)*
                    $""",
                re.VERBOSE,
            ),
            "setval": "default",
            "result": {
                "address_family": {
                    "{{ afi|d() + '_' + safi|d() + '_' + vrf|d() }}": {
                        "default": "{{ True if default is defined }}"
                    }
                }
            },
        },
        {
            "name": "default_information",
            "getval": re.compile(
                r"""\s*(?P<default>default-information\soriginate)*
                    $""",
                re.VERBOSE,
            ),
            "setval": "default-information originate",
            "result": {
                "address_family": {
                    "{{ afi|d() + '_' + safi|d() + '_' + vrf|d() }}": {
                        "default_information": "{{ True if default_information is defined }}"
                    }
                }
            },
        },
        {
            "name": "default_metric",
            "getval": re.compile(
                r"""\s*(?P<default_metric>default-metric\s\d+)*
                    $""",
                re.VERBOSE,
            ),
            "setval": "default-metric {{ default_metric }}",
            "result": {
                "address_family": {
                    "{{ afi|d() + '_' + safi|d() + '_' + vrf|d() }}": {
                        "default_metric": "{{ default_metric.split('default-metric ')[1] if default_metric is defined }}"
                    }
                }
            },
        },
        {
            "name": "distance",
            "getval": re.compile(
                r"""\s*distance\sbgp(?P<distance>\s\d+\s\d+\s\d+)*
                    $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_af_distance,
            "result": {
                "address_family": {
                    "{{ afi|d() + '_' + safi|d() + '_' + vrf|d() }}": {
                        "distance": {
                            "external": "{{ distance.split(' ')[1] }}",
                            "internal": "{{ distance.split(' ')[2] }}",
                            "local": "{{ distance.split(' ')[3] }}",
                        }
                    }
                }
            },
        },
        {
            "name": "neighbor",
            "getval": re.compile(
                r"""\s*neighbor*
                    \s*(?P<neighbor>(?:[0-9]{1,3}\.){3}[0-9]{1,3}|host\s(?:[0-9]{1,3}\.){3}[0-9]{1,3}|(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))\S+|\S+)*
                    \s*(?P<activate>activate)*
                    \s*(?P<additional_paths>additional-paths\s(disable|receive|send))*
                    \s*(?P<advertise>advertise\sadditional-paths\sall\sbest\s\d+\sgroup-best|advertise\sadditional-paths\sbest\s\d+\sgroup-best|advertise\sadditional-paths\sall\sgroup-best|advertise\sbest-external|advertise\sdiverse-path\sbackup\smpath|advertise\sdiverse-path\sbackup|advertise\sdiverse-path\smpath)*
                    \s*(?P<advertisement_interval>advertisement-interval\s\d+)*
                    \s*(?P<aigp>aigp\ssend\scost-community\s\d+\spoi\sigp-cost\stransitive|aigp\ssend\scost-community\s\d+\spoi\spre-bestpath\stransitive|aigp\ssend\smed|aigp)*
                    \s*(?P<allow_policy>allow-policy)*
                    \s*(?P<allowas_in>allowas-in\s\d+)*
                    \s*(?P<as_override>as-override)*
                    \s*(?P<bmp_activate>bmp-activate\s(all|server\s\d+))*
                    \s*(?P<capability>capability\s(both|receive|send))*
                    \s*(?P<cluster_id>cluster-id\s\S+)*
                    \s*(?P<default_originate>default-originate\sroute-map|default-originate)*
                    \s*(?P<description>description\s\S.+)*
                    \s*(?P<disable_connected_check>disable-connected-check)*
                    \s*(?P<distribute_list>distribute-list\s\d+\s(in|out))*
                    \s*(?P<dmzlink_bw>dmzlink-bw)*
                    \s*(?P<ebgp_multihop>(ebgp-multihop\s\d+|ebgp-multihop))*
                    \s*(?P<fall_over>fall-over\s((bfd\s(single-hop|multi-hop)|bfd)|route-map\s\S+))*
                    \s*(?P<filter_list>filter-list\s\d+\s(in|out))*
                    \s*(?P<ha_mode>ha-mode\s(graceful-restart\sdisable|graceful-restart))*
                    \s*(?P<inherit>inherit\speer-session\s\S+)*
                    \s*(?P<local_as>(local-as\s\d+\s(dual-as|(no-prepend\sreplace-as|no-prepend))|local-as))*
                    \s*(?P<log_neighbor_changes>log-neighbor-changes\sdisable|log-neighbor-changes)*
                    \s*(?P<maximum_prefix>maximum-prefix\s(\d+\s\d+\s(restart\s\d+|warning-only)|\d+\s(restart\s\d+|warning-only)))*
                    \s*(?P<next_hop_self>next-hop-self\sall|next-hop-self)*
                    \s*(?P<next_hop_unchanged>next-hop-unchanged\sallpaths|next-hop-unchanged)*
                    \s*(?P<password>password\s\S+)*
                    \s*(?P<path_attribute>path-attribute\s(discard\srange\s\d+\s\d+\sin|discard\s\d+\sin)|path-attribute\s(treat-as-withdraw\srange\s\d+\s\d+\sin|treat-as-withdraw\s\d+\sin))*
                    \s*(?P<peer_group>peer-group\s\S+|peer-group)*
                    \s*(?P<prefix_list>prefix-list\s\S+\s(in|out))*
                    \s*(?P<remove_private_as>remove-private-as\sall\sreplace-as|remove-private-as\sall|remove-private-as)*
                    \s*(?P<remote_as>remote-as\s\d+)*
                    \s*(?P<route_map>route-map\s\S+\s(in|out))*
                    \s*(?P<route_reflector_client>route-reflector-client)*
                    \s*(?P<route_server_client>route-server-client\scontext\s\S+|route-server-client)*
                    \s*(?P<send_community>send-community\s(both|extended|standard)|send-community)*
                    \s*(?P<soft_reconfiguration>soft-reconfiguration\sinbound)*
                    \s*(?P<timers>(timers\s\d+\s\d+\s\d+|timers\s\d+\s\d+))*
                    \s*(?P<transport>(transport\s(connection-mode\sactive|connection-mode\spassive)|transport\smulti-session|transport\s(path-mtu-discovery\sdisable|path-mtu-discovery)))*
                    \s*(?P<ttl_security>ttl-security\shops\s\d+)*
                    \s*(?P<unsuppress_map>unsuppress-map\s\S+)*
                    \s*(?P<version>version\s\d+)*
                    \s*(?P<weight>weight\s\d+)*
                    $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_af_neighbor,
            "compval": "neighbor",
            "result": {
                "address_family": {
                    "{{ afi|d() + '_' + safi|d() + '_' + vrf|d() }}": {
                        "neighbor": [
                            {
                                "address": "{{ neighbor if ':' not in neighbor and '.' in neighbor }}",
                                "ipv6_address": "{{ neighbor if ':' in neighbor and '.' in neighbor }}",
                                "tag": "{{ neighbor if ':' not in neighbor and '.' not in neighbor }}",
                                "activate": "{{ True if activate is defined }}",
                                "additional_paths": {
                                    "disable": "{{ True if additional_paths is defined and 'disable' in additional_paths }}",
                                    "receive": "{{ True if additional_paths is defined and 'receive' in additional_paths }}",
                                    "send": "{{ True if additional_paths is defined and 'send' in additional_paths }}",
                                },
                                "advertise": {
                                    "additional_paths": {
                                        "all": "{{ True if advertise is defined and 'additional-paths' in advertise and 'all' in advertise }}",
                                        "best": "{{ advertise.split('best ')[1].split(' ')[0] if advertise is defined and\
                                            'additional-paths' in advertise and 'best' in advertise }}",
                                        "group_best": "{{ True if advertise is defined and 'additional-paths' in advertise and\
                                            'group-best' in advertise }}",
                                    },
                                    "best_external": "{{ True if advertise is defined and 'best-external' in advertise }}",
                                    "diverse_path": {
                                        "backup": "{{ True if advertise is defined and 'diverse-path' in advertise and 'backup' in advertise }}",
                                        "mpath": "{{ True if advertise is defined and 'diverse-path' in advertise and 'mpath' in advertise }}",
                                    },
                                },
                                "advertisement_interval": "{{ advertisement_interval.split('advertisement-interval ')[1] if advertisement_interval is defined\
                                    }}",
                                "aigp": {
                                    "enable": "{{ True if aigp is defined and aigp.split(' ')|length == 1 }}",
                                    "send": {
                                        "cost_community": {
                                            "id": "{{ aigp.split('send cost-community ')[1].split(' ')[0] if aigp is defined and\
                                                'send cost-community' in aigp }}",
                                            "poi": {
                                                "igp_cost": "{{ True if aigp is defined and 'poi igp-cost' in aigp }}",
                                                "pre_bestpath": "{{ True if aigp is defined and 'poi pre-bestpath' in aigp }}",
                                                "transitive": "{{ True if aigp is defined and 'transitive' in aigp }}",
                                            },
                                        },
                                        "med": "{{ True if aigp is defined and 'send med' in aigp }}",
                                    },
                                },
                                "allow_policy": "{{ True if allow_policy is defined }}",
                                "allowas_in": "{{ allowas_in.split('allowas-in ')[1] if allowas_in is defined }}",
                                "as_override": "{{ True if as_override is defined }}",
                                "bmp_activate": {
                                    "all": "{{ True if bmp_activate is defined and 'all' in bmp_activate }}",
                                    "server": "{{ bmp_activate.split('server ')[1] if bmp_activate is defined and 'server' in bmp_activate }}",
                                },
                                "capability": {
                                    "both": "{{ True if capability is defined and 'both' in capability }}",
                                    "receive": "{{ True if capability is defined and 'receive' in capability }}",
                                    "send": "{{ True if capability is defined and 'send' in capability }}",
                                },
                                "cluster_id": "{{ cluster_id.split('cluster-id ')[1] if bmp_activate is defined }}",
                                "default_originate": {
                                    "set": "{{ True if default_originate is defined and default_originate.split(' ')|length == 1 }}",
                                    "route_map": "{{ default_originate.split(' ')[1] if default_originate is defined and\
                                        default_originate.split(' ')|length > 1 }}",
                                },
                                "description": "{{ description.split('description ')[1] if description is defined }}",
                                "distribute_list": {
                                    "acl": "{{ distribute_list.split(' ')[1] if distribute_list is defined }}",
                                    "in": "{{ True if distribute_list is defined and 'in' in distribute_list }}",
                                    "out": "{{ True if distribute_list is defined and 'out' in distribute_list }}",
                                },
                                "disable_connected_check": "{{ True if disable_connected_check is defined }}",
                                "dmzlink_bw": "{{ True if dmzlink_bw is defined }}",
                                "ebgp_multihop": {
                                    "enable": "{{ True if ebgp_multihop is defined and ebgp_multihop.split(' ')|length == 1 }}",
                                    "hop_count": "{{ ebgp_multihop.split(' ')[1] if ebgp_multihop is defined and len(ebgp_multihop.split(' ')) > 1 }}",
                                },
                                "filter_list": {
                                    "acl": "{{ filter_list.split(' ')[1] if filter_list is defined }}",
                                    "in": "{{ True if filter_list is defined and 'in' in filter_list }}",
                                    "out": "{{ True if filter_list is defined and 'out' in filter_list }}",
                                },
                                "ha_mode": {
                                    "set": "{{ True if ha_mode is defined and 'disable' not in ha_mode }}",
                                    "disable": "{{ True if ha_mode is defined and 'disable' in ha_mode }}",
                                },
                                "inherit": "{{ inherit.split('inherit peer-session ')[1] if inherit is defined }}",
                                "local_as": {
                                    "set": "{{ True if local_as is defined and local_as.split(' ')|length == 1 }}",
                                    "number": "{{ local_as.split(' ')[1] if local_as is defined and local_as.split(' ')|length > 1 }}",
                                    "dual_as": "{{ True if local_as is defined and local_as.split(' ')|length > 2 and 'dual-as' in local_as }}",
                                    "no_prepend": {
                                        "set": "{{\
                                            True if local_as is defined and\
                                                local_as.split(' ')|length > 2 and 'no-prepend' in local_as and\
                                                    'replace-as' not in local_as }}",
                                        "replace_as": "{{ True if local_as is defined and\
                                            local_as.split(' ')|length > 2 and 'no-prepend' in local_as and 'replace-as' in local_as }}",
                                    },
                                },
                                "log_neighbor_changes": {
                                    "set": "{{ True if log_neighbor_changes is defined and 'disable' not in log_neighbor_changes }}",
                                    "disable": "{{ True if log_neighbor_changes is defined and 'disable' in log_neighbor_changes }}",
                                },
                                "maximum_prefix": {
                                    "number": "{{ maximum_prefix.split(' ')[1] if maximum_prefix is defined }}",
                                    "threshold_value": "{{ maximum_prefix.split(' ')[2] if maximum_prefix is defined and\
                                        maximum_prefix.split(' ')|length > 3 and maximum_prefix.split(' ')[1] != 'restart' }}",
                                    "restart": "{{ maximum_prefix.split('restart ')[1] if maximum_prefix is defined and 'restart' in maximum_prefix }}",
                                    "warning_only": "{{ True if maximum_prefix is defined and 'warning-only' in maximum_prefix }}",
                                },
                                "next_hop_self": {
                                    "set": "{{ True if next_hop_self is defined and next_hop_self.split(' ')|length == 1 }}",
                                    "all": "{{ True if next_hop_self is defined and next_hop_self.split(' ')|length > 1 }}",
                                },
                                "next_hop_unchanged": {
                                    "set": "{{ True if next_hop_unchanged is defined and next_hop_unchanged.split(' ')|length == 1 }}",
                                    "allpaths": "{{ True if next_hop_unchanged is defined and next_hop_unchanged.split(' ')|length > 1 }}",
                                },
                                "prefix_list": {
                                    "name": "{{ prefix_list.split(' ')[1] if prefix_list is defined }}",
                                    "in": "{{ True if prefix_list is defined and 'in' in prefix_list }}",
                                    "out": "{{ True if prefix_list is defined and 'out' in prefix_list }}",
                                },
                                "password": "{{ password.split(' ')[1] if password is defined }}",
                                "path_attribute": {
                                    "discard": {
                                        "type": "{% if path_attribute is defined and 'discard range' in path_attribute and\
                                            path_attribute.split(' ')|length <= 5 %}{{ path_attribute.split(' ')[3] }}{% endif %}",
                                        "range": {
                                            "start": "{% if path_attribute is defined and 'discard range' in path_attribute and\
                                                path_attribute.split(' ')|length > 5 %}{{ path_attribute.split(' ')[3] }}{% endif %}",
                                            "end": "{% if path_attribute is defined and 'discard range' in path_attribute and\
                                                path_attribute.split(' ')|length > 5 %}{{ path_attribute.split(' ')[4] }}{% endif %}",
                                        },
                                        "in": "{% if path_attribute is defined and 'discard range' in path_attribute and\
                                            'in' in path_attribute %}{{ True }}{% endif %}",
                                    },
                                    "treat_as_withdraw": {
                                        "type": "{% if path_attribute is defined and 'discard treat-as-withdraw' in path_attribute and\
                                            path_attribute.split(' ')|length <= 5 %}{{ path_attribute.split(' ')[3] }}{% endif %}",
                                        "range": {
                                            "start": "{% if path_attribute is defined and 'discard treat-as-withdraw' in path_attribute and\
                                                path_attribute.split(' ')|length > 5 %}{{ path_attribute.split(' ')[3] }}{% endif %}",
                                            "end": "{% if path_attribute is defined and 'discard treat-as-withdraw' in path_attribute and\
                                                path_attribute.split(' ')|length > 5 %}{{ path_attribute.split(' ')[4] }}{% endif %}",
                                        },
                                        "in": "{% if path_attribute is defined and 'discard treat-as-withdraw' in path_attribute and\
                                            'in' in path_attribute %}{{ True }}{% endif %}",
                                    },
                                },
                                "peer_group": "{{ True if peer_group is defined }}",
                                "remote_as": "{{ remote_as.split('remote-as ')[1] if remote_as is defined }}",
                                "remove_private_as": {
                                    "set": "{{ True if remove_private_as is defined and remove_private_as.split(' ')|length == 1 }}",
                                    "all": "{{ True if remove_private_as is defined and remove_private_as.split(' ')|length > 1 and\
                                        'all' in remove_private_as }}",
                                    "replace_as": "{{ True if remove_private_as is defined and remove_private_as.split(' ')|length > 1 and\
                                        'replace-as' in remove_private_as }}",
                                },
                                "route_map": {
                                    "name": "{{ route_map.split(' ')[1] if route_map is defined }}",
                                    "in": "{{ True if route_map is defined and 'in' in route_map.split(' ') }}",
                                    "out": "{{ True if route_map is defined and 'out' in route_map.split(' ') }}",
                                },
                                "route_reflector_client": "{{ True if route_reflector_client is defined }}",
                                "route_server_client": "{{ True if route_server_client is defined }}",
                                "send_community": {
                                    "set": "{{ True if send_community is defined and send_community.split(' ')|length == 1 }}",
                                    "both": "{{ True if send_community is defined and 'both' in send_community }}",
                                    "extended": "{{ True if send_community is defined and 'extended' in send_community }}",
                                    "standard": "{{ True if send_community is defined and 'standard' in send_community }}",
                                },
                                "soft_reconfiguration": "{{ True if soft_reconfiguration is defined }}",
                                "timers": {
                                    "interval": "{{ timers.split(' ')[1] if timers is defined }}",
                                    "holdtime": "{{ timers.split(' ')[2] if timers is defined }}",
                                    "min_holdtime": "{{ timers.split(' ')[3] if timers is defined and timers.split(' ')|length > 3 }}",
                                },
                                "transport": {
                                    "connection_mode": {
                                        "active": "{{ True if transport is defined and 'connection-mode active' in transport }}",
                                        "passive": "{{ True if transport is defined and 'connection-mode passive' in transport }}",
                                    },
                                    "multi_session": "{{ True if transport is defined and 'multi-session' in transport }}",
                                    "path_mtu_discovery": {
                                        "set": "{{ True if transport is defined and 'path-mtu-discovery' in transport and 'disable' not in transport }}",
                                        "disable": "{{ True if transport is defined and 'path-mtu-discovery' in transport and 'disable' in transport }}",
                                    },
                                },
                                "ttl_security": "{{ ttl_security.split('ttl-security hops ')[1] if ttl_security is defined }}",
                                "unsuppress_map": "{{ unsuppress_map.split('unsuppress-map ')[1] if unsuppress_map is defined }}",
                                "version": "{{ version.split('version ')[1] if version is defined }}",
                                "weight": "{{ weight.split('weight ')[1] if weight is defined }}",
                            }
                        ]
                    }
                }
            },
        },
        {
            "name": "neighbor.slow_peer",
            "getval": re.compile(
                r"""\s*neighbor*
                    \s*(?P<neighbor>(?:[0-9]{1,3}\.){3}[0-9]{1,3}|host\s(?:[0-9]{1,3}\.){3}[0-9]{1,3}|(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))\S+|\S+)*
                    \s*(?P<slow_peer>slow-peer\s(detection.*|split-update-group.*))*
                    $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_neighbor_af_slow_peer,
            "compval": "neighbor",
            "result": {
                "address_family": {
                    "{{ afi|d() + '_' + safi|d() + '_' + vrf|d() }}": {
                        "neighbor": [
                            {
                                "address": "{{ neighbor if ':' not in neighbor and '.' in neighbor }}",
                                "ipv6_address": "{{ neighbor if ':' in neighbor and '.' in neighbor }}",
                                "tag": "{{ neighbor if ':' not in neighbor and '.' not in neighbor }}",
                                "slow_peer": [
                                    {
                                        "detection": {
                                            "enable": "{{ True if slow_peer is defined and 'detection' in slow_peer and\
                                                'disable' not in slow_peer and 'threshold' not in slow_peer }}",
                                            "disable": "{{ True if slow_peer is defined and 'disable' in slow_peer }}",
                                            "threshold": "{{ slow_peer.split('threshold ')[1] if slow_peer is defined and 'threshold' in slow_peer }}",
                                        },
                                        "split_update_group": {
                                            "dynamic": {
                                                "enable": "{{ True if slow_peer is defined and 'split-update-group' in slow_peer and\
                                                    'disable' not in slow_peer and 'threshold' not in slow_peer }}",
                                                "disable": "{{ True if slow_peer is defined and 'split-update-group' in slow_peer and\
                                                    'disable' in slow_peer }}",
                                                "permanent": "{{ True if slow_peer is defined and 'split-update-group' in slow_peer and\
                                                    'permanent' in slow_peer }}",
                                            },
                                            "static": "{{ True if slow_peer is defined and 'split-update-group' in slow_peer and 'static' in slow_peer }}",
                                        },
                                    }
                                ],
                            }
                        ]
                    }
                }
            },
        },
        {
            "name": "network",
            "getval": re.compile(
                r"""\s*network*
                    \s*(?P<address>(?:[0-9]{1,3}\.){3}[0-9]{1,3}|(?:[0-9]{1,3}\.){3}[0-9]{1,3}|(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))\S+|\S+)*
                    \s*(?P<mask>mask\s(?:[0-9]{1,3}\.){3}[0-9]{1,3})*
                    \s*(?P<backdoor>backdoor)*
                    \s*(?P<route_map>route-map\s\S+)*
                    $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_af_network,
            "result": {
                "address_family": {
                    "{{ afi|d() + '_' + safi|d() + '_' + vrf|d() }}": {
                        "network": [
                            {
                                "address": "{{ address if address is defined }}",
                                "mask": "{{ mask.split('mask ')[1] if mask is defined }}",
                                "backdoor": "{{ True if backdoor is defined }}",
                                "route_map": "{{ route_map.split('route-map ')[1] if route_map is defined }}",
                            }
                        ]
                    }
                }
            },
        },
        {
            "name": "snmp",
            "getval": re.compile(
                r"""\s*snmp*
                    \s*(?P<context>context\s\S+)*
                    \s*(?P<community>community\s\S+)*
                    \s*(?P<user>user\s\S+)*
                    \s*(?P<ro>ro|RO)*
                    \s*(?P<rw>rw|RW)*
                    \s*(?P<credential>credential\s\S+)*
                    \s*(?P<encrypted>encrypted)*
                    \s*(?P<auth>auth)*
                    \s*(?P<md5>md5\s\S+)*
                    \s*(?P<sha>sha\s\S+)*
                    \s*(?P<priv>priv\s(3des\s\S+|aes\s128\s\S+|aes\s192\s\S+|aes\s256\s\S+|des\s\S+))*
                    \s*(?P<access>access\s(ipv6\s\S+|\S+))*
                    \s*(?P<acl>ipv6\s\S+|\S+)*
                    $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_af_snmp,
            "result": {
                "address_family": {
                    "{{ afi|d() + '_' + safi|d() + '_' + vrf|d() }}": {
                        "snmp": {
                            "context": {
                                "name": "{{ context.split('context ')[1] if context is defined }}",
                                "community": {
                                    "snmp_community": "{{ community.split('community ')[1] if community is defined }}",
                                    "acl": "{{ acl if acl is defined and 'ipv6' not in acl }}",
                                    "ro": "{{ True if ro is defined }}",
                                    "rw": "{{ True if rw is defined }}",
                                    "ipv6": "{{ acl.split('ipv6 ')[1] if acl is defined and 'ipv6' in acl }}",
                                },
                                "user": {
                                    "name": "{{ user.split('user ')[1] if user is defined }}",
                                    "access": {
                                        "acl": "{{ access.split('access ')[1] if access is defined and 'ipv6' not in access }}",
                                        "ipv6": "{{ access.split('access ipv6 ')[1] if access is defined and 'ipv6' in access }}",
                                    },
                                    "auth": {
                                        "md5": "{{ md5.split('md5 ')[1] if md5 is defined }}",
                                        "sha": "{{ sha.split('sha ')[1] if sha is defined }}",
                                    },
                                    "priv": {
                                        "3des": "{{ priv.split('priv 3des ')[1] if priv is defined and '3des' in priv }}",
                                        "aes": {
                                            "128": "{{ priv.split('priv aes 128 ')[1] if priv is defined and 'aes 128' in priv }}",
                                            "192": "{{ priv.split('priv aes 192 ')[1] if priv is defined and 'aes 192' in priv }}",
                                            "256": "{{ priv.split('priv aes 256 ')[1] if priv is defined and 'aes 256' in priv }}",
                                        },
                                        "des": "{{ priv.split('priv des ')[1] if priv is defined and 'des' in priv }}",
                                    },
                                    "credential": "{{ True if credential is defined }}",
                                    "encrypted": "{{ True if encrypted is defined }}",
                                },
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "table_map",
            "getval": re.compile(
                r"""\s*table-map*
                    \s*(?P<name>\S+)*
                    \s*(?P<filter>filter)*
                    $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_af_table_map,
            "result": {
                "address_family": {
                    "{{ afi|d() + '_' + safi|d() + '_' + vrf|d() }}": {
                        "table_map": {
                            "name": "{{ name if name is defined }}",
                            "filter": "{{ True if filter is defined }}",
                        }
                    }
                }
            },
        },
    ]
