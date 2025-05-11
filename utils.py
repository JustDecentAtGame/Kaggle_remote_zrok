import urllib.request
import json

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
        return None
    
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
            
    response = urllib.request.Request("https://api-v1.zrok.io/api/v1/disable", headers=headers, data=json.dumps(payload))
    with urllib.request.urlopen(response) as response:
        status = response.getcode()
        data = response.read().decode('utf-8')
        data = json.loads(data)

    if status != 200:
        return None

    return data