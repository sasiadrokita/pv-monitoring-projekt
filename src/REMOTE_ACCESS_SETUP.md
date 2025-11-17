# Step-by-Step Guide: Setting Up Persistent Remote Access

This guide explains how to set up a secure remote access to your Grafana dashboard using a **Cloudflare Quick Tunnel**. This is the simplest and most reliable method that does not require a Cloudflare account, login, or any router configuration.

The tunnel will be launched as a background process, making it persistent and independent of your SSH session.

**Important:** This method provides a **temporary URL** that is active only as long as the process is running on the Raspberry Pi. The URL will change every time you restart the tunnel (e.g., after a Raspberry Pi reboot).

## Prerequisites

- Your main project (all Docker services) is already running on the Raspberry Pi.
- You are connected to your Raspberry Pi via SSH.

## Step 1: Install `cloudflared` on the Raspberry Pi

If you haven't already, install the Cloudflare Tunnel connector.

1.  Download the package for the ARM64 architecture:
    ```bash
    wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64.deb
    ```

2.  Install the package:
    ```bash
    sudo dpkg -i cloudflared-linux-arm64.deb
    ```

## Step 2: Launch the Tunnel as a Persistent Background Process

We will use the `nohup` command to ensure the tunnel keeps running even after you close your SSH session.

1.  Execute the following command from your project's root directory:
    ```bash
    nohup cloudflared tunnel --url http://localhost:3000 &
    ```
    - `nohup` (no hang up) makes the process immune to session closures.
    - `&` runs the process in the background.

2.  The terminal will immediately return control to you. All output from `cloudflared` will now be redirected to a file named `nohup.out`.

## Step 3: Get Your Public URL

The public URL for your tunnel is now available in the `nohup.out` log file.

1.  Wait about 10-15 seconds for the tunnel to establish a connection.
2.  Display the content of the log file to find your URL:
    ```bash
    cat nohup.out
    ```
3.  Look for the box in the output. It will contain your unique public URL, for example:
    ```
    +------------------------------------------------------------------+
    |  Your quick Tunnel has been created! Visit it at (it may take some time to be reachable):  |
    |  https://some-random-words.trycloudflare.com                     |
    +------------------------------------------------------------------+
    ```

You can now use this URL to access your Grafana dashboard from any device.

## How to Stop the Tunnel

To stop the tunnel, you must log back into the Raspberry Pi and terminate the `cloudflared` process manually.

1.  Find the Process ID (PID) of the running `cloudflared` process:
    ```bash
    ps aux | grep cloudflared
    ```

2.  Kill the process using its PID (replace `<PID>` with the actual number you found):
    ```bash
    kill <PID>
    ```
