import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from machine_learning.object_recognition import detector_controller
from machine_learning.object_recognition.detector_controller import DetectorController


class DirectoryObserver:

    def __init__(self, directory_path):
        patterns = ["*"]
        ignore_patterns = None
        ignore_directories = False
        case_sensitive = True
        my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
        my_event_handler.on_created = self.on_created

        path = directory_path  # "C:\\Users\\ionmi\\Downloads\\test isensiot videos"
        go_recursively = True
        my_observer = Observer()
        my_observer.schedule(my_event_handler, path, recursive=go_recursively)

        detector_controller = DetectorController

        my_observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            my_observer.stop()
            my_observer.join()

    def on_created(event):
        print(f"file {event.src_path} created. Starting to analyze")
        print(detector_controller.analyze_video(str(event.src_path)))
