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
        self.me = None
        self.you = None

    def heuristic(self, brd):
        """Assign a heuristic value to the current state of the board"""

        value = 0
        
        if "defensive": 
            # This simply causes the ai to play defensively:
            #   if the AI can win, play that move
            #   else avoid outcomes where the other player wins
            if brd.get_outcome() == self.me and brd.player == self.you:
                return 1000000

            if brd.get_outcome() == self.you and brd.player == self.me:
                return -100000

            # Iterate through the board to find states that will lead to a favorable outcome. 
            # Weighted to be defensive
            for c in range(0, brd.w):
                for r in range(0, brd.h):
                    if brd.board[r][c] != 0:
                        if brd.is_any_line_at(c, r):
                            if brd.board[r][c] == self.you:
                                value -= 10 ** (brd.n - 1)
                            elif brd.board[r][c] == self.me:
                                value += 10 ** (brd.n - 2)
                            else:
                                value += 0
        
        if "aggresive":
            # vertical value
            for c in range(0, brd.w):
                for r in range(0, brd.h - brd.n + 1):
                    value += self.n2_line_at(brd, c, r, 0, 1)

            # horrizonal value
            for c in range(0, brd.w - brd.n + 1):
                for r in range(0, brd.h):
                    value += self.n2_line_at(brd, c, r, 1, 0)

            # diagonal1 value
            for c in range(0, brd.w - brd.n + 1):
                for r in range(0, brd.h - brd.n + 1):
                    value += self.n2_line_at(brd, c, r, 1, 1)

            # diagonal2 value
            for c in range(brd.n - 1, brd.w):
                for r in range(0, brd.h - brd.n + 1):
                    value += self.n2_line_at(brd, c, r, 1, -1)

        return value
    
    def n2_line_at(self, brd, x, y, dx, dy):
        n = 1
        sign = 0

        # Avoid out-of-bounds errors
        if ((x + (brd.n-1) * dx >= brd.w) or
            (y + (brd.n-1) * dy < 0) or (y + (brd.n-1) * dy >= brd.h)):
            return 0
        
        # Get token at (x,y)
        t = brd.board[y][x]
        if t == self.me:
            sign = 1
        else:
            sign = -1

        # Go through elements
        for i in range(1, brd.n):
            if brd.board[y + i*dy][x + i*dx] == t:
                n *= 10
            else:
                break

        return (n * sign)
    
    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    def go(self, brd):
        """Search for the best move (choice of column for the token)"""
        # Your code here
        self.me = brd.player
        self.you = (not (brd.player-1))+1
        alpha = -math.inf
        beta = math.inf
        ((b,c),v) = self.max(brd, self.max_depth, alpha, beta)
        return c
    
    def max(self, brd, n, alpha, beta):
        """Find the maximum of the children of the current board"""
        if n == 0:
            return ((brd, None), self.heuristic(brd))
        
        best_value = -math.inf
        best_brd = None
        best_col = None

        successors = self.get_successors(brd)
        for (board, column) in successors:
            ((b, c), value) = self.min(board, n-1, alpha, beta)
            if value > best_value:
                best_brd = board
                best_col = column
                best_value = value
            if best_value >= beta:
                return ((best_brd, best_col), best_value)
            alpha = max(alpha, best_value)
        return ((best_brd, best_col), best_value)

    def min(self, brd, n, alpha, beta):
        """Find the minimum of the children of the current board"""
        if n == 0:
            return ((brd, None), self.heuristic(brd))
        
        best_value = math.inf
        best_brd = None
        best_col = None

        successors = self.get_successors(brd)
        for (board, column) in successors:
            ((b, c), value) = self.max(board, n-1, alpha, beta)
            if value < best_value:
                best_brd = board
                best_col = column
                best_value = value
            if best_value <= alpha:
                return ((best_brd, best_col), best_value)
            beta = min(beta, best_value)
        return ((best_brd, best_col), best_value)

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