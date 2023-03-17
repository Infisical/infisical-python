<h1 align="center">
    <a href="https://github.com/Infisical/infisical">
        <img width="300" src="https://raw.githubusercontent.com/Infisical/infisical-node/main/img/logoname-white.svg#gh-dark-mode-only" alt="infisical">
    </a>
</h1>
<p align="center">
  <p align="center">Open-source, end-to-end encrypted tool to manage secrets and configs across your team, devices, and infrastructure.</p>
</p>


<p align="center">
<a href="https://github.com/Astropilot/infisicalpy/actions?query=workflow%3ATest+event%3Apush+branch%3Amain" target="_blank">
    <img src="https://github.com/Astropilot/infisicalpy/workflows/Test/badge.svg?event=push&branch=main" alt="Test">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/Astropilot/infisicalpy" target="_blank">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/Astropilot/infisicalpy.svg" alt="Coverage">
</a>
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

## Links

- [SDK docs](https://infisical.com/docs/sdk/overview/usage)

## Usage

### Requirements

Python 3.7+

### Installation

```console
$ pip install infisicalpy
```

### Example

```py
import infisicalpy

infisicalpy.connect()

secrets = infisicalpy.get()
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

## License

`infisicalpy` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
