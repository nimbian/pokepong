from argparse import ArgumentParser
from redis import StrictRedis
import json
r = StrictRedis(host='127.0.0.1')

if __name__ == '__main__':
    PARSER = ArgumentParser('Create a team in queue')
    PARSER.add_argument('-n', '--name', help='name of trainer')
    PARSER.add_argument('-p', '--pokemon', help='comma seperated list of pokemon ie 152,153,154')
    ARGS = PARSER.parse_args()
    d = {'name': ARGS.name, 'pokemon':ARGS.pokemon.split(',')}
    r.rpush('lineup', json.dumps(d))
