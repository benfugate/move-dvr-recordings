#!/usr/local/bin/python

import os
import re
from glob import glob
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Define the watch path and destination path
watch_path = "/media/ChannelsDVR/TV/"
dest_path = "/media/Plex/TV Shows/"

# Dictionary of shows
shows = {
    "Big Brother": "Big Brother (2000)",
    "The Challenge": "The Challenge - USA (2022)"
}

# Function to process a new file
def process_new_file(file_path):
    filename = os.path.basename(file_path)
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
                    os.link(file_path, f"{new_location}{filename}")
                    print("Success!")
                    break
        except Exception as e:
            print(f"Error: {e}")

# Define a custom event handler
class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        # React to file creation
        if not event.is_directory:
            process_new_file(event.src_path)

if __name__ == "__main__":
    # Set up the observer to watch the directory
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, path=watch_path, recursive=True)

    # Start the observer
    observer.start()

    print(f"Monitoring '{watch_path}' for new files...")

    try:
        observer.join()
    except KeyboardInterrupt:
        observer.stop()
