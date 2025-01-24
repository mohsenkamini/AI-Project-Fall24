from random import randint
import random

from player_submission import CustomPlayer
from player_submission import CustomEvalFn

class RandomPlayer():

    def __init__(self, name="RandomPlayer"):
        self.name = name

    """Player that chooses a move randomly."""

    def move(self, game, legal_moves, time_left):
        if not legal_moves:
            return None
        else:
            return random.choice(legal_moves)

    def get_name(self):
        return self.name



class HumanPlayer():

    def __init__(self, name="HumanPlayer", eval_fn=CustomEvalFn()):
        self.name = name
        self.eval_fn = eval_fn

    """Player that chooses a move according to user's input."""
    def move(self, game, legal_moves, time_left):
        choice = {}

        if not len(legal_moves):
            print("No more moves left.")
            return None, None

        counter = 1
        for move in legal_moves:
            choice.update({counter: move})
            if not move[2]:
                print('\t'.join(['[%d] (%d,%d)'%(counter, move[0], move[1])]))
            else:
                print('\t'.join(['[%d] (%d,%d) - push' % (counter, move[0], move[1])]))
            counter += 1

        print("-------------------------")
        print(game.print_board(legal_moves))
        print("-------------------------")
        print(">< - impassable, o - valid move")
        print("-------------------------")

        valid_choice = False

        while not valid_choice:
            try:
                index = int(input('Select move index [1-cus'+str(len(legal_moves))+']:'))
                valid_choice = 1 <= index <= len(legal_moves)

                if not valid_choice:
                    print('Illegal move of queen! Try again.')
                print('=======================================')
                self.utility(game, maximizing_player=False)
                print('+++++++++++++++++++++++++++++++++++++++')
                self.utility(game, maximizing_player=True)
            except Exception:
                print('Invalid entry! Try again.')

        return choice[index]
    def utility(self, game, maximizing_player):
        """Can be updated if desired. Not compulsory. """
        return self.eval_fn.score(game)

    def get_name(self):
        return self.name
