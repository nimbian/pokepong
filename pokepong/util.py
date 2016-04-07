from pygame.image import load
import json
import random
import sys
import zmq
IMAGES = 'images/'

HIGH_ARC = [(101, 302), (234, 120), (402, -26), (420, -54), (460, -100), (490, -110),
            (520, -100), (580, -80), (640, -60), (700, -5), (760, 50)]
LOW_ARC = []


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
