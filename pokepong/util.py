from pygame.image import load
from pygame import display
import json
from sqlite3 import connect
import random
import sys
import zmq
images = 'images/'

def send_move(move, socket):
    socket.send(json.dumps(move.args))
    print 'waiting for response'
    socket.recv()

def recv_move(socket):
    move = json.loads(socket.recv())
    socket.send('')
    return move


class MyMoveOccuring(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)

class OppMoveOccuring(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)

def loadalphaimg(img):
    return loadimg(img).convert_alpha()

def loadimg(img):
    return load(images + img)

def alphabet():
    alpha_dict = dict()
    alph = [' ','!','<','&',"'",'(',')','+',',','_','.','/','0','1','2','3','4','5','6','7','8','9',':',';','?','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','[',']','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','#','$','-','=','+','>','^','%','~','*','']
    c = 0
    for i in range(47,1168,140):
        for j in range(16,791,86):
            alpha_dict[alph[c]] = (j,i,54,60)
            c+=1
    return alpha_dict

def set_seed(seed):
    random.seed(seed)

def get_random():
    return random.random()

def choice(items):
    return random.choice(items)

def randint(low, high):
    return random.randint(low, high)

def send_team(myid, mypkmnlist, socket, client):
    if client:
        seed = random.randint(0,sys.maxint)
        set_seed(seed)
        socket.send(json.dumps([myid, mypkmnlist, seed]))
    else:
        socket.send(json.dumps([myid, mypkmnlist]))

def get_team(socket, client):
    if client:
        return json.loads(socket.recv(zmq.NOBLOCK))
    else:
        tmp = json.loads(socket.recv(zmq.NOBLOCK))
        set_seed(tmp[2])
        return tmp[:2]

