#!/usr/bin/env python
# Copyright (c) 2015:
# Istituto Nazionale di Fisica Nucleare (INFN), Italy
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


#
# fgapiserver_queries - Provide queries for fgapiserver tests
#

__author__ = 'Riccardo Bruno'
__copyright__ = '2019'
__license__ = 'Apache'
__version__ = 'v0.0.0'
__maintainer__ = 'Riccardo Bruno'
__email__ = 'riccardo.bruno@ct.infn.it'
__status__ = 'devel'
__update__ = '2019-03-21 19:19:57'


fgapiserverdaemon_queries = [
    {'id': 0,
     'query': 'SELECT VERSION()',
     'result': [['test', ], ]},
    {'id': 1,
     'query': 'select version from db_patches order by id desc limit 1;',
     'result': [['0.0.12b'], ]},
    {'id': 2,
     'query': 'select id\n'
              'from fg_user\n'
              'where name=%s;',
     'result': [[1], ]},
    {'id': 3,
     'query': 'select count(*)>0 from srv_registry\n'
              'where uuid=%s\n'
              '  and enabled=%s;',
     'result': [[1], ]},
    {'id': 4,
     'query': 'select cfg_hash srv_hash\n'
              'from srv_registry\n'
              'where uuid=%s;',
     'result': [['TEST_CFG_HASH', 'TEST_SRV_HASH'], ]},
    {'id': 5,
     'query': 'select md5(group_concat(value)) cfg_hash\n'
              'from srv_config\n'
              'where uuid = %s\n'
              'group by uuid;',
     'result': [['TEST_MDG_GROUP_CONTACT_VALUE'], ]},
    {'id': 6,
     'query': 'select name,\n'
              '       value\n'
              'from srv_config\n'
              'where uuid=%s and enabled=%s;',
     'result': [['TEST_CFG_NAME', 'TEST_CFG_VALUE'], ]},
    {'id': 7,
     'query': 'update srv_registry set cfg_hash = %s where uuid = %s;',
     'result': None},
]

# fgapiserver tests queries
queries = [
    {'category': 'fgapiserverdaemon',
     'statements': fgapiserverdaemon_queries}]
