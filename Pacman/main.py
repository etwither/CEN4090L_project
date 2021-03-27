from Game import *
import cProfile
import re

if __name__ == "__main__":

    game = Game()
    game.start()
    #cProfile.run('Game()', "output.dat")

    import pstats
    from pstats import SortKey

"""     with open("output_time.txt", 'w') as f:
        p = pstats.Stats("output.dat", stream=f)
        p.sort_stats("time").print_stats()

    with open("output_calls.txt", 'w') as f:
        p = pstats.Stats("output.dat", stream=f)
        p.sort_stats("calls").print_stats() """