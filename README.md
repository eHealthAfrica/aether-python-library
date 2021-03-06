# Aether Python Library

This is the official Python Library with Aether functions.

## Table of contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Distribution](#distribution)
- [Tests](#tests)
- [Usage](#usage)
  - [Redis tools](#redis-tools)


## Requirements

This library requires **Python 3.6** and above.

Python libraries:

- [eha-jsonpath](https://github.com/eHealthAfrica/jsonpath-extensions/)
  Provides new Extensions to the jsonpath_ng python library to provide commonly requested functions.
- [jsonschema](https://github.com/Julian/jsonschema)
  An implementation of JSON Schema validation for Python.
- [redis](https://github.com/andymccurdy/redis-py)
  Python client for Redis key-value store.
- [requests](https://2.python-requests.org//en/master/)
  HTTP for Humans.
- [spavro](http://github.com/pluralsight/spavro)
  An Avro library, Spavro is a (sp)eedier avro implementation using Cython.

Extra dependencies (based on settings):

- **test**
  - [birdisle](https://github.com/bmerry/birdisle)
    A modified version of redis that runs as a library inside another process.
  - [coverage](https://coverage.readthedocs.io/)
    A tool for measuring code coverage of Python programs.
  - [flake8](http://flake8.pycqa.org/en/latest/)
    Tool For Style Guide Enforcement.
  - [flake8-quotes](https://github.com/zheller/flake8-quotes)
    Flake8 extension for checking quotes in python.
  - [tblib](https://github.com/ionelmc/python-tblib)
    Traceback serialization library.

*[Return to TOC](#table-of-contents)*


## Installation

```bash
# standalone
pip3 install aether.python
```

*[Return to TOC](#table-of-contents)*


## Distribution

How to create the package distribution

Execute the following command:

```bash
python3 setup.py bdist_wheel
```

or

```bash
./scripts/build.sh
```

*[Return to TOC](#table-of-contents)*


## Tests

Depending on your preference you can either use virtualenv or pipenv to test the library locally.

#### Virtual Env

First install dependencies (execute it only once):

```bash
./scripts/install.sh
```

After that execute the following command:

```bash
source ./venv/bin/activate
./scripts/test.sh
```

#### Pipenv

In the root folder run:
```bash
pipenv install .
```

Then to test run:
```bash
pipenv run scripts/test.sh
```


The file `scripts/test.ini` contains the environment variables used in the tests.

*[Return to TOC](#table-of-contents)*


## Usage

### Redis Tools
This provides an interface to a Redis server via supplied redis parameters.

It makes available a number of `CRUD` redis operation which include but not limited to:
    - Formats document keys into `_{type}:{tenant}:{id}` before being cached on redis.
    - Retrieves documents based on preformated keys.
    - Removes documents based on preformated keys.
    - Subscribes to key based channels with a callback function.

#### Usage

```python
from aether.python.redis.task import TaskHelper

REDIS_TASK = TaskHelper(settings, redis_instance)

# Settings must have the following properties:
# REDIS_HOST str - Redis server host,
# REDIS_PORT int - Redis server port,
# REDIS_PASSWORD str - Redis server password,
# REDIS_DB str - Redis database name

# redis_instance (Optional) - Pass an existing redis connection
# (If provided, ignores all settings and uses redis_instance)

document = {
    'id': 'document_id',
    'name': 'document name'
}

document_type = 'test_document'
aether_tenant = 'prod'

# add document to redis
REDIS_TASK.add(task=document, type=document_type, tenant=aether_tenant)

# retrieve document from redis
REDIS_TASK.get(_id=document['id'], type=document_type, tenant=aether_tenant)

# subcribe to a key based channel

CHANNEL = '_test_document*' # listens for messages published to all channels starting with '_test_document'

def handle_callback(msg):
    print(msg) # handle returned message

REDIS_TASK.subscribe(callback=handle_callback, pattern=CHANNEL, keep_alive=True)


# publish document
REDIS_TASK.publish(task=document, type=document_type, tenant=aether_tenant) # this will trigger the 'handle_callback' function with the published document to all subscribed clients
```
