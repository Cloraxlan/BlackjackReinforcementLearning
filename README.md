Class: CSC 4631\
Section: 111\
Names: Konrad Rozpadek, Kalki Sarangan

# Overview

Problem: Blackjack\
Gameplay & Rules:\
-- Players can hit or stand\
-- Goal is to try to get higher than the dealer without going bust\
-- After stand, dealer hits until a threshold

Agents:
- Random
- Card Counting with Illustrious 18
- QLearning with value of player hand
- QLearning with value of player and dealer hand

Goal of this project:\
Could a QLearning agent beat Card Counting?

# Description of each file (excluding program result files)

agent.py - File implementing various agents including random, card counting, qlearning.\
blackjack.py - File implementing the class to simulate a game of blackjack.\
main.py - File implementing methods to play 1 or more round(s) of blackjack, and play a demo round.\
visualizations.py - File implementing methods for various plots to compare agents, or performance of the agents.\
generate_visualizations.ipynb - Generates visualizations used in presentations using optimal hyperparameters.\
hyperparam_search.ipynb - Uses grid search with epoch count of 10000 to search for optimal hyperparams for both versions of the state.

# Description of each folder

table - Folder containing pickle files of the generated q-tables for various epoch sizes and state representations.

# Instructions for compiling and running the code. Including libraries that need installation.
-- SKLearn, Numpy and MatPlotLib are required libraries for this project.\
Command to run the program:\
-- python3 main.py

# Location of the code outputs and how they're interpreted
The results are the bar plots that show the comparison between agents, agent wins, performance with epoch sizes located in generate_visualizations.ipynb