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
import yaml
import json
import logging

# Logging object
logger = logging.getLogger(__name__)


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


# ExecutorInterface supporteed actions are stored in this class as static values
# This emulates eunum constants due to incompatibilities betweeen py2 and py3
class EIActions(object):

    Actions = ['CLEAN',     # Clean any reference of a task releasing allocated resources
               'SUBMIT',    # Submit a task on a targeted infrastructure.
               'GETSTATUS', # Get the status of a task (unused; no reference to API specs).
               'GETOUTPUT', # Get the output of a task (unused; no reference to API specs).
               'CANCEL',    # Cancel the execution of a task (unused; no reference to API specs).
               'DELETE',    # # Delete the reference of a task (unused)
               ]

    @staticmethod
    def equals(action):
        for i in range(0, len(EIActions.Actions)):
            if action == EIActions.Actions[i]:
                return action
        return None

def executor_interface(ei_name):
    """
    executor_interface, return a given executor interface object by its name
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
        if action == EIActions.equals('CLEAN'):
            self.clean()
        elif action == EIActions.equals('SUBMIT'):
            self.submit()
        elif action == EIActions.equals('GETSTATUS'):
            self.get_status()
        elif action == EIActions.equals('GETOUTPUT'):
            self.get_output()
        elif action == EIActions.equals('CANCEL'):
            self.cancel()
        elif action == EIActions.equals('DELETE'):
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

class EIConfig(dict):

    # Base Executor Interface contain only json_indent value
    defaults = {'generic': {'json_indent': '4'}}

    # Configuration data types
    # Following vectors consider only int and bool types remaining
    # configuration options will be considered strings as default
    int_types = ['json_indent']
    bool_types = []

    def __init__(self, config_file):
        """
        Initialize the configutation object loading the given
        configuration file
        """
        dict.__init__(self)

        # Load config from config_file
        if config_file is None:
            config_file = ''
        conf_yaml = {}
        try:
            conf_file = open(config_file, 'r')
            conf_yaml = yaml.load(conf_file)
            self.config_file = config_file
        except IOError:
            logging.warn(
                "Couldn't find configuration file '%s'; "
                " default options will be used" % config_file)
            pass

        # Load configuration settings using hardcoded key values as key
        # reference
        for section in self.defaults.keys():
            for conf_name in self.defaults[section].keys():
                def_value = self.defaults[section][conf_name]
                try:
                    self[conf_name] = conf_yaml[section][conf_name]
                except KeyError:
                    self[conf_name] = def_value
                    logging.warn(
                        "Couldn't find option '%s' "
                        "in section '%s'; "
                        "using default value '%s'"
                        % (conf_name, section, def_value))
                # The use of environment varialbes override any default or
                # configuration setting present in the configuration file
                try:
                    env_value = os.environ[conf_name.upper()]
                    logging.warn(
                        "Environment bypass of '%s': '%s' <- '%s'" %
                        (conf_name, self[conf_name], env_value))
                    self[conf_name] = env_value
                except KeyError:
                    # Corresponding environment variable not exists
                    pass

        if self['debug']:
            logging.debug(self.show_conf())

    def __getitem__(self, key):
        conf_value = dict.__getitem__(self, key)
        if key in self.bool_types:
            conf_value = (str(conf_value).lower() == 'true')
        if key in self.int_types:
            conf_value = int(conf_value)
        return conf_value

    def __setitem__(self, key, value):
        if key in self.bool_types:
            conf_value = (str(value).lower() == 'true')
        elif key in self.int_types:
            conf_value = int(value)
        else:
            conf_value = value
        dict.__setitem__(self, key, conf_value)

    def __repr__(self):
        """
        Perform object representation as in defaults scheme
        :return:
        """
        config = {}
        for section in self.defaults.keys():
            section_config = {}
            for key in self.defaults[section]:
                section_config[key] = self[key]
            config[section] = section_config
        return json.dumps(config, indent=int(self['json_indent']))

    def show_conf(self):
        """
        Show the loaded APIServer fron-end configuration
        :return:
        """
        config = {}
        for section in self.defaults.keys():
            section_config = {}
            for key in self.defaults[section]:
                section_config[key] = self[key]
            config[section] = section_config

        return ("\n"
                "---------------------------------------\n"
                " %s config \n"
                "---------------------------------------\n"
                "%s\n" % (__name__, self))

    def get_messages(self):
        """
        Return the messages created during configuration loading
        """
        return self.fg_config_messages

    def load_config(self, cfg_dict):
        """
        Save configuration settings stored in the given dictionary
        """
        if cfg_dict is not None:
            for key in cfg_dict:
                value = cfg_dict[key]
                self[key] = value
