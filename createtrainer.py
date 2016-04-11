from pokepong.models import Trainer
from pokepong.database import db
from argparse import ArgumentParser

if __name__ == "__main__":
    PARSER = ArgumentParser('Create a Trainer')
    PARSER.add_argument('-n', '--name', help='Trainer name', required=True)
    PARSER.add_argument('-m', '--money', help='Amount of Money to get Trainer', required=True)
    ARGS = PARSER.parse_args()
    tmp = Trainer(ARGS.name)
    tmp.money = ARGS.money
    db.add(tmp)
    db.commit()
