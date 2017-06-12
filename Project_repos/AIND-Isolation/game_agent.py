"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass

def final_heuristic(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves - 3 * opp_moves)


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves - 3 * opp_moves) / (len(game.get_blank_spaces()) + 1)


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    filled_spaces = [(i, j) for j in range(game.width) for i in range(game.height) if game._board_state[i + j * game.height] == 1]

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    
    w, h = game.width / 2., game.height / 2.
    y, x = game.get_player_location(player)
    if(game.move_count < 10 and float((h - y)**2 + (w - x)**2)**0.5 <= 2):
        return float(100 - opp_moves)
    else:
        return float(own_moves - 3 * opp_moves)
    # return float(own_moves - 3 * opp_moves) * (len(filled_spaces) - len(game.get_blank_spaces()) + 1)

def custom_score(game, player, startfactor=2, factor=3):
    """
        Return a score for game and player based on the stage of the game, my moves,
        oponent moves (with weight) and moves targeting the center of the board.
        :param game:
        :param player:
        :param startfactor: move quantity threshold for center opening
        :param factor: opponent moves weight
        :return:
        """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    if (game.move_count < factor):
        location = game.get_player_location(player)
        opponent_moves = game.get_legal_moves(game.get_opponent(player))

        if (location[0] >= 2 and location[0] < game.height - 2) and\
            (location[1] >= 2 and location[1] < game.width - 2):
            return float(100 - len(opponent_moves))
        else:
            my_moves = game.get_legal_moves(player)

            return float(len(my_moves) + factor*len(opponent_moves))
    else:
        my_moves = game.get_legal_moves(player)
        opponent_moves = game.get_legal_moves(game.get_opponent(player))

        return float(len(my_moves) + factor*len(opponent_moves))

class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=final_heuristic, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            depth = 1

            while(True):
                best_move = self.minimax(game, depth)
                depth += 1

        except SearchTimeout as timeout:
            return best_move # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax_max_value(self, game, depth):
        """ Returns a candidate move with the max possible value
            Parameters:
            ----------
                game: isolation.Board
                    The state of the game with a certain move applied
                depth: int
                    The current depth, used for iterative deepening
                move: (int, int)
                    The move being tested
            Returns:
            -------
                max_candidate : (move, int)
                    The candidate move with the max possible value
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0:
            return ((-1, -1), self.score(game, self))

        max_candidate = ((-1, -1), float("-inf"))

        for move in game.get_legal_moves(game.active_player):

            score = self.minimax_min_value(game.forecast_move(move), depth -1)[1]

            if score > max_candidate[1]:
                max_candidate = (move, score)

        return max_candidate

    def minimax_min_value(self, game, depth):
        """ Returns a candidate move with the min possible value
            Parameters:
            ----------
                game: isolation.Board
                    The state of the game with a certain move applied
                depth: int
                    The current depth, used for iterative deepening
                move: (int, int)
                    The move being tested
            Returns:
            -------
                min_candidate : (move, int)
                    The candidate move with the min possible value
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0:
            return ((-1, -1), self.score(game, self))

        min_candidate = ((-1, -1), float("inf"))

        for move in game.get_legal_moves(game.active_player):

            score = self.minimax_max_value(game.forecast_move(move), depth -1)[1]

            if score < min_candidate[1]:
                min_candidate = (move, score)

        return min_candidate

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        return self.minimax_max_value(game, depth)[0]


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """ Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        
        best_move = game.get_player_location(game.active_player)
        try:
            depth = 1

            while(True):
                best_move = self.alphabeta(game, depth)
                depth += 1

        except SearchTimeout as timeout:
            return best_move
        # Return the best move from the last completed search iteration
        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return game.get_player_location(game.active_player)
        
        _, move = self.alphabeta_max_value(game, depth, alpha, beta)

        # returns score and first visit of path
        return move

    def alphabeta_max_value(self, game, depth, alpha, beta):
        """ Returns a candidate move with the max possible value
            Parameters:
            ----------
                game: isolation.Board
                    The state of the game with a certain move applied
                depth: int
                    The current depth, used for iterative deepening
                move: (int, int)
                    The move being tested
            Returns:
            -------
                max_candidate : (move, int)
                    The candidate move with the max possible value
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        max_candidate = (float("-inf"), game.get_player_location(game.active_player))
        legal_moves = game.get_legal_moves(game.active_player)

        if depth == 0 or not legal_moves:
            return (self.score(game, self), max_candidate[1])

        for move in legal_moves:
            score = self.alphabeta_min_value(game.forecast_move(move), depth -1, alpha, beta)[0]

            if score > max_candidate[0]:
                max_candidate = (score, move)

            if max_candidate[0] >= beta:
                return (score, move)

            alpha = max(alpha, score)

        return max_candidate

    def alphabeta_min_value(self, game, depth, alpha, beta):
        """ Returns a candidate move with the min possible value. 
            Parameters:
            ----------
                game: isolation.Board
                    The state of the game with a certain move applied
                depth: int
                    The current depth, used for iterative deepening
                move: (int, int)
                    The move being tested
            Returns:
            -------
                min_candidate : (move, int)
                    The candidate move with the min possible value
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        min_candidate = (float("inf"), game.get_player_location(game.active_player))
        legal_moves = game.get_legal_moves(game.active_player)

        if depth == 0 or not legal_moves:
            return (self.score(game, self), min_candidate[1])

        for move in legal_moves:
            score = self.alphabeta_max_value(game.forecast_move(move), depth - 1, alpha, beta)[0]

            if score < min_candidate[0]:
                min_candidate = (score, move)

            if min_candidate[0] <= alpha:
                return (score, move)

            beta = min(beta, score)

        return min_candidate