# Unified KVM QEMU libvirt virt manager Installation Guide

This installs a complete local virtualization stack on **Fedora, Ubuntu Debian, and Arch based systems**, including QEMU KVM, libvirt, virt manager, virtual networking, UEFI firmware, SPICE viewer, TPM support, and the command line management tools.

The important connection is `qemu:///system`. This is generally preferable to `qemu:///session` because the system connection supports proper libvirt networking, bridges, storage pools, and VM autostart.

## 1. Fedora

```bash
sudo dnf group install virtualization

sudo dnf install \
    virt-manager \
    virt-install \
    virt-viewer \
    qemu-kvm \
    qemu-img \
    libvirt \
    libvirt-daemon \
    libvirt-daemon-config-network \
    libvirt-daemon-driver-qemu \
    libvirt-client \
    dnsmasq \
    bridge-utils \
    edk2-ovmf \
    swtpm \
    swtpm-tools
```

Enable libvirt:

```bash
sudo systemctl enable --now libvirtd
```

Add your user to libvirt:

```bash
sudo usermod -aG libvirt "$USER"
```

Fedora's virtualization group is the recommended way to pull in the core virtualization stack, while Fedora's documentation separately identifies `libvirt` and `virt-install` as the core packages.

## 2. Ubuntu / Debian

```bash
sudo apt update

sudo apt install \
    qemu-system-x86 \
    qemu-utils \
    qemu-kvm \
    libvirt-daemon-system \
    libvirt-daemon \
    libvirt-clients \
    libvirt-daemon-driver-qemu \
    libvirt-daemon-config-network \
    virt-manager \
    virt-install \
    virt-viewer \
    dnsmasq \
    bridge-utils \
    ovmf \
    swtpm \
    swtpm-tools
```

Enable libvirt:

```bash
sudo systemctl enable --now libvirtd
```

Add your user:

```bash
sudo adduser "$USER" libvirt
```

If the `libvirtd` service is not present on a newer installation, check the libvirt sockets:

```bash
systemctl list-unit-files | grep libvirt
```

Then verify:

```bash
virsh -c qemu:///system
```

## 3. Arch Linux / CachyOS

```bash
sudo pacman -Syu

sudo pacman -S \
    virt-manager \
    virt-install \
    virt-viewer \
    qemu-desktop \
    qemu-img \
    libvirt \
    dnsmasq \
    edk2-ovmf \
    swtpm \
    bridge-utils
```

Enable the libvirt socket:

```bash
sudo systemctl enable --now libvirtd.socket
```

For VM autostart and the traditional daemon setup, also enable:

```bash
sudo systemctl enable --now libvirtd.service
```

Add your user:

```bash
sudo usermod -aG libvirt "$USER"
```

Arch currently documents `libvirtd.socket` for QEMU connections and `libvirtd.service` when daemon based functionality such as domain autostart is required.

## 4. Log out and back in

After modifying group membership:

```bash
logout
```

Log back into your desktop session.

You can alternatively start a new shell with the group:

```bash
newgrp libvirt
```

## 5. Verify KVM

Check that the CPU exposes virtualization:

```bash
lscpu | grep -E 'Virtualization|VT-x|AMD-V'
```

Check KVM:

```bash
ls -l /dev/kvm
```

You should see `/dev/kvm`.

Check the kernel modules:

```bash
lsmod | grep kvm
```

Intel systems should normally show:

```text
kvm_intel
kvm
```

AMD systems should normally show:

```text
kvm_amd
kvm
```

## 6. Verify libvirt

Test the system connection:

```bash
virsh -c qemu:///system
```

Then:

```bash
virsh -c qemu:///system list --all
```

You should get the VM list without a connection error.

Check libvirt:

```bash
virsh -c qemu:///system version
```

Check the daemon:

```bash
systemctl status libvirtd
```

On socket activated systems:

```bash
systemctl status libvirtd.socket
```

## 7. Verify the default virtual network

List networks:

```bash
virsh -c qemu:///system net-list --all
```

You ideally want:

```text
Name      State    Autostart
default   active   yes
```

If `default` exists but is inactive:

```bash
sudo virsh net-start default
sudo virsh net-autostart default
```

If the default network does not exist:

```bash
sudo virsh net-define /usr/share/libvirt/networks/default.xml
sudo virsh net-start default
sudo virsh net-autostart default
```

## 8. Launch virt manager
rtbte-prep
```bash
virt-manager
```

The connection should appear as:
rtbte-prep
```text
QEMU/KVM
```

For the normal system connection, the URI should be:

```text
qemu:///system
```

You can explicitly launch virt manager against it:

```bash
virt-manager --connect qemu:///system
```

`virt-manager` is a graphical frontend to libvirt, while QEMU provides the actual virtualization and libvirt provides the management layer.

## 9. UEFI support

The UEFI packages installed above provide OVMF firmware.

Check Fedora:

```bash
ls /usr/share/edk2/ovmf/
```

Check Arch:

```bash
ls /usr/share/edk2/x64/
```

Check Ubuntu:

```bash
ls /usr/share/OVMF/
```

UEFI firmware is supplied through OVMF, with package names varying by distribution.

## 10. Useful diagnostic commands

### Check all virtualization packages

Fedora:

```bash
rpm -qa | grep -Ei 'qemu|libvirt|virt-manager|ovmf|swtpm'
```

Ubuntu Debian:

```bash
dpkg -l | grep -Ei 'qemu|libvirt|virt-manager|ovmf|swtpm'
```

Arch:

```bash
pacman -Q | grep -Ei 'qemu|libvirt|virt-manager|ovmf|swtpm'
```

### Check libvirt connections

```bash
virsh -c qemu:///system uri
virsh -c qemu:///system nodeinfo
virsh -c qemu:///system list --all
virsh -c qemu:///system net-list --all
virsh -c qemu:///system pool-list --all
```

### Check the libvirt socket

```bash
ls -l /run/libvirt/
```

### Check recent libvirt errors

```bash
sudo journalctl -u libvirtd -b --no-pager
```

Or:

```bash
sudo journalctl -u libvirtd.socket -b --no-pager
```

## 11. If virt manager says "Cannot connect to libvirt"

First test the connection outside virt manager:

```bash
virsh -c qemu:///system
```

If that fails, check:

```bash
systemctl status libvirtd
systemctl status libvirtd.socket
ls -l /dev/kvm
groups
```

Then:

```bash
sudo systemctl restart libvirtd
```

And retry:

```bash
virsh -c qemu:///system
```

If `virsh` works but virt manager does not, explicitly add the connection in virt manager using:

```text
QEMU/KVM
Connection: qemu:///system
```

## 12. Recommended final verification

Run this after installation:

```bash
echo "=== KVM ==="
ls -l /dev/kvm

echo "=== LIBVIRT ==="
virsh -c qemu:///system uri

echo "=== VMS ==="
virsh -c qemu:///system list --all

echo "=== NETWORKS ==="
virsh -c qemu:///system net-list --all

echo "=== STORAGE ==="
virsh -c qemu:///system pool-list --all

echo "=== GROUPS ==="
groups
```

A correctly configured host should give you a working `/dev/kvm`, a successful `qemu:///system` connection, a usable libvirt network, and access to the storage pools.

**Architecture:**

```text
virt-manager
     │
     ▼
libvirt
     │
     ├── QEMU/KVM
     │
     ├── Virtual Networks
     │      └── dnsmasq
     │
     ├── Storage Pools
     │
     ├── UEFI
     │      └── OVMF
     │
     ├── TPM
     │      └── swtpm
     │
     └── Display
            └── SPICE / virt-viewer
```
