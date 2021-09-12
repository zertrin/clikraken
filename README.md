![Actively Maintained](https://img.shields.io/badge/Maintenance%20Level-Actively%20Maintained-green.svg)

[![Travis-CI Build Status](https://travis-ci.org/zertrin/clikraken.svg?branch=master)](https://travis-ci.org/zertrin/clikraken)
[![Appveyor Build status](https://ci.appveyor.com/api/projects/status/jom3ee762u02q2fo/branch/master?svg=true)](https://ci.appveyor.com/project/zertrin/clikraken/branch/master)
[![PyPI Package latest release](https://img.shields.io/pypi/v/clikraken.svg)](https://pypi.python.org/pypi/clikraken)
[![Wheel available](https://img.shields.io/pypi/wheel/clikraken.svg)](https://pypi.python.org/pypi/clikraken)
[![Supported Versions](https://img.shields.io/pypi/pyversions/clikraken.svg)](https://pypi.python.org/pypi/clikraken)
[![Supported implementations](https://img.shields.io/pypi/implementation/clikraken.svg)](https://pypi.python.org/pypi/clikraken)
[![GitHub license](https://img.shields.io/badge/license-Apache%202-blue.svg)](https://raw.githubusercontent.com/flepied/clikraken/master/LICENSE)

# clikraken

**Command-line client for the Kraken exchange**

This command line client allows you to get useful public and private information
from [Kraken's API](https://www.kraken.com/help/api) and displays it in formatted tables.

Moreover you can place or cancel simple orders
(only simple or leveraged buy/sell market/limit orders are currently implemented).

It is mainly oriented as an alternative to manually entering orders on Kraken's webpages, to save some time and eliminate mouse clicks. It is not optimized for automated use.

See package on PyPI: https://pypi.python.org/pypi/clikraken

**WARNING**: This software is currently in development.
I consider it in _beta_ state, which means that it works well enough for me but hasn't been thoroughly tested.
There are probably undetected bugs left. **Use at your own risk!**

See list of changes in the [Changelog](CHANGELOG.md).

## List of supported Kraken API endpoints

| API Type | [API Endpoint](https://www.kraken.com/features/api) | used by clikraken command |
|----------|----------|-------------------|
| public | `AssetPairs` | asset_pairs (ap) |
| public | `Depth` | depth (d) |
| public | `OHLC` | ohlc (oh) |
| public | `Ticker` | ticker (t) |
| public | `Trades` | last_trades (lt) |
| private | `AddOrder` | place (p) |
| private | `Balance` | balance (bal) |
| private | `CancelOrder` | cancel (x) |
| private | `ClosedOrders` | clist (cl) |
| private | `DepositAddresses` | deposit_addresses (da) |
| private | `DepositMethods` | deposit_methods (dm) |
| private | `Ledgers` | ledgers (lg) |
| private | `OpenOrders` | olist (ol) |
| private | `OpenPositions` | positions (pos) |
| private | `QueryLedgers` | ledgers (lg) |
| private | `QueryOrders` | olist (ol) / clist (cl) |
| private | `QueryTrades` | trades (tr) |
| private | `TradeBalance` | trade_balance (tbal) |
| private | `TradesHistory` | trades (tr) |

Note: any API endpoint listed at <https://www.kraken.com/features/api> but not in the above list has not been implemented in clikraken (yet).

## Installation

### Step 0: Create a virtualenv (optional)

You can install it in a virtualenv if you wish to keep this program and dependencies isolated from the rest of your system, but that's not mandatory.

```
mkdir -p ~/.venv  # or any folder of your choice
pyvenv ~/.venv/clikraken
```

And activate it:

```
source ~/.venv/clikraken/bin/activate
```

### Step 1: Install clikraken

```
pip install clikraken
```

If everything went well, `clikraken --version` should output the program's version without error.

### Step 2: Add your API key in the file `~/.config/clikraken/kraken.key`

You will need it to perform private queries to the Kraken API.

(Create the config folder if needed: `mkdir -p ~/.config/clikraken`)

```
keykeykeykeykeykeykeykeykeykeykeykeykeykeykeykeykeykeykey
secretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecret
```

You should probably change the permissions to this file to protect it: `chmod 600 ~/.config/clikraken/kraken.key`

Alternatively, you can set a path in the environment variable `CLIKRAKEN_API_KEYFILE` to override the default keyfile location.

### Step 3 (optional): Generate a settings file and adapt it to your needs

clikraken looks for settings in `~/.config/clikraken/settings.ini` per default. 

If the settings file doesn't exist yet, default settings are assumed. You can see the default settings by calling `clikraken generate_settings`. Currently these settings are mostly useful for defining the default currency pair to use if the option `--pair` (or `-p`) is not provided. *The current built-in default pair is XETHZEUR* (Ethereum/Euro). You may want to change that if you are mostly trading with another currency pair. Alternatively, you can set the environment variable `CLIKRAKEN_DEFAULT_PAIR` to override the default currency pair.

You can generate your `settings.ini` by doing the following:

```
mkdir -p ~/.config/clikraken # only if the folder doesn't exist yet
clikraken generate_settings > ~/.config/clikraken/settings.ini
```

Alternatively, you can set a path in the environment variable `CLIKRAKEN_USER_SETTINGS_PATH` to override the default user settings file location.

## Usage

If installed in a virtualenv, don't forget to activate it first: `source ~/.venv/clikraken/bin/activate` (When you are done using clikraken, you can deactivate the virtualenv with `deactivate`.)

This command line client works by calling subcommands with their respective options and arguments (similar to git).

Get help to see the available subcommands:

```
clikraken --help
```

Output:

```
usage: clikraken [-h] [-V] [--debug] [--raw] [--csv]
                 [--csvseparator CSVSEPARATOR] [--cron]
                 {generate_settings,asset_pairs,ap,ticker,t,depth,d,last_trades,lt,ohlc,oh,balance,bal,trade_balance,tbal,place,p,cancel,x,olist,ol,positions,pos,clist,cl,ledgers,lg,trades,tr,deposit_methods,dm,deposit_addresses,da}
                 ...

clikraken - Command line client for the Kraken exchange

positional arguments:
  {generate_settings,asset_pairs,ap,ticker,t,depth,d,last_trades,lt,ohlc,oh,balance,bal,trade_balance,tbal,place,p,cancel,x,olist,ol,positions,pos,clist,cl,ledgers,lg,trades,tr,deposit_methods,dm,deposit_addresses,da}
                        available subcommands
    generate_settings   [clikraken] Print default settings.ini to stdout
    asset_pairs (ap)    [public] Get the list of available asset pairs
    ticker (t)          [public] Get the ticker
    depth (d)           [public] Get the current market depth data
    last_trades (lt)    [public] Get the last trades
    ohlc (oh)           [public] Get ohlc data
    balance (bal)       [private] Get your current balance
    trade_balance (tbal)
                        [private] Get your current trade balance
    place (p)           [private] Place an order
    cancel (x)          [private] Cancel orders
    olist (ol)          [private] Get a list of your open orders
    positions (pos)     [private] Get a list of your open positions
    clist (cl)          [private] Get a list of your closed orders
    ledgers (lg)        [private] Get ledgers info
    trades (tr)         [private] Get trades history
    deposit_methods (dm)
                        [private] Get deposit methods
    deposit_addresses (da)
                        [private] Get deposit addresses

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         show program version
  --debug               debug mode
  --raw                 output raw json results from the API
  --csv                 output results from the API as CSV
  --csvseparator CSVSEPARATOR
                        separator character to use with CSV output
  --cron                activate cron mode (tone down errors due to timeouts
                        or unavailable Kraken service)

To get help about a subcommand use: clikraken SUBCOMMAND --help
For example:
    clikraken place --help

Current default currency pair: XETHZEUR.

Create or edit the setting file ~/.config/clikraken/settings.ini to change it.
If the setting file doesn't exist yet, you can create one by doing:
    clikraken generate_settings > ~/.config/clikraken/settings.ini

You can also set the CLIKRAKEN_DEFAULT_PAIR environment variable
which has precedence over the settings from the settings file.
```

Each subcommand has different optional arguments, to get information on how to use a subcommand:

```
clikraken SUBCOMMAND --help
```

For example, the `place` subcommand has the following help:

```
usage: clikraken place [-h] [-l LEVERAGE] [-p PAIR] [-t {market,limit}]
                         [-s STARTTM] [-e EXPIRETM] [-r USERREF] [-q] [-T]
                         [-v]
                         {sell,buy} volume [price]

positional arguments:
  {sell,buy}
  volume
  price

optional arguments:
  -h, --help            show this help message and exit
  -l LEVERAGE, --leverage LEVERAGE
                        leverage for margin trading (default: none)
  -p PAIR, --pair PAIR  asset pair (default: XETHZEUR)
  -t {market,limit}, --ordertype {market,limit}
                        order type. Currently implemented: [limit, market].
                        (default: limit)
  -s STARTTM, --starttm STARTTM
                        scheduled start time (default: 0)
  -e EXPIRETM, --expiretm EXPIRETM
                        expiration time (default: 0)
  -r USERREF, --userref USERREF
                        user reference id. 32-bit signed number. (optional)
                        (default: None)
  -q, --viqc            volume in quote currency (default: False)
  -T, --nopost          disable 'post-only' option (for limit taker orders)
                        (default: False)
  -v, --validate        validate inputs only. do not submit order (default:
                        False)
```

### Usage examples

Notice: Without the `-p` option, the default currency pair is taken from the settings file or the aforementioned environment variable, defaulting to `XETHZEUR` if neither of those exists.

```
clikraken ticker
clikraken balance
clikraken depth
clikraken ohlc --interval 15 --since 1508513700

clikraken place buy -t limit 0.42 11.1337
clikraken place buy -t market 0.1

# without the -t option, defaults to limit orders
clikraken place sell 0.5 13.3701

clikraken cancel OUQUPX-9FBMJ-DL7L6W
```

Using leverage (maximum multiplier allowed depends on the currency pair chosen):

```
# open a short position with 5:1 leverage
clikraken place sell 0.1 -l 5

clikraken positions
clikraken trade_balance

# to close an open position the same volume and leverage should be used
clikraken place buy -t limit 0.1 1492.0 -l 5
```

Examples in another currency pair:

```
# BTC/EUR currency pair
clikraken ticker -p XXBTZEUR
clikraken depth -p XXBTZEUR
clikraken place buy 0.08 587.12 -p XXBTZEUR
clikraken olist -p XXBTZEUR

# ETH/BTC currency pair
clikraken ticker -p XETHXXBT
clikraken depth -p XETHXXBT
clikraken last_trades -p XETHXXBT
```

Global options examples:

```
# format the output as CSV data
clikraken --csv ohlc

# change the separator character for output in CSV format
clikraken --csv --csvseparator "|" ohlc
clikraken --csv --csvseparator "\t" ohlc

# output the raw JSON output from Kraken API
clikraken --raw ticker
```

Store the results in a file:

```
# store the results as CSV file
clikraken --csv ohlc > /path/to/my/results.csv
```

## Upgrade

```
pip install -U clikraken
```

## Attribution

clikraken code is licensed under the Apache license, Version 2.0.
See the `LICENSE` file. For the full text, see [here][corelicense].

## Requirements

Python 3.4+

clikraken is tested with Python 3.4 to 3.6. Future Python versions should be compatible but haven't been tested yet.

There is no plan to support Python 2 at all and it's unlikely that Python 3.0 to 3.3 will ever be supported. Sorry!

clikraken has been tested on Linux (Debian Jessie) and Windows. I guess it should work with other systems but your mileage may vary.

### Dependencies

The dependencies should be automatically installed when installing clikraken with pip.
But if working in a fresh environment (for example after cloning the source code to develop), you may need to install these manually with pip.

* `pip install -r requirements.txt`

The following modules are used by clikraken.

* [krakenex][python3-krakenex] is licensed under the LGPLv3 license.
* [arrow][arrow-license] is licensed under the Apache License, Version 2.0.
* [tabulate][tabulate-license] is licensed under the MIT License.
* [colorlog][colorlog-license] is licensed under the MIT License.

### Development dependencies

The development dependencies are only needed for developing, testing and packaging clikraken.

* GNU Make if using the provided Makefile
* `pip install -r requirements_dev.txt`

## Quickstart for developing on clikraken

### Setup

* Clone this repository and cd into it.
* Preferably create and activate a fresh virtualenv.
  - `python3 -m venv /path/to/your/venv`
  - `source /path/to/your/venv/bin/activate` (for windows, omit `source`)
* If make is available: `make setup_dev`
* Otherwise:
  - `pip install -r requirements.txt`
  - `pip install -r requirements_dev.txt`
  - `python setup.py develop`

### Tests

Tests can be run by calling `tox`.

## Contributors

Special thanks to @t0neg, @citec and @melko for their contributions to clikraken.

[corelicense]: https://www.apache.org/licenses/LICENSE-2.0
[python3-krakenex]: https://github.com/veox/python3-krakenex
[arrow-license]: https://github.com/crsmithdev/arrow/blob/master/LICENSE
[tabulate-license]: https://pypi.python.org/pypi/tabulate
[colorlog-license]: https://github.com/borntyping/python-colorlog
