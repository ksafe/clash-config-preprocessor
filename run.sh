#!/usr/bin/env bash
rm -f config/*.yaml
#python main.py preclash/DlerCloud-SS.yaml config/DlerCloud-SS.yaml
#python main.py preclash/DlerCloud-V2Ray.yaml config/DlerCloud-V2Ray.yaml
#python main.py preclash/DlerCloud-Trojan.yaml config/DlerCloud-Trojan.yaml
python main.py preclash/ksafe.yaml config/ksafe.yaml
python main.py preclash/DlerCloud.yaml config/Dler.yaml
#python main.py preclash/Renzhe.yaml config/Renzhe.yaml
./rsync.sh
