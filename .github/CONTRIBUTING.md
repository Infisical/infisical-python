Start by cloning the repository:
```console
$ git clone https://github.com/Astropilot/infisicalpy
$ cd infisicalpy
```

We recommand that you create a virtual environment:
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

Then install the project in editable mode and the dependencies with:
```console
$ pip install -e '.[dev,test]'
```

To run all the tests you can use the following command:
```console
$ pytest tests
```
