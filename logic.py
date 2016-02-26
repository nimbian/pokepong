from pygame import image, draw, display, event
import pygame
from util import loadimg, loadalphaimg, alphabet
from random import choice, randint
from time import sleep
from classes import pokemon
from math import ceil,floor
from sqlite3 import connect


SIZE = (1280,1024)
WHITE = (253, 236, 254)
GREEN = (63,156,79)
YELLOW = (255,228,104)
RED = (209,71,40)
GREY = (108,108,108)
BLACK = (0,0,0)
SCREEN = display.set_mode(SIZE)

BTM = loadalphaimg('btmclean.png')
MYHP = loadalphaimg('myhp.png')
OPPHP = loadalphaimg('opphp.png')
MOVECHOICE = loadalphaimg('choiceclean.png')
ATTACK = loadalphaimg('attack.png')
ALPHA = loadalphaimg('alphafull.png')
HPBAR = loadalphaimg('hpbar.png')
MYBAR = loadalphaimg('mybar.png')
OPPBAR = loadalphaimg('oppbar.png')
ALIVE = loadalphaimg('alive.png')
FAINTED = loadalphaimg('fainted.png')
CONF = loadalphaimg('conf.png')
LOGO = loadalphaimg('logo.png')
TRAINER = loadalphaimg('trainer.png')
TRAINERBACK = loadalphaimg('trainerback.png')
POKE1 = loadalphaimg('poke1.png')
POKE2 = loadalphaimg('poke2.png')

SSIZE = [392,392]

BTM_TUPLE = (10, SIZE[1]-340)
MYHPBAR_RECT = [SIZE[0] - 700, SIZE[1]-505, MYHP.get_width(), MYHP.get_height()]
MYHP_RECT = [SIZE[0]-532, SIZE[1]-486, 399, 14]
MYPKMN = [59,SIZE[1]-740]

OPPHPBAR_RECT = [80, 120, 602, 91]
OPPHP_RECT = [227,141,399,15]
OPPPKMN = [SIZE[0]-500,0]
ALPHA_DICT = alphabet()

def clear():
    SCREEN.fill(WHITE)

def word_builder(word,start_x, start_y):
    x = start_x
    draw.rect(SCREEN, WHITE, [x, start_y, len(word)*56,60])
    for l in word:
        SCREEN.blit(ALPHA,(start_x, start_y),ALPHA_DICT[l])
        start_x+=56
    return [x, start_y, len(word)*56,60]

def write_btm(*args):
    clearbtm()
    SCREEN.blit(BTM, BTM_TUPLE)
    retval = []
    retval.append([BTM_TUPLE[0], BTM_TUPLE[1], BTM.get_width(), BTM.get_height()])
    retval.append(word_builder(args[0], 50, SIZE[1]-250))
    try:
        retval.append(word_builder(args[1], 50, SIZE[1]-130))
    except:
        pass
    return retval

def clearbtm():
    draw.rect(SCREEN, WHITE, [0,SIZE[1]-340,SIZE[0],340])

def draw_my_hp_bar():
    draw.rect(SCREEN, WHITE, MYHPBAR_RECT)
    SCREEN.blit(MYHP, MYHPBAR_RECT[:2])
    return [MYHPBAR_RECT]

def draw_my_lvl(pkmn):
    return [word_builder('%' + str(pkmn.lvl), SIZE[0] - 405, SIZE[1]-565)]

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
    SCREEN.blit(pkmn.img, MYPKMN)
    return [MYPKMN + SSIZE]

def draw_my_pkmn_name(pkmn):
    display.update(draw.rect(SCREEN, WHITE, [SIZE[0] - 630, SIZE[1]-625,600,60]))
    return [word_builder(pkmn.name.upper(), SIZE[0] - 630, SIZE[1]-625)]

def draw_my_poke_balls(team):
    draw.rect(SCREEN, WHITE, MYHPBAR_RECT)
    SCREEN.blit(MYBAR, (SIZE[0]-700, SIZE[1]-442))
    offset = 0
    for mon in team:
        if mon.hp == 0:
            SCREEN.blit(FAINTED, (SIZE[0]-575 + offset * 65, SIZE[1]-430))
        else:
            SCREEN.blit(ALIVE, (SIZE[0]-575 + offset * 65, SIZE[1]-430))
        offset += 1
    for i in range(offset, 6):
        SCREEN.blit(FAINTED, (SIZE[0]-500 + i * 65, SIZE[1]-430))
    return [MYHPBAR_RECT]

def draw_opp_hp_bar():
    draw.rect(SCREEN,WHITE, OPPHPBAR_RECT)
    SCREEN.blit(OPPHP,OPPHPBAR_RECT[:2])
    return [OPPHPBAR_RECT]

def draw_opp_lvl(pkmn):
    return [word_builder('%' + str(pkmn.lvl), 230,60)]

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
    SCREEN.blit(pkmn.img, OPPPKMN)
    return [OPPPKMN + SSIZE]

def draw_opp_pkmn_name(pkmn):
    display.update(draw.rect(SCREEN, WHITE, [60,1,600,60]))
    return [word_builder(pkmn.name.upper(), 60, 1)]




def draw_opp_poke_balls(team):
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
        SCREEN.blit(FAINTED, (180 + i * 65, 132))
    return [OPPHPBAR_RECT]

def return_my_pokemon(me):
    dirty = []
    dirty.append(draw.rect(SCREEN, WHITE, MYPKMN + SSIZE))
    dirty.extend(write_btm('Return', me.current.name))
    display.update(dirty)
    sleep(1)



def pop_ball(name):
    display.update(write_btm('Go! ' + name + '!'))
    sleep(1)
    SCREEN.blit(POKE1,(115,450))
    display.update(115,450, POKE1.get_width(), POKE1.get_height())
    sleep(.2)
    dirty = []
    dirty.append(draw.rect(SCREEN, WHITE, [115,450,302,302]))
    dirty.extend(write_btm('Go! ' + name + '!'))
    dirty.append(SCREEN.blit(POKE2,(120,450)))
    display.update(dirty)
    sleep(.2)
    draw.rect(SCREEN, WHITE, [115,450,302,302])
    write_btm('')
    display.update(115,450,302,302)



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

def intro(current):
    clear()
    display.flip()
    SCREEN.blit(current, [305, 520])
    SCREEN.blit(TRAINER, [640, 512])
    display.update([[305, 520, current.get_width(), current.get_height()],
                    [640, 512, TRAINER.get_width(), TRAINER.get_height()]])
    width = LOGO.get_width()
    height = LOGO.get_height()
    for i in range(-470,50,1):
        draw.rect(SCREEN, WHITE, [130,i-1,width,height])
        SCREEN.blit(LOGO, (130, i))
        display.update([130,i-1,width,height+1])
    for i in range(50,-20,-1):
        draw.rect(SCREEN, WHITE, [130,i+1,width,height])
        SCREEN.blit(LOGO, (130, i))
        display.update([130,i+1,width,height+1])
    for i in range(-20,50,1):
        draw.rect(SCREEN, WHITE, [130,i-1,width,height])
        SCREEN.blit(LOGO, (130, i))
        display.update([130,i-1,width,height+1])

def scrolling(current,possible):
    width = current.get_width()
    height = current.get_height()
    for x in range(305, -392,-1):
        draw.rect(SCREEN, WHITE, [x+1,520, width, height])
        SCREEN.blit(current, (x, 520))
        SCREEN.blit(TRAINER,(640,512))
        display.update([x+1,520,width + 1, height])
    old = current
    while old == current:
        current = choice(possible)
    for x in range(1280, 304, -1):
        draw.rect(SCREEN, WHITE, [x+1,520, width, height])
        SCREEN.blit(current, (x, 520))
        SCREEN.blit(TRAINER,(640,512))
        display.update([x+1,520,width + 1, height])
    return current

def build_team(pkmn, me = False):
    team = []
    for i in pkmn:
        team.append(pokemon(i))
        if me:
            pkmn = loadimg('backs/{0}.PNG'.format(i)).convert()
        else:
            pkmn = loadimg('fronts/{0}.PNG'.format(i)).convert()
        pkmn.set_colorkey((255,255,255))
        team[-1].setimg(pkmn)
    return team

def move_opp_trainer_in():
    width = TRAINER.get_width()
    height = TRAINER.get_height()
    for i in range(SIZE[0] + 10, SIZE[0]-501, -1):
        draw.rect(SCREEN, WHITE, [i+1,0,width,height])
        SCREEN.blit(TRAINER,(i,10))
        display.update(i,0,width+1,height)

def move_opp_trainer_out():
    width = TRAINER.get_width()
    height = TRAINER.get_height()
    for i in range(SIZE[0] - 500, SIZE[0]+10, 1):
        draw.rect(SCREEN, WHITE, [i-1,0,width,height])
        SCREEN.blit(TRAINER,(i,10))
        display.update(i-1,0,width+1,height)

def move_my_trainer():
    width = TRAINERBACK.get_width()
    height = TRAINERBACK.get_height()
    for i in range(59, -400, -1):
        draw.rect(SCREEN, WHITE, [i+1, SIZE[1]-740, width, height])
        SCREEN.blit(TRAINERBACK,(i, SIZE[1]-740))
        display.update(i, SIZE[1]-740, width + 1 , height)

def draw_my_trainer():
    width = TRAINERBACK.get_width()
    height = TRAINERBACK.get_height()
    SCREEN.blit(TRAINERBACK,(59, SIZE[1]-740))
    return [[59, SIZE[1]-740, width, height]]

def draw_choice(select):
    dirty = []
    dirty.append(SCREEN.blit(MOVECHOICE,BTM_TUPLE))
    dirty.append(word_builder(['>',' ',' ',' '][select] + 'FIGHT',SIZE[0]-730, SIZE[1]-250))
    dirty.append(word_builder([' ','>',' ',' '][select] + 'ITEM',SIZE[0]-730, SIZE[1]-130))
    dirty.append(word_builder([' ',' ','>',' '][select] + '#$',SIZE[0]-350, SIZE[1]-250))
    dirty.append(word_builder([' ',' ',' ','>'][select] + 'RUN',SIZE[0]-350, SIZE[1]-130))
    display.update(dirty)

def update_choice(select):
    dirty = []
    dirty.append(word_builder(['>',' ',' ',' '][select],SIZE[0]-730, SIZE[1]-250))
    dirty.append(word_builder([' ','>',' ',' '][select],SIZE[0]-730, SIZE[1]-130))
    dirty.append(word_builder([' ',' ','>',' '][select],SIZE[0]-350, SIZE[1]-250))
    dirty.append(word_builder([' ',' ',' ','>'][select],SIZE[0]-350, SIZE[1]-130))
    display.update(dirty)


def me_next_mon(me, opp, mode):
    if mode == 'battle':
        pkmn = opp_change_pkmn()
        if opp.current != pkmn:
            pass
            #TODO swap opp pkmn
    draw_choose_pkmn(me, opp, mydeath = True)
    draw_all_opp(opp.current)




def opp_next_mon(me, opp, mode):
    display.update(draw.rect(SCREEN, WHITE, [230,60,180,60]))
    display.update(draw.rect(SCREEN, WHITE, [60,1,600,60]))
    display.update(draw_opp_poke_balls(opp.pkmn))
    if mode == 'random':
        opp.get_next_pkmn()
    elif mode == 'pong':
        opp.get_next_pkmn()
    elif mode == 'battle':
        opp.set_current(wait_for_opp_next_mon())
    display.update(write_btm(opp.name +' is', 'about to use'))
    if mode != 'pong':
        wait_for_button()
    else:
        sleep(1)
    display.update(write_btm('about to use', opp.current.name))
    if mode != 'pong':
        wait_for_button()
    else:
        sleep(1)
    if mode != 'pong':
        change_pokemon(me, opp)
    else:
        no_change()
    dirty = []
    dirty.extend(write_btm(opp.name + ' sent', 'out ' + opp.current.name + '!'))
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
        #sleep(2)
        move_opp_trainer_out()
        draw_all_opp(opp.current)
        dirty.extend(write_btm(opp.name + ' sent', 'out ' + opp.current.name + '!'))
    else:
        draw_all_opp(opp.current)
        move_opp_trainer_out()
        dirty.extend(write_btm('A wild ' + opp.current.name, 'has appeard!'))
    display.update(dirty)


    move_my_trainer()
    pop_ball(me.current.name)
    draw_all_me(me.current)

def attacking(me):
    dirty = []
    selector = 0
    clearbtm()
    dirty.append(draw.rect(SCREEN, WHITE, [0, 442 ,695,300]))
    dirty.append(SCREEN.blit(ATTACK, (10, SIZE[1]-577)))
    dirty.append(word_builder(['>',' ',' ',' '][selector] + me.current.moves[0].name.upper(),300, SIZE[1]-285))
    dirty.append(word_builder([' ','>',' ',' '][selector] + me.current.moves[1].name.upper(),300, SIZE[1]-225))
    dirty.append(word_builder([' ',' ','>',' '][selector] + me.current.moves[2].name.upper(),300, SIZE[1]-165))
    dirty.append(word_builder([' ',' ',' ','>'][selector] + me.current.moves[3].name.upper(),300, SIZE[1]-105))
    dirty.append(word_builder('TYPE/',60, SIZE[1]-530))
    dirty.extend(draw_move(me.current.moves[selector]))
    display.update(dirty)

def update_attacking(me, selector):
    dirty = []
    dirty.append(draw.rect(SCREEN, WHITE, [0, 442 ,695,300]))
    dirty.append(SCREEN.blit(ATTACK, (10, SIZE[1]-577)))
    dirty.append(word_builder(['>',' ',' ',' '][selector] + me.current.moves[0].name.upper() ,300, SIZE[1]-285))
    dirty.append(word_builder([' ','>',' ',' '][selector],300, SIZE[1]-225))
    dirty.append(word_builder([' ',' ','>',' '][selector],300, SIZE[1]-165))
    dirty.append(word_builder([' ',' ',' ','>'][selector],300, SIZE[1]-105))
    dirty.append(word_builder('TYPE/',60, SIZE[1]-530))
    dirty.extend(draw_move(me.current.moves[selector]))
    display.update(dirty)

def clean_me_up(me):
    dirty = []
    dirty.append(clearbtm())
    dirty.append(draw.rect(SCREEN, WHITE, [0, 442 ,695,300]))
    draw_all_me(me.current)
    display.update(dirty)

def run_me_faint(me):
    for i in range(0,400,2):
        draw.rect(SCREEN, WHITE, [59, SIZE[1]-740, 392, 392])
        SCREEN.blit(me.current.img, (59, SIZE[1]-740 + i), (0,0,392,392-i))
        display.update(59, SIZE[1]-738 + i, 392,394-i)
    display.update(write_btm(me.current.name, 'fainted!'))

def run_opp_faint(opp):
    for i in range(0,393,2):
        draw.rect(SCREEN, WHITE, [SIZE[0]-500, 0, 392, 392])
        SCREEN.blit(opp.current.img, (SIZE[0]-500, i), (0,0,392,392-i))
        display.update([SIZE[0]-500, i-2,392,394-i])
    display.update(write_btm('Enemy ' + opp.current.name.upper(),'fainted!'))
    sleep(2)

def dmg_pkmn(pkmn, dmg, me = False):
    for d in range(dmg):
        pkmn.sethp(pkmn.hp-1)
        if me:
            display.update(draw_my_hp(pkmn))
        else:
            display.update(draw_opp_hp(pkmn))
        if pkmn.hp == 0:
            return True
        sleep(.01)
    return False

def run_move(me, opp, move):
    if move.pp > 0:
        move.usepp()
        if me.current.hit_or_miss(opp.current, move):
            crit, type_, dmg = me.current.calc_dmg(me.current, move)
            display.update(write_btm(me.current.name, 'used {0}'.format(move.name.upper())))
            #sleep(1)
            #TODO CRIT/SUPER EFFECTIVE
            return dmg_pkmn(opp.current, dmg)
        else:
            display.update(write_btm(me.current.name, 'used {0}'.format(move.name.upper())))
            sleep(1)
            display.update(write_btm(me.current.name + "'s", 'attack missed!'))
            sleep(1)



def wait_for_button():
    pygame.event.clear()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return
        sleep(.1)

def selecting(select):
    dirty = []
    dirty.append(word_builder(['>',' '][select] + 'YES', 50, 460))
    dirty.append(word_builder([' ','>'][select] + 'NO', 50, 570))
    display.update(dirty)

def draw_pkmn_choice(mon,offset):
    SCREEN.blit(HPBAR, (220, offset * 110 + 75))
    word_builder(mon.name, 160, offset* 110 + 10)
    maxhp = mon.maxhp
    hp = mon.hp
    bar_len = floor(hp/float(maxhp)*399)
    if bar_len < 100:
        color = RED
    elif bar_len < 200:
        color = YELLOW
    else:
        color = GREEN
    if hp > 0:
        draw.rect(SCREEN, color, [325,offset * 110 + 82, bar_len, 14])
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
    word_builder('{0}/{1}'.format(hp,maxhp),800 , offset * 110 + 60)
    SCREEN.blit(mon.sprite1, (60, offset * 110+ 15))

def update_choose(old, new, me):
    dirty = []
    dirty.append(word_builder(' ', 0, 110 * old + 60))
    dirty.append(draw.rect(SCREEN, WHITE, [10, 110 * old + 15, 105, 105]))
    dirty.append(draw.rect(SCREEN, WHITE, [60, 110 * old + 15, 101, 101]))
    dirty.append(SCREEN.blit(me.pkmn[old].sprite1, (60, 110 * old + 15)))
    dirty.append(word_builder('>', 0, 110 * new + 60))
    display.update(dirty)






def draw_choose_pkmn(me, opp, oppdeath = False, mydeath = False):
    clear()
    offset = 0
    dirty = []
    for mon in me.pkmn:
        draw_pkmn_choice(mon,offset)
        offset += 1
    word_builder('>', 0, 110 * me.get_current_index() + 60)
    write_btm('Bring out which', 'POK~MON?')
    pygame.display.flip()
    pygame.event.clear()
    select = me.get_current_index()
    count = 0
    tmp = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                if select > 0:
                    select -= 1
                    update_choose(select+1, select, me)
                    count = 1
                    tmp = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                if select < len(me.pkmn) - 1:
                    select += 1
                    update_choose(select-1, select, me)
                    count = 1
                    tmp = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                if select == me.get_current_index():
                    display.update(write_btm(me.current.name, 'is already out!'))
                    wait_for_button()
                    display.update(write_btm('Bring out which', 'POK~MON?'))
                elif me.pkmn[select].hp == 0:
                    #TODO can't bring out fainted
                    pass
                else:
                    clear()
                    pygame.display.flip()
                    if not oppdeath:
                        draw_all_opp(opp.current)
                    else:
                        draw_all_me(me.current)
                        return_my_pokemon(me)
                    if mydeath or oppdeath:
                        me.set_current(select)
                        pop_ball(me.current.name)
                        draw_all_me(me.current)
                        sleep(.5)
                    return select
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                if not mydeath:
                    clear()
                    draw_all_opp(opp.current)
                    return False

        sleep(.1)
        con1 = count % 2 == 0 and me.pkmn[select].hp > me.pkmn[select].maxhp / 2
        con2 = count % 5 == 0 and me.pkmn[select].hp <= me.pkmn[select].maxhp / 2
        if con1 or con2:
            dirty = draw.rect(SCREEN, WHITE, [60, select * 110+ 15, 101, 101])
            if tmp:
                SCREEN.blit(me.pkmn[select].sprite2, (60, select * 110+ 15))
            else:
                SCREEN.blit(me.pkmn[select].sprite1, (60, select * 110+ 15))
            display.update(dirty)
            tmp = not tmp


        count += 1



def wait_for_opp_move(opp,mode):
    if mode == 'random' or mode == 'wild':
        #TODO PP check
        return opp.current.moves[randint(0,3)]
    else:
        #TODO OPP wait
        pass

def wait_for_opp_next_mon():
    #TODO waiting for opp
    pass

def run_opp_move(me, opp, move):
    move.usepp()
    if opp.current.hit_or_miss(me.current, move):
        crit, type_, dmg = opp.current.calc_dmg(opp.current, move)
        display.update(write_btm('Enemy ' + opp.current.name, 'used {0}'.format(move.name.upper())))
        #sleep(1)
        #TODO CRIT/SUPER EFFECTIVE
        return dmg_pkmn(me.current, dmg, me = True)
    else:
        display.update(write_btm('Enemy ' + opp.current.name, 'used {0}'.format(move.name.upper())))
        sleep(1)
        display.update(write_btm('Enemy ' + opp.current.name + "'s", 'attack missed'))
        sleep(1)








def change_pokemon(me, opp):
    dirty = []
    dirty.append(draw.rect(SCREEN, WHITE, [0, 403, 375, 280]))
    dirty.extend(write_btm('Will ' + me.name, 'change POK~MON?'))
    SCREEN.blit(CONF,(10,410))
    display.update(dirty)
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
                dirty = []
                dirty.append(draw.rect(SCREEN, WHITE, [0, 403, 375, 280]))
                dirty.extend(draw_my_pkmn_sprite(me.current))
                display.update(dirty)
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                draw_choose_pkmn(me, opp, oppdeath = True)
                clear()
                display.flip()
                draw_all_me(me.current)
                return True


def run_attack(me, opp):
    attacking(me)
    select = 0
    pygame.event.clear()
    while True:
        if me.current.pp_left():
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    if select < len(me.current.moves)-1:
                        select += 1
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    if select > 0:
                        select -= 1
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                    clean_me_up(me)
                    draw_choice(0)
                    return False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                    if me.current.moves[select].has_pp():
                        return me.current.moves[select]
                    else:
                        clean_me_up(me)
                        display.update(write_btm('No PP!'))
                        wait_for_button()
                        attacking(me)

                update_attacking(me, select)
        else:
            #TODO NO PP
            return False

def draw_move(move):
    retval = []
    retval.append(word_builder(move.type_.upper() + '/',116, SIZE[1]-470))
    retval.append(word_builder(str(move.pp) + '/' + str(move.maxpp),284, SIZE[1]-410))
    return retval


def lost(me, mode):
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
    SCREEN.fill(GREY)
    display.flip()
    sleep(.5)
    SCREEN.fill(BLACK)
    display.flip()
    sleep(1)

def win(me, opp, mode):
    display.update(write_btm(me.name + ' defeated', opp.name + '!'))
    if mode != 'pong':
        wait_for_button()
    else:
        sleep(2)



def run_game(me, opp, mode):
    selector = 0
    pygame.event.clear()
    while True:
        for ev in event.get():
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
                    my_move = run_attack(me, opp)
                    if my_move:
                        opp_move = wait_for_opp_move(opp, mode)
                        if my_move.name == 'Quick Attack' != opp_move.name == 'Quick Attack':
                            if my_move.name == 'Quick Attack':
                                run_move(me, opp, my_move)
                                clean_me_up(me)
                                if not opp.current.alive():
                                    return 0
                                run_opp_move(me, opp, opp_move)
                                if not me.current.alive():
                                    return 1
                            else:
                                clean_me_up(me)
                                run_opp_move(me, opp, opp_move)
                                if not me.current.alive():
                                    return 1
                                run_move(me, opp, my_move)
                                if not opp.current.alive():
                                    return 0
                        else:
                            if me.current.calc_speed() > opp.current.calc_speed():
                                run_move(me, opp, my_move)
                                clean_me_up(me)
                                if not opp.current.alive():
                                    return 0
                                run_opp_move(me, opp, opp_move)
                                if not me.current.alive():
                                    return 1
                            else:
                                clean_me_up(me)
                                run_opp_move(me, opp, opp_move)
                                if not me.current.alive():
                                    return 1
                                run_move(me, opp, my_move)
                                if not opp.current.alive():
                                    return 0
                        return 3
                if selector == 2:
                    select = draw_choose_pkmn(me,opp)
                    clear()
                    pygame.display.flip()
                    draw_all_opp(opp.current)
                    if type(select) == int:
                        opp_move = wait_for_opp_move(opp, mode)
                        draw_all_me(me.current)
                        if opp_move.__class__.__name__ == 'move':
                            if opp_move.name == 'Quick Attack' or opp.current.calc_speed() > me.current.calc_speed():
                                run_opp_move(me,opp,opp_move)
                                sleep(2)
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
                                run_opp_move(me,opp,opp_move)
                                if not me.current.alive:
                                    return 1
                    draw_all_me(me.current)
                    clearbtm()
                    selector = 0
                    draw_choice(0)
                if selector == 3:
                    if mode != 'wild':
                        display.update(write_btm("Can't escape a", "trainer battle"))
                        sleep(2)
                        clearbtm()
                        selector = 0
                        draw_choice(0)
                    else:
                        #TODO ESCAPE!
                        pass
            update_choice(selector)
    sleep(.1)


