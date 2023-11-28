touch .env
echo "LINE_CHANEL_API_KEY='your_api_key'" >> .env
echo "LINE_USER_ID='your_user_id'" >> .env
echo "LINE_CANNEL_SECLET='your_channel_seclet'" >> .env
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
