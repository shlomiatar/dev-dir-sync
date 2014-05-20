###
# DevDirSync
# ==========
#
# A utility to watch and sync development folders
#
###


import argparse
import os
from config import Config
from watcher import Watcher

import logging

logging.getLogger().setLevel(logging.DEBUG)

def main():
    """
    Start the app
    """

    config = load_config()

    # Start the watcher
    Watcher(config)


def load_config():
    """
    Load configuration
    """

    parser = argparse.ArgumentParser(description='Configure the change tracking app.')

    parser.add_argument('--sync_cmd', type=str, action='store', nargs='?',
                        help='The command line to sync once there is change', default=Config.DEFAULT_SYNC_CMD)

    parser.add_argument('--delay', type=float, action='store', nargs='?',
                        help='Number of seconds to batch for sync', default=Config.DEFAULT_DELAY)

    parser.add_argument('--filter_regexp', type=str, action='store', nargs='?',
                        help='Regexp for filtering files from sync', default=Config.DEFAULT_FILTER_REGEXP)

    parser.add_argument('--watch_dir', type=str, action='store', nargs='?',
                        help='Path of the dir to watch', default=os.getcwd())

    args = parser.parse_args()

    # New config
    conf = Config()

    # update conf
    conf.delay = args.delay
    conf.sync_cmd = args.sync_cmd
    conf.filter_regexp = args.filter_regexp
    conf.directory = args.watch_dir

    # return
    return conf


if __name__ == '__main__':
    main()


