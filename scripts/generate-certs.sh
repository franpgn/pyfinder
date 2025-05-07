#!/usr/bin/env bash
set -euo pipefail
export MSYS_NO_PATHCONV=1
export MSYS2_ARG_CONV_EXCL="*"

# Function to get the IP address
get_ip_address() {
    # Detect OS type
    OS=$(uname)

    if [[ "$OS" == "Linux" ]]; then
        # For Linux, use hostname -I
        IP_ADDRESS=$(hostname -I | awk '{print $1}')
    elif [[ "$OS" == "Darwin" ]]; then
        # For macOS, use ifconfig
        IP_ADDRESS=$(ifconfig en0 | grep inet | awk '{print $2}' | head -n 1)
    else
        # For Windows (using Git Bash), use ipconfig
        IP_ADDRESS=$(ipconfig | grep -A 5 "Ethernet adapter" | grep "IPv4" | head -n 1 | cut -d ':' -f2 | tr -d '[:space:]')
    fi
    echo "$IP_ADDRESS"
}

# Get the IP address
IP_ADDRESS=$(get_ip_address)

# Check if the IP address is empty or invalid
if [[ -z "$IP_ADDRESS" || ! "$IP_ADDRESS" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Invalid or empty IP address detected. Please enter your IP address manually:"
    read -p "Enter IP Address: " IP_ADDRESS
fi

echo "Using IP Address: $IP_ADDRESS"

# Proceed with the rest of the script
cd "$(dirname "$0")"
mkdir -p "../tls"
IP="$IP_ADDRESS"
ORG="PampaComputing"
TLS_DIR="../tls"
mkdir -p "$TLS_DIR/ca"

cat > ca_ext.cnf <<EOF
[ v3_ca ]
basicConstraints       = critical,CA:true
keyUsage               = critical, digitalSignature, keyCertSign, cRLSign
subjectKeyIdentifier   = hash
EOF

openssl genrsa -out "$TLS_DIR/ca/ca.key" 4096

openssl req -new \
  -key    "$TLS_DIR/ca/ca.key" \
  -subj   "/C=BR/ST=RS/L=Bage/O=$ORG/OU=CA/CN=MyLocalCA" \
  -out    ca.csr

openssl x509 -req \
  -in       ca.csr \
  -signkey  "$TLS_DIR/ca/ca.key" \
  -days     3650 \
  -sha256   \
  -extfile  ca_ext.cnf \
  -extensions v3_ca \
  -out      "$TLS_DIR/ca/ca.crt"

rm -v ca.csr ca_ext.cnf

echo "CA key and cert with CA:true + keyCertSign are in $TLS_DIR/ca"

cat > server_ext.cnf <<EOF
[ req ]
default_bits       = 2048
prompt             = no
default_md         = sha256
distinguished_name = dn
req_extensions     = v3_req
[ dn ]
C  = BR
ST = RS
L  = Bage
O  = PampaComputing
CN = "$IP_ADDRESS"
[ v3_req ]
subjectAltName = @alt_names
[ alt_names ]
DNS.1 = localhost
IP.1  = 127.0.0.1
IP.2  = "$IP_ADDRESS"
EOF

openssl genrsa -out server.key 2048

openssl req -new \
  -key    server.key \
  -out    server.csr \
  -config server_ext.cnf

openssl x509 -req \
  -in       server.csr \
  -CA       ../tls/ca/ca.crt \
  -CAkey    ../tls/ca/ca.key \
  -CAcreateserial \
  -out      server.crt \
  -days     825 \
  -sha256   \
  -extfile  server_ext.cnf \
  -extensions v3_req

mv server.crt server.key ../tls/

rm server.csr
