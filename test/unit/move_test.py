# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
Unit tests for pokepong.domove
'''

import unittest
import pygame

from test.unit import dbutil
from nose.tools import assert_equal
from os import remove

SCREEN = pygame.display.set_mode((0,0))

class Moves(unittest.TestCase):
    def setUp(self):
        from pokepong.database import init_db, db
        from pokepong.models import Trainer, Owned
        engine = create_engine('sqlite://test.db')
        init_db()
        self.me = Owned(1)
        self.opp = Owned(1)

    def tearDown(self):
        from pokepong.database import engine, db
        db.close()
        engine.dispose()
        remove('test.db')

    @with_setup(setUp, tearDown)
    def test_absorb(self):
        from sqlalchemy import func
        from pokepong.modes import Move
        from pokepong.domove import do_move
        move = Move.query.filter(func.lower(name) == func.lower(inspect.stack()[0][3][5:])).one()
        do_move(self.me, self.opp, move, 'wild', True, True)
        do_move(self.me, self.opp, move, 'wild', True, False)
        do_move(self.opp, self.me, move, 'wild', False, True)
        do_move(self.opp, self.me, move, 'wild', False, False)



    def test_acid(self):
        pass

    def test_acid_armor(self):
        pass

    def test_agility(self):
        pass

    def test_amnesia(self):
        pass

    def test_aurora_beam(self):
        pass

    def test_barrage(self):
        pass

    def test_barrier(self):
        pass

    def test_bide(self):
        pass

    def test_bind(self):
        pass

    def test_bite(self):
        pass

    def test_blizzard(self):
        pass

    def test_body_slam(self):
        pass

    def test_bone_club(self):
        pass

    def test_bonemerang(self):
        pass

    def test_bubble(self):
        pass

    def test_bubblebeam(self):
        pass

    def test_clamp(self):
        pass

    def test_comet_punch(self):
        pass

    def test_confuse_ray(self):
        pass

    def test_confusion(self):
        pass

    def test_constrict(self):
        pass

    def test_conversion(self):
        pass

    def test_counter(self):
        pass

    def test_crabhammer(self):
        pass

    def test_cut(self):
        pass

    def test_defense_curl(self):
        pass

    def test_dig(self):
        pass

    def test_dig_prep(self):
        pass

    def test_disable(self):
        pass

    def test_dizzy_punch(self):
        pass

    def test_double_kick(self):
        pass

    def test_double_team(self):
        pass

    def test_double_edge(self):
        pass

    def test_doubleslap(self):
        pass

    def test_dragon_rage(self):
        pass

    def test_dream_eater(self):
        pass

    def test_drill_peck(self):
        pass

    def test_earthquake(self):
        pass

    def test_egg_bomb(self):
        pass

    def test_ember(self):
        pass

    def test_explosion(self):
        pass

    def test_fire_blast(self):
        pass

    def test_fire_punch(self):
        pass

    def test_fire_spin(self):
        pass

    def test_fissure(self):
        pass

    def test_flamethrower(self):
        pass

    def test_flash(self):
        pass

    def test_fly(self):
        pass

    def test_fly_prep(self):
        pass

    def test_focus_energy(self):
        pass

    def test_fury_attack(self):
        pass

    def test_fury_swipes(self):
        pass

    def test_glare(self):
        pass

    def test_growl(self):
        pass

    def test_growth(self):
        pass

    def test_guillotine(self):
        pass

    def test_gust(self):
        pass

    def test_harden(self):
        pass

    def test_haze(self):
        pass

    def test_headbutt(self):
        pass

    def test_hi_jump_kick(self):
        pass

    def test_horn_attack(self):
        pass

    def test_horn_drill(self):
        pass

    def test_hydro_pump(self):
        pass

    def test_hyper_beam(self):
        pass

    def test_hyper_fang(self):
        pass

    def test_hypnosis(self):
        pass

    def test_ice_beam(self):
        pass

    def test_ice_punch(self):
        pass

    def test_jump_kick(self):
        pass

    def test_karate_chop(self):
        pass

    def test_kinesis(self):
        pass

    def test_leech_life(self):
        pass

    def test_leech_seed(self):
        pass

    def test_leer(self):
        pass

    def test_lick(self):
        pass

    def test_light_screen(self):
        pass

    def test_lovely_kiss(self):
        pass

    def test_low_kick(self):
        pass

    def test_meditate(self):
        pass

    def test_mega_drain(self):
        pass
    def test_mega_kick(self):
        pass

    def test_mega_punch(self):
        pass

    def test_metronome(self):
        pass

    def test_mimic(self):
        pass

    def test_minimize(self):
        pass

    def test_mirror_move(self):
        pass

    def test_mist(self):
        pass

    def test_night_shade(self):
        pass

    def test_pay_day(self):
        pass

    def test_peck(self):
        pass

    def test_petal_dance(self):
        pass

    def test_pin_missile(self):
        pass

    def test_poison_gas(self):
        pass

    def test_poison_sting(self):
        pass

    def test_poisonpowder(self):
        pass

    def test_pound(self):
        pass

    def test_psybeam(self):
        pass

    def test_psychic(self):
        pass

    def test_psywave(self):
        pass

    def test_quick_attack(self):
        pass

    def test_rage(self):
        pass

    def test_razor_leaf(self):
        pass

    def test_razor_wind_prep(self):
        pass

    def test_razor_wind(self):
        pass

    def test_recover(self):
        pass

    def test_reflect(self):
        pass

    def test_rest(self):
        pass

    def test_roar(self):
        pass

    def test_rock_slide(self):
        pass

    def test_rock_throw(self):
        pass

    def test_rolling_kick(self):
        pass

    def test_sand_attack(self):
        pass

    def test_scratch(self):
        pass

    def test_screech(self):
        pass

    def test_seismic_toss(self):
        pass

    def test_selfdestruct(self):
        pass

    def test_sharpen(self):
        pass

    def test_sing(self):
        pass

    def test_skull_bash(self):
        pass

    def test_skull_bash_prep(self):
        pass
    def test_sky_attack(self):
        pass
    def test_sky_attack_prep(self):
        pass
    def test_slam(self):
        pass

    def test_slash(self):
        pass

    def test_sleep_powder(self):
        pass

    def test_sludge(self):
        pass

    def test_smog(self):
        pass

    def test_smokescreen(self):
        pass

    def test_softboiled(self):
        pass

    def test_solarbeam_prep(self):
        pass
    def test_solarbeam(self):
        pass
    def test_sonicboom(self):
        pass

    def test_spike_cannon(self):
        pass

    def test_splash(self):
        pass

    def test_spore(self):
        pass

    def test_stomp(self):
        pass

    def test_strength(self):
        pass

    def test_string_shot(self):
        pass

    def test_struggle(self):
        pass

    def test_stun_spore(self):
        pass

    def test_submission(self):
        pass

    def test_substitute(self):
        pass

    def test_super_fang(self):
        pass

    def test_supersonic(self):
        pass

    def test_surf(self):
        pass

    def test_swift(self):
        pass

    def test_swords_dance(self):
        pass

    def test_tackle(self):
        pass

    def test_tail_whip(self):
        pass

    def test_take_testwn(self):
        pass

    def test_teleport(self):
        pass

    def test_thrash(self):
        pass

    def test_thunder(self):
        pass

    def test_thunder_wave(self):
        pass

    def test_thunderbolt(self):
        pass

    def test_thunderpunch(self):
        pass

    def test_thundershock(self):
        pass

    def test_toxic(self):
        pass

    def test_transform(self):
        pass

    def test_tri_attack(self):
        pass

    def test_twineedle(self):
        pass

    def test_vicegrip(self):
        pass

    def test_vine_whip(self):
        pass

    def test_water_gun(self):
        pass

    def test_waterfall(self):
        pass

    def test_whirlwind(self):
        pass

    def test_wing_attack(self):
        pass

    def test_withdraw(self):
        pass

    def test_wrap(self):
        pass
