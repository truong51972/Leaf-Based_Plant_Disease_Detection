import requests
import dns.resolver

my_ddns = 'truong51972.ddns.net'
port = 8000

base_url = "http://{}:{}"

def __ddns_to_ip(domain: str) -> str:
    answers = dns.resolver.resolve(domain, 'A')
    return next(iter(answers)).address

def _request(api_name: str, json: dict):
    try:
        ip = __ddns_to_ip(my_ddns)
        url = base_url.format(ip, port) + api_name
        print(f"Sending request to: '{url}'!")
        response = requests.post(url, json= json, timeout=5)
    except:
        class Response:
            def __init__(self) -> None:
                self.response = {
                    'message' : 'Server not Found!',
                    'code': '404'
                }
            def json(self) -> dict[str, str]:
                return self.response
            
        response = Response()
    return response