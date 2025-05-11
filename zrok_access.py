import os
import subprocess
import time
import re
import urllib.request
import json
import argparse


def main(token: str):
    try:
        # 1. Get zrok share token
        req = urllib.request.Request(
            url="https://api-v1.zrok.io/api/v1/overview",
            headers={"x-token": token},
        )

        with urllib.request.urlopen(req) as response:
            status = response.getcode()
            data = response.read().decode('utf-8')
            data = json.loads(data)

        if status != 200:
            raise Exception("zrok API 응답이 올바르지 않습니다.")

        share_token = None
        for item in data["environments"]:
            env = item.get("environment", {})
            if env.get("description") == "kaggle":
                for share in item.get("shares", []):
                    if (share.get("backendMode") == "tcpTunnel" and
                        share.get("backendProxyEndpoint") == "localhost:22"):
                        share_token = share.get("shareToken")
                        break

        if not share_token:
            raise Exception("kaggle 환경의 share token을 찾을 수 없습니다.")

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
            print("SSH config에 이미 kaggle-local 설정이 존재합니다.")

        # 5. Launch VS Code remote-SSH
        subprocess.Popen(
            ["code", "--remote", "ssh-remote+kaggle-local", "/kaggle/working"],
            shell=True,
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )

    except Exception as e:
        print(f"오류 발생: {e}")
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
