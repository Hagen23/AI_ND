"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest

import isolation
import game_agent

from importlib import reload

WRONG_MOVE = """
The {} function failed because it returned a non-optimal move at search depth {}.
Valid choices: {}
Your selection: {}
"""

WRONG_NUM_EXPLORED = """
Your {} search visited the wrong nodes at search depth {}.  If the number
of visits is too large, make sure that iterative deepening is only
running when the `iterative` flag is set in the agent constructor.
Max explored size: {}
Number you explored: {}
"""

UNEXPECTED_VISIT = """
Your {} search did not visit the number of expected unique nodes at search
depth {}.
Max explored size: {}
Number you explored: {}
"""

ID_FAIL = """
Your agent explored the wrong number of nodes using Iterative Deepening and
minimax. Remember that ID + MM should check every node in each layer of the
game tree before moving on to the next layer.
"""

INVALID_MOVE = """
Your agent returned an invalid move. Make sure that your function returns
a selection when the search times out during iterative deepening.
Valid choices: {!s}
Your choice: {}
"""

TIMER_MARGIN = 15  # time (in ms) to leave on the timer to avoid timeout

def makeEvalTable(table):
    """Use a closure to create a heuristic function that returns values from
    a table that maps board locations to constant values. This supports testing
    the minimax and alphabeta search functions.
    THIS HEURISTIC IS ONLY USEFUL FOR TESTING THE SEARCH FUNCTIONALITY -
    IT IS NOT MEANT AS AN EXAMPLE OF A USEFUL HEURISTIC FOR GAME PLAYING.
    """

    def score(game, player):
        row, col = game.get_player_location(player)
        return table[row][col]

    return score

class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(game_agent)
        self.player1 = "Player1"
        self.player2 = "Player2"
        self.game = isolation.Board(self.player1, self.player2)

    def initAUT(self, depth, eval_fn, iterative=False,
                method="minimax", loc1=(3, 3), loc2=(0, 0), w=7, h=7):
        """Generate and initialize player and board objects to be used for
        testing.
        """
        reload(game_agent)
        agentUT = game_agent.IsolationPlayer(depth, eval_fn, iterative, method)
        board = CounterBoard(agentUT, 'null_agent', w, h)
        board.apply_move(loc1)
        board.apply_move(loc2)
        return agentUT, board

    def test_minimax(self):
        """ Test CustomPlayer.minimax
        This test uses a scoring function that returns a constant value based
        on the location of the search agent on the board to force minimax to
        choose a branch that visits those cells at a specific fixed-depth.
        If minimax is working properly, it will visit a constant number of
        nodes during the search and return one of the acceptable legal moves.
        """
        h, w = 7, 7  # board size
        starting_location = (2, 3)
        adversary_location = (0, 0)  # top left corner
        iterative_search = False
        method = "minimax"

        # The agent under test starts at position (2, 3) on the board, which
        # gives eight (8) possible legal moves [(0, 2), (0, 4), (1, 1), (1, 5),
        # (3, 1), (3, 5), (4, 2), (4, 4)]. The search function will pick one of
        # those moves based on the estimated score for each branch.  The value
        # only changes on odd depths because even depths end on when the
        # adversary has initiative.
        value_table = [[0] * w for _ in range(h)]
        value_table[1][5] = 1  # depth 1 & 2
        value_table[4][3] = 2  # depth 3 & 4
        value_table[6][6] = 3  # depth 5
        heuristic = makeEvalTable(value_table)

        # These moves are the branches that will lead to the cells in the value
        # table for the search depths.
        expected_moves = [set([(1, 5)]),
                          set([(3, 1), (3, 5)]),
                          set([(3, 5), (4, 2)])]

        # Expected number of node expansions during search
        counts = [(8, 8), (24, 10), (92, 27), (418, 32), (1650, 43)]

        # Test fixed-depth search; note that odd depths mean that the searching
        # player (student agent) has the last move, while even depths mean that
        # the adversary has the last move before calling the heuristic
        # evaluation function.
        for idx in range(5):
            test_depth = idx + 1
            agentUT, board = self.initAUT(test_depth, heuristic,
                                          iterative_search, method,
                                          loc1=starting_location,
                                          loc2=adversary_location)

            # disable search timeout by returning a constant value
            agentUT.time_left = lambda: 1e3
            _, move = agentUT.minimax(board, test_depth)

            num_explored_valid = board.counts[0] == counts[idx][0]
            num_unique_valid = board.counts[1] == counts[idx][1]

            self.assertTrue(num_explored_valid, WRONG_NUM_EXPLORED.format(
                method, test_depth, counts[idx][0], board.counts[0]))

            self.assertTrue(num_unique_valid, UNEXPECTED_VISIT.format(
                method, test_depth, counts[idx][1], board.counts[1]))

            self.assertIn(move, expected_moves[idx // 2], WRONG_MOVE.format(
                method, test_depth, expected_moves[idx // 2], move))


if __name__ == '__main__':
    unittest.main()
