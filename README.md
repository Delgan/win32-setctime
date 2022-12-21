# win32-setctime

[![Pypi version](https://img.shields.io/pypi/v/win32-setctime.svg)](https://pypi.python.org/pypi/win32-setctime) [![Python version](https://img.shields.io/badge/python-3.5%2B-blue.svg)](https://pypi.python.org/pypi/win32-setctime) [![Build status](https://img.shields.io/github/actions/workflow/status/Delgan/win32-setctime/tests.yml?branch=master)](https://github.com/Delgan/win32-setctime/actions/workflows/tests.yml?query=branch:master) [![License](https://img.shields.io/github/license/delgan/win32-setctime.svg)](https://github.com/Delgan/win32-setctime/blob/master/LICENSE)

A small Python utility to set file creation time on Windows.


## Installation

```shell
pip install win32-setctime
```

## Usage

```python
from win32_setctime import setctime

setctime("my_file.txt", 1561675987.509, follow_symlinks=True)
```
