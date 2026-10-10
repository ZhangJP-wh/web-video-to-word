#!/bin/zsh
cd -- "${0:A:h}" || exit 1
export SSL_CERT_FILE=/etc/ssl/cert.pem
export NODE_EXTRA_CA_CERTS=/etc/ssl/cert.pem
.venv/bin/python smoke_qianwen.py
result=$?
read '?测试结束，按回车关闭窗口。'
exit "$result"
