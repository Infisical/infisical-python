<h1 align="center">
    <a href="https://github.com/Infisical/infisical">
        <img width="300" src="https://raw.githubusercontent.com/Infisical/infisical-node/main/img/logoname-white.svg#gh-dark-mode-only" alt="infisical">
    </a>
</h1>
<p align="center">
  <p align="center">Open-source, end-to-end encrypted tool to manage secrets and configs across your team and infrastructure.</p>
</p>


<p align="center">
<a href="https://github.com/Astropilot/infisical-python/actions?query=workflow%3ATest+event%3Apush+branch%3Amain" target="_blank">
    <img src="https://github.com/Astropilot/infisical-python/workflows/Test/badge.svg?event=push&branch=main" alt="Test">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/Astropilot/infisical-python" target="_blank">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/Astropilot/infisical-python.svg" alt="Coverage">
</a>
<a href="https://pypi.org/project/infisical" target="_blank">
    <img src="https://img.shields.io/pypi/v/infisical?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/infisical" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/infisical.svg?color=%2334D058" alt="Supported Python versions">
</a>
<a href="https://github.com/Astropilot/infisical-python/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/Astropilot/infisical-python" alt="MIT License">
</a>
</p>

## Links

- [SDK docs](https://infisical.com/docs/sdks/languages/python)

## Basic Usage

```py
from flask import Flask
from infisical import InfisicalClient

app = Flask(__name__)

client = InfisicalClient(token="your_infisical_token")

@app.route("/")
def hello_world():
    # access value
    name = client.get_secret("NAME")
    return f"Hello! My name is: {name.secret_value}"
```

This example demonstrates how to use the Infisical Python SDK with a Flask application. The application retrieves a secret named "NAME" and responds to requests with a greeting that includes the secret value.

## Installation

You need Python 3.7+.

```console
$ pip install infisical
```

## Configuration

Import the SDK and create a client instance with your [Infisical Token](https://infisical.com/docs/getting-started/dashboard/token).


```py
from infisical import InfisicalClient

client = InfisicalClient(token="your_infisical_token")
```

### Options

| Parameter | Type     | Description |
| --------- | -------- | ----------- |
| `token`   | `string` | An Infisical Token scoped to a project and environment. |
| `site_url` | `string` | Your self-hosted Infisical site URL. Default: `https://app.infisical.com`. |
| `cache_ttl`| `number` | Time-to-live (in seconds) for refreshing cached secrets. Default: `300`.|
| `debug`   | `boolean` | Turns debug mode on or off. Default: `false`.      |

### Caching

The SDK caches every secret and updates it periodically based on the provided `cache_ttl`. For example, if `cache_ttl` of `300` is provided, then a secret will be refetched 5 minutes after the first fetch; if the fetch fails, the cached secret is returned.

## Working with Secrets

### Get Secrets

```py
secrets = client.get_all_secrets()
```

Retrieve all secrets within the Infisical project and environment

### Get Secret

```py
secret = client.get_secret("API_KEY")
value = secret.secret_value # get its value
```

By default, `get_secret()` fetches and returns a personal secret. If not found, it returns a shared secret, or tries to retrieve the value from `os.environ`. If a secret is fetched, `get_secret()` caches it to reduce excessive calls and re-fetches periodically based on the `cacheTTL` option (default is 300 seconds) when initializing the client — for more information, see the caching section.

To explicitly retrieve a shared secret:

```py
secret = client.get_secret(secret_name="API_KEY", type="shared")
value = secret.secret_value # get its value
```

### Parameters

- `secret_name` (string): The key of the secret to retrieve.
- `type` (string, optional): The type of the secret. Valid options are "shared" or "personal". If not specified, the default value is "personal".

### Create Secret

Create a new secret in Infisical

```py
new_api_key = client.create_secret("API_KEY", "FOO")
```

### Parameters

- `secret_name` (string): The key of the secret to create.
- `secret_value` (string): The value of the secret.
- `type` (string, optional): The type of the secret. Valid options are "shared" or "personal". If not specified, the default value is "shared". A personal secret can only be created if a shared secret with the same name exists.

### Update Secret

Update an existing secret in Infisical

```py
updated_api_key = client.update_secret("API_KEY", "BAR")
```

### Parameters

- `secret_name` (string): The key of the secret to update.
- `secret_value` (string): The new value of the secret.
- `type` (string, optional): The type of the secret. Valid options are "shared" or "personal". If not specified, the default value is "shared".

### Delete Secret

Delete a secret in Infisical

```py
deleted_secret = client.delete_secret("API_KEY")
```

### Parameters

- `secret_name` (string): The key of the secret to delete.
- `type` (string, optional): The type of the secret. Valid options are "shared" or "personal". If not specified, the default value is "shared".

## Contributing

Bug fixes, docs, and library improvements are always welcome. Please refer to our [Contributing Guide](https://infisical.com/docs/contributing/overview) for detailed information on how you can contribute.

[//]: contributor-faces

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->

<a href="https://github.com/Astropilot"><img src="https://avatars.githubusercontent.com/u/11898378?v=4" width="50" height="50" alt=""/></a> <a href="https://github.com/dangtony98"><img src="https://avatars.githubusercontent.com/u/25857006?v=4" width="50" height="50" alt=""/></a> <a href="https://github.com/Nnahoy"><img src="https://avatars.githubusercontent.com/u/86289996?v=4" width="50" height="50" alt=""/></a>

## Getting Started

If you want to familiarize yourself with the SDK, you can start by [forking the repository](https://docs.github.com/en/get-started/quickstart/fork-a-repo) and [cloning it in your local development environment](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository). 

After cloning the repository, we recommend that you create a virtual environment:

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

Make sure that you have the latest version of `pip` to avoid errors on the next step:
```console
$ python -m pip install --upgrade pip
```

Then install the project in editable mode and the dependencies with:
```console
$ pip install -e '.[dev,test]'
```

To run existing tests, you need to make a `.env` at the root of this project containing a `INFISICAL_TOKEN` and `SITE_URL`. This will execute the tests against a project and environment scoped to the `INFISICAL_TOKEN` on a running instance of Infisical at the `SITE_URL` (this could be [Infisical Cloud](https://app.infisical.com)).

To run all the tests you can use the following command:

```console
$ pytest tests
```

## License

`infisical-python` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
