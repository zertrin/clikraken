# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/) 
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]

### Added
- New setting "traging_agreement", defaulting to "not_agree".

### Fixed
- Fix market orders by adding "trading_agreement = agree" in the AddOrder call.

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

## Added
- Implemented user settings in a INI file ("~/.config/clikraken/settings.ini")
- New subcommand that outputs the contents of the default settings.ini file

## [0.1.1] - 2016-08-20

### Changed
- API key file location moved to '~/.config/clikraken/kraken.key'

[Unreleased]: https://github.com/zertrin/clikraken/compare/0.1.8...HEAD
[0.1.8]: https://github.com/zertrin/clikraken/compare/0.1.7...0.1.8
[0.1.7]: https://github.com/zertrin/clikraken/compare/0.1.6...0.1.7
[0.1.6]: https://github.com/zertrin/clikraken/compare/0.1.5...0.1.6
[0.1.5]: https://github.com/zertrin/clikraken/compare/0.1.4...0.1.5
[0.1.4]: https://github.com/zertrin/clikraken/commit/f8596bd4010feeb53d7d7738eeb58a87fee3e397
[0.1.3]: https://github.com/zertrin/clikraken/commit/101886a6c49e6b1e2ac5dc68a0314f59c2dd5937
[0.1.2]: https://github.com/zertrin/clikraken/compare/0.1.1...0.1.2
[0.1.1]: https://github.com/zertrin/clikraken/commit/bb4f073ce49555bb96e342d64f6212af09489f47

