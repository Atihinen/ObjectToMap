# Object to map API

Restful API made with python Bottle framework

## Documentation
[API is documented here](https://rawgit.com/Atihinen/ObjectToMap/master/views/api.html)

## Installation

### Easy way
[Use virtualbox + vagrant setup](https://github.com/Atihinen/object-to-map-provisioning)

### Manual way

Requirements

* Python 2.7.x
  * Python c headers
* MySQL
* pip
* Linux: python-mysqldb
* Windows: [MySQL-python](https://pypi.python.org/pypi/MySQL-python/1.2.5)

Clone this repository

Run command `pip install -r requirements.txt`

## Setup

1. Create database
2. Create database user
3. Cd into repository
4. Run command `python manage.py init_db_config -u <mysql_user> -p <mysql_password> -d <database> -r <localhost/domain> -o <port>
5. Run sql scripts from evolutions folder


## Running the api

You can start the API with command `python api.py` and it'll start the api in port 8080. If you need to use different port, just run same command with argument. E.g. `python api.py 4000` and now the API is running on port 4000


## Unit tests

Run following command `nosetests test/`

## Acceptance tests

### Requirements

* Robot Framework, currently tests supports 2.8.7
* RequestsLibrary

### Running tests

1. Cd to folder test/acceptance
2. Run command `pybot -A localhost.txt .`
  * Notice that if the API is not running on port 8080 you need to change the value
  * If you want to test completely different environment the easiest way is to create copy of the localhost.txt and change the correct information there
