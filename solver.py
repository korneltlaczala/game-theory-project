class Game():

    def __init__(self):
        self.result = []
        self.is_periodic = False
        self.is_arithmeticly_periodic = False
        self.first_period_start = None
        self.first_period_end = None

    def detect_periodicity(self):
        n = len(self.result)
        for l in range(n//3):
            for p in range(1, (n - l)//3):  
                is_periodic = True
                for i in range(l, n - p):
                    if self.result[i] != self.result[i + p]:
                        is_periodic = False
                        break
                if is_periodic:
                    self.is_periodic = True
                    self.first_period_start = l
                    self.first_period_end = l + p-1
        

    def detect_arithmetic_periodicity(self):
        pass

    def __str__(self):
        if self.is_periodic:
            return f"Periodic game with period {self.first_period_start} - {self.first_period_end}"
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
        

    def __str__(self):
        if self.valid_moves == set():
            return f"Subtraction game with no valid moves"
        return f"Subtraction game with valid moves {sorted(self.valid_moves)}\n" + super().__str__()

if __name__ == '__main__':
    game = SubtractionGame()
    game.add_moves([1,2,6,11])
    game.calculate(40)
    game.detect_periodicity()
    print(game)
    game.show_result()