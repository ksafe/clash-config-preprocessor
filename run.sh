#!/usr/bin/env bash
SHELL_FOLDER=$(
  cd "$(dirname "$0")" || exit
  pwd
)
cd "${SHELL_FOLDER}" || exit
./private/proxy.sh || exit
./rules.sh || exit
./main.sh || exit
./private/rsync.sh || exit
