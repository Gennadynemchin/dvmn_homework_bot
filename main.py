import requests
import os
import telegram
import logging
from dotenv import load_dotenv
from time import time


def long_polling(url, token, chat_id):
    bot = telegram.Bot(token=os.getenv('TG_TOKEN'))
    headers = {'Authorization': token}
    params = {'timestamp': time()}
    timeout = 150
    while True:
        try:
            response = requests.get(url, headers=headers, params=params, timeout=timeout)
            response.raise_for_status()
            decoded_response = response.json()
            if decoded_response['status'] == 'timeout':
                params = {'timestamp': decoded_response['timestamp_to_request']}
                continue
            elif decoded_response['status'] == 'found':
                work_title = decoded_response["new_attempts"][0]["lesson_title"]
                work_link = decoded_response["new_attempts"][0]["lesson_url"]
                work_status = decoded_response["new_attempts"][0]["is_negative"]
                if work_status:
                    bot.send_message(chat_id=chat_id,
                                     text=f"Работа '{work_title}' возвращена с проверки. Посмотреть ошибки и исправить"
                                          f" можно по ссылке: {work_link}")
                elif not work_status:
                    bot.send_message(chat_id=chat_id,
                                     text=f"Работа '{work_title}' успешно выполнена. {work_link}")
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
    chat_id = os.getenv('CHAT_ID')
    print(long_polling(url_long_polling, authorization, chat_id))


if __name__ == '__main__':
    main()
