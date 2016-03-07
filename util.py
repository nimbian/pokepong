from pygame.image import load
from pygame import display
import json
from sqlite3 import connect
import random
import sys
images = 'images/'


def loadalphaimg(img):
    return loadimg(img).convert_alpha()

def loadimg(img):
    return load(images + img)

def alphabet():
    alpha_dict = dict()
    alph = [' ','!','#','&',"'",'(',')','+',',','_','.','/','0','1','2','3','4','5','6','7','8','9',':',';','?','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','[',']','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','#','$','-','=','+','>','^','%','~','*','']
    c = 0
    for i in range(47,1168,140):
        for j in range(16,791,86):
            alpha_dict[alph[c]] = (j,i,54,60)
            c+=1
    return alpha_dict

def send_teams(mypkmn, opppkmn, myname, oppname, socket):
    conn = connect('shawn')
    c = conn.cursor()
    tmp = []
    for i in mypkmn:
        x = c.execute("SELECT * from ownedpkmn where rowid = '{0}'".format(i)).fetchone()
        tmp.append([x[1], [x[2],x[3],x[4],x[5]], x[6], [x[7],x[8],x[9],x[10],x[11]], 
                [x[12],x[13],x[14],x[15]], x[16], [x[17],x[18],x[19],x[20]]])

    tmp2 = []
    for i in opppkmn:
        x = c.execute("SELECT * from ownedpkmn where rowid = '{0}'".format(i)).fetchone()
        tmp2 .append([x[1], [x[2],x[3],x[4],x[5]], x[6], [x[7],x[8],x[9],x[10],x[11]], 
                 [x[12],x[13],x[14],x[15]], x[16], [x[17],x[18],x[19],x[20]]])

    seed = random.randint(0,sys.maxint)
    socket.send(json.dumps([tmp2, tmp, oppname, myname, seed]))
    return [tmp, tmp2, myname, oppname, seed]

def get_teams(socket):
    return json.loads(socket.recv())

def set_seed(seed):
    random.seed(seed)

def get_random():
    return random.random()

def choice(items):
    return random.choice(items)

def randint(low, high):
    return random.randint(low, high)