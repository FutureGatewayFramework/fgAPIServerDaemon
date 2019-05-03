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

import logging

"""
  GridEngine APIServerDaemon command; it stores and manages queue commands
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


def set_config(config_obj):
    """
    Receive fgAPIServerDaemon configuration settings
    :param config_obj:
    :return:
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


class APIServerCommand(dict):
    """
    FutureGateway API Server Command class
    """
    task_id = None
    target_id = None
    target = None
    action = None
    status = None
    target_status = None
    retry = None
    creation = None
    last_change = None
    check = None
    info = None
    modify_flag = False

    def __init__(self, **kwargs):
        """
        Constructor uses arguments to setup class values
        """
        dict.__init__(self)

        self['task_id'] = kwargs.get('task_id', None)
        self['target_id'] = kwargs.get('target_id', None)
        self['target'] = kwargs.get('target', None)
        self['action'] = kwargs.get('action', None)
        self['status'] = kwargs.get('status', None)
        self['target_status'] = kwargs.get('target_status', None)
        self['retry'] = kwargs.get('retry', None)
        self['creation'] = kwargs.get('creation', None)
        self['last_change'] = kwargs.get('last_change', None)
        self['check'] = kwargs.get('check', None)
        self['info'] = kwargs.get('info', None)
        logging.debug(self)
