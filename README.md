# clikraken

Command-line client for the Kraken exchange

This command line client allows you to get useful public and private information
from Kraken's API and displays it in formatted tables.

Moreover you can place or cancel simple orders
(only buy/sell market/limit is currently implemented).

**WARNING**: This software is currently in development.
I consider it in _alpha_ state, which means that it works well enough for me but hasn't been thoroughly tested.
There are probably undetected bugs left. **Use at your own risk!**

## Installation

You should install it in a virtualenv, but that's not mandatory.

### Step 1: Create a virtualenv

```
mkdir -p ~/.venv  # or any folder of your choice
pyvenv ~/.venv/clikraken
```

And activate it:

```
source ~/.venv/clikraken/bin/activate
```

### Step 2: Install dependencies

clikraken depends on the following extra modules:

* `arrow`, for better handling of date and time
* `tabulate`, for printing results as tables
* `python3-krakenex`, for the low-level interface with the Kraken API

Somehow you need to install the dependencies manually before installing clikraken. I haven't had success in making the dependency system of pip work consistently with `python3-krakenex` being only available as a Git repository yet. It would be nicer if it were packaged for Pypi.

Install arrow and tabulate in the activated virtualenv:

```
pip install arrow tabulate
```

Install python3-krakenex in the activated virtualenv:

```
pip install -e "git+https://github.com/veox/python3-krakenex.git@33b758f1f56257a35da85b0b14eb9cb1afb7b045#egg=krakenex-0.0.6"
```

### Step 3: Install clikraken

```
# make sure you have installed arrow, tabulate and krakenex before! You can check with 'pip list'
pip install clikraken
```

If everything went well, `clikraken --version` should output the program's version without error.

### Step 4: Add your API key in the file `~/.config/clikraken/kraken.key`

You will need it to perform private queries to the Kraken API.

(Create the config folder if needed: `mkdir -p ~/.config/clikraken`)

```
keykeykeykeykeykeykeykeykeykeykeykeykeykeykeykeykeykeykey
secretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecret
```

You should probably change the permissions to this file to protect it: `chmod 600 ~/.config/clikraken/kraken.key`

### Step 5 (optional): Generate a settings file and adapt it to your needs

clikraken looks for settings in `~/.config/clikraken/settings.ini`. 

If the settings file doesn't exist yet, default settings are assumed. You can see the default settings by calling `clikraken generate_settings`. Currently these settings are mostly useful for defining the default currency pair to assume if not provided as an option (--pair). The current built-in default pair is XETHZEUR. You may want to change that if you are mostly trading with another currency pair.

You can generate your `settings.ini` by doing the following:

```
mkdir -p ~/.config/clikraken # only if the folder doesn't exist yet
clikraken generate_settings > ~/.config/clikraken/settings.ini
```

## Usage

First activate the virtualenv:

```
source ~/.venv/clikraken/bin/activate
```

(When you are done using clikraken, you can deactivate the virtualenv with `deactivate`.)

This command line client works by calling subcommands with their respective options and arguments

Get help to see the available subcommands:

```
clikraken --help
```

Output:

```
usage: clikraken [-h] [-v] [--raw]
                 {generate_settings,ticker,depth,last_trades,lt,balance,bal,place,cancel,olist,ol,clist,cl}
                 ...

Command line client for the Kraken exchange

positional arguments:
  {generate_settings,ticker,depth,last_trades,lt,balance,bal,place,cancel,olist,ol,clist,cl}
                        available subcommands
    generate_settings   [clikraken] Output the default settings.ini file
    ticker              [public] Get the Ticker
    depth               [public] Get the current market depth data
    last_trades (lt)    [public] Get the last trades
    balance (bal)       [private] Get your current balance
    place               [private] Place an order
    cancel              [private] Cancel an order
    olist (ol)          [private] Get a list of your open orders
    clist (cl)          [private] Get a list of your closed orders

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program version
  --raw                 output raw json results from the API

Current default currency pair: XETHZEUR. Create or edit
~/.config/clikraken/settings.ini to change it. See also the
subcommand 'generate_settings'.
```

To get information on how to use a subcommand:

```
clikraken SUBCOMMAND --help
```

## Upgrade

In the activated virtualenv:

```
pip install -U --no-deps clikraken
```

`--no-deps` is currently needed because trying to upgrade the dependency `krakenex` fails, because it is not available on PyPi, only as a Git repository.

## Attribution

clikraken code is licensed under the Apache license, Version 2.0.
See the `LICENSE` file. For the full text, see [here][corelicense].

### Dependencies

* [python3-krakenex][python3-krakenex] code is licensed under the LGPLv3 license.
* [Arrow][arrow-license] code is licensed under is licensed under the Apache License, Version 2.0.
* [tabulate][tabulate-license] code is licensed under is licensed under the MIT Licence.

### Development dependencies

* `pip install pypandoc twine wheel`

[corelicense]: https://www.apache.org/licenses/LICENSE-2.0
[python3-krakenex]: https://github.com/veox/python3-krakenex
[arrow-license]: https://github.com/crsmithdev/arrow/blob/master/LICENSE
[tabulate-license]: https://pypi.python.org/pypi/tabulate
