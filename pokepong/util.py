from pygame.image import load
from pygame import display, draw
import pygame
import json
import random
import sys
import zmq
from math import floor
from redis import StrictRedis
from time import sleep
from pygame.mixer import Sound
pygame.mixer.init()

CLIENT = False
r = StrictRedis(host='127.0.0.1')

SIZE = (1280, 1024)
WHITE = (253, 236, 254)
GREEN = (63, 156, 79)
YELLOW = (255, 228, 104)
RED = (209, 71, 40)
GREY = (108, 108, 108)
BLACK = (0, 0, 0)
IMAGES = 'images/'
MYHP_RECT = [SIZE[0] - 532, SIZE[1] - 486, 399, 14]
OPPHP_RECT = [227, 141, 399, 15]

HIGH_ARC = [(101, 302), (234, 120), (402, -26), (420, -54), (460, -100), (490, -110),
            (520, -100), (580, -80), (640, -60), (700, -5), (760, 50)]
LOW_ARC = []

PINS = {'BROCK': [1,2,3,4],'MISTY': [1,2,3,4],'Lt. SURGE': [1,2,3,4],
        'ERIKA': [1,2,3,4],'KOGA': [1,2,3,4],'SABRINA': [1,2,3,4],
        'BLAINE': [1,2,3,4],'GIOVANNI': [1,2,3,4],'LORELEI': [1,2,3,4],
        'BRUNO': [1,2,3,4],'AGATHA': [1,2,3,4],'LANCE': [1,2,3,4]}

GYMS = {'PEWTER CITY': ['BROCK',[152,153]], 'CERULEAN CITY': ['MISTY',[154,155]],
        'VERMILION CITY': ['Lt. SURGE',[156,157,158]], 'CELADON CITY': ['ERIKA',[159,160,161]],
        'FUCHSIA CITY': ['KOGA',[166,167,168,169]], 'SAFFRON CITY': ['SABRINA',[162,163,164,165]],
        'CINNABAR ISLAND': ['BLAINE',[170,171,172,173]], 'VIRIDIAN CITY': ['GIOVANNI',[174,175,176,177,178]],
        'ELITE 4-1': ['LORELEI',[179,180,181,182,183]], 'ELITE 4-2': ['BRUNO',[184,185,186,187,188]],
        'ELITE 4-3': ['AGATHA',[189,190,191,192,193]], 'ELITE 4-4': ['LANCE',[194,195,196,197,198]],
        'CHAMPION': None}


def set_client(tmp):
    global CLIENT
    CLIENT = tmp

def get_client():
    global CLIENT
    return CLIENT

def clearbtm():
    """
    function
    """
    draw.rect(SCREEN, WHITE, [0, SIZE[1] - 340, SIZE[0], 340])

def word_builder(word, start_x, start_y):
    """
    function
    """
    x = start_x
    draw.rect(SCREEN, WHITE, [x, start_y, len(word) * 56, 60])
    for l in word:
        SCREEN.blit(ALPHA, (start_x, start_y), ALPHA_DICT[l])
        start_x += 56
    return [x, start_y, len(word) * 56, 60]

def write_btm(*args):
    """
    function
    """
    clearbtm()
    retval = []
    retval.append(SCREEN.blit(BTM, BTM_TUPLE))
    retval.append(word_builder(args[0], 50, SIZE[1] - 250))
    try:
        retval.append(word_builder(args[1], 50, SIZE[1] - 130))
    except IndexError:
        pass
    return retval

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

def send_move(move, socket):
    """
    function
    """
    socket.send(json.dumps(move.args))
    print 'waiting for response'
    socket.recv()


def recv_move(socket):
    """
    function
    """
    move = json.loads(socket.recv())
    socket.send('')
    return move


class MyMoveOccuring(Exception):
    """
    class
    """

    def __init__(self, *args, **kwargs):
        """
        function
        """
        Exception.__init__(self, *args, **kwargs)


class OppMoveOccuring(Exception):
    """
    class
    """

    def __init__(self, *args, **kwargs):
        """
        function
        """
        Exception.__init__(self, *args, **kwargs)


def loadalphaimg(img):
    """
    function
    """
    return loadimg(img).convert_alpha()


def loadimg(img):
    """
    function
    """
    return load(IMAGES + img)


def alphabet():
    """
    function
    """
    alpha_dict = dict()
    alph = [' ', '!', '<', '&', "'", '(', ')', '+', ',', '_', '.', '/', '0',
            '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '?', 'A',
            'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
            'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[',
            ']', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
            'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
            'z', '#', '$', '-', '=', '+', '>', '^', '%', '~', '*', '']
    count = 0
    for i in range(47, 1168, 140):
        for j in range(16, 791, 86):
            alpha_dict[alph[count]] = (j, i, 54, 60)
            count += 1
    return alpha_dict


def set_seed(seed):
    """
    function
    """
    random.seed(seed)


def get_random():
    """
    function
    """
    return random.random()


def choice(items):
    """
    function
    """
    return random.choice(items)


def randint(low, high):
    """
    function
    """
    return random.randint(low, high)


def send_team(myid, mypkmnlist, socket, client):
    """
    function
    """
    if client:
        seed = random.randint(0, sys.maxint)
        set_seed(seed)
        socket.send(json.dumps([myid, mypkmnlist, seed]))
    else:
        socket.send(json.dumps([myid, mypkmnlist]))


def get_team(socket, client):
    """
    function
    """
    if client:
        return json.loads(socket.recv(zmq.NOBLOCK))
    else:
        tmp = json.loads(socket.recv(zmq.NOBLOCK))
        set_seed(tmp[2])
        return tmp[:2]

def wait_for_button():
    #TODO only wait on mode != pong
    """
    function
    """
    pygame.event.clear()
    c = 1
    tmp = False
    display.update(word_builder('^',SIZE[0]-120, SIZE[1]-120))
    while True:
        if r.get('lock'):
            raise OppMoveOccuring
        for event_ in pygame.event.get():
            if event_.type == pygame.KEYDOWN:
                return
        if c % 4 == 0:
            if tmp:
                display.update(word_builder('^',SIZE[0]-120, SIZE[1]-120))
            else:
                display.update(word_builder(' ',SIZE[0]-120, SIZE[1]-120))
            tmp = not tmp
            c = 1
        else:
            c += 1
        sleep(.1)


SCREEN = display.set_mode(SIZE)
ALPHA = loadalphaimg('alphafull.png')
BTM = loadalphaimg('btmclean.png')
BTM_TUPLE = (10, SIZE[1] - 340)
MYHP = loadalphaimg('myhp.png')
OPPHP = loadalphaimg('opphp.png')

ALPHA_DICT = alphabet()
OPPHP_RECT = [227, 141, 399, 15]
MYHPBAR_RECT = [
    SIZE[0] - 700, SIZE[1] - 505, MYHP.get_width(), MYHP.get_height()]
