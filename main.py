import requests
import os
import telegram
import logging
from dotenv import load_dotenv
from time import time, sleep


class TelegramLogsHandler(logging.Handler):
    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.tg_bot = tg_bot
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def long_polling(url, bot, token, chat_id):
    # bot = telegram.Bot(token=os.getenv('TG_TOKEN'))
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
            sleep(5)
            bot.send_message(chat_id=chat_id, text=f'Something wrong with the connection. '
                                                   f'Trying to reconnect {counter_response_timeout}')
            if counter_response_timeout == 5:
                sleep(300)
                counter_response_timeout = 0
            continue


def main():
    load_dotenv()
    authorization = os.environ['DVMN_AUTHORIZATION']
    url_long_polling = os.environ['DVMN_URL_LONG_POLLING']
    chat_id = os.environ['TG_CHAT_ID']
    tg_token = os.environ['TG_TOKEN']

    bot = telegram.Bot(token=tg_token)

    logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    logger = logging.getLogger('MyLogger')
    logger.addHandler(TelegramLogsHandler(tg_bot=bot, chat_id=chat_id))

    try:
        logger.info(msg='The bot has been started')
        long_polling(url_long_polling, bot, authorization, chat_id)
    finally:
        logger.error(msg='Error has occured', exc_info=True)


if __name__ == '__main__':
    main()
