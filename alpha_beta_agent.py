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

        self.max_depth = max_depth
        self.player = None

    # ISAAC: probably shouldn't focus on this until we have a working 
    #        minimax algorithm. I adjusted the stupid large heuristic values 
    def heuristic(self, brd):

        # using board.getoutcome() to determine a winning or a losing board
        if brd.get_outcome() == self.player and brd.player != self.player:
            return 1000000

        if brd.get_outcome() != self.player and brd.player == self.player:
            return -1000000

        board_heuristics = 0
        for i in range(0, brd.h):
            for j in range(0, brd.w):
                if brd.board[i][j] != 0:
                    if brd.is_any_line_at(i, j):
                        if brd.board[i][j] != self.player:
                            board_heuristics -= 10
                        elif brd.board[i][j] == self.player:
                            board_heuristics += 1
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
            succ.append((nb, col))
        return succ