import socket
import requests
import os
import telegram
import logging
from dotenv import load_dotenv
from time import time, sleep
from urllib3.exceptions import NewConnectionError
from requests.adapters import HTTPAdapter, Retry

logger = logging.getLogger('MyLogger')


class TelegramLogsHandler(logging.Handler):
    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.tg_bot = tg_bot
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def long_polling(url, bot, token, chat_id):
    headers = {'Authorization': token}
    params = {'timestamp': time()}
    session = requests.Session()
    while True:
        try:
            total_retries = 5
            backoff_factor = 150
            retries = Retry(total=total_retries, backoff_factor=backoff_factor)
            session.mount(url, HTTPAdapter(max_retries=retries))
            response = session.get(url, headers=headers, params=params)
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
        except requests.exceptions.Timeout:
            continue
        except (requests.exceptions.HTTPError,
                requests.RequestException, NewConnectionError):
            logger.error('Get some sleep. Then try to reconnect')
            sleep(300)
        except socket.timeout:
            logger.error('Everything has gone down the cunt')


def main():
    load_dotenv()
    authorization = os.environ['DVMN_AUTHORIZATION']
    url_long_polling = os.environ['DVMN_URL_LONG_POLLING']
    chat_id = os.environ['TG_CHAT_ID']
    tg_token = os.environ['TG_TOKEN']

    bot = telegram.Bot(token=tg_token)
    logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    logger.addHandler(TelegramLogsHandler(tg_bot=bot, chat_id=chat_id))
    logger.info(msg='The bot has been started')
    long_polling(url_long_polling, bot, authorization, chat_id)


if __name__ == '__main__':
    main()
