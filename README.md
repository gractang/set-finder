# set -- SetFinder
## One-page overview
### Summary
A program that uses computer vision to find and evaluate Sets from a photograph of a Set game.

### Project Proposal (modified)
Ever play a game of Set and think, “Wow, there’s no Set here! Or maybe I’m just stupid. Guess I’ll deal another card.” Ever feel that sense of disappointment because it’s supposed to be a 1 in 15 to 30 chance that there’s no Set in the 12 cards, but you haven’t found one in the past three boards? SUFFER NO MORE!! With the new SetFinder7000™, you can take a photo of your game and instantly know not only whether you missed a Set or not, but also all the Sets that you overlooked in your feeble attempt to be competent at the game! For just a measly $4.20, all your Set problems will disappear! Preorder today.

Okay, but actually… 

I hope to use computer vision image processing to recognize the patterns in the Set cards, turn those patterns into a data structure representing the board, then code a program to solve for the Sets. It would also be nice to create a nice user interface, perhaps through iOS app development; I will evaluate the plausibility of doing so as my work on the program progresses.  I intend to learn primarily about machine learning applications on pattern recognition and to identify effective ways to store and evaluate the game. At the end of the project, I hope to at the bare minimum have a way of recognizing the various cards, and hopefully (if time allows) implement a solver and UI as well. 

## Design
### Definitional Terminology
Card - A card that has four characteristics: Number, Color, Fill, and Shape. 
	Number - 1, 2, or 3
	Color - Red, Green, or Purple
	Fill - Solid, Striped, or Empty
	Shape - Oval, Diamond, or Squiggle

Set - A group of three Cards, of which each characteristic on the three cards is either all the same or all different.

Board - The cards from which the SetFinder will find sets. Usually consists of twelve Cards, but can be more if there are no Sets present in the twelve-card Board.

### Image Recognition
Goal: Uses image to return data representation of the Cards in the Board
General idea:
Detect edges of Cards (contrast between light and dark w/ edges)
Detect Number (similar to detecting Cards), Color (using pixel colors), Fill (average pixel brightness?), and Shape (similar to detecting Cards)
Change the info into the Card representation (see below)
### Solver
Goal: Uses data from image recognition to find all the Sets in the Board. 
Program logic:
  Card Representation
    Array of four integers
    The values of the integers can be 0, 1, or 2
    Each index and each value represents a certain characteristic
    Ex {0, 0, 0, 0} is a Card with the pattern 1 Red Solid Oval
  Actual logic
    For every three cards, check if sum of “columns” mod 3 == 0
    If so, is a set
### Interface (TBD)
  Goal: Use phone camera to take picture and send to program
  Might need to know: iOS dev tools

## Metrics
### Success
Using OpenCV, I can check the percent confidence of the model in predicting patterns. I’ll use these to evaluate its success!

## Core principle considerations
### Speed
Python. For the solver, shouldn’t be an issue given the small size of the board. Unsure how long the computer vision thing will take, but ideally under a few seconds.
### Correctness
Whether or not the Sets are detected, and whether those Sets are legitimate.
Take a lot of pictures of boards, then run them through the program. 

## TODO
- fill
- potential followup: making an iOS app that uses phone camera to provide input.
