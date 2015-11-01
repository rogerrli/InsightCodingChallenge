#!/usr/bin/env bash
# execute python program tweets_cleaned.py, use data from tweets.txt, and print the cleaned tweets and average vertex
# degree into ft1.txt and ft2.txt respectively.
python -m py_compile ./src/tweets_cleaned.py
python ./src/tweets_cleaned.py ./tweet_input/tweets.txt ./tweet_output/ft1.txt ./tweet_output/ft2.txt
