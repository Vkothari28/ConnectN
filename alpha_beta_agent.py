import math
import agent

###########################
# Alpha-Beta Search Agent #
###########################

class AlphaBetaAgent(agent.Agent):
    """Agent that uses alpha-beta search"""

    # Class constructor.
    #
    # PARAM [string] name:      the name of this player
    # PARAM [int]    max_depth: the maximum search depth
    def __init__(self, name, max_depth):
        super().__init__(name)
        # Max search depth
        self.max_depth = max_depth

    def path_heuristics(self,brd,player):

        if player==1:
            user=1
            opponent=2

        else:
             user=2
             opponent=1

            #using board.getoutcome() to determine a winning or a losing board
    if brd.get_outcome() == user and brd.player==opponent:
        return 100000000000000000000000000000000000000000000000

    if brd.get_outcome()==opponent and brd.player== user:
          return -9999999999999999999999999999999999999999999999999

    board_heuristics =0
    for i in range (0,board.h):
         for j in range(0,board.w):
             if brd.board[i][j]!=0:
                 if brd.is_any_line_at(i, j):
                     if brd.board[i][j] == opponent:
                         board_heuristics -= 10
                     elif brd.board[i][j]== user:
                         board_heuristics +=1
                     else:
                         board_heuristics += 0
                        return board_heuristics



    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    def go(self, brd):
        """Search for the best move (choice of column for the token)"""
        # Your code here
        # this is a test

    # Get the successors of the given board.
    #
    # PARAM [board.Board] brd: the board state
    # RETURN [list of (board.Board, int)]: a list of the successor boards,
    #                                      along with the column where the last
    #                                      token was added in it
    def get_successors(self, brd):
        """Returns the reachable boards from the given board brd. The return value is a tuple (new board state, column number where last token was added)."""
        # Get possible actions
        freecols = brd.free_cols()
        # Are there legal actions left?
        if not freecols:
            return []
        # Make a list of the new boards along with the corresponding actions
        succ = []
        for col in freecols:
            # Clone the original board
            nb = brd.copy()
            # Add a token to the new board
            # (This internally changes nb.player, check the method definition!)
            nb.add_token(col)
            # Add board to list of successors
            succ.append((nb,col))
        return succ
