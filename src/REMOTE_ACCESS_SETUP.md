k# Step-by-Step Guide: Setting Up an Automated & Persistent Remote Access

This guide explains how to set up a fully automated, persistent, and secure remote access to your Grafana dashboard using a **Cloudflare Tunnel running as a systemd service**.

This is the recommended method for a "fire-and-forget" setup. The tunnel will:
- Start automatically on every boot of the Raspberry Pi.
- Restart automatically if it ever crashes.
- Run completely in the background, independent of any user session.

**Note:** This setup uses a "Quick Tunnel" which provides a **temporary URL**. The URL will be active as long as the Raspberry Pi is running, but a **new URL will be generated after every reboot**. A helper script is included to display the current URL upon SSH login.

## Prerequisites
- Your main project (all Docker services) is already running.
- You are connected to your Raspberry Pi via SSH.

## Step 1: Install `cloudflared`
(If not already installed)

1.  Download the package for the ARM64 architecture:
    ```bash
    wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64.deb
    ```
2.  Install the package:
    ```bash
    sudo dpkg -i cloudflared-linux-arm64.deb
    ```

## Step 2: Create a `systemd` Service for the Tunnel

This will define how the tunnel starts and behaves.

1.  Create a new service definition file using `nano`:
    ```bash
    sudo nano /etc/systemd/system/cloudflared-tunnel.service
    ```
2.  Paste the following content into the editor. **Remember to replace `mateusz` with your actual username if it's different.**
    ```ini
    [Unit]
    Description=Cloudflare Tunnel for Grafana
    After=network.target docker.service
    Wants=docker.service

    [Service]
    User=mateusz
    Group=mateusz
    WorkingDirectory=/home/mateusz/pv-monitoring-projekt
    ExecStart=/usr/local/bin/cloudflared tunnel --url http://localhost:3000
    Restart=always
    RestartSec=5s

    [Install]
    WantedBy=multi-user.target
    ```
3.  Save the file and exit (`Ctrl+O`, `Enter`, `Ctrl+X`).

## Step 3: Enable and Start the Service

Now, we'll tell `systemd` to use our new service.

1.  Reload the `systemd` daemon to recognize the new file:
    ```bash
    sudo systemctl daemon-reload
    ```
2.  Enable the service to start automatically on boot:
    ```bash
    sudo systemctl enable cloudflared-tunnel.service
    ```
3.  Start the service immediately:
    ```bash
    sudo systemctl start cloudflared-tunnel.service
    ```
4.  (Optional) Check the status to ensure it's running without errors:
    ```bash
    sudo systemctl status cloudflared-tunnel.service
    ```

## Step 4: Create a Helper Script to Display the URL

The tunnel's URL is now hidden in the system logs. This script will find it and display it for you.

1.  Create the script file in your home directory:
    ```bash
    nano ~/get_tunnel_url.sh
    ```
2.  Paste the following content:
    ```bash
    #!/bin/bash
    TUNNEL_URL=$(journalctl -u cloudflared-tunnel.service | grep -o 'https://[a-zA-Z0-9-]\+\.trycloudflare\.com' | tail -n 1)

    echo "===================================================================="
    echo "Cloudflare Tunnel Status:"

    if systemctl is-active --quiet cloudflared-tunnel.service; then
      echo -e "\033[0;32m● ACTIVE\033[0m"
      if [ -n "$TUNNEL_URL" ]; then
        echo "Public URL: $TUNNEL_URL"
      else
        echo -e "\033[0;33mURL not found yet. Service might be starting...\033[0m"
      fi
    else
      echo -e "\033[0;31m● INACTIVE or FAILED\033[0m"
      echo "Run 'sudo systemctl status cloudflared-tunnel.service' for details."
    fi
    echo "===================================================================="
    ```
3.  Make the script executable:
    ```bash
    chmod +x ~/get_tunnel_url.sh
    ```

## Step 5: Display the URL on SSH Login

Finally, let's make the script run automatically every time you log in.

1.  Add the script to your `.bashrc` file:
    ```bash
    echo "~/get_tunnel_url.sh" >> ~/.bashrc
    ```

**Setup is complete!** Now, after every reboot, the tunnel will start automatically. When you log in via SSH, you will be greeted with the current public URL of your Grafana dashboard.
