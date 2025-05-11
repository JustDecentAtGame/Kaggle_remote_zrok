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


you might want to transfer files around between local and remote, in our case we can use `rsync` for this:

```bash
# from local to remote
rsync -e "ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i ~/.ssh/kaggle_rsa -p 9191" <path_to_the_local_file> root@127.0.0.1:/kaggle/working
```

```bash
# from remote to local
rsync -e "ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i ~/.ssh/kaggle_rsa -p 9191" root@127.0.0.1:<path_to_the_remote_file> <destination_path_in_local>
```


# Acknowledgement
This project is based on [Kaggle_VSCode_Remote_SSH](https://github.com/buidai123/Kaggle_VSCode_Remote_SSH/tree/feat/zrok-integration)
