# mmr-predictor

## About
Fun side project to develop a web-tool to predict a player's MMR from game statistics. 

Dota 2 (Defence of the Ancients 2) is a multiplayer online battle arena video game, where two teams of five players each try to destroy their opponents "Ancient". During the game, each player controls a "hero", each with a different ability set and role.

Each player has a "rank" that is used by the game to match them and form balanced teams for each game. The only way to increase ones rank is to win more games than to lose. 

It is the aim of this project to create a predictive model by analysing large number of Dota 2 games that can accurately predict a player's rank, given how they have performed in a given game.

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