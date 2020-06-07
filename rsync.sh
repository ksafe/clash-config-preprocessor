#!/usr/bin/env bash
rsync -avP config/*.yaml root@192.168.88.10:/etc/openclash/config/
rsync -avP config/*.yaml root@192.168.88.11:/etc/openclash/config/
rsync -avP config/*.yaml 192.168.88.3:~/.config/clash/
rsync -avP config/*.yaml ~/Downloads/Config/
