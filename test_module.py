import pickle
import random

from solver import SubtractionGame

class Tester():
    def __init__(self):
        self.subtraction_game_test_library_by_move_count = dict()
        self.subtraction_game_test_library_by_largest_possible_move = dict()
        self.all_but_game_test_library_by_move_count = dict()
        self.all_but_game_test_library_by_largest_possible_move = dict()

    def save(self, name):
        with open(name, 'wb') as file:
            pickle.dump(self, file)
    
    def test_periodicity_of_subtraction_game_by_move_count(self, move_count):
        collection = TestCollection(move_count=move_count)
        collection.run_tests(upper_boundry=100)
        self.subtraction_game_test_library_by_move_count[move_count] = collection

    def test_periodicity_of_subtraction_game_by_largest_possible_move(self, largest_possible_move):
        collection = TestCollection(largest_possible_move=largest_possible_move)
        # collection.run_tests

    def display_library(self, game_type, test_type):
        if game_type == "subtraction":
            if test_type == "move_count":
                library = self.subtraction_game_test_library_by_move_count
            elif test_type == "lpm":
                library = self.subtraction_game_test_library_by_largest_possible_move
        elif game_type == "allbut":
            if test_type == "move_count":
                library = self.all_but_game_test_library_by_move_count
            elif test_type == "lpm":
                library = self.all_but_game_test_library_by_largest_possible_move
        for key, collection in library.items():
            print(collection)


class TestCollection():

    def __init__(self, move_count=None, largest_possible_move=None):
        self.move_count = move_count
        self.largest_possible_move = largest_possible_move
        self.tests = []
    
    def run_tests(self, upper_boundry):
        for i in range(10, upper_boundry+1, 10):
            print(i)
            test = Test(move_count=self.move_count, largest_possible_move=i)
            test.run()
            self.tests.append(test)

    def __str__(self):
        output =  f"TestCollection with {len(self.tests)} tests for {self.move_count} moves\n"
        for test in self.tests:
            output += test.__str__() + "\n"
        return output


class Test():
    
    def __init__(self, move_count, largest_possible_move, game_count=100, depth=None):
        self.move_count = move_count
        self.largest_possible_move = largest_possible_move
        self.game_count = game_count
        if depth is None:
            self.depth =  largest_possible_move * largest_possible_move * 10
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
            self.mean_period = sum(self.periods) / len(self.periods)

    def __str__(self):
        return f"Testing {self.game_count} games with {self.move_count} moves and largest possible move {self.largest_possible_move}. Mean period: {self.mean_period}"


def load(name):
    with open(name, 'rb') as file:
        return pickle.load(file)

if __name__ == "__main__":
    tester = load("tester.pkl")
    # tester.test_periodicity_of_subtraction_game_by_move_count(move_count=5)
    tester.save("tester.pkl")
    tester.display_library("subtraction", "move_count")
