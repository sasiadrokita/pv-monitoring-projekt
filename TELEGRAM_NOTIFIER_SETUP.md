# Guide: Setting Up Automatic Telegram Notifications on Boot

This guide explains how to configure your Raspberry Pi to automatically send the new, public Grafana URL to your Telegram whenever the system restarts. This is extremely useful when using Cloudflare Quick Tunnels, as the URL changes with every reboot.

## Prerequisites
- You have a Telegram Bot Token and Chat ID (see [Alerts Setup](./ALERTS_SETUP.md)).
- The Cloudflare Tunnel service is set up and running.

## Step 1: Prepare the Script

1.  Copy the template script from the project to your home directory:
    ```bash
    cp send_url_telegram.sh.example ~/send_url_telegram.sh
    ```
2.  Open the script for editing:
    ```bash
    nano ~/send_url_telegram.sh
    ```
3.  **Fill in your credentials:**
    - Replace `YOUR_BOT_TOKEN_HERE` with your actual Bot Token.
    - Replace `YOUR_CHAT_ID_HERE` with your actual Chat ID.
4.  Save and exit (`Ctrl+O`, `Enter`, `Ctrl+X`).
5.  Make the script executable:
    ```bash
    chmod +x ~/send_url_telegram.sh
    ```

## Step 2: Create a System Service

We need to tell the system to run this script automatically after booting.

1.  Create a new service file:
    ```bash
    sudo nano /etc/systemd/system/telegram-url-notifier.service
    ```
2.  Paste the following configuration (replace `mateusz` with your username if different):
    ```ini
    [Unit]
    Description=Send Cloudflare Tunnel URL to Telegram
    After=network.target cloudflared-tunnel.service
    
    [Service]
    Type=oneshot
    User=mateusz
    ExecStart=/home/mateusz/send_url_telegram.sh
    
    [Install]
    WantedBy=multi-user.target
    ```
3.  Save and exit.

## Step 3: Enable the Service

Enable the service so it starts on boot:
```bash
sudo systemctl enable telegram-url-notifier.service
