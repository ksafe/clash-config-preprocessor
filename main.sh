#!/usr/bin/env bash
SHELL_FOLDER=$(
  cd "$(dirname "$0")" || exit
  pwd
)
cd "${SHELL_FOLDER}" || exit
rm -f config/*.yaml
echo "生成Clash配置文件..."
python main.py private/preclash/ksafe.yaml config/ksafe.yaml
python main.py private/preclash/dler-ss.yaml config/dler-ss.yaml
python main.py private/preclash/dler-v2ray.yaml config/dler-v2ray.yaml
python main.py private/preclash/dler-trojan.yaml config/dler-trojan.yaml
#python main.py private/preclash/dler-ss-ad.yaml config/dler-ss-ad.yaml
#python main.py private/preclash/dler-v2ray-ad.yaml config/dler-v2ray-ad.yaml
#python main.py private/preclash/dler-trojan-ad.yaml config/dler-trojan-ad.yaml
python main.py private/preclash/renzhe.yaml config/renzhe.yaml
