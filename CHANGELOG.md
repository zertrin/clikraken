# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/) 
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]
- placeholder

## [0.6.1] - 2017-06-15
- Fix issue #6: force tabulate to represent floats with more decimals.
- Fix issue #7: 4-letter asset pairs aren't correctly displayed
- add Makefile commands `setup_dev` and `test` to facilitate setting a development environment up.

## [0.6.0] - 2017-04-28
- Add new subcommand "asset_pairs" (alias "ap") to list the available asset pairs (thanks t0neg)
- Add setting "ticker_currency_pairs" for the default asset pair list for the ticker subcommand. Default value is XBTUSD,XBTEUR,ETHUSD,ETHEUR

## [0.5.0] - 2017-04-01
- List open and closed orders are not filtered automatically anymore unless explicitly specified by `--pair` parameter. (by t0neg)
- Allow to use short version of asset pair (e.g. ETHEUR) in addition to the fully qualified version (e.g. XETHZEUR) when filtering results of list open and closed orders. (by t0neg)
- Add `requirements.txt`.
- Add `--debug` top-level option. Does not do much at the moment. In combination with the `--raw` option, shows normal clikraken's output in addition to the raw JSON output.

## [0.4.2] - 2017-03-31
- Remove setup.cfg setting "universal wheel", since this project is nt python2 compatible at all.

## [0.4.1] - 2017-03-31
- Add Appveyor CI for windows testing.
- Remove cram from the test framework since it's not usable on windows.
- Clikraken is now officially compatible with Python 3.5 and 3.6.

## [0.4.0] - 2017-03-30
- Put the source under src folder and slightly restructure package to make it more stable and suitable to development and testing.
- Introduce test framework using tox, pytest, flake8 and cram.
- Introduce CI with Travis-CI.

## [0.3.2] - 2017-03-16
- Loosen the check on the API keyfile. Allow public API queries even if no keyfile is available.

## [0.3.1] - 2017-03-16
- Allow 'cancel' subcommand to take many order IDs.

## [0.3.0] - 2017-03-13
### Changed
- Include timezone in timestamp outputs.

## [0.2.5] - 2017-03-13
### Changed
- Silence 'EAPI:Invalid nonce' errors while in cron mode.

## [0.2.4] - 2017-02-13
### Changed
- Catch http.client.BadStatusLine while querying Kraken's API and silence it while in cron mode.

## [0.2.3] - 2016-12-29
### Changed
- Catch ValueError while querying Kraken's API and silence it while in cron mode.

## [0.2.2] - 2016-12-11
### Added
- Add a `--cron` option that downgrades errors related to the communication with Kraken's API (for example TimeoutError or ConnectionResetError) from ERROR to INFO level. Together with the change described below, this means that those errors are now sent to stdout instead of stderr when cron mode is active. So you can use the new option together with `1>/dev/null` in a cron script and avoid being spammed when Kraken is not available.

### Changed
- Logging now sends DEBUG and INFO messages to stdout, and WARNING and above to stderr (previously all was sent to stderr).
- If available, call `win_unicode_console.enable()` to fix issues with unicode characters in Windows console.

## [0.2.1] - 2016-11-20

### Changed
- Big refactoring: get rid of the monolithic clikraken.py and split the code into many smaller modules.
- Use pypandoc.convert_file() in setup.py since pypandoc.convert() is now deprecated.
- Add a hint on how to get help about a subcommand in the main help string.

## [0.2.0] - 2016-11-05

### Added
- New environment variable CLIKRAKEN_DEFAULT_PAIR to override the default currency pair.
- New environment variable CLIKRAKEN_API_KEYFILE to override the default keyfile location.
- New environment variable CLIKRAKEN_USER_SETTINGS_PATH to override the default user settings file location.
- Add short alias "p" for the "place" command.
- Do proper logging of info/warning/error messages.
- Log lines will be colorized on terminal if colorlog is available (pip install colorlog).

### Changed
- Remove manual steps in the README concerning manual installation of dependencies. Now that python3-krakenex is packaged on PyPI, it is not necessary anymore.

## [0.1.9] - 2016-10-29

### Added
- New setting "trading_agreement", defaulting to "not_agree".

### Fixed
- Fix market orders by adding "trading_agreement" in the AddOrder call.

## [0.1.8] - 2016-10-23

### Added
- Add link to PyPI package page in the README.

### Fixed
- Fix bug when Kraken API returns no error field.

## [0.1.7] - 2016-10-22

### Added
- Add a real CHANGELOG.
- Usage examples in the README.
- Always print errors coming from Kraken API.
- Pretty-print output of PlaceOrder and CancelOrder API Calls.

### Fixed
- Market orders now work, price is an optional argument.

### Changed
- Option to show program version changed from '-v' to '-V'.
- Do not force the price to be of Decimal type. Allows to use relative price.
- ticker: dynamic unit prefixing for volume value.

## [0.1.6] - 2016-09-26

### Added
- Add short aliases to ticker, depth and cancel commands

## [0.1.5] - 2016-08-22

### Fixed
- Fix sorting by prices by casting to Decimal.

## [0.1.4] - 2016-08-21

### Fixed
- Catch ValueError raised from krakenex when the API response is empty

## [0.1.3] - 2016-08-20

### Changed
- Some rework and clarifications in the README

## [0.1.2] - 2016-08-20

### Added
- Implemented user settings in a INI file ("~/.config/clikraken/settings.ini")
- New subcommand that outputs the contents of the default settings.ini file

## [0.1.1] - 2016-08-20

### Changed
- API key file location moved to '~/.config/clikraken/kraken.key'

[Unreleased]: https://github.com/zertrin/clikraken/compare/0.6.1...HEAD
[0.6.1]: https://github.com/zertrin/clikraken/compare/0.6.0...0.6.1
[0.6.0]: https://github.com/zertrin/clikraken/compare/0.5.0...0.6.0
[0.5.0]: https://github.com/zertrin/clikraken/compare/0.4.2...0.5.0
[0.4.2]: https://github.com/zertrin/clikraken/compare/0.4.1...0.4.2
[0.4.1]: https://github.com/zertrin/clikraken/compare/0.4.0...0.4.1
[0.4.0]: https://github.com/zertrin/clikraken/compare/0.3.2...0.4.0
[0.3.2]: https://github.com/zertrin/clikraken/compare/0.3.1...0.3.2
[0.3.1]: https://github.com/zertrin/clikraken/compare/0.3.0...0.3.1
[0.3.0]: https://github.com/zertrin/clikraken/compare/0.2.5...0.3.0
[0.2.5]: https://github.com/zertrin/clikraken/compare/0.2.4...0.2.5
[0.2.4]: https://github.com/zertrin/clikraken/compare/0.2.3...0.2.4
[0.2.3]: https://github.com/zertrin/clikraken/compare/0.2.2...0.2.3
[0.2.2]: https://github.com/zertrin/clikraken/compare/0.2.1...0.2.2
[0.2.1]: https://github.com/zertrin/clikraken/compare/0.2.0...0.2.1
[0.2.0]: https://github.com/zertrin/clikraken/compare/0.1.9...0.2.0
[0.1.9]: https://github.com/zertrin/clikraken/compare/0.1.8...0.1.9
[0.1.8]: https://github.com/zertrin/clikraken/compare/0.1.7...0.1.8
[0.1.7]: https://github.com/zertrin/clikraken/compare/0.1.6...0.1.7
[0.1.6]: https://github.com/zertrin/clikraken/compare/0.1.5...0.1.6
[0.1.5]: https://github.com/zertrin/clikraken/compare/0.1.4...0.1.5
[0.1.4]: https://github.com/zertrin/clikraken/commit/f8596bd4010feeb53d7d7738eeb58a87fee3e397
[0.1.3]: https://github.com/zertrin/clikraken/commit/101886a6c49e6b1e2ac5dc68a0314f59c2dd5937
[0.1.2]: https://github.com/zertrin/clikraken/compare/0.1.1...0.1.2
[0.1.1]: https://github.com/zertrin/clikraken/commit/bb4f073ce49555bb96e342d64f6212af09489f47

