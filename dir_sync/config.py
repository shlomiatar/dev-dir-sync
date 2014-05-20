import os


class Config(object):
    """
    Configuration class
    """

    DEFAULT_SYNC_CMD = 'vagrant rsync'
    DEFAULT_DELAY = 1.5
    DEFAULT_FILTER_REGEXP = ''
    DEFAULT_SPECIFIC_FILES_THRESHOLD = 50

    def __init__(self):
        """
        Setup the defaults
        """

        # Set the sync command
        self.sync_cmd = self.DEFAULT_SYNC_CMD

        # Batch changes delay (in secs)
        self.delay = self.DEFAULT_DELAY

        # Extensions filtering
        self.filter_regexp = self.DEFAULT_FILTER_REGEXP

        # Maximum number of files to sync individually
        self.specific_files_threshold = self.DEFAULT_SPECIFIC_FILES_THRESHOLD

        # Watch directory
        self.directory = os.getcwd()