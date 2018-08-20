#!/bin/bash

CLIENT=0

POSITIONAL=()
while [[ $# -gt 0 ]]
do

  key="$1"

  case $key in
    -m|--mode)
      MODE="$2"
      shift
      shift
      ;;
    -f|--frames)
      FRAMES="$2"
      shift
      shift
      ;;
    -i|--increment)
      INCREMENT="$2"
      shift
      shift
      ;;
    -a|--address)
      ADDRESS="$2"
      shift
      shift
      ;;
    -s|--sleep)
      SLEEP="$2"
      shift
      shift
      ;;
    *)
      POSITIONAL+=("$1")
      shift
      ;;
  esac
done

set -- "${POSITIONAL[@]}"

source setup_env.sh

if [[ "${MODE}" = "server" ]]; then
  if [[ ! -d "$EOP_SOCKET_EOP_FOLDER" ]]; then
    echo "No EasyOpenPose installation found."
    echo "Aborting..."
    exit 1
  fi
  if [[ `ls -1 inbox/*.jpg 2>/dev/null | wc -l` -gt 0 ]]; then
    rm inbox/*.jpg
  fi
  python3 main.py
else
  CLIENT=1
fi

if [[ "${CLIENT}" = 1 ]]; then
  CAPTURE_DIR="client/capture/"
  if [[ ! -d "$CAPTURE_DIR" ]]; then
    mkdir "$CAPTURE_DIR"
  fi
  python3 main_client.py -f $FRAMES -i $INCREMENT -a $ADDRESS -s $SLEEP
fi
