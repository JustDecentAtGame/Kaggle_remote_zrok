# Kaggle_zrok
This project communicates directly over HTTP with zrok’s official web console (API v1) and fully leverages OpenZiti’s dual‐plane architecture:

- Control Plane: A centralized authentication and management service that automatically retrieves and synchronizes user environment data in real time, eliminating repetitive setup tasks.

- Data Plane: A distributed P2P overlay network that attempts direct peer connections whenever possible and falls back to relay servers only when necessary, delivering high bandwidth and reliability at no cost.

This allows developers to experience a secure and efficient tunneling environment. The integration with Kaggle via SSH serves merely as one example by adapting the provided code, you can easily extend this advanced approach to other platforms and use cases.




## zrok compare ngrok

| Feature                | zrok          | ngrok               |
| ---------------------- | ------------- | ------------------- |
| Data Transfer       | 150GB/month | 1GB/month           |
| Open Source        | Yes           | No                  |
| Credit Card Required | No          | Yes (for free plan) |
| Free Plan              | Yes           | Yes                 |
| Self-hosting           | Do your thing | Enterprise only     |
| Security Model         | Zero Trust Network | VPN-based tunneling |
| Connection Type	| P2P-first (relay as fallback) | Central relay-based |




## Setup

### Step 1 : Zrok 
Create an account at [zrok](https://zrok.io) and copy your auth token

### Step 2 : Setup SSH public key authentication (Optional)

<details>
<summary>
Click to see how to setup SSH public key authentication

</summary>
Kaggle notebooks are ephemeral Linux servers, so they don't use public key authentication by default.
However, you can still choose to use public key authentication if you prefer.

Follow the prompts. Save the keys in the location ~/.ssh/kaggle_rsa


```sh
ssh-keygen -t rsa -b 4096 -C "kaggle_remote_ssh" -f ~/.ssh/kaggle_rsa
```


Now you got the key pair, what you need to do now is pushing that key to whatever remote server that allows us to fetch it(google drive, or github, gitlab, ...), here i use github

Create a new repo, copy `~/.ssh/kaggle_rsa.pub` to that repo and push it to github(remember to make a public repo), now the public key is available on github, you now need to head over to that repository and click to the public key you've pushed now you click to raw button at the top right and copy the url

You can provide this URL as the authorized_keys_url argument when running zrok_server.py.

```sh
!python3 zrok_server.py --token <zrok token> --authorized_keys_url <key url>
```
</details>

### Step 3 : Setup Kaggle Notebook

[kaggle-zrok notebook](https://www.kaggle.com/code/kayak0/kaggle-zrok) 

Go to the link and click Copy & Edit to copy the notebook.

In Session options, change internet to on and start the session to run the example notebook cells.

This will automatically set up an environment named **kaggle_server**.

### Step 4 : Setup local machine

Install [**zrok**](https://docs.zrok.io/docs/guides/install/) and [**vscode**](https://code.visualstudio.com/download) on your local machine. 

Additionally, you need to install the vscode extension [**Remote-SSH**](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh) to run the **code --remote ssh-remote** command.

Finally, run the zrok_client.py file.

```bash
python zrok_client.py
# or 
python zrok_client.py --token <zrok token>
```

## Notice
- you might want to transfer files around between local and remote, in our case we can use `rsync` for this:

```bash
# from local to remote
rsync -e "ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i ~/.ssh/kaggle_rsa -p 9191" <path_to_the_local_file> root@127.0.0.1:/kaggle/working
```

```bash
# from remote to local
rsync -e "ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i ~/.ssh/kaggle_rsa -p 9191" root@127.0.0.1:<path_to_the_remote_file> <destination_path_in_local>
```

- To minimize exceptions, the environment is disabled and re-enabled each time the code runs. This approach helps maintain stability. The code can be modified to run faster, but doing so may lead to numerous errors.  
Also, there may be exceptional situations in these operations. In such cases, you should access https://api-v1.zrok.io/ and manually delete the conflicting environments.




# Acknowledgement
This project is based on [Kaggle_VSCode_Remote_SSH](https://github.com/buidai123/Kaggle_VSCode_Remote_SSH/tree/feat/zrok-integration)
