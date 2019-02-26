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

from fgapiserverdaemon_db import\
    set_config as set_config_db
from fgapiserverdaemon_config import\
    FGApiServerConfig
from fgapiserverdaemon_process import\
    set_config as set_config_process,\
    fgAPIServerDaemonProcess
from fgapiserverdaemon_tools import\
    set_config as set_config_tools,\
    get_fgapiserver_db,\
    check_db_ver,\
    check_db_reg
from multiprocessing import Process
import os
import sys
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
__update__ = '2019-02-26 13:36:13'

# Retrieve filename
file_name, file_ext = os.path.basename(__file__).split('.')

# fgAPIServerDeemon configuration file
config_file = file_name + '.yaml'

# fgAPIServerDaemon log config file
log_config_file = file_name + '_log.conf'

# Retrieve execution dir and place it to path
run_dir = os.path.dirname(os.path.abspath(__file__)) + '/'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Create root logger object and configure logger
logging.config.fileConfig(run_dir + log_config_file)

# Load configuration
fg_config = FGApiServerConfig(config_file)

# Spread configuration across components
set_config_db(fg_config)
set_config_tools(fg_config)
set_config_process(fg_config)

# FutureGateway database object
fgapisrv_db = get_fgapiserver_db()

# Spread db object across components
# set_config_tools(fgapisrv_db)
# set_db_process(fgapisrv_db)


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
        process_object = fgAPIServerDaemonProcess(fg_config['maxthreads'])
        p = Process(target=process_object.run_processes,
                    args=())
        processes.append(p)
    for p in processes:
        p.start()
    for i in processes:
        p.join()

    # fgAPIServerDaemon terminated
    logging.info("fgAPIServerDaemon terminated ...")


# Main code for fgAPIServerDaemon
if __name__ == "__main__":
    main()
