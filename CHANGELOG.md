# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/) 
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]
### Changed
- Silence 'EAPI:Invalid nonce' errors while in cron mode

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

[Unreleased]: https://github.com/zertrin/clikraken/compare/0.2.4...HEAD
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

