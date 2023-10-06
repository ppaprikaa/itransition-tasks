from game import try_init_game
import sys

def main():
    args = sys.argv[1:]
    game = try_init_game(args)
    if game is not None:
        game.try_run()


if __name__ == "__main__":
    main()
