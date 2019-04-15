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
import importlib
from enum import Enum

"""
  FutureGateway Executor Inteface
"""

__author__ = 'Riccardo Bruno'
__copyright__ = '2019'
__license__ = 'Apache'
__version__ = 'v0.0.10'
__maintainer__ = 'Riccardo Bruno'
__email__ = 'riccardo.bruno@ct.infn.it'
__status__ = 'devel'
__update__ = '2019-03-23 16:12:11'


# Executor supporteed actions are stored in this enumerated class
class EIActions(Enum):
         # Release all task resources and any reference to it.
        CLEAN=0
        # Submit a task on a targeted infrastructure.
        SUBMIT=1
        # Get the status of a task (unused; no reference to API specs).
        GETSTATUS=2
        # Get the output of a task (unused; no reference to API specs).
        GETOUTPUT=3
        # Cancel the execution of a task (unused; no reference to API specs).
        CANCEL=4
        # Delete the reference of a task (unused)
        DELETE=5


def executor_interface(ei_name):
    """
    executor_interface, return a given executor interface by name
    """
    instance = None
    try:
       module = importlib.import_module(ei_name)
       class_ = getattr(module, ei_name)
       instance = class_()
    except ImportError:
       print("Unable to find module")
    except AttributeError:
       print("Unable to find class")
    return instance

class BaseExecutorInterface(object):
    """
    Executor Interface Abstract class
    """
    
    def __init__(self):
        """
        Executor Interface Constructor
        """
        pass

    def __repr__(self):
        """
        Representation for BaseExecutorInterface
        """
        raise EIError("ExecutorInterface representation is not implemented")

    def action(self, action):
        """
        Perform the given executor interface action
        """
        if action == EIActions.CLEAN.name:
            self.clean()
        elif action == EIActions.SUBMIT.name:
            self.submit()
        elif action == EIActions.GETSTATUS.name:
            self.get_status()
        elif action == EIActions.GETOUTPUT.name:
            self.get_output()
        elif action == EIActions.CANCEL.name:
            self.cancel()
        elif action == EIActions.DELETE.name:
            self.delete()
        else:
            raise EIError("Unknown action '%s'" % action);

    def clean(self):
        """
        Clean
        """
        raise EIError("Action: 'CLEAN' is not implemented")

    def get_status(self):
        """
        Get Status
        """
        raise EIError("Action: 'GET_STATUS' is not implemented")

    def get_output(self):
        """
        Get Output
        """
        raise EIError("Action: 'GET_OUTPUT' is not implemented")

    def cancel(self):
        """
        Cancel
        """
        raise EIError("Action: 'CANCEL' is not implemented")

    def submit(self):
        """
        Submit
        """
        raise EIError("Action: 'SUBMIT' is not implemented")

    def delete(self):
        """
        Delete
        """
        raise EIError("Action 'DELETE' is not implemented")


class EIError(Exception):
     """
     Called when an unknown Executor Interface Action is called
     """
     pass




