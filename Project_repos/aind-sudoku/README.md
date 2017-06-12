# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: Solving a Sudoku puzzle with constraint propagation is done through the repeated application of a series of constraints to narrow down the possible solutions in each box. By using the naked twins technique, an additional constraint is added: When two boxes in a unit have the same pair of possible solutions, it can be assumed that no other box in the same unit can have those values; the possible values of the "twins" can be removed from the other possible values of the boxes in the unit of both twins. This reduces the number of possible solutions of the puzzle and makes it easier to solve.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: The constraints used to solve a Sudoku puzzle are based on the concept of units and peers. A unit (rows, columns, and 3x3 squares) is a set of boxes where if a box has a value, the other boxes cannot have the same value. In order to solve the diagonal sudoku problem (among the two main diagonals, the numbers 1 to 9 should all appear exactly once), it is only needed to consider two additional units (and update the peers as needed): the diagonals. This makes it so that the constraints are applied to the diagonals as well.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

