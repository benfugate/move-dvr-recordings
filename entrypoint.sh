#!/bin/bash
python3 -u move_episode.py >> /var/log/copier.log 2>&1 &
tail -f /var/log/copier.log