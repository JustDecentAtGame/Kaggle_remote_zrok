import subprocess
import argparse
from utils import Zrok


def main(args):
    zrok = Zrok(args.token)
    
    if not Zrok.is_installed():
        Zrok.install()

    # Find and delete existing environment
    env = zrok.find_env(args.name)
    if env is not None:
        zrok.delete_environment(env["zId"])

    # for clear file
    try:
        subprocess.run(["zrok", "disable"], check=True)
    except Exception as e:
        print(e)
        print("zrok already disable")

    zrok.enable(args.name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Kaggle SSH connection setup')
    parser.add_argument('--token', help='zrok API token')
    parser.add_argument('--name', default='kaggle_server', help='Environment name to create (default: kaggle_server)')
    args = parser.parse_args()

    if not args.token:
        args.token = input("Enter your zrok API token: ")

    main(args)