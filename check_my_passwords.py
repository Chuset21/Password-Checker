import requests
import hashlib
import sys


def request_api_data(query_chars: str) -> requests.Response:
    response = requests.get(f'https://api.pwnedpasswords.com/range/{query_chars}')
    if response.status_code != 200:
        raise RuntimeError(f'Error fetching: {response.status_code}, check the API and try again')
    return response


def hash_password(password: str) -> str:
    return hashlib.sha1(password.encode('utf-8')).hexdigest().upper()


def get_password_leaks_count(response: requests.Response, hash_to_check: str) -> int:
    hashes = map(lambda line: line.split(':'), response.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return int(count)
    return 0


def pwned_api_check(password: str) -> int:
    sha1_password = hash_password(password)
    first5_char, tail = sha1_password[:5], sha1_password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)


def check_passwords(passwords: list[str]) -> None:
    for password in passwords:
        count = pwned_api_check(password)
        if count:
            print(f'{password} was found {count} time{"s" if count > 1 else ""}'
                  f'... you should probably change your password.')
        else:
            print(f'{password} was NOT found. Carry on!')


if __name__ == '__main__':
    sys.exit(check_passwords(sys.argv[1:]))
