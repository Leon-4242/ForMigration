#!/usr/bin/env bash
set -Eeuo pipefail

APP_NAME="Korjik_test"
APP_DIR="/root/${APP_NAME}"
ENV_FILE="${APP_DIR}/.env"
CREDENTIALS_FILE="${APP_DIR}/data/auth/korjik-tgbot.json"
SERVICE_NAME="korjik_test.service"
SOURCE_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

if [[ ${EUID} -ne 0 ]]; then
    echo "Run this installer as root: sudo ./install.sh" >&2
    exit 1
fi

export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y python3 python3-venv python3-pip rsync

if [[ "${SOURCE_DIR}" != "${APP_DIR}" ]]; then
    install -d -o root -g root -m 0700 "${APP_DIR}"
    rsync -a --delete \
        --exclude='.git/' \
        --exclude='.venv/' \
        --exclude='.env' \
        --exclude='data/auth/' \
        --exclude='data/json/' \
        --exclude='data/sqlite_db/' \
        "${SOURCE_DIR}/" "${APP_DIR}/"
fi

install -d -o root -g root -m 0700 \
    "${APP_DIR}/data/auth" \
    "${APP_DIR}/data/json" \
    "${APP_DIR}/data/sqlite_db"

if [[ ! -f "${ENV_FILE}" ]]; then
    echo "Missing ${ENV_FILE}. Create it from ${APP_DIR}/.env.example and fill in the real token." >&2
    exit 1
fi

if [[ ! -f "${CREDENTIALS_FILE}" ]]; then
    echo "Missing ${CREDENTIALS_FILE}. Copy the real Google service-account JSON there." >&2
    exit 1
fi

chown root:root "${ENV_FILE}" "${CREDENTIALS_FILE}"
chmod 0600 "${ENV_FILE}" "${CREDENTIALS_FILE}"

python3 -m venv "${APP_DIR}/.venv"
"${APP_DIR}/.venv/bin/python" -m pip install --upgrade pip
"${APP_DIR}/.venv/bin/python" -m pip install -r "${APP_DIR}/requirements.txt"

install -o root -g root -m 0644 \
    "${SOURCE_DIR}/deploy/korjik_test.service" \
    "/etc/systemd/system/${SERVICE_NAME}"

systemctl daemon-reload
systemctl enable --now "${SERVICE_NAME}"
systemctl --no-pager --full status "${SERVICE_NAME}"
