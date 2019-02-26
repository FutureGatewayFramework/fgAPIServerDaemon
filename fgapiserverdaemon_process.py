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
from fgapiserverdaemon_thread_manager\
    import ThreadManager
import os
import sys
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
__update__ = '2019-02-26 13:36:13'

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


class fgAPIServerDaemonProcess():
    """
    fgAPIServerDaemon process class
    """
    max_threads = 0

    def __init__(self, max_threads):
        self.max_threads = max_threads
        self.process_pid = os.getpid()

    def run_processes(self):
        """
            fgAPIServerDaemonProcess
        """
        global fg_config

        logging.debug(
            "Initializing fgAPIServerDaemon process, with PID: %s"
            % self.process_pid)
        logging.debug("Starting daemon processes")

        # Scope of the process is to start the basic threads and use available
        # free slots (max_threads-2) to start ExecutorInterfaces instances
        # Basic threads are two:
        #   - The task extraction polling
        #   - The check task polling

        # Initialize the ThreadManager with available slots
        thread_manager = ThreadManager(self.max_threads - 2)

        # Starting basic threads - Task extractor
        # task_extractor=fgAPIServerDaemonProcessTaskExtractor(thread_manager)
        # task_extractor.start()
        # task_extractor.join()

        # Starting basic threads - Task checker
        # task_checker = fgAPIServerDaemonProcessTaskChecker(thread_manager)
        # task_checker.start()
        # task_checker.join()

        lock_file = '%s/%s%s' % (fg_config['lock_dir'],
                                 self.process_pid,
                                 fg_config['process_lock_file'])
        try:
            t_file = open(lock_file, 'w')
            t_file.close()
            logging.debug("Process with lock file: '%s', created"
                          % lock_file)
            logging.debug("Entering loop for process: '%s'"
                          % self.process_pid)
            while os.path.isfile(lock_file):
                print("loop breath")
                logging.debug("Process loop, sleeping for %s seconds"
                              % fg_config['process_loop_delay'])
                time.sleep(fg_config['process_loop_delay'])
        except IOError:
            logging.error("Unable to create lock file: '%s'" % lock_file)

        # Process run finished
        logging.debug("Process with lock file: '%s', terminated" % lock_file)
