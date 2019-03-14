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
import hashlib
import json
import os
from fgapiserverdaemon_gui import app

__author__ = 'Riccardo Bruno'
__copyright__ = '2019'
__license__ = 'Apache'
__version__ = 'v0.0.0'
__maintainer__ = 'Riccardo Bruno'
__email__ = 'riccardo.bruno@ct.infn.it'
__status__ = 'devel'
__update__ = '2019-03-14 18:48:34'

# FGTESTS_STOPATFAIL environment controls the execution
# of the tests, if defined, it stops test execution as
# soon as the first test error occurs
stop_at_fail = os.getenv('FGTESTS_STOPATFAIL') is not None


class TestfgAPIServer(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.app.debug = True

    @staticmethod
    def banner(test_name):
        print("")
        print("------------------------------------------------")
        print(" Testing: %s" % test_name)
        print("------------------------------------------------")

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
    # GUI Address
    #

    def test_get_index(self):
        self.banner("Endpoint: /")
        result = self.app.get('/')
        md5 = self.md5sum_str(result.data)
        print("Result: '%s'" % result)
        print("Result data: '%s'" % result.data)
        print("MD5: '%s'" % md5)
        self.assertEqual(md5, 'c7b4690c8c46625ef0f328cd7a24a0a3')


if __name__ == '__main__':
    print("----------------------------------")
    print("Starting unit tests ...")
    print("----------------------------------")
    unittest.main(failfast=stop_at_fail)
    print("Tests completed")
