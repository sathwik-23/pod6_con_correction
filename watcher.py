import time
from pathlib import Path
import traceback

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from main import ConfigCorrectionAgent


RESOLUTION_FOLDER = Path("Incidents/Resolution")


class ResolutionWatcher(FileSystemEventHandler):

    def __init__(self):
        super().__init__()
        self.agent = ConfigCorrectionAgent()

    def on_created(self, event):

        if event.is_directory:
            return

        file_path = Path(event.src_path)

        if file_path.suffix.lower() != ".json":
            return

        print(
            f"\nNew resolution file detected: "
            f"{file_path.name}"
        )

        # Wait for the file to finish copying
        time.sleep(1)

        try:
            self.agent.process(
                str(file_path),
                use_github=True
            )

        except Exception as error:
             print(f"Processing failed: {type(error).__name__}: {error}")
             traceback.print_exc()


def start_watcher():

    RESOLUTION_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    observer = Observer()
    event_handler = ResolutionWatcher()

    observer.schedule(
        event_handler,
        str(RESOLUTION_FOLDER),
        recursive=False
    )

    observer.start()

    print("Config Correction Watcher started.")
    print(
        f"Watching: "
        f"{RESOLUTION_FOLDER.resolve()}"
    )
    print("Add a new JSON file to test.")
    print("Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nStopping watcher...")

    finally:
        observer.stop()
        observer.join()


if __name__ == "__main__":
    start_watcher()