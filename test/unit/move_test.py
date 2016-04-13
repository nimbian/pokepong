# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
Unit tests for pokepong.domove
'''

import unittest
import pygame
import sqlalchemy

from nose.tools import assert_equal
from nose import with_setup
from os import remove

SCREEN = pygame.display.set_mode((0,0))

class Moves(unittest.TestCase):
    def setUp(self):
        from pokepong.database import init_db, db
        from pokepong.models import Trainer, Owned
        from sqlalchemy import create_engine
        engine = create_engine('sqlite:///test.db')
        init_db(tmp = engine)
        self.me = Owned(1)
        self.opp = Owned(1)

    def tearDown(self):
        from pokepong.database import engine, db
        db.close()
        engine.dispose()
        remove('test.db')

    def test_absorb(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)

    def test_acid(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_acid_armor(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(3)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_agility(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_amnesia(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_aurora_beam(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(6)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_barrage(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_barrier(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_bide(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move2 = Move.query.get(159)
        move.disabled = False
        move2.disabled = False
        move.pp = move.maxpp
        move2.pp = move.maxpp
        move.high_crit = False
        move2.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.opp, self.me, move2, 'wild', False, True)
        do_move(self.opp, self.me, move2, 'wild', False, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.me, self.opp, move2, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, False)
        do_move(self.opp, self.me, move, 'wild', False, False)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_bind(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_bite(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_blizzard(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_body_slam(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(13)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_bone_club(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(14)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_bonemerang(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_bubble(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_bubblebeam(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_clamp(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_comet_punch(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(19)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_confuse_ray(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(20)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_confusion(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_constrict(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_conversion(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_counter(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_crabhammer(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_cut(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_defense_curl(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(27)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_dig(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_disable(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_dizzy_punch(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(30)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_double_kick(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(31)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_double_team(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(32)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_double_edge(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(33)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_doubleslap(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_dragon_rage(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(35)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_dream_eater(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(36)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_drill_peck(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(37)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_earthquake(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_egg_bomb(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(39)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_ember(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_explosion(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_fire_blast(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(42)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_fire_punch(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(43)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_fire_spin(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(44)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_fissure(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_flamethrower(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_flash(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_fly(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_focus_energy(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(49)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_fury_attack(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(50)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_fury_swipes(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(51)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_glare(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_growl(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_growth(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_guillotine(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_gust(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_harden(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_haze(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_headbutt(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_hi_jump_kick(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(60)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_horn_attack(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(61)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_horn_drill(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(62)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_hydro_pump(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(63)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_hyper_beam(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(64)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_hyper_fang(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(65)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_hypnosis(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_ice_beam(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(67)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_ice_punch(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(68)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_jump_kick(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(69)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_karate_chop(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(70)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_kinesis(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_leech_life(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(72)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_leech_seed(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(73)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_leer(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_lick(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_light_screen(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(76)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_lovely_kiss(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(77)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_low_kick(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(78)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_meditate(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_mega_drain(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(80)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)

    def test_mega_kick(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(81)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_mega_punch(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(82)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_metronome(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_mimic(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_minimize(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_mirror_move(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(86)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_mist(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_night_shade(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(88)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_pay_day(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(89)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_peck(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_petal_dance(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(91)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_pin_missile(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(92)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_poison_gas(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(93)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_poison_sting(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(94)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_poisonpowder(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_pound(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_psybeam(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_psychic(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_psywave(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_quick_attack(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(100)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_rage(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_razor_leaf(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(101)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_razor_wind_prep(self):
        #TODO controllable last move
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(102)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_razor_wind(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(103)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_recover(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_reflect(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_rest(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_roar(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_rock_slide(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(108)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_rock_throw(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(109)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_rolling_kick(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(110)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_sand_attack(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(111)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_scratch(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_screech(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_seismic_toss(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(114)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_selfdestruct(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_sharpen(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_sing(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_skull_bash(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(117)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_skull_bash_prep(self):
        #TODO controllable lastmove
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(117)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)

    def test_sky_attack(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(118)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)

    def test_sky_attack_prep(self):
        #TODO controllable lastmove
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(118)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)

    def test_slam(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_slash(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_sleep_powder(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(121)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_sludge(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_smog(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_smokescreen(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_softboiled(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_solarbeam_prep(self):
        #TODO CONTROLLABLE LAST MOVE
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(126)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)

    def test_solarbeam(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)

    def test_sonicboom(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_spike_cannon(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(128)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_splash(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_spore(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_stomp(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_strength(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_string_shot(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(133)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_struggle(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_stun_spore(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(135)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_submission(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_substitute(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_super_fang(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(138)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_supersonic(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_surf(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_swift(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_swords_dance(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(142)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_tackle(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_tail_whip(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(144)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_take_down(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(145)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_teleport(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_thrash(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_thunder(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_thunder_wave(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(149)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_thunderbolt(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_thunderpunch(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_thundershock(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_toxic(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_transform(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_tri_attack(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(155)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_twineedle(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_vicegrip(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_vine_whip(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(158)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_water_gun(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(159)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_waterfall(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_whirlwind(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_wing_attack(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.get(162)
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_withdraw(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)


    def test_wrap(self):
        from sqlalchemy import func
        from pokepong.models import Move
        from pokepong.domove import do_move
        import inspect
        move = Move.query.filter(func.lower(Move.name) == func.lower(inspect.stack()[0][3][5:])).one()
        move.disabled = False
        move.pp = move.maxpp
        move.high_crit = False
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)

