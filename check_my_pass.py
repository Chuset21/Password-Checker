import requests
import hashlib


def request_api_data(query_chars: str) -> requests.Response:
    response = requests.get(f'https://api.pwnedpasswords.com/range/{query_chars}')
    if response.status_code != 200:
        raise RuntimeError(f'Error fetching: {response.status_code}, check the API and try again')
    return response


def pwned_api_check(password: str):
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    return sha1_password


def main():
    password = 'password123'
    request_api_data('12345')


if __name__ == '__main__':
    main()
