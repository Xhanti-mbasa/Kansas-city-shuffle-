#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

HOST_IP="$(
python3 - <<'PY'
import socket

def detect_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("1.1.1.1", 80))
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()

print(detect_ip())
PY
)"

port_free() {
python3 - "$1" <<'PY'
import socket
import sys

port = int(sys.argv[1])
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind(("0.0.0.0", port))
    print("free")
except OSError:
    print("busy")
finally:
    s.close()
PY
}

DNS_HOST_PORT=53
if [ "$(port_free 53)" != "free" ]; then
    DNS_HOST_PORT=8053
fi

MAILHOG_WEB_PORT=8025
if [ "$(port_free 8025)" != "free" ]; then
    MAILHOG_WEB_PORT=18025
fi

cat > domains <<EOF
${HOST_IP} portal.school.local
${HOST_IP} mail.school.local
${HOST_IP} blue.school.local
${HOST_IP} wazuh.school.local
${HOST_IP} dns.school.local
EOF

cat > endpoints <<EOF
host_ip=${HOST_IP}
portal=http://${HOST_IP}:8080
mailhog=http://${HOST_IP}:${MAILHOG_WEB_PORT}
dns_port=${DNS_HOST_PORT}
EOF

export DNS_HOST_PORT MAILHOG_WEB_PORT

docker compose up --build -d

printf '\nLab endpoints:\n'
printf '  portal: http://%s:8080\n' "$HOST_IP"
printf '  mailhog: http://%s:%s\n' "$HOST_IP" "$MAILHOG_WEB_PORT"
printf '  dns: %s:%s\n' "$HOST_IP" "$DNS_HOST_PORT"
