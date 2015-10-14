#!/bin/bash

SSH_KEY=$1
USERNAME=$2
REMOTE_HOST=$3
REMOTE_SCRIPT=$4
STDOUT_FILE=$5
STDERR_FILE=$6
PID_FILE=$7
ARGS=${@:8}

REMOTE_ACTION='$(bash -x '${REMOTE_SCRIPT}' '${ARGS}' > '${STDOUT_FILE}' 2> '${STDERR_FILE}' && rm -f '${PID_FILE}') & echo $! > '${PID_FILE}''

ssh -n -f -i ${SSH_KEY} -o ConnectTimeout=5 ${USERNAME}@${REMOTE_HOST} "${REMOTE_ACTION}"
