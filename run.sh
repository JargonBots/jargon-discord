#!/bin/bash

#poetry --directory /opt/pysetup shell

env_file="/workspace/config/.env"
jargonai_env="/jargonai/config/.env"

if [ ! -f "${env_file}" ]; then
    echo ".env file does not exist. Please create and add correct API keys."
    exit 1
fi

source ${env_file}
source ${jargonai_env}

#pushd /jargonai && poetry --directory /opt/pysetup install && popd

python -m discord_bot