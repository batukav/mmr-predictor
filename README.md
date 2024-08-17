# mmr-predictor

## About
Fun side project to develop a web-tool to predict a player's MMR from game statistics.

:construction: This project is work in progress :construction:

## Getting started
### Collect data
To collect and parse MMR data from the OpenDota API, run collection script, e.g.

`python3 collect_data_auto.py --output_dir './resources/data' --wait_time 900`

which will call the API every 15 minutes, due to connection restrictions.

## Development
### Updates
For the latest changes, see CHANGELOG.md

### Setup
This project requires Python 3.11+ as well as packages which you can find in `requirements.txt`. You can install them using PIP

`pip install -r requirements.txt`

### Software testing
Test-driven development is encouraged. To run the pytest based unit tests, make sure you have `pytest` installed, then run

`pytest --verbose`

in the project root directory.
