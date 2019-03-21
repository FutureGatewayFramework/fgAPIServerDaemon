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

from fgapiserverdaemon_config import fg_config
from fgapiserverdaemon_db import fgapisrv_db
import os
import sys
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
__update__ = '2019-03-21 20:33:35'

# Logger object
logger = None


class fgAPIServerDaemonEI(threading.Thread):
    def __init__(self, thread_manager):
        global logger
        threading.Thread.__init__(self)

        logger = logging.getLogger(__name__)

        # Store thread_manager
        self.thread_manager = thread_manager

    def run(self):
        global logger
        global fgapisrv_db
        logger.debug("Starting fgAPIServerDaemon EI")
        logger.debug("Available thread slots: %s"
                     % self.thread_manager.get_slots())
