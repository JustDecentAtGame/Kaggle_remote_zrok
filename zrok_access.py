import os
import subprocess
import time
import argparse
from utils import get_zrok_overview, delete_zrok_environment

def main(token: str):
    try:
        # 1. Get zrok share token
        overview = get_zrok_overview(token)

        if overview is not None:
            raise Exception("zrok API overview error")

        share_token = None
        for item in overview["environments"]:
            env = item.get("environment", {})
            if env.get("description") == "kaggle":
                for share in item.get("shares", []):
                    if (share.get("backendMode") == "tcpTunnel" and
                        share.get("backendProxyEndpoint") == "localhost:22"):
                        share_token = share.get("shareToken")
                        break

        if not share_token:
            raise Exception("kaggle environment not found")

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

    except Exception as e:
        print(e)
        input("Press Enter to exit")
        return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Kaggle SSH connection setup')
    parser.add_argument('--token', help='zrok API token')
    args = parser.parse_args()

    token = args.token
    if not token:
        token = input("Enter your zrok API token: ")

    main(token)  
