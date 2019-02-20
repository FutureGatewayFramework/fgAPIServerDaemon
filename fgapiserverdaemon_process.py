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

from fgapiserverdaemon_config\
    import FGApiServerConfig
from fgapiserverdaemon_tools\
    import get_fgapiserver_db
from fgapiserverdaemon_task_checker\
    import fgAPIServerDaemonProcessTaskChecker
from fgapiserverdaemon_task_extractor\
    import fgAPIServerDaemonProcessTaskExtractor
from fgapiserverdaemon_thread_manager\
    import ThreadManager
import os
import sys
import logging.config

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
__update__ = '2019-02-20 23:01:48'

# Logger object
logger = None

# Available EI slots
ei_slots = 0

# FutureGateway database object
fgapisrv_db = get_fgapiserver_db()

# Logging
def init_config():
    global logger
    # setup path
    fgapirundir = os.path.dirname(os.path.abspath(__file__)) + '/'
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    # fgapiserver configuration file
    fgapiserver_config_file = fgapirundir + 'fgapiserverdaemon.conf'

    # Load configuration
    fg_config = FGApiServerConfig(fgapiserver_config_file)

    # Prepare logger object
    logging.config.fileConfig(fg_config['fgapiserverdaemon_logcfg'])
    logger = logging.getLogger(__name__)
    logger.debug("fgAPIServerDaemonProcess is starting ...")

#
# fgAPIServerDaemonProcess
#
def fgAPIServerDaemonProcess(max_threads):
    global logger
    global ei_slots
    init_config()
    logger.debug("Called fgAPIServerDaemonProcess")
    logger.debug("Maximum number of threads: %s" % max_threads)
    # Scope of the process is to start the basic threads and use available
    # free slots (max_threads-2) to start ExecutorInterfaces instances
    # Basic threads are two:
    #   - The task extraction polling
    #   - The check task polling
    ei_slots = max_threads - 2
    logger.debug("Available EI slots: %s" % ei_slots)
    # Initialize the ThreadManager with available slots
    thread_manager = ThreadManager(ei_slots)

    # Starting basic threads - Task extractor
    task_extractor = fgAPIServerDaemonProcessTaskExtractor(thread_manager)
    task_extractor.start()
    task_extractor.join()

    # Starting basic threads - Task checker
    task_checker = fgAPIServerDaemonProcessTaskChecker(thread_manager)
    task_checker.start()
    task_checker.join()

