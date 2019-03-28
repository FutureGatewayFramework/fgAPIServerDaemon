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

import logging.config
import time
import logging.config
import threading
from fgapiserverdaemon_command import APIServerCommand

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
__update__ = '2019-03-28 18:58:57'

# Logging
logger = logging.getLogger(__name__)

# fgAPIServerDaemon configuration
fg_config = None

# FutureGateway database object
fgapisrv_db = None


def set_config(config_obj):
    """
    Receive fgAPIServerDaemon configuration settings
    :param config_obj: Configuration settings object
    """
    global fg_config
    fg_config = config_obj
    logging.debug("Receiving configuration object")


def set_db(db_obj):
    """
    Receive fgAPIServerDaemon database object
    :param db_obj: database object
    """
    global fgapisrv_db
    fgapisrv_db = db_obj
    logging.debug("Receiving database object")


class APIServerDaemonProcessTaskChecker(threading.Thread):

    loop_state = True
    process_id = None
    commands_queue = None

    def __init__(self, process_id, commands_queue):
        threading.Thread.__init__(self)
        self.process_id = process_id
        self.commands_queue = commands_queue

    def log_str(self, string):
        return "%s: %s" % (self.process_id, string)

    def run(self):
        # Database object must be present
        if fgapisrv_db is None:
            logging.error(self.log_str(
                "Database object not present, unable to start"
                "APIServerDaemon task checker thread"))
            return

        # Database object has to operate correctly
        if not fgapisrv_db.test():
            logging.error(self.log_str(
                "fgAPIServerDaemon task checker could not connect to the "
                "database"))
            return

        # Task checker main loop
        logging.debug(self.log_str(
            "Starting fgAPIServerDaemon task checker"))
        while self.loop_state is True:
            logging.debug(self.log_str(
                "Task extractor loop, sleepping 15 seconds ..."))
            time.sleep(15)
        logging.debug(self.log_str(
            "Terminated fgAPIServerDaemon task checker"))

    def end(self):
        self.loop_state = False
