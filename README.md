# Devman homework check bot

For starting the bot just run main.py on command line. The bot will request to dvmn.org server. The server response appx. every 90 seconds.
If there is checked homework has found - the bot sends message to a user.

You have to add some variables in .env:
```
'TG_TOKEN'='<TOKEN YOU GOT FROM THE @BOTFATHER OF TELEGRAM>'
'DVMN_AUTHORIZATION'='<YOUR DEVMAN API TOKEN>' (see https://dvmn.org/api/docs for information)
'TG_CHAT_ID'='<YOUR TELEGRAM CHAT_ID>'
'DVMN_URL_LONG_POLLING'='<URL THAT USES FOR LONG POLLING REQUESTS>' (see https://dvmn.org/api/docs for information)
```

### How to install
Clone the project:
```
git clone https://github.com/Gennadynemchin/dvmn_homework_bot.git
cd dvmn_homework_bot
```
Create and activate a virtual environment:
```
python3 -m venv env
source env/bin/activate
```
Python3 should be already installed. 
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
