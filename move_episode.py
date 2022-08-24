#!/usr/local/bin/python

"""
This script has a very specific use case. It should not be useful after Season 24 of Big Brother, or at the very least
the renaming aspect of this script shouldn't be.

Currently, 'Big Brother' has the incorrect episode numbers, and show name from the electronic program guide (EPG).
This script gets around these issues by renaming the episode to represent the correct number, and move the file from
a temp storage directory to the "Season 24" folder of "Big Brother (US)" mounted to "/dest/". This will cause Plex
to refresh metadata, and properly show the recorded episode as expected.

Scripts in Tautulli are set up to refresh Sonarr so the episode can be monitored and managed after this is done.
"""

import os
import re
import shutil
from glob import glob

watch = glob("/watch/**/*", recursive=True)
for file in watch:
    filename = os.path.basename(file)
    if filename.endswith((".ts", "mp4", "mkv")):
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
