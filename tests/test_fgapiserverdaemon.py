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

import unittest
import fgapiserverdaemon
import hashlib
import os
from fgapiserverdaemon_tools import get_fgapiserver_db

__author__ = 'Riccardo Bruno'
__copyright__ = '2019'
__license__ = 'Apache'
__version__ = 'v0.0.0'
__maintainer__ = 'Riccardo Bruno'
__email__ = 'riccardo.bruno@ct.infn.it'
__status__ = 'devel'
__update__ = '2019-02-26 13:36:13'

# FGTESTS_STOPATFAIL environment controls the execution
# of the tests, if defined, it stops test execution as
# soon as the first test error occurs
stop_at_fail = os.getenv('FGTESTS_STOPATFAIL') is not None


class TestfgAPIServer(unittest.TestCase):

    @staticmethod
    def banner(test_name):
        print ""
        print "------------------------------------------------"
        print " Testing: %s" % test_name
        print "------------------------------------------------"

    @staticmethod
    def md5sum(filename, blocksize=65536):
        hash_value = hashlib.md5()
        with open(filename, "rb") as f:
            for block in iter(lambda: f.read(blocksize), b""):
                hash_value.update(block)
        return hash_value.hexdigest()

    @staticmethod
    def md5sum_str(string):
        return hashlib.md5(string).hexdigest()

    #
    # fgapiserver
    #

    def test_checkDbVer(self):
        self.banner("checkDbVer()")
        self.assertEqual('0.0.12b', fgapiserverdaemon.check_db_ver())

    #
    # fgapiserverdb
    #
    fgapisrv_db = get_fgapiserver_db()

    def test_dbobject(self):
        self.banner("Testing fgapiserverdb get DB object")
        assert self.fgapisrv_db is not None

    def test_dbobj_connect(self):
        self.banner("Testing fgapiserverdb connect")
        conn = self.fgapisrv_db.connect()
        assert conn is not None

    def test_dbobj_test(self):
        self.banner("Testing fgapiserverdb test")
        result = self.fgapisrv_db.test()
        state = self.fgapisrv_db.get_state()
        print result
        print "DB state: %s" % (state,)
        assert state[0] is False


if __name__ == '__main__':
    print "----------------------------------"
    print "Starting unit tests ..."
    print "----------------------------------"
    unittest.main(failfast=stop_at_fail)
    print "Tests completed"