# benchmark

Install package in editable mode for development:

```console
$ git clone https://github.com/aprell/benchmark
$ pip install --user -e benchmark
```

Run tests:

```console
$ (cd benchmark/test && pytest -sv)
```

Why `pytest -s`? Problems with capturing stdout and stderr are documented
[here](https://github.com/pytest-dev/pytest/issues/5997).
