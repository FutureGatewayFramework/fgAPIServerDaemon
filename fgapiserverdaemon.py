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

from fgapiserverdaemon_process import\
    APIServerDaemonProcess
from fgapiserverdaemon_config import fg_config
from fgapiserverdaemon_db import fgapisrv_db
from fgapiserverdaemon_tools import\
    check_db_ver,\
    check_db_reg
from multiprocessing import Process
import os
import logging
import logging.config

"""
  FutureGateway APIServerDaemon
"""
__author__ = 'Riccardo Bruno'
__copyright__ = '2019'
__license__ = 'Apache'
__version__ = 'v0.0.0'
__maintainer__ = 'Riccardo Bruno'
__email__ = 'riccardo.bruno@ct.infn.it'
__status__ = 'devel'
__update__ = '2019-03-28 18:58:57'

# Create root logger object and configure logger
logging.config.fileConfig(fg_config['fgasd_log_conf'])

#
# The fgAPIServerDaemon starts here
#

# Get database object and check the DB
check_db_ver()

# Server registration and configuration from fgdb
check_db_reg(fg_config)


def main():
    """
    Main code for fgAPIServerDaemon
    :return: None
    """
    logging.debug("fgAPIServerDaemon starts ...")

    # Create or check lock directory
    logging.debug("Checking lock directory: '%s'" % fg_config['lock_dir'])
    if (os.path.isdir(fg_config['lock_dir'])):
        logging.debug("Lock dir: '%s' already exists" % fg_config['lock_dir'])
    else:
        logging.warn("Lock dir: '%s' does not exists, creating it"
                     % fg_config['lock_dir'])
        try:
            os.makedirs(fg_config['lock_dir'])
            logging.warn("Lock dir: '%s', successfuly created"
                         % fg_config['lock_dir'])
        except OSError:
            logging.error("Unable to create process dir: '%s'"
                          % fg_config['lock_dir'])
            exit(1)

    # Inform user about server activity
    logging.info("fgAPIServerDaemon is running ...")
    processes = []
    for i in range(0, fg_config['processes']):
        logging.debug(
            "Starting process (%s/%s)" % (1 + i, fg_config['processes']))
        process_object = APIServerDaemonProcess(i)
        p = Process(target=process_object.run_processes,
                    args=())
        processes.append(p)
    for p in processes:
        p.start()
    for p in processes:
        p.join()

    # fgAPIServerDaemon terminated
    logging.info("fgAPIServerDaemon terminated ...")


# Main code for fgAPIServerDaemon
if __name__ == "__main__":
    main()
