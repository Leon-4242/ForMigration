#!/usr/bin/env bash
set -Eeuo pipefail

APP_NAME="Korjik_test"
APP_USER="korjik_test"
APP_GROUP="korjik_test"
APP_DIR="/opt/${APP_NAME}"
ENV_FILE="/etc/${APP_NAME}.env"
CREDENTIALS_DIR="/etc/${APP_NAME}"
CREDENTIALS_FILE="${CREDENTIALS_DIR}/google-service-account.json"
SERVICE_NAME="korjik_test.service"
SOURCE_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

if [[ ${EUID} -ne 0 ]]; then
    echo "Run this installer as root: sudo ./install.sh" >&2
    exit 1
fi

if [[ ! -f "${ENV_FILE}" ]]; then
    echo "Missing ${ENV_FILE}. Create it from .env.example and fill in real values." >&2
    exit 1
fi

if [[ ! -f "${CREDENTIALS_FILE}" ]]; then
    echo "Missing ${CREDENTIALS_FILE}. Install the Google service-account JSON with mode 0640." >&2
    exit 1
fi

export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y python3 python3-venv python3-pip rsync

if ! getent group "${APP_GROUP}" >/dev/null; then
    groupadd --system "${APP_GROUP}"
fi

if ! id -u "${APP_USER}" >/dev/null 2>&1; then
    useradd --system --gid "${APP_GROUP}" --home-dir "${APP_DIR}" --shell /usr/sbin/nologin "${APP_USER}"
fi

install -d -o "${APP_USER}" -g "${APP_GROUP}" -m 0750 "${APP_DIR}"
install -d -o root -g "${APP_GROUP}" -m 0750 "${CREDENTIALS_DIR}"
chown root:"${APP_GROUP}" "${ENV_FILE}" "${CREDENTIALS_FILE}"
chmod 0640 "${ENV_FILE}" "${CREDENTIALS_FILE}"

rsync -a --delete \
    --exclude='.git/' \
    --exclude='.venv/' \
    --exclude='.env' \
    --exclude='data/auth/' \
    --exclude='data/json/' \
    --exclude='data/sqlite_db/' \
    "${SOURCE_DIR}/" "${APP_DIR}/"

install -d -o "${APP_USER}" -g "${APP_GROUP}" -m 0700 \
    "${APP_DIR}/data/auth" \
    "${APP_DIR}/data/json" \
    "${APP_DIR}/data/sqlite_db"

python3 -m venv "${APP_DIR}/.venv"
"${APP_DIR}/.venv/bin/python" -m pip install --upgrade pip
"${APP_DIR}/.venv/bin/python" -m pip install -r "${APP_DIR}/requirements.txt"

chown -R root:"${APP_GROUP}" "${APP_DIR}"
chmod -R g+rX,o-rwx "${APP_DIR}"
chown -R "${APP_USER}:${APP_GROUP}" "${APP_DIR}/data"
install -o root -g root -m 0644 \
    "${SOURCE_DIR}/deploy/korjik_test.service" \
    "/etc/systemd/system/${SERVICE_NAME}"

systemctl daemon-reload
systemctl enable --now "${SERVICE_NAME}"
systemctl --no-pager --full status "${SERVICE_NAME}"
