<div align="center">

<h1>mmr-predictor</h1>
![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white)

![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=fff)

![Matplotlib](https://custom-icon-badges.demolab.com/badge/Matplotlib-71D291?logo=matplotlib&logoColor=fff)

![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)

![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=fff)

![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?logo=mongodb&logoColor=white)

<h4>Fun side project to develop a web-tool to predict a player's MMR from game statistics. </h4>
</div>

## About
Dota 2 (Defence of the Ancients 2) is a multiplayer online battle arena video game, where two teams of five players each try to destroy their opponents "Ancient". During the game, each player controls a "hero", each with a different ability set and role.

Each player has a "rank" that is used by the game to match them and form balanced teams for each game. The only way to increase ones rank is to win more games than to lose. 

It is the aim of this project to create a predictive model by analysing large number of Dota 2 games that can accurately predict a player's rank, given how they have performed in a given game.

<div align="center">:construction: This project is work in progress :construction:</div>

## Getting started
### Exploring the project
The repository mainly consists of two parts: Firstly, we have streamlined the collection and processing of match data (see below). On the other hand, you can gain insights into our previous match data analyses in the various Jupyter notebooks located in `src/*`.

### Collecting match data
To collect and parse MMR data from the OpenDota API, run collection script, e.g.

`python3 collect_data_auto.py --output_dir './resources/data' --wait_time 900`

which will call the API every 15 minutes, due to connection restrictions. The data used in the project so far is _not_ included in this repository, so you need to collect the data for yourself!

## Development
### Updates
For the latest changes, see `CHANGELOG.md`

### Setup
This project requires Python 3.11+ as well as packages which you can find in `requirements.txt`. You can install them using PIP

`pip install -r requirements.txt`

We are using a docker-compose backend to efficiently store and query the collected and processed match data. To setup the backend needed for the `mmr_predictor.create_game_db` script you need the Docker daemon to be installed, then call

`docker compose up -d`

### Software testing
Test-driven development is encouraged. To run the pytest based unit tests, make sure you have `pytest` installed, then run

`pytest --verbose`

in the project root directory.

## Overview of Current Dataset

**Total number of parsed matches:** 17048

Below is a short summary of our initial data exploration with the aim of understanding what differentiates a high-rank player from a lower-rank one.

<figure>
    <h3> Distribution of rank tiers across the dataset</h3>
    <img src="resources/plots/initial_feature_selection/rank_tiers_distribution.png" alt="Rank tier distribution">
<figure>
    <h3>Distribution of hero roles across the dataset</h3>
    <img src="resources/plots/initial_feature_selection/hero_role_distr.png" alt="Hero role distribution">
</figure>

<figure>
    <h3>Selected key performance indices per role group</h3>
    <img src="resources/plots/initial_feature_selection/all_stats_mean_per_role_grid.png" alt="Selected key performance indices (KPI) per role group">
</figure>
<figure>
    <h3>Assist and death per game for the support across all ranks</h3>
    <img src="resources/plots/support_feature_exploration/assist_death_per_rank_all.png" alt ="Selected statistics for the support class">
</figure>