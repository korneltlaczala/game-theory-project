import pickle
import random
import matplotlib.pyplot as plt

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
        collection.run_tests(upper_boundry=150)
        self.subtraction_game_test_library_by_move_count[move_count] = collection

    def test_periodicity_of_subtraction_game_by_largest_possible_move(self, largest_possible_move):
        collection = TestCollection(largest_possible_move=largest_possible_move)
        collection.run_tests()
        self.subtraction_game_test_library_by_largest_possible_move[largest_possible_move] = collection

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

    def plot_library(self, game_type, test_type):
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
            collection.plot()


class TestCollection():

    def __init__(self, move_count=None, largest_possible_move=None):
        self.move_count = move_count
        self.largest_possible_move = largest_possible_move
        self.tests = []
    
    def run_tests(self, upper_boundry=None, max_move_count=None):
        if self.move_count is not None:
            for lpm in range(10, upper_boundry+1, 10):
                print(lpm)
                test = Test(move_count=self.move_count, largest_possible_move=lpm)
                test.run()
                self.tests.append(test)
        if self.largest_possible_move is not None:
            if max_move_count is None:
                max_move_count = self.largest_possible_move
            for move_count in range(1, max_move_count + 1, max(max_move_count//10, 1)):
                print(move_count)
                test = Test(move_count=move_count, largest_possible_move=self.largest_possible_move)
                test.run()
                self.tests.append(test)

    def plot(self):
        if self.move_count is not None:
            self.plot_move_count()
        if self.largest_possible_move is not None:
            self.plot_lpm()

    def plot_move_count(self):
        x = [test.largest_possible_move for test in self.tests]
        y = [test.mean_period for test in self.tests]
        game_count = self.tests[0].game_count
        plt.plot(x, y, label=f"Mean period over {game_count} games")
        plt.xlabel("Largest possible move")
        plt.ylabel("Mean period")
        plt.title(f"Mean period of {self.move_count} moves")
        plt.legend()
        plt.show()


    def plot_lpm(self):
        x = [test.move_count for test in self.tests]        
        y = [test.mean_period for test in self.tests]
        game_count = self.tests[0].game_count
        plt.plot(x, y, label=f"Mean period of over {game_count} games")
        plt.xlabel("Number of moves")
        plt.ylabel("Mean period")
        plt.title(f"Mean period of {self.largest_possible_move} as largest possible move")
        plt.legend()
        plt.show()

    def __str__(self):
        if self.move_count is not None:
            output =  f"TestCollection with {len(self.tests)} tests for {self.move_count} moves\n"
            for test in self.tests:
                output += test.__str__() + "\n"
            return output
        if self.largest_possible_move is not None:
            output =  f"TestCollection with {len(self.tests)} tests for {self.largest_possible_move} as largest possible move\n"
            for test in self.tests:
                output += test.__str__() + "\n"
            return output


class Test():
    
    def __init__(self, move_count, largest_possible_move, game_count=200, depth=None):
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
    # tester.test_periodicity_of_subtraction_game_by_move_count(move_count=3)
    # tester.test_periodicity_of_subtraction_game_by_move_count(move_count=5)
    # tester.test_periodicity_of_subtraction_game_by_largest_possible_move(largest_possible_move=40)
    # tester.test_periodicity_of_subtraction_game_by_largest_possible_move(largest_possible_move=30)
    # tester.test_periodicity_of_subtraction_game_by_largest_possible_move(largest_possible_move=10)
    # tester.save("tester.pkl")
    # tester.display_library("subtraction", "move_count")
    # tester.display_library("subtraction", "lpm")
    tester.plot_library("subtraction", "move_count")
    tester.plot_library("subtraction", "lpm")
    # print(tester.subtraction_game_test_library_by_largest_possible_move[40].tests[0].periods)
