#!/usr/local/bin/python

import os
import re
from glob import glob
from datetime import datetime

watch_path = "/media/ChannelsDVR/TV/**/*"
dest_path = "/media/Plex/TV Shows/"
watch = glob(watch_path, recursive=True)

shows = {
    "Big Brother": "Big Brother (2000)",
    "The Challenge": "The Challenge - USA (2022)"
}

for file in watch:
    filename = os.path.basename(file)
    if filename.endswith((".ts", "mp4", "mkv", "mpg")):
        try:
            for show, show_dest in shows.items():
                if show in filename:
                    parts = re.match(r".*(S(\d+)E\d+).*", filename)
                    season_number = parts.group(2).lstrip("0")
                    new_location = f"{dest_path}/{show_dest}/Season {season_number}/"

                    if any(parts.group(1) in existing_file for existing_file in reversed(glob(f"{new_location}*"))):
                        continue

                    print(f"Creating hard link for {filename}... ", end="")
                    os.makedirs(new_location, exist_ok=True, mode=0o755)
                    os.link(file, f"{new_location}{filename}")
                    print("Success!")
                    break
        except Exception as e:
            print(f"Error: {e}")

print(f"Heartbeat... {datetime.now().isoformat()}")
