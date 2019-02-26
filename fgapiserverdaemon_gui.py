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
from fgapiserverdaemon_config import\
    FGApiServerConfig
# from flask_login import LoginManager,\
#                         login_required,\
#                         current_user
from fgapiserverdaemon_tools import\
    get_fgapiserver_db,\
    check_db_ver,\
    check_db_reg,\
    update_db_config
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
__update__ = '2019-02-26 12:53:42'


# setup path
fgapirundir = os.path.dirname(os.path.abspath(__file__)) + '/'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# fgapiserver configuration file
fgapiserver_config_file = fgapirundir + 'fgapiserverdaemon.conf'

# Load configuration
fg_config = FGApiServerConfig(fgapiserver_config_file)

# FutureGateway database object
fgapisrv_db = get_fgapiserver_db()

# Logging
logging.config.fileConfig(fg_config['logcfg'])
logger = logging.getLogger(__name__)
logger.debug("fgAPIServerDaemon GUI Starting")

# setup Flask app
app = Flask(__name__)
# login_manager = LoginManager()
# login_manager.init_app(app)

##
# Routes as specified for APIServer at http://docs.csgfapis.apiary.io
##


@app.route('/')
def index():

    logger.debug('index(%s): %s' % (request.method, request.values.to_dict()))
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
    print ("fgAPIServerDaemon GUI running in stand-alone mode ...")

    # Starting-up server
    if len(fg_config['fgapiserverdaemon_crt']) > 0 and \
            len(fg_config['fgapiserverdaemon_key']) > 0:
        context = (fg_config['fgapiserverdaemon_crt'],
                   fg_config['fgapiserverdaemon_key'])
        app.run(host=fg_config['fgapiserverdaemon_host'],
                port=fg_config['fgapiserverdaemon_port'],
                ssl_context=context,
                debug=fg_config['fgapiserverdaemon_debug'])
    else:
        app.run(host=fg_config['fgapiserverdaemon_host'],
                port=fg_config['fgapiserverdaemon_port'],
                debug=fg_config['fgapiserverdaemon_debug'])
