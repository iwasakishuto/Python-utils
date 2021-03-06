# Python-Charmers

[![header](https://github.com/iwasakishuto/Python-Charmers/blob/master/image/header.png?raw=true)](https://github.com/iwasakishuto/Python-Charmers)
[![PyPI version](https://badge.fury.io/py/Python-Charmers.svg)](https://pypi.org/project/Python-Charmers/)
[![GitHub version](https://badge.fury.io/gh/iwasakishuto%2FPython-Charmers.svg)](https://github.com/iwasakishuto/Python-Charmers)
![Python package](https://github.com/iwasakishuto/Python-Charmers/workflows/Python%20package/badge.svg)
![Upload Python Package](https://github.com/iwasakishuto/Python-Charmers/workflows/Upload%20Python%20Package/badge.svg)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://github.com/iwasakishuto/Python-Charmers/blob/master/LICENSE)

A collection of useful python programs.

## Installation

1. Install **`Python-Charmers`** (There are two ways to install):
    - **Install from PyPI (recommended):**
        ```sh
        $ sudo pip install Python-Charmers
        ```
    - **Alternatively: install PyGuitar from the GitHub source:**
        ```sh
        $ git clone https://github.com/iwasakishuto/Python-Charmers.git
        $ cd Python-Charmers
        $ sudo python setup.py install
        ```
2. Install **driver** for `selenium`:
**`Selenium`** requires a driver to interface with the chosen browser, so please visit the [documentation](https://selenium-python.readthedocs.io/installation.html#drivers) to install it.
    ```sh
    # Example: Chrome
    # visit "chrome://settings/help" to check your chrome version.
    # visit "https://chromedriver.chromium.org/downloads" to check <Suitable.Driver.Version> for your chrome.
    $ wget https://chromedriver.storage.googleapis.com/<Suitable.Driver.Version>/chromedriver_mac64.zip
    $ unzip chromedriver_mac64.zip
    $ mv chromedriver /usr/local/bin/chromedriver
    $ chmod +x /usr/local/bin/chromedriver
    ```

## CLI

**CLI** is a command line program that accepts text input to execute operating system functions.

|Command|Description|
|:-:|:-|
| `pycharmers-show`    | Show all Python-Charmers's command line programs. |
| `regexp-replacement` | String replacement in a file using regular expression. |
| `render-template`    | Render templates. |
| `cv-window`          | Handle OpenCV Windows. |
| `pdfmine`            | Mine a PDF file. |

## Quick example

- **[example notebooks](https://nbviewer.jupyter.org/github/iwasakishuto/Python-Charmers/blob/master/examples/)**