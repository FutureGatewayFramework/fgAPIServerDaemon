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
from fgapiserverdaemon_config\
    import FGApiServerConfig
from fgapiserverdaemon_tools\
    import get_fgapiserver_db
import os
import sys
import logging.config
import threading

"""
  FutureGateway APIServerDaemon thread manager  class
"""

__author__ = 'Riccardo Bruno'
__copyright__ = '2019'
__license__ = 'Apache'
__version__ = 'v0.0.0'
__maintainer__ = 'Riccardo Bruno'
__email__ = 'riccardo.bruno@ct.infn.it'
__status__ = 'devel'
__update__ = '2019-02-21 21:40:19'

# Logger object
logger = None

# FutureGateway database object
fgapisrv_db = get_fgapiserver_db()

#
# Thread management class
#


class ThreadManager:
    num_slots = 0

    def __init__(self, num_slots):
        global logger
        # setup path
        fgapirundir = os.path.dirname(os.path.abspath(__file__)) + '/'
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

        # fgapiserver configuration file
        fgapiserver_config_file = fgapirundir + 'fgapiserverdaemon.conf'

        # Load configuration
        fg_config = FGApiServerConfig(fgapiserver_config_file)

        # Prepare logger object
        logging.config.fileConfig(fg_config['logcfg'])
        logger = logging.getLogger(__name__)

        # Store the number of available slots
        self.num_slots = num_slots

    def get_slots(self):
        return self.num_slots
