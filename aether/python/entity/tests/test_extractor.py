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

import uuid
from unittest import TestCase

from aether.python.entity import extractor

from aether.python.tests import (
    EXAMPLE_MAPPING, EXAMPLE_MAPPING_EDGE, EXAMPLE_SCHEMA, EXAMPLE_SOURCE_DATA,
    EXAMPLE_DATA_FOR_NESTED_SCHEMA, EXAMPLE_REQUIREMENTS_NESTED_SCHEMA,
    EXAMPLE_NESTED_SOURCE_DATA, EXAMPLE_REQUIREMENTS, EXAMPLE_REQUIREMENTS_ARRAY_BASE,
    EXAMPLE_ENTITY_DEFINITION, EXAMPLE_FIELD_MAPPINGS, EXAMPLE_FIELD_MAPPINGS_EDGE,
    EXAMPLE_ENTITY, EXAMPLE_FIELD_MAPPINGS_ARRAY_BASE, EXAMPLE_PARTIAL_WILDCARDS
)


class EntityExtractorTests(TestCase):

    def test_get_field_mappings(self):
        mapping = EXAMPLE_MAPPING
        expected = EXAMPLE_FIELD_MAPPINGS
        field_mapping = str(extractor.get_field_mappings(mapping))
        self.assertTrue(str(expected) in field_mapping, field_mapping)

    def test_get_field_mappings__edge(self):
        mapping = EXAMPLE_MAPPING_EDGE
        expected = EXAMPLE_FIELD_MAPPINGS_EDGE
        field_mapping = str(extractor.get_field_mappings(mapping))
        self.assertTrue(str(expected) in field_mapping, field_mapping)

    def test_JSP_get_basic_fields(self):
        avro_obj = EXAMPLE_SCHEMA
        expected = ['id', '_rev', 'name', 'dob', 'villageID']
        basic_fields = str(extractor.JSP_get_basic_fields(avro_obj))
        self.assertTrue(str(expected) in basic_fields, basic_fields)

    def test_get_entity_definitions(self):
        entity_type = 'Person'
        mapping = EXAMPLE_MAPPING
        schema = {entity_type: EXAMPLE_SCHEMA}
        expected = EXAMPLE_ENTITY_DEFINITION
        entity_definition = str(extractor.get_entity_definitions(mapping, schema))
        self.assertTrue(str(expected) in entity_definition, entity_definition)

    def test_get_entity_requirements(self):
        entities = EXAMPLE_ENTITY_DEFINITION
        field_mappings = EXAMPLE_FIELD_MAPPINGS
        expected = EXAMPLE_REQUIREMENTS
        entity_requirements = str(
            extractor.get_entity_requirements(entities, field_mappings))
        self.assertTrue(str(expected) in entity_requirements,
                        entity_requirements)

    def test_get_entity_requirements__union_base(self):
        entities = EXAMPLE_ENTITY_DEFINITION
        field_mappings = EXAMPLE_FIELD_MAPPINGS_ARRAY_BASE
        expected = EXAMPLE_REQUIREMENTS_ARRAY_BASE
        entity_requirements = str(
            extractor.get_entity_requirements(entities, field_mappings))
        self.assertTrue(str(expected) in entity_requirements,
                        entity_requirements)

    def test_get_entity_stub(self):
        requirements = EXAMPLE_REQUIREMENTS
        source_data = EXAMPLE_SOURCE_DATA
        entity_definitions = EXAMPLE_ENTITY_DEFINITION
        entity_name = 'Person'
        stub = extractor.get_entity_stub(
            requirements, entity_definitions, entity_name, source_data)
        self.assertEqual(len(stub.get('dob')), 3)

    def test_nest_object__simple_object(self):
        obj = {}
        path = 'a.b.c'
        value = 1
        extractor.nest_object(obj, path, value)
        self.assertEqual(obj['a']['b']['c'], value)

    def test_nest_object__unlikely_dotted_reference(self):
        obj = {'a.b': 2, 'a.b.c': None}
        path = 'a.b.c'
        value = 1
        extractor.nest_object(obj, path, value)
        self.assertEqual(obj['a']['b']['c'], value)
        self.assertEqual(obj['a.b'], 2)

    def test_put_nested__simple_object(self):
        keys = ['a', 'b', 'c']
        obj = extractor.put_nested({}, keys, 1)
        self.assertEqual(obj['a']['b']['c'], 1)

    def test_put_nested__array(self):
        keys = ['a', 'b', 'c', 'de[0]']
        obj = extractor.put_nested({}, keys, 1)
        self.assertEqual(obj['a']['b']['c']['de'][0], 1)

    def test_put_in_array__simple(self):
        obj = None
        val = 'a'
        obj = extractor.put_in_array(obj, 0, val)
        self.assertEqual(obj[0], val)

    def test_put_in_array__existing_value(self):
        starting = 1
        obj = [starting]
        val = 'a'
        obj = extractor.put_in_array(obj, 0, val)
        self.assertEqual(obj[0], val)
        self.assertEqual(obj[1], starting)

    def test_put_in_array__large_idx(self):
        obj = None
        val = 'a'
        obj = extractor.put_in_array(obj, 100, val)
        self.assertEqual(obj[0], val)

    def test_resolve_source_reference__single_resolution(self):
        data = EXAMPLE_SOURCE_DATA
        requirements = EXAMPLE_REQUIREMENTS
        entities = EXAMPLE_ENTITY
        entity_name = 'Person'
        field = 'villageID'
        path = requirements.get(entity_name, {}).get(field)[0]
        resolved_count = extractor.resolve_source_reference(
            path, entities, entity_name, 0, field, data)
        self.assertEqual(resolved_count, 1)

    def test_resolve_source_reference__multiple_resolutions(self):
        data = EXAMPLE_SOURCE_DATA
        requirements = EXAMPLE_REQUIREMENTS
        entities = EXAMPLE_ENTITY
        entity_name = 'Person'
        field = 'dob'
        path = requirements.get(entity_name, {}).get(field)[0]
        resolved_count = extractor.resolve_source_reference(
            path, entities, entity_name, 0, field, data)
        self.assertEqual(resolved_count, 3)

    def test_resolve_source_reference__wildcard_resolutions(self):
        data = EXAMPLE_SOURCE_DATA
        entities = EXAMPLE_ENTITY
        entity_name = 'Person'
        field = 'dob'
        path = 'data.pe*[*].dob'
        resolved_count = extractor.resolve_source_reference(
            path, entities, entity_name, 0, field, data)
        self.assertEqual(resolved_count, 3)

    def test_resolve_source_reference__nested_schema(self):
        data = EXAMPLE_DATA_FOR_NESTED_SCHEMA
        requirements = EXAMPLE_REQUIREMENTS_NESTED_SCHEMA
        entities = {'Nested': [{}, {}, {}]}
        entity_name = 'Nested'
        field = 'location.lat'
        path = requirements.get(entity_name, {}).get(field)
        resolved_count = extractor.resolve_source_reference(
            path, entities, entity_name, 0, field, data)
        self.assertEqual(resolved_count, 3)

    def test_keyed_object_partial_wildcard(self):
        data = EXAMPLE_PARTIAL_WILDCARDS
        bad_path = '$households[0].name*'  # missing '.' after $
        try:
            extractor.find_by_jsonpath(data, bad_path)
        except Exception:
            pass
        else:
            self.fail('Should have thrown an error')
        expected = [
            ('$.households[0].name*', 2),
            ('$.households[1].name*', 1),
            ('$.households[*].name*', 3),
            ('$.households[0].name1', 1),
            ('$.households[*].name1', 2)
        ]
        for path, matches in expected:
            self.assertEqual(len(extractor.find_by_jsonpath(data, path)), matches), (path, matches)

    def test_coercion(self):
        test_cases = [
            ('a', 'string', 'a'),
            ('true', 'boolean', True),
            ('True', 'boolean', True),
            ('T', 'boolean', True),
            ('0', 'boolean', True),
            (0, 'boolean', False),
            (1, 'string', '1'),
            ('1', 'json', 1),
            (1, 'int', 1),
            ('1', 'int', 1),
            ('1.00', 'float', 1.00),
            ('["a"]', 'json', ['a']),
            ('{"hold": ["a"]}', 'json', {'hold': ['a']})
        ]
        for t in test_cases:
            res = extractor.coerce(t[0], t[1])
            self.assertTrue(res == t[2])
        try:
            extractor.coerce('a_string', 'float')
        except ValueError:
            pass
        else:
            self.fail('Should have thrown an error')

    def test_action_none(self):
        self.assertTrue(extractor.action_none() is None)

    def test_action_constant(self):
        args = ['154', 'int']
        self.assertTrue(extractor.action_constant(args) == 154)
        self.assertTrue(extractor.action_constant(['154']) == '154')
        try:
            extractor.action_constant(['a', 'bad_type'])
        except ValueError:
            pass
        else:
            self.fail('Should have thrown a type error on unsupported type')

    def test_anchor_references(self):
        source_data = EXAMPLE_NESTED_SOURCE_DATA
        source = 'data.houses[*].people[*]'
        context = 'data.houses[*]'
        instance_number = 5
        idx = extractor.anchor_reference(
            source, context, source_data, instance_number)
        self.assertEqual(idx, 1), 'Person #5 be found in second house, index @ 1'

    def test_get_or_make_uuid(self):
        entity_type = 'Person'
        field_name = '_id'
        instance_number = 0
        source_data = EXAMPLE_SOURCE_DATA
        # first time
        _id_1 = str(extractor.get_or_make_uuid(
            entity_type, field_name, instance_number, source_data, '#testing#'))
        self.assertEqual(_id_1.count('-'), 4)
        # second time
        _id_2 = str(extractor.get_or_make_uuid(
            entity_type, field_name, instance_number, source_data, '#testing#'))
        self.assertEqual(_id_1, _id_2)
        # another time but different mapping
        _id_3 = str(extractor.get_or_make_uuid(
            entity_type, field_name, instance_number, source_data, '#another#'))
        self.assertNotEqual(_id_1, _id_3)

    def test_get_or_make_uuid__old_version(self):
        entity_type = 'Person'
        field_name = '_id'
        instance_number = 0
        old_id = str(uuid.uuid4())
        source_data = {
            **EXAMPLE_SOURCE_DATA,
            extractor.ENTITY_EXTRACTION_ENRICHMENT: {
                entity_type: {field_name: [old_id]}
            }
        }
        _id = str(extractor.get_or_make_uuid(
            entity_type, field_name, instance_number, source_data, '#testing#'))
        self.assertEqual(_id, old_id)

    def test_extractor_action__entity_reference(self):
        source_path = '#!entity-reference#bad-reference'
        try:
            extractor.extractor_action(
                source_path, None, None, None, None, None, None)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

    def test_extractor_action__none(self):
        source_path = '#!none'
        res = extractor.extractor_action(
            source_path, None, None, None, None, None, None)
        self.assertEqual(res, None)

    def test_extractor_action__constant(self):
        source_path = '#!constant#1#int'
        res = extractor.extractor_action(
            source_path, None, None, None, None, None, None)
        self.assertEqual(res, 1)

    def test_extractor_action__missing(self):
        source_path = '#!undefined#1#int'
        try:
            extractor.extractor_action(
                source_path, None, None, None, None, None, None)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

    def test_extract_entity(self):
        requirements = EXAMPLE_REQUIREMENTS
        response_data = EXAMPLE_SOURCE_DATA
        entity_definitions = EXAMPLE_ENTITY_DEFINITION
        expected_entity = EXAMPLE_ENTITY
        entities = {'Person': []}
        entity_name = 'Person'
        entity_stub = extractor.get_entity_stub(
            requirements, entity_definitions, entity_name, response_data
        )
        failed_actions = extractor.extract_entity(
            entity_name, entities, requirements, response_data, entity_stub, '#testing#'
        )
        self.assertEqual(
            len(expected_entity['Person']), len(entities['Person']))
        self.assertEqual(len(failed_actions), 0)

    def test_extract_entities(self):
        '''
        Assert that the number of extracted entities equals the
        number of Persons in the source data.
        '''
        requirements = EXAMPLE_REQUIREMENTS
        response_data = EXAMPLE_SOURCE_DATA
        entity_stubs = EXAMPLE_ENTITY_DEFINITION
        schemas = {'Person': EXAMPLE_SCHEMA}
        submission_data, entities = extractor.extract_entities(
            requirements,
            response_data,
            entity_stubs,
            schemas,
            '#testing#',
        )
        expected_entity = EXAMPLE_ENTITY
        self.assertEqual(
            len(expected_entity['Person']), len(entities['Person']))

    def test_extract_create_entities__no_requirements(self):
        '''
        If the mapping contains neither paths nor entity references, no
        entities can be extracted.
        '''
        submission_payload = EXAMPLE_SOURCE_DATA
        mapping_definition = {'mapping': [], 'entities': {}}
        schemas = {}
        submission_data, entities = extractor.extract_create_entities(
            submission_payload,
            mapping_definition,
            schemas,
            '#testing#',
        )
        submission_errors = submission_data.get(extractor.ENTITY_EXTRACTION_ERRORS, [])
        self.assertEqual(len(submission_errors), 0)
        self.assertEqual(len(entities), 0)

    def test_extract_create_entities__success(self):
        '''
        Assert that no errors are accumulated and that the
        extracted entities are of the expected type.
        '''
        submission_payload = EXAMPLE_SOURCE_DATA
        mapping_definition = EXAMPLE_MAPPING
        schemas = {'Person': EXAMPLE_SCHEMA}
        mapping_id = '#testing#'
        submission_data, entities = extractor.extract_create_entities(
            submission_payload,
            mapping_definition,
            schemas,
            mapping_id,
        )
        submission_errors = submission_data.get(extractor.ENTITY_EXTRACTION_ERRORS, [])
        self.assertEqual(len(submission_errors), 0)
        self.assertTrue(len(entities) > 0)
        for entity in entities:
            self.assertIn(entity.schemadecorator_name, schemas.keys())
            self.assertEqual(entity.status, 'Publishable')
            self.assertEqual(entity.id, entity.payload['id'])

        # generated "id" saved for re-extractions
        self.assertEqual(
            submission_data[extractor.ENTITY_EXTRACTION_ENRICHMENT],
            {f'mapping:{mapping_id}': {'Person': {'id': [e.id for e in entities]}}}
        )

    def test_extract_create_entities__enrichment(self):
        '''
        Assert that in case of re-extraction the
        extracted entities have the same ids as the time before
        for the same mappings.
        '''
        submission_payload = {
            'parents': [
                {'name': 'Father'},
                {'name': 'Mother'}
            ],
            'children': [
                {'name': 'Boy'},
                {'name': 'Girl'},
            ],
        }
        mapping_definition = {
            'entities': {
                'Parent': '1',
                'Child': '2',
            },
            'mapping': [
                ['#!uuid', 'Parent.id'],
                ['parents[*].name', 'Parent.name'],
                ['#!uuid', 'Child.id'],
                ['children[*].name', 'Child.name'],
            ],
        }
        person_schema = {
            'name': 'Person',
            'type': 'record',
            'fields': [
                {'name': 'id', 'type': 'string'},
                {'name': 'name', 'type': ['null', 'string']},
            ],
        }
        schemas = {'Parent': person_schema, 'Child': person_schema}

        mapping_id = '#testing#'
        submission_data, entities = extractor.extract_create_entities(
            submission_payload,
            mapping_definition,
            schemas,
            mapping_id,
        )

        submission_errors = submission_data.get(extractor.ENTITY_EXTRACTION_ERRORS, [])
        self.assertEqual(len(submission_errors), 0)
        self.assertEqual(len(entities), 4)

        # generated "id" saved for re-extractions
        enrichment = submission_data[extractor.ENTITY_EXTRACTION_ENRICHMENT]
        self.assertEqual(len(enrichment[f'mapping:{mapping_id}']['Parent']['id']), 2)
        self.assertEqual(len(enrichment[f'mapping:{mapping_id}']['Child']['id']), 2)
        self.assertNotEqual(
            enrichment[f'mapping:{mapping_id}']['Parent']['id'],
            enrichment[f'mapping:{mapping_id}']['Child']['id'],
        )

        # second round
        submission_data_2, entities_2 = extractor.extract_create_entities(
            submission_payload,
            mapping_definition,
            schemas,
            mapping_id,
        )
        self.assertEqual(entities, entities_2)
        enrichment_2 = submission_data_2[extractor.ENTITY_EXTRACTION_ENRICHMENT]
        self.assertEqual(enrichment, enrichment_2)

        # third round, different mapping
        submission_data_3, entities_3 = extractor.extract_create_entities(
            submission_payload,
            mapping_definition,
            schemas,
            '#another#',
        )
        self.assertNotEqual(entities, entities_3)
        enrichment_3 = submission_data_2[extractor.ENTITY_EXTRACTION_ENRICHMENT]
        self.assertEqual(enrichment, enrichment_3)

    def test_extract_create_entities__old_enrichment(self):
        '''
        Assert that old enrichment formats are migrated to new format.
        '''
        old_enrichment = {
            'Parent': {'id': [str(uuid.uuid4()), str(uuid.uuid4())]},
            'Child': {'id': [str(uuid.uuid4()), str(uuid.uuid4())]},
            'Another': {'id': [str(uuid.uuid4()), str(uuid.uuid4())]},
        }
        submission_payload = {
            'parents': [
                {'name': 'Father'},
                {'name': 'Mother'}
            ],
            'children': [
                {'name': 'Boy'},
                {'name': 'Girl'},
            ],
            extractor.ENTITY_EXTRACTION_ENRICHMENT: dict(old_enrichment),
        }
        mapping_definition = {
            'entities': {
                'Parent': '1',
                'Child': '2',
            },
            'mapping': [
                ['#!uuid', 'Parent.id'],
                ['parents[*].name', 'Parent.name'],
                ['#!uuid', 'Child.id'],
                ['children[*].name', 'Child.name'],
            ],
        }
        person_schema = {
            'name': 'Person',
            'type': 'record',
            'fields': [
                {'name': 'id', 'type': 'string'},
                {'name': 'name', 'type': ['null', 'string']},
            ],
        }
        schemas = {'Parent': person_schema, 'Child': person_schema}

        mapping_id = '#testing#'
        submission_data, entities = extractor.extract_create_entities(
            submission_payload,
            mapping_definition,
            schemas,
            mapping_id,
        )

        new_enrichment = submission_data[extractor.ENTITY_EXTRACTION_ENRICHMENT]
        self.assertNotIn('Parent', new_enrichment)
        self.assertEqual(new_enrichment[f'mapping:{mapping_id}']['Parent'], old_enrichment['Parent'])
        self.assertNotIn('Child', new_enrichment)
        self.assertEqual(new_enrichment[f'mapping:{mapping_id}']['Child'], old_enrichment['Child'])
        self.assertIn('Another', new_enrichment, 'no migrated yet')
        self.assertEqual(new_enrichment['Another'], old_enrichment['Another'])

    def test_extract_create_entities__multiple(self):
        '''
        Assert that different mappings don't share IDs.
        '''
        submission_payload = {
            'parents': [
                {'name': 'Father'},
                {'name': 'Mother'}
            ],
            'children': [
                {'name': 'Boy'},
                {'name': 'Girl'},
            ],
        }
        person_schema = {
            'name': 'Person',
            'type': 'record',
            'fields': [
                {'name': 'id', 'type': 'string'},
                {'name': 'name', 'type': ['null', 'string']},
            ],
        }
        schemas = {'Person': person_schema}

        parent_definition = {
            'entities': {
                'Person': '1',
            },
            'mapping': [
                ['#!uuid', 'Person.id'],
                ['parents[*].name', 'Person.name'],
            ],
        }
        child_definition = {
            'entities': {
                'Person': '1',
            },
            'mapping': [
                ['#!uuid', 'Person.id'],
                ['children[*].name', 'Person.name'],
            ],
        }

        __, parents = extractor.extract_create_entities(
            submission_payload,
            parent_definition,
            schemas,
            '#testing-parent#',
        )

        __, children = extractor.extract_create_entities(
            submission_payload,
            child_definition,
            schemas,
            '#testing-child#',
        )

        self.assertNotEqual(
            [p.id for p in parents],
            [c.id for c in children],
        )

        enrichment = submission_payload[extractor.ENTITY_EXTRACTION_ENRICHMENT]
        self.assertIn('Person', enrichment['mapping:#testing-parent#'])
        self.assertIn('Person', enrichment['mapping:#testing-child#'])
        self.assertNotEqual(
            enrichment['mapping:#testing-parent#']['Person'],
            enrichment['mapping:#testing-child#']['Person'],
        )

    def test_extract_create_entities__validation_error(self):
        '''
        Assert that validation errors are accumulated and that they contain
        information about the non-validating entities.
        '''
        submission_payload = EXAMPLE_SOURCE_DATA
        mapping_definition = EXAMPLE_MAPPING
        # This schema shares the field names `id` and `name` with
        # EXAMPLE_SCHEMA. The field types differ though, so we should expect a
        # validation error to occur during entity extraction.
        error_count = 2
        schema = {
            'type': 'record',
            'name': 'Test',
            'fields': [
                {
                    'name': 'id',
                    'type': 'int',  # error 1
                },
                {
                    'name': 'name',  # error 2
                    'type': {
                        'type': 'enum',
                        'name': 'Name',
                        'symbols': ['John', 'Jane'],
                    }
                },
            ]
        }
        schemas = {'Person': schema}
        submission_data, entities = extractor.extract_create_entities(
            submission_payload,
            mapping_definition,
            schemas,
            '#testing#',
        )
        submission_errors = submission_data.get(extractor.ENTITY_EXTRACTION_ERRORS, [])
        self.assertEqual(
            len(submission_errors),
            len(EXAMPLE_SOURCE_DATA['data']['people']) * error_count,
        )
        self.assertEqual(len(entities), 0)

    def test_extract_create_entities__error_not_a_uuid(self):
        submission_payload = {'id': 'not-a-uuid', 'a': 1}
        mapping_definition = {
            'entities': {'Test': str(uuid.uuid4())},
            'mapping': [
                ['$.id', 'Test.id'],
                ['$.a', 'Test.b'],
            ],
        }
        schema = {
            'type': 'record',
            'name': 'Test',
            'fields': [
                {
                    'name': 'id',
                    'type': 'string',
                },
                {
                    'name': 'b',
                    'type': 'int',
                },
            ],
        }
        schemas = {'Test': schema}
        submission_data, entities = extractor.extract_create_entities(
            submission_payload,
            mapping_definition,
            schemas,
            '#testing#',
        )
        submission_errors = submission_data.get(extractor.ENTITY_EXTRACTION_ERRORS, [])
        self.assertEqual(len(entities), 0)
        self.assertEqual(len(submission_errors), 1)
        self.assertIn('is not a valid uuid',
                      submission_errors[0]['description'])

    def test_is_not_custom_jsonpath(self):
        # Examples taken from https://github.com/json-path/JsonPath#path-examples
        example_paths = [
            '$.store.book[*].author',
            '$..author',
            '$.store.*',
            '$.store..price',
            '$..book[2]',
            '$..book[-2]',
            '$..book[0,1]',
            '$..book[:2]',
            '$..book[1:2]',
            '$..book[-2:]',
            '$..book[2:]',
            '$..book[?(@.isbn)]',
            '$.store.book[?(@.price < 10)]',
            '$..book[?(@.price <= $["expensive"])]'
            '$..book[?(@.author =~ /.*REES/i)]'
            '$..*',
            '$..book.length()',
        ]
        for path in example_paths:
            result = extractor.CUSTOM_JSONPATH_WILDCARD_REGEX.match(path)
            self.assertIsNone(result)

    def test_find_by_jsonpath__no_match(self):
        obj = {}
        res = [i for i in extractor.find_by_jsonpath(obj, 'some.missing.path')]
        assert(not res)

    def test_find_by_jsonpath__filter_by_prefix(self):
        obj = {
            'dose-1': {
                'id': 1,
            },
            'dose-2': {
                'id': 2,
            },
            'person-1': {
                'id': 3,
            },
        }
        expected = set([1, 2])
        path = '$.dose-*.id'
        result = set([x.value for x in extractor.find_by_jsonpath(obj, path)])
        self.assertEqual(expected, result)

    def test_find_by_jsonpath__filter_by_prefix_nested_base(self):
        obj = {
            'data': {
                'dose-1': {
                    'id': 1,
                },
                'dose-2': {
                    'id': 2,
                },
                'person-1': {
                    'id': 3,
                },
            }
        }
        expected = set([1, 2])
        path = '$.data.dose-*.id'
        result = set([x.value for x in extractor.find_by_jsonpath(obj, path)])
        self.assertEqual(expected, result)

    def test_find_by_jsonpath__nested(self):
        obj = {
            'dose-1': {
                'id': 1,
            },
            'dose-2': {
                'id': 2,
            },
            'person-1': {
                'id': 3,
                'household': {
                    'id': 4,
                },
            },
        }
        expected = set([4])
        path = '$.person-*.household.id'
        result = set([x.value for x in extractor.find_by_jsonpath(obj, path)])
        self.assertEqual(expected, result)

    def test_find_by_jsonpath__fallback_to_jsonpath_ng(self):
        obj = {
            'dose-1': {
                'id': 1,
            },
            'dose-2': {
                'id': 2,
            },
            'person-1': {
                'id': 3,
            },
        }
        expected = set([1, 2, 3])
        path = '$.*.id'
        result = set([x.value for x in extractor.find_by_jsonpath(obj, path)])
        self.assertEqual(expected, result)

    def test_find_by_jsonpath__fallback_array(self):
        obj = {
            'households': [
                {
                    'id': 1,
                },
                {
                    'id': 2,
                },
                {
                    'id': 3,
                },
            ]
        }
        expected = set([1, 2, 3])
        path = '$.households[*].id'
        result = set([x.value for x in extractor.find_by_jsonpath(obj, path)])
        self.assertEqual(expected, result)
