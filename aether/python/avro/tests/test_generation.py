# Copyright (C) 2019 by eHealth Africa : http://www.eHealthAfrica.org
#
# See the NOTICE file distributed with this work for additional information
# regarding copyright ownership.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# 'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.


import json
import pytest

from aether.python.avro.generation import SampleGenerator
from aether.python.avro.schema import Node
from aether.python.avro.tools import AvroValidationException


from aether.python.avro.tests import *  # noqa

from aether.python.tests import (
    EXAMPLE_SIMPLE_SCHEMA,
)


@pytest.mark.unit
def test__basic_generation(SimpleGenerator):
    sample = SimpleGenerator.make_sample()
    assert(sample is not None)


@pytest.mark.unit
def test__basic_generation_complex(ComplexGenerator):
    sample = ComplexGenerator.make_sample()
    assert(sample is not None)


@pytest.mark.unit
def test__basic_generation_all_types(AllTypesGenerator):
    sample = AllTypesGenerator.make_sample()
    assert(sample is not None)


@pytest.mark.unit
def test__fail_init():
    with pytest.raises(ValueError):
        SampleGenerator()


@pytest.mark.unit
def test__other_init_methods():
    raw_schema_gen = SampleGenerator(raw_schema=json.dumps(EXAMPLE_SIMPLE_SCHEMA))
    assert(raw_schema_gen.make_sample() is not None)
    node_gen = SampleGenerator(node=Node(EXAMPLE_SIMPLE_SCHEMA))
    assert(node_gen.make_sample() is not None)


@pytest.mark.unit
def test__fail_validation(SimpleGenerator):
    SimpleGenerator.set_exclusion('id')  # don't render required field
    with pytest.raises(AvroValidationException):
        SimpleGenerator.make_sample()


@pytest.mark.unit
def test__override_setting(SimpleGenerator):
    SimpleGenerator.set_overrides('Patient_Age', {'min': 1, 'max': 1})
    SimpleGenerator.set_overrides('start', {'constant': 'not-random'})
    obj = SimpleGenerator.make_sample()
    assert(obj['Patient_Age'] == 1)
    assert(obj['start'] == 'not-random')


@pytest.mark.unit
def test__type_handler_basic(ComplexGenerator):
    def make_override(response):
        def override(*args, **kwargs):
            return response
        return (override, {})
    ComplexGenerator.register_type_handler('string', make_override('a'), True)
    ComplexGenerator.register_type_handler('string', make_override('b'), False)
    ComplexGenerator.set_overrides('_open_days', {'max': 1})
    ComplexGenerator.set_overrides('operational_status', {'choices': ['bonkers']})
    ComplexGenerator.set_overrides('healthcare', {'choices': ['bonkers']})
    ComplexGenerator.register_field_handler('id', make_override('an-id'))
    obj = ComplexGenerator.make_sample()
    assert(obj['username'] == 'a')
    assert(obj['id'] == 'an-id')
    assert(len(obj['_open_days']) == 1)
    assert(obj['operational_status'] == 'bonkers')
    assert(obj['healthcare'] == ['bonkers'])
