#!/usr/bin/env bash
SHELL_FOLDER=$(
  cd "$(dirname "$0")" || exit
  pwd
)
cd "${SHELL_FOLDER}" || exit
./private/proxy.sh
./rules.sh
./main.sh
./private/rsync.sh
