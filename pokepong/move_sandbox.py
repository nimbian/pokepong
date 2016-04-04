from pygame import image, draw, display
import pygame
from util import loadalphaimg, loadimg, alphabet, HIGH_ARC, LOW_ARC
from math import floor
from time import sleep
from vlc import MediaPlayer
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
POP = [loadalphaimg('pop1.png'), loadalphaimg('pop2.png'),
       loadalphaimg('pop3.png'), loadalphaimg('pop4.png'),
       loadalphaimg('pop5.png')]

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

#def invert():
#    pixels = pygame.surfarray.pixels3d(SCREEN)
#    pixels[:,:,:3] = CHANGE[(pixels[:,:,0],pixels[:,:,1],pixels[:,:,2])]

def low_big():
    norm = loadalphaimg('moves/Bignorm.png')
    return SCREEN.blit(norm,  (760, 228))

def mid_big():
    norm = loadalphaimg('moves/Bignorm.png')
    return SCREEN.blit(norm,  (896, 133))

def high_big():
    norm = loadalphaimg('moves/Bignorm.png')
    return SCREEN.blit(norm,  (930, 0))

def big_3(attacker,defender):
    tmp = low_big()
    display.update(tmp)
    draw.rect(SCREEN,WHITE,tmp)
    draw_opp_pkmn_sprite(defender)
    draw_my_pkmn_name(attacker)
    sleep(.15)
    tmp2 = mid_big()
    display.update([tmp, tmp2])
    sleep(.15)
    draw_opp_pkmn_sprite(defender)
    tmp = high_big()
    display.update([tmp, tmp2])
    sleep(.15)
    draw_opp_pkmn_sprite(defender)
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

def med_3(attacker,defender):
    tmp = right_med()
    display.update(tmp)
    draw_opp_pkmn_sprite(defender)
    sleep(.15)
    tmp2 = left_med()
    display.update([tmp, tmp2])
    sleep(.15)
    draw_opp_pkmn_sprite(defender)
    tmp = mid_med()
    display.update([tmp, tmp2])
    sleep(.15)
    draw_opp_pkmn_sprite(defender)
    display.update(tmp)

def left_double():
    norm = loadalphaimg('moves/Mednorm.png')
    return SCREEN.blit(norm,  (820, 133))

def right_double():
    norm = loadalphaimg('moves/Mednorm.png')
    return SCREEN.blit(norm,  (930, 222))

def double(attacker,defender):
    tmp = left_double()
    display.update(tmp)
    draw_opp_pkmn_sprite(defender)
    sleep(.15)
    tmp2 = right_double()
    display.update([tmp, tmp2])
    sleep(.15)
    draw_opp_pkmn_sprite(defender)
    display.update(tmp2)

def high_arch_away(attacker,defender, img):
    old = [[0,0],[0,0]]
    for x in HIGH_ARC:
        draw_all_opp(defender)
        draw_my_pkmn_sprite(attacker)
        tmp = SCREEN.blit(img, x)
        display.update([old,tmp])
        sleep(.1)
        old = tmp
        draw.rect(SCREEN, WHITE, old)
    sleep(.1)
    draw_my_pkmn_sprite(attacker)
    display.update(old)

def high_arch_towards(attacker,defender, img):
    old = [0,0,0,0]
    for x in HIGH_ARC[::-1]:
        draw_all_opp(defender)
        draw_my_pkmn_sprite(attacker)
        tmp = SCREEN.blit(img, x)
        display.update([old,tmp])
        sleep(.1)
        old = tmp
        draw.rect(SCREEN, WHITE, old)
    sleep(.1)
    draw_my_pkmn_sprite(attacker)
    display.update(old)

def low_arch_away(attacker,defender, img):
    old = [0,0,0,0]
    for x in LOW_ARC:
        draw_all_opp(defender)
        draw_my_pkmn_sprite(attacker)
        tmp = SCREEN.blit(img, x)
        display.update([old,tmp])
        sleep(.1)
        old = tmp
        draw.rect(SCREEN, WHITE, old)
    sleep(.1)
    draw_my_pkmn_sprite(attacker)
    display.update(old)

def low_arch_towards(attacker,defender, img):
    old = [0,0,0,0]
    for x in LOW_ARC[::-1]:
        draw_all_opp(defender)
        draw_my_pkmn_sprite(attacker)
        tmp = SCREEN.blit(img, x)
        display.update([old,tmp])
        sleep(.1)
        old = tmp
        draw.rect(SCREEN, WHITE, old)
    sleep(.1)
    draw_my_pkmn_sprite(attacker)
    display.update(old)

def sandbox():
    SCREEN.fill(WHITE)
    SCREEN.blit(BTM, BTM_TUPLE)
    display.flip()
    me = trainer(pokemon())
    opp = trainer(pokemon())
    draw_all_opp(opp.current)
    draw_all_me(me.current)
    x = 800
    y = 204
    for i in POP[:-1]:
        tmp = SCREEN.blit(i,(x,y))
        display.update(tmp)
        sleep(.1)
        old = tmp
        draw.rect(SCREEN, WHITE, old)
        draw_opp_pkmn_sprite(opp.current)
        draw_all_me(me.current)
    tmp = SCREEN.blit(POP[-1],(x-28,y-28))
    display.update(tmp)
    sleep(.1)
    draw.rect(SCREEN, WHITE, tmp)
    draw_opp_pkmn_sprite(opp.current)
    draw_all_me(me.current)
    display.update(tmp)
    sleep(15)

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
    pixels = pygame.surfarray.pixels2d(SCREEN)
    pixels ^= 2 ** 32 - 1
    del pixels
    pygame.display.flip()
    SCREEN.unlock()




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

def beam(attacker,defender,type_ = None):
    beams = []
    for i in range(1,7):
        beams.append(loadalphaimg('moves/beam{0}.png'.format(i)))
    x = SCREEN.blit(beams[0],(339,232))
    for i in beams:
        pygame.draw.rect(SCREEN, WHITE, x)
        draw_all_me(attaker)
        draw_all_opp(defender)
        display.update(SCREEN.blit(i,(339,232)))
        sleep(.1)

    pygame.draw.rect(SCREEN, WHITE, x)
    draw_all_me(me.current)
    draw_all_opp(opp.current)
    sleep(.1)
    dmged()


def do_absorb(attacker,defender,attacking):
    s = MediaPlayer("Absorb.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_acid(attacker,defender,attacking):
    s = MediaPlayer("Acid.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_acid_armor(attacker,defender,attacking):
    s = MediaPlayer("Acid Armor.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_agility(attacker,defender,attacking):
    s = MediaPlayer("Agility.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_amnesia(attacker,defender,attacking):
    s = MediaPlayer("Amnesia.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_aurora_beam(attacker,defender,attacking):
    s = MediaPlayer("Aurora Beam.mp3")
    s.start()
    if attacking:
        beam(attacker,defender,type_ = 'aurora')
    else:
        pass #TODO defending
    s.stop()

def do_barrage(attacker,defender,attacking):
    s = MediaPlayer("Barrage.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_barrier(attacker,defender,attacking):
    s = MediaPlayer("Barrier.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_bide(attacker,defender,attacking):
    s = MediaPlayer("Bide.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_bind(attacker,defender,attacking):
    s = MediaPlayer("Bind.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_bite(attacker,defender,attacking):
    s = MediaPlayer("Bite.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_blizzard(attacker,defender,attacking):
    s = MediaPlayer("Blizzard.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_body_slam(attacker,defender,attacking):
    s = MediaPlayer("Body Slam.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_bone_club(attacker,defender,attacking):
    s = MediaPlayer("Bone Club.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_bonemerang(attacker,defender,attacking):
    s = MediaPlayer("Bonmerang.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_bubble(attacker,defender,attacking):
    s = MediaPlayer("Bubble Beam.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_bubblebeam(attacker,defender,attacking):
    s = MediaPlayer("Bubble.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_clamp(attacker,defender,attacking):
    s = MediaPlayer("Clamp.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_comet_punch(attacker,defender,attacking):
    s = MediaPlayer("Comet Punch.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_confuse_ray(attacker,defender,attacking):
    s = MediaPlayer("Confuse Ray.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_confusion(attacker,defender,attacking):
    s = MediaPlayer("Confusion.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_constrict(attacker,defender,attacking):
    s = MediaPlayer("Constrict.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_conversion(attacker,defender,attacking):
    s = MediaPlayer("Conversion.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_counter(attacker,defender,attacking):
    s = MediaPlayer("Counter.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_crabhammer(attacker,defender,attacking):
    s = MediaPlayer("Crabhammer.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_cut(attacker,defender,attacking):
    s = MediaPlayer("Cut.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_defense_curl(attacker,defender,attacking):
    s = MediaPlayer("Defence Curl.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_dig(attacker,defender,attacking):
    s = MediaPlayer("Dig1.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_dig_prep(attacker,defender,attacking):
    s = MediaPlayer("Dig2.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_disable(attacker,defender,attacking):
    s = MediaPlayer("Disable.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_dizzy_punch(attacker,defender,attacking):
    s = MediaPlayer("Dizzy Punch.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_double_kick(attacker,defender,attacking):
    s = MediaPlayer("Double-Egde.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_double_team(attacker,defender,attacking):
    s = MediaPlayer("Double Kick.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_double_edge(attacker,defender,attacking):
    s = MediaPlayer("DoubleSlap.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_doubleslap(attacker,defender,attacking):
    s = MediaPlayer("Double Team.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_dragon_rage(attacker,defender,attacking):
    s = MediaPlayer("Dragon Rage.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_dream_eater(attacker,defender,attacking):
    s = MediaPlayer("Dream Eater.mp")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_drill_peck(attacker,defender,attacking):
    s = MediaPlayer("Drill Peck.mp")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_earthquake(attacker,defender,attacking):
    s = MediaPlayer("Earthquake.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_egg_bomb(attacker,defender,attacking):
    s = MediaPlayer("Egg Bomb.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_ember(attacker,defender,attacking):
    s = MediaPlayer("Ember.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_explosion(attacker,defender,attacking):
    s = MediaPlayer("Explosion.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_fire_blast(attacker,defender,attacking):
    s = MediaPlayer("Fire Blast.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_fire_punch(attacker,defender,attacking):
    s = MediaPlayer("Fire Punch.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_fire_spin(attacker,defender,attacking):
    s = MediaPlayer("Fire Spin.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_fissure(attacker,defender,attacking):
    s = MediaPlayer("Fissure.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_flamethrower(attacker,defender,attacking):
    s = MediaPlayer("Flamethrower.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_flash(attacker,defender,attacking):
    s = MediaPlayer("Flash.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_fly(attacker,defender,attacking):
    s = MediaPlayer("Fly.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_fly_prep(attacker,defender,attacking):
    s = MediaPlayer("Fly_prep.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_focus_energy(attacker,defender,attacking):
    s = MediaPlayer("Focus Energy.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_fury_attack(attacker,defender,attacking):
    s = MediaPlayer("Fury Attack.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_fury_swipes(attacker,defender,attacking):
    s = MediaPlayer("Fury Swipes.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_glare(attacker,defender,attacking):
    s = MediaPlayer("Glare.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_growl(attacker,defender,attacking):
    s = MediaPlayer(attacker.base.name + '.mp3')
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_growth(attacker,defender,attacking):
    s = MediaPlayer("Growth.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_guillotine(attacker,defender,attacking):
    s = MediaPlayer("Guillotine.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_gust(attacker,defender,attacking):
    s = MediaPlayer("Gust.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_harden(attacker,defender,attacking):
    s = MediaPlayer("Harden.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_haze(attacker,defender,attacking):
    s = MediaPlayer("Haze.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_headbutt(attacker,defender,attacking):
    s = MediaPlayer("HeadButt.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_hi_jump_kick(attacker,defender,attacking):
    s = MediaPlayer("Hi Jump Kick.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_horn_attack(attacker,defender,attacking):
    s = MediaPlayer("Horn Attack.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_horn_drill(attacker,defender,attacking):
    s = MediaPlayer("Horn Drill.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_hydro_pump(attacker,defender,attacking):
    s = MediaPlayer("Hydro Pump.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_hyper_beam(attacker,defender,attacking):
    s = MediaPlayer("Hyper Beam.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_hyper_fang(attacker,defender,attacking):
    s = MediaPlayer("Hyper Fang.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_hypnosis(attacker,defender,attacking):
    s = MediaPlayer("Hypnosis.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_ice_beam(attacker,defender,attacking):
    s = MediaPlayer("Ice Beam.mp3")
    s.start()
    if attacking:
        beam(attacker,defender,type_='ice')
    else:
        pass #TODO defending
    s.stop()

def do_ice_punch(attacker,defender,attacking):
    s = MediaPlayer("Ice Punch.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_jump_kick(attacker,defender,attacking):
    s = MediaPlayer("Jump Kick.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_karate_chop(attacker,defender,attacking):
    s = MediaPlayer("Karate Chop.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_kinesis(attacker,defender,attacking):
    s = MediaPlayer("Kinesis.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_leech_life(attacker,defender,attacking):
    s = MediaPlayer("Leach Kiss.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_leech_seed(attacker,defender,attacking):
    s = MediaPlayer("Leach Seed.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_leer(attacker,defender,attacking):
    s = MediaPlayer("Leer.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_lick(attacker,defender,attacking):
    s = MediaPlayer("Lick.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_light_screen(attacker,defender,attacking):
    s = MediaPlayer("Light Screen.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_lovely_kiss(attacker,defender,attacking):
    s = MediaPlayer("Lovely Kiss.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_low_kick(attacker,defender,attacking):
    s = MediaPlayer("Low Kick.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_meditate(attacker,defender,attacking):
    s = MediaPlayer("Meditate.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_mega_drain(attacker,defender,attacking):
    s = MediaPlayer("Meaga Drain.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_mega_kick(attacker,defender,attacking):
    s = MediaPlayer("Mega Kick.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_mega_punch(attacker,defender,attacking):
    s = MediaPlayer("Mega Punch.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_metronome(attacker,defender,attacking):
    s = MediaPlayer("Metronome.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_mimic(attacker,defender,attacking):
    s = MediaPlayer("Mimic.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_minimize(attacker,defender,attacking):
    s = MediaPlayer("Minimize.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_mirror_move(attacker,defender,attacking):
    pass #TODO mirror opp last move
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_mist(attacker,defender,attacking):
    s = MediaPlayer("Mist.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_night_shade(attacker,defender,attacking):
    s = MediaPlayer("Night Shade.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_pay_day(attacker,defender,attacking):
    s = MediaPlayer("Pay Day.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_peck(attacker,defender,attacking):
    s = MediaPlayer("Peck.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_petal_dance(attacker,defender,attacking):
    s = MediaPlayer("Petal Dance.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_pin_missile(attacker,defender,attacking):
    s = MediaPlayer("Pin Missle.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_poison_gas(attacker,defender,attacking):
    s = MediaPlayer("Posion Gas.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_poison_sting(attacker,defender,attacking):
    s = MediaPlayer("Poision Sting.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_poisonpowder(attacker,defender,attacking):
    s = MediaPlayer("Poison Powder.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_pound(attacker,defender,attacking):
    s = MediaPlayer("Pound.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_psybeam(attacker,defender,attacking):
    s = MediaPlayer("Psybeam.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_psychic(attacker,defender,attacking):
    s = MediaPlayer("Psychic.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_psywave(attacker,defender,attacking):
    s = MediaPlayer("Psywave.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_quick_attack(attacker,defender,attacking):
    s = MediaPlayer("Quick Attack.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_rage(attacker,defender,attacking):
    s = MediaPlayer("Rage.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_razor_leaf(attacker,defender,attacking):
    s = MediaPlayer("Razor Leaf.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_razor_wind_prep(attacker,defender,attacking):
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_razor_wind(attacker,defender,attacking):
    s = MediaPlayer("Razor Wind.mp")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_recover(attacker,defender,attacking):
    s = MediaPlayer("Recover.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_reflect(attacker,defender,attacking):
    s = MediaPlayer("Reflect.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_rest(attacker,defender,attacking):
    s = MediaPlayer("Rest.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_roar(attacker,defender,attacking):
    s = MediaPlayer(attacker.base.name + '.mp3')
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_rock_slide(attacker,defender,attacking):
    s = MediaPlayer("Rock Slide.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_rock_throw(attacker,defender,attacking):
    s = MediaPlayer("Rock Throw.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_rolling_kick(attacker,defender,attacking):
    s = MediaPlayer("Rolling Kick.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_sand_attack(attacker,defender,attacking):
    s = MediaPlayer("Sand Attack.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_scratch(attacker,defender,attacking):
    s = MediaPlayer("Scratch.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_screech(attacker,defender,attacking):
    s = MediaPlayer("Screech.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_seismic_toss(attacker,defender,attacking):
    s = MediaPlayer("Seismic Toss.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_selfdestruct(attacker,defender,attacking):
    s = MediaPlayer("Selfdestruct.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_sharpen(attacker,defender,attacking):
    s = MediaPlayer("Sharpen.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_sing(attacker,defender,attacking):
    s = MediaPlayer("Sing.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_skull_bash(attacker,defender,attacking):
    s = MediaPlayer("Skull Bash.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_skull_bash_prep(attacker,defender,attacking):
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_sky_attack(attacker,defender,attacking):
    s = MediaPlayer("Sky Attack.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_sky_attack_prep(attacker,defender,attacking):
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_slam(attacker,defender,attacking):
    s = MediaPlayer("Slam.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_slash(attacker,defender,attacking):
    s = MediaPlayer("Slash.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_sleep_powder(attacker,defender,attacking):
    s = MediaPlayer("Sleep Powder.mp")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_sludge(attacker,defender,attacking):
    s = MediaPlayer("Sludge.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_smog(attacker,defender,attacking):
    s = MediaPlayer("Smog.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_smokescreen(attacker,defender,attacking):
    s = MediaPlayer("Smokescreen.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_softboiled(attacker,defender,attacking):
    s = MediaPlayer("Softboilied.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_solarbeam_prep(attacker,defender,attacking):
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_solarbeam(attacker,defender,attacking):
    s = MediaPlayer("SolarBeam.mp3")
    s.start()
    if attacking:
        beam(attacker,defender,type_='solar')
    else:
        pass #TODO defending
    s.stop()

def do_sonicboom(attacker,defender,attacking):
    s = MediaPlayer("Sonic Boom.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_spike_cannon(attacker,defender,attacking):
    s = MediaPlayer("Spike Cannon.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_splash(attacker,defender,attacking):
    s = MediaPlayer("Spash.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_spore(attacker,defender,attacking):
    s = MediaPlayer("Spore.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_stomp(attacker,defender,attacking):
    s = MediaPlayer("Stomp.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_strength(attacker,defender,attacking):
    s = MediaPlayer("Strength.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_string_shot(attacker,defender,attacking):
    s = MediaPlayer("String Shot.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_struggle(attacker,defender,attacking):
    s = MediaPlayer("Struggle.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_stun_spore(attacker,defender,attacking):
    s = MediaPlayer("Stun Spore.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_submission(attacker,defender,attacking):
    s = MediaPlayer("Submission.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_substitute(attacker,defender,attacking):
    s = MediaPlayer("Substitute.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_super_fang(attacker,defender,attacking):
    s = MediaPlayer("Super Fang.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_supersonic(attacker,defender,attacking):
    s = MediaPlayer("Supersonic.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_surf(attacker,defender,attacking):
    s = MediaPlayer("Surf.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_swift(attacker,defender,attacking):
    s = MediaPlayer("Swift.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_swords_dance(attacker,defender,attacking):
    s = MediaPlayer("Swords Dance.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_tackle(attacker,defender,attacking):
    s = MediaPlayer("Tackle.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_tail_whip(attacker,defender,attacking):
    s = MediaPlayer("Tail Whip.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_take_down(attacker,defender,attacking):
    s = MediaPlayer("Take Down.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_teleport(attacker,defender,attacking):
    s = MediaPlayer("Teleport.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_thrash(attacker,defender,attacking):
    s = MediaPlayer("Thrash.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_thunder(attacker,defender,attacking):
    s = MediaPlayer("Thunder.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_thunder_wave(attacker,defender,attacking):
    s = MediaPlayer("Thunder Wave.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_thunderbolt(attacker,defender,attacking):
    s = MediaPlayer("Thunderbolt.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_thunderpunch(attacker,defender,attacking):
    s = MediaPlayer("Thunder Punch.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_thundershock(attacker,defender,attacking):
    s = MediaPlayer("ThunderShock.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_toxic(attacker,defender,attacking):
    s = MediaPlayer("Toxic.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_transform(attacker,defender,attacking):
    s = MediaPlayer("Transform.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_tri_attack(attacker,defender,attacking):
    s = MediaPlayer("Tri Attack.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_twineedle(attacker,defender,attacking):
    s = MediaPlayer("Twineedle.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_vicegrip(attacker,defender,attacking):
    s = MediaPlayer("Vice Grip.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_vine_whip(attacker,defender,attacking):
    s = MediaPlayer("Vine Whip.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_water_gun(attacker,defender,attacking):
    s = MediaPlayer("Water Gun.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_waterfall(attacker,defender,attacking):
    s = MediaPlayer("Waterfall.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_whirlwind(attacker,defender,attacking):
    s = MediaPlayer("Whirlwind.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_wing_attack(attacker,defender,attacking):
    s = MediaPlayer("Wing Attack.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_withdraw(attacker,defender,attacking):
    s = MediaPlayer("Withdraw.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

def do_wrap(attacker,defender,attacking):
    s = MediaPlayer("Wrap.mp3")
    s.start()
    if attacking:
        pass #TODO attacking
    else:
        pass #TODO defending
    s.stop()

