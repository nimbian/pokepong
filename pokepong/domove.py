from pygame import display
from pokepong.util import choice, randint, get_random, sleep
from pokepong.util import write_btm, draw_opp_hp, draw_my_hp, wait_for_button
from pokepong.models import Move, Pokemon, tmpMove
from copy import deepcopy
from math import floor
import pokepong.move_sandbox
DISABLE = ['Counter', 'Bide', 'Dig', 'Fly']
FLAT = ['Sonicboom', 'Dragon Rage']
MULTI = ['Spike Cannon', 'Comet Punch', 'Barrage',
         'Doubleslap', 'Fury Attack', 'Pin Missile', 'Fury Swipes']
CONFUSE = ['Confuse Ray', 'Supersonic']
ESCAPE = ['Roar', 'Teleport', 'Whirlwind']
MISSDMG = ['Hi Jump Kick', 'Jump Kick']
PAR = ['Stun Spore', 'Thunder Wave', 'Glare']
PSN = ['Poison Gas', 'Poisonpowder']
SLP = ['Hypnosis', 'Lovely Kiss', 'Sing', 'Sleep Powder', 'Spore']
HEAL = ['Recover', 'Softboiled']
ABSORB = ['Dream Eater', 'Mega Drain', 'Absorb', 'Leech Life']
DOUBLE = ['Bonemerang', 'Double Kick']
EXPLOSION = ['Explosion', 'Selfdestruct']
THRASH = ['Thrash', 'Petal Dance']
KO = ['Fissure', 'Guillotine', 'Horn Drill']
WRAP = ['Clamp', 'Bind', 'Fire Spin', 'Wrap']
PREP = ['Sky Attack', 'Solarbeam', 'Skull Bash', 'Razor Wind', 'Dig', 'Fly']
RECOIL = ['Double-edge', 'Take Down', 'Submission', 'Struggle']
RAISEABILITY = ['Meditate', 'Sharpen', 'Swords Dance', 'Defense Curl', 'Harden',
                'Withdraw', 'Acid Armor', 'Barrier', 'Double Team', ' Minimize',
                'Growth', 'Amnesia', 'Agility']

LOWERABILITY = ['Flash', 'Kinesis', 'Sand-Attack', 'Smokescreen', 'Growl', 'Leer',
                'Tail Whip', 'Screech', 'String Shot']

PROC = ['Flamethrower', 'Fire Punch', 'Ember', 'Psybeam', 'Confusion', 'Blizzard',
        'Ice Beam', 'Ice Punch', 'Aurora Beam', 'Acid', 'Bubblebeam', 'Bubble',
        'Constrict', 'Hyper Fang', 'Bone Club', 'Bite', 'Thunder', 'Thunderbold',
        'Thunderpunch', 'Thundershock', 'Poison Sting', 'Fire Blast', 'Psychic',
        'Headbutt', 'Stomp', 'Rolling Kick', 'Low Kick', 'Body Slam', 'Lick',
        'Sludge', 'Smog']


# TODO handle confusion mechanics

# TODO disabled Counter

# TODO disable Mirror move?

# TODO Substitute stays after switched out?

def usable_move(move, mode):
    """
    function
    """
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
    """
    function
    """
    if pkmn.substitute == 0:
        if pkmn.bide:
            pkmn.bidedmg += dmg * 2
        if dmg > 0:
            for d in range(dmg):
                if pkmn.hp <= 0:
                    return 1
                pkmn.sethp(pkmn.hp - 1)
                if not me:
                    display.update(draw_my_hp(pkmn))
                else:
                    display.update(draw_opp_hp(pkmn))
                sleep(.02)
        else:
            for d in range(0, dmg, -1):
                if pkmn.maxhp == pkmn.hp:
                    break
                pkmn.sethp(pkmn.hp + 1)
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


def do_move(attack, defend, move, mode, me, first):
    """
    function
    """
    if mode == 'pong' and move.name != 'Transform':
        if me:
            display.update(
                write_btm(attack.name, 'used {0}'.format(move.name.upper())))
        else:
            display.update(
                write_btm('Enemy ' + attack.name, 'used {0}'.format(move.name.upper())))
        return dmg_pkmn(defend, defend.hp, me)

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
            preping(attack, move, defend, me)
            return 0
        if me:
            display.update(
                write_btm(attack.name, 'used {0}'.format(move.name.upper())))
        else:
            display.update(
                write_btm('Enemy ' + attack.name, 'used {0}'.format(move.name.upper())))
        sleep(1)
        if move.power != None:
            if move.name == 'Bide' and attack.bidecnt == -1:
                attack.bidecnt = choice([2, 3])
                attack.controllable = False
                bide(attack)
                return 0

            if move.name == 'Hyper Beam':
                attack.controllable = False
            if attack.hit_or_miss(defend, move):
                if move.name in MULTI:
                    return multi(attack, defend, move, me)
                elif move.name in FLAT:
                    return flat(attack, defend, move, me)
                elif move.name in KO:
                    return ko(attack, defend, move, me)
                elif move.name in ABSORB:
                    return absorb(attack, defend, move, me)
                elif move.name in DOUBLE:
                    return double(attack, defend, move, me)
                elif move.name in EXPLOSION:
                    return explosion(attack, defend, move, me)
                elif move.name in RECOIL:
                    return recoil(attack, defend, move, me)
                elif move.name in PROC:
                    return proc(attack, defend, move, me, first)
                elif move.name in ['Seismic Toss', 'Night Shade']:
                    tmp = dmg_pkmn(defend, attack.lvl, me)
                    meth = getattr(
                        pokepong.move_sandbox, 'do_' + move.name.lower().replace(' ', '_').replace('-', '_'))
                    meth(attack, defend, me)
                    return tmp
                elif move.name == 'Psywave':
                    tmp = dmg_pkmn(defend, randint(1, int(floor(attack.lvl * 1.5))), me)
                    pokepong.move_sandbox.do_psywave(attack, defend, me)
                    return tmp
                elif move.name == 'Super Fang':
                    tmp = dmg_pkmn(defend, defend.hp / 2, me)
                    pokepong.move_sandbox.do_super_fang(attack, defend, me)
                    return tmp
                elif move.name == 'Rage':
                    attack.controllable = False
                    attack.rage = True
                    return do_attacks(attack, defend, move, me)
                elif move.name in WRAP:
                    return wrap(attack, defend, move, me)
                elif move.name in THRASH:
                    return thrash(attack, defend, move, me)
                elif move.name == 'Pay Day':
                    attack.payday += attack.lvl * 2
                    return do_attacks(attack, defend, move, me)
                else:
                    return do_attacks(attack, defend, move, me)

            else:
                if me:
                    display.update(
                        write_btm(attack.name + "'s", 'attack missed!'))
                else:
                    display.update(
                        write_btm('Enemy ' + attack.name + "'s", 'attack missed!'))
                sleep(2)
                # TODO missdmg hyperbeam charge explosion?
        elif move.acc:
            if attack.hit_or_miss(defend, move):
                if move.name in LOWERABILITY:
                    lowerability(defend, move, attack, me)
                else:
                    if move.name in CONFUSE:
                        tmp = defend.confused < 1
                    elif move.name in PSN:
                        tmp = 'PSN' not in defend.buffs
                    elif move.name in PAR:
                        tmp = 'PAR' not in defend.buffs
                    elif move.name in SLP:
                        tmp = 'SLP' not in defend.buffs
                    elif move.name == 'Toxic':
                        tmp = 'PSN' not in defend.buffs
                    elif move.name == 'Leech Seed':
                        tmp = 'SEED' not in defend.buffs
                    elif move.name == 'Disable':
                        tmp = defend.disabled < 1
                    elif move.name == 'Mimic':
                        tmp = True
                    elif move.name == 'Roar' or move.name == 'Whirlwind':
                        #TODO needs to end battle
                        if mode == 'wild':
                            tmp = 1
                        else:
                            tmp = 0
                    if tmp:
                        meth = getattr(
                            pokepong.move_sandbox, 'do_' + move.name.lower().replace(' ', '_').replace('-', '_'))
                        meth(attack, defend, me)
                    if move.name in CONFUSE:
                        tmp = confuse(defend)
                    elif move.name in PSN:
                        tmp = poisoned(defend)
                    elif move.name in PAR:
                        tmp = paralyze(defend)
                    elif move.name in SLP:
                        tmp = sleeper(defend)
                    elif move.name == 'Toxic':
                        tmp = toxic(defend)
                    elif move.name == 'Leech Seed':
                        tmp = leech(defend)
                    elif move.name == 'Disable':
                        tmp = disable(defend)
                    elif move.name == 'Mimic':
                        tmp = mimic(move, defend)
                    if not tmp:
                        display.update(write_btm('but it failed!'))
                        sleep(1)



            else:
                if me:
                    display.update(
                        write_btm(attack.name + "'s", 'attack missed!'))
                else:
                    display.update(
                        write_btm('Enemy ' + attack.name + "'s", 'attack missed!'))
                sleep(2)
            return 0

        else:
            if move.name in RAISEABILITY:
                raiseability(attack, move, defend, me)
            elif move.name == 'Focus Energy':
                if 'FCS' not in attack.buffs:
                    attack.buffs.append('FCS')
                    pokepong.move_sandbox.do_focus_energy(attack, defend, me)
                else:
                    display.update(write_btm('but it failed!'))
            elif move.name == 'Splash':
                pokepong.move_sandbox.do_splash(attack, defend, me)
                display.update(write_btm('It had no effect'))
            elif move.name == 'Haze':
                pokepong.move_sandbox.do_haze(attack, defend, me)
                attack.haze()
                defend.haze()
            elif move.name == 'Reflect':
                if 'REFL' not in attack.buffs:
                    attack.buffs.append('REFL')
                    pokepong.move_sandbox.do_reflect(attack, defend, me)
                else:
                    display.update(write_btm('but it failed!'))
            elif move.name == 'Light Screen':
                if 'SCREEN' not in attack.buffs:
                    attack.buffs.append('SCREEN')
                    pokepong.move_sandbox.do_light_screen(attack, defend, me)
                else:
                    display.update(write_btm('but it failed!'))
            elif move.name == 'Rest':
                pokepong.move_sandbox.do_rest(attack, defend, me)
                attack.buffs = ['SLP']
                attack.sleep = 2
                attack.haze()
                dmg_pkmn(attack, (attack.maxhp - attack.hp) * -1, not me)
                display.update(write_btm(attack.name, 'fell asleep'))
            elif move.name in HEAL:
                meth = getattr(
                    pokepong.move_sandbox, 'do_' + move.name.lower().replace(' ', '_').replace('-', '_'))
                meth(attack, defend, me)

                return dmg_pkmn(attack, int(attack.maxhp / 2) * -1, not me)
            elif move.name == 'Substitute':
                hp = int(attack.maxhp / 4)
                if hp > attack.hp:
                    display.update(write_btm('but it failed!'))
                else:
                    pokepong.move_sandbox.do_substitute(attack, defend, me)
                    dmg_pkmn(attack, hp, not me)
                    attack.substitute = hp
                return 0
            elif move.name == 'Metronome':
                name = move.name
                while 'Struggle' != move.name not in attack.list_moves():
                    move = Move.query.get(randint(1, 166))
                pokepong.move_sandbox.do_metronome(attack, defend, me)
                return do_move(attack, defend, tmpMove(move, 0), mode, me, first)
            elif move.name == 'Transform':
                attack.transform(defend)
                pokepong.move_sandbox.do_transform(attack, defend, me)
            elif move.name == 'Conversion':
                convert(attack, defend, me)
            elif move.name == 'Mist':
                pokepong.move_sandbox.do_mist(attack, defend, me)
                attack.buffs.append('MIST')
            elif move.name == 'Mirror Move':
                if not first and defend.lastmove and defend.lastmove.name != 'Mirror Move':
                    return do_move(attack, defend, defend.lastmove, mode, me, first)
                else:
                    display.update(write_btm('but it failed!'))
                    return 0
            elif move.name == 'Teleport':
                #TODO should end battle
                if mode == 'wild':
                    pokepong.move_sandbox.do_teleport(attack, defend, me)
                else:
                    display.update(write_btm('but it failed!'))
            return 0

    else:
        if attack.rage:
            retval = do_attacks(attack, defend, move, me)
            display.update(write_btm(attack.name + "'s", 'rage is building'))
            attack.raise_attack(1)
            sleep(1)
            return 0
        elif attack.lastmove.name == 'Hyper Beam':
            display.update(write_btm(attack.name, 'is recharging'))
            attack.controllable = True
            return 0
        elif attack.lastmove.name in PREP:
            if me:
                display.update(
                    write_btm(attack.name, 'used {0}'.format(move.name.upper())))
            else:
                display.update(
                    write_btm('Enemy ' + attack.name, 'used {0}'.format(move.name.upper())))
            if attack.lastmove.name == 'Fly':
                attack.buffs.pop(attack.buffs.index('FLY'))
            if attack.lastmove.name == 'Dig':
                attack.buffs.pop(attack.buffs.index('DIG'))
            if attack.hit_or_miss(defend, move):
                attack.controllable = True
                return do_attacks(attack, defend, move, me)
            else:
                if me:
                    display.update(
                        write_btm(attack.name + "'s", 'attack missed!'))
                else:
                    display.update(
                        write_btm('Enemy ' + attack.name + "'s", 'attack missed!'))
                sleep(2)
                attack.controllable = True
                return 0
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
            display.update(write_btm(attack.name + "'s", 'attack continues'))
            defend.wrapped -= 1
            if defend.wrapped <= 0:
                attack.controllable = True
            return do_attacks(attack, defend, move, me)
        elif attack.lastmove.name in THRASH:
            display.update(write_btm(attack.name, 'is thrashing about'))
            return do_attacks(attack, defend, move, me)
        if attack.thrashing > 0:
            attack.thrashing -= 1
        else:
            attack.controllable = True
            confuse(attack)
            attack.thrashing = -1


def do_attacks(attack, defend, move, me, times=1):
    """
    function
    """
    crit, type_, dmg = attack.calc_dmg(defend, move)
    meth = getattr(
        pokepong.move_sandbox, 'do_' + move.name.lower().replace(' ', '_').replace('-', '_'))
    meth(attack, defend, me)
    for i in range(times):
        retval = dmg_pkmn(defend, dmg, me)
        if crit and type_ > 0:
            display.update(write_btm('Critical Hit!'))
        if retval == 1:
            break
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
    """
    function
    """
    multi_ = [2, 2, 2, 3, 3, 3, 4, 5]
    times = choice(multi_)
    retval = do_attacks(attack, defend, move, me, times=times)
    display.update(write_btm('hit {0} times!'.format(times)))
    sleep(1)
    return retval


def flat(attack, defend, move, me):
    """
    function
    """
    tmp = dmg_pkmn(defend, move.power * -1, me)
    meth = getattr(
        pokepong.move_sandbox, 'do_' + move.name.lower().replace(' ', '_').replace('-', '_'))
    meth(attack, defend, me)
    return tmp


def wrap(attack, defend, move, me):
    """
    function
    """
    attack.controllable = False
    defend.wrapped = randint(3, 7)
    return do_attacks(attack, defend, move, me)


def thrash(attack, defend, move, me):
    """
    function
    """
    attack.controllable = False
    attack.thrashing = randint(2, 3)
    return do_attacks(attack, defend, move, me)


def ko(attack, defend, move, me):
    """
    function
    """
    if defend.calc_speed() > attack.calc_speed() or defend.lvl > attack.lvl:
        display.update(write_btm('but it failed!'))
        return 0
    else:
        meth = getattr(
            pokepong.move_sandbox, 'do_' + move.name.lower().replace(' ', '_').replace('-', '_'))
        meth(attack, defend, me)
        return dmg_pkmn(defend, defend.hp, me)


def absorb(attack, defend, move, me):
    """
    function
    """
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
    if retval:
        meth = getattr(
            pokepong.move_sandbox, 'do_' + move.name.lower().replace(' ', '_').replace('-', '_'))
        meth(attack, defend, me)
    dmg_pkmn(attack, int(floor(dmg / 2) * -1), not me)
    return retval


def double(attack, defend, move, me):
    """
    function
    """
    retval = do_attacks(attack, defend, move, me, times=2)
    display.update(write_btm('hit {0} times!'.format(2)))
    sleep(1)
    if move.name == 'Twineedle' and get_random() < .2:
        poisoned(defend)
    return retval


def explosion(attack, defend, move, me):
    """
    function
    """
    ret1 = do_attacks(attack, defend, move, me)
    ret2 = dmg_pkmn(attack, attack.hp, not me)
    if ret1 and ret2:
        return 3
    elif ret1:
        return 1
    else:
        return 2


def recoil(attack, defend, move, me):
    """
    function
    """
    crit, type_, dmg = attack.calc_dmg(defend, move)
    ret1 = dmg_pkmn(defend, dmg, me)
    if dmg:
        meth = getattr(
            pokepong.move_sandbox, 'do_' + move.name.lower().replace(' ', '_').replace('-', '_'))
        meth(attack, defend, me)
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
    ret2 = dmg_pkmn(attack, dmg / 4, not me)
    if ret2:
        display.update(write_btm(attack.name + ' was', 'hit with recoil!'))
    if ret1 and ret2:
        return 3
    elif ret1:
        return 1
    elif ret2:
        return 2
    else:
        return 0


def proc(attack, defend, move, me, first):
    """
    function
    """
    if move.name == 'Lick' and defend.base.type1 == 'Psychic':
        display.update(write_btm(defend.name, 'was unaffected'))
    else:
        retval = do_attacks(attack, defend, move, me)
        if not retval:
            if move.name in ['Flamethrower', 'Fire Punch', 'Ember'] and get_random() < .1:
                burn(defend)
            elif move.name in ['Psybeam', 'Confusion'] and get_random() < .1:
                confuse(defend)
            elif move.name in ['Blizzard', 'Ice Beam', 'Ice Punch'] and get_random() < .1:
                freeze(defend)
            elif move.name == 'Aurora Beam' and get_random() < .1:
                diff, stat = stat_change(defend, -1, 'attack')
                if diff:
                    display_stat(defend, diff, stat)
            elif move.name == 'Acid' and get_random() < .1:
                diff, stat = stat_change(defend, -1, 'defense')
                if diff:
                    display_stat(defend, diff, stat)
            elif move.name in ['Bubblebeam', 'Bubble', 'Constrict'] and get_random() < .1:
                diff, stat = stat_change(defend, -1, 'speed')
                if diff:
                    display_stat(defend, diff, stat)
            elif move.name in ['Hyper Fang', 'Bone Club', 'Bite'] and get_random() < .1:
                if first:
                    flinch(defend)
            elif move.name in ['Thunder', 'Thunderbold', 'Thunderpunch', 'Thundershock'] and get_random() < .1:
                paralyze(defend)
            elif move.name == 'Poison Sting' and get_random() < .2:
                poisoned(defend)
            elif move.name == 'Fire Blast' and get_random() < .3:
                burn(defend)
            elif move.name == 'Psychic' and get_random() < .3:
                diff, stat = stat_change(defend, -1, 'special')
                if diff:
                    display_stat(defend, diff, stat)

            elif move.name in ['Headbutt', 'Stomp', 'Rolling Kick', 'Low Kick'] and get_random() < .3:
                if first:
                    flinch(defend)
            elif move.name in ['Lick', 'Body Slam'] and get_random() < .3:
                paralyze(defend)
            elif move.name in ['Sludge', 'Smog'] and get_random() < .3:
                poisoned(defend)
    return 0


def display_stat(defend, diff, stat):
    build = defend.name + "'s " + stat
    if diff == 2:
        tmp = 'greatly rose!'
    if diff == 1:
        tmp = 'rose!'
    if diff == -1:
        tmp = 'fell!'
    if diff == -2:
        tmp = 'greatly fell!'
    display.update(write_btm(build, tmp))
    wait_for_button()


def lowerability(defend, move, attack, me):
    """
    function
    """
    if 'MIST' not in defend.buffs:
        if move.name in ['Flash', 'Kinesis', 'Sand-Attack', 'Smokescreen']:
            diff, stat = stat_change(defend, -1, 'accuracy')
        elif move.name == 'Growl':
            diff, stat = stat_change(defend, -1, 'attack')
        elif move.name in ['Leer', 'Tail Whip']:
            diff, stat = stat_change(defend, -1, 'defense')
        elif move.name == 'Screech':
            diff, stat = stat_change(defend, -2, 'defense')
        elif move.name == 'String Shot':
            diff, stat = stat_change(defend, -1, 'speed')
        if diff:
            meth = getattr(
                pokepong.move_sandbox, 'do_' + move.name.lower().replace(' ', '_').replace('-', '_'))
            meth(attack, defend, me)
            build = defend.name + "'s " + stat
            if diff == 2:
                tmp = 'greatly rose!'
            if diff == 1:
                tmp = 'rose!'
            if diff == -1:
                tmp = 'fell!'
            if diff == -2:
                tmp = 'greatly fell!'
            display.update(write_btm(build, tmp))
        else:
            display.update(write_btm('But nothing happened!'))

    else:
        display.update(write_btm('but if failed!'))
    wait_for_button()
    return 0


def raiseability(attack, move, defend, me):
    """
    function
    """
    if move.name in ['Meditate', 'Sharpen']:
        diff, stat = stat_change(attack, 1, 'attack')
    elif move.name == 'Swords Dance':
        diff, stat = stat_change(attack, 2, 'attack')
    elif move.name in ['Defense Curl', 'Harden', 'Withdraw']:
        diff, stat = stat_change(attack, 1, 'defense')
    elif move.name in ['Acid Armor', 'Barrier']:
        diff, stat = stat_change(attack, 2, 'defense')
    elif move.name in ['Double Team', 'Minimize']:
        diff, stat = stat_change(attack, 1, 'evasion')
    elif move.name == 'Growth':
        diff, stat = stat_change(attack, 1, 'special')
    elif move.name == 'Amnesia':
        diff, stat = stat_change(attack, 2, 'special')
    elif move.name == 'Agility':
        diff, stat = stat_change(attack, 2, 'speed')
    if diff:
        meth = getattr(
            pokepong.move_sandbox, 'do_' + move.name.lower().replace(' ', '_').replace('-', '_'))
        meth(attack, defend, me)
        build = attack.name + "'s " + stat
        if diff == 2:
            tmp = 'greatly rose!'
        if diff == 1:
            tmp = 'rose!'
        if diff == -1:
            tmp = 'fell!'
        if diff == -2:
            tmp = 'greatly fell!'
        display.update(write_btm(build, tmp))
    else:
        display.update(write_btm('But nothing happened!'))
    wait_for_button()
    return 0


def stat_change(pokemon, diff, stat):
    """
    function
    """
    if 'MIST' in pokemon.buffs and diff < 0:
        return [0, stat]
    meth = getattr(pokemon, 'raise_' + stat)
    if meth(diff):
        return [diff, stat]
    else:
        return [0, stat]


def burn(pokemon):
    """
    function
    """
    if 'BRN' in pokemon.buffs:
        return 0
    else:
        pokemon.buffs.append('BRN')
        display.update(write_btm(pokemon.name, 'was burned!'))
        sleep(1)


def freeze(pokemon):
    """
    function
    """
    if 'FRZ' in pokemon.buffs:
        return 0
    else:
        pokemon.buffs.append('FRZ')
        display.update(write_btm(pokemon.name, 'has been frozen!'))
        sleep(1)


def paralyze(pokemon):
    """
    function
    """
    if 'PAR' in pokemon.buffs:
        display.update(write_btm('but it failed'))
        sleep(1)
        return 0
    else:
        pokemon.buffs.append('PAR')
        display.update(write_btm(pokemon.name, 'was paralyzed!'))
        sleep(1)


def poisoned(pokemon):
    """
    function
    """
    if 'PSN' in pokemon.buffs:
        return
    else:
        pokemon.buffs.append('PSN')
        display.update(write_btm(pokemon.name, 'was poisoned!'))
        sleep(1)


def flinch(pokemon):
    """
    function
    """
    if 'FLINCH' in pokemon.buffs:
        return 0
    else:
        pokemon.buffs.append('FLINCH')


def confuse(pokemon):
    """
    function
    """
    if pokemon.confused > 0:
        return 0
    else:
        pokemon.confused = randint(1, 4)
        display.update(write_btm(pokemon.name, 'became confused!'))
        sleep(1)
        return 1


def sleeper(pokemon):
    """
    function
    """
    if 'SLP' in pokemon.buffs:
        display.update(write_btm('but it failed'))
        sleep(1)
        return 0
    else:
        pokemon.sleep = randint(1, 7)
        pokemon.buffs.append('SLP')
        display.update(write_btm(pokemon.name, 'fell asleep!'))
        sleep(1)
        return 1


def toxic(pokemon):
    """
    function
    """
    if 'TOXIC' in pokemon.buffs:
        display.update(write_btm('but it failed'))
        sleep(1)
        return 0
    else:
        pokemon.buffs.append('TOXIC')
        display.update(write_btm(pokemon.name, 'was badly poisoned!'))
        sleep(1)
        return 1


def leech(pokemon):
    """
    function
    """
    if 'SEED' in pokemon.buffs:
        display.update(write_btm('but it failed'))
        sleep(1)
        return 0
    else:
        pokemon.buffs.append('SEED')
        display.update(write_btm(pokemon.name, 'was seeded!'))
        sleep(1)
        return 1


def preping(attack, move, defend, me):
    """
    function
    """
    meth = getattr(
        pokepong.move_sandbox, 'do_' + move.name.lower().replace(' ', '_').replace('-', '_')+ '_prep')
    meth(attack, defend, me)
    attack.controllable = False
    if move.name == 'Skull Bash':
        display.update(write_btm(attack.name, "lowered it's head"))
    elif move.name == 'Solarbeam':
        display.update(write_btm(attack.name, "is charging up"))
    elif move.name == 'Razor Wind':
        display.update(write_btm(attack.name, "is charging up"))
    elif move.name == 'Sky Attack':
        display.update(write_btm(attack.name, "started to glow"))
    elif move.name == 'Fly':
        attack.buffs.append('FLY')
        display.update(write_btm(attack.name, "flew up high"))
    elif move.name == 'Dig':
        attack.buffs.append('DIG')
        display.update(write_btm(attack.name, "dug underground"))
    sleep(1)


def disable(defend):
    """
    function
    """
    if defend.disabled > 0:
        display.update(write_btm('but if failed!'))
        sleep(1)
        return 0
    else:
        defend.disabled = randint(1, 7)
        defend.moves[randint(0, len(defend.moves) - 1)].disabled = True
        sleep(1)
        return 1


def mimic(move, defend):
    """
    function
    """
    pp = move.pp
    move = deepcopy(defend.moves[randint(0, len(defend.moves) - 1)])
    move.pp = pp


def convert(attack, defend, me):
    """
    function
    """
    types = []
    for i in attack.moves:
        if i.type_ != attack.base.type1 and i.type_ != attack.base.type2:
            types.append(i.type_)
    if types:
        attack.base.type1 = choice(types)
        pokepong.move_sandbox.do_conversion(attack, defend, me)
    else:
        display.update(write_btm('but if failed!'))
        sleep(1)


def bide(attack):
    """
    function
    """
    attack.bide = True
