class Game():

    def __init__(self):
        self.result = []
        self.is_periodic = False
        self.is_arithmeticly_periodic = False
        self.first_period_start = None
        self.period_length = None

    def __str__(self):
        if self.is_periodic:
            return f"Periodic game with period starting at {self.first_period_start} with length {self.period_length}"
        return f"Non-periodic game"

class SubtractionGame(Game):

    def __init__(self):
        super().__init__()
        self.valid_moves = set()

    def add_move(self, move):
        self.valid_moves.add(move)

    def add_moves(self, moves):
        for move in moves:
            self.valid_moves.add(move)

    def remove_move(self, move):
        self.valid_moves.remove(move)

    def remove_moves(self, moves):
        for move in moves:
            self.valid_moves.remove(move)

    def mex(self, S):
        n = len(S)
        for i in range(n + 1):
            if i not in S:
                return i

    def calculate(self, n):
        self.result = [0]
        for position in range(1, n + 1):
            reachable = set()
            for move in self.valid_moves:
                if position - move >= 0:
                    reachable.add(self.result[position - move])
            if len(reachable) == 0:
                self.result.append(0)
            else:
                self.result.append(self.mex(reachable))

    def show_result(self):
        print(self.result)

    def solve(self, starting_position):
        print(f"Starting with {starting_position} tokens: ", end="")
        if self.result[starting_position] == 0:
            print("Player 2 wins")
        else:
            print("Player 1 wins")

    def player1_winrate(self, max_starting_position):
        wins = 0
        for position in range(1, max_starting_position + 1):
            if self.does_player1_win(position):
                wins += 1
        winrate = wins / max_starting_position
        print(f"Player 1 expected winrate: {round(winrate * 100, 2)}%")
        return winrate
        
    def does_player1_win(self, starting_position):
        if self.result[starting_position] == 0:
            return False
        return True

    def detect_periodicity(self):
        n = len(self.result)
        max_move = max(self.valid_moves)
        max_period = n - max_move
        for period_candidate in range(1, max_period + 1):
            candidate_valid = True
            for i in range(n-max_move, n):
                if self.result[i] != self.result[i - period_candidate]:
                    candidate_valid = False
                    break
            if candidate_valid:
                self.is_periodic = True
                self.period_length = period_candidate
                break

    def __str__(self):
        if self.valid_moves == set():
            return f"Subtraction game with no valid moves"
        return f"Subtraction game with valid moves {sorted(self.valid_moves)}\n" + super().__str__()

if __name__ == '__main__':
    game = SubtractionGame()
    game.add_moves([1,2,6])
    # game.add_moves([1,2,6,11])
    # game.add_moves([2,3])
    game.calculate(int(50))
    game.detect_periodicity()
    print(game)
    game.show_result()