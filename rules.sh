#!/usr/bin/env bash
SHELL_FOLDER=$(
  cd "$(dirname "$0")" || exit
  pwd
)
cd "${SHELL_FOLDER}" || exit

export ALL_PROXY=socks5://192.168.88.3:7891

rm -f config/rule_provider/*.yaml
echo "下载翻墙策略..."
curl 'https://raw.githubusercontent.com/DivineEngine/Profiles/master/Clash/RuleSet/China.yaml' -o config/rule_provider/China.yaml || exit
curl 'https://raw.githubusercontent.com/DivineEngine/Profiles/master/Clash/RuleSet/Global.yaml' -o config/rule_provider/Global.yaml || exit
curl 'https://raw.githubusercontent.com/DivineEngine/Profiles/master/Clash/RuleSet/Unbreak.yaml' -o config/rule_provider/Unbreak.yaml || exit
curl 'https://raw.githubusercontent.com/DivineEngine/Profiles/master/Clash/RuleSet/Guard/Advertising.yaml' -o config/rule_provider/Advertising.yaml || exit
curl 'https://raw.githubusercontent.com/DivineEngine/Profiles/master/Clash/RuleSet/Guard/Hijacking.yaml' -o config/rule_provider/Hijacking.yaml || exit
curl 'https://raw.githubusercontent.com/DivineEngine/Profiles/master/Clash/RuleSet/StreamingMedia/StreamingCN.yaml' -o config/rule_provider/StreamingCN.yaml || exit
curl 'https://raw.githubusercontent.com/DivineEngine/Profiles/master/Clash/RuleSet/StreamingMedia/StreamingSE.yaml' -o config/rule_provider/StreamingSE.yaml || exit
curl 'https://raw.githubusercontent.com/DivineEngine/Profiles/master/Clash/RuleSet/StreamingMedia/Streaming.yaml' -o config/rule_provider/Streaming.yaml || exit
curl 'https://raw.githubusercontent.com/DivineEngine/Profiles/master/Clash/RuleSet/StreamingMedia/Video/Netflix.yaml' -o config/rule_provider/Netflix.yaml || exit
curl 'https://raw.githubusercontent.com/DivineEngine/Profiles/master/Clash/RuleSet/StreamingMedia/Video/YouTube.yaml' -o config/rule_provider/YouTube.yaml || exit

unset ALL_PROXY
sudo sync