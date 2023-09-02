#!/bin/bash
python3 -u move_recording.py >> /var/log/copier.log 2>&1 &
tail -f /var/log/copier.log