# Korjik_test deployment

The repository intentionally contains no production secrets or user databases.
Keep the Telegram token, Google service-account key, SQLite databases, and runtime
JSON files on the target server only.

## Install

From this directory on an Ubuntu/Debian server:

```bash
sudo install -o root -g root -m 0600 .env.example /etc/Korjik_test.env
sudo editor /etc/Korjik_test.env

sudo install -d -o root -g root -m 0750 /etc/Korjik_test
sudo install -o root -g root -m 0600 /secure/path/google-service-account.json \
  /etc/Korjik_test/google-service-account.json

sudo ./install.sh
```

The installer creates a dedicated `korjik_test` system user, installs the app in
`/opt/Korjik_test`, builds `/opt/Korjik_test/.venv`, installs dependencies, and
enables `korjik_test.service` with automatic restart.

Useful commands:

```bash
sudo systemctl status korjik_test
sudo journalctl -u korjik_test -f
sudo systemctl restart korjik_test
```

Re-running `install.sh` updates code and dependencies while preserving runtime
files under `data/auth`, `data/json`, and `data/sqlite_db`.
