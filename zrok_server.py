import subprocess
import argparse
from utils import Zrok


def main(args):
    zrok = Zrok(args.token, args.name)
    
    if not Zrok.is_installed():
        Zrok.install()

    zrok.disable()
    zrok.enable()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Kaggle SSH connection setup')
    parser.add_argument('--token', help='zrok API token')
    parser.add_argument('--name', default='kaggle_server', help='Environment name to create (default: kaggle_server)')
    args = parser.parse_args()

    if not args.token:
        args.token = input("Enter your zrok API token: ")

    main(args)