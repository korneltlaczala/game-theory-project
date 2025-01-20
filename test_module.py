import pickle
import random

from solver import SubtractionGame

class Tester:
    def __init__(self):
        subtraction_game_test_library = dict()
        all_but_game_test_library = dict()

    def save(self, name):
        with open(name, 'wb') as file:
            pickle.dump(self, file)
    
    def test_subtraction_period(self, move_count, largest_possible_move, depth=None):
        # test_collection
        pass

class Test:
    
    def __init__(self, move_count, largest_possible_move, game_count=1000, depth=None):
        self.move_count = move_count
        self.largest_possible_move = largest_possible_move
        self.game_count = game_count
        if depth is None:
            self.depth =  largest_possible_move * 100
        else:
            self.depth = depth

    def run(self):
        self.periods = []
        for i in range(self.game_count):
            game = SubtractionGame()
            moves = random.sample(range(1, self.largest_possible_move + 1), self.move_count)
            game.add_moves(moves)

            game.calculate(depth=self.depth)
            game.detect_periodicity()
            self.periods.append(game.period_length)
    
    @property
    def mean_period(self):
        return sum(self.periods) / len(self.periods)

    def __str__(self):
        return f"Testing {self.game_count} games with {self.move_count} moves and largest possible move {self.largest_possible_move}. Mean period: {self.mean_period}"


def load(name):
    with open(name, 'rb') as file:
        return pickle.load(file)

if __name__ == "__main__":
    # tester = Tester()
    # tester = load("tester.pkl")
    # tester.save("tester.pkl")
    test = Test(move_count=5, largest_possible_move=10, game_count=10)
    test.run()
    print(test)
    
