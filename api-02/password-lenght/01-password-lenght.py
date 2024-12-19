import requests
import base64
import logging

url = "http://34.139.11.27:8181/onos/v1/docs/index.html"
username = 'onos'

logging.basicConfig(
    filename="01_password_length_results.log",  # Arquivo onde os logs serão armazenados
    level=logging.DEBUG,                   # Nível de log (INFO para capturar mensagens de sucesso e erro)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Formato do log
)


def encode_credentials(username:str, password: str): 
    credentials = f"{username}:{password}"
    return base64.b64encode(credentials.encode('ISO-8859-1')).decode('ISO-8859-1')

def test_password_length(username: str, password_length: int):
    password = 'A' * password_length

    headers = {
        'Authorization': f'Basic {encode_credentials(username=username, password=password)}',
        'User-Agent': 'Mozilla/5.0'
    }
    
    response = requests.get(url=url, headers=headers)

    return response

def main():
    password_length = 6080


    response = test_password_length(username=username, password_length=password_length)
    print(response.status_code, response.content)

    if(response.status_code == 431):
        logging.debug(f'O tamanho da password com o username {username} é: {password_length}')


if __name__ == '__main__':
    main()