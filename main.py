from Generator import Generator
from Generator import Difficulty


def main():
    # gen_easy = Generator(Difficulty.EASY)
    # gen_easy.generate_grid()
    # del gen_easy
    #
    # gen_medium = Generator(Difficulty.MEDIUM)
    # gen_medium.generate_grid()
    # del gen_medium

    gen_hard = Generator(Difficulty.HARD)
    gen_hard.generate_grid()
    del gen_hard


if __name__ == "__main__":
    main()