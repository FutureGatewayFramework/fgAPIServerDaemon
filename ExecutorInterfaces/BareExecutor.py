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
from abc import ABCMeta, abstractmethod
from enum import Enum
import importlib
from ExecutorInterface import ExecutorInterface

"""
  FutureGateway Bare Executor Inteface
"""

__author__ = 'Riccardo Bruno'
__copyright__ = '2019'
__license__ = 'Apache'
__version__ = 'v0.0.10'
__maintainer__ = 'Riccardo Bruno'
__email__ = 'riccardo.bruno@ct.infn.it'
__status__ = 'devel'
__update__ = '2019-03-23 16:12:11'


class BareExecutor(ExecutorInterface):
    """
    Bare Executor Interface, it jus execute commands in localhost
    """

    def __init__(self):
        print("init BareExecutor")

    def clean(self):
        """
        Clean
        """
        print("clean BareExecutor")

    def get_status(self):
        """
        Get Status
        """
        print("get_status BareExecutor")

    def get_output(self):
        """
        Get Output
        """
        print("get_output BareExecutor")

    def cancel(self):
        """
        Cancel
        """
        print("cancel BareExecutor")

    def submit(self):
        """
        Submit
        """
        print("submit BareExecutor")

    def delete(self):
        """
        Delete
        """
        print("delete BareExecutor")