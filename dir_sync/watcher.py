import os
import subprocess
import threading
import time
from watchdog.observers import Observer
from change_handler import ChangeHandler

DEFAULT_EXCLUDES = ['.vagrant', '.git', '.pyc', '.tmp']
import logging

class Watcher(object):
    """
    Wathcer
    =======

    Watch and sync files

    """

    def __init__(self, config):
        """
        Initialize the watcher, use the config passed from main
        """
        self.config = config

        # List of pending files
        self.pending_files = set()

        self.sync_timer = None

        # Setup our watchdog observer
        observer = Observer()
        observer.schedule(ChangeHandler(self.on_file_changed), path=config.directory, recursive=True)
        observer.start()

        logging.info("Starting change tracker, cmd: {}, dir: {}, delay: {}".format(config.sync_cmd,
                                                                                   config.directory,
                                                                                   config.delay))
        try:
            while True:
                time.sleep(0.5)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

    def on_file_changed(self, path, change_type):
        """
        File change handler


        """

        # Notify changes
        logging.info("[{}] {}".format(change_type, path))

        # If we already have a pending sync promise, cancel it
        if self.sync_timer and self.sync_timer.is_alive():
            self.sync_timer.cancel()

        # Add to the pending files
        self.pending_files.add(path)

        # Queue the sync
        self.sync_timer = threading.Timer(self.config.delay, self.sync)
        # Start the sync timer
        self.sync_timer.start()


    def sync(self):
        """
        The actual sync command
        """

        # Clear pending files
        files = self.pending_files.copy()
        self.pending_files = set()

        cmd = self.config.sync_cmd

        # If the number of files to sync is less than the threshold,
        # use specific files
        if len(files) < self.config.specific_files_threshold:
            cmd += self._generate_includes(files)

        # Add exclusion patterns
        cmd += self._generate_excludes()

        logging.info("[sync] ({} files) {}".format(len(files), cmd))

        # Execute the command
        subprocess.call(cmd, shell=True)

    def _generate_includes(self, files):
        """
        Convert a list of files to a list of --include= arguments
        """

        args = ["--include '{}'".format(self._normalize_path(f)) for f in files]

        # Add a global exclude
        args.append("--exclude '*'")

        return " " + " ".join(args)

    def _generate_excludes(self):
        """
        Generate --exclude arguments
        """

        items = DEFAULT_EXCLUDES + [f.strip() for f in self.config.filter_regexp.split(',')]

        excludes = ["--exclude '{}'".format(f) for f in items if f]

        return " " + " ".join(excludes)

    def _normalize_path(self, path):
        """
        Convert absolute path to relative based on the working directory
        """
        return os.path.relpath(path, self.config.directory)



