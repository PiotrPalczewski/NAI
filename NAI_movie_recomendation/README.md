# NAI - recomendation engine
Finding corelation beetwen users uploaded from .json file to recomend movies.

## Table of contents

* [Introdicton](#introduction)
* [Technologies](#Technologies)
* [Setup](#Setup)
* [Features](#features)
* [Code examples](#code-examples)

## Introduction
University project created to find corelation between data sets provided by users that watched and scored movies with main assumption that atleast some of the movies will be shared among users. 
Main function of the application is to find the most compalitble (the closest corelation between users) user, then to find movies not watched by primary user and recommend the higest rated movies along side with the worst as not recommended.

## Technologies
Project created using:

* Python 3.8.3
* NumPy 1.19.0
* Click 7.2

## Setup
To run this application you will need Git installed on your computer. From command line:
```
# Clone this repository
$ git clone https://github.com/https://github.com/PiotrPalczewski/NAI/tree/main/NAI_movie_recomendation

# Go into the repository
$ cd NAI_movie_recomendation

# Run the app
$ npm run
```

## Features
* importing user movies scores by json
* finding corelation between users using euclidean or Pearson scores
* finding not watched movies with high and low scores in best corelation users (until finding x number of movies)

### To do (potentialy):
* web scrapping

## Code examples
Most notable parts of code are:

* '_pearson_score'
Method used to compute Pearson score between two users. Uses arguments: user1 and user2 (as strings) and returns score (float).
More about Pearson score please refere to this [link](https://en.wikipedia.org/wiki/Pearson_correlation_coefficient).
Below the mathematical part of the method:
```
        # counting sums of common movies ratings
        user1_sum = np.sum([self._data[user1][item] for item in common_movies])
        user2_sum = np.sum([self._data[user2][item] for item in common_movies])

        # counting squared sums of common movies ratings
        user1_squared_sum = np.sum(
            [np.square(self._data[user1][item]) for item in common_movies]
        )
        user2_squared_sum = np.sum(
            [np.square(self._data[user2][item]) for item in common_movies]
        )

        sum_of_products = np.sum(
            [
                self._data[user1][item] * self._data[user2][item]
                for item in common_movies
            ]
        )

        # getting Pearson's coefficients
        Sxy = sum_of_products - (user1_sum * user2_sum / num_ratings)
        Sxx = user1_squared_sum - np.square(user1_sum) / num_ratings
        Syy = user2_squared_sum - np.square(user2_sum) / num_ratings
```
The score is presented as a:
```
return Sxy / np.sqrt(Sxx * Syy)
```

* '_euclidean_score'
Method used to compute euclidean distance between two users on Euclidean space (more [here](https://en.wikipedia.org/wiki/Euclidean_distance)). Uses arguments user1 and user2 (as strings) and returns score (as float).
Method main function is:
```
 # squared difference between points (movies)
        squared_diff = []

        for item in self._data[user1]:
            if item in self._data[user2]:
                squared_diff.append(
                    np.square(self._data[user1][item] - self._data[user2][item])
                )
```
The result score is presented as:
```
return 1 / (1 + np.sqrt(np.sum(squared_diff)))
```
* 'find_recommendations'
