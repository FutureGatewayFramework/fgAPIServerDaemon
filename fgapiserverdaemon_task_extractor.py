#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

import logging.config
import time
import logging.config
import threading
from fgapiserverdaemon_config import fg_config
from fgapiserverdaemon_db_process import fgapisrv_db_process

"""
  FutureGateway APIServerDaemon task extractor
"""

__author__ = 'Riccardo Bruno'
__copyright__ = '2019'
__license__ = 'Apache'
__version__ = 'v0.0.0'
__maintainer__ = 'Riccardo Bruno'
__email__ = 'riccardo.bruno@ct.infn.it'
__status__ = 'devel'
__update__ = '2019-05-03 17:04:36'

# Logging
logger = logging.getLogger(__name__)


class APIServerDaemonProcessTaskExtractor(threading.Thread):

    loop_state = True
    process_id = None
    commands_queue = None
    queue_lock = None

    def __init__(self, process_id, commands_queue):
        threading.Thread.__init__(self)
        self.process_id = process_id
        self.commands_queue = commands_queue
        self.queue_lock = threading.Lock()

    def log_str(self, string):
        return "%s: %s" % (self.process_id, string)

    def run(self):
        # Database object must be present
        if fgapisrv_db_process is None:
            logging.error(self.log_str(
                "Database object not present, unable to start"
                "APIServerDaemon task extractor thread"))
            return

        # Database object has to operate correctly
        if not fgapisrv_db_process.test():
            logging.error(self.log_str(
                "fgAPIServerDaemon task extractor could not connect to the "
                "database"))
            return

        # Task extractor main loop
        logging.debug(self.log_str(
            "Starting fgAPIServerDaemon task extractor"))
        while self.loop_state is True:
            self.extract_commands()
            logging.debug(self.log_str(
                "Task extractor loop, sleeping 10 seconds ..."))
            time.sleep(10)
        logging.debug(self.log_str(
            "Terminated fgAPIServerDaemon task extractor"))

    def end(self):
        self.loop_state = False

    def extract_commands(self):
        commands = fgapisrv_db_process.get_queued_commands(
            fg_config['extract_loop_records'])
        for command in commands:
            self.queue_lock.acquire()
            self.commands_queue.put(command)
            self.queue_lock.release()
