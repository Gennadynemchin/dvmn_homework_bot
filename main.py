import requests
import os
from dotenv import load_dotenv
import logging
import time


def get_user_reviews(url, token):
    headers = {'Authorization': token}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def long_polling(url, token):
    #params = {'timeout': time.time()}
    headers = {'Authorization': token}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    decoded_response = response.json()
    while decoded_response['status'] == 'timeout':
        params = {'timeout':decoded_response['timestamp_to_request']}
        response.raise_for_status()
        decoded_response = response.json()
        return decoded_response
    return decoded_response

def main():
    load_dotenv()
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    authorization = os.getenv('AUTHORIZATION')
    url_user_reviews = os.getenv('URL_USER_REVIEWS')
    url_long_polling = os.getenv('URL_LONG_POLLING')
    #result = get_user_reviews(url_user_reviews, authorization)
    while True:
        print(long_polling(url_long_polling, authorization), f'LOCAL TIMESTAMP: {time.time()}')


if __name__ == '__main__':
    main()
