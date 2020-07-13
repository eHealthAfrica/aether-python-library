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

TENANT = 'test'
MAPPINGSET_ID = '41282431-50bb-4309-92bf-ef9359494dc6'
PAYLOAD = {
    'id': 'a5336669-605c-4a65-ab4c-c0318e28115b',
    'staff': {
        'nurse': 40,
        'doctor': 15
    },
    'patient': {
        'name': 'Nancy William',
        'patient_id': 'c55021d0-cc34-46ba-ac5b-4cd5bcbde3f9'
    },
    'opening_hour': '7AM working days',
    'facility_name': 'Primary Health Care Abuja'
}
MAPPINGSET = {
    'id': MAPPINGSET_ID,
    'name': 'Dummy',
    'schema': {
        'name': 'Dummy',
        'type': 'record',
        'fields': [
            {
                'name': 'id',
                'type': 'string'
            },
            {
                'name': 'facility_name',
                'type': 'string'
            },
            {
                'name': 'staff',
                'type': {
                    'name': 'Auto_1',
                    'type': 'record',
                    'fields': [
                        {
                            'name': 'doctor',
                            'type': 'int'
                        },
                        {
                            'name': 'nurse',
                            'type': 'int'
                        }
                    ]
                }
            },
            {
                'name': 'opening_hour',
                'type': 'string'
            },
            {
                'name': 'patient',
                'type': {
                    'name': 'Auto_2',
                    'type': 'record',
                    'fields': [
                        {
                            'name': 'patient_id',
                            'type': 'string'
                        },
                        {
                            'name': 'name',
                            'type': 'string'
                        }
                    ]
                }
            }
        ]
    },
    'input': PAYLOAD
}

MAPPINGS = [
    {
        'id': '0d4a9cc6-291c-4f9a-a409-1ba87cc93c57',
        'mappingset': MAPPINGSET_ID,
        'revision': '1',
        'name': 'passthrough',
        'definition': {
            'mapping': [
                [
                    '$.id',
                    'Pass.id'
                ],
                [
                    '$.facility_name',
                    'Pass.facility_name'
                ],
                [
                    '$.staff',
                    'Pass.staff'
                ],
                [
                    '$.opening_hour',
                    'Pass.opening_hour'
                ],
                [
                    '$.patient',
                    'Pass.patient'
                ]
            ],
            'entities': {
                'Pass': 'cc3e081a-e802-47eb-a5ea-f1c056737453'
            }
        },
        'is_active': True,
        'is_read_only': False,
        'schemadecorators': [
            'cc3e081a-e802-47eb-a5ea-f1c056737453'
        ]
    },
    {
        'id': '3ae8649f-2d5d-4703-82d3-94baaee4914e',
        'mappingset': MAPPINGSET_ID,
        'revision': '1',
        'name': 'crossthrough',
        'definition': {
            'mapping': [
                [
                    '#!uuid',
                    'Facility.id'
                ],
                [
                    '$.patient.patient_id',
                    'Patient.id'
                ],
                [
                    '$.patient.name',
                    'Patient.name'
                ],
                [
                    '$.facility_name',
                    'Facility.name'
                ],
                [
                    '$.staff.doctor + $.staff.nurse',
                    'Facility.staff'
                ]
            ],
            'entities': {
                'Patient': '134a750e-913b-458f-80a1-394c03a64ba5',
                'Facility': '92ac6021-cc1d-47fa-95a0-3e497125c538'
            }
        },
        'is_active': True,
        'is_read_only': False,
        'schemadecorators': [
            '134a750e-913b-458f-80a1-394c03a64ba5',
            '92ac6021-cc1d-47fa-95a0-3e497125c538'
        ]
    }
]

SCHEMA_DECORATORS = [
    {
        'id': 'cc3e081a-e802-47eb-a5ea-f1c056737453',
        'schema_definition': {
            'name': 'Pass',
            'type': 'record',
            'fields': [
                {
                    'name': 'id',
                    'type': 'string'
                },
                {
                    'name': 'facility_name',
                    'type': [
                        'null',
                        'string'
                    ]
                },
                {
                    'name': 'staff',
                    'type': [
                        'null',
                        {
                            'name': 'Auto_1',
                            'type': 'record',
                            'fields': [
                                {
                                    'name': 'doctor',
                                    'type': 'int'
                                },
                                {
                                    'name': 'nurse',
                                    'type': 'int'
                                }
                            ]
                        }
                    ]
                },
                {
                    'name': 'opening_hour',
                    'type': [
                        'null',
                        'string'
                    ]
                },
                {
                    'name': 'patient',
                    'type': [
                        'null',
                        {
                            'name': 'Auto_2',
                            'type': 'record',
                            'fields': [
                                {
                                    'name': 'patient_id',
                                    'type': 'string'
                                },
                                {
                                    'name': 'name',
                                    'type': 'string'
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        'name': 'Pass',
        'schema': 'cc3e081a-e802-47eb-a5ea-f1c056737453'
    },
    {
        'id': '134a750e-913b-458f-80a1-394c03a64ba5',
        'schema_definition': {
            'name': 'Patient',
            'type': 'record',
            'fields': [
                {
                    'name': 'id',
                    'type': 'string'
                },
                {
                    'name': 'name',
                    'type': [
                        'null',
                        'string'
                    ]
                }
            ]
        },
        'name': 'Patient',
        'schema': '134a750e-913b-458f-80a1-394c03a64ba5'
    },
    {
        'id': '92ac6021-cc1d-47fa-95a0-3e497125c538',
        'schema_definition': {
            'name': 'Facility',
            'type': 'record',
            'fields': [
                {
                    'name': 'id',
                    'type': 'string'
                },
                {
                    'name': 'name',
                    'type': [
                        'null',
                        'string'
                    ]
                },
                {
                    'name': 'staff',
                    'type': [
                        'null',
                        'int'
                    ]
                }
            ]
        },
        'name': 'Facility',
        'schema': '92ac6021-cc1d-47fa-95a0-3e497125c538'
    }
]

SCHEMAS = [
    {
        'id': 'cc3e081a-e802-47eb-a5ea-f1c056737453',
        'revision': '1',
        'name': 'Pass',
        'definition': {
            'name': 'Pass',
            'type': 'record',
            'fields': [
                {
                    'name': 'id',
                    'type': 'string'
                },
                {
                    'name': 'facility_name',
                    'type': [
                        'null',
                        'string'
                    ]
                },
                {
                    'name': 'staff',
                    'type': [
                        'null',
                        {
                            'name': 'Auto_1',
                            'type': 'record',
                            'fields': [
                                {
                                    'name': 'doctor',
                                    'type': 'int'
                                },
                                {
                                    'name': 'nurse',
                                    'type': 'int'
                                }
                            ]
                        }
                    ]
                },
                {
                    'name': 'opening_hour',
                    'type': [
                        'null',
                        'string'
                    ]
                },
                {
                    'name': 'patient',
                    'type': [
                        'null',
                        {
                            'name': 'Auto_2',
                            'type': 'record',
                            'fields': [
                                {
                                    'name': 'patient_id',
                                    'type': 'string'
                                },
                                {
                                    'name': 'name',
                                    'type': 'string'
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        'family': None
    },
    {
        'id': '134a750e-913b-458f-80a1-394c03a64ba5',
        'revision': '1',
        'name': 'Patient',
        'definition': {
            'name': 'Patient',
            'type': 'record',
            'fields': [
                {
                    'name': 'id',
                    'type': 'string'
                },
                {
                    'name': 'name',
                    'type': [
                        'null',
                        'string'
                    ]
                }
            ]
        },
        'family': None
    },
    {
        'id': '92ac6021-cc1d-47fa-95a0-3e497125c538',
        'revision': '1',
        'name': 'Facility',
        'definition': {
            'name': 'Facility',
            'type': 'record',
            'fields': [
                {
                    'name': 'id',
                    'type': 'string'
                },
                {
                    'name': 'name',
                    'type': [
                        'null',
                        'string'
                    ]
                },
                {
                    'name': 'staff',
                    'type': [
                        'null',
                        'int'
                    ]
                }
            ]
        },
        'family': None
    }
]
SUBMISSION = {
    'mappingset': MAPPINGSET_ID,
    'payload': PAYLOAD,
    'mappings': [
        '0d4a9cc6-291c-4f9a-a409-1ba87cc93c57',
        '3ae8649f-2d5d-4703-82d3-94baaee4914e'
    ]
}

EXAMPLE_SCHEMA = {
    'extends': 'http://ehealthafrica.org/#CouchDoc',
    'type': 'record',
    'name': 'Person',
    'aetherBaseSchema': True,
    'fields': [
        {
            'jsonldPredicate': '@id',
            'type': 'string',
            'name': 'id',
            'doc': 'ID',
            'inherited_from': 'http://ehealthafrica.org/#CouchDoc',
        },
        {
            'type': [
                'null',
                'string',
            ],
            'name': '_rev',
            'doc': 'REVISION',
            'inherited_from': 'http://ehealthafrica.org/#CouchDoc',
        },
        {
            'type': [
                'null',
                'string',
                {
                    'type': 'array',
                    'items': 'string',
                }
            ],
            'name': 'name',
            'doc': 'NAME',
        },
        {
            'type': 'string',
            'name': 'dob',
        },
        {
            'jsonldPredicate': {
                '_type': '@id',
                '_id': 'http://ehealthafrica.org/#Village',
            },
            'type': 'string',
            'name': 'villageID',
            'doc': 'VILLAGE',
        },
    ],
}

NESTED_ARRAY_SCHEMA = {
    'fields': [
        {
            'name': 'id',
            'type': 'string'
        },
        {
            'name': 'geom',
            'namespace': 'Test',
            'type': {
                'fields': [
                    {
                        'name': 'coordinates',
                        'namespace': 'Test.geom',
                        'type': {
                            'items': 'float',
                            'type': 'array'
                        }
                    },
                    {
                        'name': 'type',
                        'namespace': 'Test.geom',
                        'type': 'string'
                    }
                ],
                'name': 'geom',
                'namespace': 'Test',
                'type': 'record'
            }
        }
    ],
    'name': 'Test',
    'namespace': 'org.eha.Test',
    'type': 'record'
}

EXAMPLE_MAPPING = {
    'entities': {
        'Person': '1',
    },
    'mapping': [
        ['#!uuid', 'Person.id'],
        ['data.village', 'Person.villageID'],
        ['data.people[*].name', 'Person.name'],
        ['data.people[*].dob', 'Person.dob'],
    ],
}

EXAMPLE_MAPPING_EDGE = {
    'entities': {
        'Person': '1',
    },
    'mapping': [
        ['#!uuid', 'Person.id'],
        ['[*].village', 'Person.villageID'],
        ['$[*].name', 'Person.name'],
        ['$.data.people[*].dob', 'Person.dob.nested'],
    ],
}

EXAMPLE_SOURCE_DATA = {
    'data': {
        'village': 'somevillageID',
        'people': [
            {
                'name': 'PersonA',
                'dob': '2000-01-01',
            },
            {
                'name': 'PersonB',
                'dob': '2001-01-01',
            },
            {
                'name': ['FirstC', 'MiddleC', 'LastC'],
                'dob': '2002-01-01',
            },
        ],
    },
}

EXAMPLE_DATA_FOR_NESTED_SCHEMA = [
    {
        'name': 'a',
        'lat': 10,
        'lng': 20
    },
    {
        'name': 'b',
        'lat': 11,
        'lng': 21
    },
    {
        'name': 'c',
        'lat': 12,
        'lng': 22
    },
]

EXAMPLE_REQUIREMENTS_NESTED_SCHEMA = {
    'Nested': {
        'name': '[*].name',
        'location.lat': '[*].lat',
        'location.lng': '[*].lng'
    }
}

EXAMPLE_NESTED_SOURCE_DATA = {
    'data': {
        'village': 'somevillageID',
        'houses': [
            {
                'num': 0,
                'people': [
                    {
                        'name': 'PersonA',
                        'dob': '2000-01-01',
                    },
                    {
                        'name': 'PersonB',
                        'dob': '2001-01-01',
                    },
                    {
                        'name': ['FirstC', 'MiddleC', 'LastC'],
                        'dob': '2002-01-01',
                    },
                ],
            },
            {
                'num': 1,
                'people': [
                    {
                        'name': 'PersonD',
                        'dob': '2000-01-01',
                    },
                    {
                        'name': 'PersonE',
                        'dob': '2001-01-01',
                    },
                    {
                        'name': 'PersonF',
                        'dob': '2002-01-01',
                    },
                ],
            },
        ],
    },
}

EXAMPLE_REQUIREMENTS = {
    'Person': {
        'id': ['#!uuid'],
        'name': ['data.people[*].name'],
        'dob': ['data.people[*].dob'],
        'villageID': ['data.village'],
    },
}

EXAMPLE_REQUIREMENTS_ARRAY_BASE = {
    'Person': {
        'id': ['#!uuid'],
        'name': ['[*].name'],
        'dob': ['[*].dob'],
        'villageID': ['[*].village']
    }
}

EXAMPLE_ENTITY_DEFINITION = {
    'Person': [
        'id', '_rev', 'name', 'dob', 'villageID'
    ]
}

EXAMPLE_FIELD_MAPPINGS = [
    ['#!uuid', 'Person.id'],
    ['data.village', 'Person.villageID'],
    ['data.people[*].name', 'Person.name'],
    ['data.people[*].dob', 'Person.dob'],
]

EXAMPLE_FIELD_MAPPINGS_EDGE = [
    ['#!uuid', 'Person.id'],
    ['[*].village', 'Person.villageID'],
    ['$[*].name', 'Person.name'],
    ['$.data.people[*].dob', 'Person.dob.nested']
]

EXAMPLE_ENTITY = {
    'Person': [
        {
            'id': '1d119b5d-ca71-4f03-a061-1481e1a694ea',
            'name': 'PersonA',
            'dob': '2000-01-01',
            'villageID': 'somevillageID',
        },
        {
            'id': '5474b768-92d9-431f-bf90-3c6db1788109',
            'name': 'PersonB',
            'dob': '2001-01-01',
            'villageID': 'somevillageID',
        },
        {
            'id': '64d30f72-c15e-4476-9522-d26cb036c73b',
            'name': ['FirstC', 'MiddleC', 'LastC'],
            'dob': '2002-01-01',
            'villageID': 'somevillageID',
        },
    ],
}

EXAMPLE_FIELD_MAPPINGS_ARRAY_BASE = [
    ['#!uuid', 'Person.id'],
    ['[*].village', 'Person.villageID'],
    ['[*].name', 'Person.name'],
    ['[*].dob', 'Person.dob'],
]

EXAMPLE_PARTIAL_WILDCARDS = {
    'households': [
        {
            'address': '74 Whyioughta St.',
            'name1': 'Larry',
            'number1': 1,
            'name2': 'Curly',
            'number2': 2
        },
        {
            'address': '1600 Ipoke Ave',
            'name1': 'Moe',
            'number1': 3
        }
    ]
}

EXAMPLE_SIMPLE_SCHEMA = {
    'name': 'rapidtest',
    'doc': 'Rapid Test - Start (id: rapidtest_start, version: 2019012807)',
    'type': 'record',
    'fields': [
        {
            'default': 'rapidtest_start',
            'doc': 'xForm ID',
            'name': '_id',
            'namespace': 'Rapidtest_Start_2019012807',
            'type': [
                'null',
                'string'
            ]
        },
        {
            'default': '2019012807',
            'doc': 'xForm version',
            'name': '_version',
            'namespace': 'Rapidtest_Start_2019012807',
            'type': [
                'null',
                'string'
            ]
        },
        {
            'name': 'start',
            'namespace': 'Rapidtest_Start_2019012807',
            'type': [
                'null',
                'string'
            ]
        },
        {
            'name': 'end',
            'namespace': 'Rapidtest_Start_2019012807',
            'type': [
                'null',
                'string'
            ]
        },
        {
            'doc': 'Test Name',
            'name': 'Test_Name',
            'namespace': 'Rapidtest_Start_2019012807',
            'type': [
                'null',
                'string'
            ]
        },
        {
            'doc': 'Scan QR Code',
            'name': 'QR_Code',
            'namespace': 'Rapidtest_Start_2019012807',
            'type': [
                'null',
                'string'
            ]
        },
        {
            'doc': 'Patient Name',
            'name': 'Patient_Name',
            'namespace': 'Rapidtest_Start_2019012807',
            'type': [
                'null',
                'string'
            ]
        },
        {
            'doc': 'Patient Age',
            'name': 'Patient_Age',
            'namespace': 'Rapidtest_Start_2019012807',
            'type': [
                'null',
                'int'
            ]
        },
        {
            'doc': 'Location',
            'name': 'Location',
            'namespace': 'Rapidtest_Start_2019012807',
            'type': [
                'null',
                {
                    'doc': 'Location',
                    'fields': [
                        {
                            'doc': 'latitude',
                            'name': 'latitude',
                            'namespace': 'Rapidtest_Start_2019012807.Location',
                            'type': [
                                'null',
                                'float'
                            ]
                        },
                        {
                            'doc': 'longitude',
                            'name': 'longitude',
                            'namespace': 'Rapidtest_Start_2019012807.Location',
                            'type': [
                                'null',
                                'float'
                            ]
                        },
                        {
                            'doc': 'altitude',
                            'name': 'altitude',
                            'namespace': 'Rapidtest_Start_2019012807.Location',
                            'type': [
                                'null',
                                'float'
                            ]
                        },
                        {
                            'doc': 'accuracy',
                            'name': 'accuracy',
                            'namespace': 'Rapidtest_Start_2019012807.Location',
                            'type': [
                                'null',
                                'float'
                            ]
                        }
                    ],
                    'name': 'Location',
                    'namespace': 'Rapidtest_Start_2019012807',
                    'type': 'record'
                }
            ]
        },
        {
            'name': 'Encounter_Date_Time',
            'namespace': 'Rapidtest_Start_2019012807',
            'type': [
                'null',
                'string'
            ]
        },
        {
            'name': 'meta',
            'namespace': 'Rapidtest_Start_2019012807',
            'type': [
                'null',
                {
                    'fields': [
                        {
                            'name': 'instanceID',
                            'namespace': 'Rapidtest_Start_2019012807.meta',
                            'type': [
                                'null',
                                'string'
                            ]
                        }
                    ],
                    'name': 'meta',
                    'namespace': 'Rapidtest_Start_2019012807',
                    'type': 'record'
                }
            ]
        },
        {
            'doc': 'UUID',
            'name': 'id',
            'type': 'string'
        }
    ]
}


EXAMPLE_ANNOTATED_SCHEMA = {
    'doc': 'MySurvey (title: HS OSM Gather Test id: gth_hs_test, version: 2)',
    'name': 'MySurvey',
    'type': 'record',
    'fields': [
        {
            'doc': 'xForm ID',
            'name': '_id',
            'type': [
                'null',
                'string'
            ],
            'namespace': 'MySurvey'
        },
        {
            'doc': 'xForm version',
            'name': '_version',
            'type': [
                'null',
                'string'
            ],
            'namespace': 'MySurvey',
            '@aether_default_visualization': 'undefined'
        },
        {
            'doc': 'Surveyor',
            'name': '_surveyor',
            'type': [
                'null',
                'string'
            ],
            'namespace': 'MySurvey'
        },
        {
            'doc': 'Submitted at',
            'name': '_submitted_at',
            'type': [
                'null',
                'string'
            ],
            'namespace': 'MySurvey',
            '@aether_extended_type': 'dateTime'
        },
        {
            'name': '_start',
            'type': [
                'null',
                'string'
            ],
            'namespace': 'MySurvey',
            '@aether_extended_type': 'dateTime'
        },
        {
            'name': 'timestamp',
            'type': [
                'null',
                'string'
            ],
            'namespace': 'MySurvey',
            '@aether_extended_type': 'dateTime'
        },
        {
            'name': 'username',
            'type': [
                'null',
                'string'
            ],
            'namespace': 'MySurvey',
            '@aether_extended_type': 'string'
        },
        {
            'name': 'source',
            'type': [
                'null',
                'string'
            ],
            'namespace': 'MySurvey',
            '@aether_extended_type': 'string'
        },
        {
            'name': 'osm_id',
            'type': [
                'null',
                'string'
            ],
            'namespace': 'MySurvey',
            '@aether_extended_type': 'string'
        },
        {
            'doc': 'Name of Facility',
            'name': 'name',
            'type': [
                'null',
                'string'
            ],
            'namespace': 'MySurvey',
            '@aether_extended_type': 'string'
        },
        {
            'doc': 'Address',
            'name': 'addr_full',
            'type': [
                'null',
                'string'
            ],
            'namespace': 'MySurvey',
            '@aether_extended_type': 'string'
        },
        {
            'doc': 'Phone Number',
            'name': 'contact_number',
            'type': [
                'null',
                'string'
            ],
            'namespace': 'MySurvey',
            '@aether_extended_type': 'string'
        },
        {
            'doc': 'Facility Operator Name',
            'name': 'operator',
            'type': [
                'null',
                'string'
            ],
            'namespace': 'MySurvey',
            '@aether_extended_type': 'string'
        },
        {
            'doc': 'Operator Type',
            'name': 'operator_type',
            'type': [
                'null',
                'string'
            ],
            'namespace': 'MySurvey',
            '@aether_default_visualization': 'pie',
            '@aether_lookup': [
                {
                    'label': 'Public',
                    'value': 'public'
                },
                {
                    'label': 'Private',
                    'value': 'private'
                },
                {
                    'label': 'Community',
                    'value': 'community'
                },
                {
                    'label': 'Religious',
                    'value': 'religious'
                },
                {
                    'label': 'Government',
                    'value': 'government'
                },
                {
                    'label': 'NGO',
                    'value': 'ngo'
                },
                {
                    'label': 'Combination',
                    'value': 'combination'
                }
            ],
            '@aether_extended_type': 'select1'
        },
        {
            'doc': 'Facility Location',
            'name': 'geometry',
            'type': [
                'null',
                {
                    'doc': 'Facility Location',
                    'name': 'geometry',
                    'type': 'record',
                    'fields': [
                        {
                            'doc': 'latitude',
                            'name': 'latitude',
                            'type': [
                                'null',
                                'float'
                            ],
                            'namespace': 'MySurvey.geometry'
                        },
                        {
                            'doc': 'longitude',
                            'name': 'longitude',
                            'type': [
                                'null',
                                'float'
                            ],
                            'namespace': 'MySurvey.geometry'
                        },
                        {
                            'doc': 'altitude',
                            'name': 'altitude',
                            'type': [
                                'null',
                                'float'
                            ],
                            'namespace': 'MySurvey.geometry'
                        },
                        {
                            'doc': 'accuracy',
                            'name': 'accuracy',
                            'type': [
                                'null',
                                'float'
                            ],
                            'namespace': 'MySurvey.geometry'
                        }
                    ],
                    'namespace': 'MySurvey',
                    '@aether_extended_type': 'geopoint'
                }
            ],
            'namespace': 'MySurvey',
            '@aether_extended_type': 'geopoint'
        },
        {
            'doc': 'Operational Status',
            'name': 'operational_status',
            'type': [
                'null',
                'string'
            ],
            'namespace': 'MySurvey',
            '@aether_default_visualization': 'pie',
            '@aether_lookup': [
                {
                    'label': 'Operational',
                    'value': 'operational'
                },
                {
                    'label': 'Non Operational',
                    'value': 'non_operational'
                },
                {
                    'label': 'Unknown',
                    'value': 'unknown'
                }
            ],
            '@aether_extended_type': 'select1'
        },
        {
            'doc': 'When is the facility open?',
            'name': '_opening_hours_type',
            'type': [
                'null',
                'string'
            ],
            'namespace': 'MySurvey',
            '@aether_lookup': [
                {
                    'label': 'Pick the days of the week open and enter hours for each day',
                    'value': 'oh_select'
                },
                {
                    'label': 'Only open on weekdays with the same hours every day.',
                    'value': 'oh_weekday'
                },
                {
                    'label': '24/7 - All day, every day',
                    'value': 'oh_24_7'
                },
                {
                    'label': 'Type in OSM String by hand (Advanced Option)',
                    'value': 'oh_advanced'
                },
                {
                    'label': 'I do not know the operating hours',
                    'value': 'oh_unknown'
                }
            ],
            '@aether_extended_type': 'select1'
        },
        {
            'doc': 'Which days is this facility open?',
            'name': '_open_days',
            'type': [
                'null',
                {
                    'type': 'array',
                    'items': 'string'
                }
            ],
            'namespace': 'MySurvey',
            '@aether_lookup': [
                {
                    'label': 'Monday',
                    'value': 'Mo'
                },
                {
                    'label': 'Tuesday',
                    'value': 'Tu'
                },
                {
                    'label': 'Wednesday',
                    'value': 'We'
                },
                {
                    'label': 'Thursday',
                    'value': 'Th'
                },
                {
                    'label': 'Friday',
                    'value': 'Fr'
                },
                {
                    'label': 'Saturday',
                    'value': 'Sa'
                },
                {
                    'label': 'Sunday',
                    'value': 'Su'
                },
                {
                    'label': 'Public Holidays',
                    'value': 'PH'
                }
            ],
            '@aether_extended_type': 'select'
        },
        {
            'doc': 'Open hours by day of the week',
            'name': '_dow_group',
            'type': [
                'null',
                {
                    'doc': 'Open hours by day of the week',
                    'name': '_dow_group',
                    'type': 'record',
                    'fields': [
                        {
                            'doc': 'Enter open hours for each day:',
                            'name': '_hours_note',
                            'type': [
                                'null',
                                'string'
                            ],
                            'namespace': 'MySurvey._dow_group',
                            '@aether_extended_type': 'string'
                        },
                        {
                            'doc': 'Monday open hours',
                            'name': '_mon_hours',
                            'type': [
                                'null',
                                'string'
                            ],
                            'namespace': 'MySurvey._dow_group',
                            '@aether_extended_type': 'string'
                        },
                        {
                            'doc': 'Tuesday open hours',
                            'name': '_tue_hours',
                            'type': [
                                'null',
                                'string'
                            ],
                            'namespace': 'MySurvey._dow_group',
                            '@aether_extended_type': 'string'
                        },
                        {
                            'doc': 'Wednesday open hours',
                            'name': '_wed_hours',
                            'type': [
                                'null',
                                'string'
                            ],
                            'namespace': 'MySurvey._dow_group',
                            '@aether_extended_type': 'string'
                        },
                        {
                            'doc': 'Thursday open hours',
                            'name': '_thu_hours',
                            'type': [
                                'null',
                                'string'
                            ],
                            'namespace': 'MySurvey._dow_group',
                            '@aether_extended_type': 'string'
                        },
                        {
                            'doc': 'Friday open hours',
                            'name': '_fri_hours',
                            'type': [
                                'null',
                                'string'
                            ],
                            'namespace': 'MySurvey._dow_group',
                            '@aether_extended_type': 'string'
                        },
                        {
                            'doc': 'Saturday open hours',
                            'name': '_sat_hours',
                            'type': [
                                'null',
                                'string'
                            ],
                            'namespace': 'MySurvey._dow_group',
                            '@aether_extended_type': 'string'
                        },
                        {
                            'doc': 'Sunday open hours',
                            'name': '_sun_hours',
                            'type': [
                                'null',
                                'string'
                            ],
                            'namespace': 'MySurvey._dow_group',
                            '@aether_extended_type': 'string'
                        },
                        {
                            'doc': 'Public Holiday open hours',
                            'name': '_ph_hours',
                            'type': [
                                'null',
                                'string'
                            ],
                            'namespace': 'MySurvey._dow_group',
                            '@aether_extended_type': 'string'
                        },
                        {
                            'name': '_select_hours',
                            'type': [
                                'null',
                                'string'
                            ],
                            'namespace': 'MySurvey._dow_group',
                            '@aether_extended_type': 'string'
                        }
                    ],
                    'namespace': 'MySurvey',
                    '@aether_extended_type': 'group'
                }
            ],
            'namespace': 'MySurvey',
            '@aether_extended_type': 'group'
        },
        {
            'doc': 'Enter weekday hours',
            'name': '_weekday_hours',
            'type': [
                'null',
                'string'
            ],
            'namespace': 'MySurvey',
            '@aether_extended_type': 'string'
        },
        {
            'doc': 'OSM:opening_hours',
            'name': '_advanced_hours',
            'type': [
                'null',
                'string'
            ],
            'namespace': 'MySurvey',
            '@aether_extended_type': 'string'
        },
        {
            'name': 'opening_hours',
            'type': [
                'null',
                'string'
            ],
            'namespace': 'MySurvey',
            '@aether_extended_type': 'string'
        },
        {
            'doc': 'Verify the open hours are correct or go back and fix:',
            'name': '_disp_hours',
            'type': [
                'null',
                'string'
            ],
            'namespace': 'MySurvey',
            '@aether_extended_type': 'string'
        },
        {
            'doc': 'Facility Category',
            'name': 'amenity',
            'type': [
                'null',
                'string'
            ],
            'namespace': 'MySurvey',
            '@aether_lookup': [
                {
                    'label': 'Clinic',
                    'value': 'clinic'
                },
                {
                    'label': 'Doctors',
                    'value': 'doctors'
                },
                {
                    'label': 'Hospital',
                    'value': 'hospital'
                },
                {
                    'label': 'Dentist',
                    'value': 'dentist'
                },
                {
                    'label': 'Pharmacy',
                    'value': 'pharmacy'
                }
            ],
            '@aether_extended_type': 'select1'
        },
        {
            'doc': 'Available Services',
            'name': 'healthcare',
            'type': [
                'null',
                {
                    'type': 'array',
                    'items': 'string'
                }
            ],
            'namespace': 'MySurvey',
            '@aether_lookup': [
                {
                    'label': 'Doctor',
                    'value': 'doctor'
                },
                {
                    'label': 'Pharmacy',
                    'value': 'pharmacy'
                },
                {
                    'label': 'Hospital',
                    'value': 'hospital'
                },
                {
                    'label': 'Clinic',
                    'value': 'clinic'
                },
                {
                    'label': 'Dentist',
                    'value': 'dentist'
                },
                {
                    'label': 'Physiotherapist',
                    'value': 'physiotherapist'
                },
                {
                    'label': 'Alternative',
                    'value': 'alternative'
                },
                {
                    'label': 'Laboratory',
                    'value': 'laboratory'
                },
                {
                    'label': 'Optometrist',
                    'value': 'optometrist'
                },
                {
                    'label': 'Rehabilitation',
                    'value': 'rehabilitation'
                },
                {
                    'label': 'Blood donation',
                    'value': 'blood_donation'
                },
                {
                    'label': 'Birthing center',
                    'value': 'birthing_center'
                }
            ],
            '@aether_extended_type': 'select'
        },
        {
            'doc': 'Specialities',
            'name': 'speciality',
            'type': [
                'null',
                {
                    'type': 'array',
                    'items': 'string'
                }
            ],
            'namespace': 'MySurvey',
            '@aether_lookup': [
                {
                    'label': 'xx',
                    'value': 'xx'
                }
            ],
            '@aether_extended_type': 'select'
        },
        {
            'doc': 'Speciality medical equipment available',
            'name': 'health_amenity_type',
            'type': [
                'null',
                {
                    'type': 'array',
                    'items': 'string'
                }
            ],
            'namespace': 'MySurvey',
            '@aether_lookup': [
                {
                    'label': 'Ultrasound',
                    'value': 'ultrasound'
                },
                {
                    'label': 'MRI',
                    'value': 'mri'
                },
                {
                    'label': 'X-Ray',
                    'value': 'x_ray'
                },
                {
                    'label': 'Dialysis',
                    'value': 'dialysis'
                },
                {
                    'label': 'Operating Theater',
                    'value': 'operating_theater'
                },
                {
                    'label': 'Laboratory',
                    'value': 'laboratory'
                },
                {
                    'label': 'Imaging Equipment',
                    'value': 'imaging_equipment'
                },
                {
                    'label': 'Intensive Care Unit',
                    'value': 'intensive_care_unit'
                },
                {
                    'label': 'Emergency Department',
                    'value': 'emergency_department'
                }
            ],
            '@aether_extended_type': 'select'
        },
        {
            'doc': 'Does this facility provide Emergency Services?',
            'name': 'emergency',
            'type': [
                'null',
                'string'
            ],
            'namespace': 'MySurvey',
            '@aether_lookup': [
                {
                    'label': 'Yes',
                    'value': 'yes'
                },
                {
                    'label': 'No',
                    'value': 'no'
                }
            ],
            '@aether_extended_type': 'select1'
        },
        {
            'doc': 'Does the pharmacy dispense prescription medication?',
            'name': 'dispensing',
            'type': [
                'null',
                'string'
            ],
            'namespace': 'MySurvey',
            '@aether_lookup': [
                {
                    'label': 'Yes',
                    'value': 'yes'
                },
                {
                    'label': 'No',
                    'value': 'no'
                }
            ],
            '@aether_extended_type': 'select1'
        },
        {
            'doc': 'Number of Beds',
            'name': 'beds',
            'type': [
                'null',
                'int'
            ],
            'namespace': 'MySurvey',
            '@aether_extended_type': 'int'
        },
        {
            'doc': 'Number of Doctors',
            'name': 'staff_doctors',
            'type': [
                'null',
                'int'
            ],
            'namespace': 'MySurvey',
            '@aether_extended_type': 'int'
        },
        {
            'doc': 'Number of Nurses',
            'name': 'staff_nurses',
            'type': [
                'null',
                'int'
            ],
            'namespace': 'MySurvey',
            '@aether_extended_type': 'int'
        },
        {
            'doc': 'Types of insurance accepted?',
            'name': 'insurance',
            'type': [
                'null',
                {
                    'type': 'array',
                    'items': 'string'
                }
            ],
            'namespace': 'MySurvey',
            '@aether_lookup': [
                {
                    'label': 'Public',
                    'value': 'public'
                },
                {
                    'label': 'Private',
                    'value': 'private'
                },
                {
                    'label': 'None',
                    'value': 'no'
                },
                {
                    'label': 'Unknown',
                    'value': 'unknown'
                }
            ],
            '@aether_extended_type': 'select'
        },
        {
            'doc': 'Is this facility wheelchair accessible?',
            'name': 'wheelchair',
            'type': [
                'null',
                'string'
            ],
            'namespace': 'MySurvey',
            '@aether_lookup': [
                {
                    'label': 'Yes',
                    'value': 'yes'
                },
                {
                    'label': 'No',
                    'value': 'no'
                }
            ],
            '@aether_extended_type': 'select1'
        },
        {
            'doc': 'What is the source of water for this facility?',
            'name': 'water_source',
            'type': [
                'null',
                'string'
            ],
            'namespace': 'MySurvey',
            '@aether_lookup': [
                {
                    'label': 'Well',
                    'value': 'well'
                },
                {
                    'label': 'Water works',
                    'value': 'water_works'
                },
                {
                    'label': 'Manual pump',
                    'value': 'manual_pump'
                },
                {
                    'label': 'Powered pump',
                    'value': 'powered_pump'
                },
                {
                    'label': 'Groundwater',
                    'value': 'groundwater'
                },
                {
                    'label': 'Rain',
                    'value': 'rain'
                }
            ],
            '@aether_extended_type': 'select1'
        },
        {
            'doc': 'What is the source of power for this facility?',
            'name': 'electricity',
            'type': [
                'null',
                'string'
            ],
            'namespace': 'MySurvey',
            '@aether_lookup': [
                {
                    'label': 'Power grid',
                    'value': 'grid'
                },
                {
                    'label': 'Generator',
                    'value': 'generator'
                },
                {
                    'label': 'Solar',
                    'value': 'solar'
                },
                {
                    'label': 'Other Power',
                    'value': 'other'
                },
                {
                    'label': 'No Power',
                    'value': 'none'
                }
            ],
            '@aether_extended_type': 'select1'
        },
        {
            'doc': 'URL for this location (if available)',
            'name': 'url',
            'type': [
                'null',
                'string'
            ],
            'namespace': 'MySurvey',
            '@aether_extended_type': 'string'
        },
        {
            'doc': 'In which health are is the facility located?',
            'name': 'is_in_health_area',
            'type': [
                'null',
                'string'
            ],
            'namespace': 'MySurvey',
            '@aether_extended_type': 'string'
        },
        {
            'doc': 'In which health zone is the facility located?',
            'name': 'is_in_health_zone',
            'type': [
                'null',
                'string'
            ],
            'namespace': 'MySurvey',
            '@aether_extended_type': 'string'
        },
        {
            'name': 'meta',
            'type': [
                'null',
                {
                    'name': 'meta',
                    'type': 'record',
                    'fields': [
                        {
                            'name': 'instanceID',
                            'type': [
                                'null',
                                'string'
                            ],
                            'namespace': 'MySurvey.meta',
                            '@aether_extended_type': 'string'
                        }
                    ],
                    'namespace': 'MySurvey',
                    '@aether_extended_type': 'group'
                }
            ],
            'namespace': 'MySurvey',
            '@aether_extended_type': 'group'
        },
        {
            'doc': 'UUID',
            'name': 'id',
            'type': 'string'
        },
        {
            'doc': 'Some vestigial garbage',
            'name': '__junk',
            'type': [
                'null',
                'string'
            ]
        },
        {
            'doc': 'a mandatory date',
            'name': 'mandatory_date',
            'type': 'int',
            'logicalType': 'date'
        },
        {
            'doc': 'an optional datetime',
            'name': 'optional_dt',
            'type': [
                'null',
                {
                    'type': 'long',
                    'logicalType': 'timestamp-millis'
                }
            ]
        }
    ],
    'namespace': 'org.ehealthafrica.aether.odk.xforms.Mysurvey'
}
'''
{
            'doc': 'an optional datetime',
            'name': 'optional_dt',
            'type': [
                'null',
                {
                    'type': 'long',
                    'logicalType': 'datetime-millis'
                }
            ]
        }
'''
EXAMPLE_ALL_TYPES = {
    'name': 'AllTypes',
    'type': 'record',
    'fields': [
        {
            'name': 'test_array',
            'type': {
                'type': 'array',
                'items': 'string'
            }
        },
        {
            'name': 'test_fixed',
            'type': {
                'type': 'fixed',
                'size': 32,
                'name': 'md5'
            }
        },
        {
            'name': 'test_enum',
            'type': {
                'name': 'TestEnum',
                'type': 'enum',
                'symbols': ['A', 'B', 'C']
            }
        },
        {
            'name': 'test_map',
            'type': {
                'type': 'map',
                'values': 'int'
            }
        },
        {'name': 'test_string', 'type': 'string'},
        {'name': 'test_boolean', 'type': 'boolean'},
        {'name': 'test_null', 'type': 'null'},
        {'name': 'test_bytes', 'type': 'bytes'},
        {'name': 'test_int', 'type': 'int'},
        {'name': 'test_long', 'type': 'long'},
        {'name': 'test_double', 'type': 'double'},
        {'name': 'test_float', 'type': 'float'}
    ],
    'namespace': 'org.ehealthafrica.aether.example'
}
