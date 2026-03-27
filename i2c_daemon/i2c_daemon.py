#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Entry Point for File System Monitoring Utility

This utility monitors file system events via Inotify or Polling.
"""
import argparse
import logging

from i2c_daemon.main import monitor_file_system

def main():
    parser = argparse.ArgumentParser(
        description='File System Monitoring Utility',
        epilog="""This utility monitors file system events via Inotify or Polling.""",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # Log file location
    parser.add_argument('--log-file', '-l', action='store', help='Write logs to log_file. Default: [%(default)s]', default='/tmp/tmpdirwatch.log')
    subparsers = parser.add_subparsers(dest='subcommand')

    # Do polling or inotify; for polling, how many seconds?
    watcher_type_parser = subparsers.add_parser('poll', help='Use polling method to monitor file system events')
    watcher_type_parser.add_argument('--polling-interval', '-p', type=int, help='Number of seconds to wait between polling events', default=5)

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, datefmt='%m/%d/%Y %H:%M:%S', format='%(asctime)s [%(levelname)s] %(message)s', filename=args.log_file)

    monitor_file_system(args)

if __name__ == '__main__':
    main()
