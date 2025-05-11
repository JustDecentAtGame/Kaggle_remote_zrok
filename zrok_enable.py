import requests
import json
import subprocess
import os
import sys
import tarfile
import urllib.request
import argparse


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
        subprocess.run(["zrok", "version"], check=True, capture_output=True)
        print("Zrok installed successfully")
    except subprocess.CalledProcessError:
        print("Error: Zrok install failed")
        sys.exit(1)


def get_zrok_overview(token: str):
    response = requests.get(
        url="https://api-v1.zrok.io/api/v1/overview",
        headers={"x-token": token},
    )
    return response.json()


def delete_zrok_environment(token: str, zid: str):
    headers = {
        "x-token": token,
        "Accept": "*/*",
        "Content-Type": "application/zrok.v1+json"
    }
    payload = {
        "identity": zid
    }
            
    response = requests.post("https://api-v1.zrok.io/api/v1/disable", headers=headers, data=json.dumps(payload))
    return response.json()


def main(token: str):
    # First ensure zrok is installed
    try:
        subprocess.run(["zrok", "version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        install_zrok()

    response = get_zrok_overview(token)

    if response.status_code == 200:
        json_data = response.json()
        # print(json.dumps(json_data, indent=4))

        kaggle_zid = None
        for item in json_data["environments"]:
            env = item["environment"]
            if env["description"].lower() == "kaggle":
                kaggle_zid = env["zId"]
                break
                
        if kaggle_zid:
            response = delete_zrok_environment(token, kaggle_zid)
        
            print("Status Code:", response.status_code)
            print("Response:", response.text)

    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")

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