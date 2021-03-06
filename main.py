#!/usr/bin/env python3
import re
import sys
import yaml
from collections import OrderedDict

import utils
import v1

_HELP_TEXT = """\
Usage: python main.py <source-path> [save-path]
    <source-path>: path to preprocessor config
    [save-path]: path to clash config

See also:
    https://github.com/Kr328/clash-config-preprocessor
"""


def main():
    utils.setup_order_yaml()

    if len(sys.argv) < 2:
        print("Argument source required")
        print(_HELP_TEXT)
        return

    print("开始执行: " + sys.argv[1] + " ...")
    with open(sys.argv[1], "r") as f:
        data: OrderedDict = yaml.load(f, Loader=yaml.Loader)

    if data["preprocessor"]["version"] == 1:
        result = v1.handle_v1(data)
    else:
        print("Unsupported version")
        return

    result = yaml.dump(result, default_flow_style=False, allow_unicode=True)
    regex = re.compile(r'\b(password:\s*)\b[\"\']?(.*)[\'\"]?\b', re.VERBOSE)
    result = regex.sub(r'\1"\2"', result)
    if len(sys.argv) > 2:
        with open(sys.argv[2], "w") as f:
            f.write(result)
        print("生成Clash配置文件: " + sys.argv[2])
    else:
        print(result)


if __name__ == "__main__":
    main()
