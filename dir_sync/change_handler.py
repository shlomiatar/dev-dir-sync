from watchdog.events import FileSystemEventHandler


class ChangeType(object):
    Modified = 'modified'
    Removed = 'removed'
    Created = 'created'


class ChangeHandler(FileSystemEventHandler):
    """
    Simple class to handle file system changes and call a callback
    """

    def __init__(self, callback):
        """
        Setup the handler and store the callback
        """

        self.callback = callback


    def on_modified(self, event):
        # Skip directory events
        if event.is_directory:
            return

        # Call the callback
        self.callback(event.src_path, ChangeType.Modified)

    def on_create(self, event):
        # Skip directory events
        if event.is_directory:
            return

        # Call the callback
        self.callback(event.src_path, ChangeType.Created)

    def on_deleted(self, event):
        # Skip directory events
        if event.is_directory:
            return

        # Mac issue that we discovered on 31/12/13 where
        # modification caused Watchdog to send "deleted" events
        # This is our fix for it
        self.callback(event.src_path, ChangeType.Modified)