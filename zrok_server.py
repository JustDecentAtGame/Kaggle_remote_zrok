import subprocess
import argparse
from utils import *

    
def main(token: str):
    if not is_zrok_installed():
        install_zrok()

    response = get_zrok_overview(token)

    if response is not None and response['environments'] is not None:
        kaggle_zid = None
        for item in response["environments"]:
            env = item["environment"]
            if env["description"].lower() == "kaggle":
                kaggle_zid = env["zId"]
                break
                
        if kaggle_zid:
            response = delete_zrok_environment(token, kaggle_zid)
        
            print("Status Code:", response.status_code)
            print("Response:", response.text)

    try:
        subprocess.run(["zrok", "disable"], check=True)
    except Exception as e:
        print(e)
        print("zrok already disable")

    subprocess.run(["zrok", "enable", token, "-d", "kaggle"], check=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Kaggle SSH connection setup')
    parser.add_argument('--token', help='zrok API token')
    args = parser.parse_args()

    token = args.token
    if not token:
        token = input("Enter your zrok API token: ")

    main(token)  