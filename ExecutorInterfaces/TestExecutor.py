#!/usr/bin/env python
# coding: utf-8
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
from __future__ import print_function
from ExecutorInterface\
    import BaseExecutorInterface,\
           executor_interface,\
           EIError

"""
  FutureGateway Test Executor Inteface
"""

__author__ = 'Riccardo Bruno'
__copyright__ = '2019'
__license__ = 'Apache'
__version__ = 'v0.0.10'
__maintainer__ = 'Riccardo Bruno'
__email__ = 'riccardo.bruno@ct.infn.it'
__status__ = 'devel'
__update__ = '2019-03-23 16:12:11'


class TestExecutor(BaseExecutorInterface):
    """
    Test Executor Interface, it jus execute commands in localhost
    """

    def __init__(self):
        print("init TestExecutor")

    def clean(self):
        """
        Clean
        """
        print("clean action in %s called, " % __name__, end='')

    def get_status(self):
        """
        Get Status
        """
        print("get_status action in %s called, " % __name__, end='')

    def get_output(self):
        """
        Get Output
        """
        print("get_output action in %s called, " % __name__, end=' ')

    def cancel(self):
        """
        Cancel
        """
        print("cancel action in %s called, " % __name__, end=' ')

    def submit(self):
        """
        Submit
        """
        print("submit action in %s called, " % __name__, end=' ')

    def delete(self):
        """
        Delete
        """
        print("delete action in  TestExecutor", end=' ')

if __name__ == "__main__":
    print("This is a test ExecutorInterface")

    ei_name = 'TestExecutor'
    test_ei = executor_interface(ei_name)

    if test_ei is not None:

        # Using exec method
        try:
            print("Using action method:")
            print("  CLEAN ... ", end='')
            test_ei.action('CLEAN')
            print("ok")
            print("  GETSTATUS ... ", end='')
            test_ei.action('GETSTATUS')
            print("ok")
            print("  GETOUTPUT ... ", end='')
            test_ei.action('GETOUTPUT')
            print("ok")
            print("  CANCEL ... ", end='')
            test_ei.action('CANCEL')
            print("ok")
            print("  SUBMIT ... ", end='')
            test_ei.action('SUBMIT')
            print("ok")
            print("  DELETE ... ", end='')
            test_ei.action('DELETE')
            print("ok")
            print("  UNKNOWN ... ", end='')
            test_ei.action('UNKNOWN')
            print("ok")
        except EIError as e:
            print("failed")
            print("EI exception occurred: '%s'" % e)

        # Method may be called directly
        try:
            print("Using direct call:")
            print("  clean() ... ", end='')
            test_ei.clean()
            print("ok")
            print("  get_status() ... ", end='')
            test_ei.get_status()
            print("ok")
            print("  get_output() ... ", end='')
            test_ei.get_output()
            print("ok")
            print("  cancel() ... ", end='')
            test_ei.cancel()
            print("ok")
            print("  submit() ... ", end='')
            test_ei.submit()
            print("ok")
            print("  delete() ... ", end='')
            test_ei.delete()
            print("ok")
            print("  undefined() ... ", end='')
            test_ei.undefined()
            print("ok")
        except AttributeError as e:
            print("Generic exception: '%s'" % e)
    else:
        print("No '%s' interface received" % ei_name)
