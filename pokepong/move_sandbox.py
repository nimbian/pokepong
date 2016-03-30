from pygame import image, draw, display
import pygame
from util import loadalphaimg, loadimg, alphabet
from math import floor
from time import sleep
sleep(1)

SIZE = (1280,1024)
WHITE = (255, 237, 255)
GREEN = (63,156,79)
YELLOW = (255,228,104)
RED = (209,71,40)
GREY = (108,108,108)
BLACK = (18,11,11)

SCREEN = display.set_mode(SIZE)
frontimg = loadimg('fronts/{0}.PNG'.format(34)).convert()
backimg = loadimg('backs/{0}.PNG'.format(34)).convert()
frontimg.set_colorkey((255,255,255))
backimg.set_colorkey((255,255,255))

BTM = loadalphaimg('btmclean.png')
MYHP = loadalphaimg('myhp.png')
OPPHP = loadalphaimg('opphp.png')
HPBAR = loadalphaimg('hpbar.png')
MYBAR = loadalphaimg('mybar.png')
OPPBAR = loadalphaimg('oppbar.png')
SSIZE = [392,392]
BTM_TUPLE = (10, SIZE[1]-340)
ALPHA = loadalphaimg('alphafull.png')
ALPHA_DICT = alphabet()

MYHPBAR_RECT = [SIZE[0] - 700, SIZE[1]-505, MYHP.get_width(), MYHP.get_height()]
MYHP_RECT = [SIZE[0]-532, SIZE[1]-486, 399, 14]
MYPKMN = [59,SIZE[1]-736]

OPPHPBAR_RECT = [80, 120, 602, 91]
OPPHP_RECT = [227,141,399,15]
OPPPKMN = [SIZE[0]-500,0]

CHANGE = {(63, 156, 79): (156, 209, 122),
         (79, 112, 182): (138, 156, 218),
         (104, 147, 201): (165, 201, 237),
         (112, 112, 138): (209, 165, 173),
         (122, 104, 147): (246, 173, 130),
         (138, 156, 218): (79, 112, 182),
         (156, 209, 122): (63, 156, 79),
         (165, 104, 63): (228, 156, 112),
         (165, 112, 182): (218, 173, 192),
         (165, 201, 237): (104, 147, 201),
         (209, 71, 40): (255, 156, 71),
         (209, 156, 0): (255, 228, 104),
         (209, 165, 173): (112, 112, 138),
         (218, 173, 192): (165, 112, 182),
         (228, 112, 165): (246, 173, 192),
         (228, 156, 112): (165, 104, 63),
         (246, 173, 130): (122, 104, 147),
         (246, 173, 192): (228, 112, 165),
         (255, 156, 71): (209, 71, 40),
         (255, 228, 104): (209, 156, 0),
         WHITE:BLACK,
         BLACK:WHITE,
         (0,0,0):WHITE,
         (24,16,16):WHITE}

def word_builder(word,start_x, start_y):
    x = start_x
    draw.rect(SCREEN, WHITE, [x, start_y, len(word)*56,60])
    for l in word:
        SCREEN.blit(ALPHA,(start_x, start_y),ALPHA_DICT[l])
        start_x+=56
    return [x, start_y, len(word)*56,60]

def draw_my_hp_bar():
    draw.rect(SCREEN, WHITE, MYHPBAR_RECT)
    SCREEN.blit(MYHP, MYHPBAR_RECT[:2])
    return [MYHPBAR_RECT]

def draw_my_lvl(pkmn):
    return [word_builder('%' + str(pkmn.lvl) + ' ', SIZE[0] - 405, SIZE[1]-565)]

def draw_my_hp(pkmn):
    maxhp = pkmn.maxhp
    hp = pkmn.hp
    bar_len = floor(hp/float(maxhp)*399)
    if bar_len < 100:
        color = RED
    elif bar_len < 200:
        color = YELLOW
    else:
        color = GREEN
    if 10 <= maxhp < 100:
        maxhp = ' ' + str(maxhp)
    elif maxhp < 10:
        maxhp = '  ' + str(maxhp)
    else:
        maxhp = str(maxhp)
    if 10 <= hp < 100:
        hp = ' ' + str(hp)
    elif hp < 10:
        hp = '  ' + str(hp)
    else:
        hp = str(hp)
    draw.rect(SCREEN, WHITE, MYHP_RECT)
    if hp > 0:
        draw.rect(SCREEN, color, [MYHP_RECT[0], MYHP_RECT[1], bar_len, MYHP_RECT[3]])
    retval = []
    retval.append(MYHP_RECT)
    retval.append(word_builder('{0}/{1}'.format(hp,maxhp), SIZE[0] - 570, SIZE[1]-445))
    return retval

def draw_my_pkmn_sprite(pkmn):
    draw.rect(SCREEN, WHITE, MYPKMN + SSIZE)
    SCREEN.blit(pkmn.backimg, MYPKMN)
    return [MYPKMN + SSIZE]

def draw_my_pkmn_name(pkmn):
    tmp = draw.rect(SCREEN, WHITE, [SIZE[0] - 630, SIZE[1]-625,600,60])
    return [word_builder(pkmn.name.upper(), SIZE[0] - 630, SIZE[1]-625), tmp]

def draw_opp_hp_bar():
    draw.rect(SCREEN,WHITE, OPPHPBAR_RECT)
    SCREEN.blit(OPPHP,OPPHPBAR_RECT[:2])
    return [OPPHPBAR_RECT]

def draw_opp_lvl(pkmn):
    return [word_builder('%' + str(pkmn.lvl) + ' ', 230,60)]

def draw_opp_hp(pkmn):
    maxhp = pkmn.maxhp
    hp = pkmn.hp
    bar_len = floor(hp/float(maxhp)*399)
    if bar_len < 100:
        color = RED
    elif bar_len < 200:
        color = YELLOW
    else:
        color = GREEN
    draw.rect(SCREEN, WHITE, OPPHP_RECT)
    if hp > 0:
        draw.rect(SCREEN, color, [OPPHP_RECT[0], OPPHP_RECT[1], bar_len, OPPHP_RECT[3]])
    return [OPPHP_RECT]

def draw_opp_pkmn_sprite(pkmn):
    draw.rect(SCREEN, WHITE, OPPPKMN + SSIZE)
    SCREEN.blit(pkmn.frontimg, OPPPKMN)
    return [OPPPKMN + SSIZE]

def draw_opp_pkmn_name(pkmn):
    tmp = draw.rect(SCREEN, WHITE, [60,1,600,60])
    return [word_builder(pkmn.name.upper(), 60, 1), tmp]

def draw_all_me(pkmn):
    x = []
    x.extend(draw_my_pkmn_sprite(pkmn))
    x.extend(draw_my_pkmn_name(pkmn))
    x.extend(draw_my_hp_bar())
    x.extend(draw_my_hp(pkmn))
    x.extend(draw_my_lvl(pkmn))
    display.update(x)

def draw_all_opp(pkmn):
    x = []
    x.extend(draw_opp_pkmn_sprite(pkmn))
    x.extend(draw_opp_pkmn_name(pkmn))
    x.extend(draw_opp_hp_bar())
    x.extend(draw_opp_hp(pkmn))
    x.extend(draw_opp_lvl(pkmn))
    display.update(x)

class pokemon(object):
    name = 'NIDOKING'
    hp = 200
    maxhp = 200
    frontimg = frontimg
    backimg = backimg
    lvl = 20

class trainer(object):
    def __init__(self,current):
        self.current = current

def invert():
    pixels = pygame.surfarray.pixels3d(SCREEN)
    pixels[:,:,:3] = CHANGE[(pixels[:,:,0],pixels[:,:,1],pixels[:,:,2])]

def low_big():
    norm = loadalphaimg('moves/Bignorm.png')
    return SCREEN.blit(norm,  (760, 228))

def mid_big():
    norm = loadalphaimg('moves/Bignorm.png')
    return SCREEN.blit(norm,  (896, 133))

def high_big():
    norm = loadalphaimg('moves/Bignorm.png')
    return SCREEN.blit(norm,  (930, 0))

def big_3(me,opp):
    tmp = low_big()
    display.update(tmp)
    draw.rect(SCREEN,WHITE,tmp)
    draw_opp_pkmn_sprite(opp.current)
    draw_my_pkmn_name(me.current)
    sleep(.15)
    tmp2 = mid_big()
    display.update([tmp, tmp2])
    sleep(.15)
    draw_opp_pkmn_sprite(opp.current)
    tmp = high_big()
    display.update([tmp, tmp2])
    sleep(.15)
    draw_opp_pkmn_sprite(opp.current)
    display.update(tmp)

def right_med():
    norm = loadalphaimg('moves/Mednorm.png')
    return SCREEN.blit(norm,  (990, 133))

def left_med():
    norm = loadalphaimg('moves/Mednorm.png')
    return SCREEN.blit(norm,  (770, 169))

def mid_med():
    norm = loadalphaimg('moves/Mednorm.png')
    return SCREEN.blit(norm,  (876, 228))

def med_3(me,opp):
    tmp = right_med()
    display.update(tmp)
    draw_opp_pkmn_sprite(opp.current)
    sleep(.15)
    tmp2 = left_med()
    display.update([tmp, tmp2])
    sleep(.15)
    draw_opp_pkmn_sprite(opp.current)
    tmp = mid_med()
    display.update([tmp, tmp2])
    sleep(.15)
    draw_opp_pkmn_sprite(opp.current)
    display.update(tmp)

def left_double():
    norm = loadalphaimg('moves/Mednorm.png')
    return SCREEN.blit(norm,  (820, 133))

def right_double():
    norm = loadalphaimg('moves/Mednorm.png')
    return SCREEN.blit(norm,  (930, 222))

def double(me,opp):
    tmp = left_double()
    display.update(tmp)
    draw_opp_pkmn_sprite(opp.current)
    sleep(.15)
    tmp2 = right_double()
    display.update([tmp, tmp2])
    sleep(.15)
    draw_opp_pkmn_sprite(opp.current)
    display.update(tmp2)



def sandbox():
    SCREEN.fill(WHITE)
    SCREEN.blit(BTM, BTM_TUPLE)
    display.flip()
    me = trainer(pokemon())
    opp = trainer(pokemon())
    draw_all_opp(opp.current)
    draw_all_me(me.current)

def wave(count):
    orig = SCREEN.copy()
    tmp1 = SCREEN.copy()
    tmp2 = SCREEN.copy()
    tmp1.fill(WHITE)
    tmp2.fill(WHITE)
    for i in range(SIZE[1]/14+1):
        t = i%8
        if t > 4:
           t = 8-t
        t = t-2
        tmp1.blit(SCREEN, (t*7,i*14),(0,i*14,SIZE[0],(i+1)*14))
        tmp2.blit(SCREEN, (t*-7,i*14),(0,i*14,SIZE[0],(i+1)*14))
    for c in range(count):
        SCREEN.blit(tmp1,(0,0))
        display.flip()
        sleep(.1)
        SCREEN.blit(tmp2,(0,0))
        display.flip()
        sleep(.1)
    SCREEN.blit(orig,(0,0))
    display.flip()

def convert(array):
    return CHANGE[tuple(array)]

def invert():
    pixels = pygame.surfarray.pixels3d(SCREEN)




def dmged():
    tmp = SCREEN.copy()
    clear()
    SCREEN.blit(tmp,(7,0))
    pygame.display.flip()
    sleep(.2)
    clear()
    SCREEN.blit(tmp,(0,0))
    pygame.display.flip()
    sleep(.2)
    clear()
    SCREEN.blit(tmp,(7,0))
    pygame.display.flip()
    sleep(.2)
    clear()
    SCREEN.blit(tmp,(0,0))
    pygame.display.flip()
    sleep(2)

def beam(me,opp,type_ = None):
    beams = []
    for i in range(1,7):
        beams.append(loadalphaimg('moves/beam{0}.png'.format(i)))
    x = SCREEN.blit(beams[0],(339,232))
    for i in beams:
        pygame.draw.rect(SCREEN, WHITE, x)
        draw_all_me(me.current)
        draw_all_opp(opp.current)
        display.update(SCREEN.blit(i,(339,232)))
        sleep(.1)

    pygame.draw.rect(SCREEN, WHITE, x)
    draw_all_me(me.current)
    draw_all_opp(opp.current)
    sleep(.1)
    dmged()


def do_absorb(me,opp):
    pass

def do_acid(me,opp):
    pass

def do_acid_armor(me,opp):
    pass

def do_agility(me,opp):
    pass

def do_amnesia(me,opp):
    pass

def do_aurora_beam(me,opp):
    beam(me,opp,type_ = 'aurora')

def do_barrage(me,opp):
    pass

def do_barrier(me,opp):
    pass

def do_bide(me,opp):
    pass

def do_bind(me,opp):
    pass

def do_bite(me,opp):
    pass

def do_blizzard(me,opp):
    pass

def do_body_slam(me,opp):
    pass

def do_bone_club(me,opp):
    pass

def do_bonemerang(me,opp):
    pass

def do_bubble(me,opp):
    pass

def do_bubblebeam(me,opp):
    pass

def do_clamp(me,opp):
    pass

def do_comet_punch(me,opp):
    pass

def do_confuse_ray(me,opp):
    pass

def do_confusion(me,opp):
    pass

def do_constrict(me,opp):
    pass

def do_conversion(me,opp):
    pass

def do_counter(me,opp):
    pass

def do_crabhammer(me,opp):
    pass

def do_cut(me,opp):
    pass

def do_defense_curl(me,opp):
    pass

def do_dig(me,opp):
    pass

def do_disable(me,opp):
    pass

def do_dizzy_punch(me,opp):
    pass

def do_double_kick(me,opp):
    pass

def do_double_team(me,opp):
    pass

def do_double_edge(me,opp):
    pass

def do_doubleslap(me,opp):
    pass

def do_dragon_rage(me,opp):
    pass

def do_dream_eater(me,opp):
    pass

def do_drill_peck(me,opp):
    pass

def do_earthquake(me,opp):
    pass

def do_egg_bomb(me,opp):
    pass

def do_ember(me,opp):
    pass

def do_explosion(me,opp):
    pass

def do_fire_blast(me,opp):
    pass

def do_fire_punch(me,opp):
    pass

def do_fire_spin(me,opp):
    pass

def do_fissure(me,opp):
    pass

def do_flamethrower(me,opp):
    pass

def do_flash(me,opp):
    pass

def do_fly(me,opp):
    pass

def do_focus_energy(me,opp):
    pass

def do_fury_attack(me,opp):
    pass

def do_fury_swipes(me,opp):
    pass

def do_glare(me,opp):
    pass

def do_growl(me,opp):
    pass

def do_growth(me,opp):
    pass

def do_guillotine(me,opp):
    pass

def do_gust(me,opp):
    pass

def do_harden(me,opp):
    pass

def do_haze(me,opp):
    pass

def do_headbutt(me,opp):
    pass

def do_hi_jump_kick(me,opp):
    pass

def do_horn_attack(me,opp):
    pass

def do_horn_drill(me,opp):
    pass

def do_hydro_pump(me,opp):
    pass

def do_hyper_beam(me,opp):
    pass

def do_hyper_fang(me,opp):
    pass

def do_hypnosis(me,opp):
    pass

def do_ice_beam(me,opp):
    beam(me,opp,type_='ice')

def do_ice_punch(me,opp):
    pass

def do_jump_kick(me,opp):
    pass

def do_karate_chop(me,opp):
    pass

def do_kinesis(me,opp):
    pass

def do_leech_life(me,opp):
    pass

def do_leech_seed(me,opp):
    pass

def do_leer(me,opp):
    pass

def do_lick(me,opp):
    pass

def do_light_screen(me,opp):
    pass

def do_lovely_kiss(me,opp):
    pass

def do_low_kick(me,opp):
    pass

def do_meditate(me,opp):
    pass

def do_mega_drain(me,opp):
    pass

def do_mega_kick(me,opp):
    pass

def do_mega_punch(me,opp):
    pass

def do_metronome(me,opp):
    pass

def do_mimic(me,opp):
    pass

def do_minimize(me,opp):
    pass

def do_mirror_move(me,opp):
    pass

def do_mist(me,opp):
    pass

def do_night_shade(me,opp):
    pass

def do_pay_day(me,opp):
    pass

def do_peck(me,opp):
    pass

def do_petal_dance(me,opp):
    pass

def do_pin_missile(me,opp):
    pass

def do_poison_gas(me,opp):
    pass

def do_poison_sting(me,opp):
    pass

def do_poisonpowder(me,opp):
    pass

def do_pound(me,opp):
    pass

def do_psybeam(me,opp):
    pass

def do_psychic(me,opp):
    pass

def do_psywave(me,opp):
    pass

def do_quick_attack(me,opp):
    pass

def do_rage(me,opp):
    pass

def do_razor_leaf(me,opp):
    pass

def do_razor_wind(me,opp):
    pass

def do_recover(me,opp):
    pass

def do_reflect(me,opp):
    pass

def do_rest(me,opp):
    pass

def do_roar(me,opp):
    pass

def do_rock_slide(me,opp):
    pass

def do_rock_throw(me,opp):
    pass

def do_rolling_kick(me,opp):
    pass

def do_sand_attack(me,opp):
    pass

def do_scratch(me,opp):
    pass

def do_screech(me,opp):
    pass

def do_seismic_toss(me,opp):
    pass

def do_selfdestruct(me,opp):
    pass

def do_sharpen(me,opp):
    pass

def do_sing(me,opp):
    pass

def do_skull_bash(me,opp):
    pass

def do_sky_attack(me,opp):
    pass

def do_slam(me,opp):
    pass

def do_slash(me,opp):
    pass

def do_sleep_powder(me,opp):
    pass

def do_sludge(me,opp):
    pass

def do_smog(me,opp):
    pass

def do_smokescreen(me,opp):
    pass

def do_softboiled(me,opp):
    pass

def do_solarbeam_prep(me,opp):
    pass

def do_solarbeam_attack(me,opp):
    beam(me,opp,type_='solar')

def do_sonicboom(me,opp):
    pass

def do_spike_cannon(me,opp):
    pass

def do_splash(me,opp):
    pass

def do_spore(me,opp):
    pass

def do_stomp(me,opp):
    pass

def do_strength(me,opp):
    pass

def do_string_shot(me,opp):
    pass

def do_struggle(me,opp):
    pass

def do_stun_spore(me,opp):
    pass

def do_submission(me,opp):
    pass

def do_substitute(me,opp):
    pass

def do_super_fang(me,opp):
    pass

def do_supersonic(me,opp):
    pass

def do_surf(me,opp):
    pass

def do_swift(me,opp):
    pass

def do_swords_dance(me,opp):
    pass

def do_tackle(me,opp):
    pass

def do_tail_whip(me,opp):
    pass

def do_take_down(me,opp):
    pass

def do_teleport(me,opp):
    pass

def do_thrash(me,opp):
    pass

def do_thunder(me,opp):
    pass

def do_thunder_wave(me,opp):
    pass

def do_thunderbolt(me,opp):
    pass

def do_thunderpunch(me,opp):
    pass

def do_thundershock(me,opp):
    pass

def do_toxic(me,opp):
    pass

def do_transform(me,opp):
    pass

def do_tri_attack(me,opp):
    pass

def do_twineedle(me,opp):
    pass

def do_vicegrip(me,opp):
    pass

def do_vine_whip(me,opp):
    pass

def do_water_gun(me,opp):
    pass

def do_waterfall(me,opp):
    pass

def do_whirlwind(me,opp):
    pass

def do_wing_attack(me,opp):
    pass

def do_withdraw(me,opp):
    pass

def do_wrap(me,opp):
    pass

