# folioqpy

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![codecov](https://codecov.io/github/MBounouar/folioqpy/branch/main/graph/badge.svg?token=1H51ZECQ7H)](https://codecov.io/github/MBounouar/folioqpy)
[![CodeFactor](https://www.codefactor.io/repository/github/mbounouar/folioqpy/badge)](https://www.codefactor.io/repository/github/mbounouar/folioqpy)

**folioqpy** is a Python library that merges the functionalities of the defunct quantopian `pyfolio` and `empyrical` packages into a single one, but using `plotly` instead of `matplotlib`.

## Summary

`plotly` allows for more cumstomized online reports (using Dash), interactive graphs, ...
Taking advantage of a well tested but unfortunately defunct library and attempt to maintain and keep it up to date (typing, ...).
Python >= 3.9

## Installation

```bash
$ pip install folioqpy
```

## Examples

Basic Dash examples can be found under the folder `examples/dash`

## Development

Ideally follow the principles outlined [here](https://nvie.com/posts/a-successful-git-branching-model/)
PR's, ideas and other suggestions are welcome.

## TODO's

- [] Port all the pyfolio plots
- [] typing
- [] Docs
