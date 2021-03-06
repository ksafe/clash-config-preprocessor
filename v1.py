import re
import requests
import yaml
from collections import OrderedDict

import utils


def get_proxies_regex(item, param):
    if "proxies-filters" in item and param in item["proxies-filters"] is not None:
        return re.compile(item["proxies-filters"][param])
    return re.compile("")


def handle_v1(data: OrderedDict) -> OrderedDict:
    preprocessor: OrderedDict = data["preprocessor"]

    if preprocessor is None or preprocessor["version"] != 1:
        raise utils.ParseException("Version != 1")

    result: OrderedDict = OrderedDict()

    general_block: OrderedDict = data["clash-general"]
    result.update(general_block)

    proxy_sources_dicts: list = data["proxy-sources"]
    proxies: list = []

    for item in proxy_sources_dicts:
        proxies2: list = []
        if item["type"] == "url":
            proxies2 += load_url_proxies(item["url"])
        elif item["type"] == "file":
            proxies2 += load_file_proxies(item["path"])
        elif item["type"] == "plain":
            proxies2.append(load_plain_proxies(item))

        if "name-prefix" in item:
            name_prefix = item["name-prefix"]
            for p in proxies2:
                p["name"] = name_prefix + " - " + p["name"]

        if "proxies-filters" in item:
            black_regex = get_proxies_regex(item, "black-regex")
            white_regex = get_proxies_regex(item, "white-regex")

            for p in proxies2:
                p_name: str = p["name"]
                if white_regex.fullmatch(p_name) and not black_regex.fullmatch(p_name):
                    proxies.append(p)
        else:
            proxies += proxies2

    proxy_group_dispatch_dicts: list = data["proxy-group-dispatch"]
    proxy_groups: list = []
    removed_proxy: list = []
    for item in proxy_group_dispatch_dicts:
        group_data: OrderedDict = item.copy()
        ps: list = []
        black_regex = get_proxies_regex(item, "black-regex")
        white_regex = get_proxies_regex(item, "white-regex")

        if "flat-proxies" in item and item["flat-proxies"] is not None:
            ps.extend(item["flat-proxies"])

        for p in proxies:
            p_name: str = p["name"]
            if white_regex.fullmatch(p_name) and not black_regex.fullmatch(p_name):
                ps.append(p_name)

        if "back-flat-proxies" in item and item["back-flat-proxies"] is not None:
            ps.extend(item["back-flat-proxies"])

        group_data.pop("proxies-filters", None)
        group_data.pop("flat-proxies", None)
        group_data.pop("back-flat-proxies", None)

        if len(ps) < 1:
            removed_proxy.append(group_data["name"])
            continue

        group_data["proxies"] = ps

        proxy_groups.append(group_data)

    for proxy_group in proxy_groups:
        proxy_group_proxies: list = []
        for p in proxy_group["proxies"]:
            if p in removed_proxy:
                continue
            proxy_group_proxies.append(p)
        proxy_group["proxies"] = proxy_group_proxies

    rule_sets_dicts: list = data["rule-sets"]
    rule_sets: dict = {}

    if rule_sets_dicts is not None:
        for item in rule_sets_dicts:
            item_name: str = item["name"]
            item_type: str = item["type"]
            item_behavior: str = item.get("behavior", "classical")
            item_map: dict = {}
            item_rule_skip = item.get("rule-skip", {})
            item_target_skip = item.get("target-skip", {})
            for target_map_element in item.get("target-map", {}):
                kv: list = target_map_element.split(",")
                item_map[kv[0]] = kv[1]

            if item_type == "url":
                rule_sets[item_name] = load_url_rule_set(item["url"], item_behavior, item_map, item_rule_skip, item_target_skip)
            elif item_type == "file":
                rule_sets[item_name] = load_file_rule_set(item["path"], item_behavior, item_map, item_rule_skip, item_target_skip)

    rules: list = []

    for rule in data["rule"]:
        if str(rule).startswith("RULE-SET"):
            rule_set = str(rule).split(",")
            if len(rule_set) < 3:
                rules.extend(rule_sets[rule_set[1]])
            else:
                for item in rule_sets[rule_set[1]]:
                    if str(item).endswith("no-resolve"):
                        rules.append(str(item).replace(",no-resolve", "," + rule_set[2] + ",no-resolve"))
                    else:
                        rules.append(item + "," + rule_set[2])
        else:
            rules.append(rule)

    result["proxies"] = proxies
    result["proxy-groups"] = proxy_groups
    result["rules"] = rules

    return result


def get_clash_item(ordered_dict: OrderedDict, *nodes: str):
    for node in nodes:
        if node in ordered_dict:
            return ordered_dict[node]
    return ordered_dict


def load_url_proxies(url: str) -> OrderedDict:
    print("Load Url: ", url)
    data = requests.get(url)
    data_yaml: OrderedDict = yaml.load(data.content.decode(), Loader=yaml.Loader)

    return get_clash_item(data_yaml, "Proxy", "proxies")


def load_file_proxies(path: str) -> OrderedDict:
    print("Load File: ", path)
    with open(path, "r") as f:
        data_yaml: OrderedDict = yaml.load(f, Loader=yaml.Loader)

    return get_clash_item(data_yaml, "Proxy", "proxies")


def load_plain_proxies(data: OrderedDict) -> OrderedDict:
    print("Load Plain: ", data)
    return data["data"]


def load_url_rule_set(url: str, behavior: str, target_map: dict, skip_rule: set, skip_target: set) -> list:
    print("Load Rule Url: ", url)
    data: OrderedDict = yaml.load(requests.get(url).content, Loader=yaml.Loader)
    result: list = []

    for rule in get_clash_item(data, "Rule", "rules", "payload"):
        if behavior == "ipcidr":
            rule = "IP-CIDR," + rule
        original_target = str(rule).split(",")[-1]
        map_to: str = target_map.get(original_target)
        if str(rule).split(',')[0] not in skip_rule and original_target not in skip_target:
            if map_to is not None:
                result.append(str(rule).replace(original_target, map_to))
            else:
                result.append(str(rule))

    return result


def load_file_rule_set(path: str, behavior: str, target_map: dict, skip_rule: set, skip_target: set) -> list:
    print("Load Rule File: ", path)
    with open(path, "r") as f:
        data: OrderedDict = yaml.load(f, Loader=yaml.Loader)
    result: list = []

    for rule in get_clash_item(data, "Rule", "rules", "payload"):
        if behavior == "ipcidr":
            rule = "IP-CIDR," + rule
        original_target = str(rule).split(",")[-1]
        map_to: str = target_map.get(original_target)
        if str(rule).split(',')[0] not in skip_rule and original_target not in skip_target:
            if map_to is not None:
                result.append(str(rule).replace(original_target, map_to))
            else:
                result.append(rule)

    return result
