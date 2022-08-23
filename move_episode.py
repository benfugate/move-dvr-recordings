#!/usr/local/bin/python

import os
import re
import shutil
from glob import glob

watch = glob("/watch/**/*", recursive=True)
for file in watch:
    filename = os.path.basename(file)
    if filename.endswith((".mkv", "mp4")):
        try:
            parts = re.match(r"(.*S\d+E)(\d+)(.*)", filename)
            episode_number = int(parts.group(2))
            new_episode_number = f"{(episode_number + 1):02d}"
            new_filename = parts.group(1) + new_episode_number + parts.group(3)
            print(f"Changing {filename} to {new_filename}... ", end="")
            shutil.move(file, f"/dest/{new_filename}")
            print("Success!")
        except Exception as e:
            print(f"Error: {e}")

for folder, _, _ in os.walk("/watch", topdown=False):  # Listing the files
    if folder == "/watch":
        break
    try:
        os.rmdir(folder)
    except OSError as ex:
        continue
