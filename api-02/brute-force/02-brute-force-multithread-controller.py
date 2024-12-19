import subprocess
from concurrent.futures import ThreadPoolExecutor

# Configuração do script e número de threads
script_to_run = "02-brute-force-multithread.py"  # Nome do script que será executado em múltiplas threads.
num_threads = 100  # Quantidade de threads a serem usadas para execução simultânea.

# Função para executar o script em uma instância específica.
def run_script(instance_id):
    # Exibe uma mensagem indicando o início da execução para a instância específica.
    print(f"[INFO] Iniciando instância {instance_id}")

    try:
        # Executa o script fornecido utilizando o módulo `subprocess`.
        # `capture_output=False` permite que a saída padrão seja exibida diretamente no console.
        # `text=False` mantém os dados como bytes em vez de strings.
        result = subprocess.run(["python", script_to_run], capture_output=False, text=False)

        # Exibe a saída do script para a instância atual.
        print(f"[OUTPUT] Instância {instance_id} Output:\n{result.stdout}")
        # Verifica se houve erro durante a execução e exibe a mensagem de erro, se presente.
        if result.stderr:
            print(f"[ERROR] Instância {instance_id} Erro:\n{result.stderr}")
    except Exception as e:
        # Captura e exibe qualquer exceção que ocorra durante a execução do script.
        print(f"[ERROR] Instância {instance_id} falhou ao ser executada: {e}")

# Função principal que gerencia a execução multithread.
def main():
    # Cria um pool de threads com um número máximo de trabalhadores definido em `num_threads`.
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Mapeia a função `run_script` para cada instância, variando de 1 até o número total de threads.
        executor.map(run_script, range(1, num_threads + 1))

# Ponto de entrada do programa.
if __name__ == '__main__':
    main()
