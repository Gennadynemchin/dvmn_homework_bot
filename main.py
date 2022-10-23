import requests
import os
import telegram
import logging
from dotenv import load_dotenv
from time import time, sleep

logger = logging.getLogger(__name__)


def long_polling(url, token, chat_id):
    bot = telegram.Bot(token=os.getenv('TG_TOKEN'))
    headers = {'Authorization': token}
    params = {'timestamp': time()}
    timeout = 150
    counter_response_timeout = 0
    while True:
        try:
            response = requests.get(url, headers=headers, params=params, timeout=timeout)
            response.raise_for_status()
            homework_response = response.json()
            if homework_response['status'] == 'timeout':
                params = {'timestamp': homework_response['timestamp_to_request']}
                continue
            elif homework_response['status'] == 'found':
                last_attempt_timestamp = homework_response['last_attempt_timestamp']
                work_title = homework_response["new_attempts"][0]["lesson_title"]
                work_link = homework_response["new_attempts"][0]["lesson_url"]
                work_status = homework_response["new_attempts"][0]["is_negative"]
                if work_status:
                    bot.send_message(chat_id=chat_id,
                                     text=f"Работа '{work_title}' возвращена с проверки. Посмотреть ошибки и исправить"
                                          f" можно по ссылке: {work_link}")
                elif not work_status:
                    bot.send_message(chat_id=chat_id,
                                     text=f"Работа '{work_title}' успешно выполнена. {work_link}")
                params = {'timestamp': last_attempt_timestamp}
                continue
        except (requests.exceptions.HTTPError,
                requests.RequestException):
            counter_response_timeout += 1
            if counter_response_timeout == 5:
                sleep(300)
                counter_response_timeout = 0
            continue


def main():
    load_dotenv()
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    '''
    authorization = os.getenv('DVMN_AUTHORIZATION')
    url_long_polling = os.getenv('DVMN_URL_LONG_POLLING')
    chat_id = os.getenv('TG_CHAT_ID')
    '''
    # env for Heroku
    authorization = os.environ['DVMN_AUTHORIZATION']
    url_long_polling = os.environ['DVMN_URL_LONG_POLLING']
    chat_id = os.environ['TG_CHAT_ID']
    long_polling(url_long_polling, authorization, chat_id)


if __name__ == '__main__':
    main()
