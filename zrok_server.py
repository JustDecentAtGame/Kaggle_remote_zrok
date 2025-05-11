import subprocess
import argparse
from utils import Zrok


def main(token: str):
    zrok = Zrok(token)
    
    if not Zrok.is_installed():
        Zrok.install()

    # Find and delete existing environment
    env = zrok.find_env("kaggle_server")
    if env is not None:
        zrok.delete_environment(env["zId"])

    try:
        subprocess.run(["zrok", "disable"], check=True)
    except Exception as e:
        print(e)
        print("zrok already disable")

    zrok.enable("kaggle_server")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Kaggle SSH connection setup')
    parser.add_argument('--token', help='zrok API token')
    args = parser.parse_args()

    token = args.token
    if not token:
        token = input("Enter your zrok API token: ")

    main(token)