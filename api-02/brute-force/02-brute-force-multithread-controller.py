import subprocess 
from concurrent.futures import ThreadPoolExecutor

#configuration
script_to_run = "brute-force/02-brute-force-multithread.py"
num_threads = 100

#script execution function
def run_script(instance_id):
    print(f"[INFO] Starting instance {instance_id}")

    try:
        result = subprocess.run(["python", script_to_run], capture_output=False, text=False)

        print(f"[OUTPUT] Instance {instance_id} Output:\n{result.stdout}")
        if result.stderr:
            print(f"[ERROR] Instance {instance_id} Error:\n{result.stderr}")
    except Exception as e:
        print(f"[ERROR] Failed to execute instance {instance_id}: {e}")

def main():
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        executor.map(run_script, range(1, num_threads + 1))

if __name__ == '__main__':
    main()