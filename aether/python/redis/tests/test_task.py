# Copyright (C) 2019 by eHealth Africa : http://www.eHealthAfrica.org
#
# See the NOTICE file distributed with this work for additional information
# regarding copyright ownership.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import birdisle.redis
import uuid
import time
import os
from typing import NamedTuple


from unittest import TestCase

from aether.python.redis.task import (
    Task, TaskEvent, TaskHelper, get_settings, UUIDEncoder
)


class Settings(NamedTuple):
    REDIS_PASSWORD: str
    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_DB: str


settings = Settings(
    REDIS_DB=os.environ.get('REDIS_DB', 0),
    REDIS_PASSWORD=os.environ.get('REDIS_PASSWORD'),
    REDIS_HOST=os.environ.get('REDIS_HOST'),
    REDIS_PORT=int(os.environ.get('REDIS_PORT', 6379)),
)

WAIT_FOR_REDIS = 0.5


class TaskTests(TestCase):
    test_doc = {
        'id': '000-000-000-00',
        'name': 'test_name'
    }
    # work around a birdisle bug with redis 3.3 compat
    birdisle.redis.LocalSocketConnection.health_check_interval = 0
    redis_instance = birdisle.redis.StrictRedis()
    # set keyspace notifications as we do in live
    task = TaskHelper(settings, redis_instance)

    # callable function generator that changes a value on the local scope
    def get_callable(self, obj):
        def callable(msg):
            obj['result'] = msg
        return callable

    def test_helper_func(self):
        assert get_settings(('tuple_test',)) == 'tuple_test'
        encoder = UUIDEncoder()
        id = uuid.uuid4()
        expected = str(id)
        assert encoder.default(id) == expected

    def test_helper_init(self):
        task = TaskHelper(settings)
        assert task is not None

    def test_add_get_list_exists_remove(self):
        self.task.add(self.test_doc, 'mappings', 'aether')
        assert(
            len(self.task.get_keys('_map*')) == 1
        )
        doc = self.task.get(self.test_doc['id'], 'mappings', 'aether')
        assert doc['id'] == self.test_doc['id']

        doc_ids = list(self.task.list('mappings', 'aether'))
        assert doc['id'] in doc_ids

        assert(
            self.task.exists(self.test_doc['id'], 'mappings', 'aether')
            is True
        )
        assert(
            self.task.exists('wrong-id', 'mappings', 'aether')
            is False
        )
        with self.assertRaises(ValueError):
            self.task.get('wrong-id', 'mappings', 'aether')

        assert (
            self.task.remove('wrong-id', 'mappings', 'aether')
            is False
        )
        assert (
            self.task.remove(self.test_doc['id'], 'mappings', 'aether')
            is True
        )
        assert(
            len(self.task.get_keys('_map*')) == 0
        )
        assert(
            self.task.exists(self.test_doc['id'], 'mappings', 'aether')
            is False
        )

    def test_add_mt_list_all(self):
        self.task.add(self.test_doc, 'mappings', 'aether')
        assert(
            len(self.task.get_keys('_map*')) == 1
        )
        self.task.add(self.test_doc, 'mappings', 'other-tenant')
        assert(
            len(self.task.get_keys('_map*')) == 2
        )

        with self.assertRaises(ValueError):
            list(self.task.list('*', '*'))

        with self.assertRaises(ValueError):
            list(self.task.list('mappings', '*'))

        assert(len(list(self.task.list('mappings'))) == 2)
        assert (
            self.task.remove(self.test_doc['id'], 'mappings', 'aether')
            is True
        )
        assert (
            self.task.remove(self.test_doc['id'], 'mappings', 'other-tenant')
            is True
        )

    def test_subscribe(self):
        obj = {}
        callable = self.get_callable(obj)

        self.task.subscribe(callable, '_test*', True)
        time.sleep(.1)
        self.task.add(self.test_doc, 'test', 'aether')
        time.sleep(.1)
        assert(isinstance(obj['result'], Task))
        self.task.remove(self.test_doc['id'], 'test', 'aether')
        time.sleep(.1)
        assert(isinstance(obj['result'], TaskEvent))

    def test_subscribe_again(self):
        obj = {}
        callable = self.get_callable(obj)

        self.task.subscribe(callable, '_test*', True)
        assert(
            self.task.publish(self.test_doc, 'test', 'aether') == 1
        )
        # subscribe again
        assert(
            self.task.subscribe(callable, '_test*', False) is None
        )

        assert(
            self.task._unsubscribe_all() is None
        )
        self.task.stop()
        self.redis_instance = None
