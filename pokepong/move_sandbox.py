from pygame import draw, display
import sys
from pygame.mixer import Sound
from pokepong.models import Move, Owned
from pokepong.database import db
import pygame
from pokepong.util import loadalphaimg, loadimg, alphabet, HIGH_ARC, LOW_ARC, sleep
from math import floor
pygame.mixer.init()
sleep(1)

SIZE = (1280, 1024)
WHITE = (255, 237, 255)
GREEN = (63, 156, 79)
YELLOW = (255, 228, 104)
RED = (209, 71, 40)
GREY = (108, 108, 108)
BLACK = (18, 11, 11)

SCREEN = display.set_mode(SIZE)
frontimg = loadimg('fronts/{0}.PNG'.format(34)).convert()
backimg = loadimg('backs/{0}.PNG'.format(34)).convert()
frontimg.set_colorkey((255, 255, 255))
backimg.set_colorkey((255, 255, 255))
POP = [loadalphaimg('pop1.png'), loadalphaimg('pop2.png'),
       loadalphaimg('pop3.png'), loadalphaimg('pop4.png'),
       loadalphaimg('pop5.png')]

BTM = loadalphaimg('btmclean.png')
MYHP = loadalphaimg('myhp.png')
OPPHP = loadalphaimg('opphp.png')
HPBAR = loadalphaimg('hpbar.png')
MYBAR = loadalphaimg('mybar.png')
OPPBAR = loadalphaimg('oppbar.png')
SSIZE = [392, 392]
BTM_TUPLE = (10, SIZE[1] - 340)
ALPHA = loadalphaimg('alphafull.png')
ALPHA_DICT = alphabet()
CONF = loadalphaimg('conf.png')
FORGET = loadalphaimg('forget.png')

MYHPBAR_RECT = [
    SIZE[0] - 700, SIZE[1] - 505, MYHP.get_width(), MYHP.get_height()]
MYHP_RECT = [SIZE[0] - 532, SIZE[1] - 486, 399, 14]
MYPKMN = [59, SIZE[1] - 736]

OPPHPBAR_RECT = [80, 120, 602, 91]
OPPHP_RECT = [227, 141, 399, 15]
OPPPKMN = [SIZE[0] - 500, 0]

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
          WHITE: BLACK,
          BLACK: WHITE,
          (0, 0, 0): WHITE,
          (24, 16, 16): WHITE}


def wait_for_button():
    pygame.event.clear()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return
        sleep(.1)


def selecting(select):
    dirty = []
    dirty.append(word_builder(['>', ' '][select] + 'YES', 50, 465))
    dirty.append(word_builder([' ', '>'][select] + 'NO', 50, 575))
    display.update(dirty)


def conf():
    display.update(draw.rect(
        SCREEN, WHITE, [3, 408, CONF.get_width() + 14, CONF.get_height() + 14]))
    display.update(SCREEN.blit(CONF, (10, 415)))
    select = 0
    pygame.event.clear()
    while True:
        selecting(select)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                if select == 0:
                    select = 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                if select == 1:
                    select = 0
            if event.type == pygame.KEYDOWN and ((event.key == pygame.K_z and select == 1) or event.key == pygame.K_x):
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                return True
        sleep(.01)


def word_builder(word, start_x, start_y):
    x = start_x
    draw.rect(SCREEN, WHITE, [x, start_y, len(word) * 56, 60])
    for l in word:
        SCREEN.blit(ALPHA, (start_x, start_y), ALPHA_DICT[l])
        start_x += 56
    return [x, start_y, len(word) * 56, 60]


def write_btm(*args):
    clearbtm()
    retval = []
    retval.append(SCREEN.blit(BTM, BTM_TUPLE))
    retval.append(word_builder(args[0], 50, SIZE[1] - 250))
    try:
        retval.append(word_builder(args[1], 50, SIZE[1] - 130))
    except:
        pass
    return retval

def clear():
    SCREEN.fill(WHITE)

def clearbtm():
    draw.rect(SCREEN, WHITE, [0, SIZE[1] - 340, SIZE[0], 340])


def draw_my_hp_bar():
    draw.rect(SCREEN, WHITE, MYHPBAR_RECT)
    SCREEN.blit(MYHP, MYHPBAR_RECT[:2])
    return [MYHPBAR_RECT]


def draw_my_lvl(pkmn):
    return [word_builder('%' + str(pkmn.lvl) + ' ', SIZE[0] - 405, SIZE[1] - 565)]


def draw_my_hp(pkmn):
    maxhp = pkmn.maxhp
    hp = pkmn.hp
    bar_len = floor(hp / float(maxhp) * 399)
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
        draw.rect(
            SCREEN, color, [MYHP_RECT[0], MYHP_RECT[1], bar_len, MYHP_RECT[3]])
    retval = []
    retval.append(MYHP_RECT)
    retval.append(
        word_builder('{0}/{1}'.format(hp, maxhp), SIZE[0] - 570, SIZE[1] - 445))
    return retval


def draw_my_pkmn_sprite(pkmn):
    draw.rect(SCREEN, WHITE, MYPKMN + SSIZE)
    SCREEN.blit(pkmn.backimg, MYPKMN)
    return [MYPKMN + SSIZE]


def draw_my_pkmn_name(pkmn):
    tmp = draw.rect(SCREEN, WHITE, [SIZE[0] - 630, SIZE[1] - 625, 600, 60])
    return [word_builder(pkmn.name.upper(), SIZE[0] - 630, SIZE[1] - 625), tmp]


def draw_opp_hp_bar():
    draw.rect(SCREEN, WHITE, OPPHPBAR_RECT)
    SCREEN.blit(OPPHP, OPPHPBAR_RECT[:2])
    return [OPPHPBAR_RECT]


def draw_opp_lvl(pkmn):
    return [word_builder('%' + str(pkmn.lvl) + ' ', 230, 60)]


def draw_opp_hp(pkmn):
    maxhp = pkmn.maxhp
    hp = pkmn.hp
    bar_len = floor(hp / float(maxhp) * 399)
    if bar_len < 100:
        color = RED
    elif bar_len < 200:
        color = YELLOW
    else:
        color = GREEN
    draw.rect(SCREEN, WHITE, OPPHP_RECT)
    if hp > 0:
        draw.rect(
            SCREEN, color, [OPPHP_RECT[0], OPPHP_RECT[1], bar_len, OPPHP_RECT[3]])
    return [OPPHP_RECT]


def draw_opp_pkmn_sprite(pkmn):
    draw.rect(SCREEN, WHITE, OPPPKMN + SSIZE)
    SCREEN.blit(pkmn.frontimg, OPPPKMN)
    return [OPPPKMN + SSIZE]


def draw_opp_pkmn_name(pkmn):
    tmp = draw.rect(SCREEN, WHITE, [60, 1, 600, 60])
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

    def __init__(self, current):
        self.current = current

# def invert():
#    pixels = pygame.surfarray.pixels3d(SCREEN)
#    pixels[:,:,:3] = CHANGE[(pixels[:,:,0],pixels[:,:,1],pixels[:,:,2])]


def low_big():
    norm = loadalphaimg('moves/Bignorm.png')
    return SCREEN.blit(norm, (760, 228))


def mid_big():
    norm = loadalphaimg('moves/Bignorm.png')
    return SCREEN.blit(norm, (896, 133))


def high_big():
    norm = loadalphaimg('moves/Bignorm.png')
    return SCREEN.blit(norm, (930, 0))


def big_3(attacker, defender):
    tmp = low_big()
    display.update(tmp)
    sleep(.25)
    draw.rect(SCREEN, WHITE, tmp)
    draw_opp_pkmn_sprite(defender)
    draw_all_me(attacker)

    tmp2 = mid_big()
    display.update([tmp, tmp2])
    draw.rect(SCREEN, WHITE, tmp2)
    sleep(.25)
    draw_opp_pkmn_sprite(defender)
    tmp = high_big()
    display.update([tmp, tmp2])
    draw.rect(SCREEN, WHITE, tmp)
    sleep(.25)
    draw_opp_pkmn_sprite(defender)
    display.update(tmp)


def opp_low_big():
    norm = loadalphaimg('moves/Bignorm.png')
    return SCREEN.blit(norm, (20, 450))


def opp_mid_big():
    norm = loadalphaimg('moves/Bignorm.png')
    return SCREEN.blit(norm, (156, 345))


def opp_high_big():
    norm = loadalphaimg('moves/Bignorm.png')
    return SCREEN.blit(norm, (190, 222))


def opp_big_3(attacker, defender):
    tmp = opp_low_big()
    display.update(tmp)
    draw.rect(SCREEN, WHITE, tmp)
    draw_my_pkmn_sprite(defender)
    sleep(.25)
    tmp2 = opp_mid_big()
    display.update([tmp, tmp2])
    draw.rect(SCREEN, WHITE, tmp2)
    sleep(.25)
    draw_my_pkmn_sprite(defender)
    tmp = opp_high_big()
    display.update([tmp, tmp2])
    draw.rect(SCREEN, WHITE, tmp)
    sleep(.25)
    draw_my_pkmn_sprite(defender)
    display.update(tmp)

def right_med():
    norm = loadalphaimg('moves/Mednorm.png')
    return SCREEN.blit(norm, (990, 133))


def left_med():
    norm = loadalphaimg('moves/Mednorm.png')
    return SCREEN.blit(norm, (770, 169))


def mid_med():
    norm = loadalphaimg('moves/Mednorm.png')
    return SCREEN.blit(norm, (876, 228))


def med_3(attacker, defender):
    tmp = right_med()
    display.update(tmp)
    draw.rect(SCREEN, WHITE, tmp)
    draw_opp_pkmn_sprite(defender)
    sleep(.2)
    tmp2 = left_med()
    display.update([tmp, tmp2])
    draw.rect(SCREEN, WHITE, tmp2)
    sleep(.2)
    draw_opp_pkmn_sprite(defender)
    tmp = mid_med()
    display.update([tmp, tmp2])
    draw.rect(SCREEN, WHITE, tmp)
    sleep(.2)
    draw_opp_pkmn_sprite(defender)
    display.update(tmp)

def opp_right_med():
    norm = loadalphaimg('moves/Mednorm.png')
    return SCREEN.blit(norm, (350, 350))


def opp_left_med():
    norm = loadalphaimg('moves/Mednorm.png')
    return SCREEN.blit(norm, (130, 386))


def opp_mid_med():
    norm = loadalphaimg('moves/Mednorm.png')
    return SCREEN.blit(norm, (236, 445))


def opp_med_3(attacker, defender):
    tmp = opp_right_med()
    display.update(tmp)
    draw.rect(SCREEN, WHITE, tmp)
    draw_my_pkmn_sprite(defender)
    sleep(.2)
    tmp2 = opp_left_med()
    display.update([tmp, tmp2])
    draw.rect(SCREEN, WHITE, tmp2)
    sleep(.2)
    draw_my_pkmn_sprite(defender)
    tmp = opp_mid_med()
    display.update([tmp, tmp2])
    draw.rect(SCREEN, WHITE, tmp)
    sleep(.2)
    draw_my_pkmn_sprite(defender)
    display.update(tmp)


def left_double():
    norm = loadalphaimg('moves/Mednorm.png')
    return SCREEN.blit(norm, (820, 133))


def right_double():
    norm = loadalphaimg('moves/Mednorm.png')
    return SCREEN.blit(norm, (930, 222))


def double(attacker, defender):
    tmp = left_double()
    display.update(tmp)
    draw_opp_pkmn_sprite(defender)
    sleep(.15)
    tmp2 = right_double()
    display.update([tmp, tmp2])
    sleep(.15)
    draw_opp_pkmn_sprite(defender)
    display.update(tmp2)

def opp_left_double():
    norm = loadalphaimg('moves/Mednorm.png')
    return SCREEN.blit(norm, (170, 350))


def opp_right_double():
    norm = loadalphaimg('moves/Mednorm.png')
    return SCREEN.blit(norm, (280, 439))


def opp_double(attacker, defender):
    tmp = opp_left_double()
    display.update(tmp)
    draw_my_pkmn_sprite(defender)
    sleep(.15)
    tmp2 = opp_right_double()
    display.update([tmp, tmp2])
    sleep(.15)
    draw_my_pkmn_sprite(defender)
    display.update(tmp2)

def high_arch_away(left, right, img):
    old = [[0, 0], [0, 0]]
    for x in HIGH_ARC:
        draw_all_opp(right)
        draw_my_pkmn_sprite(left)
        tmp = SCREEN.blit(img, x)
        display.update([old, tmp])
        sleep(.2)
        old = tmp
        draw.rect(SCREEN, WHITE, old)
    sleep(.2)
    draw_opp_pkmn_sprite(left)
    display.update(old)


def high_arch_towards(left, right, img):
    old = [0, 0, 0, 0]
    for x in HIGH_ARC[::-1]:
        draw_all_opp(right)
        draw_my_pkmn_sprite(left)
        tmp = SCREEN.blit(img, x)
        display.update([old, tmp])
        sleep(.2)
        old = tmp
        draw.rect(SCREEN, WHITE, old)
    sleep(.2)
    draw_my_pkmn_sprite(left)
    display.update(old)


def low_arch_away(left, right, img):
    old = [0, 0, 0, 0]
    for x in LOW_ARC:
        draw_all_opp(right)
        draw_my_pkmn_sprite(left)
        tmp = SCREEN.blit(img, x)
        display.update([old, tmp])
        sleep(.15)
        old = tmp
        draw.rect(SCREEN, WHITE, old)
    sleep(.15)
    draw_opp_pkmn_sprite(right)
    display.update(old)


def low_arch_towards(left, right, img):
    old = [0, 0, 0, 0]
    for x in LOW_ARC[::-1]:
        draw_all_opp(right)
        draw_my_pkmn_sprite(left)
        tmp = SCREEN.blit(img, x)
        display.update([old, tmp])
        sleep(.15)
        old = tmp
        draw.rect(SCREEN, WHITE, old)
    sleep(.15)
    draw_my_pkmn_sprite(left)
    display.update(old)


def ask_move(pkmn, move):
    display.update(write_btm(pkmn.name.upper() + ' is', 'trying to learn'))
    wait_for_button()
    display.update(write_btm('trying to learn', move.name.upper() + '!'))
    wait_for_button()
    display.update(write_btm('but ' + pkmn.name.upper(), "can't learn more"))
    wait_for_button()
    display.update(write_btm("can't learn more", 'than 4 moves!'))
    wait_for_button()
    display.update(write_btm('Delete an older', 'move to make room'))
    wait_for_button()
    display.update(
        write_btm('move to make room', 'for ' + move.name.upper() + '?'))


def update_move(selector):
    dirty = []
    dirty.append(
        word_builder(['>', ' ', ' ', ' '][selector], 300, SIZE[1] - 573))
    dirty.append(
        word_builder([' ', '>', ' ', ' '][selector], 300, SIZE[1] - 513))
    dirty.append(
        word_builder([' ', ' ', '>', ' '][selector], 300, SIZE[1] - 453))
    dirty.append(
        word_builder([' ', ' ', ' ', '>'][selector], 300, SIZE[1] - 393))
    display.update(dirty)


def move_choose(pkmn):
    selector = 0
    dirty = []
    dirty.append(word_builder(
        ['>', ' ', ' ', ' '][selector] + pkmn.moves[0].name.upper(), 300, SIZE[1] - 573))
    dirty.append(word_builder(
        [' ', '>', ' ', ' '][selector] + pkmn.moves[1].name.upper(), 300, SIZE[1] - 513))
    dirty.append(word_builder(
        [' ', ' ', '>', ' '][selector] + pkmn.moves[2].name.upper(), 300, SIZE[1] - 453))
    dirty.append(word_builder(
        [' ', ' ', ' ', '>'][selector] + pkmn.moves[3].name.upper(), 300, SIZE[1] - 393))
    display.update(dirty)
    pygame.event.clear()
    while True:
        update_move(selector)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                if selector < 3:
                    selector += 1
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                if selector > 0:
                    selector -= 1
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                return -1
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                return selector


def new_move(pkmn, move):
    orig = SCREEN.copy()
    while True:
        ask_move(pkmn, move)
        if conf():
            SCREEN.blit(orig, (0, 0))
            clearbtm()
            display.update(
                pygame.draw.rect(SCREEN, WHITE, (258, 386, SIZE[0] - 258, SIZE[1] - 386)))
            display.flip()
            tmp = SCREEN.blit(FORGET, (10, 396))
            word_builder('Which move should', 50, SIZE[1] - 250)
            word_builder('be forgotten?', 50, SIZE[1] - 130)
            display.update(tmp)
            retval = move_choose(pkmn)
            if retval > -1:
                display.update(write_btm('1, 2 and... Poof!'))
                wait_for_button()
                display.update(
                    write_btm(pkmn.name.upper() + ' forgot', pkmn.moves[retval].name + '!'))
                wait_for_button()
                display.update(write_btm('And...'))
                wait_for_button()
                display.update(
                    write_btm(pkmn.name.upper() + ' learned', move.name + '!'))
                setattr(pkmn, 'pp' + str(retval + 1), 0)
                setattr(pkmn, 'move' + str(retval + 1), move)
                pkmn.moves[retval] = Move(move, 0)
                db.add(pkmn)
                db.commit()
                SCREEN.blit(orig, (0, 0))
                display.flip()
                return retval
            else:
                SCREEN.blit(orig, (0, 0))
                display.flip()
                continue

        else:
            display.update(
                write_btm('Abandon learning', move.name.upper() + '?'))
            if conf():
                display.update(write_btm(pkmn.name.upper(), 'did not learn'))
                wait_for_button()
                display.update(write_btm('did not learn', move.name.upper()))
                wait_for_button()
                SCREEN.blit(orig, (0, 0))
                display.flip()
                return False
            else:
                SCREEN.blit(orig, (0, 0))
                display.flip()
                continue





def wave(count):
    orig = SCREEN.copy()
    tmp1 = SCREEN.copy()
    tmp2 = SCREEN.copy()
    tmp1.fill(WHITE)
    tmp2.fill(WHITE)
    for i in range(SIZE[1] / 14 + 1):
        t = i % 8
        if t > 4:
            t = 8 - t
        t = t - 2
        tmp1.blit(SCREEN, (t * 7, i * 14), (0, i * 14, SIZE[0], (i + 1) * 14))
        tmp2.blit(SCREEN, (t * -7, i * 14), (0, i * 14, SIZE[0], (i + 1) * 14))
    for c in range(count):
        SCREEN.blit(tmp1, (0, 0))
        display.flip()
        sleep(.1)
        SCREEN.blit(tmp2, (0, 0))
        display.flip()
        sleep(.1)
    SCREEN.blit(orig, (0, 0))
    display.flip()


def convert(array):
    return CHANGE[tuple(array)]


def invert():
    pixels = pygame.surfarray.pixels2d(SCREEN)
    pixels ^= 2 ** 32 - 1
    del pixels
    pygame.display.flip()
    SCREEN.unlock()


def dmged():
    tmp = SCREEN.copy()
    clear()
    SCREEN.blit(tmp, (7, 0))
    pygame.display.flip()
    sleep(.2)
    clear()
    SCREEN.blit(tmp, (0, 0))
    pygame.display.flip()
    sleep(.2)
    clear()
    SCREEN.blit(tmp, (7, 0))
    pygame.display.flip()
    sleep(.2)
    clear()
    SCREEN.blit(tmp, (0, 0))
    pygame.display.flip()


def beam(attacker, defender, attacking, type_=None):
    beams = []
    if attacking:
        if type_ == 'aurora':
            for i in range(1, 7):
                beams.append(loadalphaimg('moves/aurora{0}.png'.format(i)))
        elif type_ == 'ice':
            for i in range(1, 7):
                beams.append(loadalphaimg('moves/icebeam{0}.png'.format(i)))
        elif type_ == 'psy':
            for i in range(1, 7):
                beams.append(loadalphaimg('moves/psybeam{0}.png'.format(i)))
        elif type_ == 'solar':
            for i in range(1, 7):
                beams.append(loadalphaimg('moves/solarbeam{0}.png'.format(i)))
        else:
            for i in range(1, 7):
                beams.append(loadalphaimg('moves/beam{0}.png'.format(i)))
        x = SCREEN.blit(beams[0], (339, 232))
        for i in beams:
            pygame.draw.rect(SCREEN, WHITE, x)
            draw_all_me(attacker)
            draw_all_opp(defender)
            display.update(SCREEN.blit(i, (339, 232)))
            sleep(.1)

        display.update(pygame.draw.rect(SCREEN, WHITE, x))
        draw_all_me(attacker)
        draw_all_opp(defender)
    else:
        if type_ == 'aurora':
            for i in range(1, 7):
                beams.append(loadalphaimg('moves/opp_aurora{0}.png'.format(i)))
        elif type_ == 'ice':
            for i in range(1, 7):
                beams.append(loadalphaimg('moves/opp_icebeam{0}.png'.format(i)))
        elif type_ == 'psy':
            for i in range(1, 7):
                beams.append(loadalphaimg('moves/opp_psybeam{0}.png'.format(i)))
        elif type_ == 'solar':
            for i in range(1, 7):
                beams.append(loadalphaimg('moves/opp_solarbeam{0}.png'.format(i)))
        else:
            for i in range(1, 7):
                beams.append(loadalphaimg('moves/opp_beam{0}.png'.format(i)))
        x = SCREEN.blit(beams[0], (339, 232))
        for i in beams:
            pygame.draw.rect(SCREEN, WHITE, x)
            draw_all_me(defender)
            draw_all_opp(attacker)
            display.update(SCREEN.blit(i, (339, 232)))
            sleep(.1)

        display.update(pygame.draw.rect(SCREEN, WHITE, x))
        draw_all_me(defender)
        draw_all_opp(attacker)


def sandbox():
    SCREEN.fill(WHITE)
    SCREEN.blit(BTM, BTM_TUPLE)
    display.flip()
    me = trainer(Owned.query.get(153))
    opp = trainer(Owned.query.get(152))
    draw_all_opp(opp.current)
    draw_all_me(me.current)
    do_cut(me.current,opp.current,True)
    sleep(2)
    do_cut(opp.current,me.current,False)

    sleep(15)

def do_absorb(attacker, defender, attacking):
    s = Sound("sounds/Absorb.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_acid(attacker, defender, attacking):
    s = Sound("sounds/Acid.ogg")
    tmp = loadalphaimg('moves/acid.png')
    drop = loadalphaimg('moves/drop.png')
    s.play()
    if attacking:
        low_arch_away(attacker,defender,tmp)
        display.update(SCREEN.blit(tmp,LOW_ARC[-1]))
        display.update(SCREEN.blit(drop, (900,220)))
        draw_opp_pkmn_sprite(defender)
        sleep(.1)
        display.update([900,220, drop.get_width(), drop.get_height()])
        display.update(SCREEN.blit(drop, (900,270)))
        draw_opp_pkmn_sprite(defender)
        sleep(.1)
        display.update([900,270, drop.get_width(), drop.get_height()])

        display.update(SCREEN.blit(drop, (900,320)))
        draw_opp_pkmn_sprite(defender)
        sleep(.1)
        display.update([900,320, drop.get_width(), drop.get_height()])
        display.update(SCREEN.blit(drop, (950,220)))
        draw_opp_pkmn_sprite(defender)
        sleep(.1)
        display.update([950,220, drop.get_width(), drop.get_height()])
        display.update(SCREEN.blit(drop, (950,270)))
        draw_opp_pkmn_sprite(defender)
        sleep(.1)
        display.update([950,270, drop.get_width(), drop.get_height()])
        display.update(SCREEN.blit(drop, (950,320)))
        sleep(.1)
        display.update(draw_opp_pkmn_sprite(defender))
    else:
        low_arch_towards(defender,attacker,tmp)
        display.update(SCREEN.blit(tmp,(200,400)))
        display.update(SCREEN.blit(drop, (220,510)))
        draw_my_pkmn_sprite(defender)
        sleep(.1)
        display.update([220,510, drop.get_width(), drop.get_height()])
        display.update(SCREEN.blit(drop, (220,560)))
        draw_my_pkmn_sprite(defender)
        sleep(.1)
        display.update([220,560, drop.get_width(), drop.get_height()])

        display.update(SCREEN.blit(drop, (220,610)))
        draw_my_pkmn_sprite(defender)
        sleep(.1)
        display.update([220,610, drop.get_width(), drop.get_height()])
        display.update(SCREEN.blit(drop, (270,510)))
        draw_my_pkmn_sprite(defender)
        sleep(.1)
        display.update([270,510, drop.get_width(), drop.get_height()])
        display.update(SCREEN.blit(drop, (270,560)))
        draw_my_pkmn_sprite(defender)
        sleep(.1)
        display.update([270,560, drop.get_width(), drop.get_height()])
        display.update(SCREEN.blit(drop, (270,610)))
        sleep(.1)
        display.update(draw_my_pkmn_sprite(defender))
    dmged()
    s.stop()


def do_acid_armor(attacker, defender, attacking):
    s = Sound("sounds/Acid Armor.ogg")
    s.play()
    if attacking:
        for i in range(0, 400, 2):
            draw.rect(SCREEN, WHITE, [59, SIZE[1] - 740, 392, 398])
            SCREEN.blit(
                attacker.backimg, (59, SIZE[1] - 740 + i), (0, 0, 392, 392 - i))
            display.update(59, SIZE[1] - 742 + i, 392, 398 - i)
        display.update(draw_my_pkmn_sprite(attacker))
    else:
        for i in range(0, 393, 2):
            draw.rect(SCREEN, WHITE, [SIZE[0] - 500, 0, 392, 398])
            SCREEN.blit(
                attacker.frontimg, (SIZE[0] - 500, i), (0, 0, 392, 392 - i))
            display.update([SIZE[0] - 500, i - 2, 392, 398 - i])
        display.update(draw_opp_pkmn_sprite(attacker))
    s.stop()


def do_agility(attacker, defender, attacking):
    s = Sound("sounds/Agility.ogg")
    s.play()
    sleep(s.get_length())
    s.stop()


def do_amnesia(attacker, defender, attacking):
    s = Sound("sounds/Amnesia.ogg")
    tmp = loadalphaimg('moves/amnesia.png')
    s.play()
    if attacking:
        display.update(SCREEN.blit(tmp,(300,300)))
        sleep(.2)
        draw.rect(SCREEN, WHITE, [300,300,tmp.get_width(),tmp.get_height()])
        draw_my_pkmn_sprite(attacker)
        display.update([300,300,tmp.get_width(),tmp.get_height()])
        display.update(SCREEN.blit(tmp,(500,350)))
        sleep(.2)
        draw.rect(SCREEN, WHITE, [500,350,tmp.get_width(),tmp.get_height()])
        draw_my_pkmn_sprite(attacker)
        display.update([500,350,tmp.get_width(),tmp.get_height()])
        display.update(SCREEN.blit(tmp,(300,300)))
        sleep(.2)
        draw.rect(SCREEN, WHITE, [300,300,tmp.get_width(),tmp.get_height()])
        draw_my_pkmn_sprite(attacker)
        display.update([300,300,tmp.get_width(),tmp.get_height()])
        display.update(SCREEN.blit(tmp,(500,350)))
        sleep(.2)
        draw.rect(SCREEN, WHITE, [500,350,tmp.get_width(),tmp.get_height()])
        draw_my_pkmn_sprite(attacker)
        display.update([500,350,tmp.get_width(),tmp.get_height()])
    else:
        display.update(SCREEN.blit(tmp,(900,20)))
        sleep(.2)
        draw.rect(SCREEN, WHITE, [900,20,tmp.get_width(),tmp.get_height()])
        draw_opp_pkmn_sprite(attacker)
        display.update([900,20,tmp.get_width(),tmp.get_height()])
        display.update(SCREEN.blit(tmp,(1100,70)))
        sleep(.2)
        draw.rect(SCREEN, WHITE, [1100,70,tmp.get_width(),tmp.get_height()])
        draw_opp_pkmn_sprite(attacker)
        display.update([1100,70,tmp.get_width(),tmp.get_height()])
        display.update(SCREEN.blit(tmp,(900,20)))
        sleep(.2)
        draw.rect(SCREEN, WHITE, [900,20,tmp.get_width(),tmp.get_height()])
        draw_opp_pkmn_sprite(attacker)
        display.update([900,20,tmp.get_width(),tmp.get_height()])
        display.update(SCREEN.blit(tmp,(1100,70)))
        sleep(.2)
        draw.rect(SCREEN, WHITE, [1100,70,tmp.get_width(),tmp.get_height()])
        draw_opp_pkmn_sprite(attacker)
        display.update([1100,70,tmp.get_width(),tmp.get_height()])
    s.stop()


def do_aurora_beam(attacker, defender, attacking):
    s = Sound("sounds/Aurora Beam.ogg")
    s.play()
    if attacking:
        beam(attacker, defender, attacking, type_='aurora')
    else:
        beam(defender, attacker, attacking, type_='aurora')
    dmged()
    s.stop()


def do_barrage(attacker, defender, attacking):
    s = Sound("sounds/Barrage.ogg")
    tmp = loadalphaimg('moves/barrage.png')
    s.play()
    if attacking:
        low_arch_away(attacker, defender, tmp)
    else:
        low_arch_towards(defender, attacker, tmp)
    dmged()
    s.stop()


def do_barrier(attacker, defender, attacking):
    s = Sound("sounds/Barrier.ogg")
    if attacking:
        tmp = loadalphaimg('moves/barrier.png')
    else:
        tmp = loadalphaimg('moves/opp_barrier.png')
    s.play()
    if attacking:

        display.update(SCREEN.blit(tmp,(470,285)))
        sleep(.15)
        draw.rect(SCREEN, WHITE, (470,285, tmp.get_width(), tmp.get_height()))
        draw_my_pkmn_sprite(attacker)
        display.update([470,285, tmp.get_width(), tmp.get_height()])
        sleep(.15)
        display.update(SCREEN.blit(tmp,(470,285)))
        sleep(.15)
        draw.rect(SCREEN, WHITE, (470,285, tmp.get_width(), tmp.get_height()))
        draw_my_pkmn_sprite(attacker)
        display.update([470,285, tmp.get_width(), tmp.get_height()])
        sleep(.15)
        display.update(SCREEN.blit(tmp,(470,285)))
        sleep(.15)
        draw.rect(SCREEN, WHITE, (470,285, tmp.get_width(), tmp.get_height()))
        draw_my_pkmn_sprite(attacker)
        display.update([470,285, tmp.get_width(), tmp.get_height()])
        sleep(.15)
        display.update(SCREEN.blit(tmp,(470,285)))
        sleep(.15)
        draw.rect(SCREEN, WHITE, (470,285, tmp.get_width(), tmp.get_height()))
        draw_my_pkmn_sprite(attacker)
        display.update([470,285, tmp.get_width(), tmp.get_height()])
        sleep(.15)
        display.update(SCREEN.blit(tmp,(470,285)))
        sleep(.15)
        draw.rect(SCREEN, WHITE, (470,285, tmp.get_width(), tmp.get_height()))
        draw_my_pkmn_sprite(attacker)
        display.update([470,285, tmp.get_width(), tmp.get_height()])
        sleep(.15)
        display.update(SCREEN.blit(tmp,(470,285)))
        sleep(.15)
        draw.rect(SCREEN, WHITE, (470,285, tmp.get_width(), tmp.get_height()))
        draw_my_pkmn_sprite(attacker)
        display.update([470,285, tmp.get_width(), tmp.get_height()])
        sleep(.15)
    else:

        display.update(SCREEN.blit(tmp,(700,0)))
        sleep(.15)
        draw.rect(SCREEN, WHITE, (700,0, tmp.get_width(), tmp.get_height()))
        draw_my_pkmn_sprite(attacker)
        display.update([700,0, tmp.get_width(), tmp.get_height()])
        sleep(.15)
        display.update(SCREEN.blit(tmp,(700,0)))
        sleep(.15)
        draw.rect(SCREEN, WHITE, (700,0, tmp.get_width(), tmp.get_height()))
        draw_my_pkmn_sprite(attacker)
        display.update([700,0, tmp.get_width(), tmp.get_height()])
        sleep(.15)
        display.update(SCREEN.blit(tmp,(700,0)))
        sleep(.15)
        draw.rect(SCREEN, WHITE, (700,0, tmp.get_width(), tmp.get_height()))
        draw_my_pkmn_sprite(attacker)
        display.update([700,0, tmp.get_width(), tmp.get_height()])
        sleep(.15)
        display.update(SCREEN.blit(tmp,(700,0)))
        sleep(.15)
        draw.rect(SCREEN, WHITE, (700,0, tmp.get_width(), tmp.get_height()))
        draw_my_pkmn_sprite(attacker)
        display.update([700,0, tmp.get_width(), tmp.get_height()])
        sleep(.15)
        display.update(SCREEN.blit(tmp,(700,0)))
        sleep(.15)
        draw.rect(SCREEN, WHITE, (700,0, tmp.get_width(), tmp.get_height()))
        draw_my_pkmn_sprite(attacker)
        display.update([700,0, tmp.get_width(), tmp.get_height()])
        sleep(.15)
        display.update(SCREEN.blit(tmp,(700,0)))
        sleep(.15)
        draw.rect(SCREEN, WHITE, (700,0, tmp.get_width(), tmp.get_height()))
        draw_my_pkmn_sprite(attacker)
        display.update([700,0, tmp.get_width(), tmp.get_height()])
        sleep(.15)
    s.stop()


def do_bide_prep(attacker, defender, attacking):
    if attacking:
        pass
    else:
        pass

def do_bide(attacker, defender, attacking):
    s = Sound("sounds/Bide.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_bind(attacker, defender, attacking):
    s = Sound("sounds/Bind.ogg")
    tmp = loadalphaimg('moves/bind.png')

    s.play()
    if attacking:
        display.update(SCREEN.blit(tmp,(720,100)))
        sleep(.2)
        draw.rect(SCREEN, WHITE, (720,100, tmp.get_width(), tmp.get_height()))
        draw_opp_pkmn_sprite(defender)
        display.update([720,100, tmp.get_width(), tmp.get_height()])
        sleep(.2)
        display.update(SCREEN.blit(tmp,(720,100)))
        sleep(.2)
        draw.rect(SCREEN, WHITE, (720,100, tmp.get_width(), tmp.get_height()))
        draw_opp_pkmn_sprite(defender)
        display.update([720,100, tmp.get_width(), tmp.get_height()])
        sleep(.2)
    else:
        display.update(SCREEN.blit(tmp,(40,450)))
        sleep(.2)
        draw.rect(SCREEN, WHITE, (40,450, tmp.get_width(), tmp.get_height()))
        draw_my_pkmn_sprite(defender)
        display.update([40,450, tmp.get_width(), tmp.get_height()])
        sleep(.2)
        display.update(SCREEN.blit(tmp,(40,450)))
        sleep(.2)
        draw.rect(SCREEN, WHITE, (40,450, tmp.get_width(), tmp.get_height()))
        draw_my_pkmn_sprite(defender)
        display.update([40,450, tmp.get_width(), tmp.get_height()])
        sleep(.2)
    dmged()
    s.stop()


def do_bite(attacker, defender, attacking):
    s = Sound("sounds/Bite.ogg")
    s.play()
    if attacking:
        med_3(attacker, defender)
    else:
        opp_med_3(attacker, defender)
    dmged()
    s.stop()


def do_blizzard(attacker, defender, attacking):
    s = Sound("sounds/Blizzard.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_body_slam(attacker, defender, attacking):
    s = Sound("sounds/Body Slam.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_bone_club(attacker, defender, attacking):
    s = Sound("sounds/Bone Club.ogg")
    s.play()
    if attacking:
        med_3(attacker, defender)
    else:
        opp_med_3(attacker, defender)
    dmged()
    s.stop()


def do_bonemerang(attacker, defender, attacking):
    s = Sound("sounds/Bonmerang.ogg")
    s.play()
    if attacking:
        med_3(attacker, defender)
    else:
        opp_med_3(attacker, defender)
    dmged()
    s.stop()


def do_bubble(attacker, defender, attacking):
    s = Sound("sounds/Bubble.ogg")
    tmp = SCREEN.copy()
    bubble = []
    if attacking:
        for i in range(1, 5):
            bubble.append(loadalphaimg('moves/bubble{0}.png'.format(i)))
    else:
        for i in range(1, 5):
            bubble.append(loadalphaimg('moves/opp_bubble{0}.png'.format(i)))
    s.play()
    if attacking:
        for i in range(4):
            display.update(SCREEN.blit(bubble[i],(450,50)))
            sleep(.3)
    else:
        for i in range(4):
            display.update(SCREEN.blit(bubble[i],(200,200)))
            sleep(.3)
    dmged()
    SCREEN.blit(tmp,(0,0))
    display.flip()
    s.stop()


def do_bubblebeam(attacker, defender, attacking):
    s = Sound("sounds/Bubble Beam.ogg")
    tmp = SCREEN.copy()
    bubble = []
    if attacking:
        for i in range(1, 5):
            bubble.append(loadalphaimg('moves/bubble{0}.png'.format(i)))
    else:
        for i in range(1, 5):
            bubble.append(loadalphaimg('moves/opp_bubble{0}.png'.format(i)))
    s.play()
    if attacking:
        for i in range(4):
            display.update(SCREEN.blit(bubble[i],(450,50)))
            sleep(.3)
    else:
        for i in range(4):
            display.update(SCREEN.blit(bubble[i],(200,200)))
            sleep(.3)
    dmged()
    SCREEN.blit(tmp,(0,0))
    display.flip()
    s.stop()


def do_clamp(attacker, defender, attacking):
    s = Sound("sounds/Clamp.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_comet_punch(attacker, defender, attacking):
    s = Sound("sounds/Comet Punch.ogg")
    s.play()
    if attacking:
        med_3(attacker, defender)
        med_3(attacker, defender)
    else:
        opp_med_3(attacker, defender)
        opp_med_3(attacker, defender)
    dmged()
    s.stop()


def do_confuse_ray(attacker, defender, attacking):
    s = Sound("sounds/Confuse Ray.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_confusion(attacker, defender, attacking):
    s = Sound("sounds/Confusion.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_constrict(attacker, defender, attacking):
    s = Sound("sounds/Constrict.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_conversion(attacker, defender, attacking):
    s = Sound("sounds/Conversion.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_counter(attacker, defender, attacking):
    s = Sound("sounds/Counter.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_crabhammer(attacker, defender, attacking):
    s = Sound("sounds/Crabhammer.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_cut(attacker, defender, attacking):
    s = Sound("sounds/Cut.ogg")
    tmp = loadalphaimg('moves/cut1.png')
    tmp2 = loadalphaimg('moves/cut2.png')
    s.play()
    if attacking:
        display.update(SCREEN.blit(tmp,(800,10)))
        sleep(.15)
        display.update(draw_opp_pkmn_sprite(defender))
        display.update(SCREEN.blit(tmp2,(800,10)))
        sleep(.15)
        display.update(draw_opp_pkmn_sprite(defender))
    else:
        display.update(SCREEN.blit(tmp,(70,300)))
        sleep(.15)
        display.update(draw_my_pkmn_sprite(defender))
        display.update(SCREEN.blit(tmp2,(70,300)))
        sleep(.15)
        display.update(draw_my_pkmn_sprite(defender))
    dmged()
    s.stop()


def do_defense_curl(attacker, defender, attacking):
    s = Sound("sounds/Defence Curl.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_dig(attacker, defender, attacking):
    s = Sound("sounds/Dig1.ogg")
    s.play()
    if attacking:
        draw_my_pkmn_sprite(attacker)
        med_3(attacker,defender)
    else:
        draw_opp_pkmn_sprite(attacker)
        opp_med_3(attacker,defender)
    dmged()
    s.stop()


def do_dig_prep(attacker, defender, attacking):
    s = Sound("sounds/Dig2.ogg")
    s.play()
    if attacking:
        display.update(draw.rect(SCREEN, WHITE, MYPKMN + [attacker.backimg.get_width(),attacker.backimg.get_width()]))
    else:
        display.update(draw.rect(SCREEN, WHITE, OPPPKMN + [attacker.backimg.get_width(),attacker.backimg.get_width()]))
    s.stop()


def do_disable(attacker, defender, attacking):
    s = Sound("sounds/Disable.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_dizzy_punch(attacker, defender, attacking):
    s = Sound("sounds/Dizzy Punch.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_double_kick(attacker, defender, attacking):
    s = Sound("sounds/Double-Egde.ogg")
    s.play()
    if attacking:
        double(attacker, defender)
        sleep(.15)
        double(attacker, defender)
    else:
        opp_double(attacker, defender)
        sleep(.15)
        opp_double(attacker, defender)
    dmged()
    s.stop()


def do_double_team(attacker, defender, attacking):
    s = Sound("sounds/Double Kick.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_double_edge(attacker, defender, attacking):
    s = Sound("sounds/Double Team.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_doubleslap(attacker, defender, attacking):
    s = Sound("sounds/DoubleSlap.ogg")
    s.play()
    if attacking:
        double(attacker, defender)
        sleep(.15)
        double(attacker, defender)
    else:
        opp_double(attacker, defender)
        sleep(.15)
        opp_double(attacker, defender)
    dmged()
    s.stop()


def do_dragon_rage(attacker, defender, attacking):
    s = Sound("sounds/Dragon Rage.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_dream_eater(attacker, defender, attacking):
    s = Sound("sounds/Dream Eater.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_drill_peck(attacker, defender, attacking):
    s = Sound("sounds/Drill Peck.ogg")
    s.play()
    if attacking:
        big_3(attacker, defender)
    else:
        opp_big_3(attacker, defender)
    dmged()
    s.stop()


def do_earthquake(attacker, defender, attacking):
    s = Sound("sounds/Earthquake.ogg")
    s.play()
    dmged()
    dmged()
    dmged()
    dmged()
    dmged()
    dmged()
    s.stop()


def do_egg_bomb(attacker, defender, attacking):
    s = Sound("sounds/Egg Bomb.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_ember(attacker, defender, attacking):
    s = Sound("sounds/Ember.ogg")
    small = loadalphaimg('moves/smallfire.png')
    big = loadalphaimg('moves/bigfire.png')
    s.play()
    if attacking:
        display.update(SCREEN.blit(small,(800,280)))
        sleep(.2)
        display.update(draw_opp_pkmn_sprite(defender))
        display.update(SCREEN.blit(big,(800,280)))
        sleep(.2)
        display.update(draw_opp_pkmn_sprite(defender))
        display.update(SCREEN.blit(small,(1000,280)))
        sleep(.2)
        display.update(draw_opp_pkmn_sprite(defender))
        display.update(SCREEN.blit(big,(1000,280)))
        sleep(.2)
        display.update(draw_opp_pkmn_sprite(defender))
        display.update(SCREEN.blit(small,(900,280)))
        sleep(.2)
        display.update(draw_opp_pkmn_sprite(defender))
        display.update(SCREEN.blit(big,(900,280)))
        sleep(.2)
        display.update(draw_opp_pkmn_sprite(defender))
    else:
        display.update(SCREEN.blit(small,(100,568)))
        sleep(.2)
        display.update(draw_my_pkmn_sprite(defender))
        display.update(SCREEN.blit(big,(100,568)))
        sleep(.2)
        display.update(draw_my_pkmn_sprite(defender))
        display.update(SCREEN.blit(small,(300,568)))
        sleep(.2)
        display.update(draw_my_pkmn_sprite(defender))
        display.update(SCREEN.blit(big,(300,568)))
        sleep(.2)
        display.update(draw_my_pkmn_sprite(defender))
        display.update(SCREEN.blit(small,(200,568)))
        sleep(.2)
        display.update(draw_my_pkmn_sprite(defender))
        display.update(SCREEN.blit(big,(200,568)))
        sleep(.2)
        display.update(draw_my_pkmn_sprite(defender))
    dmged()
    s.stop()


def do_explosion(attacker, defender, attacking):
    s = Sound("sounds/Explosion.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_fire_blast(attacker, defender, attacking):
    s = Sound("sounds/Fire Blast.ogg")
    orig = SCREEN.copy()
    s.play()
    big = loadalphaimg('moves/bigfire.png')
    smallblast = loadalphaimg('moves/smallblast.png')
    bigblast = loadalphaimg('moves/bigblast.png')

    if attacking:
        display.update(SCREEN.blit(big,(230,500)))
        sleep(.15)
        display.update(SCREEN.blit(big,(380,425)))
        sleep(.15)
        display.update(SCREEN.blit(big,(530,350)))
        sleep(.15)
        display.update(SCREEN.blit(big,(680,275)))
        sleep(.15)
        display.update(SCREEN.blit(big,(830,200)))
        sleep(.15)
        display.update(SCREEN.blit(orig,(0,0)))
        display.update(SCREEN.blit(smallblast, (800,50)))
        sleep(.15)
        display.update(SCREEN.blit(bigblast, (800,50)))
        sleep(.15)
        display.update(draw_opp_pkmn_sprite(defender))
        sleep(.1)
        display.update(SCREEN.blit(smallblast, (800,50)))
        sleep(.15)
        display.update(SCREEN.blit(bigblast, (800,50)))
        sleep(.15)
        display.update(draw_opp_pkmn_sprite(defender))
        sleep(.15)
        display.update(SCREEN.blit(big,(800,280)))
        sleep(.15)
        display.update(draw_opp_pkmn_sprite(defender))
        display.update(SCREEN.blit(big,(900,280)))
        sleep(.15)
        display.update(draw_opp_pkmn_sprite(defender))
        display.update(SCREEN.blit(big,(1000,280)))
        sleep(.15)
        display.update(draw_opp_pkmn_sprite(defender))
        display.update(SCREEN.blit(big,(800,168)))
        display.update(SCREEN.blit(big,(800,280)))
        sleep(.15)
        display.update(draw_opp_pkmn_sprite(defender))
        display.update(SCREEN.blit(big,(900,168)))
        display.update(SCREEN.blit(big,(900,280)))
        sleep(.15)
        display.update(draw_opp_pkmn_sprite(defender))
        display.update(SCREEN.blit(big,(1000,168)))
        display.update(SCREEN.blit(big,(1000,280)))
        sleep(.15)
        display.update(draw_opp_pkmn_sprite(defender))

    else:
        display.update(SCREEN.blit(big,(830,200)))
        sleep(.15)
        display.update(SCREEN.blit(big,(680,275)))
        sleep(.15)
        display.update(SCREEN.blit(big,(530,350)))
        sleep(.15)
        display.update(SCREEN.blit(big,(380,425)))
        sleep(.15)
        display.update(SCREEN.blit(big,(230,500)))
        sleep(.15)
        display.update(SCREEN.blit(orig,(0,0)))
        display.update(SCREEN.blit(smallblast, (150,350)))
        sleep(.15)
        display.update(SCREEN.blit(bigblast, (150,350)))
        sleep(.15)
        display.update(draw_my_pkmn_sprite(defender))
        sleep(.1)
        display.update(SCREEN.blit(smallblast, (150,350)))
        sleep(.15)
        display.update(SCREEN.blit(bigblast, (150,350)))
        sleep(.15)
        display.update(draw_my_pkmn_sprite(defender))
        sleep(.15)
        display.update(SCREEN.blit(big,(100,568)))
        sleep(.15)
        display.update(draw_my_pkmn_sprite(defender))
        display.update(SCREEN.blit(big,(200,568)))
        sleep(.15)
        display.update(draw_my_pkmn_sprite(defender))
        display.update(SCREEN.blit(big,(300,568)))
        sleep(.15)
        display.update(draw_my_pkmn_sprite(defender))
        display.update(SCREEN.blit(big,(100,456)))
        display.update(SCREEN.blit(big,(100,568)))
        sleep(.15)
        display.update(draw_my_pkmn_sprite(defender))
        display.update(SCREEN.blit(big,(200,456)))
        display.update(SCREEN.blit(big,(200,568)))
        sleep(.15)
        display.update(draw_my_pkmn_sprite(defender))
        display.update(SCREEN.blit(big,(300,456)))
        display.update(SCREEN.blit(big,(300,568)))
        sleep(.15)
        display.update(draw_my_pkmn_sprite(defender))
    dmged()
    s.stop()


def do_fire_punch(attacker, defender, attacking):
    s = Sound("sounds/Fire Punch.ogg")
    s.play()
    small = loadalphaimg('moves/smallfire.png')
    big = loadalphaimg('moves/bigfire.png')
    s.play()
    if attacking:
        med_3(attacker,defender)
        display.update(SCREEN.blit(small,(800,280)))
        sleep(.2)
        display.update(draw_opp_pkmn_sprite(defender))
        display.update(SCREEN.blit(big,(800,280)))
        sleep(.2)
        display.update(draw_opp_pkmn_sprite(defender))
        display.update(SCREEN.blit(small,(1000,280)))
        sleep(.2)
        display.update(draw_opp_pkmn_sprite(defender))
        display.update(SCREEN.blit(big,(1000,280)))
        sleep(.2)
        display.update(draw_opp_pkmn_sprite(defender))
        display.update(SCREEN.blit(small,(900,280)))
        sleep(.2)
        display.update(draw_opp_pkmn_sprite(defender))
        display.update(SCREEN.blit(big,(900,280)))
        sleep(.2)
        display.update(draw_opp_pkmn_sprite(defender))
    else:
        opp_med_3(attacker,defender)
        display.update(SCREEN.blit(small,(100,568)))
        sleep(.2)
        display.update(draw_my_pkmn_sprite(defender))
        display.update(SCREEN.blit(big,(100,568)))
        sleep(.2)
        display.update(draw_my_pkmn_sprite(defender))
        display.update(SCREEN.blit(small,(300,568)))
        sleep(.2)
        display.update(draw_my_pkmn_sprite(defender))
        display.update(SCREEN.blit(big,(300,568)))
        sleep(.2)
        display.update(draw_my_pkmn_sprite(defender))
        display.update(SCREEN.blit(small,(200,568)))
        sleep(.2)
        display.update(draw_my_pkmn_sprite(defender))
        display.update(SCREEN.blit(big,(200,568)))
        sleep(.2)
        display.update(draw_my_pkmn_sprite(defender))
    dmged()


def do_fire_spin(attacker, defender, attacking):
    s = Sound("sounds/Fire Spin.ogg")
    s.play()
    big = loadalphaimg('moves/bigfire.png')
    smallblast = loadalphaimg('moves/smallblast.png')
    bigblast = loadalphaimg('moves/bigblast.png')

    if attacking:
        display.update(SCREEN.blit(big,(800,280)))
        sleep(.2)
        display.update(draw_opp_pkmn_sprite(defender))
        display.update(SCREEN.blit(big,(900,280)))
        sleep(.2)
        display.update(draw_opp_pkmn_sprite(defender))
        display.update(SCREEN.blit(big,(1000,280)))
        sleep(.2)
        display.update(draw_opp_pkmn_sprite(defender))
        display.update(SCREEN.blit(big,(800,168)))
        display.update(SCREEN.blit(big,(800,280)))
        sleep(.2)
        display.update(draw_opp_pkmn_sprite(defender))
        display.update(SCREEN.blit(big,(900,168)))
        display.update(SCREEN.blit(big,(900,280)))
        sleep(.2)
        display.update(draw_opp_pkmn_sprite(defender))
        display.update(SCREEN.blit(big,(1000,168)))
        display.update(SCREEN.blit(big,(1000,280)))
        sleep(.2)
        display.update(draw_opp_pkmn_sprite(defender))
        display.update(SCREEN.blit(big,(800,56)))
        display.update(SCREEN.blit(big,(800,168)))
        display.update(SCREEN.blit(big,(800,280)))
        sleep(.2)
        display.update(draw_opp_pkmn_sprite(defender))
        display.update(SCREEN.blit(big,(900,56)))
        display.update(SCREEN.blit(big,(900,168)))
        display.update(SCREEN.blit(big,(900,280)))
        sleep(.2)
        display.update(draw_opp_pkmn_sprite(defender))
        display.update(SCREEN.blit(big,(1000,56)))
        display.update(SCREEN.blit(big,(1000,168)))
        display.update(SCREEN.blit(big,(1000,280)))
        sleep(.2)
        display.update(draw_opp_pkmn_sprite(defender))

    else:
        display.update(SCREEN.blit(big,(100,568)))
        sleep(.2)
        display.update(draw_my_pkmn_sprite(defender))
        display.update(SCREEN.blit(big,(200,568)))
        sleep(.2)
        display.update(draw_my_pkmn_sprite(defender))
        display.update(SCREEN.blit(big,(300,568)))
        sleep(.2)
        display.update(draw_my_pkmn_sprite(defender))
        display.update(SCREEN.blit(big,(100,456)))
        display.update(SCREEN.blit(big,(100,568)))
        sleep(.2)
        display.update(draw_my_pkmn_sprite(defender))
        display.update(SCREEN.blit(big,(200,456)))
        display.update(SCREEN.blit(big,(200,568)))
        sleep(.2)
        display.update(draw_my_pkmn_sprite(defender))
        display.update(SCREEN.blit(big,(300,456)))
        display.update(SCREEN.blit(big,(300,568)))
        sleep(.2)
        display.update(draw_my_pkmn_sprite(defender))
        display.update(SCREEN.blit(big,(100,344)))
        display.update(SCREEN.blit(big,(100,456)))
        display.update(SCREEN.blit(big,(100,568)))
        sleep(.2)
        display.update(draw_my_pkmn_sprite(defender))
        display.update(SCREEN.blit(big,(200,344)))
        display.update(SCREEN.blit(big,(200,456)))
        display.update(SCREEN.blit(big,(200,568)))
        sleep(.2)
        display.update(draw_my_pkmn_sprite(defender))
        display.update(SCREEN.blit(big,(300,344)))
        display.update(SCREEN.blit(big,(300,456)))
        display.update(SCREEN.blit(big,(300,568)))
        sleep(.2)
        display.update(draw_my_pkmn_sprite(defender))
    dmged()
    s.stop()


def do_fissure(attacker, defender, attacking):
    s = Sound("sounds/Fissure.ogg")
    orig = SCREEN.copy()
    s.play()
    dmged()
    dmged()
    SCREEN.fill(BLACK)
    display.flip()
    sleep(.2)
    display.update(SCREEN.blit(orig,(0,0)))
    dmged()
    dmged()
    s.stop()


def do_flamethrower(attacker, defender, attacking):
    s = Sound("sounds/Flamethrower.ogg")
    orig = SCREEN.copy()
    s.play()
    big = loadalphaimg('moves/bigfire.png')
    if attacking:
        display.update(SCREEN.blit(big,(230,500)))
        sleep(.15)
        display.update(SCREEN.blit(big,(380,425)))
        sleep(.15)
        display.update(SCREEN.blit(big,(530,350)))
        sleep(.15)
        display.update(SCREEN.blit(big,(680,275)))
        sleep(.15)
        display.update(SCREEN.blit(big,(830,200)))
        sleep(.15)
        display.update(SCREEN.blit(orig,(0,0)))
        sleep(.15)
        display.update(SCREEN.blit(big,(900,280)))
        sleep(.15)
        display.update(draw_opp_pkmn_sprite(defender))
        display.update(SCREEN.blit(big,(1000,280)))
        sleep(.15)
        display.update(draw_opp_pkmn_sprite(defender))
        display.update(SCREEN.blit(big,(800,168)))
        display.update(SCREEN.blit(big,(800,280)))
        sleep(.15)
        display.update(draw_opp_pkmn_sprite(defender))
        display.update(SCREEN.blit(big,(900,168)))
        display.update(SCREEN.blit(big,(900,280)))
        sleep(.15)
        display.update(draw_opp_pkmn_sprite(defender))
        display.update(SCREEN.blit(big,(1000,168)))
        display.update(SCREEN.blit(big,(1000,280)))
        sleep(.15)
        display.update(draw_opp_pkmn_sprite(defender))

    else:
        display.update(SCREEN.blit(big,(830,200)))
        sleep(.15)
        display.update(SCREEN.blit(big,(680,275)))
        sleep(.15)
        display.update(SCREEN.blit(big,(530,350)))
        sleep(.15)
        display.update(SCREEN.blit(big,(380,425)))
        sleep(.15)
        display.update(SCREEN.blit(big,(230,500)))
        sleep(.15)
        display.update(SCREEN.blit(orig,(0,0)))
        sleep(.15)
        display.update(draw_my_pkmn_sprite(defender))
        sleep(.15)
        display.update(SCREEN.blit(big,(100,568)))
        sleep(.15)
        display.update(draw_my_pkmn_sprite(defender))
        display.update(SCREEN.blit(big,(200,568)))
        sleep(.15)
        display.update(draw_my_pkmn_sprite(defender))
        display.update(SCREEN.blit(big,(300,568)))
        sleep(.15)
        display.update(draw_my_pkmn_sprite(defender))
        display.update(SCREEN.blit(big,(100,456)))
        display.update(SCREEN.blit(big,(100,568)))
        sleep(.15)
        display.update(draw_my_pkmn_sprite(defender))
        display.update(SCREEN.blit(big,(200,456)))
        display.update(SCREEN.blit(big,(200,568)))
        sleep(.15)
        display.update(draw_my_pkmn_sprite(defender))
        display.update(SCREEN.blit(big,(300,456)))
        display.update(SCREEN.blit(big,(300,568)))
        sleep(.15)
        display.update(draw_my_pkmn_sprite(defender))
    dmged()
    s.stop()


def do_flash(attacker, defender, attacking):
    s = Sound("sounds/Flash.ogg")
    s.play()
    orig = SCREEN.copy()
    SCREEN.fill(BLACK)
    display.flip()
    sleep(.2)
    display.update(SCREEN.blit(orig,(0,0)))
    sleep(.2)
    SCREEN.fill(BLACK)
    display.flip()
    sleep(.2)
    display.update(SCREEN.blit(orig,(0,0)))
    sleep(.2)
    SCREEN.fill(BLACK)
    display.flip()
    sleep(.2)
    display.update(SCREEN.blit(orig,(0,0)))
    s.stop()


def do_fly(attacker, defender, attacking):
    s = Sound("sounds/Fly.ogg")
    s.play()
    if attacking:
        draw_my_pkmn_sprite(attacker)
        med_3(attacker,defender)
    else:
        draw_opp_pkmn_sprite(attacker)
        opp_med_3(attacker,defender)
    dmged()
    s.stop()


def do_fly_prep(attacker, defender, attacking):
    s = Sound("sounds/Fly_prep.ogg")
    s.play()
    if attacking:
        display.update(draw.rect(SCREEN, WHITE, MYPKMN + [attacker.backimg.get_width(),attacker.backimg.get_width()]))
    else:
        display.update(draw.rect(SCREEN, WHITE, OPPPKMN + [attacker.backimg.get_width(),attacker.backimg.get_width()]))
    s.stop()


def do_focus_energy(attacker, defender, attacking):
    s = Sound("sounds/Focus Energy.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_fury_attack(attacker, defender, attacking):
    s = Sound("sounds/Fury Attack.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_fury_swipes(attacker, defender, attacking):
    s = Sound("sounds/Fury Swipes.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_glare(attacker, defender, attacking):
    s = Sound("sounds/Glare.ogg")
    s.play()
    orig = SCREEN.copy()
    SCREEN.fill(BLACK)
    display.flip()
    sleep(.2)
    display.update(SCREEN.blit(orig,(0,0)))
    sleep(.2)
    SCREEN.fill(BLACK)
    display.flip()
    sleep(.2)
    display.update(SCREEN.blit(orig,(0,0)))
    s.stop()


def do_growl(attacker, defender, attacking):
    #s = Sound('sounds/crys/' + attacker.base.name + '.ogg')
    #s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    #s.stop()


def do_growth(attacker, defender, attacking):
    s = Sound("sounds/Growth.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_guillotine(attacker, defender, attacking):
    s = Sound("sounds/Guillotine.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_gust(attacker, defender, attacking):
    s = Sound("sounds/Gust.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_harden(attacker, defender, attacking):
    s = Sound("sounds/Harden.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_haze(attacker, defender, attacking):
    s = Sound("sounds/Haze.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_headbutt(attacker, defender, attacking):
    s = Sound("sounds/HeadButt.ogg")
    s.play()
    if attacking:
        display.update(mid_big())
        sleep(.15)
        display.update(draw_opp_pkmn_sprite(defender))
    else:
        display.update(opp_mid_big())
        sleep(.15)
        display.update(draw_my_pkmn_sprite(defender))
    dmged()
    s.stop()


def do_hi_jump_kick(attacker, defender, attacking):
    s = Sound("sounds/Hi Jump Kick.ogg")
    s.play()
    if attacking:
        big_3(attacker, defender)
    else:
        opp_big_3(attacker, defender)
    dmged()
    s.stop()


def do_horn_attack(attacker, defender, attacking):
    s = Sound("sounds/Horn Attack.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_horn_drill(attacker, defender, attacking):
    s = Sound("sounds/Horn Drill.ogg")
    s.play()
    if attacking:
        display.update(mid_big())
        sleep(.1)
        display.update(draw_opp_pkmn_sprite(defender))
        sleep(.1)
        display.update(mid_big())
        sleep(.1)
        display.update(draw_opp_pkmn_sprite(defender))
        sleep(.1)
        display.update(mid_big())
        sleep(.1)
        display.update(draw_opp_pkmn_sprite(defender))
        sleep(.1)
        display.update(mid_big())
        sleep(.1)
        display.update(draw_opp_pkmn_sprite(defender))
    else:
        display.update(opp_mid_big())
        sleep(.1)
        display.update(draw_my_pkmn_sprite(defender))
        sleep(.1)
        display.update(opp_mid_big())
        sleep(.1)
        display.update(draw_my_pkmn_sprite(defender))
        sleep(.1)
        display.update(opp_mid_big())
        sleep(.1)
        display.update(draw_my_pkmn_sprite(defender))
        sleep(.1)
        display.update(opp_mid_big())
        sleep(.1)
        display.update(draw_my_pkmn_sprite(defender))
    dmged()
    s.stop()


def do_hydro_pump(attacker, defender, attacking):
    s = Sound("sounds/Hydro Pump.ogg")
    pumps = []
    for i in range(1,7):
        pumps.append(loadalphaimg('moves/hydro{0}.png'.format(i)))
    s.play()
    if attacking:
        for i in range(6):
            display.update(SCREEN.blit(pumps[i],(820,75)))
            sleep(.15)
            display.update(draw_opp_pkmn_sprite(defender))
        for i in range(6):
            display.update(SCREEN.blit(pumps[i],(940,75)))
            sleep(.15)
            display.update(draw_opp_pkmn_sprite(defender))
        sleep(.3)
        for i in range(6):
            display.update(SCREEN.blit(pumps[i],(820,75)))
            sleep(.15)
            display.update(draw_opp_pkmn_sprite(defender))
        for i in range(6):
            display.update(SCREEN.blit(pumps[i],(940,75)))
            sleep(.15)
            display.update(draw_opp_pkmn_sprite(defender))
    else:
        for i in range(6):
            display.update(SCREEN.blit(pumps[i],(150,365)))
            sleep(.15)
            display.update(draw_my_pkmn_sprite(defender))
        for i in range(6):
            display.update(SCREEN.blit(pumps[i],(270,365)))
            sleep(.15)
            display.update(draw_my_pkmn_sprite(defender))
        sleep(.3)
        for i in range(6):
            display.update(SCREEN.blit(pumps[i],(150,365)))
            sleep(.15)
            display.update(draw_my_pkmn_sprite(defender))
        for i in range(6):
            display.update(SCREEN.blit(pumps[i],(270,365)))
            sleep(.15)
            display.update(draw_my_pkmn_sprite(defender))
    dmged()
    s.stop()


def do_hyper_beam(attacker, defender, attacking):
    s = Sound("sounds/Hyper Beam.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_hyper_fang(attacker, defender, attacking):
    s = Sound("sounds/Hyper Fang.ogg")
    s.play()
    if attacking:
        med_3(attacker, defender)
    else:
        opp_med_3(attacker, defender)
    s.stop()


def do_hypnosis(attacker, defender, attacking):
    s = Sound("sounds/Hypnosis.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_ice_beam(attacker, defender, attacking):
    s = Sound("sounds/Ice Beam.ogg")
    ice = []
    for i in range(1,5):
        ice.append(loadalphaimg('moves/ice{0}.png'.format(i)))
    s.play()
    if attacking:
        beam(attacker, defender, attacking, type_='ice')
        for i in range(4):
            display.update(SCREEN.blit(ice[i],(780,150)))
            sleep(.15)
            display.update(draw_opp_pkmn_sprite(defender))
    else:
        beam(attacker, defender, attacking, type_='ice')
        for i in range(4):
            display.update(SCREEN.blit(ice[i],(59,456)))
            sleep(.15)
            display.update(draw_my_pkmn_sprite(defender))
    dmged()
    s.stop()


def do_ice_punch(attacker, defender, attacking):
    s = Sound("sounds/Ice Punch.ogg")
    ice = []
    for i in range(1,5):
        ice.append(loadalphaimg('moves/ice{0}.png'.format(i)))
    s.play()
    if attacking:
        med_3(attacker, defender)
        for i in range(4):
            display.update(SCREEN.blit(ice[i],(780,150)))
            sleep(.15)
            display.update(draw_opp_pkmn_sprite(defender))
    else:
        opp_med_3(attacker, defender)
        for i in range(4):
            display.update(SCREEN.blit(ice[i],(59,456)))
            sleep(.15)
            display.update(draw_my_pkmn_sprite(defender))
    dmged()
    s.stop()


def do_jump_kick(attacker, defender, attacking):
    s = Sound("sounds/Jump Kick.ogg")
    s.play()
    if attacking:
        big_3(attacker, defender)
    else:
        opp_big_3(attacker, defender)
    dmged()
    s.stop()


def do_karate_chop(attacker, defender, attacking):
    s = Sound("sounds/Karate Chop.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_kinesis(attacker, defender, attacking):
    s = Sound("sounds/Kinesis.ogg")
    s.play()
    if attacking:
        double(attacker, defender)
    else:
        opp_double(attacker, defender)
    s.stop()


def do_leech_life(attacker, defender, attacking):
    s = Sound("sounds/Leach Kiss.ogg")
    s.play()
    if attacking:
        med_3(attacker, defender)
    else:
        opp_med_3(attacker, defender)
    dmged()
    s.stop()


def do_leech_seed(attacker, defender, attacking):
    s = Sound("sounds/Leach Seed.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_leer(attacker, defender, attacking):
    s = Sound("sounds/Leer.ogg")
    orig = SCREEN.copy()
    s.play()
    SCREEN.fill(BLACK)
    display.flip()
    sleep(.15)
    SCREEN.blit(orig,(0,0))
    sleep(.15)
    dmged()
    s.stop()


def do_lick(attacker, defender, attacking):
    s = Sound("sounds/Lick.ogg")
    tmp = loadalphaimg('moves/acid.png')
    drop = loadalphaimg('moves/drop.png')
    s.play()
    if attacking:
        display.update(SCREEN.blit(tmp,LOW_ARC[-1]))
        display.update(SCREEN.blit(drop, (900,220)))
        draw_opp_pkmn_sprite(defender)
        sleep(.15)
        display.update([900,220, drop.get_width(), drop.get_height()])
        display.update(SCREEN.blit(drop, (900,270)))
        draw_opp_pkmn_sprite(defender)
        sleep(.15)
        display.update([900,270, drop.get_width(), drop.get_height()])

        display.update(SCREEN.blit(drop, (900,320)))
        draw_opp_pkmn_sprite(defender)
        sleep(.15)
        display.update([900,320, drop.get_width(), drop.get_height()])
        display.update(SCREEN.blit(drop, (950,220)))
        draw_opp_pkmn_sprite(defender)
        sleep(.15)
        display.update([950,220, drop.get_width(), drop.get_height()])
        display.update(SCREEN.blit(drop, (950,270)))
        draw_opp_pkmn_sprite(defender)
        sleep(.15)
        display.update([950,270, drop.get_width(), drop.get_height()])
        display.update(SCREEN.blit(drop, (950,320)))
        sleep(.15)
        display.update(draw_opp_pkmn_sprite(defender))
    else:
        display.update(SCREEN.blit(tmp,(200,400)))
        display.update(SCREEN.blit(drop, (220,510)))
        draw_my_pkmn_sprite(defender)
        sleep(.15)
        display.update([220,510, drop.get_width(), drop.get_height()])
        display.update(SCREEN.blit(drop, (220,560)))
        draw_my_pkmn_sprite(defender)
        sleep(.15)
        display.update([220,560, drop.get_width(), drop.get_height()])

        display.update(SCREEN.blit(drop, (220,610)))
        draw_my_pkmn_sprite(defender)
        sleep(.15)
        display.update([220,610, drop.get_width(), drop.get_height()])
        display.update(SCREEN.blit(drop, (270,510)))
        draw_my_pkmn_sprite(defender)
        sleep(.15)
        display.update([270,510, drop.get_width(), drop.get_height()])
        display.update(SCREEN.blit(drop, (270,560)))
        draw_my_pkmn_sprite(defender)
        sleep(.15)
        display.update([270,560, drop.get_width(), drop.get_height()])
        display.update(SCREEN.blit(drop, (270,610)))
        sleep(.15)
        display.update(draw_my_pkmn_sprite(defender))
    dmged()
    s.stop()


def do_light_screen(attacker, defender, attacking):
    s = Sound("sounds/Light Screen.ogg")
    s.play()
    if attacking:
        tmp = loadalphaimg('moves/screen.png')
    else:
        tmp = loadalphaimg('moves/opp_screen.png')
    if attacking:
        display.update(SCREEN.blit(tmp,(470,285)))
        sleep(.15)
        draw.rect(SCREEN, WHITE, (470,285, tmp.get_width(), tmp.get_height()))
        draw_my_pkmn_sprite(attacker)
        display.update([470,285, tmp.get_width(), tmp.get_height()])
        sleep(.15)
        display.update(SCREEN.blit(tmp,(470,285)))
        sleep(.15)
        draw.rect(SCREEN, WHITE, (470,285, tmp.get_width(), tmp.get_height()))
        draw_my_pkmn_sprite(attacker)
        display.update([470,285, tmp.get_width(), tmp.get_height()])
        sleep(.15)
        display.update(SCREEN.blit(tmp,(470,285)))
        sleep(.15)
        draw.rect(SCREEN, WHITE, (470,285, tmp.get_width(), tmp.get_height()))
        draw_my_pkmn_sprite(attacker)
        display.update([470,285, tmp.get_width(), tmp.get_height()])
        sleep(.15)
        display.update(SCREEN.blit(tmp,(470,285)))
        sleep(.15)
        draw.rect(SCREEN, WHITE, (470,285, tmp.get_width(), tmp.get_height()))
        draw_my_pkmn_sprite(attacker)
        display.update([470,285, tmp.get_width(), tmp.get_height()])
        sleep(.15)
        display.update(SCREEN.blit(tmp,(470,285)))
        sleep(.15)
        draw.rect(SCREEN, WHITE, (470,285, tmp.get_width(), tmp.get_height()))
        draw_my_pkmn_sprite(attacker)
        display.update([470,285, tmp.get_width(), tmp.get_height()])
        sleep(.15)
        display.update(SCREEN.blit(tmp,(470,285)))
        sleep(.15)
        draw.rect(SCREEN, WHITE, (470,285, tmp.get_width(), tmp.get_height()))
        draw_my_pkmn_sprite(attacker)
        display.update([470,285, tmp.get_width(), tmp.get_height()])
        sleep(.15)
    else:

        display.update(SCREEN.blit(tmp,(700,0)))
        sleep(.15)
        draw.rect(SCREEN, WHITE, (700,0, tmp.get_width(), tmp.get_height()))
        draw_my_pkmn_sprite(attacker)
        display.update([700,0, tmp.get_width(), tmp.get_height()])
        sleep(.15)
        display.update(SCREEN.blit(tmp,(700,0)))
        sleep(.15)
        draw.rect(SCREEN, WHITE, (700,0, tmp.get_width(), tmp.get_height()))
        draw_my_pkmn_sprite(attacker)
        display.update([700,0, tmp.get_width(), tmp.get_height()])
        sleep(.15)
        display.update(SCREEN.blit(tmp,(700,0)))
        sleep(.15)
        draw.rect(SCREEN, WHITE, (700,0, tmp.get_width(), tmp.get_height()))
        draw_my_pkmn_sprite(attacker)
        display.update([700,0, tmp.get_width(), tmp.get_height()])
        sleep(.15)
        display.update(SCREEN.blit(tmp,(700,0)))
        sleep(.15)
        draw.rect(SCREEN, WHITE, (700,0, tmp.get_width(), tmp.get_height()))
        draw_my_pkmn_sprite(attacker)
        display.update([700,0, tmp.get_width(), tmp.get_height()])
        sleep(.15)
        display.update(SCREEN.blit(tmp,(700,0)))
        sleep(.15)
        draw.rect(SCREEN, WHITE, (700,0, tmp.get_width(), tmp.get_height()))
        draw_my_pkmn_sprite(attacker)
        display.update([700,0, tmp.get_width(), tmp.get_height()])
        sleep(.15)
        display.update(SCREEN.blit(tmp,(700,0)))
        sleep(.15)
        draw.rect(SCREEN, WHITE, (700,0, tmp.get_width(), tmp.get_height()))
        draw_my_pkmn_sprite(attacker)
        display.update([700,0, tmp.get_width(), tmp.get_height()])
        sleep(.15)
    s.stop()


def do_lovely_kiss(attacker, defender, attacking):
    s = Sound("sounds/Lovely Kiss.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_low_kick(attacker, defender, attacking):
    s = Sound("sounds/Low Kick.ogg")
    s.play()
    if attacking:
        big_3(attacker, defender)
    else:
        opp_big_3(attacker, defender)
    dmged()


def do_meditate(attacker, defender, attacking):
    s = Sound("sounds/Meditate.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_mega_drain(attacker, defender, attacking):
    s = Sound("sounds/Meaga Drain.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_mega_kick(attacker, defender, attacking):
    s = Sound("sounds/Mega Kick.ogg")
    s.play()
    if attacking:
        big_3(attacker, defender)
    else:
        opp_big_3(attacker, defender)
    s.stop()


def do_mega_punch(attacker, defender, attacking):
    s = Sound("sounds/Mega Punch.ogg")
    s.play()
    if attacking:
        big_3(attacker, defender)
    else:
        opp_big_3(attacker, defender)
    s.stop()


def do_metronome(attacker, defender, attacking):
    s = Sound("sounds/Metronome.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_mimic(attacker, defender, attacking):
    s = Sound("sounds/Mimic.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_minimize(attacker, defender, attacking):
    s = Sound("sounds/Minimize.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_mist(attacker, defender, attacking):
    s = Sound("sounds/Mist.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_night_shade(attacker, defender, attacking):
    s = Sound("sounds/Night Shade.ogg")
    s.play()
    invert()
    sleep(.1)
    invert()
    sleep(.1)
    invert()
    sleep(.1)
    invert()
    sleep(.1)
    wave(10)
    dmged()
    s.stop()


def do_pay_day(attacker, defender, attacking):
    s = Sound("sounds/Pay Day.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_peck(attacker, defender, attacking):
    s = Sound("sounds/Peck.ogg")
    s.play()
    if attacking:
        double(attacker, defender)
    else:
        opp_double(attacker, defender)
    s.stop()


def do_petal_dance(attacker, defender, attacking):
    s = Sound("sounds/Petal Dance.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_pin_missile(attacker, defender, attacking):
    s = Sound("sounds/Pin Missle.ogg")
    s.play()
    if attacking:
        double(attacker, defender)
    else:
        opp_double(attacker, defender)
    s.stop()


def do_poison_gas(attacker, defender, attacking):
    s = Sound("sounds/Posion Gas.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_poison_sting(attacker, defender, attacking):
    s = Sound("sounds/Poision Sting.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_poisonpowder(attacker, defender, attacking):
    s = Sound("sounds/Poison Powder.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_pound(attacker, defender, attacking):
    s = Sound("sounds/Pound.ogg")
    s.play()
    if attacking:
        double(attacker, defender)
    else:
        opp_double(attacker, defender)
    s.stop()


def do_psybeam(attacker, defender, attacking):
    s = Sound("sounds/Psybeam.ogg")
    s.play()
    if attacking:
        beam(attacker, defender, attacking, type_='psy')
    else:
        beam(attacker, defender, attacking, type_='psy')
    invert()
    sleep(.15)
    invert()
    dmged()
    s.stop()


def do_psychic(attacker, defender, attacking):
    s = Sound("sounds/Psychic.ogg")
    s.play()
    invert()
    sleep(.15)
    invert()
    sleep(.15)
    invert()
    sleep(.15)
    invert()
    sleep(.15)
    invert()
    sleep(.15)
    invert()
    sleep(.15)
    wave(10)
    dmged()
    s.stop()


def do_psywave(attacker, defender, attacking):
    s = Sound("sounds/Psywave.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_quick_attack(attacker, defender, attacking):
    s = Sound("sounds/Quick Attack.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_rage(attacker, defender, attacking):
    s = Sound("sounds/Rage.ogg")
    s.play()
    if attacking:
        double(attacker, defender)
    else:
        opp_double(attacker, defender)
    dmged()
    s.stop()


def do_razor_leaf(attacker, defender, attacking):
    s = Sound("sounds/Razor Leaf.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_razor_wind_prep(attacker, defender, attacking):
    #TODO NO SOUND?
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending


def do_razor_wind(attacker, defender, attacking):
    s = Sound("sounds/Razor Wind.mp")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_recover(attacker, defender, attacking):
    s = Sound("sounds/Recover.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_reflect(attacker, defender, attacking):
    s = Sound("sounds/Reflect.ogg")
    if attacking:
        tmp = loadalphaimg('moves/barrier.png')
    else:
        tmp = loadalphaimg('moves/opp_barrier.png')
    s.play()
    invert()
    if attacking:
        invert()
        display.update(SCREEN.blit(tmp,(470,285)))
        invert()
        sleep(.15)
        invert()
        draw.rect(SCREEN, WHITE, (470,285, tmp.get_width(), tmp.get_height()))
        draw_my_pkmn_sprite(attacker)
        display.update([470,285, tmp.get_width(), tmp.get_height()])
        invert()
        sleep(.15)
        invert()
        display.update(SCREEN.blit(tmp,(470,285)))
        invert()
        sleep(.15)
        invert()
        draw.rect(SCREEN, WHITE, (470,285, tmp.get_width(), tmp.get_height()))
        draw_my_pkmn_sprite(attacker)
        display.update([470,285, tmp.get_width(), tmp.get_height()])
        invert()
        sleep(.15)
        invert()
        display.update(SCREEN.blit(tmp,(470,285)))
        invert()
        sleep(.15)
        invert()
        draw.rect(SCREEN, WHITE, (470,285, tmp.get_width(), tmp.get_height()))
        draw_my_pkmn_sprite(attacker)
        display.update([470,285, tmp.get_width(), tmp.get_height()])
        invert()
        sleep(.15)
        invert()
        display.update(SCREEN.blit(tmp,(470,285)))
        invert()
        sleep(.15)
        invert()
        draw.rect(SCREEN, WHITE, (470,285, tmp.get_width(), tmp.get_height()))
        draw_my_pkmn_sprite(attacker)
        display.update([470,285, tmp.get_width(), tmp.get_height()])
        invert()
        sleep(.15)
        invert()
        display.update(SCREEN.blit(tmp,(470,285)))
        invert()
        sleep(.15)
        invert()
        draw.rect(SCREEN, WHITE, (470,285, tmp.get_width(), tmp.get_height()))
        draw_my_pkmn_sprite(attacker)
        display.update([470,285, tmp.get_width(), tmp.get_height()])
        invert()
        sleep(.15)
        invert()
        display.update(SCREEN.blit(tmp,(470,285)))
        invert()
        sleep(.15)
        invert()
        draw.rect(SCREEN, WHITE, (470,285, tmp.get_width(), tmp.get_height()))
        draw_my_pkmn_sprite(attacker)
        display.update([470,285, tmp.get_width(), tmp.get_height()])
        invert()
        sleep(.15)
    else:
        invert()
        display.update(SCREEN.blit(tmp,(700,0)))
        invert()
        sleep(.15)
        invert()
        draw.rect(SCREEN, WHITE, (700,0, tmp.get_width(), tmp.get_height()))
        draw_opp_pkmn_sprite(attacker)
        display.update([700,0, tmp.get_width(), tmp.get_height()])
        invert()
        sleep(.15)
        invert()
        display.update(SCREEN.blit(tmp,(700,0)))
        invert()
        sleep(.15)
        invert()
        draw.rect(SCREEN, WHITE, (700,0, tmp.get_width(), tmp.get_height()))
        draw_opp_pkmn_sprite(attacker)
        display.update([700,0, tmp.get_width(), tmp.get_height()])
        invert()
        sleep(.15)
        invert()
        display.update(SCREEN.blit(tmp,(700,0)))
        invert()
        sleep(.15)
        invert()
        draw.rect(SCREEN, WHITE, (700,0, tmp.get_width(), tmp.get_height()))
        draw_opp_pkmn_sprite(attacker)
        display.update([700,0, tmp.get_width(), tmp.get_height()])
        invert()
        sleep(.15)
        invert()
        display.update(SCREEN.blit(tmp,(700,0)))
        invert()
        sleep(.15)
        invert()
        draw.rect(SCREEN, WHITE, (700,0, tmp.get_width(), tmp.get_height()))
        draw_opp_pkmn_sprite(attacker)
        display.update([700,0, tmp.get_width(), tmp.get_height()])
        invert()
        sleep(.15)
        invert()
        display.update(SCREEN.blit(tmp,(700,0)))
        invert()
        sleep(.15)
        invert()
        draw.rect(SCREEN, WHITE, (700,0, tmp.get_width(), tmp.get_height()))
        draw_opp_pkmn_sprite(attacker)
        display.update([700,0, tmp.get_width(), tmp.get_height()])
        invert()
        sleep(.15)
        invert()
        display.update(SCREEN.blit(tmp,(700,0)))
        invert()
        sleep(.15)
        invert()
        draw.rect(SCREEN, WHITE, (700,0, tmp.get_width(), tmp.get_height()))
        draw_opp_pkmn_sprite(attacker)
        display.update([700,0, tmp.get_width(), tmp.get_height()])
        invert()
        sleep(.15)
    invert()
    s.stop()


def do_rest(attacker, defender, attacking):
    s = Sound("sounds/Rest.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_roar(attacker, defender, attacking):
    #s = Sound('sounds/crys/' + attacker.base.name + '.ogg')
    #s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    #s.stop()


def do_rock_slide(attacker, defender, attacking):
    s = Sound("sounds/Rock Slide.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_rock_throw(attacker, defender, attacking):
    s = Sound("sounds/Rock Throw.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_rolling_kick(attacker, defender, attacking):
    s = Sound("sounds/Rolling Kick.ogg")
    s.play()
    if attacking:
        big_3(attacker, defender)
    else:
        opp_big_3(attacker, defender)
    s.stop()


def do_sand_attack(attacker, defender, attacking):
    s = Sound("sounds/Sand Attack.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_scratch(attacker, defender, attacking):
    s = Sound("sounds/Scratch.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_screech(attacker, defender, attacking):
    s = Sound("sounds/Screech.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_seismic_toss(attacker, defender, attacking):
    s = Sound("sounds/Seismic Toss.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_selfdestruct(attacker, defender, attacking):
    s = Sound("sounds/Selfdestruct.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_sharpen(attacker, defender, attacking):
    s = Sound("sounds/Sharpen.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_sing(attacker, defender, attacking):
    s = Sound("sounds/Sing.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_skull_bash(attacker, defender, attacking):
    s = Sound("sounds/Skull Bash.ogg")
    s.play()
    if attacking:
        display.update(mid_big())
        sleep(.15)
        display.update(draw_opp_pkmn_sprite(defender))
    else:
        display.update(opp_mid_big())
        sleep(.15)
        display.update(draw_my_pkmn_sprite(defender))
    s.stop()


def do_skull_bash_prep(attacker, defender, attacking):
    #TODO NO SOUND?
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending


def do_sky_attack(attacker, defender, attacking):
    s = Sound("sounds/Sky Attack.ogg")
    s.play()
    if attacking:
        big_3(attacker, defender)
    else:
        opp_big_3(attacker, defender)
    dmged()
    s.stop()


def do_sky_attack_prep(attacker, defender, attacking):
    #TODO NO SOUND?
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending


def do_slam(attacker, defender, attacking):
    s = Sound("sounds/Slam.ogg")
    s.play()
    if attacking:
        med_3(attacker, defender)
    else:
        opp_med_3(attacker, defender)
    s.stop()


def do_slash(attacker, defender, attacking):
    s = Sound("sounds/Slash.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_sleep_powder(attacker, defender, attacking):
    s = Sound("sounds/Sleep Powder.mp")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_sludge(attacker, defender, attacking):
    s = Sound("sounds/Sludge.ogg")
    tmp = loadalphaimg('moves/acid.png')
    drop = loadalphaimg('moves/drop.png')
    s.play()
    if attacking:
        low_arch_away(attacker,defender,tmp)
        display.update(SCREEN.blit(tmp,LOW_ARC[-1]))
        display.update(SCREEN.blit(drop, (900,220)))
        draw_opp_pkmn_sprite(defender)
        sleep(.1)
        display.update([900,220, drop.get_width(), drop.get_height()])
        display.update(SCREEN.blit(drop, (900,270)))
        draw_opp_pkmn_sprite(defender)
        sleep(.1)
        display.update([900,270, drop.get_width(), drop.get_height()])

        display.update(SCREEN.blit(drop, (900,320)))
        draw_opp_pkmn_sprite(defender)
        sleep(.1)
        display.update([900,320, drop.get_width(), drop.get_height()])
        display.update(SCREEN.blit(drop, (950,220)))
        draw_opp_pkmn_sprite(defender)
        sleep(.1)
        display.update([950,220, drop.get_width(), drop.get_height()])
        display.update(SCREEN.blit(drop, (950,270)))
        draw_opp_pkmn_sprite(defender)
        sleep(.1)
        display.update([950,270, drop.get_width(), drop.get_height()])
        display.update(SCREEN.blit(drop, (950,320)))
        sleep(.1)
        display.update(draw_opp_pkmn_sprite(defender))
    else:
        low_arch_towards(defender,attacker,tmp)
        display.update(SCREEN.blit(tmp,(200,400)))
        display.update(SCREEN.blit(drop, (220,510)))
        draw_my_pkmn_sprite(defender)
        sleep(.1)
        display.update([220,510, drop.get_width(), drop.get_height()])
        display.update(SCREEN.blit(drop, (220,560)))
        draw_my_pkmn_sprite(defender)
        sleep(.1)
        display.update([220,560, drop.get_width(), drop.get_height()])

        display.update(SCREEN.blit(drop, (220,610)))
        draw_my_pkmn_sprite(defender)
        sleep(.1)
        display.update([220,610, drop.get_width(), drop.get_height()])
        display.update(SCREEN.blit(drop, (270,510)))
        draw_my_pkmn_sprite(defender)
        sleep(.1)
        display.update([270,510, drop.get_width(), drop.get_height()])
        display.update(SCREEN.blit(drop, (270,560)))
        draw_my_pkmn_sprite(defender)
        sleep(.1)
        display.update([270,560, drop.get_width(), drop.get_height()])
        display.update(SCREEN.blit(drop, (270,610)))
        sleep(.1)
        display.update(draw_my_pkmn_sprite(defender))
    dmged()
    s.stop()


def do_smog(attacker, defender, attacking):
    s = Sound("sounds/Smog.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_smokescreen(attacker, defender, attacking):
    s = Sound("sounds/Smokescreen.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_softboiled(attacker, defender, attacking):
    s = Sound("sounds/Softboilied.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_solarbeam_prep(attacker, defender, attacking):
    #TODO NO SOUND?
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending


def do_solarbeam(attacker, defender, attacking):
    s = Sound("sounds/SolarBeam.ogg")
    s.play()
    if attacking:
        beam(attacker, defender, attacking, type_='solar')
        double(attacker, defender)
    else:
        beam(attacker, defender, attacking, type_='solar')
        opp_double(attacker, defender)
    dmged()
    s.stop()


def do_sonicboom(attacker, defender, attacking):
    s = Sound("sounds/Sonic Boom.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_spike_cannon(attacker, defender, attacking):
    s = Sound("sounds/Spike Cannon.ogg")
    s.play()
    if attacking:
        big_3(attacker, defender)
    else:
        opp_big_3(attacker, defender)
    dmged()
    s.stop()


def do_splash(attacker, defender, attacking):
    s = Sound("sounds/Spash.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_spore(attacker, defender, attacking):
    s = Sound("sounds/Spore.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_stomp(attacker, defender, attacking):
    s = Sound("sounds/Stomp.ogg")
    s.play()
    if attacking:
        display.update(mid_big())
        sleep(.15)
        display.update(draw_opp_pkmn_sprite(defender))
    else:
        display.update(opp_mid_big())
        sleep(.15)
        display.update(draw_my_pkmn_sprite(defender))
    dmged()
    s.stop()


def do_strength(attacker, defender, attacking):
    s = Sound("sounds/Strength.ogg")
    s.play()
    if attacking:
        big_3(attacker, defender)
    else:
        opp_big_3(attacker, defender)
    s.stop()


def do_string_shot(attacker, defender, attacking):
    s = Sound("sounds/String Shot.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_struggle(attacker, defender, attacking):
    s = Sound("sounds/Struggle.ogg")
    s.play()
    if attacking:
        double(attacker, defender)
    else:
        opp_double(attacker, defender)
    dmged()
    s.stop()


def do_stun_spore(attacker, defender, attacking):
    s = Sound("sounds/Stun Spore.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_submission(attacker, defender, attacking):
    s = Sound("sounds/Submission.ogg")
    s.play()
    if attacking:
        double(attacker, defender)
    else:
        opp_double(attacker, defender)
    dmged()
    s.stop()


def do_substitute(attacker, defender, attacking):
    s = Sound("sounds/Substitute.ogg")
    s.play()
    invert()
    if attacking:
        big_3(attacker, defender)
    else:
        opp_big_3(attacker, defender)
    invert()
    dmged()
    s.stop()


def do_super_fang(attacker, defender, attacking):
    s = Sound("sounds/Super Fang.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_supersonic(attacker, defender, attacking):
    s = Sound("sounds/Supersonic.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_surf(attacker, defender, attacking):
    s = Sound("sounds/Surf.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_swift(attacker, defender, attacking):
    s = Sound("sounds/Swift.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_swords_dance(attacker, defender, attacking):
    s = Sound("sounds/Swords Dance.ogg")
    s.play()
    if attacking:
        pass
    else:
        pass  # TODO defending
    s.stop()


def do_tackle(attacker, defender, attacking):
    s = Sound("sounds/Tackle.ogg")
    s.play()
    if attacking:
        display.update(draw.rect(SCREEN, WHITE, MYPKMN + SSIZE))
        display.update(SCREEN.blit(attacker.backimg, tuple(map(sum,zip(tuple(MYPKMN),(28,0))))))
        sleep(.25)
        display.update(draw.rect(SCREEN, WHITE, tuple(map(sum,zip(tuple(MYPKMN + SSIZE),(28,0,0,0))))))
        display.update(SCREEN.blit(attacker.backimg, MYPKMN))
        sleep(.25)
    else:
        display.update(draw.rect(SCREEN, WHITE, OPPPKMN + SSIZE))
        display.update(SCREEN.blit(attacker.frontimg, tuple(map(sum,zip(tuple(OPPPKMN),(-28,0))))))
        sleep(.25)
        display.update(draw.rect(SCREEN, WHITE, tuple(map(sum,zip(tuple(OPPPKMN + SSIZE),(-28,0,0,0))))))
        display.update(SCREEN.blit(attacker.frontimg, OPPPKMN))
        sleep(.25)
    dmged()
    s.stop()


def do_tail_whip(attacker, defender, attacking):
    s = Sound("sounds/Tail Whip.ogg")
    s.play()
    if attacking:
        display.update(draw.rect(SCREEN, WHITE, MYPKMN + SSIZE))
        display.update(SCREEN.blit(attacker.backimg, tuple(map(sum,zip(tuple(MYPKMN),(28,0))))))
        sleep(.25)
        display.update(draw.rect(SCREEN, WHITE, tuple(map(sum,zip(tuple(MYPKMN + SSIZE),(28,0,0,0))))))
        display.update(SCREEN.blit(attacker.backimg, MYPKMN))
        sleep(.25)
        display.update(draw.rect(SCREEN, WHITE, MYPKMN + SSIZE))
        display.update(SCREEN.blit(attacker.backimg, tuple(map(sum,zip(tuple(MYPKMN),(28,0))))))
        sleep(.25)
        display.update(draw.rect(SCREEN, WHITE, tuple(map(sum,zip(tuple(MYPKMN + SSIZE),(28,0,0,0))))))
        display.update(SCREEN.blit(attacker.backimg, MYPKMN))
        sleep(.25)
    else:
        display.update(draw.rect(SCREEN, WHITE, OPPPKMN + SSIZE))
        display.update(SCREEN.blit(attacker.frontimg, tuple(map(sum,zip(tuple(OPPPKMN),(-28,0))))))
        sleep(.25)
        display.update(draw.rect(SCREEN, WHITE, tuple(map(sum,zip(tuple(OPPPKMN + SSIZE),(-28,0,0,0))))))
        display.update(SCREEN.blit(attacker.frontimg, OPPPKMN))
        sleep(.25)
        display.update(draw.rect(SCREEN, WHITE, OPPPKMN + SSIZE))
        display.update(SCREEN.blit(attacker.frontimg, tuple(map(sum,zip(tuple(OPPPKMN),(-28,0))))))
        sleep(.25)
        display.update(draw.rect(SCREEN, WHITE, tuple(map(sum,zip(tuple(OPPPKMN + SSIZE),(-28,0,0,0))))))
        display.update(SCREEN.blit(attacker.frontimg, OPPPKMN))
        sleep(.25)
    s.stop()


def do_take_down(attacker, defender, attacking):
    s = Sound("sounds/Take Down.ogg")
    s.play()
    if attacking:
        display.update(draw.rect(SCREEN, WHITE, MYPKMN + SSIZE))
        display.update(SCREEN.blit(attacker.backimg, tuple(map(sum,zip(tuple(MYPKMN),(28,0))))))
        sleep(.15)
        display.update(draw.rect(SCREEN, WHITE, tuple(map(sum,zip(tuple(MYPKMN + SSIZE),(28,0,0,0))))))
        display.update(SCREEN.blit(attacker.backimg, MYPKMN))
        invert()
        sleep(.15)
        invert()

    else:
        display.update(draw.rect(SCREEN, WHITE, OPPPKMN + SSIZE))
        display.update(SCREEN.blit(attacker.frontimg, tuple(map(sum,zip(tuple(OPPPKMN),(-28,0))))))
        sleep(.15)
        display.update(draw.rect(SCREEN, WHITE, tuple(map(sum,zip(tuple(OPPPKMN + SSIZE),(-28,0,0,0))))))
        display.update(SCREEN.blit(attacker.frontimg, OPPPKMN))
        invert()
        sleep(.15)
        invert()
    dmged()
    s.stop()


def do_teleport(attacker, defender, attacking):
    s = Sound("sounds/Teleport.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_thrash(attacker, defender, attacking):
    s = Sound("sounds/Thrash.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_thunder(attacker, defender, attacking):
    s = Sound("sounds/Thunder.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_thunder_wave(attacker, defender, attacking):
    s = Sound("sounds/Thunder Wave.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_thunderbolt(attacker, defender, attacking):
    s = Sound("sounds/Thunderbolt.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_thunderpunch(attacker, defender, attacking):
    s = Sound("sounds/Thunder Punch.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_thundershock(attacker, defender, attacking):
    s = Sound("sounds/ThunderShock.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_toxic(attacker, defender, attacking):
    s = Sound("sounds/Toxic.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_transform(attacker, defender, attacking):
    s = Sound("sounds/Transform.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_tri_attack(attacker, defender, attacking):
    s = Sound("sounds/Tri Attack.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_twineedle(attacker, defender, attacking):
    s = Sound("sounds/Twineedle.ogg")
    s.play()
    if attacking:
        double(attacker, defender)
        sleep(.15)
        double(attacker, defender)
    else:
        opp_double(attacker, defender)
        sleep(.15)
        opp_double(attacker, defender)
    dmged()
    s.stop()


def do_vicegrip(attacker, defender, attacking):
    s = Sound("sounds/Vice Grip.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_vine_whip(attacker, defender, attacking):
    s = Sound("sounds/Vine Whip.ogg")
    s.play()
    tmp = loadalphaimg('moves/cut1.png')
    tmp2 = loadalphaimg('moves/cut2.png')
    s.play()
    if attacking:
        display.update(SCREEN.blit(tmp,(800,10)))
        sleep(.15)
        display.update(draw_opp_pkmn_sprite(defender))
        display.update(SCREEN.blit(tmp2,(800,10)))
        sleep(.15)
        display.update(draw_opp_pkmn_sprite(defender))
        double(attacker, defender)
    else:
        display.update(SCREEN.blit(tmp,(70,300)))
        sleep(.15)
        display.update(draw_my_pkmn_sprite(defender))
        display.update(SCREEN.blit(tmp2,(70,300)))
        sleep(.15)
        display.update(draw_my_pkmn_sprite(defender))
        opp_double(attacker, defender)
    dmged()
    s.stop()
    s.stop()


def do_water_gun(attacker, defender, attacking):
    s = Sound("sounds/Water Gun.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_waterfall(attacker, defender, attacking):
    s = Sound("sounds/Waterfall.ogg")

    pumps =  []
    for i in range(1,7):
        pumps.append(loadalphaimg('moves/hydro{0}.png'.format(i)))
    s.play()
    if attacking:
        for i in range(6):
            display.update(SCREEN.blit(pumps[i],(820,75)))
            sleep(.15)
            display.update(draw_opp_pkmn_sprite(defender))
        for i in range(6):
            display.update(SCREEN.blit(pumps[i],(940,75)))
            sleep(.15)
            display.update(draw_opp_pkmn_sprite(defender))
        sleep(.3)
        double(attacker, defender)

    else:
        for i in range(6):
            display.update(SCREEN.blit(pumps[i],(150,365)))
            sleep(.15)
            display.update(draw_my_pkmn_sprite(defender))
        for i in range(6):
            display.update(SCREEN.blit(pumps[i],(270,365)))
            sleep(.15)
            display.update(draw_my_pkmn_sprite(defender))
        sleep(.3)
        opp_double(attacker, defender)

    dmged()
    s.stop()


def do_whirlwind(attacker, defender, attacking):
    s = Sound("sounds/Whirlwind.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_wing_attack(attacker, defender, attacking):
    s = Sound("sounds/Wing Attack.ogg")
    s.play()
    if attacking:
        big_3(attacker, defender)
    else:
        opp_big_3(attacker, defender)
    dmged()
    s.stop()


def do_withdraw(attacker, defender, attacking):
    s = Sound("sounds/Withdraw.ogg")
    s.play()
    if attacking:
        pass  # TODO attacking
    else:
        pass  # TODO defending
    s.stop()


def do_wrap(attacker, defender, attacking):
    s = Sound("sounds/Wrap.ogg")
    s.play()
    tmp = loadalphaimg('moves/bind.png')

    s.play()
    if attacking:
        display.update(SCREEN.blit(tmp,(720,100)))
        sleep(.2)
        draw.rect(SCREEN, WHITE, (720,100, tmp.get_width(), tmp.get_height()))
        draw_opp_pkmn_sprite(defender)
        display.update([720,100, tmp.get_width(), tmp.get_height()])
        sleep(.2)
        display.update(SCREEN.blit(tmp,(720,100)))
        sleep(.2)
        draw.rect(SCREEN, WHITE, (720,100, tmp.get_width(), tmp.get_height()))
        draw_opp_pkmn_sprite(defender)
        display.update([720,100, tmp.get_width(), tmp.get_height()])
        sleep(.2)
    else:
        display.update(SCREEN.blit(tmp,(40,450)))
        sleep(.2)
        draw.rect(SCREEN, WHITE, (40,450, tmp.get_width(), tmp.get_height()))
        draw_my_pkmn_sprite(defender)
        display.update([40,450, tmp.get_width(), tmp.get_height()])
        sleep(.2)
        display.update(SCREEN.blit(tmp,(40,450)))
        sleep(.2)
        draw.rect(SCREEN, WHITE, (40,450, tmp.get_width(), tmp.get_height()))
        draw_my_pkmn_sprite(defender)
        display.update([40,450, tmp.get_width(), tmp.get_height()])
        sleep(.2)
    dmged()
    s.stop()
