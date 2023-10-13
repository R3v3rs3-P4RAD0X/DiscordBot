import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import threading
import psutil
from typing import Union, List

# CONSTANTS
FILE_TO_LOAD: str = "main.py"
SUPPORTED_SUBDIRECTORIES: List[str] = ["events", "components"]

class Watcher:
    # Define the directory to watch
    DIRECTORY_TO_WATCH: str = os.getcwd()

    def __init__(self):
        self.observer: Observer = Observer()

    def run(self):
        event_handler: Handler = Handler()
        # Schedule the event handler for the directory to watch (including subdirectories)
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()

        try:
            while True:
                time.sleep(5)
        except Exception as _:
            self.observer.stop()
            print("Error")

        self.observer.join()

class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event: Union[FileSystemEventHandler, List[str]]) -> None:
        # If the event is a directory, skip
        if event.is_directory:
            return None

        # If the event is modifying a file, check if it is a python file
        if event.event_type == "modified":
            # Check the extension
            if event.src_path.endswith(".py"):
                # Check if the file is watcher.py
                if event.src_path.endswith("watcher.py"):
                    return None
                
                # Check if the file is in a supported subdirectory
                if len(SUPPORTED_SUBDIRECTORIES) > 0:
                    if not any([True for i in SUPPORTED_SUBDIRECTORIES if i in event.src_path]):
                        return None
              
                    # Clear the terminal
                    os.system("clear")

                    # Print file change was detected, reloading main.py
                    print("File change detected: {}\nReloading: {}".format(event.src_path, FILE_TO_LOAD))

                    # Kill the main.py process
                    for proc in psutil.process_iter(attrs=['name', 'cmdline']):
                        # Check if the process is python and if the process is main.py
                        if proc.info['name'] == "python" and FILE_TO_LOAD in " ".join(proc.info['cmdline']):
                            # Kill the process
                            proc.kill()

                    # Call the function to start a new threaded process of FILE_TO_LOAD
                    threading.Thread(target=subprocess.call, args=(["python", os.path.join(os.getcwd(), FILE_TO_LOAD)],)).start()

# Run the watcher
if __name__ == "__main__":
    # Create the watcher and run it
    w = Watcher()
    w.run()