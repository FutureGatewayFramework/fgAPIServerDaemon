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
from flask import Flask
from flask import request
from fgapiserverdaemon_db import\
    set_config as set_config_db
from fgapiserverdaemon_config import\
    FGApiServerConfig
from fgapiserverdaemon_config import\
    FGApiServerConfig
from fgapiserverdaemon_tools import\
    set_config as set_config_tools,\
    get_fgapiserver_db,\
    check_db_ver,\
    check_db_reg
# from flask_login import LoginManager,\
#                         login_required,\
#                         current_user
import os
import sys
import logging.config

"""
  FutureGateway APIServer front-end
"""

__author__ = 'Riccardo Bruno'
__copyright__ = '2019'
__license__ = 'Apache'
__version__ = 'v0.0.0'
__maintainer__ = 'Riccardo Bruno'
__email__ = 'riccardo.bruno@ct.infn.it'
__status__ = 'devel'
__update__ = '2019-02-26 16:08:31'


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

# FutureGateway database object
fgapisrv_db = get_fgapiserver_db()

# Spread db object across components
# set_config_tools(fgapisrv_db)
# set_db_process(fgapisrv_db)


# setup Flask app
app = Flask(__name__)
# login_manager = LoginManager()
# login_manager.init_app(app)

##
# Routes as specified for APIServer at http://docs.csgfapis.apiary.io
##


@app.route('/')
def index():

    logging.debug('index(%s): %s' % (request.method, request.values.to_dict()))
    resp = "<html><body><h1>It works!</h1></body></html>"
    return resp


#
# The fgAPIServer app starts here
#


# Get database object and check the DB
check_db_ver()

# Server registration and configuration from fgdb
check_db_reg(fg_config)

# Now execute accordingly to the app configuration (stand-alone/wsgi)
if __name__ == "__main__":
    # Inform user about server activity
    print("fgAPIServerDaemon GUI running in stand-alone mode ...")

    # Starting-up server
    if len(fg_config['crt']) > 0 and \
            len(fg_config['key']) > 0:
        context = (fg_config['crt'],
                   fg_config['key'])
        app.run(host=fg_config['host'],
                port=fg_config['port'],
                ssl_context=context,
                debug=fg_config['debug'])
    else:
        app.run(host=fg_config['host'],
                port=fg_config['port'],
                debug=fg_config['debug'])
