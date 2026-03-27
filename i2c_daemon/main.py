#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""File System Monitoring Utility"""

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from watchdog.observers.polling import PollingObserver

import signal
import logging

logger = logging.getLogger(__name__)

class MyEventHandler(FileSystemEventHandler):
    def catch_all_handler(self, event, *args):
        # This would be the event we'd want to try to get the fd for the `src_path`
        path = event.src_path

        logger.info(event)
        if args:
            logger.info(args)

    def on_moved(self, event):
        self.catch_all_handler(event)

    def on_created(self, event):
        # TODO reset the offset of the path in the map
        self.catch_all_handler(event)

    def on_deleted(self, event):
        self.catch_all_handler(event)

    def on_modified(self, event):
        self.catch_all_handler(event)


def monitor_file_system(args, directory='/tmp', recursive=True):
    # TODO Add a way to have a list of files to ignore
    event_handler = MyEventHandler()
    do_polling = args.subcommand == 'poll'

    observer = PollingObserver(args.polling_interval) if do_polling else Observer()
    observer_method = 'by Polling every {} seconds'.format(args.polling_interval) if do_polling else 'via Inotify'
    # TODO: Allow for multiple files to be monitored
    logger.info(observer.schedule(event_handler, directory, recursive=recursive))

    logger.info('Starting to observe: {!r} {}...'.format(directory, observer_method))
    observer.start()
    try:
        while True:
            signal.pause()
    finally:
        logger.error('We are stopping our watch!')
        observer.stop()
        logger.info('We are going to join and finish up!')
        observer.join()
        logger.info('Finished observation session.')
