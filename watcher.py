import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import threading
import psutil


class Watcher:
    DIRECTORY_TO_WATCH = os.getcwd()

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler,
                               self.DIRECTORY_TO_WATCH,
                               recursive=False)
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
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == "modified":
            if event.src_path.endswith(
                    ".py") and not event.src_path.endswith("watcher.py"):
                os.system("clear")
                print("Python file changed: {}".format(event.src_path))
                for proc in psutil.process_iter():
                    if proc.name() == "python" and "main.py" in " ".join(
                            proc.cmdline()):
                        proc.kill()
                threading.Thread(
                    target=subprocess.call,
                    args=(["python", "/root/Projects/DiscordBot/main.py"], ),
                ).start()


if __name__ == "__main__":
    w = Watcher()
    w.run()
