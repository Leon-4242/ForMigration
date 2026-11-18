# Korjik_test deployment

The layout matches the existing installation on `bots-server`:

- application: `/root/Korjik_test`;
- Telegram token: `/root/Korjik_test/.env`;
- Google credentials: `/root/Korjik_test/data/auth/korjik-tgbot.json`;
- virtual environment: `/root/Korjik_test/.venv`;
- service: `korjik_test.service`.

The repository intentionally contains no production secrets or user databases.

## Install

Place the real secret files at their existing paths, then run the installer from
this directory on an Ubuntu/Debian server:

```bash
sudo install -d -o root -g root -m 0700 /root/Korjik_test/data/auth
sudo install -o root -g root -m 0600 /secure/path/Korjik_test.env \
  /root/Korjik_test/.env
sudo install -o root -g root -m 0600 /secure/path/korjik-tgbot.json \
  /root/Korjik_test/data/auth/korjik-tgbot.json

sudo ./install.sh
```

The installer copies code to `/root/Korjik_test` when necessary, preserves the
secret and runtime-data paths, builds `/root/Korjik_test/.venv`, installs
dependencies, and enables `korjik_test.service` with automatic restart.

Useful commands:

```bash
sudo systemctl status korjik_test
sudo journalctl -u korjik_test -f
sudo systemctl restart korjik_test
```

Re-running `install.sh` updates code and dependencies while preserving runtime
files under `data/auth`, `data/json`, and `data/sqlite_db`.
