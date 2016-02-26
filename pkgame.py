import pygame
from random import choice
from time import sleep
from randbattle import pokemon
from math import ceil
from sqlite3 import connect

size = (1280,1024)
WHITE = (253, 236, 254)
GREEN = (63,156,79)
YELLOW = (255,228,104)
RED = (209,71,40)
GREY = (108,108,108)
BLACK = (0,0,0)
screen = pygame.display.set_mode(size)
alpha_dict = dict()
images = '/home/brian.j.ramsel/newgame/images/'
btm = pygame.image.load(images + 'btmclean.png').convert_alpha()
myhp = pygame.image.load(images + 'myhp.png').convert_alpha()
opphp = pygame.image.load(images + 'opphp.png').convert_alpha()
movechoice = pygame.image.load(images + 'choiceclean.png').convert_alpha()
attack = pygame.image.load(images + 'attack.png').convert_alpha()
alpha = pygame.image.load(images + 'alphafull.png').convert_alpha()
hpbar = pygame.image.load(images + 'hpbar.png').convert_alpha()
mon1 = pygame.image.load(images + 'mon1.png').convert_alpha()
mon2 = pygame.image.load(images + 'mon2.png').convert_alpha()
mybar = pygame.image.load(images + 'mybar.png').convert_alpha()
oppbar = pygame.image.load(images + 'oppbar.png').convert_alpha()
alive = pygame.image.load(images + 'alive.png').convert_alpha()
fainted = pygame.image.load(images + 'fainted.png').convert_alpha()
conf = pygame.image.load(images + 'conf.png').convert_alpha()
logo = pygame.image.load(images + 'logo.png').convert_alpha()
trainer = pygame.image.load(images + 'trainer.png').convert_alpha()
trainerback = pygame.image.load(images + 'trainerback.png').convert_alpha()
poke1 = pygame.image.load(images + 'poke1.png').convert_alpha()
poke2 = pygame.image.load(images + 'poke2.png').convert_alpha()

left_off = 10
bottom_off = size[1]-340
btm_tuple = (left_off, bottom_off)

c = 0
alph = [' ','!','#','&',"'",'(',')','+',',','_','.','/','0','1','2','3','4','5','6','7','8','9',':',';','?','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','[',']','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','#','$','-','=','+','>','^','%','~','','']
for i in range(47,1168,140):
    for j in range(16,791,86):
        alpha_dict[alph[c]] = (j,i,54,60)
        c+=1
def clear():
    screen.fill(WHITE)

def writebtm(*args):
    clearbtm()
    screen.blit(btm, btm_tuple)
    word_builder(args[0], 50, size[1]-250)
    try:
        word_builder(args[1], 50, size[1]-130)
    except:
        pass
    pygame.display.flip()

def drawmyhpbar():
    screen.blit(myhp,(size[0] - 700, size[1]-505))
    word_builder('%50', size[0] - 405, size[1]-565)


def drawmybar(team):
    pygame.draw.rect(screen, WHITE, [size[0] - 700, size[1]-505, 602, 104])
    screen.blit(mybar, (size[0]-700, size[1]-442))
    offset = 0
    for mon in team:
        if mon.hp == 0:
            screen.blit(fainted, (size[0]-575 + offset * 65, size[1]-430))
        else:
            screen.blit(alive, (size[0]-575 + offset * 65, size[1]-430))
        offset += 1

    for i in range(offset, 6):
        screen.blit(alive, (size[0]-500 + i * 65, size[1]-430))

def drawoppbar(team):
    pygame.draw.rect(screen, WHITE, [80, 120, 602, 91])
    screen.blit(oppbar,(80, 120))
    offset = 0
    for mon in team[::-1]:
        if mon.hp == 0:
            screen.blit(fainted, (180 + offset * 65, 132))
        else:
            screen.blit(alive, (180 + offset * 65, 132))
        offset += 1

    for i in range(offset, 6):
        screen.blit(alive, (180 + i * 65, 132))




def drawmyhp(pkmn):
    maxhp = pkmn.maxhp
    hp = pkmn.hp
    bar_len = hp/float(maxhp)*399
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
    pygame.draw.rect(screen, WHITE, [size[0]-532, size[1]-486, 399, 14])
    pygame.draw.rect(screen, color, [size[0]-532, size[1]-486, bar_len, 14])
    pygame.display.update(size[0]-532, size[1]-486, 399, 14)
    word_builder('{0}/{1}'.format(hp,maxhp), size[0] - 570, size[1]-445)


def drawmypkmn(pkmn):
    pygame.draw.rect(screen, WHITE, [0, size[1]-740,751,410])
    screen.blit(pkmn.img,(59, size[1]-740))
    pygame.display.update(0, size[1]-740,451,392)
    word_builder(pkmn.name.upper(), size[0] - 630, size[1]-625)
    drawmyhp(pkmn)
    drawmyhpbar()

def drawopppkmn(pkmn):
    screen.blit(pkmn.img,(size[0]-500,0))

def drawopphp(pkmn):
    maxhp = pkmn.maxhp
    hp = pkmn.hp
    bar_len = hp/float(maxhp)*399
    if bar_len < 100:
        color = RED
    elif bar_len < 200:
        color = YELLOW
    else:
        color = GREEN
    pygame.draw.rect(screen, WHITE, [227, 141, 399, 14])
    pygame.draw.rect(screen, color, [227, 141, bar_len, 14])
    pygame.display.update(227, 141, 399, 14)
    word_builder(pkmn.name.upper(), 60,1)

def drawoppname(pkmn):
    pygame.draw.rect(screen, WHITE, [80, 120, 602, 91])
    word_builder('%' + str(pkmn.lvl), 230,60)
    screen.blit(opphp,(80, 120))
    pygame.display.update(80,120,602,91)

def drawattack(pkmn,selector):
    clearbtm()
    pygame.draw.rect(screen, WHITE, [0, 442 ,695,300])
    screen.blit(attack, (left_off, bottom_off - 237))
    word_builder(['>',' ',' ',' '][selector] + pkmn.moves[0].name.upper(),300, size[1]-285)
    word_builder([' ','>',' ',' '][selector] + pkmn.moves[1].name.upper(),300, size[1]-225)
    word_builder([' ',' ','>',' '][selector] + pkmn.moves[2].name.upper(),300, size[1]-165)
    word_builder([' ',' ',' ','>'][selector] + pkmn.moves[3].name.upper(),300, size[1]-105)
    word_builder('TYPE/',60, size[1]-530)
    drawmove(pkmn.moves[selector])
    pygame.display.flip()


def drawmove(move):
    word_builder(move.type_.upper() + '/',116, size[1]-470)
    word_builder(str(move.pp) + '/' + str(move.maxpp),284, size[1]-410)


def drawchoice(selector):
    screen.blit(movechoice,btm_tuple)
    word_builder(['>',' ',' ',' '][selector] + 'FIGHT',size[0]-730, size[1]-250)
    word_builder([' ','>',' ',' '][selector] + 'ITEM',size[0]-730, size[1]-130)
    word_builder([' ',' ','>',' '][selector] + '#$',size[0]-350, size[1]-250)
    word_builder([' ',' ',' ','>'][selector] + 'ITEM',size[0]-350, size[1]-130)

def word_builder(word,start_x, start_y):
    x = start_x
    pygame.draw.rect(screen, WHITE, [x, start_y, len(word)*56,60])
    for l in word:
        screen.blit(alpha,(start_x, start_y),alpha_dict[l])
        start_x+=56
    pygame.display.update(x, start_y, len(word)*56,60)

def toptxt(word):
    word_builder(word, 50, size[1]-250)

def btmtxt(word):
    word_builder(word, 50, size[1]-130)

def mypkmnfaint(pkmn):
    diff = pkmn.maxhp / 399.
    for i in range(1,400,2):
        pygame.draw.rect(screen, WHITE, [size[0]-532, size[1]-486, 399, 14])
        if i < 200:
            pygame.draw.rect(screen, GREEN, [size[0]-532, size[1]-486, 399-i, 14])
        elif i < 300:
            pygame.draw.rect(screen, YELLOW, [size[0]-532, size[1]-486, 399-i, 14])
        elif i < 399:
            pygame.draw.rect(screen, RED, [size[0]-532, size[1]-486, 399-i, 14])
        pygame.draw.rect(screen, WHITE, [size[0]-570, size[1]-445, 420, 65])
        drawmyhp(pkmn)
        pygame.display.flip()
    for i in range(1,392,2):
        pygame.draw.rect(screen, WHITE, [59, size[1]-740, 392, 392])
        screen.blit(pkmn.img, (59, size[1]-740 + i), (0,0,392,392-i))
        pygame.display.update([59, size[1]-740 + i + 1, 392,392-i])
    pkmn.sethp(0)
    writebtm(pkmn.name,'fainted!')
    sleep(2)

def clearbtm():
    pygame.draw.rect(screen, WHITE, [0,size[1]-340,size[0],340])


def opppkmnfaint(pkmn):
    for i in range(1,392,2):
        pygame.draw.rect(screen, WHITE, [size[0]-500, 0, 392, 392])
        screen.blit(pkmn.img, (size[0]-500, i), (0,0,392,392-i))
        pygame.display.update([size[0]-500, i,392,392-i])
    pygame.draw.rect(screen, WHITE, [0,0,800,250])
    clearbtm()
    writebtm('Enemy ' + pkmn.name.upper(),'fainted!')
    sleep(2)



def drawmymove(mypkmn, opppkmn, selector):
    clear()
    drawmypkmn(mypkmn)
    drawopppkmn(opppkmn)
    drawoppname(opppkmn)
    drawopphp(opppkmn)
    writebtm(mypkmn.name.upper(),('used {0}'.format(mypkmn.moves[selector].name.upper())))
    drawmyattackanimation('move')

def drawmyattackanimation(move):
    sleep(1)

def drawpickmon(myteam, num):
    clear()
    offset = 0
    for mon in myteam:
        screen.blit(hpbar, (220, offset + 75))
        word_builder(mon.name, 160, offset + 10)
        maxhp = mon.maxhp
        hp = mon.hp
        if hp != 0:
            pygame.draw.rect(screen, GREEN, [325, offset + 82, 399, 14])
            word_builder('%50', 700, offset + 10)
        else:
            word_builder('%50 FNT', 700, offset + 10)
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
        word_builder('{0}/{1}'.format(hp,maxhp),800 , offset + 60)
        screen.blit(mon1, (60, offset + 15))
        offset += 110
    word_builder('>', 0, 110 * num + 60)
    writebtm('Bring out which', 'POK~MON?')
    flag = True
    for i in range(5):
        pygame.draw.rect(screen, WHITE, [60, 110 * num + 15, 101,101])
        if flag:
            screen.blit(mon2, (60, 110 * num + 15))
        else:
            screen.blit(mon1, (60, 110 * num + 15))
        flag = not flag
        pygame.display.flip()
        sleep(.5)
    num += 1
    pygame.draw.rect(screen, WHITE, [0,0,60,800])
    word_builder('>', 0, 110 * num + 60)
    writebtm('Bring out which', 'POK~MON?')
    flag = True
    for i in range(10):
        pygame.draw.rect(screen, WHITE, [60, 110 * num + 15, 101,101])
        if flag:
            screen.blit(mon2, (60, 110 * num + 15))
        else:
            screen.blit(mon1, (60, 110 * num + 15))
        flag = not flag
        pygame.display.flip()
        sleep(.2)



def drawoppattackanimation(move):
    sleep(2)

def drawoppmove(opppkmn):
    writebtm('Enemy ' + opppkmn.name.upper(),'used {0}!'.format('TACKLE'.upper()))
    drawoppattackanimation('move')


def opppkmnattacks(mypkmn, opppkmn):
    clear()
    drawmypkmn(mypkmn)
    drawopppkmn(opppkmn)
    drawopphp(opppkmn)
    drawoppmove(opppkmn)

def dmgopp(pkmn, dmg):
    for d in range(dmg):
        pkmn.sethp(pkmn.hp-1)
        drawopphp(pkmn)
        if pkmn.hp == 0:
            opppkmnfaint(pkmn)
            return True
        sleep(.01)
    return False



def mypkmnattacks(mypkmn, opppkmn):
    clear()
    drawmypkmn(mypkmn)
    drawopppkmn(opppkmn)
    drawopphp(opppkmn)
    pygame.draw.rect(screen, WHITE, [0, 442 ,695,300])
    drawattack()
    pygame.display.flip()
    sleep(2)
    drawmymove(mypkmn, opppkmn)
    pygame.display.flip()

def lost(name):
    writebtm(name + ' is out of', 'useable POK~MON!')
    sleep(2)
    writebtm(name + ' blacked', 'out!')
    sleep(2)
    screen.fill(GREY)
    pygame.display.flip()
    sleep(.5)
    screen.fill(BLACK)
    pygame.display.flip()
    sleep(1)


def win(myname, oppname):
    writebtm( myname + ' defeated', oppname + '!')
    sleep(2)

clear()
pygame.display.flip()
poss = [1,4,7,25]
possible = []
for p in poss:
    pkmn = pygame.image.load(images + 'fronts/{0}.PNG'.format(p)).convert()
    pkmn.set_colorkey((255,255,255))
    possible.append(pkmn)
    if p == 4:
        current = pkmn

screen.blit(current, [305, 520])
screen.blit(trainer,[640,512])
pygame.display.flip()
width = logo.get_width()
height = logo.get_height()

#for i in range(-470,50,1):
#    pygame.draw.rect(screen, WHITE, [130,i-1,logo.get_width(),logo.get_height()])
#    screen.blit(logo, (130, i))
#    pygame.display.update([130,i-1,width,height+1])
#for i in range(50,-20,-1):
#    pygame.draw.rect(screen, WHITE, [130,i+1,logo.get_width(),logo.get_height()])
#    screen.blit(logo, (130, i))
#    pygame.display.update([130,i+1,width,height+1])
#for i in range(-20,50,1):
#    pygame.draw.rect(screen, WHITE, [130,i-1,logo.get_width(),logo.get_height()])
#    screen.blit(logo, (130, i))
#    pygame.display.update([130,i-1,width,height+1])
#
#
#width = current.get_width()
#height = current.get_height()
#count = 0
#while count < 2:
#    conn = connect('/home/brian.j.ramsel/shawn/shawn')
#    c = conn.cursor()
#    tmp = c.execute("SELECT * from teams order by ROWID").fetchone()
#    if tmp:
#        if count == 0:
#            myname = tmp[0]
#            mypkmn = tmp[1:]
#        if count == 1:
#            oppname = tmp[0]
#            opppkmn = tmp[1:]
#        c.execute("DELETE from teams where name = '{0}'".format(tmp[0]))
#        conn.commit()
#        count += 1
#    for x in range(305, -392,-1):
#        pygame.draw.rect(screen, WHITE, [x+1,520, width, height])
#        screen.blit(current, (x, 520))
#        screen.blit(trainer,(640,512))
#        pygame.display.update([x+1,520,width + 1, height])
#    old = current
#    while old == current:
#        current = choice(possible)
#    for x in range(1280, 304, -1):
#        pygame.draw.rect(screen, WHITE, [x+1,520, width, height])
#        screen.blit(current, (x, 520))
#        screen.blit(trainer,(640,512))
#        pygame.display.update([x+1,520,width + 1, height])
#    sleep(2)
#    sleep(5)

mypkmn = [9,150,149,6,25,100]
opppkmn = [9,150,149,6,25,100]
myname = 'ASD'
oppname = 'TEst2'

myteam = []
oppteam = []
for i in mypkmn:
    myteam.append(pokemon(i))
    pkmn = pygame.image.load(images + 'backs/{0}.PNG'.format(i)).convert()
    pkmn.set_colorkey((255,255,255))
    myteam[-1].setimg(pkmn)
for i in opppkmn:
    oppteam.append(pokemon(i))
    pkmn = pygame.image.load(images + 'fronts/{0}.PNG'.format(i)).convert()
    pkmn.set_colorkey((255,255,255))
    oppteam[-1].setimg(pkmn)
t = 0
me = 0
opp = 0


def popball(name):
    writebtm('Go! ' + myteam[me].name + '!')
    sleep(1)
    screen.blit(poke1,(115,450))
    pygame.display.flip()
    sleep(.2)
    pygame.draw.rect(screen, WHITE, [115,450,302,302])
    writebtm('Go! ' + name + '!')
    screen.blit(poke2,(120,450))
    pygame.display.flip()
    sleep(.2)
    pygame.draw.rect(screen, WHITE, [115,450,302,302])


selector = 0
def attacking(select):
    drawattack(myteam[me], select)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                if select < 3:
                    select += 1
                    drawattack(myteam[me], select)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                if select > 0:
                    select -= 1
                    drawattack(myteam[me], select)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                if myteam[me].moves[select].pp > 0:
                    myteam[me].moves[select].usepp()
                    if myteam[me].hit_or_miss(oppteam[opp], myteam[me].moves[select]):
                        drawmymove(myteam[me], oppteam[opp], select)
                        crit, type_, dmg =  myteam[me].calc_dmg(oppteam[opp], myteam[me].moves[select])
                        dead = dmgopp(oppteam[opp], dmg)
                        if dead:
                            drawoppbar(oppteam)
                            drawmypkmn(myteam[me])
                            writebtm(oppname +' is', 'about to use')
                            #TODO add arrow and button press
                            sleep(2)
                            writebtm('about to use', oppteam[opp].name)
                            sleep(2)
                            pygame.draw.rect(screen, WHITE, [0, 403, 375, 280])
                            screen.blit(conf,(10,410))
                            pygame.display.update(0, 403, 375, 280)
                            sel = 0
                            f = True
                            while f:
                                word_builder(['>',' '][sel] + 'YES', 50, 460)
                                word_builder([' ','>'][sel] + 'NO', 50, 570)
                                for event in pygame.event.get():
                                    if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                                        if sel == 0:
                                            sel = 1
                                    if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                                        if sel == 1:
                                            sel = 0
                                    if event.type == pygame.KEYDOWN and ((event.key == pygame.K_z and sel == 0) or event.key == pygame.K_x):
                                        f = False
                                        break
                                    if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                                        f = False
                                        break

                                sleep(.1)

                            writebtm('Will ' + myname, 'change POK~MON?')

                        clearbtm()
                        drawmypkmn(myteam[me])
                        drawchoice(selector)
                        pygame.display.flip()
                        return
                    else:
                        clearbtm()
                        drawmypkmn(myteam[me])
                        pygame.display.flip()
                        writebtm(myteam[me].name + "'s attack", 'missed!')
                        sleep(2)
                        clearbtm()
                        drawchoice(selector)
                        pygame.display.flip()
                        return
                else:
                    #TODO NO PP
                    pass
            if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                    clearbtm()
                    drawmypkmn(myteam[me])
                    drawchoice(selector)
                    pygame.display.flip()
                    return
        sleep(.1)






    sleep(.1)


def run(selector):
    while True:
        for event in pygame.event.get():
            #if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            #    mypkmnattacks(myteam[me], oppteam[opp])
            #    opppkmnfaint(oppteam[opp])
            #    opp += 1
            #    t = 1
            #    flag = False
            #    break
            #if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            #    opppkmnattacks(myteam[me], oppteam[opp])
            #    mypkmnfaint(myteam[me])
            #    if me < 5:
            #        drawpickmon(myteam,me)
            #    me += 1
            #    t = 2
            #    flag = False
            #    break
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                if selector == 0 or selector == 1:
                    selector += 2
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                if selector == 2 or selector == 3:
                    selector -= 2
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                if selector == 0 or selector == 2:
                    selector += 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                if selector == 1 or selector == 3:
                    selector -= 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                select = 0
                if selector == 0:
                    attacking(select)
                    pygame.draw.rect(screen, WHITE, [size[0]-730, size[1]-250, 450,200])
                    drawchoice(selector)
                    pygame.display.update(size[0]-730, size[1]-250, 450,200)
            drawchoice(selector)
            pygame.display.flip()
    sleep(.1)


while me < 6 and opp < 6:
    flag = True
    clear()
    if t == 1:
        drawoppbar(oppteam)
        drawmypkmn(myteam[me])
        writebtm(oppname +' is', 'about to use')
        sleep(2)
        writebtm('about to use', oppteam[opp].name)
        sleep(2)
        pygame.draw.rect(screen, WHITE, [0, 403, 375, 280])
        screen.blit(conf,(10,410))
        word_builder('>YES', 50, 460)
        word_builder(' NO', 50, 570)
        writebtm('Will ' + myname, 'change POK~MON?')
        sleep(1)
        pygame.draw.rect(screen, WHITE, [0, 403, 375, 280])
        screen.blit(conf,(10,410))
        screen.blit(conf,(10,410))
        word_builder(' YES', 50, 460)
        word_builder('>NO', 50, 570)
        pygame.display.flip()
        sleep(1)
        pygame.draw.rect(screen, WHITE, [0, 403, 375, 280])
        drawmypkmn(myteam[me])
        drawopppkmn(oppteam[opp])
        writebtm(oppname + ' sent','out ' + oppteam[opp].name + '!')
        sleep(2)
        drawoppname(oppteam[opp])
        drawopphp(oppteam[opp])
    if t == 2:
        drawoppname(oppteam[opp])
        drawopphp(oppteam[opp])
        drawopppkmn(oppteam[opp])
        popball(myteam[me].name)
        drawmypkmn(myteam[me])

    if t == 0:
        drawoppbar(oppteam)
        screen.blit(trainerback,(59, size[1]-740))
        drawmybar(myteam)
        width = trainer.get_width()
        height = trainer.get_height()
        writebtm(oppname + ' wants', 'to fight!')
        for i in range(size[0] + 10, size[0]-501, -1):
            pygame.draw.rect(screen, WHITE, [i+1,0,width,height])
            screen.blit(trainer,(i,10))
            pygame.display.update(i,0,width+1,height)
        pygame.draw.rect(screen, WHITE, [780,0,500,400])
        #sleep(2)
        for i in range(size[0] - 500, size[0]+10, 1):
            pygame.draw.rect(screen, WHITE, [i-1,0,width,height])
            screen.blit(trainer,(i,10))
            pygame.display.update(i-1,0,width+1,height)
        pygame.draw.rect(screen, WHITE, [780,0,500,400])
        drawopppkmn(oppteam[opp])
        drawoppname(oppteam[opp])
        drawopphp(oppteam[opp])
        writebtm(oppname + ' sent', 'out ' + oppteam[opp].name + '!')
        width = trainerback.get_width()
        height = trainerback.get_height()
        #sleep(1)
        for i in range(59, -400, -1):
            pygame.draw.rect(screen, WHITE, [i+1, size[1]-740, width, height])
            screen.blit(trainerback,(i, size[1]-740))
            pygame.display.update(i, size[1]-740, width + 1 , height)
        popball(myteam[me].name)
        pygame.draw.rect(screen, WHITE, [size[0] - 700, size[1]-505, 602, 154])
        drawmypkmn(myteam[me])

    selector = 0
    clearbtm()
    drawchoice(selector)
    pygame.display.flip()
    run(selector)







if me == 6:
    lost(myname)
else:
    win(myname, oppname)


