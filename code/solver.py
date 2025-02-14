import random

from numpy import mean


class Game():

    def __init__(self):
        self.result = []
        self.is_periodic = False
        self.is_arithmeticly_periodic = False
        self.first_period_start = None
        self.period_length = None
        self.saltus = None

    def __str__(self):
        if self.is_periodic:
            return f"Periodic game with period starting at {self.first_period_start} with length {self.period_length}"
        return f"Non-periodic game"

    def mex(self, S):
        n = len(S)
        for i in range(n + 1):
            if i not in S:
                return i

class AllButGame(Game):

    def __init__(self):
        super().__init__()
        self.invalid_moves = set()

    def add_move(self, move):
        self.invalid_moves.add(move)

    def add_moves(self, moves):
        for move in moves:
            self.invalid_moves.add(move)

    def remove_move(self, move):
        self.invalid_moves.remove(move)

    def remove_moves(self, moves):
        for move in moves:
            self.invalid_moves.remove(move)

    def calculate(self, depth):
        self.result = [0]
        for position in range(1, depth + 1):
            reachable = set()
            for move in range(1, depth + 1):
                if move not in self.invalid_moves and position - move >= 0:
                    reachable.add(self.result[position - move])
            if len(reachable) == 0:
                self.result.append(0)
            else:
                self.result.append(self.mex(reachable))

    def create_inverse_game(self):
        m = max(self.invalid_moves)
        inv_game = SubtractionGame()
        inv_game.add_moves(range(1, m+1))
        for move in self.invalid_moves:
            inv_game.remove_move(move)
        inv_game.calculate(m)
        return inv_game

    def detect_periodicity(self):
        n = len(self.result)
        if len(self.invalid_moves) == 0:
            self.is_periodic = True
            self.period_length = 1
            self.first_period_start = 0
            self.saltus = 1
            return
        max_move = max(self.invalid_moves)
        max_period = n - max_move
        for period_candidate in range(1, max_period + 1):
            break_flag=False
            #print(f"period_candidate: {period_candidate}")
            for saltus_candidate in range(1,period_candidate+1):
                candidate_valid=True
                for i in range(n-max_move, n):
                    if self.result[i] != self.result[i - period_candidate]+saltus_candidate:
                        candidate_valid = False
                        break
                if candidate_valid:
                    self.is_periodic = True
                    self.period_length = period_candidate
                    self.saltus=saltus_candidate
                    break_flag=True
                    break
            if break_flag:
                break
        if not self.is_periodic:
            print(f"Either there is no period, or the period is longer than {max_period}")
            return

        prev_matching = 0
        for i in range(self.period_length, n):
            if self.result[i] == self.result[i - self.period_length]+self.saltus:
                prev_matching += 1
            else:
                prev_matching = 0
            if prev_matching == self.period_length:
                self.first_period_start = i - 2 * self.period_length + 1
                break
    def show_result(self):
        print(self.result)
    
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

    def calculate(self, depth):
        self.result = [0]
        for position in range(1, depth + 1):
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
        if len(self.valid_moves) == 0:
            self.is_periodic = True
            self.period_length = 1
            self.first_period_start = 0
            self.saltus = None
            return
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

        if not self.is_periodic:
            print(f"Either there is no period, or the period is longer than {max_period}")
            return

        prev_matching = 0
        for i in range(self.period_length, n):
            if self.result[i] == self.result[i - self.period_length]:
                prev_matching += 1
            else:
                prev_matching = 0
            if prev_matching == self.period_length:
                self.first_period_start = i - 2*self.period_length + 1
                break

    def update(self, depth=int(1e3)):
        self.calculate(depth)
        self.detect_periodicity()
        print(self)

    def __str__(self):
        if self.valid_moves == set():
            return f"Subtraction game with no valid moves\n" + super().__str__()
        return f"Subtraction game with valid moves {sorted(self.valid_moves)}\n" + super().__str__()

if __name__ == '__main__':
    pass
    # game = SubtractionGame()
    # game.add_moves([1,4,10])
    # game.add_moves([1,2,6,11])
    # game.add_moves([1,8,11])
    # game.calculate(int(190))
    # game.detect_periodicity()
    # print(game)
    # game.update()

    # game = AllButGame()
    # game.add_moves([2,7])
    # game.calculate(100)
    # game.detect_periodicity()
    # print(game.period_length)
    # print(game.saltus)
    # print(game.first_period_start)
    # game.show_result()
    # mean_periods=[]
    # mean_saltuses=[]
    # periods=[]
    # saltuses=[]
    # fes=[]
    # for j in range(3,100):
    #     for i in range(50):
    #         a=random.randint(2,j)
    #         b=random.randint(2,j)
    #         while a==b:
    #             b = random.randint(1,10)
    #         game=AllButGame()
    #         game.add_moves([a,b])
    #         game.calculate(1000)
    #         game.detect_periodicity()
    #         periods.append(game.period_length)
    #         saltuses.append(game.saltus)
    #         fes.append([a,b])
    #     mean_periods.append(mean(periods))
    #     mean_saltuses.append(mean_saltuses)
