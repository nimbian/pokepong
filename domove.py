from pygame import display
from util import choice,randint, get_random
from logic import write_btm, draw_opp_hp, draw_my_hp, wait_for_button, clean_me_up
from time import sleep
from classes import move as oneoff
from copy import deepcopy
from math import floor
DISABLE = ['Counter', 'Bide', 'Dig', 'Fly']
FLAT = ['Sonicboom', 'Dragon Rage']
MULTI = ['Spike Cannon', 'Comet Punch', 'Barrage', 'Doubleslap', 'Fury Attack', 'Pin Missile', 'Fury Swipes']
CONFUSE = ['Confuse Ray', 'Supersonic']
ESCAPE = ['Roar','Teleport','Whirlwind']
MISSDMG = ['Hi Jump Kick', 'Jump Kick']
PAR = ['Stun Spore','Thunder Wave','Glare']
PSN = ['Poison Gas','Poisonpowder']
SLP = ['Hypnosis','Lovely Kiss','Sing','Sleep Powder','Spore']
HEAL = ['Recover','Softboiled']
ABSORB = ['Dream Eater','Mega Drain','Absorb','Leech Life']
DOUBLE = ['Bonemerang','Double Kick']
EXPLOSION = ['Explosion','Selfdestruct']
THRASH = ['Thrash', 'Petal Dance']
KO = ['Fissure','Guillotine','Horn Drill']
WRAP = ['Clamp','Bind','Fire Spin','Wrap']
PREP = ['Sky Attack','Solarbeam','Skull Bash','Razor Wind', 'Dig', 'Fly']
RECOIL = ['Double-edge','Take Down','Submission', 'Struggle']
RAISEABILITY = ['Meditate','Sharpen','Swords Dance','Defense Curl','Harden',
                'Withdraw','Acid Armor','Barrier','Double Team',' Minimize',
                'Growth','Amnesia','Agility']

LOWERABILITY = ['Flash','Kinesis','Sand-Attack','Smokescreen','Growl','Leer',
                'Tail Whip','Screech','String Shot']

PROC = ['Flamethrower','Fire Punch','Ember','Psybeam','Confusion','Blizzard',
        'Ice Beam','Ice Punch','Aurora Beam','Acid','Bubblebeam','Bubble',
        'Constrict','Hyper Fang','Bone Club','Bite','Thunder','Thunderbold',
        'Thunderpunch','Thundershock','Poison Sting','Fire Blast','Psychic',
        'Headbutt','Stomp','Rolling Kick','Low Kick','Body Slam','Lick',
        'Sludge','Smog']


#TODO handle confusion mechanics

#TODO disabled Counter

#TODO disable Mirror move?

#TODO Substitute stays after switched out?

def usable_move(move, mode):
    if mode == 'pongbattle' and (move.name in DISABLE or move.name in WRAP):
        display.update(write_btm('This move is not', 'useable in this mode'))
        wait_for_button()
        return False
    if not move.has_pp():
        display.update(write_btm('No PP left!'))
        wait_for_button()
        return False
    if move.disabled:
        display.update(write_btm('This move is disabled!'))
        return False
    return True

def dmg_pkmn(pkmn, dmg, me):
    if pkmn.substitute == 0:
        if pkmn.bide:
            pkmn.bidedmg += dmg * 2
        if dmg > 0:
            for d in range(dmg):
                pkmn.sethp(pkmn.hp-1)
                if not me:
                    display.update(draw_my_hp(pkmn))
                else:
                    display.update(draw_opp_hp(pkmn))
                if pkmn.hp == 0:
                    return 1
                sleep(.02)
        else:
            for d in range(0,dmg,-1):
                if pkmn.maxhp == pkmn.hp:
                    break
                pkmn.sethp(pkmn.hp+1)
                if not me:
                    display.update(draw_my_hp(pkmn))
                else:
                    display.update(draw_opp_hp(pkmn))
                sleep(.02)

        return 0
    else:
        pkmn.substitute -= dmg
        if pkmn.substitute < 1:
            pkmn.substitute = 0
            display.update(write_btm('The substitute broke'))
            sleep(1)
            #TODO handle breaking of substitute



def do_move(attack, defend, move, mode, me, first):
    if attack.wrapped > 0:
        display.update(write_btm(attack.name, "can't move"))
        attack.wrapped -= 1
        return 0
    if move.disabled:
        display.update(write_btm('Disabled!'))
        return 0
    if attack.controllable:
        attack.lastmove = move
        move.usepp()
        if move.name in PREP:
            preping(attack, move)
            return 0
        if me:
            display.update(write_btm(attack.name, 'used {0}'.format(move.name.upper())))
        else:
            display.update(write_btm('Enemy ' + attack.name, 'used {0}'.format(move.name.upper())))
        sleep(1)
        if move.power:
            if move.name == 'Bide' and attack.bidecnt == -1:
                attack.bidecnt = choice([2,3])
                attack.controllable = False
                bide(attack)
                return 0

            if move.name == 'Hyper Beam':
                attack.controllable = False
            if attack.hit_or_miss(defend, move):
                if move.name in MULTI:
                    return multi(attack,defend,move,me)
                elif move.name in FLAT:
                    return flat(attack,defend,move,me)
                elif move.name in KO:
                    return ko(attack,defend,move,me)
                elif move.name in ABSORB:
                    return absorb(attack,defend,move,me)
                elif move.name in DOUBLE:
                    return double(attack,defend,move,me)
                elif move.name in EXPLOSION:
                    return explosion(attack,defend,move,me)
                elif move.name in RECOIL:
                    return recoil(attack,defend,move,me)
                elif move.name in PROC:
                    return proc(attack,defend,move,me,first)
                elif move.name in ['Seismic Toss', 'Night Shade']:
                    return dmg_pkmn(defend, attack.lvl, me)
                elif move.name == 'Psywave':
                    return dmg_pkmn(defend, randint(1,int(floor(attack.lvl*1.5))), me)
                elif move.name == 'Super Fang':
                    return dmg_pkmn(defend, defend.hp/2, me)
                elif move.name == 'Rage':
                    attack.controllable = False
                    attack.rage = True
                    return do_attacks(attack,defend,move,me)
                elif move.name in WRAP:
                    return wrap(attack,defend,move,me)
                elif move.name in THRASH:
                    return thrash(attack,defend,move,me)
                elif move.name == 'Pay Day':
                    attack.payday += attack.lvl * 2
                    return do_attacks(attack,defend, move, me)
                else:
                    return do_attacks(attack,defend, move, me)

            else:
                if me:
                    display.update(write_btm(attack.name + "'s", 'attack missed!'))
                else:
                    display.update(write_btm('Enemy ' + attack.name + "'s", 'attack missed!'))
                sleep(2)
                #TODO missdmg hyperbeam charge explosion?
        elif move.acc:
            if attack.hit_or_miss(defend, move):
                if move.name in LOWERABILITY:
                    lowerability(defend, move)
                elif move.name in CONFUSE:
                    confuse(defend)
                elif move.name in PSN:
                    poison(defend)
                elif move.name in PAR:
                    paralyze(defend)
                elif move.name in SLP:
                    sleeper(defend)
                elif move.name == 'Toxic':
                    toxic(defend)
                elif move.name == 'Leech Seed':
                    leech(defend)
                elif move.name == 'Disabled':
                    disable(defend)
                elif move.name == 'Mimic':
                    mimic(move,defend)

            else:
                if me:
                    display.update(write_btm(attack.name + "'s", 'attack missed!'))
                else:
                    display.update(write_btm('Enemy ' + attack.name + "'s", 'attack missed!'))
                sleep(2)
            return 0

        else:
            if move.name in RAISEABILITY:
                raiseability(attack, move)
            elif move.name == 'Focus Energy':
                attack.buffs.append('FCS')
            elif move.name == 'Splash':
                write_btm('It had no effect')
            elif move.name == 'Haze':
                attack.haze()
                defend.haze()
            elif move.name == 'Reflect':
                attack.buffs.append('REFL')
            elif move.name == 'Light Screen':
                attack.buffs.append('SCREEN')
            elif move.name == 'Rest':
                attack.buffs = ['SLP']
                attack.sleep = 2
                return dmg_pkmn(attack, dmg * -1, not me)
            elif move.name in HEAL:
                return dmg_pkmn(attack, int(attack.maxhp/2) * -1, not me)
            elif move.name == 'Substitute':
                hp = int(attack.maxhp/4)
                if hp > attack.hp:
                    display.update(write_btm('but it failed!'))
                else:
                    dmg_pkmn(attack, hp, not me)
                    attack.substitute = hp
                return 0
            elif move.name == 'Metronome':
                name = move.name
                conn = connect('shawn')
                c = conn.cursor()
                while name not in attack.list_moves() and name != 'Struggle':
                    tmp = c.execute("SELECT move from moves where rowid = '{0}'".format(randint(1,166))).fetchone()
                    name = tmp[0]
                return do_move(attack, defend, oneoff(name), mode, me)
            elif move.name == 'Transform':
                attack.transform(defend)
            elif move.name == 'Conversion':
                convert(attack)
            elif move.name == 'Mist':
                attack.buffs.append('MIST')
            elif move.name == 'Mirror Move':
                if not first and defend.lastmove and defend.lastmove.name != 'Mirror Move':
                    return do_move(attack, defend, defend.lastmove, mode, me, first)
                else:
                    display.update(write_btm('but it failed!'))
                    return 0
            return 0




    else:
        if attack.rage:
            retval = do_attacks(attack, defend, move, me)
            display.update(write_btm(attack.name +"'s", 'rage is building'))
            attack.raise_attack(1)
            sleep(1)
            return 0
        elif attack.lastmove.name == 'Hyper Beam':
            display.update(write_btm(attack.name, 'is recharging'))
            attack.controllable = True
            return 0
        elif attack.lastmove.name in PREP:
            if me:
                display.update(write_btm(attack.name, 'used {0}'.format(move.name.upper())))
            else:
                display.update(write_btm('Enemy ' + attack.name, 'used {0}'.format(move.name.upper())))
            if attack.lastmove.name == 'Fly':
                attack.buffs.pop(attack.buffs.index('FLY'))
            if attack.lastmove.name == 'Dig':
                attack.buffs.pop(attack.buffs.index('DIG'))
            if attack.hit_or_miss(defend, move):
                return do_attacks(attack, defend, move, me)
            else:
                if me:
                    display.update(write_btm(attack.name + "'s", 'attack missed!'))
                else:
                    display.update(write_btm('Enemy ' + attack.name + "'s", 'attack missed!'))
                sleep(2)
                return 0
            attack.controllable = True
        elif attack.lastmove.name == 'Bide':
            if attack.bidecnt == 0:
                attack.controllable = True
                if defend.type1 != 'Ghost':
                    retval = dmg_pkmn(defend, attack.bidedmg, me)
                else:
                    display.update(write_btm(defend.name, 'was unaffected'))
                    retval = 0
                attack.bidedmg = 0
                attack.bidecnt = -1
                attack.bide = False
                return retval
            else:
                display.update(write_btm(attack.name, 'is biding time'))
                sleep(1)
                attack.bidecnt -= 1
        elif attack.lastmove.name in WRAP:
            display.update(write_btm(attack.name+ "'s", 'attack continues'))
            defend.wrapped -= 1
            if defend.wrapped == 0:
                attack.controllable = True
            return do_attacks(attack,defend,move,me)
        elif attack.lastmove.name in THRASH:
            display.update(write_btm(attack.name, 'is thrashing about'))
            return do_attacks(attack,defend,move,me)
            if attack.thrashing > 0:
                attack.thrashing -= 1
            else:
                attack.controllable = True
                confuse(attack)
                attack.thrashing = -1





def do_attacks(attack, defend, move, me, times = 1):
    crit, type_, dmg = attack.calc_dmg(defend, move)
    for i in range(times):
        retval = dmg_pkmn(defend, dmg, me)
        if crit:
            display.update(write_btm('Critical Hit!'))
        sleep(1)
    if crit:
        sleep(1)
    if type_ > 1:
        display.update(write_btm("It's Super Effective!"))
        sleep(1)
    elif 0 < type_ < 1:
        display.update(write_btm("It wasn't", "very effective!"))
        sleep(1)
    elif type_ == 0:
        display.update(write_btm("It had no effect"))
        sleep(1)
    return retval


def multi(attack, defend, move, me):
    multi = [2,2,2,3,3,3,4,5]
    times = choice(multi)
    retval = do_attacks(attack, defend, move, me, times = times)
    display.update(write_btm('hit {0} times!'.format(times)))
    sleep(1)
    return retval

def flat(attack, defend, move, me):
    return dmg_pkmn(defend, move.power * -1, me)

def wrap(attack, defend, move, me):
    attack.controllable = False
    defend.wrapped = randint(2,5)
    return do_attacks(attack, defend, move, me)

def thrash(attack,defend,move, me):
    attack.controllable = False
    attack.thrashing = randint(2,3)
    return do_attacks(attack,defend,move,me)

def ko(attack, defend, move, me):
    if defend.calc_speed() > attack.calc_speed() or defend.lvl > attack.lvl:
        display.update(write_btm('but it failed!'))
        return 0
    else:
        return dmg_pkmn(defend, defend.hp, me)

def absorb(attack, defend, move, me):
    if move.name == 'Dream Eater':
        if 'SLP' not in defend.buffs:
            display.update(write_btm('but it failed!'))
            sleep(1)
            return 0
    crit, type_, dmg = attack.calc_dmg(defend, move)
    if crit:
        display.update(write_btm('Critical Hit!'))
        sleep(1)
    if type_ > 1:
        display.update(write_btm("It's Super Effective!"))
        sleep(1)
    elif 0 < type_ < 1:
        display.update(write_btm("It wasn't", "very effective!"))
        sleep(1)
    elif type_ == 0:
        display.update(write_btm("It had no effect"))
        sleep(1)
    retval = dmg_pkmn(defend, dmg, me)
    dmg_pkmn(attack, int(floor(dmg / 2) * -1), not me)
    return retval

def double(attack, defend, move, me):
    retval = do_attacks(attack, defend, move, me, times = 2)
    display.update(write_btm('hit {0} times!'.format(times)))
    sleep(1)
    if move.name == 'Twineedle' and get_random() < .2:
        poisoned(defend)
    return retval

def explosion(attack, defend, move, me):
    ret1 = do_attacks(attack, defend, move, me)
    ret2 = dmg_pkmn(attack, attack.hp, not me)
    if ret1 and ret2:
        return 3
    elif ret1:
        return 1
    else:
        return 2

def recoil(attack, defend, move, me):
    crit, type_, dmg = attack.calc_dmg(defend, move)
    if crit:
        display.update(write_btm('Critical Hit!'))
        sleep(1)
    if type_ > 1:
        display.update(write_btm("It's Super Effective!"))
        sleep(1)
    elif 0 < type_ < 1:
        display.update(write_btm("It wasn't", "very effective!"))
        sleep(1)
    elif type_ == 0:
        display.update(write_btm("It had no effect"))
        sleep(1)
    ret1 = dmg_pkmn(defend, dmg, me)
    ret2 = dmg_pkmn(attack, dmg / 4, not me)
    if ret1 and ret2:
        return 3
    elif ret1:
        return 1
    elif ret2:
        return 2
    else:
        return 0

def proc(attack,defend,move,me,first):
    if move.name == 'Lick' and defend.type1 == 'Psychic':
        display.update(write_btm(defend.name, 'was unaffected'))
    else:
        retval = do_attacks(attack, defend, move, me)
        if not retval:
            if move.name in ['Flamethrower','Fire Punch','Ember'] and get_random() < .1:
                burn(defend)
            elif move.name in ['Psybeam','Confusion'] and get_random() < .1:
                confuse(defend)
            elif move.name in ['Blizzard','Ice Beam','Ice Punch'] and get_random() < .1:
                freeze(defend)
            elif move.name == 'Aurora Beam' and get_random() < .1:
                stat_change(defend, -1, 'attack')
            elif move.name == 'Acid' and get_random() < .1:
                stat_change(defend, -1, 'defense')
            elif move.name in ['Bubblebeam','Bubble','Constrict'] and get_random() < .1:
                stat_change(defend, -1, 'speed')
            elif move.name in ['Hyper Fang','Bone Club','Bite'] and get_random() < .1:
                if first:
                    flinch(defend)
            elif move.name in ['Thunder','Thunderbold', 'Thunderpunch','Thundershock'] and get_random() < .1:
                paralyze(defend)
            elif move.name == 'Poison Sting' and get_random() < .2:
                poison(defend)
            elif move.name == 'Fire Blast' and get_random() < .3:
                burn(defend)
            elif move.name == 'Psychic' and get_random() < .3:
                stat_change(defend, -1, 'special')
            elif move.name in ['Headbutt','Stomp','Rolling Kick','Low Kick'] and get_random() < .3:
                if first:
                    flinch(defend)
            elif move.name in ['Lick','Body Slam'] and get_random() < .3:
                paralyze(defend)
            elif move.name in ['Sludge','Smog'] and get_random() < .3:
                poison(defend)
    return 0

def lowerability(defend, move):
    if 'MIST' not in defend.buffs:
        if move.name in ['Flash','Kinesis','Sand-Attack','Smokescreen']:
            stat_change(defend, -1, 'accuracy')
        elif move.name == 'Growl':
            stat_change(defend, -1, 'attack')
        elif move.name in ['Leer', 'Tail Whip']:
            stat_change(defend, -1, 'defense')
        elif move.name == 'Screech':
            stat_change(defend, -2, 'defense')
        elif move.name == 'String Shot':
            stat_change(defend, -1, 'speed')
    else:
        display.update(write_btm('but if failed!'))
    return 0


def raiseability(attack, move):
    if move.name in ['Meditate','Sharpen']:
        stat_change(attack, 1, 'attack')
    elif move.name == 'Swords Dance':
        stat_change(attack, 2, 'attack')
    elif move.name in ['Defense Curl', 'Harden', 'Withdraw']:
        stat_change(attack, 1, 'defense')
    elif move.name in ['Acid Armor','Barrier']:
        stat_change(attack, 2, 'defense')
    elif move.name in ['Double Team','Minimize']:
        stat_change(attack, 1, 'evasion')
    elif move.name == 'Growth':
        stat_change(attack, 1, 'special')
    elif move.name == 'Amnesia':
        stat_change(attack, 2, 'special')
    elif move.name == 'Agility':
        stat_change(attack, 2, 'speed')
    return 0


def stat_change(pokemon, diff, stat):
    if 'MIST' in pokemon.buffs and diff < 0:
        return 0
    if eval('pokemon.raise_'+stat+'('+str(diff)+')'):
        build = pokemon.name + "'s " + stat
        if diff == 2:
            tmp = 'greatly rose!'
        if diff == 1:
            tmp = 'rose!'
        if diff == -1:
            tmp = 'fell!'
        if diff == -2:
            tmp = 'greatly fell!'
        display.update(write_btm(build,tmp))
    else:
        display.update(write_btm('Nothing happened!'))
    sleep(2)
    return 0


def burn(pokemon):
    if 'BRN' in pokemon.buffs:
        return
    else:
        pokemon.buffs.append('BRN')
        display.update(write_btm(pokemon.name, 'was burned!'))
        sleep(1)

def freeze(pokemon):
    if 'FRZ' in pokemon.buffs:
        return
    else:
        pokemon.buffs.append('FRZ')
        display.update(write_btm(pokemon.name, 'has been frozen!'))
        sleep(1)

def paralyze(pokemon):
    if 'PAR' in pokemon.buffs:
        display.update(write_btm('but it failed'))
        sleep(1)
        return
    else:
        pokemon.buffs.append('PAR')
        display.update(write_btm(pokemon.name, 'was paralyzed!'))
        sleep(1)

def poisoned(pokemon):
    if 'PSN' in pokemon.buffs:
        return
    else:
        pokemon.buffs.append('PSN')
        display.update(write_btm(pokemon.name, 'was poisoned!'))
        sleep(1)

#TODO flinch only if second mon.
def flinch(pokemon):
    if 'FLINCH' in pokemon.buffs:
        return
    else:
        pokemon.buffs.append('FLINCH')

def confuse(pokemon):
    if pokemon.confused > 0:
        return
    else:
        pokemon.confused = randint(1,4)
        display.update(write_btm(pokemon.name, 'became confused!'))
        sleep(1)

def sleeper(pokemon):
    if 'SLP' in pokemon.buffs:
        display.update(write_btm('but it failed'))
        sleep(1)
        return
    else:
        pokemon.sleep = randint(1,7)
        pokemon.buffs.append('SLP')
        display.update(write_btm(pokemon.name, 'fell asleep!'))
        sleep(1)


def poisoned(pokemon):
    if 'TOXIC' in pokemon.buffs:
        display.update(write_btm('but it failed'))
        sleep(1)
        return
    else:
        pokemon.buffs.append('TOXIC')
        display.update(write_btm(pokemon.name, 'was badly poisoned!'))
        sleep(1)

def leech(pokemon):
    if 'SEED' in pokemon.buffs:
        display.update(write_btm('but it failed'))
        sleep(1)
        return
    else:
        pokemon.buffs.append('SEED')
        display.update(write_btm(pokemon.name, 'was seeded!'))
        sleep(1)

def preping(attack, move):
    attack.controllable = False
    if move.name == 'Skull Bash':
        display.update(write_btm(attack.name,  "lowered it's head"))
    elif move.name == 'Solar Beam':
        display.update(write_btm(attack.name, "is charging up"))
    elif move.name == 'Razor Wind':
        display.update(write_btm(attack.name, "is charging up"))
    elif move.name == 'Sky Attack':
        display.update(write_btm(attack.name, "started to glow"))
    elif move.name == 'Fly':
        attack.buffs.append('Fly')
        display.update(write_btm(attack.name, "flew up high"))
    elif move.name == 'Dig':
        attack.buffs.append('DIG')
        display.update(write_btm(attack.name, "dug underground"))
    sleep(1)

def disable(defend):
    if defend.disabled > 0:
        display.update(write_btm('but if failed!'))
    else:
        defend.disabled = randint(1,7)
        defend.moves[randint(0, len(defend.moves)-1)].disabled = True

def mimic(move, defend):
    pp = move.pp
    move = deepcopy(defend.moves[randint(0,len(defend.moves)-1)])
    move.pp = pp

def convert(defend):
    types = []
    for i in defend.moves:
        if i.type_ != defend.type1 and i.type_ != defend.type2:
            types += i.type_
    if types:
        defend.type1 = choice(types)
    else:
        display.update(write_btm('but if failed!'))
        sleep(1)

def bide(attack):
    attack.bide = True
