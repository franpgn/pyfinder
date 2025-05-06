#!/usr/bin/env bash
set -euo pipefail
export MSYS_NO_PATHCONV=1
export MSYS2_ARG_CONV_EXCL="*"
cd "$(dirname "$0")"

IP="192.168.0.102"
ORG="PampaComputing"
TLS_DIR="../tls"
mkdir -p "$TLS_DIR/ca"

# 1) Create a tiny CA extensions file
cat > ca_ext.cnf <<EOF
[ v3_ca ]
basicConstraints       = critical,CA:true
keyUsage               = critical, digitalSignature, keyCertSign, cRLSign
subjectKeyIdentifier   = hash
EOF

# 2) Generate the CA private key
openssl genrsa -out "$TLS_DIR/ca/ca.key" 4096

# 3) Create a CSR for the CA (no SANs needed)
openssl req -new \
  -key    "$TLS_DIR/ca/ca.key" \
  -subj   "/C=BR/ST=RS/L=Bage/O=$ORG/OU=CA/CN=MyLocalCA" \
  -out    ca.csr

# 4) Self-sign the CA cert WITH the v3_ca extensions
openssl x509 -req \
  -in       ca.csr \
  -signkey  "$TLS_DIR/ca/ca.key" \
  -days     3650 \
  -sha256   \
  -extfile  ca_ext.cnf \
  -extensions v3_ca \
  -out      "$TLS_DIR/ca/ca.crt"

# 5) Clean up
rm -v ca.csr ca_ext.cnf

echo "✅ CA key and cert with CA:true + keyCertSign are in $TLS_DIR/ca"
