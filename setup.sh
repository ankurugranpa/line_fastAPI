touch .env
echo "LINE_CHANEL_API_KEY='your_api_key'" >> .env
echo "LINE_USER_ID='your_user_id'" >> .env
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
