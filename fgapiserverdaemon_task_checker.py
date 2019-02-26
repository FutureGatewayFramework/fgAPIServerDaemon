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
__update__ = '2019-02-26 19:33:51'

# Logging
logger = logging.getLogger(__name__)

# fgAPIServerDaemon configuration
fg_config = None

# FutureGateway database object
fgapisrv_db = None


class fgAPIServerDaemonProcessTaskChecker(threading.Thread):

    loop_state = True
    process_id = None

    def __init__(self, process_id):
        threading.Thread.__init__(self)
        self.process_id = process_id

    def log_str(self, string):
        return "%s: %s" % (self.process_id, string)

    def run(self):
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
