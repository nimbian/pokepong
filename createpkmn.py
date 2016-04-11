from pokepong.models import Owned, Move, Pokemon
from pokepong.database import db
from argparse import ArgumentParser
import pygame
SCREEN = pygame.display.set_mode((0,0))

if __name__ == "__main__":
    PARSER = ArgumentParser('Create a Pokemon')
    PARSER.add_argument('-p', '--pokemon', help='number of pokemon to add')
    PARSER.add_argument('-m1', '--move_one', help='Number of move for move 1')
    PARSER.add_argument('-m2', '--move_two', help='Number of move for move 2')
    PARSER.add_argument('-m3', '--move_three', help='Number of move for move 3')
    PARSER.add_argument('-m4', '--move_four', help='Number of move for move 4')
    PARSER.add_argument('-l', '--level', help='Level of pokemon', default = 5)
    PARSER.add_argument('-lp', '--list_pokemon', help='Will list all pokemon and corresponding numbers', action='store_true')
    PARSER.add_argument('-lm', '--list_moves', help='Will list all moves and corresponding numbers', action='store_true')
    ARGS = PARSER.parse_args()
    if ARGS.list_moves:
        tmp = Move.query.all()
        for i in tmp:
            print str(i.id) + ': ' +i.name

    elif ARGS.list_pokemon:
        tmp = Pokemon.query.all()
        for i in tmp:
            print str(i.id) + ': ' + i.name

    else:
        try:
            tmp = Owned(ARGS.pokemon, lvl=ARGS.level)
            tmp.move1 = Move.query.get(ARGS.move_one)
            if ARGS.move_two:
                tmp.move2 = Move.query.get(ARGS.move_two)
            if ARGS.move_three:
                tmp.move3 = Move.query.get(ARGS.move_three)
            if ARGS.move_four:
                tmp.move4 = Move.query.get(ARGS.move_four)
            db.add(tmp)
            db.commit()
            print tmp.id
        except:
            print 'Invalid or missing argument'

