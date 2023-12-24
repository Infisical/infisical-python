<h1 align="center">
    <a href="https://github.com/Infisical/infisical">
        <img width="300" src="https://raw.githubusercontent.com/Infisical/infisical-node/main/img/logoname-white.svg#gh-dark-mode-only" alt="infisical">
    </a>
</h1>
<p align="center">
  <p align="center">Open-source, end-to-end encrypted tool to manage secrets and configs across your team and infrastructure.</p>
</p>

# Deprecated!

This is now considered a legacy SDK, as we have released a new SDK that will be receiving all future updates. [You can find it here](https://pypi.org/project/infisical-python/).

# Table of Contents

-   [Links](#links)
-   [Basic Usage](#basic-usage)
-   [Secrets](#working-with-secrets)
    -   [Get Secrets](#get-secrets)
    -   [Get Secret](#get-secret)
    -   [Create Secret](#create-secret)
    -   [Update Secret](#update-secret)
    -   [Delete Secret](#delete-secret)
-   [Cryptography](#cryptography)
    -   [Create Symmetric Key](#create-symmetric-key)
    -   [Encrypt Symmetric](#encrypt-symmetric)
    -   [Decrypt Symmetric](#decrypt-symmetric)

# Links

-   [Infisical](https://github.com/Infisical/infisical)

# Basic Usage

```py
from flask import Flask
from infisical import InfisicalClient

app = Flask(__name__)

client = InfisicalClient(token="your_infisical_token")

@app.route("/")
def hello_world():
    # access value
    name = client.get_secret("NAME", environment="dev", path="/")
    return f"Hello! My name is: {name.secret_value}"
```

This example demonstrates how to use the Infisical Python SDK with a Flask application. The application retrieves a secret named "NAME" and responds to requests with a greeting that includes the secret value.

It is also possible to use the SDK to encrypt/decrypt text; the implementation uses `aes-256-gcm` with components of the encryption/decryption encoded in `base64`.

```python
from infisical import InfisicalClient

client = InfisicalClient()

# some plaintext you want to encrypt
plaintext = 'The quick brown fox jumps over the lazy dog'

# create a base64-encoded, 256-bit symmetric key
key = client.create_symmetric_key()

# encrypt
ciphertext, iv, tag = client.encrypt_symmetric(plaintext, key)

# decrypt
cleartext = client.decrypt_symmetric(ciphertext, key, iv, tag)
```

# Installation

You need Python 3.7+.

```console
$ pip install infisical
```

# Configuration

Import the SDK and create a client instance with your [Infisical Token](https://infisical.com/docs/getting-started/dashboard/token).

```py
from infisical import InfisicalClient

client = InfisicalClient(token="your_infisical_token")
```

Using Infisical Token V3 (Beta):

In `v1.5.0`, we released a superior token authentication method; this credential is a JSON containing a `publicKey`, `privateKey`, and `serviceToken` and can be used to initialize the Node SDK client instead of the regular service token.

You can use this beta feature like so:

```py
from infisical import InfisicalClient

client = InfisicalClient(token_json="your_infisical_token_v3_json")
```

### Options

| Parameter   | Type      | Description                                                                 |
| ----------- | --------- | --------------------------------------------------------------------------- |
| `token`     | `string`  | An Infisical Token scoped to a project and environment(s).                  |
| `tokenJson` | `string`  | An Infisical Token V3 JSON scoped to a project and environment(s) - in beta |
| `site_url`  | `string`  | Your self-hosted Infisical site URL. Default: `https://app.infisical.com`.  |
| `cache_ttl` | `number`  | Time-to-live (in seconds) for refreshing cached secrets. Default: `300`.    |
| `debug`     | `boolean` | Turns debug mode on or off. Default: `false`.                               |

### Caching

The SDK caches every secret and updates it periodically based on the provided `cache_ttl`. For example, if `cache_ttl` of `300` is provided, then a secret will be refetched 5 minutes after the first fetch; if the fetch fails, the cached secret is returned.

# Secrets

## Get Secrets

```py
secrets = client.get_all_secrets(environment="dev", path="/foo/bar/")
```

Retrieve all secrets within a given environment and folder path. The service token used must have access to the given path and environment.

### Parameters

-   `environment` (string): The slug name (dev, prod, etc) of the environment from where secrets should be fetched from.
-   `path` (string): The path from where secrets should be fetched from.
-   `include_imports` (boolean): Whether or not to include imported secrets from the current path. Read about [secret import](https://infisical.com/docs/documentation/platform/secret-reference#import-entire-folders). If not specified, the default value is `True`.
-   `attach_to_os_environ` (boolean): Whether or not to attach fetched secrets to `os.environ`. If not specified, the default value is `False`.

## Get Secret

```py
secret = client.get_secret("API_KEY", environment="dev", path="/")
value = secret.secret_value # get its value
```

By default, `get_secret()` fetches and returns a personal secret. If not found, it returns a shared secret, or tries to retrieve the value from `os.environ`. If a secret is fetched, `get_secret()` caches it to reduce excessive calls and re-fetches periodically based on the `cacheTTL` option (default is 300 seconds) when initializing the client — for more information, see the caching section.

To explicitly retrieve a shared secret:

```py
secret = client.get_secret(secret_name="API_KEY", type="shared", environment="dev", path="/")
value = secret.secret_value # get its value
```

### Parameters

-   `secret_name` (string): The key of the secret to retrieve.
-   `environment` (string): The slug name (dev, prod, etc) of the environment from where secrets should be fetched from.
-   `path` (string): The path from where secrets should be fetched from.
-   `type` (string, optional): The type of the secret. Valid options are "shared" or "personal". If not specified, the default value is "personal".

## Create Secret

Create a new secret in Infisical

```py
new_api_key = client.create_secret("API_KEY", "FOO", environment="dev", path="/", type="shared")
```

### Parameters

-   `secret_name` (string): The key of the secret to create.
-   `secret_value` (string): The value of the secret.
-   `environment` (string): The slug name (dev, prod, etc) of the environment from where secrets should be fetched from.
-   `path` (string): The path from where secrets should be created.
-   `type` (string, optional): The type of the secret. Valid options are "shared" or "personal". If not specified, the default value is "shared". A personal secret can only be created if a shared secret with the same name exists.

## Update Secret

Update an existing secret in Infisical

```py
updated_api_key = client.update_secret("API_KEY", "BAR", environment="dev", path="/", type="shared")
```

### Parameters

-   `secret_name` (string): The key of the secret to update.
-   `secret_value` (string): The new value of the secret.
-   `environment` (string): The slug name (dev, prod, etc) of the environment from where secrets should be fetched from.
-   `path` (string): The path from where secrets should be updated.
-   `type` (string, optional): The type of the secret. Valid options are "shared" or "personal". If not specified, the default value is "shared".

## Delete Secret

Delete a secret in Infisical

```py
deleted_secret = client.delete_secret("API_KEY", environment="dev", path="/", type="shared")
```

### Parameters

-   `secret_name` (string): The key of the secret to delete.
-   `environment` (string): The slug name (dev, prod, etc) of the environment from where secrets should be fetched from.
-   `path` (string): The path from where secrets should be deleted.
-   `type` (string, optional): The type of the secret. Valid options are "shared" or "personal". If not specified, the default value is "shared".

# Cryptography

## Create Symmetric Key

Create a base64-encoded, 256-bit symmetric key to be used for encryption/decryption.

```python
key = client.create_symmetric_key()
```

### Returns

`key` (string): A base64-encoded, 256-bit symmetric key.

## Encrypt Symmetric

Encrypt plaintext -> ciphertext.

```python
ciphertext, iv, tag = client.encrypt_symmetric(plaintext, key)
```

### Parameters

-   `plaintext` (string): The plaintext to encrypt.
-   `key` (string): The base64-encoded, 256-bit symmetric key to use to encrypt the `plaintext`.

### Returns

-   `ciphertext` (string): The base64-encoded, encrypted `plaintext`.
-   `iv` (string): The base64-encoded, 96-bit initialization vector generated for the encryption.
-   `tag` (string): The base64-encoded authentication tag generated during the encryption.

## Decrypt Symmetric

Decrypt ciphertext -> plaintext/cleartext.

```python
cleartext = client.decrypt_symmetric(ciphertext, key, iv, tag)
```

### Parameters

-   `ciphertext` (string): The ciphertext to decrypt.
-   `key` (string): The base64-encoded, 256-bit symmetric key to use to decrypt the `ciphertext`.
-   `iv` (string): The base64-encoded, 96-bit initiatlization vector generated for the encryption.
-   `tag` (string): The base64-encoded authentication tag generated during encryption.

### Returns

`cleartext` (string): The decrypted encryption that is the cleartext/plaintext.

# Contributing

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

# License

`infisical-python` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
