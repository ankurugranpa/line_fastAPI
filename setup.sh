#!/bin/bash

set -e  # エラーが出たらスクリプトを止める

ENV_FILE="line-fastAPI/.env"

echo -e "\e[44m [SETUP] Starting line-fastAPI setup... \e[m"

if [ -f "$ENV_FILE" ]; then
    echo -e "\e[33m [SKIP] $ENV_FILE already exists. Skipping .env creation. \e[m"
else
    echo -e "\e[32m [CREATE] Generating .env file... \e[m"
    cat <<EOF > "$ENV_FILE"
LINE_CHANEL_API_KEY='your_api_key'
LINE_USER_ID='your_user_id'
LINE_CANNEL_SECLET='your_channel_seclet'
OPENAI_API_KEY='your_openai_api_key'
DB_API_URL='data_base_api_url'
EOF
  echo -e "\e[32m [DONE] .env file Created Successfully. \e[m"
fi
