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
from fgapiserverdaemon_config import FGApiServerConfig
from fgapiserverdaemon_config import fg_config

__author__ = 'Riccardo Bruno'
__copyright__ = '2019'
__license__ = 'Apache'
__version__ = 'v0.0.0'
__maintainer__ = 'Riccardo Bruno'
__email__ = 'riccardo.bruno@ct.infn.it'
__status__ = 'devel'
__update__ = '2019-03-21 19:19:57'

# FGTESTS_STOPATFAIL environment controls the execution
# of the tests, if defined, it stops test execution as
# soon as the first test error occurs
stop_at_fail = os.getenv('FGTESTS_STOPATFAIL') is not None


class TestfgAPIServerConfig(unittest.TestCase):

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
    # fgapiserver_config
    #

    # Default fgAPIServerDaemon configuration values matching defaults
    def test_ConfigObj(self):
        self.banner("Config Object")
        fg_config_nofile = FGApiServerConfig(None)
        for key in fg_config_nofile.keys():
            print("Checking conf[%s]='%s'" % (key, fg_config_nofile[key]))
            self.assertEqual(
                fg_config_nofile[key],
                fgapiserverdaemon.fg_config[key])

    # Environment overriding feature
    def test_EnvConfig(self):
        self.banner("EnvConfig")
        for key in fgapiserverdaemon.fg_config.keys():
            # Skip following values from test
            if key in ['logcfg', ]:
                continue
            if isinstance(fgapiserverdaemon.fg_config[key], bool):
                overwritten_value = not fgapiserverdaemon.fg_config[key]
            elif isinstance(fgapiserverdaemon.fg_config[key], int):
                overwritten_value = -fgapiserverdaemon.fg_config[key]
            else:
                overwritten_value = fgapiserverdaemon.fg_config[key][::-1]
            env_key = key.upper()
            print("Check key:'%s' '%s'<->'%s'" %
                  (key, fgapiserverdaemon.fg_config[key], overwritten_value))
            os.environ[env_key] = "%s" % overwritten_value
            fg_config_nofile = FGApiServerConfig(None)
            self.assertEqual(fg_config_nofile[key], overwritten_value)


if __name__ == '__main__':
    print("----------------------------------")
    print("Starting unit tests ...")
    print("----------------------------------")
    unittest.main(failfast=stop_at_fail)
    print("Tests completed")
