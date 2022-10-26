# Devman homework check bot

For starting the bot just run main.py on command line. The bot will request to dvmn.org server. The server response appx. every 90 seconds.
If there is checked homework has found - the bot sends message to a user.

You have to add some variables in .env:
```
TG_TOKEN=TOKEN_YOU_GOT_FROM_THE_@BOTFATHER_OF_TELEGRAM
DVMN_AUTHORIZATION=YOUR_DEVMAN_API_TOKEN (see https://dvmn.org/api/docs for information)
TG_CHAT_ID=YOUR_TELEGRAM_CHAT_ID
DVMN_URL_LONG_POLLING=URL_THAT_USES_FOR_LONG_POLLING_REQUESTS (see https://dvmn.org/api/docs for information)
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
Run:
```
python3 main.py
```
### Deploy with Docker

1. Copy this repository to your server:
```
git clone https://github.com/Gennadynemchin/dvmn_homework_bot.git
```
2. `cd dvmn_homework_bot`
3. `nano .env.example`. Then fill all needed variables as shown above.
4. Save `.env.example` as `.env`
5. Build an image:
`docker build -t your-image-name . `
6. Then `docker run -d your-image-name`

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
