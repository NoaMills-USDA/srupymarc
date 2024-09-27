[![PyPI Version](https://img.shields.io/pypi/v/sruthi)](https://pypi.org/project/sruthi/)
[![Tests + Linting Python](https://github.com/metaodi/sruthi/actions/workflows/lint_python.yml/badge.svg)](https://github.com/metaodi/sruthi/actions/workflows/lint_python.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# sruthi

**sru**thi is a client for python to make [SRU requests (Search/Retrieve via URL)](http://www.loc.gov/standards/sru/).

This fork extends the [sruthi](https://github.com/metaodi/sruthi/tree/master) package to support the following output formats:
- Flattened dict (as implemented in the original sruthi package)
- [Pymarc](https://pymarc.readthedocs.io/en/latest/) record

Currently only **SRU 1.1 and 1.2** is supported.

## Table of Contents

* [Installation](#installation)
* [Usage](#usage)

## Installation

Install this package via the wheels included in the `dist/` directory:

```
$ cd dist
$ pip install sruthi-2.0.0-py3-none-any.whl
```

## Usage with Alma's SRU API

The `alma_queries_sruthi.py` script provides examples of how to use this sruthi fork. To run this example, first ensure you are connected to the VPN so you can access the Alma API. Then, create a python venv as follows:
```bash
python -m venv sru_venv
cd examples
pip install -r requirements.txt
```

Use the ```alma_queries_sruthi.py``` script as follows:

```python alma_queries_sruthi.py -o [OPERATION] -q [QUERY]```

For example, here is how you can query all of the articles that include the term `pothos` in the title. This is a recommended query to test with as it produces just enough records to observe sruthi's record iterating behaviors as described below.

```python alma_queries_sruthi.py -o searchRetrieve -q query3```

Note that when you request data through `sruthi`, it will first request the number of records specified by the `maximum_records` parameter. If you iterate through the returned records, then it will continuously make new API calls to request subsequent records until all the matches have been exhausted. Be wary of this if your query matches a large number of records.