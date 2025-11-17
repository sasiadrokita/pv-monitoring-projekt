# PV Monitoring System on the Edge

This project provides a complete, Docker-based solution for monitoring Photovoltaic (PV) systems in real-time, designed to run on a low-power edge device like a Raspberry Pi.

The system collects data, stores it in a time-series database, and visualizes it through a web-based dashboard. This `README` serves as a comprehensive step-by-step guide to set up the entire environment from a fresh Raspberry Pi OS installation.

---

## Table of Contents
1.  [Prerequisites](#prerequisites)
2.  [Step 1: Preparing the Raspberry Pi OS](#step-1-preparing-the-raspberry-pi-os)
3.  [Step 2: First Boot and System Setup](#step-2-first-boot-and-system-setup)
4.  [Step 3: Installing Docker and Cloning the Project](#step-3-installing-docker-and-cloning-the-project)
5.  [Step 4: Launching the Application](#step-4-launching-the-application)
6.  [Step 5: Accessing the Services](#step-5-accessing-the-services)
7.  [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Hardware
- A Raspberry Pi 4 (4 GB RAM recommended).
- A reliable power supply (official one is best).
- A high-endurance microSD card (min. 32 GB, A1/A2 class recommended).
- A host computer to prepare the SD card.
- An internet connection (Ethernet cable is recommended for stability).

## Step 1: Preparing the Raspberry Pi OS

This setup is "headless," meaning you won't need to connect a monitor or keyboard to the Pi.

1.  **Download Raspberry Pi Imager** on your host computer from the [official website](https://www.raspberrypi.com/software/).

2.  **Insert the microSD card** into your computer.

3.  **Run Raspberry Pi Imager** and configure it as follows:
    -   **Device**: `Raspberry Pi 4`.
    -   **Operating System**: Choose `Raspberry Pi OS (other)` -> `Raspberry Pi OS Lite (64-bit)`.
    -   **Storage**: Select your microSD card.
    -   Click `Next`, then click **`EDIT SETTINGS`**.

4.  **In the Advanced Settings menu:**
    -   **General tab**:
        -   Set a hostname (e.g., `pv-monitor`).
        -   Set a username (e.g., `mateusz`) and a strong password.
        -   (Optional) Configure your Wi-Fi credentials if not using Ethernet.
    -   **Services tab**:
        -   **Crucial Step**: Check the box to **`Enable SSH`** and select `Use password authentication`.
    -   Click `SAVE`.

5.  **Write the OS**: Click `WRITE` and wait for the process to complete.

## Step 2: First Boot and System Setup

1.  Insert the prepared microSD card into your Raspberry Pi.
2.  Connect the Ethernet cable (if using) and the power supply. Wait 2-3 minutes for the first boot.
3.  **Connect to your Pi via SSH** from your host computer's terminal (e.g., PowerShell, CMD, or any Linux/macOS terminal).

    ```bash
    # Replace 'mateusz' with your username and 'pv-monitor.local' with your hostname
    ssh mateusz@pv-monitor.local
    ```
    - On the first connection, type `yes` to trust the device.
    - Enter the password you created. You are now in control of your Raspberry Pi!

4.  **Update the system**:
    ```bash
    sudo apt update
    sudo apt full-upgrade -y
    ```

## Step 3: Installing Docker and Cloning the Project

1.  **Install Git**:
    ```bash
    sudo apt install git -y
    ```

2.  **Install Docker Engine**:
    Use the official convenience script to get the latest version.
    ```bash
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    ```

3.  **Add your user to the `docker` group**:
    This allows you to run Docker commands without `sudo`.
    ```bash
    sudo usermod -aG docker $USER
    ```

4.  **Reboot the system** to apply the group changes. You will be disconnected.
    ```bash
    sudo reboot
    ```

5.  **Reconnect via SSH** after about a minute.
    ```bash
    ssh mateusz@pv-monitor.local
    ```

6.  **Clone the project repository**:
    You will need a **Personal Access Token (PAT)** from GitHub to clone a private repository via HTTPS. Use the PAT instead of your password.
    ```bash
    git clone https://github.com/sasiadrokita/pv-monitoring-projekt.git
    cd pv-monitoring-projekt
    ```

## Step 4: Launching the Application

Now that Docker is installed and the project is cloned, you can start all the services with a single command.

```bash
# This command reads the docker-compose.yml file, builds the custom pv-simulator image,
# and starts all containers in the background.
docker compose up -d --build


---

## (Optional) Remote Access Setup

For users who wish to access the Grafana dashboard from outside their local network, a detailed guide on setting up a persistent, secure tunnel via Cloudflare is available. This setup is simple and does not require any router configuration.

➡️ **[View the Remote Access Setup Guide](./REMOTE_ACCESS_SETUP.md)**
---

## (Optional) Alerting Setup

A comprehensive guide on how to configure critical system health alerts via Telegram is available. This allows you to be notified immediately if the system stops sending data.

➡️ **[View the Alerting Setup Guide](./ALERTS_SETUP.md)**
