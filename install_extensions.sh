#!/bin/bash

# List of extensions to install
extensions=(
        "ms-python.python"
        "ms-toolsai.jupyter"
        "CS50.ddb50"
        # add more extensions here
        "aaron-bond.better-comments",
        "alefragnani.bookmarks",
        "alefragnani.project-manager",
        "changkaiyan.tf2snippets",
        "codezombiech.gitignore",
        "donjayamanne.githistory",
        "eamodio.gitlens",
        "ecmel.vscode-html-css",
        "evondev.indent-rainbow-palettes",
        "formulahendry.code-runner",
        "github.codespaces",
        "github.copilot",
        "github.copilot-chat",
        "hediet.vscode-drawio",
        "kevinrose.vsc-python-indent",
        "kydronepilot.material-deep-ocean-theme",
        "leonardssh.vscord",
        "ms-edgedevtools.vscode-edge-devtools",
        "ms-python.debugpy",
        "ms-python.vscode-pylance",
        "ms-python.vscode-python-envs",
        "ms-toolsai.datawrangler",
        "ms-toolsai.jupyter-keymap",
        "ms-toolsai.jupyter-renderers",
        "ms-toolsai.vscode-jupyter-cell-tags",
        "ms-toolsai.vscode-jupyter-powertoys",
        "ms-toolsai.vscode-jupyter-slideshow",
        "ms-vscode-remote.remote-containers",
        "ms-vscode.test-adapter-converter",
        "pkief.material-icon-theme",
        "thebarkman.vscode-djaneiro",
        "tumzunong.pycharm-like-snippets",
        "usernamehw.errorlens",
        "wholroyd.jinja",
        "ziyasal.vscode-open-in-github",
        "icrawl.discord-vscode",
        "nexmoe.monitor-pro",
        "oderwat.indent-rainbow",
        "ms-vsliveshare.vsliveshare",
        "PreetiPrajapat.documentation-bar",
        "ms-vscode-remote.vscode-remote-extensionpack",
        "donjayamanne.python-extension-pack",
        "christian-kohler.path-intellisense",
        "charliermarsh.ruff",
        "mechatroner.rainbow-csv"
      ]
)

# Install each extension
for extension in "${extensions[@]}"; do
  code --install-extension $extension &
done

# Wait for all background jobs (extension installations) to complete
wait

echo "All extensions have been installed."
