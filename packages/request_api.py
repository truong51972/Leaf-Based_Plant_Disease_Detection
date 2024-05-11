import requests
from packages import get_ip_from_ddns
from packages.encode_deconde import encrypt_password
    
my_ddns = 'truong51972.ddns.net'
port = 8000

base_url = "http://{}:{}"

def check_login(item: dict):
    ip = get_ip_from_ddns.get(my_ddns)
    url = base_url.format(ip, port) + '/check-login'
    print(url)

    response = requests.post(url, json= item)
    return response

if __name__ == '__main__':
    encrypted_password = encrypt_password('chao em').decode()
    item = {
        'user_name' : 'admin',
        'password': encrypted_password
    }

    response = check_login(item)
    print(response.json())