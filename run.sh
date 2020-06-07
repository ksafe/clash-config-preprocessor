#!/usr/bin/env bash
python main.py preclash/DlerCloud-SS.yaml > config/DlerCloud-SS.yaml
python main.py preclash/DlerCloud-V2Ray.yaml > config/DlerCloud-V2Ray.yaml
python main.py preclash/DlerCloud-Trojan.yaml > config/DlerCloud-Trojan.yaml
python main.py preclash/Renzhe.yaml > config/Renzhe.yaml

./rsync.sh 
