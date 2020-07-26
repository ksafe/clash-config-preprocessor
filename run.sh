#!/usr/bin/env bash
~/Downloads/Config/rsync.sh rules
rm -f config/*.yaml
#python main.py preclash/ksafe.yaml config/ksafe.yaml
#python main.py preclash/dler.yaml config/dler.yaml
python main.py preclash/dler-ss.yaml config/dler-ss.yaml
python main.py preclash/dler-v2ray.yaml config/dler-v2ray.yaml
python main.py preclash/dler-trojan.yaml config/dler-trojan.yaml
python main.py preclash/renzhe.yaml config/renzhe.yaml
./rsync.sh
