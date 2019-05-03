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
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
from fgapiserverdaemon_db\
    import FGAPIServerDB,\
    def_db_host,\
    def_db_port,\
    def_db_host,\
    def_db_user,\
    def_db_pass,\
    def_db_name
from fgapiserverdaemon_command import APIServerCommand
from fgapiserverdaemon_config import fg_config

"""
  GridEngine APIServerDaemon database
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


def get_db(**kwargs):
    """
    Retrieve the fgAPIServer database object

    :return: Return the fgAPIServer database object or None if the
             database connection fails
    """
    args = {}
    if kwargs is not None:
        for key, value in kwargs.items():
            args[key] = value
    db_host = args.get('db_host', def_db_host)
    db_port = args.get('db_port', def_db_port)
    db_user = args.get('db_user', def_db_user)
    db_pass = args.get('db_pass', def_db_pass)
    db_name = args.get('db_name', def_db_name)
    db_object = FGAPIServerDBProcess(
        db_host=db_host,
        db_port=db_port,
        db_user=db_user,
        db_pass=db_pass,
        db_name=db_name)
    db_state = db_object.get_state()
    if db_state[0] != 0:
        message = ("Unbable to connect to the database:\n"
                   "  host: %s\n"
                   "  port: %s\n"
                   "  user: %s\n"
                   "  pass: %s\n"
                   "  name: %s\n"
                   % (db_host,
                      db_port,
                      db_user,
                      db_pass,
                      db_name))
        return None, message
    return db_object, None


"""
  fgapiserver_db_process Class contain any database query performed by the
  process elements: task_checker and task_extractor
"""


class FGAPIServerDBProcess(FGAPIServerDB):
    """
    FutureGateway API Server Database class for process
    """

    def queue_tasks_retrieve(self):
        """
        Retrieve queued tasks

        :return: List of queued tasks
        """
        db = None
        cursor = None
        safe_transaction = False
        queued_tasks = []
        try:
            db = self.connect(safe_transaction)
            cursor = db.cursor()
            sql = ('select id\n'
                   'from as_queue;')
            sql_data = ()
            logging.debug(sql % sql_data)
            cursor.execute(sql, sql_data)
            for task_queue_record in cursor:
                queued_tasks += [
                    {"id": task_queue_record[0], }]
            self.query_done(
                "Queued tasks: %s" % queued_tasks)
        except MySQLdb.Error as e:
            self.catch_db_error(e, db, safe_transaction)
        finally:
            self.close_db(db, cursor, safe_transaction)
        return queued_tasks

    def get_queued_commands(self, max_commands):
        """
        Returns an array of commands for task submission from APIServer queue
        having at most given number of elements

        :param max_commands: Maximum number of commands to extract for
         execution
        :return Array of commands
        """
        db = None
        cursor = None
        safe_transaction = False
        commands = []
        try:
            db = self.connect(safe_transaction, 'lock tables as_queue write;')
            cursor = db.cursor()
            sql = (
                "select task_id\n"
                "      ,target_id\n"
                "      ,target\n"
                "      ,action\n"
                "      ,status\n"
                "      ,target_status\n"
                "      ,retry\n"
                "      ,creation\n"
                "      ,last_change\n"
                "      ,check_ts\n"
                "      ,action_info\n"
                "from as_queue\n"
                "where status = 'QUEUED'\n"
                "   or status = 'PROCESSED'\n"
                "order by last_change asc\n"
                "limit %s;")
            sql_data = (max_commands,)
            logging.debug(sql % sql_data)
            cursor.execute(sql, sql_data)
            for queue_command in cursor:
                command = APIServerCommand(
                    task_id=queue_command[0],
                    target_id=queue_command[1],
                    target=queue_command[2],
                    action=queue_command[3],
                    status=queue_command[4],
                    target_status=queue_command[5],
                    retry=queue_command[6],
                    creation=queue_command[7],
                    last_change=queue_command[8],
                    check_ts=queue_command[9],
                    action_info=queue_command[10])
                commands.append(command)
            # Mark taken commands as PROCESSING
            for queue_command in commands:
                sql = (
                    "update as_queue set status = 'PROCESSING'\n"
                    "                   ,last_change = now()\n"
                    "where task_id=%s\n"
                    "  and action=%s;")
                sql_data = (queue_command['task_id'],
                            queue_command['action'])
                logging.debug(sql % sql_data)
                cursor.execute(sql, sql_data)
            self.query_done("Loaded %s queue records " % len(commands))
        except MySQLdb.Error as e:
            self.catch_db_error(e, db, safe_transaction)
        finally:
            self.close_db(db, cursor, safe_transaction, 'unlock tables;')
        return commands

    def get_check_commands(self, max_commands):
        """
        Returns an array of commands to check from APIServer queue having at
        most given number of elements

        :param max_commands: Maximum number of commands to extract for check
        :return Array of commands
        """
        db = None
        cursor = None
        safe_transaction = False
        commands = []
        try:
            db = self.connect(safe_transaction,
                              'lock tables as_queue write;',
                              'unlock tables;')
            cursor = db.cursor()
            sql = (
                "select task_id\n"
                "      ,target_id\n"
                "      ,target\n"
                "      ,action\n"
                "      ,status\n"
                "      ,target_status\n"
                "      ,retry\n"
                "      ,creation\n"
                "      ,last_change\n"
                "      ,check_ts\n"
                "      ,action_info\n"
                "from as_queue\n"
                "where status = 'PROCESSING'\n"
                "   or status = 'PROCESSED'\n"
                "order by check_ts asc\n"
                "limit %s;")
            sql_data = (max_commands,)
            logging.debug(sql % sql_data)
            cursor.execute(sql, sql_data)
            for queue_command in cursor:
                command = APIServerCommand(
                    task_id=queue_command[0],
                    target_id=queue_command[1],
                    target=queue_command[2],
                    action=queue_command[3],
                    status=queue_command[4],
                    target_status=queue_command[5],
                    retry=queue_command[6],
                    creation=queue_command[7],
                    last_change=queue_command[8],
                    check_ts=queue_command[9],
                    action_info=queue_command[10])
                commands.append(command)
            # Mark taken commands as PROCESSING
            for queue_command in commands:
                sql = (
                    "update as_queue set status = 'PROCESSING'\n"
                    "                   ,last_change = now()\n"
                    "where task_id=%s\n"
                    "  and action=%s;")
                sql_data = (queue_command['task_id'],
                            queue_command['action'])
                logging.debug(sql % sql_data)
                cursor.execute(sql, sql_data)
            self.query_done("Loaded %s queue records " % len(commands))
        except MySQLdb.Error as e:
            self.catch_db_error(e, db, safe_transaction)
        finally:
            self.close_db(db, cursor, safe_transaction)
        return commands


# FutureGateway database object
fgapisrv_db_process, message = get_db(
    db_host=fg_config['fgapisrv_db_host'],
    db_port=fg_config['fgapisrv_db_port'],
    db_user=fg_config['fgapisrv_db_user'],
    db_pass=fg_config['fgapisrv_db_pass'],
    db_name=fg_config['fgapisrv_db_name'])
if fgapisrv_db_process is None:
    logging.error(message)
