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

from fgapiserverdaemon_config import FGApiServerConfig
import MySQLdb
import os
import sys
import logging


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
__update__ = '2019-02-20 23:01:48'

"""
 Database connection default settings
"""
def_db_host = 'localhost'
def_db_port = 3306
def_db_user = 'fgapiserver'
def_db_pass = 'fgapiserver_password'
def_db_name = 'fgapiserver'

# setup path
fgapirundir = os.path.dirname(os.path.abspath(__file__)) + '/'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# fgapiserver configuration file
fgapiserver_config_file = fgapirundir + 'fgapiserverdaemon.conf'

# Load configuration
fg_config = FGApiServerConfig(fgapiserver_config_file)

# Logging
logging.config.fileConfig(fg_config['logcfg'])


def get_db(**kwargs):
    """
    Retrieve the fgAPIServer database object

    :return: Return the fgAPIServer database object or None if the
             database connection fails
    """
    args = {}
    if kwargs is not None:
        for key, value in kwargs.iteritems():
            args[key] = value
    db_host = args.get('db_host', def_db_host)
    db_port = args.get('db_port', def_db_port)
    db_user = args.get('db_user', def_db_user)
    db_pass = args.get('db_pass', def_db_pass)
    db_name = args.get('db_name', def_db_name)
    fgapiserver_db = FGAPIServerDB(
        db_host=db_host,
        db_port=db_port,
        db_user=db_user,
        db_pass=db_pass,
        db_name=db_name)
    db_state = fgapiserver_db.get_state()
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
    return fgapiserver_db, None


"""
  fgapiserver_db Class contain any call interacting with fgapiserver database
"""


class FGAPIServerDB:

    """
     API Server Database connection settings
    """
    db_host = None
    db_port = None
    db_user = None
    db_pass = None
    db_name = None

    """
        Error Flag and messages filled up upon failures
    """
    err_flag = False
    err_msg = ''
    message = ''

    """
      FGAPIServerDB - Constructor may override default
                      values defined at the top of the file
    """

    def __init__(self, **kwargs):
        """

        :rtype:
        """
        self.db_host = kwargs.get('db_host', def_db_host)
        self.db_port = kwargs.get('db_port', def_db_port)
        self.db_user = kwargs.get('db_user', def_db_user)
        self.db_pass = kwargs.get('db_pass', def_db_pass)
        self.db_name = kwargs.get('db_name', def_db_name)
        logging.debug("[DB settings]\n"
                      " host: '%s'\n"
                      " port: '%s'\n"
                      " user: '%s'\n"
                      " pass: '%s'\n"
                      " name: '%s'\n"
                      % (self.db_host,
                         self.db_port,
                         self.db_user,
                         self.db_pass,
                         self.db_name))

    """
      catchDBError - common operations performed upon database
                     query/transaction failure
    """

    def catch_db_error(self, e, db, rollback):
        logging.error("[ERROR] %d: %s" % (e.args[0], e.args[1]))
        if rollback is True:
            db.rollback()
        self.err_flag = True
        self.err_msg = "[ERROR] %d: %s" % (e.args[0], e.args[1])

    """
      close_db - common operatoins performed closing DB query/transaction
    """

    @staticmethod
    def close_db(db, cursor, commit):
        if cursor is not None:
            cursor.close()
        if db is not None:
            if commit is True:
                db.commit()
            db.close()

    """
      query_done - reset the query error flag and eventually set
                   a given query related message
    """

    def query_done(self, message):
        self.err_flag = False
        self.err_msg = message
        logging.debug("Query done message:\n"
                      "%s" % message)

    """
      connect Connects to the fgapiserver database
    """

    def connect(self, safe_transaction=False):
        db = MySQLdb.connect(
            host=self.db_host,
            user=self.db_user,
            passwd=self.db_pass,
            db=self.db_name,
            port=self.db_port)
        if db is not None and safe_transaction is True:
            sql = "BEGIN"
            sql_data = ()
            cursor = db.cursor()
            logging.debug(sql % sql_data)
            cursor.execute(sql)
            cursor.close()
        return db

    """
     test - DB connection tester function
    """

    def test(self):
        db = None
        cursor = None
        safe_transaction = False
        try:
            # Connect the DB
            db = self.connect(safe_transaction)
            # Prepare SQL statement
            sql = "SELECT VERSION()"
            # Prepare SQL data for statement
            sql_data = ()
            # Prepare a cursor object
            cursor = db.cursor()
            # View query in logs
            logging.debug(sql % sql_data)
            # Execute SQL statement
            cursor.execute(sql)
            # Fetch a single row using fetchone() method.
            data = cursor.fetchone()
            self.query_done("Database version : '%s'" % data[0])
        except MySQLdb.Error as e:
            self.catch_db_error(e, db, safe_transaction)
        finally:
            self.close_db(db, cursor, safe_transaction)

    """
      get_db_version - Return the database version
    """

    def get_db_version(self):
        db = None
        cursor = None
        safe_transaction = False
        dbver = ''
        try:
            db = self.connect(safe_transaction)
            cursor = db.cursor()
            sql = 'select version from db_patches order by id desc limit 1;'
            sql_data = ()
            logging.debug(sql % sql_data)
            cursor.execute(sql, sql_data)
            dbver = cursor.fetchone()[0]
            self.query_done("fgapiserver DB schema version: '%s'" % dbver)
        except MySQLdb.Error as e:
            self.catch_db_error(e, db, safe_transaction)
        finally:
            self.close_db(db, cursor, safe_transaction)
        return dbver

    """
      is_srv_reg - Return true if the service is registered
    """

    def is_srv_reg(self, service_uuid):
        db = None
        cursor = None
        safe_transaction = False
        is_reg = False
        try:
            db = self.connect(safe_transaction)
            cursor = db.cursor()
            sql = 'select count(*)>0 from srv_registry where uuid = %s;'
            sql_data = (service_uuid,)
            logging.debug(sql % sql_data)
            cursor.execute(sql, sql_data)
            is_reg = cursor.fetchone()[0]
            self.query_done("Service registration '%s' is '%s'"
                            % (service_uuid, is_reg))
        except MySQLdb.Error as e:
            self.catch_db_error(e, db, safe_transaction)
        finally:
            self.close_db(db, cursor, safe_transaction)
        return is_reg

    """
      srv_register - Register the given server and stores its current
                     configuration
    """

    def srv_register(self, fgapisrv_uuid, config):
        db = None
        cursor = None
        safe_transaction = True
        try:
            db = self.connect(safe_transaction)
            cursor = db.cursor()
            sql = (
                'insert into srv_registry (uuid,\n'
                '                          creation,\n'
                '                          last_access,\n'
                '                          enabled)\n'
                'values (%s,now(),now(),%s);'
            )
            sql_data = (fgapisrv_uuid, True)
            logging.debug(sql % sql_data)
            cursor.execute(sql, sql_data)
            # Now save configuration settings
            for key in config.keys():
                key_value = "%s" % config[key]
                sql = (
                    'insert into srv_config (uuid,\n'
                    '                        name,\n'
                    '                        value,\n'
                    '                        enabled,\n'
                    '                        created,\n'
                    '                        modified)\n'
                    'values (%s, %s, %s, %s, now(), now());'
                )
                sql_data = (fgapisrv_uuid, key, key_value, True)
                logging.debug(sql % sql_data)
                cursor.execute(sql, sql_data)
            # Calculate configuration hash
            sql = (
                'select md5(group_concat(value)) cfg_hash\n'
                'from srv_config\n'
                'where uuid = %s\n'
                'group by uuid;'
            )
            sql_data = (fgapisrv_uuid,)
            logging.debug(sql % sql_data)
            cursor.execute(sql, sql_data)
            cfg_hash = cursor.fetchone()[0]
            # Register calculated hash
            sql = 'update srv_registry set cfg_hash = %s where uuid = %s;'
            sql_data = (cfg_hash, fgapisrv_uuid)
            logging.debug(sql % sql_data)
            cursor.execute(sql, sql_data)
            # Service registration queries executed
            self.query_done("Service with uuid: '%s' has been registered"
                            "and configuration parameters saved."
                            % fgapisrv_uuid)
        except MySQLdb.Error as e:
            self.catch_db_error(e, db, safe_transaction)
        finally:
            self.close_db(db, cursor, safe_transaction)

    """
      srv_config - returns a dictionary containing configuration settings
                   of the service using its uuid value
    """

    def srv_config(self, fgapisrv_uuid):
        global fg_config
        db = None
        cursor = None
        safe_transaction = False
        try:
            db = self.connect(safe_transaction)
            cursor = db.cursor()
            sql = (
                'select name,\n'
                '       value\n'
                'from srv_config\n'
                'where uuid=%s and enabled=%s;'
            )
            sql_data = (fgapisrv_uuid, True)
            logging.debug(sql % sql_data)
            cursor.execute(sql, sql_data)
            for config in cursor:
                kname = config[0]
                kvalue = config[1]
                fg_config[kname] = kvalue
            self.query_done("Configuration settings for service having "
                            "uuid: '%s' have been retrieved." % fgapisrv_uuid)
        except MySQLdb.Error as e:
            self.catch_db_error(e, db, safe_transaction)
        finally:
            self.close_db(db, cursor, safe_transaction)
        return fg_config

    """
      get_state returns the status and message of the last action on the DB
    """

    def get_state(self):
        """

        :return: Error flag, Error message
        """
        return self.err_flag, self.err_msg

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
                    {"id":  task_queue_record[0], }]
            self.query_done(
                "Queued tasks: %s" % queued_tasks)
        except MySQLdb.Error as e:
            self.catch_db_error(e, db, safe_transaction)
        finally:
            self.close_db(db, cursor, safe_transaction)
        return queued_tasks
