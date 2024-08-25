class TicTacToe:
    """ Tic-Tac Toe Board 
        
        Board is represented through a board object
        
        1 ¦ 2 ¦ 3
        --+---+--
        4 ¦ 5 ¦ 6
        --+---+--
        7 ¦ 8 ¦ 9
    """
    def __init__(self):
        self.spaces = 9
        self.blank = " "
        self.legal_players = ["X","O"]
        self.base =      " {} ¦ {} ¦ {} \n" + \
                          "---+---+--- \n" + \
                         " {} ¦ {} ¦ {} \n" + \
                          "---+---+--- \n" + \
                         " {} ¦ {} ¦ {} \n" 
        self.winning = [[0,1,2], # top horizontal
                        [3,4,5], # middle horizontal
                        [6,7,8], # bottom horizontal
                        [0,3,6], # left vertical
                        [1,4,7], # middle vertical
                        [2,5,8], # right vertical
                        [0,4,8], # diagonal \
                        [2,4,6]  # diagonal /
                       ]
        self.reset()
    
    def reset(self):
        """ Resets the board """
        self.board = [" "] * self.spaces

    def __str__(self):
        """ String representation of a game """
        return self.base.format(*self.board)
    
    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.board == other.board
        return False

    def __hash__(self):
        return hash("".join(self.board))
    
    def copy(self):
        """ Creates a copy of the game object """
        new_board = self.__class__()
        new_board.board = self.board[:]
        return new_board
        
    def get_moves(self):
        """ Returns open moves on the board """
        return [idx + 1 for idx, player in enumerate(self.board) if player == self.blank]
    
    def move(self, player, move):
        """ Updates the board based on player and move 
            
            example: 
                game.move("X", 4)                
        """
        player = player.upper()
        assert move in self.get_moves(), "Illegal move"
        assert player in self.legal_players, "Illegal player"
        self.board[move - 1] = player
        

    def gameover(self):
        """ Returns whether there are any legal moves left """
        return len(self.get_moves()) == 0 or self.winner() is not None
    
    def winner(self):
        """ Returns the winner of a game, 'Draw' or None if game is ongoing """
        for winner in self.winning:
            players = [self.board[pos] for pos in winner]
            s_players = set(players)
            if len(s_players) == 1 and self.blank not in s_players:
                return players[0]
        
        if self.blank not in set(self.board):
            return "Draw"

    def score_game(self, player):
        """ Scores a game based relative to player provided """
        winner = self.winner()
        player = player.upper()
        alt_players = [alt_player for alt_player in self.legal_players if alt_player != player]

        if winner == player:
            return 1
        elif winner in alt_players:
            return -1
        return 0
def play(game, bot):
    human = None
    while human is None:
        human = input("Select player: {} ".format(game.legal_players)).upper()
        if human not in game.legal_players:
            print("Invalid option")
            human = None
            
    comp = [alt_player for alt_player in game.legal_players if alt_player != human][0]
    turn = game.legal_players[0]
    while not game.gameover():    
        if comp == turn:
            move = bot.play(game, comp)
        else:
            print(game)
            move = None
            while move is None:
                move = input("Input move: ")
                if move.upper()[:1] == "Q":
                    print("Quitter...")
                    return
                elif move.upper()[:1] == "H":
                    print(game.__doc__)
                    continue
                if move.isdigit():
                    move = int(move)
        if move in game.get_moves():
            game.move(turn, move)
            turn = comp if turn == human else human
        else:
            print("Illegal move {}. Q to quit. H for help".format(move))
    print(game)
    if game.winner() == human:
        print("You won!")
    elif game.winner() == comp:
        print("You lost :-(")
    else:
        print("It's a draw")
 class MiniMaxBot:
    def __init__(self):
        """ Returns best move given game and player """
        self.memo = {}
        
    def play(self, game, player):
        return self._mini_max(game, player)[0]

    def _mini_max(self, game, player):
        """ Helper function for get_best_move. Returns best move and score given game and player """
        if player not in self.memo:
            self.memo[player] = {}
            
        player_memo = self.memo[player]
        
        if game not in player_memo:
            # Check to see if we've already seen this state
            if game.gameover():
                # Game over, no moves possible
                best_move = None
                best_score = game.score_game(player)
            else:
                alt_player = [alt_player for alt_player in game.legal_players if alt_player != player][0]
                moves = game.get_moves() # Get available moves
                best_score = float("-inf") # Default to worst possible score to ensure any move is selected

                for move in moves:
                    clone = game.copy() # Make a copy of the game to run recursively
                    clone.move(player, move) # Make the proposed move
                     # Figure out what the opponents best move would be (MINI)
                    _, score = self._mini_max(clone, player=alt_player)
                    score *= -1 # Since the game is zero-sum, what's bad for the opponent is good for us
                    if score > best_score: # Best our prior best score
                        best_move = move # Save the move
                        best_score = score # Update the best score
            self.memo[player][game] = (best_move, best_score) # Update the best move and score given the game
        return self.memo[player][game] # Return best move given player and game  
game = TicTacToe()
game.reset()
play(game, MiniMaxBot())
