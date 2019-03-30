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
from ExecutorInterface\
    import ExecutorInterface,\
           executor_interface,\
           UnknownEIAction


"""
  FutureGateway Tester application for ExecutorInteface
"""

__author__ = 'Riccardo Bruno'
__copyright__ = '2019'
__license__ = 'Apache'
__version__ = 'v0.0.10'
__maintainer__ = 'Riccardo Bruno'
__email__ = 'riccardo.bruno@ct.infn.it'
__status__ = 'devel'
__update__ = '2019-03-23 16:12:11'


ei_name = 'TestExecutor'
test_ei = executor_interface(ei_name)
if test_ei is not None:

    # Using exec method
    try:
        print("Using exec:")
        test_ei.exec('CLEAN')
        test_ei.exec('GETSTATUS')
        test_ei.exec('GETOUTPUT')
        test_ei.exec('CANCEL')
        test_ei.exec('SUBMIT')
        test_ei.exec('DELETE')
        test_ei.exec('UNKNOWN')
    except UnknownEIAction as e:
        print("Exception occurred: '%s'" % e)

    # Method may be called directly
    try:
        print("Using direct call:")
        test_ei.clean()
        test_ei.get_status()
        test_ei.get_output()
        test_ei.cancel()
        test_ei.submit()
        test_ei.delete()
        test_ei.undefined()
    except AttributeError as e:
        print("Generic exception: '%s'" % e)
else:
    print("No '%s' interface received" % ei_name)
