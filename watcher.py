import os
import time
import psutil
import subprocess
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# CONSTANTS
FILE_TO_LOAD: str = "main.py"
SUPPORTED_SUBDIRECTORIES: list[str] = ["events", "components"]

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

        except KeyboardInterrupt:
            self.observer.stop()
            os.system("clear")
            print("Stopped")

        self.observer.join()

class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event: FileSystemEventHandler | list[str]) -> None:
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
                
                # Remove the root dir and get the path
                path = event.src_path.replace(os.getcwd() + "/", "")

                # Check if "/" is in the path
                if "/" in path:
                    sdir = path.split("/")[0]
                    # Check if the path is in supported subdirectories
                    if not any([True for i in SUPPORTED_SUBDIRECTORIES if i in sdir]):
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