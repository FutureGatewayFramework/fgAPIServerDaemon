#!/usr/bin/env python
# Copyright (c) 2015:
# Istituto Nazionale di Fisica Nucleare (INFN), Italy
#
# See http://www.infn.it  for details on the copyrigh holder
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from fgapiserverdaemon_task_checker\
    import fgAPIServerDaemonProcessTaskChecker
from fgapiserverdaemon_task_extractor\
    import fgAPIServerDaemonProcessTaskExtractor
import os
import time
import logging

"""
  FutureGateway APIServerDaemonProcess
"""

__author__ = 'Riccardo Bruno'
__copyright__ = '2019'
__license__ = 'Apache'
__version__ = 'v0.0.0'
__maintainer__ = 'Riccardo Bruno'
__email__ = 'riccardo.bruno@ct.infn.it'
__status__ = 'devel'
__update__ = '2019-02-26 19:33:51'

# Logging
logger = logging.getLogger(__name__)

# fgAPIServerDaemon configuration
fg_config = None

# FutureGateway database object
fgapisrv_db = None


def set_config(config_obj):
    """
    Receive fgAPIServerDaemon configuration settings
    :param config_obj:
    :return:
    """
    global fg_config
    fg_config = config_obj
    logging.debug("Receiving configuration object")


def set_db(db_obj):
    """
    Receive fgAPIServerDaemon database object
    :param database object:
    :return:
    """
    global fgapisrv_db
    fgapisrv_db = db_obj
    logging.debug("Receiving database object")


class fgAPIServerDaemonProcess():
    """
    fgAPIServerDaemon process class
    """
    process_pid = None
    max_threads = 0

    def __init__(self, max_threads):
        self.max_threads = max_threads
        self.process_pid = os.getpid()

    def log_str(self, string):
        return "%s: %s" % (self.process_pid, string)

    def run_processes(self):
        """
            fgAPIServerDaemonProcess
        """
        global fg_config

        logging.debug(self.log_str(
            "Initializing fgAPIServerDaemon process, with PID: %s"
            % self.process_pid))

        # At least 3 thread slots must be available for DaemonProcess
        if(self.max_threads < 3):
            logging.error(self.log_str(
                "Max threads must be greather than: 3,"
                "received: '%s', instead" % self.max_threads))
            return

        # Scope of the process is to start the basic threads and use available
        # free slots (max_threads-2) to start ExecutorInterfaces instances
        # Basic threads are two:
        #   - The task extraction polling
        #   - The task checker polling

        lock_file = '%s/%s%s' % (fg_config['lock_dir'],
                                 self.process_pid,
                                 fg_config['process_lock_file'])
        try:
            t_file = open(lock_file, 'w')
            t_file.close()
            logging.debug(self.log_str(
                "Process with lock file: '%s', created" % lock_file))
            # Starting task_extrator
            task_extractor = \
                fgAPIServerDaemonProcessTaskExtractor(self.process_pid)
            task_extractor.start()

            # Starting task_checker
            task_checker = \
                fgAPIServerDaemonProcessTaskChecker(self.process_pid)
            task_checker.start()

            # Polling loop
            logging.debug(self.log_str(
                "Entering loop for process: '%s'" % self.process_pid))
            while os.path.isfile(lock_file):
                logging.debug(self.log_str(
                    "Process loop, sleeping for %s seconds"
                    % fg_config['process_loop_delay']))
                time.sleep(fg_config['process_loop_delay'])

            # Process lock file has been deleted, active threads must be
            # stopped before leaving, disabling polling loops
            task_extractor.end()
            task_checker.end()
            task_extractor.join()
            task_checker.join()
        except IOError:
            logging.error(self.log_str(
                "Unable to create lock file: '%s'" % lock_file))

        # Process run finished
        logging.debug(self.log_str(
            "Process with lock file: '%s', terminated" % lock_file))
