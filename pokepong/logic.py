from pygame import draw, display
from pygame.mixer import Sound
import pygame
from sqlalchemy.orm.exc import NoResultFound
from pokepong.util import MyMoveOccuring, OppMoveOccuring, loadalphaimg, loadimg
from pokepong.util import alphabet, randint, choice, HIGH_ARC
from time import sleep
from math import floor
import json
from pokepong.routes import ROUTES, MAPLIST, MAPROUTE, TRAINERS
from pokepong.database import db
from pokepong.util import word_builder, write_btm, draw_my_hp
from pokepong.util import draw_opp_hp, wait_for_button, clearbtm
from pokepong.util import WHITE, GREEN, YELLOW, RED, GREY, BLACK, SCREEN, SIZE
from pokepong.util import BTM, BTM_TUPLE
from pokepong.util import r

pygame.mixer.init()
SHOP = Sound("sounds/shop.ogg")
EVOLVE = Sound("sounds/evolve.ogg")


# TODO if speeds are equal me will go first.  me is different on client vs
# server

MYHP = loadalphaimg('myhp.png')
OPPHP = loadalphaimg('opphp.png')
MOVECHOICE = loadalphaimg('choiceclean.png')
ATTACK = loadalphaimg('attack.png')
HPBAR = loadalphaimg('hpbar.png')
MYBAR = loadalphaimg('mybar.png')
OPPBAR = loadalphaimg('oppbar.png')
ALIVE = loadalphaimg('alive.png')
FAINTED = loadalphaimg('fainted.png')
NOMON = loadalphaimg('nomon.png')
FORGET = loadalphaimg('forget.png')
CONF = loadalphaimg('conf.png')
WORT = loadalphaimg('wort.png')
LOGO = loadalphaimg('logo.png')
TRAINER = loadalphaimg('trainer.png')
TRAINERBACK = loadalphaimg('trainerback.png')
POKE1 = loadalphaimg('poke1.png')
POKE2 = loadalphaimg('poke2.png')
ITEMS = loadalphaimg('items.png')
MONEY = loadalphaimg('moneybar.png')
AMOUNT = loadalphaimg('amount.png')
SHOP_CHOICE = loadalphaimg('shop_choice.png')
MAP = loadimg('map.png').convert()
MAPSELECTOR = loadalphaimg('mapselector.png')
BALL = {'POK~BALL': [loadalphaimg('balls/PLball.png'),
                     loadalphaimg('balls/PCball.png'),
                     loadalphaimg('balls/PRball.png')],
        'GREAT BALL': [loadalphaimg('balls/GLball.png'),
                       loadalphaimg('balls/GCball.png'),
                       loadalphaimg('balls/GRball.png')],
        'ULTRA BALL': [loadalphaimg('balls/ULball.png'),
                       loadalphaimg('balls/UCball.png'),
                       loadalphaimg('balls/URball.png')],
        'MASTER BALL': [loadalphaimg('balls/MLball.png'),
                        loadalphaimg('balls/MCball.png'),
                        loadalphaimg('balls/MRball.png')]}

POP = [loadalphaimg('pop1.png'), loadalphaimg('pop2.png'),
       loadalphaimg('pop3.png'), loadalphaimg('pop4.png'),
       loadalphaimg('pop5.png')]

VITAMINS = ['Protein', 'Iron', 'HP Up', 'Calcium', 'Carbos']

ABLE = {'Thunderstone': {133: 135, 25: 26},
        'Fire Stone': {133: 136, 37: 38, 58: 59},
        'Water Stone': {133: 134, 90: 91, 120: 121, 61: 62},
        'Leaf Stone': {70: 71, 102: 13, 44: 45},
        'Moon Stone': {30: 31, 33: 34, 35: 36, 39: 40},
        'Link Stone': {64: 65, 67: 68, 93: 94, 75: 76}}

SSIZE = [392, 392]

MYHPBAR_RECT = [
    SIZE[0] - 700, SIZE[1] - 505, MYHP.get_width(), MYHP.get_height()]
MYHP_RECT = [SIZE[0] - 532, SIZE[1] - 486, 399, 14]
MYPKMN = [59, SIZE[1] - 736]

OPPHPBAR_RECT = [80, 120, 602, 91]
OPPHP_RECT = [227, 141, 399, 15]
OPPPKMN = [SIZE[0] - 500, 0]

def clear():
    """
    function
    """
    SCREEN.fill(WHITE)


def draw_map():
    """
    function
    """
    SCREEN.blit(MAP, (0, 0))

def get_trainers(loc):
    return choice(TRAINERS[loc])

def get_wild_mon(route):
    """
    function
    """
    tmp = ROUTES[route]
    poss = []
    for i in tmp:
        poss.extend([i] * int((tmp[i][1] * 100)))
    name = choice(poss)
    lvl = randint(tmp[name][0][0], tmp[name][0][1])
    return get_mon(name, lvl)


def get_mon(name, lvl):
    pkmn = Owned(Pokemon.query.filter(Pokemon.name == name).one().id, lvl=lvl)
    pkmn.exp = {'f': int(4 * lvl ** 3 / 5.),
                'mf': lvl ** 3,
                'ms': int(6 / 5. * lvl ** 3 - 15 * lvl ** 2 + 100 * lvl - 140),
                's': int(5 * lvl ** 3 / 4.)}[pkmn.base.lvlspeed]
    return pkmn


def draw_my_hp_bar():
    """
    function
    """
    draw.rect(SCREEN, WHITE, MYHPBAR_RECT)
    SCREEN.blit(MYHP, MYHPBAR_RECT[:2])
    return [MYHPBAR_RECT]


def draw_my_lvl(pkmn):
    """
    function
    """
    return [word_builder('%' + str(pkmn.lvl) + ' ', SIZE[0] - 405, SIZE[1] - 565)]


def draw_my_hp(pkmn):
    """
    function
    """
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
    """
    function
    """
    draw.rect(SCREEN, WHITE, MYPKMN + SSIZE)
    SCREEN.blit(pkmn.backimg, MYPKMN)
    return [MYPKMN + SSIZE]


def draw_my_pkmn_name(pkmn):
    """
    function
    """
    display.update(
        draw.rect(SCREEN, WHITE, [SIZE[0] - 630, SIZE[1] - 625, 600, 60]))
    return [word_builder(pkmn.name.upper(), SIZE[0] - 630, SIZE[1] - 625)]


def draw_my_poke_balls(team):
    """
    function
    """
    draw.rect(SCREEN, WHITE, MYHPBAR_RECT)
    SCREEN.blit(MYBAR, (SIZE[0] - 700, SIZE[1] - 442))
    offset = 0
    for mon in team:
        if mon.hp == 0:
            SCREEN.blit(FAINTED, (SIZE[0] - 575 + offset * 65, SIZE[1] - 430))
        else:
            SCREEN.blit(ALIVE, (SIZE[0] - 575 + offset * 65, SIZE[1] - 430))
        offset += 1
    for i in range(offset, 6):
        SCREEN.blit(NOMON, (SIZE[0] - 500 + (i - 1) * 65, SIZE[1] - 430))
    return [MYHPBAR_RECT]


def draw_opp_lvl(pkmn):
    """
    function
    """
    return [word_builder('%' + str(pkmn.lvl) + ' ', 230, 60)]


def draw_opp_hp_bar():
    """
    function
    """
    draw.rect(SCREEN, WHITE, OPPHPBAR_RECT)
    SCREEN.blit(OPPHP, OPPHPBAR_RECT[:2])
    return [OPPHPBAR_RECT]

def draw_opp_hp(pkmn):
    """
    function
    """
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
    """
    function
    """
    draw.rect(SCREEN, WHITE, OPPPKMN + SSIZE)
    SCREEN.blit(pkmn.frontimg, OPPPKMN)
    return [OPPPKMN + SSIZE]


def draw_opp_pkmn_name(pkmn):
    """
    function
    """
    display.update(draw.rect(SCREEN, WHITE, [60, 1, 600, 60]))
    return [word_builder(pkmn.name.upper(), 60, 1)]


def draw_opp_poke_balls(team):
    """
    function
    """
    draw.rect(SCREEN, WHITE, OPPHPBAR_RECT)
    SCREEN.blit(OPPBAR, OPPHPBAR_RECT[:2])
    offset = 0
    for mon in team:
        if mon.hp == 0:
            SCREEN.blit(FAINTED, (180 + offset * 65, 132))
        else:
            SCREEN.blit(ALIVE, (180 + offset * 65, 132))
        offset += 1
    for i in range(offset, 6):
        SCREEN.blit(NOMON, (180 + i * 65, 132))
    return [OPPHPBAR_RECT]


def return_my_pokemon(me):
    """
    function
    """
    dirty = []
    dirty.append(draw.rect(SCREEN, WHITE, MYPKMN + SSIZE))
    dirty.extend(write_btm('Return', me.current.name))
    display.update(dirty)
    sleep(1)


def pop_ball(name):
    """
    function
    """
    display.update(write_btm('Go! ' + name + '!'))
    sleep(1)
    old = [0, 0, 0, 0]
    for i in POP[:-1]:
        write_btm('Go! ' + name + '!')
        tmp = SCREEN.blit(i, (115, 450))
        display.update(tmp)
        sleep(.1)
        old = tmp
        draw.rect(SCREEN, WHITE, old)
    tmp = SCREEN.blit(POP[-1], (87, 422))
    display.update(tmp)
    sleep(.1)
    display.update(draw.rect(SCREEN, WHITE, tmp))
    display.update(write_btm(''))


def draw_all_me(pkmn):
    """
    function
    """
    x = []
    x.extend(draw_my_pkmn_sprite(pkmn))
    x.extend(draw_my_pkmn_name(pkmn))
    x.extend(draw_my_hp_bar())
    x.extend(draw_my_hp(pkmn))
    x.extend(draw_my_lvl(pkmn))
    display.update(x)


def draw_all_opp(pkmn):
    """
    function
    """
    x = []
    x.extend(draw_opp_pkmn_sprite(pkmn))
    x.extend(draw_opp_pkmn_name(pkmn))
    x.extend(draw_opp_hp_bar())
    x.extend(draw_opp_hp(pkmn))
    x.extend(draw_opp_lvl(pkmn))
    display.update(x)


def intro(current):
    """
    function
    """
    clear()
    display.flip()
    SCREEN.blit(current, [305, 520])
    SCREEN.blit(TRAINER, [640, 512])
    display.update([[305, 520, current.get_width(), current.get_height()],
                    [640, 512, TRAINER.get_width(), TRAINER.get_height()]])
    width = LOGO.get_width()
    height = LOGO.get_height()
    for i in range(-470, 50, 1):
        draw.rect(SCREEN, WHITE, [130, i - 1, width, height])
        SCREEN.blit(LOGO, (130, i))
        display.update([130, i - 1, width, height + 1])
    for i in range(50, -20, -1):
        draw.rect(SCREEN, WHITE, [130, i + 1, width, height])
        SCREEN.blit(LOGO, (130, i))
        display.update([130, i + 1, width, height + 1])
    for i in range(-20, 50, 1):
        draw.rect(SCREEN, WHITE, [130, i - 1, width, height])
        SCREEN.blit(LOGO, (130, i))
        display.update([130, i - 1, width, height + 1])


def scrolling(current, possible):
    """
    function
    """
    width = current.get_width()
    height = current.get_height()
    for x in range(305, -392, -1):
        draw.rect(SCREEN, WHITE, [x + 1, 520, width, height])
        SCREEN.blit(current, (x, 520))
        SCREEN.blit(TRAINER, (640, 512))
        display.update([x + 1, 520, width + 1, height])
    old = current
    while old == current:
        current = choice(possible)
    for x in range(1280, 304, -1):
        draw.rect(SCREEN, WHITE, [x + 1, 520, width, height])
        SCREEN.blit(current, (x, 520))
        SCREEN.blit(TRAINER, (640, 512))
        display.update([x + 1, 520, width + 1, height])
    return current


def build_team(testpkmn, me=False):
    """
    function
    """
    team = []
    for i in range(0, len(testpkmn)):
        team.append(Pokemon(*testpkmn[i]))
        if me:
            pkmn = loadimg('backs/{0}.PNG'.format(team[-1].baseid)).convert()
        else:
            pkmn = loadimg('fronts/{0}.PNG'.format(team[-1].baseid)).convert()
        pkmn.set_colorkey((255, 255, 255))
        team[-1].setimg(pkmn)
    return team


def move_opp_trainer_in():
    """
    function
    """
    width = TRAINER.get_width()
    height = TRAINER.get_height()
    for i in range(SIZE[0] + 10, SIZE[0] - 501, -1):
        draw.rect(SCREEN, WHITE, [i + 1, 0, width, height])
        SCREEN.blit(TRAINER, (i, 10))
        display.update(i, 0, width + 1, height)


def move_opp_trainer_out():
    """
    function
    """
    width = TRAINER.get_width()
    height = TRAINER.get_height()
    for i in range(SIZE[0] - 500, SIZE[0] + 10, 1):
        draw.rect(SCREEN, WHITE, [i - 1, 0, width, height])
        SCREEN.blit(TRAINER, (i, 10))
        display.update(i - 1, 0, width + 1, height)


def move_my_trainer():
    """
    function
    """
    width = TRAINERBACK.get_width()
    height = TRAINERBACK.get_height()
    for i in range(59, -400, -1):
        draw.rect(SCREEN, WHITE, [i + 1, SIZE[1] - 740, width, height])
        SCREEN.blit(TRAINERBACK, (i, SIZE[1] - 740))
        display.update(i, SIZE[1] - 740, width + 1, height)


def draw_my_trainer():
    """
    function
    """
    width = TRAINERBACK.get_width()
    height = TRAINERBACK.get_height()
    SCREEN.blit(TRAINERBACK, (59, SIZE[1] - 740))
    return [[59, SIZE[1] - 740, width, height]]


def draw_choice(select):
    """
    function
    """
    dirty = []
    dirty.append(SCREEN.blit(MOVECHOICE, BTM_TUPLE))
    dirty.append(word_builder(
        ['>', ' ', ' ', ' '][select] + 'FIGHT', SIZE[0] - 730, SIZE[1] - 250))
    dirty.append(word_builder(
        [' ', '>', ' ', ' '][select] + 'ITEM', SIZE[0] - 730, SIZE[1] - 130))
    dirty.append(
        word_builder([' ', ' ', '>', ' '][select] + '#$', SIZE[0] - 350, SIZE[1] - 250))
    dirty.append(word_builder(
        [' ', ' ', ' ', '>'][select] + 'RUN', SIZE[0] - 350, SIZE[1] - 130))
    display.update(dirty)


def update_choice(select):
    """
    function
    """
    dirty = []
    dirty.append(
        word_builder(['>', ' ', ' ', ' '][select], SIZE[0] - 730, SIZE[1] - 250))
    dirty.append(
        word_builder([' ', '>', ' ', ' '][select], SIZE[0] - 730, SIZE[1] - 130))
    dirty.append(
        word_builder([' ', ' ', '>', ' '][select], SIZE[0] - 350, SIZE[1] - 250))
    dirty.append(
        word_builder([' ', ' ', ' ', '>'][select], SIZE[0] - 350, SIZE[1] - 130))
    display.update(dirty)


def draw_location(select):
    """
    function
    """
    draw_map()
    display.flip()
    display.update(SCREEN.blit(MAPSELECTOR, MAPLIST[select]))
    display.update(word_builder(MAPROUTE[select], 50, 10))


def draw_loc_update(old, new):
    """
    function
    """
    draw_map()
    display.update(
        MAPLIST[old] + [MAPSELECTOR.get_width(), MAPSELECTOR.get_height()])
    display.update(SCREEN.blit(MAPSELECTOR, MAPLIST[new]))
    word_builder(MAPROUTE[new], 50, 10)
    display.update(50, 10, 1280, 64)


def me_next_mon(me, opp, mode, socket):
    """
    function
    """
    send_val = draw_choose_pkmn(me, opp, mode, mydeath=True)
    if mode == 'battle':
        socket.send(str(send_val))
        tmp = int(socket.recv())
        if opp.current != opp.pkmn[tmp]:
            opp.set_current(tmp)
            # TODO animate swap
    draw_all_opp(opp.current)


def toss_ball(item, me, pkmn):
    """
    function
    """
    old = [0, 0, 0, 0]
    for i in HIGH_ARC:
        draw_all_opp(pkmn)
        draw_my_pkmn_sprite(me.current)
        tmp = SCREEN.blit(BALL[item][1], (i[0], i[1] + 200))
        display.update([tmp, old])
        sleep(.1)
        old = tmp
        draw.rect(SCREEN, WHITE, old)
    draw_all_me(me.current)
    display.update(old)


def open_ball(me, opp):
    """
    function
    """
    x = 800
    y = 204
    for i in POP[:-1]:
        tmp = SCREEN.blit(i, (x, y))
        display.update(tmp)
        sleep(.1)
        old = tmp
        draw.rect(SCREEN, WHITE, old)
        draw_opp_pkmn_sprite(opp.current)
        draw_all_me(me.current)
    tmp = SCREEN.blit(POP[-1], (x - 28, y - 28))
    display.update(tmp)
    sleep(.1)
    draw.rect(SCREEN, WHITE, tmp)
    draw_opp_pkmn_sprite(opp.current)
    draw_all_me(me.current)
    display.update(tmp)


def wobble(val, item):
    """
    function
    """
    ballloc = [800, 270]
    display.update(draw.rect(SCREEN, WHITE, OPPPKMN + SSIZE))
    tmp = ballloc + [BALL[item][1].get_width(), BALL[item][1].get_height()]
    for i in range(min(3, val)):
        display.update(draw.rect(SCREEN, WHITE, tmp))
        display.update(SCREEN.blit(BALL[item][1], ballloc))
        sleep(.5)
        display.update(draw.rect(SCREEN, WHITE, tmp))
        display.update(SCREEN.blit(BALL[item][0], ballloc))
        sleep(.1)
        display.update(draw.rect(SCREEN, WHITE, tmp))
        display.update(SCREEN.blit(BALL[item][1], ballloc))
        sleep(.1)
        display.update(draw.rect(SCREEN, WHITE, tmp))
        display.update(SCREEN.blit(BALL[item][2], ballloc))
        sleep(.1)
    if val == 1:
        display.update(write_btm('Darn! The POK~MON', 'broke free!'))
    elif val == 2:
        display.update(write_btm('Aww! It appeared', 'to be caught!'))
    elif val == 3:
        display.update(write_btm('Shoot! It was so', 'close too!'))


def catchem(item, pkmn, me, opp):
    """
    function
    """
    val = pkmn.catch_me(item[0])
    toss_ball(item, me, pkmn)
    if val > 0:
        open_ball(me, opp)
        wobble(val, item)
        if val < 4:
            display.update(draw_all_opp(pkmn))
        else:
            pkmn.owner = me
            db.add(pkmn)
            db.add(me)
            db.commit()
            if len(me.pkmn) < 6:
                me.pkmn.append(pkmn)
            display.update(write_btm(pkmn.name + ' was', 'caugt!'))
    else:
        display.update(draw_all_opp(pkmn))
        display.update(write_btm('You missed the', 'POK~MON'))
    wait_for_button()
    return val == 4


def opp_next_mon(me, opp, mode, socket):
    """
    function
    """
    display.update(draw.rect(SCREEN, WHITE, [230, 60, 180, 60]))
    display.update(draw.rect(SCREEN, WHITE, [60, 1, 600, 60]))
    display.update(draw_opp_poke_balls(opp.pkmn))
    if mode == 'random':
        opp.get_next_pkmn()
    elif mode == 'pong':
        opp.get_next_pkmn()
    elif mode == 'battle':
        opp.set_current(wait_for_opp_next_mon(socket))
    display.update(write_btm(opp.name + ' is', 'about to use'))
    if mode != 'pong':
        wait_for_button()
    else:
        sleep(1)
    display.update(write_btm('about to use', opp.current.name))
    if mode != 'pong':
        wait_for_button()
    else:
        sleep(1)
    change_pokemon(me, opp, mode)
    if mode == 'battle':
        socket.send(str(me.get_current_index()))
    dirty = []
    dirty.extend(
        write_btm(opp.name + ' sent', 'out ' + opp.current.name + '!'))
    dirty.extend(draw_opp_pkmn_sprite(opp.current))
    display.update(dirty)
    sleep(1)
    dirty = []
    dirty.extend(draw_opp_hp(opp.current))
    dirty.extend(draw_opp_hp_bar())
    dirty.extend(draw_opp_pkmn_name(opp.current))
    dirty.extend(draw_opp_hp(opp.current))
    dirty.extend(draw_opp_lvl(opp.current))
    display.update(dirty)


def new_game_start(me, opp, mode):
    """
    function
    """
    clear()
    display.flip()
    dirty = []
    dirty.extend(draw_my_poke_balls(me.pkmn))
    dirty.extend(draw_my_trainer())
    if mode != 'wild':
        dirty.extend(draw_opp_poke_balls(opp.pkmn))
        dirty.extend(write_btm(opp.name + ' wants', 'to fight!'))
        display.update(dirty)
        move_opp_trainer_in()
        # sleep(2)
        move_opp_trainer_out()
        draw_all_opp(opp.current)
        dirty.extend(
            write_btm(opp.name + ' sent', 'out ' + opp.current.name + '!'))
    else:
        draw_all_opp(opp.current)
        dirty.extend(write_btm('A wild ' + opp.current.name, 'has appeard!'))
    display.update(dirty)

    move_my_trainer()
    pop_ball(me.current.name)
    draw_all_me(me.current)


def attacking(me):
    """
    function
    """
    dirty = []
    selector = 0
    clearbtm()
    dirty.append(draw.rect(SCREEN, WHITE, [0, 442, 696, 300]))
    dirty.append(SCREEN.blit(ATTACK, (10, SIZE[1] - 577)))
    dirty.append(word_builder(['>', ' ', ' ', ' '][selector] +
                              me.current.moves[0].name.upper(),
                              300, SIZE[1] - 285))
    if len(me.current.moves) > 1:
        dirty.append(word_builder([' ', '>', ' ', ' '][selector] +
                                  me.current.moves[1].name.upper(),
                                  300, SIZE[1] - 225))
    else:
        dirty.append(
            word_builder([' ', '>', ' ', ' '][selector] + ' -', 300, SIZE[1] - 225))
    if len(me.current.moves) > 2:
        dirty.append(word_builder([' ', ' ', '>', ' '][selector] +
                                  me.current.moves[2].name.upper(),
                                  300, SIZE[1] - 165))
    else:
        dirty.append(word_builder([' ', ' ', '>', ' '][selector] +
                                  ' -', 300, SIZE[1] - 165))
    if len(me.current.moves) > 3:
        dirty.append(word_builder([' ', ' ', ' ', '>'][selector] +
                                  me.current.moves[3].name.upper(),
                                  300, SIZE[1] - 105))
    else:
        dirty.append(
            word_builder([' ', ' ', ' ', '>'][selector] + ' -', 300, SIZE[1] - 105))
    dirty.append(word_builder('TYPE/', 60, SIZE[1] - 530))
    dirty.extend(draw_move(me.current.moves[selector]))
    display.update(dirty)


def update_attacking(me, selector):
    """
    function
    """
    dirty = []
    dirty.append(draw.rect(SCREEN, WHITE, [0, 442, 696, 300]))
    dirty.append(SCREEN.blit(ATTACK, (10, SIZE[1] - 577)))
    dirty.append(word_builder(
        ['>', ' ', ' ', ' '][selector] + me.current.moves[0].name.upper(), 300,
        SIZE[1] - 285))
    dirty.append(
        word_builder([' ', '>', ' ', ' '][selector], 300, SIZE[1] - 225))
    dirty.append(
        word_builder([' ', ' ', '>', ' '][selector], 300, SIZE[1] - 165))
    dirty.append(
        word_builder([' ', ' ', ' ', '>'][selector], 300, SIZE[1] - 105))
    dirty.append(word_builder('TYPE/', 60, SIZE[1] - 530))
    dirty.extend(draw_move(me.current.moves[selector]))
    display.update(dirty)


def draw_items(me, select):
    """
    function
    """
    clearbtm()
    dirty = []
    dirty.append(draw.rect(
        SCREEN, WHITE, [408, SIZE[1] - 891, ITEMS.get_width(), ITEMS.get_height()]))
    dirty.append(SCREEN.blit(ITEMS, (10, SIZE[1] - 880)))
    c = 0
    for i in me.shownitems:
        if c == select:
            word_builder('>', 460, 200 + c * 120)
        else:
            word_builder(' ', 460, 200 + c * 120)
        word_builder(i.item.name.upper().ljust(12), 520, 200 + c * 120)
        if i.item.name != 'CANCEL':
            if i.count < 10:
                num = '  ' + str(i.count)
            elif i.count < 100:
                num = ' ' + str(i.count)
            else:
                num = str(i.count)
            word_builder('*' + num, 920, 260 + c * 120)
        c += 1
    display.update(dirty)


def update_items(me, select):
    """
    function
    """
    dirty = []
    c = 0
    dirty.append(draw.rect(SCREEN, WHITE, [460, SIZE[1] - 830, 700, 490]))
    for i in me.shownitems:
        if c == select:
            dirty.append(word_builder('>', 460, 200 + c * 120))
        else:
            dirty.append(word_builder(' ', 460, 200 + c * 120))
        dirty.append(
            word_builder(i.item.name.upper().ljust(12), 520, 200 + c * 120))
        if i.item.name != 'CANCEL':
            if i.count < 10:
                num = '  ' + str(i.count)
            elif i.count < 100:
                num = ' ' + str(i.count)
            else:
                num = str(i.count)
            dirty.append(word_builder('*' + num, 920, 260 + c * 120))
            c += 1
    display.update(dirty)


def update_move(selector):
    """
    function
    """
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

def draw_moves(selector, pkmn):
    """
    function
    """
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



def move_choose(pkmn):
    """
    function
    """
    selector = 0
    draw_moves(selector, pkmn)
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

def ask_move(pkmn, move):
    """
    function
    """
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
    display.update(write_btm('move to make room', 'for ' + move.name.upper() + '?'))

def new_move(pkmn, move):
    """
    function
    """
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
                pkmn.moves[retval] = tmpMove(move, 0)
                db.add(pkmn)
                db.commit()
                wait_for_button()
                SCREEN.blit(orig, (0, 0))
                display.flip()
                return True
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


def gain_exp(me, opp, multi):
    """
    function
    """
    for mon in me.used:
        tmp = None
        if mon.id > 151:
            lvlup, exp = mon.gain_exp(me, opp, multi)
            display.update(write_btm(mon.name, 'gained ' + str(exp) + ' exp.'))
            wait_for_button()
            if mon.lvl != lvlup:
                for move in mon.base.learns:
                    if mon.lvl < move.learnedat <= lvlup:
                        tmp = move.move
                mon.gain_lvl(lvlup)
                display.update(
                    write_btm(mon.name + ' grew', 'to level ' + str(lvlup) + '!'))
                mon.load_stats()
                wait_for_button()
                if tmp:
                    if len(mon.moves) < 4:
                        setattr(mon, 'move' + str(len(mon.moves) + 1), tmp)
                        display.update(
                            write_btm(mon.name + ' learned', tmp.name))
                        mon.moves.append(tmpMove(tmp, 0))
                        wait_for_button()
                    else:
                        new_move(mon, tmp)
    me.used.clear()


def do_evolve(oldpic, newpic):
    """
    function
    """
    sleep(2)
    for i in range(100):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                return False
        if (i + 2) % 12 == 0:
            draw.rect(SCREEN, WHITE, [444, 120] + SSIZE)
            display.update(SCREEN.blit(newpic, [444, 120]))
        elif i % 12 == 0:
            draw.rect(SCREEN, WHITE, [444, 120] + SSIZE)
            display.update(SCREEN.blit(oldpic, [444, 120]))
        sleep(.01)
    for i in range(100):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                return False
        if (i + 2) % 8 == 0:
            draw.rect(SCREEN, WHITE, [444, 120] + SSIZE)
            display.update(SCREEN.blit(newpic, [444, 120]))
        elif i % 8 == 0:
            draw.rect(SCREEN, WHITE, [444, 120] + SSIZE)
            display.update(SCREEN.blit(oldpic, [444, 120]))
        sleep(.01)
    for i in range(100):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                return False
        if (i + 2) % 4 == 0:
            draw.rect(SCREEN, WHITE, [444, 120] + SSIZE)
            display.update(SCREEN.blit(newpic, [444, 120]))
        elif i % 4 == 0:
            draw.rect(SCREEN, WHITE, [444, 120] + SSIZE)
            display.update(SCREEN.blit(oldpic, [444, 120]))
        sleep(.01)
    return True


def evolve(mon, new):
    """
    function
    """
    oldpic = loadimg('fronts/{0}.PNG'.format(mon.base_id)).convert()
    oldpic.set_colorkey((255, 255, 255))
    oldpic = pygame.transform.flip(oldpic, True, False)
    newpic = loadimg('fronts/{0}.PNG'.format(new)).convert()
    newpic.set_colorkey((255, 255, 255))
    newpic = pygame.transform.flip(newpic, True, False)
    clear()
    write_btm('What? {0}'.format(mon.name), 'is evolving!')
    SCREEN.blit(oldpic, [444, 120])
    display.flip()
    SHOP.stop()
    EVOLVE.play()
    if do_evolve(oldpic, newpic):
        if mon.base.name == mon.name:
            mon.name = Pokemon.query.get(new).name
        mon.base_id = new
        db.commit()
        display.update(
            write_btm('{0} evolved'.format(mon.name), "into " + mon.base.name))
    else:
        display.update(
            write_btm('Huh? {0}'.format(mon.name), "stopped evolving!"))
    EVOLVE.stop()
    wait_for_button()


def clean_me_up(me):
    """
    function
    """
    dirty = []
    dirty.append(clearbtm())
    dirty.append(draw.rect(SCREEN, WHITE, [0, 442, 695, 300]))
    draw_all_me(me.current)
    display.update(dirty)


def run_me_faint(me):
    """
    function
    """
    for i in range(0, 400, 2):
        draw.rect(SCREEN, WHITE, [59, SIZE[1] - 740, 392, 392])
        SCREEN.blit(
            me.current.backimg, (59, SIZE[1] - 740 + i), (0, 0, 392, 392 - i))
        display.update(59, SIZE[1] - 738 + i, 392, 394 - i)
    display.update(write_btm(me.current.name, 'fainted!'))
    me.used.remove(me.current)


def run_opp_faint(opp):
    """
    function
    """
    for i in range(0, 393, 2):
        draw.rect(SCREEN, WHITE, [SIZE[0] - 500, 0, 392, 392])
        SCREEN.blit(
            opp.current.frontimg, (SIZE[0] - 500, i), (0, 0, 392, 392 - i))
        display.update([SIZE[0] - 500, i - 2, 392, 394 - i])
    display.update(write_btm('Enemy ' + opp.current.name.upper(), 'fainted!'))
    sleep(2)


def dmg_pkmn(pkmn, dmg, me=False):
    """
    function
    """
    for d in range(dmg):
        pkmn.sethp(pkmn.hp - 1)
        if me:
            display.update(draw_my_hp(pkmn))
        else:
            display.update(draw_opp_hp(pkmn))
        if pkmn.hp == 0:
            return True
        sleep(.02)
    return False


def run_move(me, opp, move, first):
    """
    function
    """
    tmp = me.current.attempt_move(True)
    if tmp == 'OK':
        do_move(me.current, opp.current, move, 'tmp', True, first)
    elif tmp == 'PAR':
        display.update(write_btm(me.current.name + ' is paralyzed!', "It can't move!"))
    elif tmp == 'SLP':
        display.update(write_btm(me.current.name + ' is fast asleep!'))
    elif tmp == 'WOKE':
        display.update(write_btm(me.current.name + ' woke up!'))
    elif tmp == 1:
        return
    if me.current.alive():
        me.current.do_status(opp.current, True)
    return


def run_opp_swap(opp, val):
    """
    function
    """
    opp.set_current(val)
    draw_all_opp(opp.current)


def shop_selecting(select):
    """
    function
    """
    dirty = []
    dirty.append(word_builder(['>', ' ', ' ', ' '][select] + 'BUY', 45, 52))
    dirty.append(word_builder([' ', '>', ' ', ' '][select] + 'SELL', 45, 162))
    dirty.append(word_builder([' ', ' ', '>', ' '][select] + 'USE', 45, 272))
    dirty.append(word_builder([' ', ' ', ' ', '>'][select] + 'QUIT', 45, 382))
    display.update(dirty)


def selecting(select):
    """
    function
    """
    dirty = []
    dirty.append(word_builder(['>', ' '][select] + 'YES', 50, 465))
    dirty.append(word_builder([' ', '>'][select] + 'NO', 50, 575))
    display.update(dirty)


def draw_pkmn_choice(mon, offset):
    """
    function
    """
    SCREEN.blit(HPBAR, (220, offset * 110 + 75))
    word_builder(mon.name, 160, offset * 110 + 10)
    maxhp = mon.maxhp
    hp = mon.hp
    bar_len = floor(hp / float(maxhp) * 399)
    if bar_len < 100:
        color = RED
    elif bar_len < 200:
        color = YELLOW
    else:
        color = GREEN
    if hp > 0:
        draw.rect(SCREEN, color, [325, offset * 110 + 82, bar_len, 14])
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
    word_builder('{0}/{1}'.format(hp, maxhp), 800, offset * 110 + 60)
    SCREEN.blit(mon.sprite1, (60, offset * 110 + 15))


def update_choose(old, new, me):
    """
    function
    """
    dirty = []
    dirty.append(word_builder(' ', 0, 110 * old + 60))
    dirty.append(draw.rect(SCREEN, WHITE, [10, 110 * old + 15, 105, 105]))
    dirty.append(draw.rect(SCREEN, WHITE, [60, 110 * old + 15, 101, 101]))
    dirty.append(SCREEN.blit(me.pkmn[old].sprite1, (60, 110 * old + 15)))
    dirty.append(word_builder('>', 0, 110 * new + 60))
    display.update(dirty)


def draw_choose_items(me):
    """
    function
    """
    selector = 0
    draw_items(me, selector)
    pygame.event.clear()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                if selector > 0:
                    selector -= 1
                    update_items(me, selector)
                elif me.shownitems[0] != me.items[0]:
                    me.shift_items_left()
                    update_items(me, selector)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                if selector < 2 and selector < len(me.shownitems) - 1:
                    selector += 1
                    update_items(me, selector)
                elif len(me.shownitems) > 3:
                    me.shift_items_right()
                    update_items(me, selector)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                return -1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                return selector

def w_or_t(select):
    """
    function
    """
    dirty = []
    dirty.append(word_builder(['>', ' '][select] + 'WILD', 50, 810))
    dirty.append(word_builder([' ', '>'][select] + 'TRAINER', 50, 910))
    display.update(dirty)

def wild_or_trainer():
    """
    function
    """
    display.update(draw.rect(
        SCREEN, WHITE, [0, 748, WORT.get_width() + 14, WORT.get_height() + 17]))
    display.update(SCREEN.blit(WORT, (10, 755)))
    select = 0
    pygame.event.clear()
    w_or_t(select)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                if select == 0:
                    select = 1
                    w_or_t(select)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                if select == 1:
                    select = 0
                    w_or_t(select)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                return -1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                return select
        sleep(.02)


def choose_loc(selector):
    """
    function
    """
    draw_location(selector)
    pygame.event.clear()
    tmp = []
    flag = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                tmp.append('U')
                tmp = tmp[-8:]
                flag = False
                if selector < len(MAPROUTE) - 1:
                    selector += 1
                    draw_loc_update(selector - 1, selector)
                else:
                    selector = 0
                    draw_loc_update(len(MAPROUTE) - 1, selector)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                tmp.append('D')
                tmp = tmp[-8:]
                flag = False
                if selector > 0:
                    selector -= 1
                    draw_loc_update(selector + 1, selector)
                else:
                    selector = len(MAPROUTE) - 1
                    draw_loc_update(0, selector)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                tmp.append('L')
                tmp = tmp[-8:]
                flag = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                tmp.append('R')
                tmp = tmp[-8:]
                flag = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                if flag:
                    return ['S.S. ANNE TRUCK', 'wild', 0]
                else:
                    if selector > 0:
                        if ROUTES.has_key(MAPROUTE[selector]) and TRAINERS.has_key(MAPROUTE[selector]):
                            tmp2 = wild_or_trainer()
                        elif ROUTES.has_key(MAPROUTE[selector]):
                            tmp2 = 0
                        else:
                            tmp2 = 1
                    else:
                        return [MAPROUTE[selector], None, selector]
                    if tmp2 >= 0:
                        return [MAPROUTE[selector], ['wild', 'random'][tmp2], selector]
                    else:
                        draw_location(selector)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                if tmp == ['U', 'U', 'D', 'D', 'L', 'R', 'L', 'R']:
                    flag = True



def update_shop(shopp, select):
    """
    function
    """
    dirty = []
    c = 0
    dirty.append(draw.rect(SCREEN, WHITE, [460, SIZE[1] - 830, 750, 490]))
    for i in shopp.shownitems:
        if c == select:
            dirty.append(word_builder('>', 460, 200 + c * 120))
        else:
            dirty.append(word_builder(' ', 460, 200 + c * 120))
        dirty.append(
            word_builder(i.name.upper().ljust(12), 520, 200 + c * 120))
        if i.name != 'CANCEL':
            dirty.append(
                word_builder('<' + str(i.buyprice).rjust(4), 920, 260 + c * 120))
        c += 1
    display.update(dirty)


def update_amount(item, select):
    """
    function
    """
    dirty = []
    dirty.append(draw.rect(
        SCREEN, WHITE, [473, 495, AMOUNT.get_width() + 14, AMOUNT.get_height() + 14]))
    dirty.append(SCREEN.blit(AMOUNT, (480, 502)))
    dirty.append(word_builder('*' + str(select).zfill(2) +
                              ('<' + str(item.buyprice * select)).rjust(8), 534, 555))
    display.update(dirty)


def amount(item):
    """
    function
    """
    selector = 1
    dirty = []
    dirty.append(draw.rect(
        SCREEN, WHITE, [473, 495, AMOUNT.get_width() + 14, AMOUNT.get_height() + 14]))
    dirty.append(SCREEN.blit(AMOUNT, (480, 502)))
    dirty.append(word_builder(
        '*' + str(selector).zfill(2) + ('<' + str(item.buyprice)).rjust(8), 534, 555))
    display.update(dirty)
    pygame.event.clear()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                if selector < 99:
                    selector += 1
                else:
                    selector = 1
                update_amount(item, selector)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                if selector > 1:
                    selector -= 1
                else:
                    selector = 99
                update_amount(item, selector)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                selector = (selector + 10) % 100
                update_amount(item, selector)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                selector = (100 + (selector - 10)) % 100
                update_amount(item, selector)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                return selector


def update_using(me, select):
    """
    function
    """
    dirty = []
    c = 0
    dirty.append(draw.rect(SCREEN, WHITE, [460, SIZE[1] - 830, 700, 490]))
    for i in me.usable_items:
        if c == select:
            dirty.append(word_builder('>', 460, 200 + c * 120))
        else:
            dirty.append(word_builder(' ', 460, 200 + c * 120))
        dirty.append(
            word_builder(i.item.name.upper().ljust(12), 520, 200 + c * 120))
        if i.item.name != 'CANCEL':
            dirty.append(
                word_builder('*' + str(i.count).rjust(3), 920, 260 + c * 120))
        c += 1
    display.update(dirty)


def update_sell(me, select):
    """
    function
    """
    dirty = []
    c = 0
    dirty.append(draw.rect(SCREEN, WHITE, [460, SIZE[1] - 830, 700, 490]))
    for i in me.all_shown:
        if c == select:
            dirty.append(word_builder('>', 460, 200 + c * 120))
        else:
            dirty.append(word_builder(' ', 460, 200 + c * 120))
        dirty.append(
            word_builder(i.item.name.upper().ljust(12), 520, 200 + c * 120))
        if i.item.name != 'CANCEL':
            dirty.append(
                word_builder('*' + str(i.count).rjust(3), 920, 260 + c * 120))
        c += 1
    display.update(dirty)


def draw_use_on(mon, offset, item):
    """
    function
    """
    word_builder(mon.name, 160, offset * 110 + 10)
    word_builder('%' + str(mon.lvl), 800, offset * 110)
    SCREEN.blit(mon.sprite1, (60, offset * 110 + 15))
    if item.item.name in ABLE:
        able = mon.base_id in ABLE[item.item.name]
    elif item.item.name in VITAMINS:
        if item.item.name == 'Protein':
            able = mon.attackev < 25600
        elif item.item.name == 'Iron':
            able = mon.defenseev < 25600
        elif item.item.name == 'HP Up':
            able = mon.hpev < 25600
        elif item.item.name == 'Calcium':
            able = mon.specialev < 25600
        elif item.item.name == 'Carbos':
            able = mon.speedev < 25600
    elif item.item.name[:2] == 'TM':
        tmp = False
        for tms in mon.base.learnabletms:
            if tms.tm.name == item.item.name:
                tmp = True
                break
        able = tmp
    elif item.item.name[:2] == 'HM':
        tmp = False
        for hms in mon.base.learnablehms:
            if hms.hm.name == item.item.name:
                tmp = True
                break
        able = tmp
    elif item.item.name == 'Rare Candy':
        able = mon.lvl < 100
    word_builder(['NOT ABLE', '    ABLE'][able], 520, offset * 110 + 60)
    return able


def update_usable(old, new, me):
    """
    function
    """
    dirty = []
    dirty.append(word_builder(' ', 0, 110 * old + 60))
    dirty.append(draw.rect(SCREEN, WHITE, [10, 110 * old + 15, 105, 105]))
    dirty.append(draw.rect(SCREEN, WHITE, [60, 110 * old + 15, 101, 101]))
    dirty.append(SCREEN.blit(me.pkmn[old].sprite1, (60, 110 * old + 15)))
    dirty.append(word_builder('>', 0, 110 * new + 60))
    display.update(dirty)


def usable_on(me, item):
    """
    function
    """
    clear()
    if item.item.name[:2] == 'TM' or item.item.name[:2] == 'HM':
        display.flip()
        display.update(write_btm('Booted up a '+ item.item.name[:2]))
        wait_for_button()
        move = TmHm.query.filter(TmHm.name == item.item.name).one().move.name
        display.update(write_btm('It contained', move + '!'))
        wait_for_button()
        display.update(write_btm('Teach ' + move, 'to a POK~MON?'))
        if not conf():
            return -1
        write_btm('Use {0} on'.format(item.item.name[:2]), 'which POK~MON')
        display.update(draw.rect(
            SCREEN, WHITE, [3, 408, CONF.get_width() + 14, CONF.get_height() + 14]))
    else:
        write_btm('Use {0} on'.format(item.item.name), 'which POK~MON')

    offset = 0
    able_list = []
    for mon in me.pkmn:
        able_list.append(draw_use_on(mon, offset, item))
        offset += 1
    word_builder('>', 0, 60)
    display.flip()
    count = 0
    select = 0
    tmp = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                if select > 0:
                    select -= 1
                    update_usable(select + 1, select, me)
                    count = 1
                    tmp = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                if select < len(me.pkmn) - 1:
                    select += 1
                    update_usable(select - 1, select, me)
                    count = 1
                    tmp = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                if able_list[select]:
                    if conf():
                        return select
                    else:
                        pass
                else:
                    # TODO reject
                    pass
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                return -1

        sleep(.1)
        con1 = count % 2 == 0 and me.pkmn[
            select].hp > me.pkmn[select].maxhp / 2
        con2 = count % 5 == 0 and me.pkmn[
            select].hp <= me.pkmn[select].maxhp / 2
        if con1 or con2:
            dirty = draw.rect(SCREEN, WHITE, [60, select * 110 + 15, 101, 101])
            if tmp:
                SCREEN.blit(me.pkmn[select].sprite2, (60, select * 110 + 15))
            else:
                SCREEN.blit(me.pkmn[select].sprite1, (60, select * 110 + 15))
            display.update(dirty)
            tmp = not tmp


def use(me, item, mon):
    """
    function
    """
    if item.item.name in ABLE:
        item.use(me)
        evolve(mon, ABLE[item.item.name][mon.base_id])
    elif item.item.name in VITAMINS:
        item.use(me)
        if item.item.name == 'Protein':
            mon.attackev += 2560
        elif item.item.name == 'Iron':
            mon.defenseev += 2560
        elif item.item.name == 'HP Up':
            mon.hpev += 2560
        elif item.item.name == 'Calcium':
            mon.specialev += 2560
        elif item.item.name == 'Carbos':
            mon.speedev += 2560
    elif item.item.name[:2] == 'TM' or item.item.name[:2] == 'HM':
        move = TmHm.query.filter(TmHm.name == item.item.name).one().move
        if len(mon.moves) < 4:
            setattr(mon, 'move' + str(len(mon.moves) + 1), move)
            display.update(
                write_btm(mon.name + ' learned', move.name))
            mon.moves.append(tmpMove(move, 0))
            wait_for_button()
            db.commit()
            learned = True
        else:
            learned = new_move(mon, move)
        if learned:
            item.use(me)
    elif item.item.name == 'Rare Candy':
        item.use(me)
        tmp = None
        lvlup = mon.lvl + 1
        mon.exp = {'f': int(4 * lvl ** 3 / 5.),
                   'mf': lvl ** 3,
                   'ms': int(6/5. * lvl ** 3 - 15 * lvl ** 2 + 100 * lvl - 140),
                   's': int(5 * lvl ** 3 / 4.)}[mon.base.lvlspeed]
        for move in mon.base.learns:
            if mon.lvl < move.learnedat <= lvlup:
                tmp = move.move
        mon.gain_lvl(lvlup)
        display.update(
            write_btm(mon.name + ' grew', 'to level ' + str(lvlup) + '!'))
        mon.load_stats()
        wait_for_button()
        if tmp:
            if len(mon.moves) < 4:
                setattr(mon, 'move' + str(len(mon.moves) + 1), tmp)
                display.update(
                    write_btm(mon.name + ' learned', tmp.name))
                mon.moves.append(tmpMove(tmp, 0))
            else:
                new_move(mon, tmp)


def update_sell_amount(item, select):
    """
    function
    """
    dirty = []
    dirty.append(draw.rect(
        SCREEN, WHITE, [473, 495, AMOUNT.get_width() + 14, AMOUNT.get_height() + 14]))
    dirty.append(SCREEN.blit(AMOUNT, (480, 502)))
    dirty.append(word_builder('*' + str(select).zfill(2) +
                              ('<' + str(item.item.sellprice * select)).rjust(8), 534, 555))
    display.update(dirty)


def sell_amount(item):
    """
    function
    """
    selector = 1
    dirty = []
    dirty.append(draw.rect(
        SCREEN, WHITE, [473, 495, AMOUNT.get_width() + 14, AMOUNT.get_height() + 14]))
    dirty.append(SCREEN.blit(AMOUNT, (480, 502)))
    dirty.append(word_builder('*' + str(selector).zfill(2) +
                              ('<' + str(item.item.sellprice)).rjust(8), 534, 555))
    display.update(dirty)
    pygame.event.clear()
    pygame.key.set_repeat(100, 50)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                if selector < item.count:
                    selector += 1
                else:
                    selector = 1
                update_sell_amount(item, selector)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                if selector > 1:
                    selector -= 1
                else:
                    selector = item.count
                update_sell_amount(item, selector)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                selector = (selector + 10) % 100
                update_sell_amount(item, selector)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                selector = (100 + (selector - 10)) % 100
                update_sell_amount(item, selector)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                return selector


def do_sell(me, item, retval):
    """
    function
    """
    me.money += item.item.sellprice * retval
    for i in range(retval):
        item.use(me)
    draw_money(me)


def draw_money(me):
    """
    function
    """
    display.update(SCREEN.blit(MONEY, (724, 0)))
    display.update(word_builder('<' + str(me.money).rjust(7), 772, 45))


def sell(me):
    """
    function
    """
    while True:
        clear()
        SCREEN.blit(ITEMS, (10, SIZE[1] - 880))
        word_builder('Which item would', 50, SIZE[1] - 250)
        word_builder('you like to sell?', 50, SIZE[1] - 130)
        display.flip()
        selector = 0
        update_sell(me, selector)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    if selector > 0:
                        selector -= 1
                        update_sell(me, selector)
                    elif me.all_items[0] != me.all_shown[0]:
                        me.shift_all_left()
                        update_sell(me, selector)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    if selector < 2 and selector < len(me.all_shown) - 1:
                        selector += 1
                        update_sell(me, selector)
                    elif len(me.all_shown) > 3:
                        me.shift_all_right()
                        update_sell(me, selector)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                    return False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                    if me.all_shown[selector].item.name == 'CANCEL':
                        return False
                    else:
                        item = me.all_shown[selector]
                        retval = sell_amount(item)
                        if retval:
                            display.update(write_btm(
                                'Sell ' + item.item.name, 'for <' + str(item.item.sellprice * retval) + '?'))
                            ret = conf()
                            if ret:
                                do_sell(me, item, retval)
                                update_sell(me, selector)
                            else:
                                display.update(
                                    draw.rect(SCREEN, WHITE, [460, SIZE[1] - 830, 700, 490]))
                                update_sell(me, selector)
                        else:
                            display.update(
                                draw.rect(SCREEN, WHITE, [460, SIZE[1] - 830, 700, 490]))
                            update_sell(me, selector)
                        return False
            sleep(.1)


def using(me):
    """
    function
    """
    while True:
        clear()
        SCREEN.blit(ITEMS, (10, SIZE[1] - 880))
        word_builder('Which item would', 50, SIZE[1] - 250)
        word_builder('you like to use?', 50, SIZE[1] - 130)
        display.flip()
        selector = 0
        update_using(me, selector)
        pygame.key.set_repeat(100, 50)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    if selector > 0:
                        selector -= 1
                        update_using(me, selector)
                    elif me.usable[0] != me.usable_items[0]:
                        me.shift_usable_left()
                        update_using(me, selector)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    if selector < 2 and selector < len(me.usable_items) - 1:
                        selector += 1
                        update_using(me, selector)
                    elif len(me.usable_items) > 3:
                        me.shift_usable_right()
                        update_using(me, selector)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                    return False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                    if me.usable_items[selector].item.name == 'CANCEL':
                        return False
                    else:
                        retval = usable_on(me, me.usable_items[selector])
                        if retval > -1:
                            use(me, me.usable_items[selector], me.pkmn[retval])
                        return False
            sleep(.1)


def shop_choice():
    """
    function
    """
    display.update(SCREEN.blit(SHOP_CHOICE, (10, 10)))
    select = 0
    pygame.event.clear()
    shop_selecting(select)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                if select < 3:
                    select += 1
                    shop_selecting(select)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                if select > 0:
                    select -= 1
                    shop_selecting(select)
            if event.type == pygame.KEYDOWN and ((event.key == pygame.K_z and select == 3) or event.key == pygame.K_x):
                return -1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                return select


def conf():
    """
    function
    """
    display.update(draw.rect(
        SCREEN, WHITE, [3, 407, CONF.get_width() + 14, CONF.get_height() + 15]))
    display.update(SCREEN.blit(CONF, (10, 415)))
    select = 0
    pygame.event.clear()
    selecting(select)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                if select == 0:
                    select = 1
                    selecting(select)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                if select == 1:
                    select = 0
                    selecting(select)
            if event.type == pygame.KEYDOWN and ((event.key == pygame.K_z and select == 1) or event.key == pygame.K_x):
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                return True
        sleep(.02)


def do_purchase(me, item, retval):
    """
    function
    """
    if me.money < item.buyprice * retval:
        display.update(write_btm("You don't have", 'enough money'))
        wait_for_button()
        display.update(
            draw.rect(SCREEN, WHITE, [460, SIZE[1] - 830, 700, 490]))
    else:
        me.money -= item.buyprice * retval
        display.update(write_btm('Here you are!', 'Thank you!'))
        try:
            o = OwnedItem.query.filter(OwnedItem.item_id == item.id) \
                               .filter(OwnedItem.owner == me).one()
            o.count += retval
            db.commit()
        except NoResultFound:
            tmp = OwnedItem(item, me, retval)
            db.add(tmp)
            db.commit()
            if tmp.item.battle:
                me.battle.insert(-1, tmp)
                me.shownitems = me.battle[:4]
            else:
                me.usable.insert(-1, tmp)
                me.usable_items = me.usable[:4]
            me.all_items.insert(-1, tmp)
            me.all_shown = me.all_items[:4]
        wait_for_button()
        clear()
        word_builder('Take your time.', 50, SIZE[1] - 250)
        SCREEN.blit(ITEMS, (10, SIZE[1] - 880))
        draw_money(me)
        display.flip()


def buy(me, shopp):
    """
    function
    """
    clear()
    word_builder('Take your time.', 50, SIZE[1] - 250)
    SCREEN.blit(ITEMS, (10, SIZE[1] - 880))
    draw_money(me)
    display.flip()
    selector = 0
    update_shop(shopp, selector)
    pygame.key.set_repeat(100, 50)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                if selector > 0:
                    selector -= 1
                    update_shop(shopp, selector)
                elif shopp.items[0] != shopp.shownitems[0]:
                    shopp.shift_items_left()
                    update_shop(shopp, selector)
                pygame.time.wait(10)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                if selector < 2 and selector < len(shopp.shownitems) - 1:
                    selector += 1
                    update_shop(shopp, selector)
                elif len(shopp.shownitems) > 3:
                    shopp.shift_items_right()
                    update_shop(shopp, selector)
                pygame.time.wait(10)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                item = shopp.shownitems[selector]
                if item.name != 'CANCEL':
                    retval = amount(item)
                    if retval:
                        display.update(
                            write_btm(item.name + '?', 'That will be'))
                        wait_for_button()
                        display.update(
                            write_btm('That will be', '<' + str(item.buyprice * retval) + '. OK?'))
                        ret = conf()
                        if ret:
                            do_purchase(me, item, retval)
                            update_shop(shopp, selector)
                        else:
                            display.update(
                                draw.rect(SCREEN, WHITE, [460, SIZE[1] - 830, 700, 490]))
                            update_shop(shopp, selector)

                    else:
                        display.update(
                            draw.rect(SCREEN, WHITE, [460, SIZE[1] - 830, 700, 490]))
                        update_shop(shopp, selector)
                else:
                    return False


def shop(me):
    """
    function
    """
    shopp = shoppe()
    SHOP.play()
    while True:
        clear()
        draw_money(me)
        write_btm('Hi there!', 'May I help you?')
        display.flip()
        retval = shop_choice()

        if retval == 0:
            buy(me, shopp)
        elif retval == 1:
            sell(me)
        elif retval == 2:
            using(me)
        elif retval == -1:
            SHOP.stop()
            return False


def draw_choose_pkmn(me, opp, mode, oppdeath=False, mydeath=False):
    """
    function
    """
    clear()
    offset = 0
    dirty = []
    for mon in me.pkmn:
        draw_pkmn_choice(mon, offset)
        offset += 1
    word_builder('>', 0, 110 * me.get_current_index() + 60)
    write_btm('Bring out which', 'POK~MON?')
    pygame.display.flip()
    pygame.event.clear()
    select = me.get_current_index()
    count = 0
    tmp = True
    while True:
        if r.get('lock'):
            raise OppMoveOccuring
        if mode == 'pong':
            if count == 10:
                select += 1
                update_choose(select - 1, select, me)
                tmp = True
            if count == 20:
                clear()
                pygame.display.flip()
                draw_all_opp(opp.current)
                me.set_current(select)
                sleep(2)
                pop_ball(me.current.name)
                draw_all_me(me.current)
                return select

        else:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    if select > 0:
                        select -= 1
                        update_choose(select + 1, select, me)
                        count = 1
                        tmp = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    if select < len(me.pkmn) - 1:
                        select += 1
                        update_choose(select - 1, select, me)
                        count = 1
                        tmp = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                    if select == me.get_current_index():
                        display.update(
                            write_btm(me.current.name, 'is already out!'))
                        wait_for_button()
                        display.update(
                            write_btm('Bring out which', 'POK~MON?'))
                    elif me.pkmn[select].hp == 0:
                        # TODO can't bring out fainted
                        pass
                    else:
                        if mode == 'battle':
                            if mydeath:
                                return select
                            if r.lock('lock').acquire():
                                raise MyMoveOccuring('swap', str(select))
                            else:
                                raise OppMoveOccuring
                        clear()
                        pygame.display.flip()
                        if not oppdeath:
                            draw_all_opp(opp.current)
                        else:
                            draw_all_me(me.current)
                            return_my_pokemon(me)
                        if mydeath or oppdeath:
                            me.set_current(select)
                            me.used.add(me.current)
                            pop_ball(me.current.name)
                            draw_all_me(me.current)
                            sleep(.5)
                        return select
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                    if not mydeath:
                        clear()
                        draw_all_opp(opp.current)
                        return -1

        sleep(.1)
        con1 = count % 2 == 0 and me.pkmn[
            select].hp > me.pkmn[select].maxhp / 2
        con2 = count % 5 == 0 and me.pkmn[
            select].hp <= me.pkmn[select].maxhp / 2
        if con1 or con2:
            dirty = draw.rect(SCREEN, WHITE, [60, select * 110 + 15, 101, 101])
            if tmp:
                SCREEN.blit(me.pkmn[select].sprite2, (60, select * 110 + 15))
            else:
                SCREEN.blit(me.pkmn[select].sprite1, (60, select * 110 + 15))
            display.update(dirty)
            tmp = not tmp

        count += 1


def wait_for_opp_move(opp, mymove, mode, socket):
    """
    function
    """
    if mode == 'random' or mode == 'wild':
        # TODO PP check
        return ['move', randint(0, len(opp.current.moves) - 1)]
    else:
        socket.send(json.dumps(mymove))
        display.update(write_btm('Waiting for opponenet'))
        x = json.loads(socket.recv())
        return x
        # TODO OPP wait


def wait_for_opp_next_mon(socket):
    """
    function
    """
    display.update(write_btm('Waiting for opponenet'))
    return int(socket.recv())


def run_opp_move(me, opp, move, first):
    """
    function
    """
    opp.current.attempt_move(False)
    retval = do_move(opp.current, me.current, move, 'tmp', False, first)
    opp.current.do_status(me.current, False)
    return retval


def change_pokemon(me, opp, mode):
    """
    function
    """
    dirty = []
    dirty.append(draw.rect(SCREEN, WHITE, [0, 403, 375, 280]))
    dirty.extend(write_btm('Will ' + me.name, 'change POK~MON?'))
    SCREEN.blit(CONF, (10, 410))
    display.update(dirty)
    select = 0
    pygame.event.clear()
    while True:
        # TODO wait for chaning pkmn in battle.  Check for token?
        sleep(.1)
        selecting(select)
        if mode == 'pong':
            sleep(1)
            selecting(1)
            sleep(1)
            dirty.append(draw.rect(SCREEN, WHITE, [0, 403, 375, 280]))
            dirty.extend(draw_my_pkmn_sprite(me.current))
            display.update(dirty)
            return False
        else:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    if select == 0:
                        select = 1
                if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    if select == 1:
                        select = 0
                if event.type == pygame.KEYDOWN and ((event.key == pygame.K_z and select == 1) or event.key == pygame.K_x):
                    dirty = []
                    dirty.append(draw.rect(SCREEN, WHITE, [0, 403, 375, 280]))
                    dirty.extend(draw_my_pkmn_sprite(me.current))
                    display.update(dirty)
                    return False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                    draw_choose_pkmn(me, opp, mode, oppdeath=True)
                    clear()
                    display.flip()
                    draw_all_me(me.current)
                    return True


def run_attack(me, mode):
    """
    function
    """
    attacking(me)
    select = 0
    pygame.event.clear()
    while True:
        if r.get('lock'):
            raise OppMoveOccuring
        if me.current.pp_left():
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    if select < len(me.current.moves) - 1:
                        select += 1
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    if select > 0:
                        select -= 1
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                    clean_me_up(me)
                    draw_choice(0)
                    return False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                    if mode != 'pong':
                        clean_me_up(me)
                        if usable_move(me.current.moves[select], mode):
                            if mode == 'battle':
                                if r.lock('lock').acquire():
                                    raise MyMoveOccuring('move', str(select))
                                else:
                                    raise OppMoveOccuring
                            return me.current.moves[select]
                        else:
                            attacking(me)
                    else:
                        return me.current.moves[select]

                update_attacking(me, select)
        else:
            # TODO struggle text
            return me.struggle()


def draw_move(move):
    """
    function
    """
    retval = []
    retval.append(
        word_builder(move.type_.type_.upper() + '/', 116, SIZE[1] - 470))
    retval.append(
        word_builder(str(move.pp) + '/' + str(move.maxpp), 284, SIZE[1] - 410))
    return retval


def lost(me, mode):
    """
    function
    """
    display.update(write_btm(me.name + ' is out of', 'useable POK~MON!'))
    if mode != 'pong':
        wait_for_button()
    else:
        sleep(2)
    display.update(write_btm(me.name + ' blacked', 'out!'))
    if mode != 'pong':
        wait_for_button()
    else:
        sleep(2)
    if mode == 'battle':
        cash = min(me.money, opp.money) / 2
        display.update(write_btm(me.name + ' lost', '<' + str(cash)))
        me.money -= cash
        db.commit()
    SCREEN.fill(GREY)
    display.flip()
    sleep(.5)
    SCREEN.fill(BLACK)
    display.flip()
    sleep(1)


def win(me, opp, mode):
    """
    function
    """
    if mode != 'wild':
        display.update(write_btm(me.name + ' defeated', opp.name + '!'))
    else:
        display.update(
            write_btm(me.name + ' defeated', opp.current.name + '!'))
    if mode != 'pong':
        wait_for_button()
    else:
        sleep(2)
    if mode == 'random':
        display.update(write_btm(me.name + ' gained', '<' + str(opp.money)))
        me.money += opp.money
        db.commit()
        wait_for_button()
    elif mode == 'battle':
        cash = min(me.money, opp.money) / 2
        display.update(write_btm(me.name + ' gained', '<' + str(cash)))
        me.money += cash
        db.commit()
        wait_for_button()




def run_pong(me, opp):
    """
    function
    """
    # TODO switch client order. or use a redis queue
    # TODO set tablenames with client
    draw_choice(0)
    while True:
        if opp.num_fainted() < int(r.get(opp.name) or 0):
            attacking(me)
            sleep(2)
            clean_me_up(me)
            do_move(
                me.current, opp.current, me.current.moves[0], 'pong', True, True)
            return 0
        elif me.num_fainted() < int(r.get(me.name) or 0):
            sleep(2)
            do_move(
                opp.current, me.current, opp.current.moves[0], 'pong', False, True)
            return 1
        sleep(.1)


def battle_logic(me, opp, move, my):
    """
    function
    """
    if move[0] == 'move':
        if my:
            run_move(me, opp, me.current.moves[int(move[1])], my)
            if not opp.current.alive():
                return 0
        else:
            run_opp_move(me, opp, opp.current.moves[int(move[1])], my)
            if not me.current.alive():
                return 1
    if move[0] == 'swap':
        if my:
            return_my_pokemon(me)
            me.set_current(int(move[1]))
            pop_ball(me.current.name)
            draw_all_me(me.current)
        else:
            run_opp_swap(opp, move[1])
    return 4


def run_game(me, opp, mode, socket):
    """
    function
    """
    selector = 0
    pygame.event.clear()
    if mode == 'pong':
        return run_pong(me, opp)
    while True:
        if r.get('lock'):
            raise OppMoveOccuring
        for ev in pygame.event.get():
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_RIGHT:
                if selector == 0 or selector == 1:
                    selector += 2
            elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_LEFT:
                if selector == 2 or selector == 3:
                    selector -= 2
            elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_DOWN:
                if selector == 0 or selector == 2:
                    selector += 1
            elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_UP:
                if selector == 1 or selector == 3:
                    selector -= 1
            elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_z:
                if selector == 0:
                    if me.current.controllable:
                        my_move = run_attack(me, mode)
                    else:
                        my_move = me.current.lastmove
                    if my_move:
                        tmp, opp_move = wait_for_opp_move(
                            opp, ['move', me.current.moves.index(my_move)], mode, socket)
                        clean_me_up(me)
                        if tmp == 'move':
                            opp_move = opp.current.moves[opp_move]
                            if my_move.name == 'Quick Attack' != opp_move.name == 'Quick Attack':
                                if my_move.name == 'Quick Attack':
                                    run_move(me, opp, my_move)
                                    if not opp.current.alive():
                                        return 0
                                    if me.current.alive():
                                        run_opp_move(me, opp, opp_move, False)
                                    else:
                                        return 1
                                else:
                                    run_opp_move(me, opp, opp_move, True)
                                    if not me.current.alive():
                                        return 1
                                    if opp.current.alive():
                                        run_move(me, opp, my_move)
                                    else:
                                        return 0
                            else:
                                if me.current.calc_speed() > opp.current.calc_speed():

                                    run_move(me, opp, my_move, True)
                                    if not opp.current.alive():
                                        return 0
                                    if me.current.alive():
                                        run_opp_move(me, opp, opp_move, False)
                                    else:
                                        return 1
                                else:
                                    run_opp_move(me, opp, opp_move, True)
                                    if not me.current.alive():
                                        return 1
                                    if opp.current.alive():
                                        run_move(me, opp, my_move, False)
                                    else:
                                        return 0
                        elif tmp == 'swap':
                            if my_move.name == 'Quick Attack':
                                run_move(me, opp, my_move, True)
                                if not opp.current.alive():
                                    return 0
                                run_opp_swap(opp, opp_move)
                            else:
                                if me.current.calc_speed() > opp.current.calc_speed():
                                    run_move(me, opp, my_move, True)
                                    if not opp.current.alive():
                                        return 0
                                    run_opp_swap(opp, opp_move)
                                else:
                                    run_opp_swap(opp, opp_move)
                                    run_move(me, opp, my_move, False)
                                    if not opp.current.alive():
                                        return 0

                        return 4
                if selector == 1:
                    select = draw_choose_items(me)
                    clear()
                    pygame.display.flip()
                    draw_all_opp(opp.current)
                    draw_all_me(me.current)
                    if select > -1:
                        item = me.shownitems[select]
                        if item.item.name != 'CANCEL':
                            item.use(me)
                            if item.item.name[-4:].upper() == 'BALL':
                                display.update(
                                    write_btm(me.name + ' used', item.item.name.upper()))
                                ret = catchem(
                                    item.item.name.upper(), opp.current, me, opp)
                                if ret:
                                    return 5
                                else:
                                    tmp, opp_move = wait_for_opp_move(
                                        opp, ['swap', select], mode, socket)
                                    draw_all_me(me.current)
                                    if tmp == 'move':
                                        opp_move = opp.current.moves[opp_move]
                                        run_opp_move(me, opp, opp_move, True)
                                        if not me.current.alive:
                                            return 1
                                    draw_all_me(me.current)
                                    clearbtm()
                                    selector = 0
                    draw_choice(0)

                if selector == 2:
                    select = draw_choose_pkmn(me, opp, mode)
                    clear()
                    pygame.display.flip()
                    draw_all_opp(opp.current)
                    if select > -1:
                        tmp, opp_move = wait_for_opp_move(
                            opp, ['swap', select], mode, socket)
                        draw_all_me(me.current)
                        if tmp == 'move':
                            opp_move = opp.current.moves[opp_move]
                            if opp_move.name == 'Quick Attack' or opp.current.calc_speed() > me.current.calc_speed():
                                run_opp_move(me, opp, opp_move, True)
                                if not me.current.alive:
                                    return 1
                                return_my_pokemon(me)
                                me.set_current(select)
                                pop_ball(me.current.name)
                                draw_all_me(me.current)
                            else:
                                return_my_pokemon(me)
                                me.set_current(select)
                                pop_ball(me.current.name)
                                draw_all_me(me.current)
                                run_opp_move(me, opp, opp_move, True)
                                if not me.current.alive:
                                    return 1
                        elif tmp == 'swap':
                            if opp.current.calc_speed() > me.current.calc_speed():
                                run_opp_swap(opp, opp_move)
                                return_my_pokemon(me)
                                me.set_current(select)
                                pop_ball(me.current.name)
                                draw_all_me(me.current)
                            else:
                                return_my_pokemon(me)
                                me.set_current(select)
                                pop_ball(me.current.name)
                                draw_all_me(me.current)
                                run_opp_swap(opp, opp_move)
                        me.used.add(me.current)
                    draw_all_me(me.current)
                    clearbtm()
                    selector = 0
                    draw_choice(0)
                if selector == 3:
                    if mode != 'wild':
                        display.update(
                            write_btm("Can't escape a", "trainer battle"))
                        sleep(2)
                        clearbtm()
                        selector = 0
                        draw_choice(0)
                    else:
                        F = (me.current.calc_speed() * 32) / \
                            (opp.current.calc_speed() / 4) + \
                            30 * me.current.fleecount
                        if randint(0, 255) < F:
                            display.update(write_btm("Got away safely!"))
                            wait_for_button()
                            return 3
                        else:
                            tmp, opp_move = wait_for_opp_move(
                                opp, False, mode, socket)
                            opp_move = opp.current.moves[opp_move]
                            display.update(write_btm("Failed to escape!"))
                            wait_for_button()
                            run_opp_move(me, opp, opp_move, False)
                            if not me.current.alive():
                                return 1
                            clearbtm()
                            selector = 0
                            draw_choice(0)
            update_choice(selector)
    sleep(.1)


from pokepong.domove import do_move, usable_move
from pokepong.models import Pokemon, Owned, tmpMove, OwnedItem, shoppe, TmHm
