#!/usr/bin/env python
from game import Board, game_as_text
from random import randint
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format="%(message)s")
logger = logging.getLogger()

# This file is your main submission that will be graded against. Do not
# add any classes or functions to this file that are not part of the classes
# that we want.


class OpenMoveEvalFn:

    def score(self, game, maximizing_player_turn=True):
        """Score the current game state

        Evaluation function that outputs a score equal to how many
        moves are open for AI player on the board minus how many moves
        are open for Opponent's player on the board.
        Note:
            1. Be very careful while doing opponent's moves. You might end up
               reducing your own moves.
            3. If you think of better evaluation function, do it in CustomEvalFn below.

            Args
                param1 (Board): The board and game state.
                param2 (bool): True if maximizing player is active.

            Returns:
                float: The current state's score. MyMoves-OppMoves.

            """

        # TODO: finish this function!
        p1=len(game.get_legal_moves())
        p2=len(game.get_opponent_moves())
        if maximizing_player_turn:
            return p1 - p2
        else: 
            return p2-p1

        raise NotImplementedError

class CustomEvalFn:
    def __init__(self):
        pass
    def is_on_border(game, position):
        r,c = position
        if r == 0 or r == game.height - 1 or c == 0 or c == game.width - 1:
            return True
        return False
    def is_first(game):
        if (len(game.get_legal_moves()) == game.width*game.height):
            return True
        else: return False
    def score(self, game, maximizing_player_turn=True):
        if maximizing_player_turn:
            p1_moves = len(game.get_legal_moves())
            p2_moves = len(game.get_opponent_moves())

            p1_position = game.__last_queen_move__[game.__active_players_queen__][:2]
            p2_position = game.__last_queen_move__[game.__inactive_players_queen__][:2]
        else:
            p2_moves = len(game.get_legal_moves())
            p1_moves = len(game.get_opponent_moves())

            p2_position = game.__last_queen_move__[game.__active_players_queen__][:2]
            p1_position = game.__last_queen_move__[game.__inactive_players_queen__][:2]
            
        result=0
        result+= (p1_moves - p2_moves)
        if CustomEvalFn.is_on_border(game,p2_position):
            result += 5
        if CustomEvalFn.is_on_border(game,p1_position):
            result -= 5
            
        return result;
            # Get the active and inactive players
            #custom_player_queen=game.__queen_2__
            #print("custome queen: ",custom_player_queen)
            #active_player = game.__active_player__
            #inactive_player = game.__inactive_player__
#
            ## Calculate mobility: number of legal moves
            #active_moves = len(game.get_legal_moves())
            #inactive_moves = len(game.get_opponent_moves())
#
            ## Central control: prioritize positions near the center of the board
            #board_width, board_height = game.width, game.height
            #center_x, center_y = board_width / 2, board_height / 2
#
            #def distance_to_center(position):
            #    return abs(position[0] - center_x) + abs(position[1] - center_y)
#
            #
            ## Get player positions
            #active_position = game.__last_queen_move__[game.__active_players_queen__][:2]
            #inactive_position = game.__last_queen_move__[game.__inactive_players_queen__][:2]
            #inactive_x, inactive_y = inactive_position
            #print("active: ",game.__active_players_queen__,": ",active_position)
            #print("inactive: ",game.__inactive_players_queen__,": ",inactive_position)
            #"""
            #if inactive_x == 0 or inactive_x == board_width - 1 or inactive_y == 0 or inactive_y == board_height - 1:
            #    # Opponent is on the border, check for a push move
            #    for move in game.get_legal_moves():
            #        next_game, _, _ = game.forecast_move(move)
            #        next_inactive_position = next_game.__last_queen_move__[game.__inactive_players_queen__][:2]
            #        if next_inactive_position is None:  # Opponent forced off the grid
            #            print("bingo")
            #            return float("inf")  # Force this move
            #"""
#
            #active_central_control = -distance_to_center(active_position)
            #inactive_central_control = -distance_to_center(inactive_position)
#
            ## Weighted evaluation
            #mobility_weight = 1.0
            #center_control_weight = 0.5
#
            #active_score = (
            #    mobility_weight * active_moves +
            #    center_control_weight * active_central_control
            #)
            #inactive_score = (
            #    mobility_weight * inactive_moves +
            #    center_control_weight * inactive_central_control
            #)
#
            ## Return the difference in scores depending on the perspective
            #return active_score - inactive_score if maximizing_player_turn else inactive_score - active_score


class CustomPlayer:
    # TODO: finish this class!
    """Player that chooses a move using your evaluation function
    and a minimax algorithm with alpha-beta pruning.
    You must finish and test this player to make sure it properly
    uses minimax and alpha-beta to return a good move."""

    def __init__(self, search_depth, eval_fn=CustomEvalFn()):
        """Initializes your player.

        if you find yourself with a superior eval function, update the default
        value of `eval_fn` to `CustomEvalFn()`

        Args:
            search_depth (int): The depth to which your agent will search
            eval_fn (function): Utility function used by your agent
        """
        self.eval_fn = eval_fn
        self.search_depth = search_depth
        self.first_move = True

    def move(self, game, legal_moves, time_left):
        """Called to determine one move by your agent

            Note:
                1. Do NOT change the name of this 'move' function. We are going to call
                the this function directly.
                2. Change the name of minimax function to alphabeta function when
                required. Here we are talking about 'minimax' function call,
                NOT 'move' function name.
                Args:
                game (Board): The board and game state.
                legal_moves (list): List of legal moves
                time_left (function): Used to determine time left before timeout

            Returns:
                tuple: best_move
            """
        opponent_move=game.__last_queen_move__[game.__inactive_players_queen__]
        center_positions = [
            (game.height // 2 - 1, game.width // 2 - 1, False),
            (game.height // 2 - 1, game.width // 2 - 1, True),
            (game.height // 2 - 1, game.width // 2,False),
            (game.height // 2 - 1, game.width // 2,True),
            (game.height // 2, game.width // 2 - 1,False),
            (game.height // 2, game.width // 2 - 1,True),
            (game.height // 2, game.width // 2,False),
            (game.height // 2, game.width // 2,True),
        ]
        # start from center
        #if len(legal_moves) == (game.width*game.height)-2 or len(legal_moves) == (game.width*game.height) :
            #return a center move that is legal
        #print(self.first_move)
        #print(game.get_legal_moves())
        if self.first_move:
            for move in center_positions:
                if move is not opponent_move:
                    self.first_move = False
                    return move
        
        # win if we can:
        winning_move = (*opponent_move[:2],True)
        opponent_position=opponent_move[:2]
        our_position=game.__last_queen_move__[game.__active_players_queen__][:2]
        #push_direction = (our_position[0] - self.position[0], our_position[1] - self.position[1])  # Direction vector
        push_direction = (
                max(-1, min(1, opponent_position[0] - our_position[0])),
                max(-1, min(1, opponent_position[1] - our_position[1])),
            )  # Ensures movement is -1, 0, or 1
        pushed_position = (opponent_position[0] + push_direction[0], opponent_position[1] + push_direction[1])
        print("push: ",push_direction)
        print(pushed_position)
        if not (0 <= pushed_position[0] < game.height and 0 <= pushed_position[1] < game.width):
            if winning_move in game.get_legal_moves():
                return winning_move

        #if (CustomEvalFn.is_on_border(game,opponent_position)):
        #    return winning_move
        
        
        best_move, utility = self.minimax(game, time_left, depth=self.search_depth)
        logger.debug(f"Chosen Move: {best_move}, Utility: {utility}")
        return best_move

    def utility(self, game, maximizing_player):
        """Can be updated if desired. Not compulsory. """
        return self.eval_fn.score(game)

    def minimax(self, game, time_left, depth, maximizing_player=True):
        """Implementation of the minimax algorithm

        Args:
            game (Board): A board and game state.
            time_left (function): Used to determine time left before timeout
            depth: Used to track how deep you are in the search tree
            maximizing_player (bool): True if maximizing player is active.

        Returns:
            (tuple, int): best_move, val
        """
        # TODO: finish this function!
        best_move = (0, 0)
        best_val = float('-inf')

        if not game.get_legal_moves():
            return best_move, best_val

        for move in game.get_legal_moves():
            next_game, _, _ = game.forecast_move(move)
            value = self.min_value(next_game, depth - 1, best_move) if maximizing_player else self.max_value(next_game, depth - 1, best_move)
            if maximizing_player:
                if value > best_val:
                    best_val, best_move = value, move
            else:
                if value < best_val:
                    best_val, best_move = value, move
            logger.debug(f"Returning from Minimax: move={move}, value={value}")
        logger.debug(f"Returning from Minimax: Depth={depth}, Best Move={best_move}, Best Value={best_val}")
        return best_move, best_val

    # Maximizing player strategy
    def max_value(self, game, depth, last_best_move):
        # if self.time_left() < TimeLimit
        #   Raise last_best_move

        # Terminal situation: depth = 0 or illegal move
        if depth == 0 or not game.get_legal_moves():
            return self.utility(game, maximizing_player=True)

        # Normal situation: find the maximizing value
        best_score = float('-inf')
        for move in game.get_legal_moves():
            next_game, _, _ = game.forecast_move(move)
            best_score = max(best_score, self.min_value(next_game, depth - 1, last_best_move))
        return best_score

    # Minimizing player strategy
    def min_value(self, game, depth, last_best_move):
        # if self.time_left() < TimeLimit
        #   Raise last_best_move

        # Terminal situation: depth = 0 or illegal move
        if depth == 0 or not game.get_legal_moves():
            return self.utility(game, maximizing_player=False)

        # Normal situation: find the minimizing value
        best_score = float('inf')
        for move in game.get_legal_moves():
            next_game, _, _ = game.forecast_move(move)
            best_score = min(best_score, self.max_value(next_game, depth - 1, last_best_move))
        return best_score


    def alphabeta(self, game, time_left, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implementation of the alphabeta algorithm

        Args:
            game (Board): A board and game state.
            time_left (function): Used to determine time left before timeout
            depth: Used to track how deep you are in the search tree
            alpha (float): Alpha value for pruning
            beta (float): Beta value for pruning
            maximizing_player (bool): True if maximizing player is active.

        Returns:
            (tuple, int): best_move, val
        """
        # TODO: finish this function!
        # Terminal situation: depth = 0 or illegal move
        if depth == 0 or not game.get_legal_moves():
            return (0, 0), self.utility(game, maximizing_player)

        best_move = (0, 0)
        if maximizing_player:
            best_val = float('-inf')
            for move in game.get_legal_moves():
                next_game, _, _ = game.forecast_move(move)
                _, val = self.alphabeta(next_game, time_left, depth - 1, alpha, beta, False)
                if val > best_val:
                    best_val = val
                    best_move = move
                alpha = max(alpha, best_val)
                if beta <= alpha:
                    break
        else:
            best_val = float('inf')
            for move in game.get_legal_moves():
                next_game, _, _ = game.forecast_move(move)
                _, val = self.alphabeta(next_game, time_left, depth - 1, alpha, beta, True)
                if val < best_val:
                    best_val = val
                    best_move = move
                beta = min(beta, best_val)
                if beta <= alpha:
                    break

        return best_move, best_val
        raise NotImplementedError
