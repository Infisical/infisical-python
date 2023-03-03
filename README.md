# infisicalpy

<p align="center">
<a href="https://pypi.org/project/infisicalpy" target="_blank">
    <img src="https://img.shields.io/pypi/v/infisicalpy?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/infisicalpy" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/infisicalpy.svg?color=%2334D058" alt="Supported Python versions">
</a>
<a href="https://github.com/Astropilot/infisicalpy/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/Astropilot/infisicalpy" alt="MIT License">
</a>
<img src="https://img.shields.io/badge/Made%20with-%E2%9D%A4%EF%B8%8F-red.svg" alt="Made with love">
</p>

-----

<p align="center">
  <a href="#about">About</a> •
  <a href="#usage">Usage</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#license">License</a>
</p>

## About

A python alternative to the [Infisical](https://github.com/Infisical/infisical) CLI for secrets fetching and wrapper around the API.

**⚠️ Warning ⚠️** This library is still under development, a first beta version will be available on Pypi once the MVP is reached. See the roadmap below:

- [x] Service token features
  - [x] Fetch secrets
  - [x] Inject secrets into os.environ
  - [ ] Unit testing

-----> Beta version

- [ ] API features
  - [ ] Users
    - [ ] Get my user
    - [ ] Get my organisations
  - [ ] Organisations
    - [ ] Get memberships
    - [ ] Update membership
    - [ ] Delete membership
    - [ ] Get projects
  - [ ] Projects
    - [ ] Get memberships
    - [ ] Update membership
    - [ ] Delete membership
    - [ ] Get key
    - [ ] Get logs
    - [ ] Get snapshots
    - [ ] Roll back to snapshop
  - [ ] Secrets
    - [ ] Create
    - [ ] Retrieve
    - [ ] Update
    - [ ] Delete
    - [ ] Get versions
    - [ ] Roll back to version

## Usage

### Requirements

Python 3.7+

### Installation

```console
$ pip install infisicalpy
```

### Example

```py
from infisicalpy import SecretService

secret_service = SecretService(
    token="YOUR_SERVICE_TOKEN",
    domain="YOUR_CUSTOM_INFISICAL_DOMAIN" # If not provided the cloud api will be used by default
)

# token can be also given with the environment variable INFISICAL_TOKEN
# domain can be also given with the environment variable INFISICAL_API_URL

secrets = secret_service.get_all()
print(secrets)

>>> [
>>> SingleEnvironmentVariable(
>>>     key='DATABASE_URL',
>>>     value='mongodb+srv://user1234:example_password@mongodb.net',
>>>     type='shared',
>>>     id='XXXXXXXXXXXXXXXXXXXXXXXX',
>>>     tags=[
>>>         Tag(
>>>             id='XXXXXXXXXXXXXXXXXXXXXXXX',
>>>             name='tag1',
>>>             slug='tag1',
>>>             workspace='XXXXXXXXXXXXXXXXXXXXXXXX'),
>>>         Tag(
>>>             id='XXXXXXXXXXXXXXXXXXXXXXXX',
>>>             name='tag2',
>>>             slug='tag2',
>>>             workspace='XXXXXXXXXXXXXXXXXXXXXXXX')
>>>     ],
>>>     comment='Secret referencing example'),
>>> SingleEnvironmentVariable(
>>>     key='DB_USERNAME',
>>>     value='user1234',
>>>     type='personal',
>>>     id='XXXXXXXXXXXXXXXXXXXXXXXX',
>>>     tags=[
>>>         Tag(
>>>             id='XXXXXXXXXXXXXXXXXXXXXXXX',
>>>             name='tag2',
>>>             slug='tag2',
>>>             workspace='XXXXXXXXXXXXXXXXXXXXXXXX')
>>>     ],
>>>     comment=''),
>>> SingleEnvironmentVariable(
>>>     key='DB_PASSWORD',
>>>     value='example_password',
>>>     type='personal',
>>>     id='XXXXXXXXXXXXXXXXXXXXXXXX',
>>>     tags=[],
>>>     comment=''),
>>> SingleEnvironmentVariable(
>>>     key='TWILIO_AUTH_TOKEN',
>>>     value='example_twillio_token',
>>>     type='shared',
>>>     id='XXXXXXXXXXXXXXXXXXXXXXXX',
>>>     tags=[
>>>         Tag(
>>>             id='XXXXXXXXXXXXXXXXXXXXXXXX',
>>>             name='tag1', slug='tag1',
>>>             workspace='XXXXXXXXXXXXXXXXXXXXXXXX')
>>>     ],
>>>     comment=''),
>>> SingleEnvironmentVariable(
>>>     key='WEBSITE_URL',
>>>     value='http://localhost:3000',
>>>     type='shared',
>>>     id='XXXXXXXXXXXXXXXXXXXXXXXX',
>>>     tags=[],
>>>     comment='')
]

# To retrieve and add secrets to environment variables:
secret_service.inject_all()

# From here all your secrets are available in os.environ!

assert os.environ['DB_PASSWORD'] == 'example_password'
```

## Contributing

Start by cloning the repository:
```console
$ git clone https://github.com/Astropilot/infisicalpy
$ cd infisicalpy
```

I recommand that you create a virtual environment:
```console
$ python -m venv env
```

Then activate the environment with:
```console
# For linux
$ source ./env/bin/activate

# For Windows PowerShell
$ .\env\Scripts\Activate.ps1
```

Then install the project and the dependencies with:
```console
$ pip install -e '.[dev,test]'
```

To run all the tests you can use the following command:
```console
$ pytest tests
```

More information about the setup to run the tests will be coming...

## License

`infisicalpy` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
