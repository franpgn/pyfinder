#!/usr/bin/env bash
set -euo pipefail

# ── disable Git‐Bash path conversion ──
export MSYS_NO_PATHCONV=1
export MSYS2_ARG_CONV_EXCL="*"

IP="192.168.3.17"
ORG="PampaComputing"

# 1) Write SAN config
cat > server_ext.cnf <<EOF
[ req ]
default_bits       = 2048
prompt             = no
default_md         = sha256
distinguished_name = dn

[ dn ]
C  = BR
ST = RS
L  = Bage
O  = $ORG
CN = $IP

[ v3_req ]
subjectAltName = @alt_names

[ alt_names ]
DNS.1 = localhost
IP.1  = 127.0.0.1
IP.2  = 26.76.169.248
IP.3  = $IP
EOF

# 2) CA key
openssl genrsa -out ca.key 4096

# 3) CA cert (self-signed; 10 years)
openssl req -x509 -new -nodes \
  -key ca.key \
  -sha256 \
  -days 3650 \
  -out ca.crt \
  -subj "/C=BR/ST=RS/L=Bage/O=$ORG/OU=CA/CN=MyLocalCA"

# 4) Server key
openssl genrsa -out server.key 2048

# 5) CSR w/ SANs
openssl req -new \
  -key server.key \
  -out server.csr \
  -config server_ext.cnf

# 6) Sign CSR → server.crt + ca.srl
openssl x509 -req \
  -in server.csr \
  -CA ca.crt \
  -CAkey ca.key \
  -CAcreateserial \
  -out server.crt \
  -days 825 \
  -sha256 \
  -extfile server_ext.cnf \
  -extensions v3_req

# 7) Show your files
ls -1 ca.* server.* server_ext.cnf

