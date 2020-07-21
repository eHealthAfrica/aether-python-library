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

import pytest

from aether.python.tests import (
    EXAMPLE_ALL_TYPES,
    EXAMPLE_ANNOTATED_SCHEMA,
    EXAMPLE_AUTOGEN_SCHEMA,
    EXAMPLE_SIMPLE_SCHEMA
)

from aether.python.avro.schema import Node
from aether.python.avro.generation import SampleGenerator


@pytest.mark.unit
@pytest.fixture(scope='module')
def AutoSchema():
    return Node(EXAMPLE_AUTOGEN_SCHEMA)


@pytest.mark.unit
@pytest.fixture(scope='module')
def SimpleSchema():
    return Node(EXAMPLE_SIMPLE_SCHEMA)


@pytest.mark.unit
@pytest.fixture(scope='module')
def ComplexSchema():
    return Node(EXAMPLE_ANNOTATED_SCHEMA)


@pytest.mark.unit
@pytest.fixture(scope='function')
def SimpleGenerator():
    return SampleGenerator(EXAMPLE_SIMPLE_SCHEMA)


@pytest.mark.unit
@pytest.fixture(scope='function')
def ComplexGenerator():
    return SampleGenerator(EXAMPLE_ANNOTATED_SCHEMA)


@pytest.mark.unit
@pytest.fixture(scope='function')
def AllTypesGenerator():
    return SampleGenerator(EXAMPLE_ALL_TYPES)
