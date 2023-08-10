#!/usr/local/bin/python

import os
import re
import shutil
from glob import glob
from datetime import datetime

watch = glob("/watch/**/*", recursive=True)

shows = {
    "Big Brother (2000)": "Big Brother (2000)",
    "The Challenge": "The Challenge - USA (2022)"
}

for file in watch:
    filename = os.path.basename(file)
    if filename.endswith((".ts", "mp4", "mkv")):
        try:
            for show in shows.keys():
                if show in filename:
                    parts = re.match(r".*S(\d+)E\d+.*", filename)
                    season_number = parts.group(1)
                    print(f"Moving {filename}... ", end="")
                    new_filename = filename
                    shutil.move(file, f"/dest/{shows[show]}/Season {season_number}/{new_filename}")
                    print("Success!")
                    break
                else:
                    print(f"Show not recognized: {filename}")
                    raise NotImplemented
        except Exception as e:
            print(f"Error: {e}")

for folder, _, _ in os.walk("/watch", topdown=False):  # Listing the files
    if folder == "/watch":
        break
    try:
        os.rmdir(folder)
    except OSError as ex:
        continue

print(f"Heartbeat... {datetime.now().isoformat()} Watch: {watch}")
