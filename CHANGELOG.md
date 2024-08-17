# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2024-08-16
### Added
- Introduced basic logging
- Experimental function `get_latest_match_ids` to get match data from the /explorer endpoint based on Postgres SQL query ([#3](https://github.com/batukav/mmr-predictor/issues/3))
- CHANGELOG and project versioning

### Changed
- Refactored parts of the collection script, split code into functions (the actual data cleaning remains unchanged)
- Improved the error handling using exceptions


## [0.1] - 2024-08-16
### Added
- Added script to fetch parsed matches from the OpenDota API
- Filter collected matches and store them as JSON files
- Added sample pytest setup for Github Actions CI