import urllib.request
import os
import sys
import tarfile
import json
import subprocess

def get_zrok_overview(token: str):
    req = urllib.request.Request(
        url="https://api-v1.zrok.io/api/v1/overview",
        headers={"x-token": token},
    )

    with urllib.request.urlopen(req) as response:
        status = response.getcode()
        data = response.read().decode('utf-8')
        data = json.loads(data) 

    if status != 200:
        print(f"Error: {status}")
        raise Exception("zrok API overview error")
    
    return data


def delete_zrok_environment(token: str, zid: str):
    headers = {
        "x-token": token,
        "Accept": "*/*",
        "Content-Type": "application/zrok.v1+json"
    }
    payload = {
        "identity": zid
    }
    
    data_bytes = json.dumps(payload).encode('utf-8')
    
    req = urllib.request.Request("https://api-v1.zrok.io/api/v1/disable", headers=headers, data=data_bytes, method="POST")
    with urllib.request.urlopen(req) as response:
        status = response.getcode()
        data_text = response.read().decode('utf-8')
        data = json.loads(data_text)

    if status != 200:
        return None

    return data


def install_zrok():
    print("Downloading latest zrok release")
    # Get latest release info
    response = urllib.request.urlopen("https://api.github.com/repos/openziti/zrok/releases/latest")
    data = json.loads(response.read())
    
    # Find linux_amd64 tar.gz download URL
    download_url = None
    for asset in data["assets"]:
        if "linux_amd64.tar.gz" in asset["browser_download_url"]:
            download_url = asset["browser_download_url"]
            break
    
    if not download_url:
        print("Error: Could not find zrok download URL")
        sys.exit(1)
    
    # Download zrok
    urllib.request.urlretrieve(download_url, "zrok.tar.gz")
    
    print("Extracting Zrok")
    try:
        with tarfile.open("zrok.tar.gz", "r:gz") as tar:
            tar.extractall("/usr/local/bin/")
        os.remove("zrok.tar.gz")
    except Exception as e:
        print(f"ERROR: Failed to extract Zrok: {e}")
        sys.exit(1)
    
    # Check if zrok is installed correctly
    try:
        subprocess.run(["zrok", "version"], check=True)
        print("Zrok installed successfully")
    except subprocess.CalledProcessError:
        print("Error: Zrok install failed")
        sys.exit(1)


def is_zrok_installed():
    try:
        subprocess.run(["zrok", "version"], check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False