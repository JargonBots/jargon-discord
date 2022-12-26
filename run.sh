#!/bin/bash

poetry --directory /opt/pysetup shell

env_file="/workspace/config/.env"
if [ ! -f "${env_file}" ]; then
    echo ".env file does not exist. Please create and add correct API keys."
    exit 1
fi

source ${env_file}

python -m discord_bot