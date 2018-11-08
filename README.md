# Chess Predictions

This repository contains 3 different main applications to create and serve a model api including:

* `transformation/` - this application takes a pgn file and converts it into a csv to be read and translated by the pipeline into a model
* `pipeline/` - this application will take a csv of game states and create a machine learning model to be consumed by the service
* `api/` - this `flask` application will handle incoming REST Json calls and make a prediction based on the specific model

This repository also contains folders for storing and exploring the data for the models:

* `notebooks/` - this folder contains preliminary and final data exploration and initial model building to guide the project
* `data/` - this folder contains the raw pgn and csv files consumed by the `transformation` and `pipeline`
* `models/` - this folder contains the models generated from `pipeline`

### API Documentation

There are 3 model endpoints that all take the same Json object:

* `/prediction/linear` - `[POST]`
* `/prediction/logistic` - `[POST]`
* `/prediction/random_forest` - `[POST]`

The POST body is a single level Json object with the total count for each type of piece for each player and the total number of pieces for the player in the form of `'[Black|White][Pawns|Rooks|Bishops|Knights|Queen|King|Total]'`

Each square will have 2 corresponding fields of `a2_color` of values null, 1, or 2, and `a2_piece` of values null, 'P', 'R', 'B', 'N', 'Q', or 'K'

The returned Json object will be the type of `{ prediction: number }`
