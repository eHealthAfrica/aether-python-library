#!/usr/bin/env python

# Copyright (C) 2020 by eHealth Africa : http://www.eHealthAfrica.org
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
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import pytest

from avro.schema import SchemaParseException

from aether.python.avro.tests import *  # noqa
from aether.python.avro.normalization import fingerprint_canonical, fingerprint_noncanonical


@pytest.mark.unit
def test__fingerprint_canonical():
    r1 = fingerprint_canonical(EXAMPLE_SIMPLE_SCHEMA)
    r2 = fingerprint_canonical(EXAMPLE_SIMPLE_SCHEMA)
    r3 = fingerprint_canonical(EXAMPLE_ANNOTATED_SCHEMA)
    with pytest.raises(SchemaParseException):
        fingerprint_canonical(EXAMPLE_AUTOGEN_SCHEMA)
    assert(r1 is not None)
    assert(r1 == r2)
    assert(r3 != r1)
    assert(len(r1) == 16)  # short hash


@pytest.mark.unit
def test__fingerprint_noncanonical():
    r1 = fingerprint_noncanonical(EXAMPLE_SIMPLE_SCHEMA)
    r2 = fingerprint_noncanonical(EXAMPLE_SIMPLE_SCHEMA)
    r3 = fingerprint_noncanonical(EXAMPLE_ANNOTATED_SCHEMA)
    r4 = fingerprint_noncanonical(EXAMPLE_AUTOGEN_SCHEMA)
    assert(r1 is not None)
    assert(r1 == r2)
    assert(r3 != r1)
    assert(r4 != r1)
    assert(len(r1) == 32)  # short hash
