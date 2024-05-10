import dns.resolver

# domain = 'truong51972.ddns.net'
"""
    Get ip from ddns
"""
def get(domain: str) -> str:
    answers = dns.resolver.resolve(domain, 'A')
    return next(iter(answers)).address

if __name__ == '__main__':
    domain = 'truong51972.ddns.net'
    print(get(domain))