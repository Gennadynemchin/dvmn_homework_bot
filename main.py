import requests
import os
from dotenv import load_dotenv


def get_user_reviews(url, token):
    headers = {'Authorization': token}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def main():
    load_dotenv()
    authorization = os.getenv('AUTHORIZATION')
    url = os.getenv('URL')
    print(get_user_reviews(url, authorization))

if __name__ == '__main__':
    main()
