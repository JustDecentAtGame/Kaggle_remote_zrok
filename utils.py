import urllib.request
import os
import sys
import tarfile
import json
import subprocess

class Zrok:
    def __init__(self, token: str):
        """Initialize Zrok instance with API token.
        
        Args:
            token (str): Zrok API token for authentication
        """
        self.token = token
        self.base_url = "https://api-v1.zrok.io/api/v1"

    def get_env(self):
        """Get overview of all zrok environments.
        
        Makes an API call to fetch information about all environments, including their
        shares and configurations.
        
        Returns:
            dict: Overview data containing environments information
            None: If the API call fails or no environments exist
        """
        req = urllib.request.Request(
            url=f"{self.base_url}/overview",
            headers={"x-token": self.token},
        )

        with urllib.request.urlopen(req) as response:
            status = response.getcode()
            data = response.read().decode('utf-8')
            data = json.loads(data) 

        if status != 200:
            print(f"Error: {status}")
            raise Exception("zrok API overview error")
        
        return data['environments']

    def find_env(self, name: str):
        """Find a specific environment by its name.
        
        Args:
            name (str): Name/description of the environment to find (case-insensitive)
        
        Returns:
            dict: Environment information if found
            None: If no environment matches the given name
        """
        overview = self.get_env()
        if overview is None:
            return None

        for item in overview:
            env = item["environment"]
            if env["description"].lower() == name.lower():
                return item
            
        return None

    def delete_environment(self, zId: str):
        """Delete a zrok environment by its ID.
        
        Args:
            zid (str): The environment ID to delete
        
        Returns:
            bool: True if the environment was successfully deleted, False otherwise
        """
        headers = {
            "x-token": self.token,
            "Accept": "*/*",
            "Content-Type": "application/zrok.v1+json"
        }
        payload = {
            "identity": zId
        }
        
        data_bytes = json.dumps(payload).encode('utf-8')
        
        req = urllib.request.Request(f"{self.base_url}/disable", headers=headers, data=data_bytes, method="POST")
        with urllib.request.urlopen(req) as response:
            status = response.getcode()

        if status != 200:
            raise Exception("Failed to delete environment")

        return True

    def enable(self, name: str):
        """Enable zrok with the specified environment name.
        
        This method runs the 'zrok enable' command with the provided token and
        environment name. It will create a new environment if one doesn't exist.
        
        Args:
            name (str): Name/description for the zrok environment
            
        Raises:
            RuntimeError: If enable command fails
        """
        subprocess.run(["zrok", "enable", self.token, "-d", name], check=True)

    @staticmethod
    def install():
        """Install the latest version of zrok.
        
        This method:
        1. Downloads the latest zrok release from GitHub
        2. Extracts the binary to /usr/local/bin/
        3. Verifies the installation
        """
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
            raise FileNotFoundError("Could not find zrok download URL for linux_amd64")
        
        # Download zrok
        urllib.request.urlretrieve(download_url, "zrok.tar.gz")
        
        print("Extracting Zrok")
        with tarfile.open("zrok.tar.gz", "r:gz") as tar:
            tar.extractall("/usr/local/bin/")
        os.remove("zrok.tar.gz")

        # Check if zrok is installed correctly
        if not Zrok.is_installed():
            raise RuntimeError("Failed to verify zrok installation")
        
        print("Successfully installed zrok")

    @staticmethod
    def is_installed():
        """Check if zrok is installed and accessible.
        
        Returns:
            bool: True if zrok is installed and can be executed, False otherwise
        """
        try:
            subprocess.run(["zrok", "version"], check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    @staticmethod
    def is_enabled() -> bool:
        """Check if zrok is enabled.
        
        Returns:
            bool: True if zrok is enabled (Account Token and Ziti Identity are set), False otherwise
        """
        try:
            result = subprocess.run(
                ["zrok", "status"],
                capture_output=True,
                text=True,
                check=True
            )
            # Check if both Account Token and Ziti Identity are set
            return "Account Token  <<SET>>" in result.stdout and "Ziti Identity  <<SET>>" in result.stdout
        except subprocess.CalledProcessError:
            return False
        except FileNotFoundError:
            return False
