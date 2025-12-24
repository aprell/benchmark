# benchmark

Install package in editable mode for development:

```console
$ pip install [--user] -e .
```

Run tests:

```console
$ pytest -sv
```

Why `pytest -s`? Problems with capturing stdout and stderr are documented
[here](https://github.com/pytest-dev/pytest/issues/5997).
