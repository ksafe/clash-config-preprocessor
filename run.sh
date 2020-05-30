#!/usr/bin/env bash
python main.py preclash/DlerCloud-SS.yaml > config/DlerCloud-SS.yaml
python main.py preclash/DlerCloud-V2Ray.yaml > config/DlerCloud-V2Ray.yaml
python main.py preclash/DlerCloud-Trojan.yaml > config/DlerCloud-Trojan.yaml
python main.py preclash/Renzhe.yaml > config/Renzhe.yaml

rsync -avP config/*.yaml root@192.168.88.10:/etc/openclash/config/
rsync -avP config/*.yaml root@192.168.88.11:/etc/openclash/config/
rsync -avP config/*.yaml 192.168.88.3:~/.config/clash/
rsync -avP config/*.yaml /home/ksafe/Downloads/Config/