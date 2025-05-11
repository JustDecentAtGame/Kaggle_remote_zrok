import os
import subprocess
import time
import argparse
from utils import Zrok


def main(token: str):
    zrok = Zrok(token)
    
    if not Zrok.is_installed():
        Zrok.install()

    if not Zrok.is_enabled():
        zrok.enable("client")

    # 1. Get zrok share token
    env = zrok.find_env("kaggle_server")
    if env is None:
        raise Exception("kaggle environment not found")

    share_token = None
    for share in env.get("shares", []):
        if (share.get("backendMode") == "tcpTunnel" and
            share.get("backendProxyEndpoint") == "localhost:22"):
            share_token = share.get("shareToken")
            break

    if not share_token:
        raise Exception("SSH tunnel not found in kaggle environment")

    # 2. Start zrok process
    print(f"zrok access private {share_token}")
    subprocess.Popen(
        ["cmd", "/k", f"zrok access private {share_token}"],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

    # 3. Wait 5 seconds for zrok connection
    time.sleep(5)

    # 4. Update SSH config
    config_path = os.path.join(os.environ['USERPROFILE'], '.ssh', 'config')
    with open(config_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    entry = """Host kaggle-local
HostName 127.0.0.1
User root
Port 9191
IdentityFile ~/.ssh/kaggle_rsa
StrictHostKeyChecking no
UserKnownHostsFile /dev/null""".strip("\n")

    if "Host kaggle-local" not in content:
        with open(config_path, 'w', encoding='utf-8', newline='') as f:
            f.write(content.rstrip("\n") + "\n" + entry)
    else:
        print("SSH config already contains kaggle-local entry")

    # 5. Launch VS Code remote-SSH
    subprocess.Popen(
        ["code", "--remote", "ssh-remote+kaggle-local", "/kaggle/working"],
        shell=True,
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Kaggle SSH connection setup')
    parser.add_argument('--token', help='zrok API token')
    args = parser.parse_args()

    token = args.token
    if not token:
        token = input("Enter your zrok API token: ")

    main(token)  
