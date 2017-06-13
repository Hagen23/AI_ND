### The following code does not pass the UDACITY-PA tests because I implemented the iterative search differently and within the minimax and alphabeta respectively, instead of within get move. Also, I addressed an issue with forfeiting by keeping a list of values and moves at the iterative deepening, and selecting the best move from that list.

"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass

def custom_score(game, player):
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

    filled_spaces = [(i, j) for j in range(game.width) for i in range(game.height) if game._board_state[i + j * game.height] == 1]

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    
    return float(own_moves - 3 * opp_moves) * (len(filled_spaces) + 1)

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

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves - 3 * opp_moves)

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
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
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
        depth = 1
        
        return self.minimax(game, depth)

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
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return (-1, -1)#game.get_player_location(game.active_player)

        best_move = (float("-inf"), legal_moves[0])
        best_moves = [best_move]

        try:
            depth = 1
            while(True):
                best_move = self.minimax_max_value(game, depth)
                if(best_move not in best_moves):
                    best_moves.append(best_move)
                depth += 1

        except SearchTimeout as timeout:
            return max(best_moves)[1]
            
        return max(best_moves)[1]

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

        legal_moves = game.get_legal_moves(game.active_player)
        max_candidate = (float("-inf"), game.get_player_location(game.active_player))

        if depth == 0 or not legal_moves:
            return (self.score(game, self), max_candidate[1])

        for move in legal_moves:
            score = self.minimax_min_value(game.forecast_move(move), depth -1)[0]

            if score > max_candidate[0]:
                max_candidate = (score, move)

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

        legal_moves = game.get_legal_moves(game.active_player)
        min_candidate = (float("inf"), game.get_player_location(game.active_player))

        if depth == 0 or not legal_moves:
            return (self.score(game, self), min_candidate[1])

        for move in legal_moves:
            score = self.minimax_min_value(game.forecast_move(move), depth -1)[0]

            if score < min_candidate[0]:
                min_candidate = (score, move)

        return min_candidate

    

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
        depth = 1
        return self.alphabeta(game, depth)

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
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return (-1, -1)#game.get_player_location(game.active_player)

        best_move = (float("-inf"), legal_moves[0])
        best_moves = [best_move]

        try:
            depth = 1
            while(True):
                best_move = self.alphabeta_max_value(game, depth, alpha, beta)
                if(best_move not in best_moves):
                    best_moves.append(best_move)
                depth += 1

        except SearchTimeout as timeout:
            # print("Depth reached ", depth)
            return max(best_moves)[1]
        # Return the best move from the last completed search iteration
        return max(best_moves)[1]

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

        legal_moves = game.get_legal_moves(game.active_player)
        max_candidate = (float("-inf"), game.get_player_location(game.active_player))

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

        legal_moves = game.get_legal_moves(game.active_player)
        min_candidate = (float("inf"), game.get_player_location(game.active_player))

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

#### The following code passes all the UDACITY-PA Tests
# """Finish all TODO items in this file to complete the isolation project, then
# test your agent's strength against a set of known agents using tournament.py
# and include the results in your report.
# """
# import random

# class SearchTimeout(Exception):
#     """Subclass base exception for code clarity. """
#     pass

# def custom_score(game, player):
#     """Calculate the heuristic value of a game state from the point of view
#     of the given player.

#     This should be the best heuristic function for your project submission.

#     Note: this function should be called from within a Player instance as
#     `self.score()` -- you should not need to call this function directly.

#     Parameters
#     ----------
#     game : `isolation.Board`
#         An instance of `isolation.Board` encoding the current state of the
#         game (e.g., player locations and blocked cells).

#     player : object
#         A player instance in the current game (i.e., an object corresponding to
#         one of the player objects `game.__player_1__` or `game.__player_2__`.)

#     Returns
#     -------
#     float
#         The heuristic value of the current game state to the specified player.
#     """
#     if game.is_loser(player):
#         return float("-inf")

#     if game.is_winner(player):
#         return float("inf")

#     filled_spaces = [(i, j) for j in range(game.width) for i in range(game.height) if game._board_state[i + j * game.height] == 1]

#     own_moves = len(game.get_legal_moves(player))
#     opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    
#     return float(own_moves - 3 * opp_moves) * (len(filled_spaces) + 1)

# def custom_score_2(game, player):
#     """Calculate the heuristic value of a game state from the point of view
#     of the given player.

#     Note: this function should be called from within a Player instance as
#     `self.score()` -- you should not need to call this function directly.

#     Parameters
#     ----------
#     game : `isolation.Board`
#         An instance of `isolation.Board` encoding the current state of the
#         game (e.g., player locations and blocked cells).

#     player : object
#         A player instance in the current game (i.e., an object corresponding to
#         one of the player objects `game.__player_1__` or `game.__player_2__`.)

#     Returns
#     -------
#     float
#         The heuristic value of the current game state to the specified player.
#     """
#     if game.is_loser(player):
#         return float("-inf")

#     if game.is_winner(player):
#         return float("inf")

#     own_moves = len(game.get_legal_moves(player))
#     opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
#     return float(own_moves - 3 * opp_moves) / (len(game.get_blank_spaces()) + 1)


# def custom_score_3(game, player):
#     """Calculate the heuristic value of a game state from the point of view
#     of the given player.

#     Note: this function should be called from within a Player instance as
#     `self.score()` -- you should not need to call this function directly.

#     Parameters
#     ----------
#     game : `isolation.Board`
#         An instance of `isolation.Board` encoding the current state of the
#         game (e.g., player locations and blocked cells).

#     player : object
#         A player instance in the current game (i.e., an object corresponding to
#         one of the player objects `game.__player_1__` or `game.__player_2__`.)

#     Returns
#     -------
#     float
#         The heuristic value of the current game state to the specified player.
#     """
#     if game.is_loser(player):
#         return float("-inf")

#     if game.is_winner(player):
#         return float("inf")

#     own_moves = len(game.get_legal_moves(player))
#     opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
#     return float(own_moves - 3 * opp_moves)

# class IsolationPlayer:
#     """Base class for minimax and alphabeta agents -- this class is never
#     constructed or tested directly.

#     ********************  DO NOT MODIFY THIS CLASS  ********************

#     Parameters
#     ----------
#     search_depth : int (optional)
#         A strictly positive integer (i.e., 1, 2, 3,...) for the number of
#         layers in the game tree to explore for fixed-depth search. (i.e., a
#         depth of one (1) would only explore the immediate sucessors of the
#         current state.)

#     score_fn : callable (optional)
#         A function to use for heuristic evaluation of game states.

#     timeout : float (optional)
#         Time remaining (in milliseconds) when search is aborted. Should be a
#         positive value large enough to allow the function to return before the
#         timer expires.
#     """
#     def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
#         self.search_depth = search_depth
#         self.score = score_fn
#         self.time_left = None
#         self.TIMER_THRESHOLD = timeout

# class MinimaxPlayer(IsolationPlayer):
#     """Game-playing agent that chooses a move using depth-limited minimax
#     search. You must finish and test this player to make sure it properly uses
#     minimax to return a good move before the search time limit expires.
#     """

#     def get_move(self, game, time_left):
#         """Search for the best move from the available legal moves and return a
#         result before the time limit expires.

#         **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

#         For fixed-depth search, this function simply wraps the call to the
#         minimax method, but this method provides a common interface for all
#         Isolation agents, and you will replace it in the AlphaBetaPlayer with
#         iterative deepening search.

#         Parameters
#         ----------
#         game : `isolation.Board`
#             An instance of `isolation.Board` encoding the current state of the
#             game (e.g., player locations and blocked cells).

#         time_left : callable
#             A function that returns the number of milliseconds left in the
#             current turn. Returning with any less than 0 ms remaining forfeits
#             the game.

#         Returns
#         -------
#         (int, int)
#             Board coordinates corresponding to a legal move; may return
#             (-1, -1) if there are no available legal moves.
#         """
#         self.time_left = time_left
#         # depth = 1
        
#         legal_moves = game.get_legal_moves()
#         if(not legal_moves):
#             return (-1, -1)

#         best_move = legal_moves[0]
        
#         try:
#             depth = 1
#             while(True):
#                 move = self.minimax(game, depth)
#                 if(move != (-1, -1)):
#                     best_move = move
#                 depth += 1

#         except SearchTimeout as timeout:
#             return best_move
            
#         return best_move

#         # return self.minimax(game, depth)

#     def minimax(self, game, depth):
#         """Implement depth-limited minimax search algorithm as described in
#         the lectures.

#         This should be a modified version of MINIMAX-DECISION in the AIMA text.
#         https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

#         **********************************************************************
#             You MAY add additional methods to this class, or define helper
#                  functions to implement the required functionality.
#         **********************************************************************

#         Parameters
#         ----------
#         game : isolation.Board
#             An instance of the Isolation game `Board` class representing the
#             current game state

#         depth : int
#             Depth is an integer representing the maximum number of plies to
#             search in the game tree before aborting

#         Returns
#         -------
#         (int, int)
#             The board coordinates of the best move found in the current search;
#             (-1, -1) if there are no legal moves

#         Notes
#         -----
#             (1) You MUST use the `self.score()` method for board evaluation
#                 to pass the project tests; you cannot call any other evaluation
#                 function directly.

#             (2) If you use any helper functions (e.g., as shown in the AIMA
#                 pseudocode) then you must copy the timer check into the top of
#                 each helper function or else your agent will timeout during
#                 testing.
#         """

#         if self.time_left() < self.TIMER_THRESHOLD:
#             raise SearchTimeout()

#         # legal_moves = game.get_legal_moves()
#         # if not legal_moves:
#         #     return (-1, -1)#game.get_player_location(game.active_player)

#         # best_move = (float("-inf"), legal_moves[0])
#         # best_moves = [best_move]

#         # try:
#         #     depth = 1
#         #     while(True):
#         #         best_move = self.minimax_max_value(game, depth)
#         #         if(best_move not in best_moves):
#         #             best_moves.append(best_move)
#         #         depth += 1

#         # except SearchTimeout as timeout:
#         #     return max(best_moves)[1]
            
#         # return max(best_moves)[1]

#         return self.minimax_max_value(game, depth)[1]

#     def minimax_max_value(self, game, depth):
#         """ Returns a candidate move with the max possible value
#             Parameters:
#             ----------
#                 game: isolation.Board
#                     The state of the game with a certain move applied
#                 depth: int
#                     The current depth, used for iterative deepening
#                 move: (int, int)
#                     The move being tested
#             Returns:
#             -------
#                 max_candidate : (move, int)
#                     The candidate move with the max possible value
#         """
#         if self.time_left() < self.TIMER_THRESHOLD:
#             raise SearchTimeout()

#         legal_moves = game.get_legal_moves(game.active_player)
#         max_candidate = (float("-inf"), game.get_player_location(game.active_player))

#         if depth == 0 or not legal_moves:
#             return (self.score(game, self), max_candidate[1])

#         for move in legal_moves:
#             score = self.minimax_min_value(game.forecast_move(move), depth -1)[0]

#             if score > max_candidate[0]:
#                 max_candidate = (score, move)

#         return max_candidate

#     def minimax_min_value(self, game, depth):
#         """ Returns a candidate move with the min possible value
#             Parameters:
#             ----------
#                 game: isolation.Board
#                     The state of the game with a certain move applied
#                 depth: int
#                     The current depth, used for iterative deepening
#                 move: (int, int)
#                     The move being tested
#             Returns:
#             -------
#                 min_candidate : (move, int)
#                     The candidate move with the min possible value
#         """
#         if self.time_left() < self.TIMER_THRESHOLD:
#             raise SearchTimeout()

#         legal_moves = game.get_legal_moves(game.active_player)
#         min_candidate = (float("inf"), game.get_player_location(game.active_player))

#         if depth == 0 or not legal_moves:
#             return (self.score(game, self), min_candidate[1])

#         for move in legal_moves:
#             score = self.minimax_max_value(game.forecast_move(move), depth -1)[0]

#             if score < min_candidate[0]:
#                 min_candidate = (score, move)

#         return min_candidate

    

# class AlphaBetaPlayer(IsolationPlayer):
#     """Game-playing agent that chooses a move using iterative deepening minimax
#     search with alpha-beta pruning. You must finish and test this player to
#     make sure it returns a good move before the search time limit expires.
#     """

#     def get_move(self, game, time_left):
#         """ Search for the best move from the available legal moves and return a
#         result before the time limit expires.

#         Modify the get_move() method from the MinimaxPlayer class to implement
#         iterative deepening search instead of fixed-depth search.

#         **********************************************************************
#         NOTE: If time_left() < 0 when this function returns, the agent will
#               forfeit the game due to timeout. You must return _before_ the
#               timer reaches 0.
#         **********************************************************************

#         Parameters
#         ----------
#         game : `isolation.Board`
#             An instance of `isolation.Board` encoding the current state of the
#             game (e.g., player locations and blocked cells).

#         time_left : callable
#             A function that returns the number of milliseconds left in the
#             current turn. Returning with any less than 0 ms remaining forfeits
#             the game.

#         Returns
#         -------
#         (int, int)
#             Board coordinates corresponding to a legal move; may return
#             (-1, -1) if there are no available legal moves.
#         """
#         # self.time_left = time_left
#         # depth = 1
#         # return self.alphabeta(game, depth)

#         self.time_left = time_left

#         # Initialize the best move so that this function returns something
#         # in case the search fails due to timeout
        
#         legal_moves = game.get_legal_moves()
#         if(not legal_moves):
#             return (-1, -1)

#         best_move = legal_moves[0]

#         try:
#             depth = 1

#             while(True):
#                 move = self.alphabeta(game, depth)
#                 if(move != (-1, -1)):
#                     best_move = move
#                 depth += 1

#         except SearchTimeout as timeout:
#             return best_move
#         # Return the best move from the last completed search iteration
#         return best_move

#     def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
#         """Implement depth-limited minimax search with alpha-beta pruning as
#         described in the lectures.

#         This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
#         https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

#         **********************************************************************
#             You MAY add additional methods to this class, or define helper
#                  functions to implement the required functionality.
#         **********************************************************************

#         Parameters
#         ----------
#         game : isolation.Board
#             An instance of the Isolation game `Board` class representing the
#             current game state

#         depth : int
#             Depth is an integer representing the maximum number of plies to
#             search in the game tree before aborting

#         alpha : float
#             Alpha limits the lower bound of search on minimizing layers

#         beta : float
#             Beta limits the upper bound of search on maximizing layers

#         Returns
#         -------
#         (int, int)
#             The board coordinates of the best move found in the current search;
#             (-1, -1) if there are no legal moves

#         Notes
#         -----
#             (1) You MUST use the `self.score()` method for board evaluation
#                 to pass the project tests; you cannot call any other evaluation
#                 function directly.

#             (2) If you use any helper functions (e.g., as shown in the AIMA
#                 pseudocode) then you must copy the timer check into the top of
#                 each helper function or else your agent will timeout during
#                 testing.
#         """
#         # legal_moves = game.get_legal_moves()
#         # if not legal_moves:
#         #     return (-1, -1)#game.get_player_location(game.active_player)

#         # best_move = (float("-inf"), legal_moves[0])
#         # best_moves = [best_move]

#         # try:
#         #     depth = 1
#         #     while(True):
#         #         best_move = self.alphabeta_max_value(game, depth, alpha, beta)
#         #         if(best_move not in best_moves):
#         #             best_moves.append(best_move)
#         #         depth += 1

#         # except SearchTimeout as timeout:
#         #     # print("Depth reached ", depth)
#         #     return max(best_moves)[1]
#         # # Return the best move from the last completed search iteration
#         # return max(best_moves)[1]

#         if self.time_left() < self.TIMER_THRESHOLD:
#             raise SearchTimeout()

#         legal_moves = game.get_legal_moves()
#         if not legal_moves:
#             return game.get_player_location(game.active_player)
        
#         _, move = self.alphabeta_max_value(game, depth, alpha, beta)

#         # returns score and first visit of path
#         return move

#     def alphabeta_max_value(self, game, depth, alpha, beta):
#         """ Returns a candidate move with the max possible value
#             Parameters:
#             ----------
#                 game: isolation.Board
#                     The state of the game with a certain move applied
#                 depth: int
#                     The current depth, used for iterative deepening
#                 move: (int, int)
#                     The move being tested
#             Returns:
#             -------
#                 max_candidate : (move, int)
#                     The candidate move with the max possible value
#         """
#         if self.time_left() < self.TIMER_THRESHOLD:
#             raise SearchTimeout()

#         legal_moves = game.get_legal_moves(game.active_player)
#         max_candidate = (float("-inf"), game.get_player_location(game.active_player))

#         if depth == 0 or not legal_moves:
#             return (self.score(game, self), max_candidate[1])

#         for move in legal_moves:
#             score = self.alphabeta_min_value(game.forecast_move(move), depth -1, alpha, beta)[0]

#             if score > max_candidate[0]:
#                 max_candidate = (score, move)

#             if max_candidate[0] >= beta:
#                 return (score, move)

#             alpha = max(alpha, score)

#         return max_candidate

#     def alphabeta_min_value(self, game, depth, alpha, beta):
#         """ Returns a candidate move with the min possible value. 
#             Parameters:
#             ----------
#                 game: isolation.Board
#                     The state of the game with a certain move applied
#                 depth: int
#                     The current depth, used for iterative deepening
#                 move: (int, int)
#                     The move being tested
#             Returns:
#             -------
#                 min_candidate : (move, int)
#                     The candidate move with the min possible value
#         """
#         if self.time_left() < self.TIMER_THRESHOLD:
#             raise SearchTimeout()

#         legal_moves = game.get_legal_moves(game.active_player)
#         min_candidate = (float("inf"), game.get_player_location(game.active_player))

#         if depth == 0 or not legal_moves:
#             return (self.score(game, self), min_candidate[1])

#         for move in legal_moves:
#             score = self.alphabeta_max_value(game.forecast_move(move), depth - 1, alpha, beta)[0]

#             if score < min_candidate[0]:
#                 min_candidate = (score, move)

#             if min_candidate[0] <= alpha:
#                 return (score, move)

#             beta = min(beta, score)

#         return min_candidate
