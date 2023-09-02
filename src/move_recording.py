#!/usr/bin/env python3

import os
import re
import json
import time
from glob import glob
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from concurrent.futures import ThreadPoolExecutor


def pprint(text):
    print(f"{datetime.now().isoformat()}: ", end="")
    print(text)


class RecordingMover:
    def __init__(self):
        # Define the variables that are required to run
        self.watch_path = os.environ.get('watch_path')
        self.dest_path = os.environ.get('dest_path')
        self.max_write_time = os.environ.get('max_write_time', 14400)

        # Do a little health check to make sure we have the variables required to run
        if not self.watch_path or not self.dest_path:
            print("All variables (watch_path, dest_path) must be defined as environmental variables. Quitting.")
            exit(1)

    # Function to check if a file is being actively written
    @staticmethod
    def _is_file_being_written(file_path, max_duration_seconds=14400):
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
    def process_new_file(self, file_path):
        filename = os.path.basename(file_path)
        with open("mappings.json") as json_data:
            mappings = json.load(json_data)
        if filename.endswith((".ts", "mp4", "mkv", "mpg")):
            try:
                for recording, recording_dest in mappings.items():
                    if recording in filename:
                        pprint(f"New file detected: '{filename}'. Waiting for recording to end.")
                        parts = re.match(r".*(S(\d+)E\d+).*", filename)
                        season_number = parts.group(2).lstrip("0")
                        new_location = f"{self.dest_path}/{recording_dest}/Season {season_number}/"

                        # Check if the file is being actively written
                        if self._is_file_being_written(file_path, max_duration_seconds=self.max_write_time):
                            pprint(f"File '{filename}' is still being written after three hours; skipping...")
                            return

                        if any(parts.group(1) in existing_file for existing_file in glob(f"{new_location}*")):
                            return

                        pprint(f"Creating hard link for '{filename}'")
                        os.makedirs(new_location, exist_ok=True, mode=0o755)
                        os.link(file_path, f"{new_location}{filename}")
                        pprint(f"Success: '{filename}'!")
                        return
                pprint(f"Skipping recording with no match in 'mappings.json': '{filename}'")
            except Exception as e:
                pprint(f"Error: {e}")


# Define a custom event handler
class FileHandler(FileSystemEventHandler):
    def __init__(self, rec_mover):
        self.recording_mover = rec_mover

    def on_created(self, event):
        # React to file creation
        if not event.is_directory:
            # Process each new file in parallel using ThreadPoolExecutor
            with ThreadPoolExecutor(max_workers=8) as executor:
                executor.submit(self.recording_mover.process_new_file, event.src_path)


if __name__ == "__main__":
    # Set up the observer to watch the directory
    recording_mover = RecordingMover()
    event_handler = FileHandler(recording_mover)
    observer = Observer()
    observer.schedule(event_handler, path=recording_mover.watch_path, recursive=True)

    # Start the observer
    observer.start()

    pprint(f"Started. Monitoring '{recording_mover.watch_path}' for new files...")

    try:
        observer.join()
    except KeyboardInterrupt:
        observer.stop()
