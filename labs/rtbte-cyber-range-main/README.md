# BTRTE: Blue Team Red Team Exercise

## What is BTRTE?

## Requirements

* Virtual Machine Manager
* Ubuntu 20.04

## Installation

### Virt Manager

```bash
yay -S virt-manager
```

### Download Ubuntu

#### Ubuntu Desktop

```bash
wget -O ~/Downloads/ISO/ubuntu-20.04.6-desktop-amd64.iso \
https://releases.ubuntu.com/20.04/ubuntu-20.04.6-desktop-amd64.iso
```

> **Important:** Do **not** run `apt update && apt upgrade`. Do not update the machine.

#### Ubuntu Server

```bash
wget https://old-releases.ubuntu.com/releases/20.04.0/ubuntu-20.04-live-server-amd64.iso
```

## Installing crAPI

Once Ubuntu Server has been installed, run the following commands:

```bash
sudo dpkg --configure -a
sudo apt install curl unzip docker-compose-v2
curl -L -o /tmp/crapi.zip https://github.com/OWASP/crAPI/archive/refs/heads/main.zip
unzip /tmp/crapi.zip
cd crAPI-main/deploy/docker
docker compose pull
docker compose -f docker-compose.yml --compatibility up -d
```

These commands download the crAPI repository to the Ubuntu Server, extract it, navigate to the Docker deployment directory, pull the required Docker images, and start the crAPI containers.

For more information, see the [crAPI repository](https://github.com/OWASP/crAPI).

## Setting Up

1. Open Virtual Machine Manager. In the top left corner, click **File** and select **New Virtual Machine**.

<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/5b802839-abbf-4383-8a77-2b10144d1df6" />

2. In the new popup, select **Local install media (ISO image or CDROM)**, then click **Forward**.

<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/6c6d0ab4-b20b-4c00-a03a-f584c6b4a88a" />

3. Click **Browse**.

<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/349eca4f-7533-41d7-b3de-a6aaf723d143" />

4. In the new popup, click **Browse Local** to browse your local files. Navigate to the folder where you downloaded the ISO using the following command:

```bash
wget https://old-releases.ubuntu.com/releases/20.04.0/ubuntu-20.04-live-server-amd64.iso
```

This is where the Ubuntu ISO file will be located.

<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/0dff50a8-d5da-4e7e-a5c3-02fb50e184bb" />

5. Select the ISO from your downloads.

<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/fda778e1-3e20-49e3-a8ae-45d87f22015a" />

6. Make sure the field updates to the Ubuntu 20.04 ISO. Once confirmed, click **Forward**.

<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/81ea0e09-2d66-4cef-94e4-5e16e36a9eae" />

7. Choose the amount of RAM and the number of CPU cores you would like to allocate to the virtual machine.

<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/09eaec84-fb92-4bbd-9d1e-c2c295b91e02" />

8. For the virtual machine's disk size, I recommend allocating **50 GB**.

<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/cdb8d554-52eb-49be-986b-43fa6d21638a" />

9. You can name the virtual machine whatever you prefer.

<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/d077772b-66ba-43bf-bac2-e403385d1320" />

10. For the Ubuntu Server installation process, after completing the Virt Manager setup steps, follow the official [Ubuntu Server installation guide](https://ubuntu.com/tutorials/install-ubuntu-server#1-overview). For the desktop version, see the [Ubuntu Desktop installation guide](https://ubuntu.com/tutorials/install-ubuntu-desktop#5-installation-setup). Skip to [Step 5](https://ubuntu.com/tutorials/install-ubuntu-desktop#5-installation-setup) and [Step 11](https://ubuntu.com/tutorials/install-ubuntu-desktop#11-dont-forget-to-update) of the desktop installation guide.

11. Once you reach the update section of the installation, click **Cancel Update** and restart the machine.
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/8b8520d0-498c-4721-84af-ccda52a0565d" />


## Wazuh Dashboard

For instructions on setting up the Wazuh Dashboard, see the [Wazuh setup guide](https://github.com/Xhanti-mbasa/rtbte-cyber-range/blob/main/Wazuk-setup.md).
