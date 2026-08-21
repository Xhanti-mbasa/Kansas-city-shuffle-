
```
sudo rpm --import https://packages.wazuh.com/key/GPG-KEY-WAZUH

sudo tee /etc/yum.repos.d/wazuh.repo >/dev/null <<'EOF'
[wazuh]
gpgcheck=1
gpgkey=https://packages.wazuh.com/key/GPG-KEY-WAZUH
enabled=1
name=EL-$releasever - Wazuh
baseurl=https://packages.wazuh.com/4.x/yum/
priority=1
EOF

sudo WAZUH_MANAGER="SERVER-IP" dnf install -y wazuh-agent
sudo systemctl enable --now wazuh-agent

```

# Then verify
```
sudo systemctl status wazuh-agent
sudo tail -f /var/ossec/logs/ossec.log
```

# firewall permissions
```
sudo firewall-cmd --permanent --add-port=1514/tcp
sudo firewall-cmd --permanent --add-port=1515/tcp
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```
