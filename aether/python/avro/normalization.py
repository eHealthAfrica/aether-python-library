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
# 'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import hashlib
import json
from typing import Dict

from avro.schema import parse
from avro.schemanormalization import Fingerprint, ToParsingCanonicalForm

# Canonical Form && Fingerprinting
# https://avro.apache.org/docs/1.8.1/spec.html#Parsing+Canonical+Form+for+Schemas
# We don't usually use the avro package (spavro is much faster) so we'll package a convenience function here.


def fingerprint_canonical(
    schema: Dict,
    algorithm='CRC-64-AVRO'
) -> str:

    avro_schema = parse(json.dumps(schema))
    normal_schema = ToParsingCanonicalForm(avro_schema)
    bytes_ = Fingerprint(normal_schema, algorithm)
    return bytes_.hex()

# TODO patch MD5 && SHA-256 into `schemanormalization` library


def fingerprint_noncanonical(
    schema: Dict,
) -> str:
    return hashlib.md5(json.dumps(schema).encode('utf-8')).hexdigest()
