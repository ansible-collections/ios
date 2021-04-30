# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The Route_maps parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re
from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network_template import (
    NetworkTemplate,
)


def _tmplt_route_map_match(config_data):
    if (
        config_data.get("match")
        and not config_data["match"].get("ip")
        and not config_data["match"].get("ipv6")
    ):
        command = []
        match = config_data["match"]
        if match and match.get("additional_paths"):
            cmd = "match additional-paths advertise-set"
            if config_data["match"]["additional_paths"].get("all"):
                cmd += " all"
            if config_data["match"]["additional_paths"].get("best"):
                cmd += " best {best}".format(
                    **config_data["match"]["additional_paths"]
                )
            if config_data["match"]["additional_paths"].get("best_range"):
                cmd += " best-range"
                if config_data["match"]["additional_paths"]["best_range"].get(
                    "lower_limit"
                ):
                    cmd += " lower-limit {lower_limit}".format(
                        **config_data["match"]["additional_paths"][
                            "best_range"
                        ]
                    )
                if config_data["match"]["additional_paths"]["best_range"].get(
                    "upper_limit"
                ):
                    cmd += " upper-limit {upper_limit}".format(
                        **config_data["match"]["additional_paths"][
                            "best_range"
                        ]
                    )
            if config_data["match"]["additional_paths"].get("group_best"):
                cmd += " group-best"
            command.append(cmd)
        if match.get("as_path"):
            cmd = "match as-path "
            if match["as_path"].get("acls"):
                temp = []
                for k, v in iteritems(match["as_path"]["acls"]):
                    temp.append(str(v))
                cmd += " ".join(sorted(temp))
            command.append(cmd)
        if match.get("clns"):
            cmd = "match clns"
            if match["clns"].get("address"):
                cmd += " address {address}".format(**match["clns"])
            elif match["clns"].get("next_hop"):
                cmd = " next-hop {next_hop}".format(**match["clns"])
            elif match["clns"].get("route_source"):
                cmd = " route-source {route_source}".format(**match["clns"])
            command.append(cmd)
        if match.get("community"):
            cmd = "match community "
            temp = []
            for k, v in iteritems(match["community"]["name"]):
                temp.append(v)
            cmd += " ".join(sorted(temp))
            if match["community"].get("exact_match"):
                cmd += " exact-match"
            command.append(cmd)
        if match.get("extcommunity"):
            cmd = "match extcommunity "
            temp = []
            for k, v in iteritems(match["extcommunity"]):
                temp.append(v)
            cmd += " ".join(sorted(temp))
            command.append(cmd)
        if match.get("interfaces"):
            cmd = "match interface "
            temp = []
            for k, v in iteritems(match["interfaces"]):
                temp.append(v)
            cmd += " ".join(sorted(temp))
            command.append(cmd)
        if match.get("length"):
            command.append(
                "match length {minimum} {maximum}".format(**match["length"])
            )
        if match.get("local_preference"):
            cmd = "match local-preference "
            if match["local_preference"].get("value"):
                temp = []
                for k, v in iteritems(match["local_preference"]["value"]):
                    temp.append(v)
                cmd += " ".join(sorted(temp))
            command.append(cmd)
        if match.get("mdt_group"):
            cmd = "match mdt-group "
            if match["mdt_group"].get("acls"):
                temp = []
                for k, v in iteritems(match["mdt_group"]["acls"]):
                    temp.append(v)
                cmd += " ".join(sorted(temp))
            command.append(cmd)
        if match.get("metric"):
            cmd = "match metric"
            if match["metric"].get("external"):
                cmd += " external"
            if match["metric"].get("value"):
                cmd += " {value}".format(**match["metric"])
            if match["metric"].get("deviation"):
                cmd += " +-"
                if match["metric"].get("deviation_value"):
                    cmd += " {deviation_value}".format(**match["metric"])
            command.append(cmd)
        if match.get("mpls_label"):
            command.append("match mpls-label")
        if match.get("policy_lists"):
            cmd = "match policy-list "
            temp = []
            for k, v in iteritems(match["policy_lists"]):
                temp.append(v)
            cmd += " ".join(sorted(temp))
            command.append(cmd)
        if match.get("route_type"):
            cmd = "match route-type"
            if match["route_type"].get("external"):
                cmd += " external"
                if match["route_type"]["external"].get("type_1"):
                    cmd += " type-1"
                elif match["route_type"]["external"].get("type_2"):
                    cmd += " type-2"
            elif match["route_type"].get("internal"):
                cmd += " internal"
            elif match["route_type"].get("level_1"):
                cmd += " level-1"
            elif match["route_type"].get("level_2"):
                cmd += " level-2"
            elif match["route_type"].get("local"):
                cmd += " local"
            elif match["route_type"].get("nssa_external"):
                cmd += " nssa-external"
                if match["route_type"]["nssa_external"].get("type_1"):
                    cmd += " type-1"
                elif match["route_type"]["nssa_external"].get("type_2"):
                    cmd += " type-2"
            command.append(cmd)
        if match.get("rpki"):
            cmd = "match rpki"
            if match["rpki"].get("invalid"):
                cmd += " invalid"
            if match["rpki"].get("not_found"):
                cmd += " not-found"
            if match["rpki"].get("valid"):
                cmd += " valid"
            command.append(cmd)
        if match.get("security_group"):
            cmd = "match security-group"
            if match["security_group"].get("source"):
                cmd += " source tag "
                temp = []
                for k, v in iteritems(match["security_group"]["source"]):
                    temp.append(str(v))
                cmd += " ".join(sorted(temp))
            elif match["security_group"].get("destination"):
                cmd += " destination tag"
                for each in match["destination"]:
                    cmd += " {0}".format(each)
            command.append(cmd)
        if match.get("source_protocol"):
            cmd = "match source-protocol"
            if match["source_protocol"].get("bgp"):
                cmd += " bgp {bgp}".format(**match["source_protocol"])
            if match["source_protocol"].get("connected"):
                cmd += " connected"
            if match["source_protocol"].get("eigrp"):
                cmd += " eigrp {eigrp}".format(**match["source_protocol"])
            if match["source_protocol"].get("isis"):
                cmd += " isis"
            if match["source_protocol"].get("lisp"):
                cmd += " lisp"
            if match["source_protocol"].get("mobile"):
                cmd += " mobile"
            if match["source_protocol"].get("ospf"):
                cmd += " ospf {ospf}".format(**match["source_protocol"])
            if match["source_protocol"].get("ospfv3"):
                cmd += " ospfv3 {ospfv3}".format(**match["source_protocol"])
            if match["source_protocol"].get("rip"):
                cmd += " rip"
            if match["source_protocol"].get("static"):
                cmd += " static"
            command.append(cmd)
        if match.get("tag"):
            cmd = "match tag"
            if match["tag"].get("tag_list"):
                cmd += " list"
                for each in match["tag"]["tag_list"]:
                    cmd += " {0}".format(each)
            elif match["tag"].get("value"):
                for each in match["tag"]["value"]:
                    cmd += " {0}".format(each)
            command.append(cmd)
        if match.get("track"):
            command.append("match track {track}".format(**match))
        return command


def _tmplt_route_map_match_ip(config_data):
    if config_data.get("match") and config_data["match"].get("ip"):

        def construct_cmd_from_list(cmd, config):
            temp = []
            for k, v in iteritems(config):
                temp.append(v)
            cmd += " " + " ".join(sorted(temp))
            return cmd

        cmd = "match ip"
        if config_data["match"]["ip"].get("address"):
            cmd += " address"
            if config_data["match"]["ip"]["address"].get("prefix_lists"):
                cmd += " prefix-list"
                cmd = construct_cmd_from_list(
                    cmd, config_data["match"]["ip"]["address"]["prefix_lists"]
                )
            elif config_data["match"]["ip"]["address"].get("acls"):
                cmd = construct_cmd_from_list(
                    cmd, config_data["match"]["ip"]["address"]["acls"]
                )
        if config_data["match"]["ip"].get("flowspec"):
            cmd += " flowspec"
            if config_data["match"]["ip"]["flowspec"].get("dest_pfx"):
                cmd += " dest-pfx"
            elif config_data["match"]["ip"]["flowspec"].get("src_pfx"):
                cmd += " src-pfx"
            if config_data["match"]["ip"]["flowspec"].get("prefix_lists"):
                cmd += " prefix-list"
                cmd = construct_cmd_from_list(
                    cmd, config_data["match"]["ip"]["flowspec"]["prefix_lists"]
                )
            elif config_data["match"]["ip"]["flowspec"].get("acls"):
                cmd = construct_cmd_from_list(
                    cmd, config_data["match"]["ip"]["flowspec"]["acls"]
                )
        if config_data["match"]["ip"].get("next_hop"):
            cmd += " next-hop"
            if config_data["match"]["ip"]["next_hop"].get("prefix_lists"):
                cmd += " prefix-list"
                cmd = construct_cmd_from_list(
                    cmd, config_data["match"]["ip"]["next_hop"]["prefix_lists"]
                )
            elif config_data["match"]["ip"]["next_hop"].get("acls"):
                cmd = construct_cmd_from_list(
                    cmd, config_data["match"]["ip"]["next_hop"]["acls"]
                )
        if config_data["match"]["ip"].get("redistribution_source"):
            cmd += " redistribution-source"
            if config_data["match"]["ip"]["redistribution_source"].get(
                "prefix_lists"
            ):
                cmd += " prefix-list"
                cmd = construct_cmd_from_list(
                    cmd,
                    config_data["match"]["ip"]["redistribution_source"][
                        "prefix_lists"
                    ],
                )
            elif config_data["match"]["ip"]["redistribution_source"].get(
                "acls"
            ):
                cmd = construct_cmd_from_list(
                    cmd,
                    config_data["match"]["ip"]["redistribution_source"][
                        "acls"
                    ],
                )
        if config_data["match"]["ip"].get("route_source"):
            cmd += " route-source"
            if config_data["match"]["ip"]["route_source"].get(
                "redistribution_source"
            ):
                cmd += " redistribution-source"
            if config_data["match"]["ip"]["route_source"].get("prefix_lists"):
                cmd += " prefix-list"
                cmd = construct_cmd_from_list(
                    cmd,
                    config_data["match"]["ip"]["route_source"]["prefix_lists"],
                )
            elif config_data["match"]["ip"]["route_source"].get("acls"):
                cmd = construct_cmd_from_list(
                    cmd, config_data["match"]["ip"]["route_source"]["acls"]
                )
        return cmd


def _tmplt_route_map_match_ipv6(config_data):
    if config_data.get("match") and config_data["match"].get("ipv6"):
        cmd = "match ipv6"
        if config_data["match"]["ipv6"].get("address"):
            cmd += " address"
            if config_data["match"]["ipv6"]["address"].get("prefix_list"):
                cmd += " prefix-list {prefix_list}".format(
                    **config_data["match"]["ipv6"]["address"]
                )
            elif config_data["match"]["ipv6"]["address"].get("acl"):
                cmd += " {acl}".format(
                    **config_data["match"]["ipv6"]["address"]
                )
        if config_data["match"]["ipv6"].get("flowspec"):
            cmd += " flowspec"
            if config_data["match"]["ipv6"]["flowspec"].get("dest_pfx"):
                cmd += " dest-pfx"
            elif config_data["match"]["ipv6"]["flowspec"].get("src_pfx"):
                cmd += " src-pfx"
            if config_data["match"]["ipv6"]["flowspec"].get("prefix_list"):
                cmd += " prefix-list {prefix_list}".format(
                    **config_data["match"]["ipv6"]["flowspec"]
                )
            elif config_data["match"]["ipv6"]["flowspec"].get("acl"):
                cmd += " {acl}".format(
                    **config_data["match"]["ipv6"]["flowspec"]
                )
        if config_data["match"]["ipv6"].get("next_hop"):
            cmd += " next-hop"
            if config_data["match"]["ipv6"]["next_hop"].get("prefix_list"):
                cmd += " prefix-list {prefix_list}".format(
                    **config_data["match"]["ipv6"]["next_hop"]
                )
            elif config_data["match"]["ipv6"]["next_hop"].get("acl"):
                cmd += " {acl}".format(
                    **config_data["match"]["ipv6"]["next_hop"]
                )
        if config_data["match"]["ipv6"].get("route_source"):
            cmd += " route-source"
            if config_data["match"]["ipv6"]["route_source"].get("prefix_list"):
                cmd += " prefix-list {prefix_list}".format(
                    **config_data["match"]["ipv6"]["route_source"]
                )
            elif config_data["match"]["ipv6"]["route_source"].get("acl"):
                cmd += " {acl}".format(
                    **config_data["match"]["ipv6"]["route_source"]
                )
        return cmd


def _tmplt_route_map_set(config_data):
    if config_data.get("set"):
        command = []
        set = config_data["set"]
        if set.get("aigp_metric"):
            cmd = "set aigp-metric"
            if set["aigp_metric"].get("value"):
                cmd += " {value}".format(**set["aigp_metric"])
            elif set["aigp_metric"].get("igp_metric"):
                cmd += " igp-metric"
            command.append(cmd)
        if set.get("as_path"):
            cmd = "set as-path"
            if set["as_path"].get("prepend"):
                cmd += " prepend"
                if set["as_path"]["prepend"].get("as_number"):
                    cmd += " {as_number}".format(**set["as_path"]["prepend"])
                elif set["as_path"]["prepend"].get("last_as"):
                    cmd += " last-as {last_as}".format(
                        **set["as_path"]["prepend"]
                    )
            if set["as_path"].get("tag"):
                cmd += " tag"
            command.append(cmd)
        if set.get("automatic_tag"):
            command.append("set automatic-tag")
        if set.get("clns"):
            command.append("set clns next-hop {clns}".format(**set))
        if set.get("comm_list"):
            command.append("set comm-list {comm_list} delete".format(**set))
        if set.get("community"):
            cmd = "set community"
            if set["community"].get("number"):
                cmd += " {number}".format(**set["community"])
            if set["community"].get("additive"):
                cmd += " additive"
            if set["community"].get("gshut"):
                cmd += " gshut"
            if set["community"].get("internet"):
                cmd += " internet"
            if set["community"].get("local_as"):
                cmd += " local-as"
            if set["community"].get("no_advertise"):
                cmd += " no-advertise"
            if set["community"].get("no_export"):
                cmd += " no-export"
            if set["community"].get("none"):
                cmd += " none"
            command.append(cmd)
        if set.get("dampening"):
            command.append(
                "set dampening {penalty_half_time} {reuse_route_val} {suppress_route_val} {max_suppress}".format(
                    **set["dampening"]
                )
            )
        if set.get("default"):
            command.append(
                "set default interface {default}".format(**set["default"])
            )
        if set.get("extcomm_list"):
            command.append(
                "set extcomm-list {extcomm_list} delete".format(**set)
            )
        if set.get("extcommunity"):
            if set["extcommunity"].get("cost"):
                cmd = "set extcommunity cost"
                if set["extcommunity"]["cost"].get("igp"):
                    cmd += " igp"
                elif set["extcommunity"]["cost"].get("pre_bestpath"):
                    cmd += " pre-bestpath"
                if set["extcommunity"]["cost"].get("id"):
                    cmd += " {id}".format(**set["extcommunity"]["cost"])
                if set["extcommunity"]["cost"].get("cost_value"):
                    cmd += " {cost_value}".format(
                        **set["extcommunity"]["cost"]
                    )
                command.append(cmd)
            if set["extcommunity"].get("rt"):
                cmd = "set extcommunity rt"
                if set["extcommunity"]["rt"].get("range"):
                    cmd += " range {lower_limit} {upper_limit}".format(
                        **set["extcommunity"]["rt"]["range"]
                    )
                elif set["extcommunity"]["rt"].get("address"):
                    cmd += " {address}".format(**set["extcommunity"]["rt"])
                if set["extcommunity"]["rt"].get("additive"):
                    cmd += " additive"
                command.append(cmd)
            if set["extcommunity"].get("soo"):
                command.append(
                    "set extcommunity soo {soo}".format(**set["extcommunity"])
                )
            if set["extcommunity"].get("vpn_distinguisher"):
                cmd = "set extcommunity vpn-distinguisher"
                if set["extcommunity"]["vpn_distinguisher"].get("range"):
                    cmd += " range {lower_limit} {upper_limit}".format(
                        **set["extcommunity"]["vpn_distinguisher"]["range"]
                    )
                elif set["extcommunity"]["vpn_distinguisher"].get("address"):
                    cmd += " {address}".format(
                        **set["extcommunity"]["vpn_distinguisher"]
                    )
                if set["extcommunity"]["vpn_distinguisher"].get("additive"):
                    cmd += " additive"
                command.append(cmd)
        if set.get("global"):
            command.append("set global")
        if set.get("interfaces"):
            cmd = "set interface "
            temp = []
            for k, v in iteritems(set["interfaces"]):
                temp.append(v)
            cmd += " ".join(sorted(temp))
            command.append(cmd)
        if set.get("level"):
            cmd = "set level"
            if set["level"].get("level_1"):
                cmd += " level-1"
            elif set["level"].get("level_1_2"):
                cmd += " level-1-2"
            elif set["level"].get("level_2"):
                cmd += " level-2"
            elif set["level"].get("nssa_only"):
                cmd += " nssa-only"
        if set.get("lisp"):
            command.append("set lisp locator-set {lisp}".format(**set))
        if set.get("local_preference"):
            command.append(
                "set local-preference {local_preference}".format(**set)
            )
        if set.get("metric"):
            cmd = "set metric"
            if set["metric"].get("metric_value"):
                cmd += " {metric_value}".format(**set["metric"])
                if set["metric"].get("deviation"):
                    if set["metric"]["deviation"] == "plus":
                        cmd += " +{eigrp_delay} {metric_reliability} {metric_bandwidth} {mtu}".format(
                            **set["metric"]
                        )
                    elif set["metric"]["deviation"] == "minus":
                        cmd += " -{eigrp_delay} {metric_reliability} {metric_bandwidth} {mtu}".format(
                            **set["metric"]
                        )
            if set["metric"].get("deviation") and not set["metric"].get(
                "eigrp_delay"
            ):
                if set["metric"]["deviation"] == "plus":
                    cmd = "set metric +{metric_value}".format(**set["metric"])
                elif set["metric"]["deviation"] == "minus":
                    cmd = "set metric -{metric_value}".format(**set["metric"])
            command.append(cmd)
        if set.get("metric_type"):
            cmd = "set metric-type"
            if set["metric_type"].get("external"):
                cmd += " external"
            elif set["metric_type"].get("internal"):
                cmd += " internal"
            elif set["metric_type"].get("type_1"):
                cmd += " type-1"
            elif set["metric_type"].get("type_2"):
                cmd += " type-2"
            command.append(cmd)
        if set.get("mpls_label"):
            command.append("set mpls-label")
        if set.get("origin"):
            cmd = "set origin"
            if set["origin"].get("igp"):
                cmd += " igp"
            elif set["origin"].get("incomplete"):
                cmd += " incomplete"
        if set.get("tag"):
            command.append("set tag {tag}".format(**set))
        if set.get("traffic_index"):
            command.append("set traffic-index {traffic_index}".format(**set))
        if set.get("vrf"):
            command.append("set vrf {vrf}".format(**set))
        if set.get("weight"):
            command.append("set weight {weight}".format(**set))
        return command


def _tmplt_route_map_set_ip(config_data):
    if config_data.get("set") and config_data["set"].get("ip"):
        command = []
        set_ip = config_data["set"]["ip"]
        cmd = "set ip"
        if set_ip.get("address"):
            command.append(
                "{0} address prefix-list {address}".format(cmd, **set_ip)
            )
        if set_ip.get("df"):
            command.append("{0} df {df}".format(cmd, **set_ip))
        if set_ip.get("global_route"):
            cmd += " global next-hop"
            if set_ip["global_route"].get("verify_availability"):
                cmd += " verify-availability {address} {sequence} track {track}".format(
                    **set_ip["global_route"]["verify_availability"]
                )
            elif set_ip["global_route"].get("address"):
                cmd += " {address}".format(**set_ip["global_route"])
            command.append(cmd)
        if set_ip.get("next_hop"):
            cmd += " next-hop"
            if set_ip["next_hop"].get("address"):
                command.append(
                    "{0} {address}".format(cmd, **set_ip["next_hop"])
                )
            if set_ip["next_hop"].get("dynamic"):
                command.append("{0} dynamic dhcp".format(cmd))
            if set_ip["next_hop"].get("encapsulate"):
                command.append(
                    "{0} encapsulate l3vpn {encapsulate}".format(
                        cmd, **set_ip["next_hop"]
                    )
                )
            if set_ip["next_hop"].get("peer_address"):
                command.append("{0} peer-address".format(cmd))
            if set_ip["next_hop"].get("recursive"):
                child_cmd = "{0} recursive".format(cmd)
                if set_ip["next_hop"]["recursive"].get("global_route"):
                    child_cmd += " global"
                elif set_ip["next_hop"]["recursive"].get("vrf"):
                    child_cmd += " vrf {vrf}".format(
                        **set_ip["next_hop"]["recursive"]
                    )
                if set_ip["next_hop"]["recursive"].get("address"):
                    child_cmd += " {address}".format(
                        **set_ip["next_hop"]["recursive"]
                    )
                command.append(child_cmd)
            if set_ip["next_hop"].get("self"):
                command.append("{0} self".format(cmd))
            if set_ip["next_hop"].get("verify_availability"):
                command.append(
                    "{0} verify-availability {address} {sequence} track {track}".format(
                        cmd, **set_ip["next_hop"]["verify_availability"]
                    )
                )
        if set_ip.get("precedence"):
            cmd += " precedence"
            if set_ip["precedence"].get("critical"):
                cmd += " critical"
            elif set_ip["precedence"].get("flash"):
                cmd += " flash"
            elif set_ip["precedence"].get("flash_override"):
                cmd += " flash-override"
            elif set_ip["precedence"].get("immediate"):
                cmd += " immediate"
            elif set_ip["precedence"].get("internet"):
                cmd += " internet"
            elif set_ip["precedence"].get("network"):
                cmd += " network"
            elif set_ip["precedence"].get("priority"):
                cmd += " priority"
            elif set_ip["precedence"].get("routine"):
                cmd += " routine"
            command.append(cmd)
        if set_ip.get("qos_group"):
            command.append("{0} qos-group {qos_group}".format(cmd, **set_ip))
        if set_ip.get("tos"):
            cmd += " tos"
            if set_ip["tos"].get("max_reliability"):
                cmd += " max-reliability"
            elif set_ip["tos"].get("max_throughput"):
                cmd += " max-throughput"
            elif set_ip["tos"].get("min_delay"):
                cmd += " min-delay"
            elif set_ip["tos"].get("min_monetary_cost"):
                cmd += " min-monetary-cost"
            elif set_ip["tos"].get("normal"):
                cmd += " normal"
            command.append(cmd)
        if set_ip.get("vrf"):
            cmd += " vrf {vrf} next-hop".format(**set_ip)
            if set_ip["vrf"].get("verify_availability").get("address"):
                cmd += " verify-availability {address} {sequence} track {track}".format(
                    **set_ip["vrf"]["verify_availability"]
                )
            elif set_ip["vrf"].get("address"):
                cmd += " {address}".format(**set_ip["vrf"])
            command.append(cmd)
        return command


def _tmplt_route_map_set_ipv6(config_data):
    if config_data.get("set") and config_data["set"].get("ipv6"):
        set_ipv6 = config_data["set"]["ipv6"]
        cmd = "set ipv6"
        if set_ipv6.get("address"):
            cmd += " address prefix-list {address}".format(**set_ipv6)
        if set_ipv6.get("default"):
            cmd += " default"
        if set_ipv6.get("global_route"):
            cmd += " global next-hop"
            if set_ipv6["global_route"].get("verify_availability"):
                cmd += " verify-availability {address} {sequence} track {track}".format(
                    **set_ipv6["global_route"]["verify_availability"]
                )
            elif set_ipv6["global_route"].get("address"):
                cmd += " {address}".format(**set_ipv6["global_route"])
        if set_ipv6.get("next_hop"):
            cmd += " next-hop"
            if set_ipv6["next_hop"].get("address"):
                cmd += " {address}".format(**set_ipv6["next_hop"])
            if set_ipv6["next_hop"].get("encapsulate"):
                cmd += " encapsulate l3vpn {encapsulate}".format(
                    **set_ipv6["next_hop"]
                )
            if set_ipv6["next_hop"].get("peer_address"):
                cmd += " peer-address"
        if set_ipv6.get("precedence"):
            cmd += " precedence {precedence}".format(**set_ipv6)
        if set_ipv6.get("vrf"):
            cmd += " vrf {vrf} next-hop verify-availability {address} {sequence} track {track}".format(
                **set_ipv6["vrf"]["verify_availability"]
            )
        return cmd


class Route_mapsTemplate(NetworkTemplate):
    def __init__(self, lines=None):
        super(Route_mapsTemplate, self).__init__(lines=lines, tmplt=self)

    PARSERS = [
        {
            "name": "route_map",
            "getval": re.compile(
                r"""
                ^route-map*
                \s*(?P<route_map>\S+)*
                \s*(?P<action>deny|permit)*
                \s*(?P<sequence>\d+)*
                $""",
                re.VERBOSE,
            ),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "route_map": "{{ route_map }}",
                    "{{ action|d() + '_' + sequence|d() }}": {
                        "entries": {
                            "action": "{{ action }}",
                            "sequence": "{{ sequence }}",
                        }
                    },
                }
            },
            "shared": True,
        },
        {
            "name": "continue_entry",
            "getval": re.compile(
                r"""
                \s+continue*
                \s*(?P<entry_sequence>\d+)*
                $""",
                re.VERBOSE,
            ),
            "setval": "continue {{ continue_entry.entry_sequence }}",
            "result": {
                "{{ route_map }}": {
                    "{{ action|d() + '_' + sequence|d() }}": {
                        "entries": {
                            "continue_entry": {
                                "set": "{{ True if entry_sequence is not defined }}",
                                "entry_sequence": "{{ entry_sequence }}",
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "description",
            "getval": re.compile(
                r"""
                \s+description*
                \s*(?P<description>\S.*)*
                $""",
                re.VERBOSE,
            ),
            "setval": "description {{ description }}",
            "result": {
                "{{ route_map }}": {
                    "{{ action|d() + '_' + sequence|d() }}": {
                        "entries": {"description": "{{ description }}"}
                    }
                }
            },
        },
        {
            "name": "match",
            "getval": re.compile(
                r"""
                \s+match*
                \s*(?P<additional_paths>additional-paths\sadvertise-set\s\S.*)*
                \s*(?P<as_path>as-path.*|as-path)*
                \s*(?P<clns>clns\s(address\s\S+|next-hop\s\S+|route-source\s\S+))*
                \s*(?P<community>community\s\S.*)*
                \s*(?P<extcommunity>extcommunity\s\S.*)*
                \s*(?P<interfaces>interface\s\S.*)*
                \s*(?P<length>length\s\d+\s\d+)*
                \s*(?P<local_preference>local-preference\s\d.*|local-preference)*
                \s*(?P<mdt_group>mdt-group\s\S.*|mdt-group)*
                \s*(?P<metric>metric\sexternal\s\S.*|metric\s\d+\S.*)*
                \s*(?P<mpls_label>mpls-label)*
                \s*(?P<policy_list>policy-list\s\S.*)*
                \s*(?P<route_type>route-type\s(external\s(type-1|type-2)|internal|level-1|level-2|local|nssa-external\s(type-1|type-2)))*
                \s*(?P<rpki>rpki\s(invalid|not-found|valid))*
                \s*(?P<security_group>security-group\s(destination\stag\s\d.*|source\stag\s\d.*))*
                \s*(?P<source_protocol>source-protocol\s\S.*)*
                \s*(?P<tag>tag\slist\s\S.*|tag\s\S.*)*
                \s*(?P<track>track\s*\d+)*
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_route_map_match,
            "result": {
                "{{ route_map }}": {
                    "{{ action|d() + '_' + sequence|d() }}": {
                        "entries": {
                            "match": {
                                "additional_paths": {
                                    "all": "{{ True if additional_paths is defined and 'all' in additional_paths }}",
                                    "best": "{{ additional_paths.split('best ')[1].split(' ')[0]|int if additional_paths is defined and\
                                             'best' in additional_paths and 'best-range' not in additional_paths }}",
                                    "best_range": {
                                        "lower_limit": "{{ additional_paths.split('best-range ')[1].split(' ')[0]|int if additional_paths is defined and\
                                                 'best-range' in additional_paths }}",
                                        "upper_limit": "{{ additional_paths.split('best-range ')[1].split(' ')[1]|int if additional_paths is defined and\
                                                 'best-range' in additional_paths }}",
                                    },
                                    "group_best": "{{ True if additional_paths is defined and 'group-best' in additional_paths }}",
                                },
                                "as_path": {
                                    "set": "{{ True if as_path is defined and as_path.split(' ')|length == 1 }}",
                                    "acls": "{{ as_path.split('as-path ')[1].split(' ') if as_path is defined and as_path.split(' ')|length > 1 }}",
                                },
                                "clns": {
                                    "address": "{{ clns.split('clns address ')[1] if clns is defined }}",
                                    "next_hop": "{{ clns.split('clns next-hop ')[1] if clns is defined }}",
                                    "route_source": "{{ clns.split('clns route-source ')[1] if clns is defined }}",
                                },
                                "community": {
                                    "name": "{{ community.split('community ')[1].split(' exact-match')[0].split(' ') if community is defined }}",
                                    "exact_match": "{{ True if community is defined and 'exact-match' in community }}",
                                },
                                "extcommunity": "{{ extcommunity.split('extcommunity ')[1].split(' ') if extcommunity is defined }}",
                                "interfaces": "{{ interfaces.split('interface ')[1].split(' ') if interfaces is defined }}",
                                "length": {
                                    "minimum": "{{ length.split(' ')[1] if length is defined }}",
                                    "maximum": "{{ length.split(' ')[2] if length is defined }}",
                                },
                                "local_preference": {
                                    "set": "{{ True if local_preference is defined and local_preference.split(' ')|length == 1 }}",
                                    "value": "{{ local_preference.split('local-preference ')[1].split(' ') if local_preference is defined }}",
                                },
                                "mdt_group": {
                                    "set": "{{ True if mdt_group is defined and mdt_group.split(' ')|length == 1 }}",
                                    "acls": "{{ mdt_group.split('mdt-group ')[1].split(' ') if mdt_group is defined }}",
                                },
                                "metric": {
                                    "external": "{{ True if metric is defined and 'external' in metric.split(' ') }}",
                                    "value": "{% if metric is defined and 'external' not in metric.split(' ') %}{{ metric.split(' ')[1] }}\
                                            {% elif metric is defined and 'external' in metric.split(' ') %}{{ metric.split(' ')[2] }}\
                                            {% endif %}",
                                    "deviation": "{{ True if metric is defined and '+-' in metric }}",
                                    "deviation_value": "{% if metric is defined and 'external' in metric and '+-' in metric %}{{ metric.split(' ')[4] }}\
                                            {% elif metric is defined and 'external' not in metric and '+-' in metric %}{{ metric.split(' ')[3] }}{% endif %}",
                                },
                                "mpls_label": "{{ True if mpls_label is defined }}",
                                "policy_lists": "{{ policy_list.split('policy-list ')[1].split(' ') if policy_list is defined }}",
                                "route_type": {
                                    "external": {
                                        "set": "{{ True if route_type is defined and 'type-1' not in route_type and 'type-2' not in route_type}}",
                                        "type_1": "{{ True if route_type is defined and 'type-1' in route_type }}",
                                        "type_2": "{{ True if route_type is defined and 'type-2' in route_type }}",
                                    },
                                    "internal": "{{ True if route_type is defined and 'internal' in route_type }}",
                                    "level_1": "{{ True if route_type is defined and 'level-1' in route_type }}",
                                    "level_2": "{{ True if route_type is defined and 'level-2' in route_type }}",
                                    "local": "{{ True if route_type is defined and 'local' in route_type }}",
                                    "nssa_external": {
                                        "set": "{{ True if route_type is defined and 'type-1' not in route_type and 'type-2' not in route_type}}",
                                        "type_1": "{{ True if route_type is defined and 'type-1' in route_type }}",
                                        "type_2": "{{ True if route_type is defined and 'type-2' in route_type }}",
                                    },
                                },
                                "rpki": {
                                    "invalid": "{{ True if rpki is defined and 'invalid' in rpki and 'valid' not in rpki.split(' ') }}",
                                    "not_found": "{{ True if rpki is defined and 'not-found' in rpki }}",
                                    "valid": "{{ True if rpki is defined and 'valid' in rpki and 'invalid' not in rpki.split(' ') }}",
                                },
                                "security_group": {
                                    "destination": "{{ security_group.split('destination tag ')[1].split(' ') if security_group is defined and\
                                        'destination' in security_group }}",
                                    "source": "{{ security_group.split('source tag ')[1].split(' ') if security_group is defined and\
                                        'source' in security_group }}",
                                },
                                "source_protocol": {
                                    "bgp": "{{ source_protocol.split('bgp ')[1].split(' ')[0] if source_protocol is defined and 'bgp' in source_protocol }}",
                                    "connected": "{{ True if source_protocol is defined and 'connected' in source_protocol }}",
                                    "eigrp": "{{ source_protocol.split('eigrp ')[1].split(' ')[0] if source_protocol is defined and\
                                            'eigrp' in source_protocol }}",
                                    "isis": "{{ True if source_protocol is defined and 'isis' in source_protocol }}",
                                    "lisp": "{{ True if source_protocol is defined and 'lisp' in source_protocol }}",
                                    "mobile": "{{ True if source_protocol is defined and 'mobile' in source_protocol }}",
                                    "ospf": "{{ source_protocol.split('ospf ')[1].split(' ')[0] if source_protocol is defined and\
                                            'ospf' in source_protocol }}",
                                    "ospfv3": "{{ source_protocol.split('ospfv3 ')[1].split(' ')[0] if source_protocol is defined and\
                                            'ospfv3' in source_protocol }}",
                                    "rip": "{{ True if source_protocol is defined and 'rip' in source_protocol }}",
                                    "static": "{{ True if source_protocol is defined and 'static' in source_protocol }}",
                                },
                                "tag": {
                                    "value": "{{ tag.split('tag ')[1].split(' ') if tag is defined and 'list' not in tag }}",
                                    "tag_list": "{{ tag.split('tag list ')[1].split(' ') if tag is defined and 'list' in tag }}",
                                },
                                "track": "{{ track.split('track ')[1] if track is defined }}",
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "match.ip",
            "getval": re.compile(
                r"""
                \s+match*
                \s*(?P<ip>ip)*
                \s*(?P<address>address\sprefix-list\s\S.*|address\s\S.*)*
                \s*(?P<flowspec>flowspec\sdest-pfx\s(prefix-list\s\S.*|\S.*)|flowspec\ssrc-pfx\s(prefix-list\s\S.*|\S.*))*
                \s*(?P<next_hop>next-hop\sprefix-list\s\S.*|next-hop\s\S.*|next-hop)*
                \s*(?P<redistribution_source>redistribution-source\sprefix-list\s\S.*|redistribution-source\s\S.*|redistribution-source)*
                \s*(?P<route_source>route-source\sredistribution-source\sprefix-list\s\S.*|route-source\sredistribution-source\s\S.*|route-source\sprefix-list\s\S.*|route-source\s\S.*|route-source\sredistribution-source|route-source)*
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_route_map_match_ip,
            "compval": "match",
            "result": {
                "{{ route_map }}": {
                    "{{ action|d() + '_' + sequence|d() }}": {
                        "entries": {
                            "match": {
                                "ip": {
                                    "address": {
                                        "acls": "{{ address.split('address ')[1].split(' ') if address is defined and\
                                            'prefix-list' not in address else none }}",
                                        "prefix_lists": "{{ address.split('address prefix-list ')[1].split(' ') if address is defined and\
                                            'prefix-list' in address else None }}",
                                    },
                                    "flowspec": {
                                        "dest_pfx": "{{ True if flowspec is defined and 'dest-pfx' in flowspec }}",
                                        "src_pfx": "{{ True if flowspec is defined and 'src-pfx' in flowspec }}",
                                        "acls": "{{ flowspec.split('flowspec ')[1].split(' ')|d() if flowspec is defined and\
                                            'prefix-list' not in flowspec else '' }}",
                                        "prefix_lists": "{{ flowspec.split('flowspec prefix-list ')[1].split(' ')|d() if flowspec is defined and\
                                            'prefix-list' in flowspec else ''}}",
                                    },
                                    "next_hop": {
                                        "set": "{{ True if next_hop is defined and next_hop.split(' ')|length == 1 }}",
                                        "acls": "{{ next_hop.split('next-hop ')[1].split(' ') if next_hop is defined and\
                                            'prefix-list' not in next_hop else '' }}",
                                        "prefix_lists": "{{ next_hop.split('next-hop prefix-list ')[1].split(' ') if next_hop is defined and\
                                             'prefix-list' in next_hop and next_hop.split('next-hop prefix-list ')[1] is not none else '' }}",
                                    },
                                    "redistribution_source": {
                                        "set": "{{ True if redistribution_source is defined and redistribution_source.split(' ')|length == 1 }}",
                                        "acls": "{{ redistribution_source.split('redistribution-source ')[1].split(' ')|d()\
                                            if redistribution_source is defined and 'prefix-list' not in redistribution_source else '' }}",
                                        "prefix_lists": "{{ redistribution_source.split('redistribution-source prefix-list ')[1].split(' ')|d()\
                                            if redistribution_source is defined and 'prefix-list' in redistribution_source else '' }}",
                                    },
                                    "route_source": {
                                        "set": "{{ True if route_source is defined and route_source.split(' ')|length == 1 }}",
                                        "redistribution_source": "{{ True if route_source is defined and 'redistribution-source' in route_source }}",
                                        "acls": "{{ route_source.split('route-source ')[1].split(' ') if route_source is defined and\
                                                'prefix-list' not in route_source else '' }}",
                                        "prefix_lists": "{{ route_source.split('route-source prefix-list ')[1].split(' ') if route_source is defined and\
                                                'prefix-list' in route_source else '' }}",
                                    },
                                }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "match.ipv6",
            "getval": re.compile(
                r"""
                \s+match*
                \s*(?P<ipv6>ipv6)*
                \s*(?P<address>address\sprefix-list\s\S.*|address\s\S.*)*
                \s*(?P<flowspec>flowspec\sdest-pfx\s(prefix-list\s\S.*|\S.*)|flowspec\ssrc-pfx\s(prefix-list\s\S.*|\S.*))*
                \s*(?P<next_hop>next-hop\sprefix-list\s\S.*|next-hop\s\S.*)*
                \s*(?P<route_source>route-source\sprefix-list\s\S.*|route-source\s\S.*)*
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_route_map_match_ipv6,
            "compval": "match",
            "result": {
                "{{ route_map }}": {
                    "{{ action|d() + '_' + sequence|d() }}": {
                        "entries": {
                            "match": {
                                "ipv6": {
                                    "address": {
                                        "acl": "{{ address.split('address ')[1] if address is defined and 'prefix-list' not in address }}",
                                        "prefix_list": "{{ address.split('address prefix-list ')[1] if address is defined and 'prefix-list' in address }}",
                                    },
                                    "flowspec": {
                                        "dest_pfx": "{{ True if flowspec is defined and 'dest-pfx' in flowspec }}",
                                        "src_pfx": "{{ True if flowspec is defined and 'src-pfx' in flowspec }}",
                                        "acl": "{{ flowspec.split('flowspec ')[1] if flowspec is defined and 'prefix-list' not in flowspec }}",
                                        "prefix_list": "{{ flowspec.split('flowspec prefix-list ')[1] if flowspec is defined and 'prefix-list' in flowspec }}",
                                    },
                                    "next_hop": {
                                        "acl": "{{ next_hop.split('next-hop ')[1] if next_hop is defined and 'prefix-list' not in next_hop }}",
                                        "prefix_list": "{{ next_hop.split('next-hop prefix-list ')[1] if next_hop is defined and 'prefix-list' in next_hop }}",
                                    },
                                    "route_source": {
                                        "acl": "{{ route_source.split('route-source ')[1] if route_source is defined and 'prefix-list' not in route_source }}",
                                        "prefix_list": "{{ route_source.split('route-source prefix-list ')[1] if route_source is defined and\
                                                'prefix-list' in route_source }}",
                                    },
                                }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "set",
            "getval": re.compile(
                r"""
                \s+set*
                \s*(?P<aigp_metric>aigp-metric\sigp-metric|aigp-metric\s\d+)*
                \s*(?P<as_path>as-path\s(prepend\s(last-as\s\d+|\S+)|tag))*
                \s*(?P<automatic_tag>automatic-tag)*
                \s*(?P<clns>clns\snext-hop\s\S.*)*
                \s*(?P<comm_list>comm-list\s\S+\sdelete)*
                \s*(?P<community>community\s\S.*)*
                \s*(?P<dampening>dampening\s\d+\s\d+\s\d+\s\d+)*
                \s*(?P<default>default\sinterface\s\S.*)*
                \s*(?P<extcomm_list>extcomm-list\s\S+\sdelete)*
                \s*(?P<extcommunity>extcommunity\s\S.*)*
                \s*(?P<global>global)*
                \s*(?P<interfaces>interface\s\S.*)*
                \s*(?P<level>level\s(level-1-2|level-1|level-2|nssa-only))*
                \s*(?P<lisp>lisp\slocator-set\s\S+)*
                \s*(?P<local_preference>local-preference\s\d+)*
                \s*(?P<metric>metric\s\S.*)*
                \s*(?P<metric_type>metric-type\s(external|internal|type-1|type-2))*
                \s*(?P<mpls_label>mpls-label)*
                \s*(?P<origin>origin\s(igp|incomplete))*
                \s*(?P<tag>tag\s(([0-9]{1,3}\.?){4}|\d+))*
                \s*(?P<traffic_index>traffic-index\s\d+)*
                \s*(?P<vrf>vrf\s\S+)*
                \s*(?P<weight>weight\s\d+)*
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_route_map_set,
            "result": {
                "{{ route_map }}": {
                    "{{ action|d() + '_' + sequence|d() }}": {
                        "entries": {
                            "set": {
                                "aigp_metric": {
                                    "value": "{{ aigp_metric.split('aigp-metric ')[1] if aigp_metric is defined and\
                                            'igp-metric' not in aigp_metric.split(' ') }}",
                                    "igp_metric": "{{ True if aigp_metric is defined and 'igp-metric' in aigp_metric.split(' ') }}",
                                },
                                "as_path": {
                                    "prepend": {
                                        "as_number": "{{ as_path.split('as-path prepend ')[1].split(' ')\
                                            if as_path is defined and 'prepend' in as_path and 'last-as' not in as_path }}",
                                        "last_as": "{{ as_path.split('as-path prepend last-as ')[1] if as_path is defined and 'prepend' in as_path and\
                                                'last-as' in as_path }}",
                                    },
                                    "tag": "{{ True if as_path is defined and 'tag' in as_path }}",
                                },
                                "automatic_tag": "{{ True if automatic_tag is defined }}",
                                "clns": "{{ clns.split('clns next-hop ')[1] if clns is defined }}",
                                "comm_list": "{{ comm_list.split(' ')[1] if comm_list is defined }}",
                                "community": {
                                    "number": "{{ community.split(' ')[1] if community is defined and 'additive' not in community.split(' ')\
                                                 and 'gshut' not in community.split(' ') and 'internet' not in community.split(' ')\
                                                     and 'internet' not in community.split(' ') and 'local_as' not in community.split(' ')\
                                                         and 'no_advertise' not in community.split(' ') and 'no_export' not in community.split(' ') }}",
                                    "additive": "{{ True if community is defined and 'additive' in community }}",
                                    "gshut": "{{ True if community is defined and 'gshut' in community }}",
                                    "internet": "{{ True if community is defined and 'internet' in community }}",
                                    "local_as": "{{ True if community is defined and 'local_as' in community }}",
                                    "no_advertise": "{{ True if community is defined and 'no_advertise' in community }}",
                                    "no_export": "{{ True if community is defined and 'no_export' in community }}",
                                    "none": "{{ True if community is defined and 'none' in community }}",
                                },
                                "dampening": {
                                    "penalty_half_time": "{{ dampening.split(' ')[1] if dampening is defined }}",
                                    "reuse_route_val": "{{ dampening.split(' ')[2] if dampening is defined }}",
                                    "suppress_route_val": "{{ dampening.split(' ')[3] if dampening is defined }}",
                                    "max_suppress": "{{ dampening.split(' ')[4] if dampening is defined }}",
                                },
                                "default": "{{ default.split('default interface ')[1] if default is defined }}",
                                "extcomm_list": "{{ extcomm_list.split(' ')[1] if extcomm_list is defined }}",
                                "extcommunity": {
                                    "cost": {
                                        "id": "{%- if extcommunity is defined and 'cost' in extcommunity and\
                                            'igp' not in extcommunity and 'pre-bestpath' not in extcommunity -%} {{ extcommunity.split(' ')[2] }}\
                                                {%- elif extcommunity is defined and 'cost' in extcommunity and ('igp' in extcommunity or\
                                                    'pre-bestpath' in extcommunity) -%} {{ extcommunity.split(' ')[3] }} {%- endif -%}",
                                        "cost_value": "{% if extcommunity is defined and 'cost' in extcommunity and 'igp' not in extcommunity and\
                                            'pre-bestpath' not in extcommunity %} {{ extcommunity.split(' ')[3] }}\
                                                {% elif extcommunity is defined and 'cost' in extcommunity and ('igp' in extcommunity or\
                                                    'pre-bestpath' in extcommunity) %} {{ extcommunity.split(' ')[4] }} {% endif %}",
                                        "igp": "{{ True if extcommunity is defined and 'cost' in extcommunity and 'igp' in extcommunity }}",
                                        "pre_bestpath": "{{ True if extcommunity is defined and 'cost' in extcommunity and 'pre-bestpath' in extcommunity }}",
                                    },
                                    "rt": {
                                        "address": "{{ extcommunity.split(' ')[2] if extcommunity is defined and 'rt' in extcommunity and\
                                                'range' not in extcommunity }}",
                                        "range": {
                                            "lower_limit": "{{ extcommunity.split('range ')[1].split(' ')[0] if extcommunity is defined and\
                                                    'rt' in extcommunity and 'range' in extcommunity }}",
                                            "upper_limit": "{{ extcommunity.split('range ')[1].split(' ')[1] if extcommunity is defined and\
                                                    'rt' in extcommunity and 'range' in extcommunity }}",
                                        },
                                        "additive": "{{ True if extcommunity is defined and 'rt' in extcommunity and 'additive' in extcommunity  }}",
                                    },
                                    "soo": "{{ extcommunity.split(' ')[2] if extcommunity is defined and 'soo' in extcommunity }}",
                                    "vpn_distinguisher": {
                                        "address": "{{ extcommunity.split(' ')[2] if extcommunity is defined and\
                                                'vpn-distinguisher' in extcommunity and 'range' not in extcommunity }}",
                                        "range": {
                                            "lower_limit": "{{ extcommunity.split('range ')[1].split(' ')[0] if extcommunity is defined and\
                                                    'vpn-distinguisher' in extcommunity and 'range' in extcommunity }}",
                                            "upper_limit": "{{ extcommunity.split('range ')[1].split(' ')[1] if extcommunity is defined and\
                                                    'vpn-distinguisher' in extcommunity and 'range' in extcommunity }}",
                                        },
                                        "additive": "{{ True if extcommunity is defined and 'vpn-distinguisher' in extcommunity and\
                                                 'additive' in extcommunity }}",
                                    },
                                },
                                "global_route": "{{ True if global is defined }}",
                                "interfaces": "{{ interfaces.split('interface ')[1].split(' ') if interfaces is defined }}",
                                "level": {
                                    "level_1": "{{ True if level is defined and 'level-1' in level and 'level-1-2' not in level }}",
                                    "level_1_2": "{{ True if level is defined and 'level-1-2' in level }}",
                                    "level_2": "{{ True if level is defined and 'level-2' in level }}",
                                    "nssa_only": "{{ True if level is defined and 'nssa-only' in level }}",
                                },
                                "lisp": "{{ lisp.split('lisp locator-set ')[1] if lisp is defined }}",
                                "local_preference": "{{ local_preference.split('local-preference ')[1] if local_preference is defined }}",
                                "metric": {
                                    "deviation": "{%- if metric is defined and '+' in metric -%}{{ 'plus' }}\
                                                {%- elif metric is defined and '-' in metric -%}{{ 'minus' }}{%- endif -%}",
                                    "metric_value": "{{ metric.split(' ')[1] if metric is defined and\
                                             (metric.split(' ')[1] != '+' or metric.split(' ')[1] != '-') }}",
                                    "eigrp_delay": "{% if metric is defined and metric.split(' ')|length > 2 and '+' in metric %}\
                                            {{ metric.split('+')[1].split(' ')[0] }}\
                                                {% elif metric is defined and metric.split(' ')|length > 2 and '+' in metric %}\
                                                    {{ metric.split('-')[1].split(' ')[0] }}\
                                                    {% endif %}",
                                    "metric_reliability": "{% if metric is defined and metric.split(' ')|length > 2 and '+' in metric %}\
                                            {{ metric.split('+')[1].split(' ')[1] }}\
                                                {% elif metric is defined and metric.split(' ')|length > 2 and '+' in metric %}\
                                                    {{ metric.split('-')[1].split(' ')[1] }}\
                                                    {% endif %}",
                                    "metric_bandwidth": "{% if metric is defined and metric.split(' ')|length > 2 and '+' in metric %}\
                                            {{ metric.split('+')[1].split(' ')[2] }}\
                                                {% elif metric is defined and metric.split(' ')|length > 2 and '+' in metric %}\
                                                    {{ metric.split('-')[1].split(' ')[2] }}\
                                                    {% endif %}",
                                    "mtu": "{% if metric is defined and metric.split(' ')|length > 2 and '+' in metric %}\
                                            {{ metric.split('+')[1].split(' ')[3] }}\
                                                {% elif metric is defined and metric.split(' ')|length > 2 and '+' in metric %}\
                                                    {{ metric.split('-')[1].split(' ')[3] }}\
                                                    {% endif %}",
                                },
                                "metric_type": {
                                    "external": "{{ True if metric_type is defined and 'external' in metric_type }}",
                                    "internal": "{{ True if metric_type is defined and 'internal' in metric_type }}",
                                    "type_1": "{{ True if metric_type is defined and 'type-1' in metric_type }}",
                                    "type_2": "{{ True if metric_type is defined and 'type-2' in metric_type }}",
                                },
                                "mpls_label": "{{ True if mpls_label is defined }}",
                                "origin": {
                                    "igp": "{{ True if origin is defined and 'igp' in origin }}",
                                    "incomplete": "{{ True if origin is defined and 'incomplete' in origin }}",
                                },
                                "tag": "{{ tag.split('tag ')[1] if tag is defined }}",
                                "traffic_index": "{{ traffic_index.split('traffic-index ')[1] if traffic_index is defined }}",
                                "vrf": "{{ vrf.split('vrf ')[1] if vrf is defined }}",
                                "weight": "{{ weight.split('weight ')[1] if weight is defined }}",
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "set.ip",
            "getval": re.compile(
                r"""
                \s+set*
                \s*(?P<ip>ip)*
                \s*(?P<address>address\sprefix-list\s\S+)*
                \s*(?P<default>default)*
                \s*(?P<df>df\s\d)*
                \s*(?P<global>global\snext-hop\s(verify-availability\s([0-9]{1,3}\.?){4}\s\d+\strack\s\d+|(([0-9]{1,3}\.?){4}).*))*
                \s*(?P<precedence>precedence\s(critical|flash|flash-override|immediate|internet|network|priority|routine)|precedence)*
                \s*(?P<qos_group>qos_group\s\d+)*
                \s*(?P<tos>tos\s(max-reliability|max-throughput|min-delay|min-monetary-cost|normal)|tos)*
                \s*(?P<vrf>vrf\s\S+\snext-hop\s\S.*)*
                \s*(?P<next_hop>next-hop\s\S.*)*
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_route_map_set_ip,
            "compval": "set",
            "result": {
                "{{ route_map }}": {
                    "{{ action|d() + '_' + sequence|d() }}": {
                        "entries": {
                            "set": {
                                "ip": {
                                    "address": "{{ address.split('address prefix-list ')[1] if address is defined }}",
                                    "default": "{{ True if default is defined }}",
                                    "df": "{{ df.split('df ')[1] if df is defined }}",
                                    "global_route": {
                                        "address": "{% if global is defined and 'verify-availability' not in global %}{{ global.split('global next-hop ')[1] }}\
                                                        {% elif global is defined and 'verify-availability' in global %}{{ global.split(' ')[3] }}{% endif %}",
                                        "verify_availability": {
                                            "address": "{{ global.split(' ')[3] if global is defined and 'verify-availability' in global }}",
                                            "sequence": "{{ global.split(' ')[4] if global is defined and 'verify-availability' in global }}",
                                            "track": "{{ global.split('track ')[1] if global is defined and 'verify-availability' in global }}",
                                        },
                                    },
                                    "next_hop": {
                                        "address": "{{ next_hop.split('next-hop ')[1] if next_hop is defined and 'peer-address' not in next_hop and\
                                                 'self' not in next_hop and next_hop.split(' ')|length == 2 }}",
                                        "dynamic": "{{ True if next_hop is defined and 'dynamic dhcp' in next_hop }}",
                                        "encapsulate": "{{ next_hop.split('next-hop encapsulate l3vpn ')[1] if next_hop is defined and\
                                                'encapsulate' in next_hop }}",
                                        "peer_address": "{{ True if next_hop is defined and 'peer-address' in next_hop }}",
                                        "recursive": {
                                            "global_route": "{{ True if next_hop is defined and 'global' in next_hop.split(' ') }}",
                                            "vrf": "{{ next_hop.split(' ')[3] if next_hop is defined and 'vrf' in next_hop }}",
                                            "address": "{%- if next_hop is defined and 'global' in next_hop.split(' ') -%}\
                                                {{  next_hop.split('next-hop recursive global ')[1] }}\
                                                {%- elif next_hop is defined and 'vrf' in next_hop.split(' ') -%}{{  next_hop.split(' ')[4] }}\
                                                {%- elif next_hop is defined and 'vrf' not in next_hop.split(' ') and 'global' not in next_hop.split(' ') -%}\
                                                    {{ next_hop.split(' ')[2] }} {%- endif -%}",
                                        },
                                        "self": "{{ True if next_hop is defined and 'self' in next_hop }}",
                                        "verify_availability": {
                                            "set": "{{ True if next_hop is defined and 'verify-availability' in next_hop and 'track' not in next_hop }}",
                                            "address": "{{ next_hop.split(' ')[2] if next_hop is defined and 'verify-availability' in next_hop and\
                                                     'track' in next_hop }}",
                                            "sequence": "{{ next_hop.split(' ')[3] if next_hop is defined and 'verify-availability' in next_hop and\
                                                     'track' in next_hop }}",
                                            "track": "{{ next_hop.split('track ')[1] if next_hop is defined and 'verify-availability' in next_hop and\
                                                     'track' in next_hop }}",
                                        },
                                    },
                                    "precedence": {
                                        "set": "{{ True if precedence is defined and precedence.split(' ')|length == 1 }}",
                                        "critical": "{{ True if precedence is defined and 'critical' in precedence }}",
                                        "flash": "{{ True if precedence is defined and 'flash' in precedence }}",
                                        "flash_override": "{{ True if precedence is defined and 'flash-override' in precedence }}",
                                        "immediate": "{{ True if precedence is defined and 'immediate' in precedence }}",
                                        "internet": "{{ True if precedence is defined and 'internet' in precedence }}",
                                        "network": "{{ True if precedence is defined and 'network' in precedence }}",
                                        "priority": "{{ True if precedence is defined and 'priority' in precedence }}",
                                        "routine": "{{ True if precedence is defined and 'routine' in precedence }}",
                                    },
                                    "qos_group": "{{ qos_group.split('qos-group ')[1] if qos_group is defined }}",
                                    "tos": {
                                        "set": "{{ True if tos is defined and tos.split(' ')|length == 1 }}",
                                        "max_reliability": "{{ True if tos is defined and 'max-reliability' in tos }}",
                                        "max_throughput": "{{ True if tos is defined and 'max-throughput' in tos }}",
                                        "min_delay": "{{ True if tos is defined and 'min-delay' in tos }}",
                                        "min_monetary_cost": "{{ True if tos is defined and 'min-monetary-cost' in tos }}",
                                        "normal": "{{ True if tos is defined and 'normal' in tos }}",
                                    },
                                    "vrf": {
                                        "name": "{{ vrf.split(' ')[1] if vrf is defined }}",
                                        "address": "{{ vrf.split('next-hop ')[1] if vrf is defined and 'verify-availability' not in vrf }}",
                                        "verify_availability": {
                                            "set": "{{ True if vrf is defined and 'track' not in vrf }}",
                                            "address": "{{ vrf.split(' ')[4] if vrf is defined and 'track' in vrf }}",
                                            "sequence": "{{ vrf.split(' ')[5] if vrf is defined and 'track' in vrf }}",
                                            "track": "{{ vrf.split('track ')[1] if vrf is defined and 'track' in vrf }}",
                                        },
                                    },
                                }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "set.ipv6",
            "getval": re.compile(
                r"""
                \s+set*
                \s*(?P<ipv6>ipv6)*
                \s*(?P<address>address\sprefix-list\s\S+)*
                \s*(?P<default>default\snext-hop\s(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))\S+)*
                \s*(?P<global>global\snext-hop\sverify-availability\s(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))\S+\s\d+\strack\s\d+)*
                \s*(?P<precedence>precedence\s\d+)*
                \s*(?P<vrf>vrf\s\S+\snext-hop\sverify-availability\s(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))\S+\s\d+\strack\s\d+)*
                \s*(?P<next_hop>next-hop\s\S.*)*
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_route_map_set_ipv6,
            "compval": "set",
            "result": {
                "{{ route_map }}": {
                    "{{ action|d() + '_' + sequence|d() }}": {
                        "entries": {
                            "set": {
                                "ipv6": {
                                    "address": "{{ address.split('address prefix-list ')[1] if address is defined }}",
                                    "default": "{{ default.split('default next-hop ')[1] if default is defined }}",
                                    "global_route": {
                                        "verify_availability": {
                                            "address": "{{ global.split(' ')[3] if global is defined and 'verify-availability' in global }}",
                                            "sequence": "{{ global.split(' ')[4] if global is defined and 'verify-availability' in global }}",
                                            "track": "{{ global.split('track ')[1] if global is defined and 'verify-availability' in global }}",
                                        },
                                        "address": "{{ global.split(' ')[2] if global is defined and 'verify-availability' not in global }}",
                                    },
                                    "next_hop": {
                                        "address": "{{ next_hop.split('next-hop ')[1] if next_hop is defined and\
                                                 next_hop.split(' ')|length == 2 and 'peer-address' not in next_hop }}",
                                        "encapsulate": "{{ next_hop.split('next-hop encapsulate l3vpn ')[1] if next_hop is defined and\
                                                 'encapsulate' in next_hop}}",
                                        "peer_address": "{{ True if next_hop is defined and next_hop.split(' ')|length == 2 and 'peer-address' in next_hop }}",
                                        "recursive": "{{ next_hop.split('next-hop recursive ')[1] if next_hop is defined }}",
                                    },
                                    "precedence": "{{ precedence.split(' ')[1] if precedence is defined }}",
                                    "vrf": {
                                        "name": "{{ vrf.split(' ')[1] if vrf is defined }}",
                                        "verify_availability": {
                                            "address": "{{ vrf.split(' ')[4] if vrf is defined and 'verify-availability' in vrf }}",
                                            "sequence": "{{ vrf.split(' ')[5] if vrf is defined and 'verify-availability' in vrf }}",
                                            "track": "{{ vrf.split('track ')[1] if vrf is defined and 'verify-availability' in vrf }}",
                                        },
                                    },
                                }
                            }
                        }
                    }
                }
            },
        },
    ]
