#!/usr/local/bin/python

from glob import glob
import shutil
import re

watch = glob("/watch")
for file in watch:
    if file.endswith((".mkv", "mp4")):
        try:
            parts = re.match(r"(.*S\d+E)(\d+)(.*)", file)
            episode_number = int(parts.group(2))
            new_episode_number = f"{(episode_number + 1):02d}"
            new_filename = parts.group(1) + new_episode_number + parts.group(3)
            print(f"Changing {file} to {new_filename}...")
            shutil.copyfile(f"/watch/{file}", f"/dest/{new_filename}")
            print("Success!")
        except Exception as e:
            print(f"Error: {e}")
