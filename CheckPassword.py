import requests
import hashlib
def req_api_data(querry_char):
    url = 'https://api.pwnedpasswords.com/range/'+querry_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the api and try agian')
    return res

def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count    
    return 0
       

def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = req_api_data(first5_char)
    return get_password_leaks_count(response, tail)

def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'{password} was found {count} times, you should porbably change your password.')
        else:
            print(f'{password} not found, you are safe')


with open('password.txt', 'r') as text:
    passwords = [line.rstrip() for line in text]
if __name__ == '__main__' :
    main(passwords)




