import fire

import pandas as pd

from util import Game, Host, Guest, play_random_game


class Main(object):

    @staticmethod
    def play_single_game(strategy="random", opts=3):
        # Get show-time elements
        game = Game.random(number_of_options=opts)
        host = Host(manage_game=game)
        guest = Guest()
        print(game)

        # Ask guest to choose a door
        first_choice = guest.choose(options=host.show_options(), strategy=Guest.Strategy.RANDOM)
        print("(t=1) Guest's first choice: {}".format(first_choice))

        # Host reveals another door
        revealed_door = host.reveal(given_guest_choice=first_choice)
        print("(t=2) Host reveals door with a goat: {}".format(revealed_door))
        # Final guest choice
        final_choice = guest.choose(options=host.show_options(), strategy=strategy)
        print("(t=3) Guest's final choice: {}".format(final_choice))

        # Host ends game!
        result = host.end_game(final_choice=final_choice)
        print("(t=4) Game result {}".format(result))

    @staticmethod
    def play_multiple_games(strategy="random", times=100, opts=3, save=""):
        # TODO: implement multiple games
        results=list(map(lambda x:play_random_game(number_of_options=opts,strategy=strategy),range(times)))
        print(results)
        if save:
            results.to_csv(save)
        #raise NotImplementedError


if _name_ == "_main_":
    fire.Fire(Main)
