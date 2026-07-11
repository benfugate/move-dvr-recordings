#!/bin/bash
set -e

PUID=${PUID:-99}
PGID=${PGID:-100}

if ! getent group "$PGID" >/dev/null; then
    groupadd -g "$PGID" appgroup
fi
GROUP_NAME=$(getent group "$PGID" | cut -d: -f1)

if ! getent passwd "$PUID" >/dev/null; then
    useradd -u "$PUID" -g "$PGID" -M -s /usr/sbin/nologin appuser
fi
USER_NAME=$(getent passwd "$PUID" | cut -d: -f1)

chown "$PUID":"$PGID" /var/log/copier.log

gosu "$USER_NAME":"$GROUP_NAME" python3 -u /app/move_recording.py >> /var/log/copier.log 2>&1 &
tail -f /var/log/copier.log