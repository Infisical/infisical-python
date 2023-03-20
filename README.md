<h1 align="center">
    <a href="https://github.com/Infisical/infisical">
        <img width="300" src="https://raw.githubusercontent.com/Infisical/infisical-node/main/img/logoname-white.svg#gh-dark-mode-only" alt="infisical">
    </a>
</h1>
<p align="center">
  <p align="center">Open-source, end-to-end encrypted tool to manage secrets and configs across your team, devices, and infrastructure.</p>
</p>


<p align="center">
<a href="https://github.com/Astropilot/infisical-python/actions?query=workflow%3ATest+event%3Apush+branch%3Amain" target="_blank">
    <img src="https://github.com/Astropilot/infisical-python/workflows/Test/badge.svg?event=push&branch=main" alt="Test">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/Astropilot/infisical-python" target="_blank">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/Astropilot/infisical-python.svg" alt="Coverage">
</a>
<a href="https://pypi.org/project/infisicalpy" target="_blank">
    <img src="https://img.shields.io/pypi/v/infisicalpy?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/infisicalpy" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/infisicalpy.svg?color=%2334D058" alt="Supported Python versions">
</a>
<a href="https://github.com/Astropilot/infisical-python/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/Astropilot/infisical-python" alt="MIT License">
</a>
</p>

## Links

- [SDK docs](https://infisical.com/docs/sdk/overview/usage)

## Installation

You need Python 3.7+.

```console
$ pip install infisicalpy
```

## Initialization

If your app only needs to connect to one Infisical project, you should use `infisical.connect`. If you need to connect to multiple Infisical projects, use `infisical.createConnection`.

Both `connect` and `createConnection` take a parameter `token` and pull in the secrets accessible by that Infisical token.

```py
import infisicalpy

infisicalpy.connect("your_infisical_token")
```

### Options

- `token`: The service token from which to retrieve secrets
- `site_url`: Your self-hosted Infisical site URL. Default: `https://app.infisical.com`.
- `attach_to_process_env`: Whether or not to attach fetched secrets to `os.environ`. Default: `false`.
- `debug`: Turns debug mode on or off. If debug mode is enabled then the SDK will attempt to print out useful debugging information. Default: `false`.

## Access a Secret Value

```py
db_url = infisicalpy.get("DB_URL")
```

## Contributing

See [Contributing documentation](./.github/CONTRIBUTING.md)

## License

`infisicalpy` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
