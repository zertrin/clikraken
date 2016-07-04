# clikraken

Command-line client for the Kraken exchange

## Installation

This software is in development. You should install it in a virtualenv.

### Step 1: Create a virtualenv

```
pyvenv ~/.venv/clikraken
```

And activate it:

```
source ~/.venv/clikraken/bin/activate
```

### Step 2: Install dependancies

clikraken depends on two external modules:

* `arrow`, for better handling of date and time
* `python3-krakenex`, for the low-level interface with the Kraken API

Somehow you need to install the two dependencies manually before installing clikraken.

I haven't been successfull in making the dependency system of pip work consistently yet.

Install arrow in the activated virtualenv:

```
pip install arrow
```

Install python3-krakenex in the activated virtualenv:

```
pip install -e "git+https://github.com/veox/python3-krakenex.git@33b758f1f56257a35da85b0b14eb9cb1afb7b045#egg=krakenex-20160418"
```

### Step 3: Install clikraken

```
# make sure you have installed arrow and krakenex before!
pip install clikraken
```

### Step4: Add your API key in the `$HOME/.config/kraken.key` file

You will need it to perform private queries to the Kraken API.

```
keykeykeykeykeykeykeykeykeykeykeykeykeykeykeykeykeykeykey
secretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecret
```

## Usage

First activate the virtualenv:

```
source ~/.venv/clikraken/bin/activate
```
Get help:

```
clikraken --help
```

## Attribution

clikraken code is licensed under the Apache license, Version 2.0.
It should be available in `LICENSE`. If not, see [here][corelicense].

### Dependencies

* [python3-krakenex][python3-krakenex] code is licensed under the LGPLv3 license.
* [Arrow][arrow-license] code is licensed under is licensed under the Apache License, Version 2.0.

[corelicense]: https://www.apache.org/licenses/LICENSE-2.0
[python3-krakenex]: https://github.com/veox/python3-krakenex
[arrow-license]: https://github.com/crsmithdev/arrow/blob/master/LICENSE
