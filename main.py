import requests
import os
import telegram
import logging
from dotenv import load_dotenv
from time import time


def long_polling(url, token):
    bot = telegram.Bot(token=os.getenv('TG_TOKEN'))
    headers = {'Authorization': token}
    params = {'timestamp': time()}
    while True:
        try:
            response = requests.get(url, headers=headers, params=params, timeout=150)
            response.raise_for_status()
            decoded_response = response.json()
            if decoded_response['status'] == 'timeout':
                bot.send_message(chat_id=os.getenv('CHAT_ID'), text=f'Timeout')
                params = {'timestamp': decoded_response['timestamp_to_request']}
                continue
            elif decoded_response['status'] == 'found':
                bot.send_message(chat_id=os.getenv('CHAT_ID'),
                                 text=f'{decoded_response["new_attempts"][0]["is_negative"]} '
                                      f'{decoded_response["new_attempts"][0]["lesson_title"]}')
                params = {'timestamp': time()}
                continue
        except (requests.exceptions.Timeout,
                requests.exceptions.HTTPError,
                requests.RequestException):
            continue


def main():
    load_dotenv()
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    authorization = os.getenv('AUTHORIZATION')
    url_long_polling = os.getenv('URL_LONG_POLLING')
    print(long_polling(url_long_polling, authorization))


if __name__ == '__main__':
    main()
