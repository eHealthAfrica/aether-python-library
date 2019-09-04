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

from unittest import TestCase, mock

from aether.python import utils

from . import EXAMPLE_NESTED_SOURCE_DATA


class UtilsTests(TestCase):

    def test_merge_objects(self):
        source = {'a': 0, 'c': 3}
        target = {'a': 1, 'b': 2}
        self.assertEqual(utils.merge_objects(source, target, 'overwrite'),
                         {'a': 1, 'b': 2})
        self.assertEqual(source,
                         {'a': 0, 'c': 3},
                         'source content is not touched')
        self.assertEqual(target,
                         {'a': 1, 'b': 2},
                         'target content is not touched')

        source = {'a': 0, 'c': 3}
        target = {'a': 1, 'b': 2}
        self.assertEqual(utils.merge_objects(source, target, 'last_write_wins'),
                         {'a': 1, 'b': 2, 'c': 3})
        self.assertEqual(source,
                         {'a': 1, 'b': 2, 'c': 3},
                         'source content is replaced')
        self.assertEqual(target,
                         {'a': 1, 'b': 2},
                         'target content is not touched')

        source = {'a': 0, 'c': 3}
        target = {'a': 1, 'b': 2}
        self.assertEqual(utils.merge_objects(source, target, 'first_write_wins'),
                         {'a': 0, 'b': 2, 'c': 3})
        self.assertEqual(source,
                         {'a': 0, 'c': 3},
                         'source content is not touched')
        self.assertEqual(target,
                         {'a': 0, 'b': 2, 'c': 3},
                         'target content is replaced')

    def test_object_contains(self):
        data = EXAMPLE_NESTED_SOURCE_DATA
        source_house = data['data']['houses'][0]
        other_house = data['data']['houses'][1]
        test_person = source_house['people'][0]

        is_included = utils.object_contains(test_person, source_house)
        not_included = utils.object_contains(test_person, other_house)

        self.assertTrue(is_included), 'Person should be found in this house.'
        self.assertFalse(not_included, 'Person should not found in this house.')

    def test__request__once(self):
        with mock.patch('aether.python.utils.requests.request',
                        return_value='ok') as mock_req_args:
            resp_args = utils.request('no matter what')
            self.assertEqual(resp_args, 'ok')
            mock_req_args.assert_called_once_with('no matter what')

        with mock.patch('aether.python.utils.requests.request',
                        return_value='ok') as mock_req_kwargs:
            resp_kwargs = utils.request(url='localhost', method='get')
            self.assertEqual(resp_kwargs, 'ok')
            mock_req_kwargs.assert_called_once_with(url='localhost', method='get')

    def test__request__twice(self):
        with mock.patch('aether.python.utils.requests.request',
                        side_effect=[Exception, 'ok']) as mock_req:
            response = utils.request(url='trying twice')
            self.assertEqual(response, 'ok')
            self.assertEqual(mock_req.call_count, 2)
            mock_req.assert_has_calls([
                mock.call(url='trying twice'),
                mock.call(url='trying twice'),
            ])

    def test__request__3_times(self):
        with mock.patch('aether.python.utils.requests.request',
                        side_effect=[Exception, Exception, 'ok']) as mock_req:
            response = utils.request(url='trying three times')
            self.assertEqual(response, 'ok')
            self.assertEqual(mock_req.call_count, 3)
            mock_req.assert_has_calls([
                mock.call(url='trying three times'),
                mock.call(url='trying three times'),
                mock.call(url='trying three times'),
            ])

    def test__request__3_times__raises(self):
        with mock.patch('aether.python.utils.requests.request',
                        side_effect=[
                            Exception('1'),
                            Exception('2'),
                            Exception('3'),
                            'ok',
                        ]) as mock_req:
            with self.assertRaises(Exception) as e:
                response = utils.request(url='raises exception')
                self.assertIsNone(response)
                self.assertIsNotNone(e)
                self.assertEqual(str(e), '3')

            self.assertEqual(mock_req.call_count, 3)
