#!/usr/local/bin/python

import os
import re
import time
from glob import glob
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from concurrent.futures import ThreadPoolExecutor

# Define the watch path and destination path
watch_path = "/media/ChannelsDVR/TV/"
dest_path = "/media/Plex/TV Shows/"

# Dictionary of shows
shows = {
    "Big Brother": "Big Brother (2000)",
    "The Challenge": "The Challenge - USA (2022)",
    "On Patrol Live": "On Patrol - Live (2022)"
}


def pprint(text):
    print(f"{datetime.now().isoformat()}: ", end="")
    print(text)


# Function to check if a file is being actively written
def is_file_being_written(file_path, max_duration_seconds=14400):
    initial_size = os.path.getsize(file_path)
    start_time = time.time()  # Get the start time
    # Check file size repeatedly until max_duration_seconds is reached
    while time.time() - start_time <= max_duration_seconds:
        time.sleep(20)  # Sleep before rechecking
        final_size = os.path.getsize(file_path)
        if initial_size == final_size:
            return False  # File size is not changing; not being actively written
        # Update initial_size if the file size changed
        initial_size = final_size
    return True  # Max duration reached; file is being actively written


# Function to process a new file
def process_new_file(file_path):
    filename = os.path.basename(file_path)
    pprint(f"New file detected: {filename}. Waiting for recording to end.")
    if filename.endswith((".ts", "mp4", "mkv", "mpg")):
        try:
            for show, show_dest in shows.items():
                if show in filename:
                    parts = re.match(r".*(S(\d+)E\d+).*", filename)
                    season_number = parts.group(2).lstrip("0")
                    new_location = f"{dest_path}/{show_dest}/Season {season_number}/"

                    # Check if the file is being actively written
                    if is_file_being_written(file_path, max_duration_seconds=14400):
                        pprint(f"File {filename} is still being written after three hours; skipping...")
                        return

                    if any(parts.group(1) in existing_file for existing_file in glob(f"{new_location}*")):
                        return

                    pprint(f"Creating hard link for {filename}")
                    os.makedirs(new_location, exist_ok=True, mode=0o755)
                    os.link(file_path, f"{new_location}{filename}")
                    pprint(f"Success: '{filename}'!")
                    return
        except Exception as e:
            pprint(f"Error: {e}")


# Define a custom event handler
class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        # React to file creation
        if not event.is_directory:
            # Process each new file in parallel using ThreadPoolExecutor
            with ThreadPoolExecutor(max_workers=8) as executor:
                executor.submit(process_new_file, event.src_path)


if __name__ == "__main__":
    # Set up the observer to watch the directory
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, path=watch_path, recursive=True)

    # Start the observer
    observer.start()

    pprint(f"Monitoring {watch_path} for new files...")

    try:
        observer.join()
    except KeyboardInterrupt:
        observer.stop()
