from Controller.RegGameGenerator import RegGameGenerator
from Model.Difficulty import Difficulty


def main():
    generator = RegGameGenerator()
    generator.create_game(Difficulty.HARD)


if __name__ == "__main__":
    main()
