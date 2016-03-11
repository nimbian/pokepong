from time import sleep
sleep(1)
from logic import *
from classes import trainer
from sqlite3 import connect
conn = connect('shawn')
c = conn.cursor()
from pygame.image import save
import numpy as np
from util import loadalphaimg



def body_slam():
    pixels = pygame.surfarray.pixels3d(SCREEN)
    pixels ^= 2 ** 32 -1
    pygame.display.flip()
    sleep(5)
    pixels ^= 2 ** 32 -1
    pygame.display.flip()
    sleep(.1)
    pixels ^= 2 ** 32 -1
    pygame.display.flip()
    sleep(.1)
    pixels ^= 2 ** 32 -1
    pygame.display.flip()
    sleep(.1)

def barrier(me):
    barrier = loadalphaimg('moves/barrier.png')
    for i in range(6):
        x = SCREEN.blit(barrier, (525,292))
        display.update(x)
        sleep(.2)
        display.update(pygame.draw.rect(SCREEN, WHITE, x))
        draw_all_me(me.current)
        sleep(.2)


def beam(me,opp):
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



def green():
    #tint green
    pixels = pygame.surfarray.pixels3d(SCREEN)
    pixels[:,:,0] |= 77
    pixels[:,:,1] |= 255
    pixels[:,:,2] |= 77
    pygame.display.flip()

    sleep(5)



def invertcolor():
    pixels = pygame.surfarray.pixels2d(SCREEN)
    pixels = (pixels ^ 2 ** 32 -1) & 5111629


def pics():
    for i in range(1,255):
        pixels = pygame.surfarray.array3d(SCREEN)
        pixels ^= i
        pygame.display.flip()
        sleep(.1)
        pixels ^= i
        pygame.display.flip()

if __name__ == '__main__':
    clear()
    display.flip()
    mypkmn = [91]
    opppkmn = [34]
    myname = 'Player1'
    oppname = 'Player2'
    tmp = []
    for i in mypkmn:
        x = c.execute("SELECT * from ownedpkmn where rowid = '{0}'".format(i)).fetchone()
        tmp.append([x[0],x[1], [x[2],x[3],x[4],x[5]], x[6], [x[7],x[8],x[9],x[10],x[11]],
                [x[12],x[13],x[14],x[15]], x[16], [x[17],x[18],x[19],x[20]]])
    tmp2 = []
    for i in opppkmn:
        x = c.execute("SELECT * from ownedpkmn where rowid = '{0}'".format(i)).fetchone()
        tmp2 .append([x[0],x[1], [x[2],x[3],x[4],x[5]], x[6], [x[7],x[8],x[9],x[10],x[11]],
                 [x[12],x[13],x[14],x[15]], x[16], [x[17],x[18],x[19],x[20]]])
    mypkmn = build_team(tmp, me = True)
    opppkmn = build_team(tmp2)
    me = trainer(myname, mypkmn)
    opp = trainer(oppname, opppkmn)
    draw_choice(0)
    draw_all_me(me.current)
    draw_all_opp(opp.current)
    sleep(2)
    pics()

