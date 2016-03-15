from sqlite3 import connect
from random import randint,random
from util import loadalphaimg
from logic import write_btm
from pygame import display
from time import sleep
from math import ceil
from redis import StrictRedis
import json

normal=['Normal','Fighting','Poison','Ground','Flying','Bug','Rock','Ghost']
special=['Fire','Water','Electric','Grass','Ice','Psychic','Dragon']

stat_stages=[1/4., 2/7., 2/6., 2/5., 1/2., 2/3., 1, 3/2., 2, 5/2., 3, 7/2., 4]

from math import floor
class pokemon(object):
    #TODO badge bonus?
    def __init__(self, id_,name, moves, lvl, evs, ivs, exp, pps, wild = False):
        self.name = name
        if name == "Farfetch'd":
            name = "Farfetch''d"
        conn = connect('shawn')
        c = conn.cursor()
        tmp = c.execute("SELECT hp, attack, defense, speed, special, exp, type1, type2, id from pokemon where pokemon = '{0}'".format(name)).fetchone()
        if wild:
            id_ = tmp[8]
            query = "SELECT move from learnablemoves where learnedat < '{0}' and pokemon = '{1}' order by learnedat desc limit 4"
            tmp2 = c.execute(query.format(lvl, name))
            for i in tmp2:
                moves.append(i[0])
                pps.append(0)
            self
        self.basecatch = c.execute("SELECT rate from catchrate where id = '{0}'".format(tmp[8])).fetchone()[0]
        self.id_ = id_
        self.attack_stage = self.defense_stage = self.speed_stage = self.special_stage = 0
        self.accuracy_stage = self.evasion_stage = 0
        self.buffs = []
        self.ttick = 0
        self.sleep = -1
        self.exp = exp
        self.lvl = lvl
        self.evs = evs
        self.ivs = ivs
        self.base = [tmp[0],tmp[1],tmp[2],tmp[3],tmp[4]]
        self.hpiv = [0,8][ivs[0] % 2] + [0,8][ivs[1] % 2] + [0,8][ivs[2] % 2] + [0,8][ivs[3] % 2]
        self.hp = self.calchp(self.base[0], self.evs[0], self.hpiv)
        self.maxhp = self.hp
        self.attack = self.calcstat(self.base[1], self.evs[1], self.ivs[0])
        self.defense = self.calcstat(self.base[2], self.evs[2], self.ivs[1])
        self.speed = self.calcstat(self.base[3], self.evs[3], self.ivs[2])
        self.special = self.calcstat(self.base[4], self.evs[4], self.ivs[3])
        self.baseexp = tmp[5]
        self.type1 = tmp[6]
        self.type2 = tmp[7]
        self.picid = tmp[8]
        self.moves = []
        for i in range(len(moves)):
            if moves[i] != '':
                self.moves.append(move(moves[i],pps[i]))
        self.sprite1 = self.set_sprite1()
        self.sprite2 = self.set_sprite2()
        self.fleecount = 0
        self.lastmove = ''
        self.lastcount = 0
        self.controllable = True
        self.disabled = 0
        self.substitute = 0
        self.struggle = move('Struggle',0)
        self.bidecnt = -1
        self.bidedmg = 0
        self.wrapped = 0
        self.thrashing = -1
        self.rage = False
        #TODO what to do with payday
        self.payday = 0
        self.confused = 0
        self.bide = False
        tmp = c.execute("SELECT speed from lvlspeed where pkmn = '{0}'".format(name)).fetchone()
        self.lvlspeed = tmp[0]
        if wild:
            self.exp = {'f': int(4 * self.lvl ** 3 / 5.),
                        'mf': self.lvl ** 3,
                        'ms': int(6/5. * self.lvl ** 3 - 15 * self.lvl ** 2 + 100 * self.lvl - 140),
                        's': int(5 * self.lvl ** 3 / 4.)}[self.lvlspeed]




    def set_sprite1(self):
        return loadalphaimg('mon1.png')

    def set_sprite2(self):
        return loadalphaimg('mon2.png')

    def calchp(self, hp, E, I):
        E = min(63,int(floor(floor((max(0, E-1)**.5)+1)/4.)))
        hp = floor((2 * hp + I + E) * self.lvl / 100. + self.lvl + 10)
        return int(hp)

    def calcstat(self, stat, E, I):
        E = min(63,int(floor(floor((max(0, E-1)**.5)+1)/4.)))
        stat = floor((2 * stat + I + E) * self.lvl / 100. + 5)
        return int(stat)

    def setimg(self, img):
        self.img = img

    def sethp(self, newhp):
        self.hp = newhp

    def limit(self, stat):
        if stat > 999:
            return 999
        return stat


    def calc_attack(self):
        return self.limit(self.attack * stat_stages[self.attack_stage + 6]* [1,.5]['BRN' in self.buffs])

    def calc_defense(self):
        return self.limit(self.defense * stat_stages[self.defense_stage + 6])

    def calc_speed(self):
        return self.limit(self.speed * stat_stages[self.speed_stage + 6]* [1,.25]['PAR' in self.buffs])

    def calc_special(self):
        return self.limit(self.special * stat_stages[self.special_stage + 6])

    def calc_accuracy(self):
        return stat_stages[self.accuracy_stage + 6]

    def calc_evasion(self):
        return stat_stages[~(self.evasion_stage + 6)]

    def valid_stat(self, stat):
        return -6 > stat or stat > 6

    def raise_attack(self, diff):
        new_attack = self.attack_stage + diff
        if self.valid_stat(new_attack):
            return False
        self.attack_stage = new_attack
        return True

    def raise_defense(self, diff):
        new_defense = self.defense_stage + diff
        if self.valid_stat(new_defense):
            return False
        self.defense_stage = new_defense
        return True

    def raise_speed(self, diff):
        new_speed = self.speed_stage + diff
        if self.valid_stat(new_speed):
            return False
        self.speed_stage = new_speed
        return True

    def raise_special(self, diff):
        new_special = self.special_stage + diff
        if self.valid_stat(new_special):
            return False
        self.special_stage = new_special
        return True

    def raise_accuracy(self, diff):
        new_accuracy = self.accuracy_stage + diff
        if self.valid_stat(new_accuracy):
            return False
        self.accuracy_stage = new_accuracy
        return True

    def raise_evasion(self, diff):
        new_evasion = self.evasion_stage + diff
        if self.valid_stat(new_evasion):
            return False
        self.evasion_stage = new_evasion
        return True

    def haze(self):
        #TODO TOXIC to PSN?
        self.attack_stage = 0
        self.defense_stage = 0
        self.speed_stage = 0
        self.special_stage = 0
        self.accuracy_stage = 0
        self.evasion_stage = 0
        self.ttick = 0
        self.buffs = []

    def heal(self, amount):
        self.hp += amount

    def do_status(self, opppkmn, me):
        from domove import dmg_pkmn
        if 'BRN' in self.buffs:
            retval = dmg_pkmn(self, int(self.maxhp*(1/8.)), not me)
            if me:
                display.update(write_btm(self.name + 'was', 'hurt by the burn'))
            else:
                display.update(write_btm('Enemy' + self.name + 'was', 'hurt by the burn'))
            sleep(1)
            if retval:
                return 1
        if 'PSN' in self.buffs:
            retval = dmg_pkmn(self, int(self.maxhp*(1/8.)), not me)
            if me:
                display.update(write_btm(self.name + 'was', 'hurt by the poison'))
            else:
                display.update(write_btm('Enemy' + self.name + 'was', 'hurt by the poison'))
            sleep(1)
            if retval:
                return 1
        if 'SEED' in self.buffs:
            retval = dmg_pkmn(self, int(self.maxhp*(1/16.)), not me)
            dmg_pkmn(opppkmn, (int(self.maxhp*(1/16.)) * -1), me)
            #TODO leech words
            display.update(write_btm('Leeched'))
            sleep(1)
            if retval:
                return 1
        if 'TOXIC' in self.buffs:
            self.hp -= self.maxhp*(tticks/8.)
            retval = dmg_pkmn(self, int(self.maxhp*(1/8.)), not me)
            if me:
                display.update(write_btm(self.name + 'was', 'hurt by the poison'))
            else:
                display.update(write_btm('Enemy' + self.name + 'was', 'hurt by the poison'))
            tticks += 1
            sleep(1)
            if retval:
                return 1
        if self.disabled > 0:
            self.disabled -= 1

    def attempt_move(self, me):
        from domove import dmg_pkmn
        #TODO keep sleep a bit OP?
        #TODO handle words here
        #TODO finish confusion
        if 'FRZ' in self.buffs:
            return 'FRZ'
        if 'PAR' in self.buffs:
            if random() < .5:
                return True
            else:
                return 'PAR'
        if 'SLP' in self.buffs:
            if self.sleep == 0:
                self.buffs.remove('SLP')
                self.sleep -= 1
                return 'WOKE'
            else:
                self.sleep -= 1
                return 'SLP'
        if self.confused > 0:
            display.update(write_btm(self.name, 'is confused'))
            self.confused -= 1
            if choice([True, False]):
                display.update(write_btm(self.name + 'hurt itself', "in it's confusion"))
                return dmg_pkmn(self, self.calc_dmg(self, 'CNF'))
            else:
                return True
        elif self.confused == 0:
            display.update(write_btm(self.name, 'is confused no more'))
            self.confused -= 1
            return True
        return True


    def crit_hit(self, high_crit):
        #TODO possible to deal less... keep or remove?
        if high_crit:
            threshold = 64.
        else:
            threshold = 512.
        if 'FCS' in self.buffs:
            threshold /= 4
        if 'DIRE' in self.buffs:
            threshold /= 4
        chance = self.speed / threshold
        if chance > 255/256.:
            chance = 255/256.

        return random() < chance


    def catch_me(self, ball):
        if ball == 'M':
            return True
        elif ball == 'U':
            x = randint(0,150)
        elif ball == 'G':
            x = randint(0,200)
        else:
            x = randint(0,255)
        if 'FRZ' in self.buffs or 'SLP' in self.buffs:
            x -= 25
        elif 'PAR' in self.buffs or 'BRN' in self.buffs or 'PSN' in self.buffs:
            x -= 12
        if x < 0:
            return True
        f = self.maxhp * 255
        if ball == 'G':
            f /= 8
        else:
            f /= 12
        r = self.hp / 4
        if r > 0:
            f /= r
        if self.basecatch < x:
            pass
        elif randint(0,255) < f:
            return True
        w = self.basecatch * 100

        if ball == 'U':
            w /= 150
        elif ball == 'G':
            w /= 200
        else:
            w /= 255
        w *= f
        w /= 255
        if 'FRZ' in self.buffs or 'SLP' in self.buffs:
            w += 10
        elif 'PAR' in self.buffs or 'BRN' in self.buffs or 'PSN' in self.buffs:
            w += 5
        if w < 10:
            return 0
        elif w < 30:
            return 1
        elif w < 70:
            return 2
        else:
            return 3


    def calc_dmg(self, opppkmn, move):
        stab = [1,1.5][self.type1 == move.type_ or self.type2 == move.type_]
        crit = self.crit_hit(move.high_crit)
        conn = connect('shawn')
        c = conn.cursor()
        type_ = 1
        if opppkmn.type2:
            build = "SELECT {0},{1} from types where type = '{2}'".format(opppkmn.type1, opppkmn.type2, move.type_)
            tmp = c.execute(build).fetchone()
            type_ *= tmp[0]
            type_ *= tmp[1]
        else:
            build = "SELECT {0} from types where type = '{1}'".format(opppkmn.type1, move.type_)
            tmp = c.execute(build).fetchone()
            type_ *= tmp[0]
        if move.type_ in normal:
            attack = self.calc_attack() * [1,.5]['burn' in self.buffs]
            defense = opppkmn.calc_defense()
        else:
            attack = self.calc_special()
            defense = opppkmn.calc_special()
        dmg = ((2 * self.lvl + 10) /250.) * (attack/float(defense)) * move.power + 2
        mod = stab * type_ * (randint(217,255) * 100 / 255./100)
        dmg *= mod
        if move.type_ in special and 'REFL' in opppkmn.buffs:
            dmg *= .5
        if move.type_ in normal and 'SCREEN' in opppkmn.buffs:
            dmg *= .5
        return [crit, type_, int(dmg)]


    def hit_or_miss(self, opppkmn, move):
        if move.acc:
            if move.name == 'Swift':
                return random() < move.acc/256.
            if 'FLY' in opppkmn.buffs or 'DIG' in opppkmn.buffs:
                return False
            acc = move.acc * self.calc_accuracy() * opppkmn.calc_evasion()
            chance = acc/256.
            if chance > 255/256.:
                chance = 255/256.
            return random() < (chance / [1,2][self.confused >= 0])
        else:
            return True

    def pp_left(self):
        return sum(i.pp for i in self.moves) > 0

    def alive(self):
        return self.hp > 0

    def inc_flee(self):
        self.fleecount += 1

    def list_moves(self):
        moves = []
        for i in self.moves:
            moves += i.name
        return moves

    def transform(self, defend):
        self.attack = defend.attack
        self.defense = defend.defense
        self.speed = defend.speed
        self.special = defend.special
        self.type1 = defend.type1
        self.type2 = defend.type2
        self.moves = defend.moves
        self.attack_stage = defend.attack_stage
        self.defense_stage = defend.defense_stage
        self.speed_stage = defend.speed_stage
        self.special_stage = defend.special_stage
        self.accuracy_stage = defend.accuracy_stage
        self.evasion_stage = defend.evasion_stage
        for i in self.move:
            self.pp = 5
            self.maxpp = 5

    def gain_exp(self,me, opp, multi):
        #TODO test exp
        if self.id_ > 151:
            self.exp += (multi * opp.current.baseexp * opp.current.lvl)/ (7 * len(me.used))
            for i in range(5):
                self.evs[i] += opp.current.base[i]
            c = 0
            while True:
                lvl = self.lvl + c
                exp = {'f': int(4 * lvl ** 3 / 5.),
                       'mf': lvl ** 3,
                       'ms': int(6/5. * lvl ** 3 - 15 * lvl ** 2 + 100 * lvl - 140),
                       's': int(5 * lvl ** 3 / 4.)}[self.lvlspeed]
                if self.exp < exp:
                    break
                c += 1
            #TODO set to actual host
            r = StrictRedis(host='127.0.0.1')
            d = {'id': self.id_, 'exp': self.exp, 'lvl': self.lvl+c, 'evs': self.evs}
            r.rpush('gain', json.dumps(d))
            return [self.lvl + c, (opp.current.baseexp * opp.current.lvl)/ (7 * len(me.used))]

    def gain_lvl(self, lvl):
        self.lvl = lvl
        self.maxhp = self.calchp(self.base[0], self.evs[0], self.hpiv)
        self.attack = self.calcstat(self.base[1], self.evs[1], self.ivs[0])
        self.defense = self.calcstat(self.base[2], self.evs[2], self.ivs[1])
        self.speed = self.calcstat(self.base[3], self.evs[3], self.ivs[2])
        self.special = self.calcstat(self.base[4], self.evs[4], self.ivs[3])


    def clean(self):
        self.hp = self.maxhp
        for i in moves:
            i.pp = i.maxpp
        self.haze()
        self.fleecount = 0
        self.lastmove = ''
        self.lastcount = 0
        self.controllable = True
        self.disabled = 0
        self.substitute = 0
        self.struggle = move('Struggle',0)
        self.bidecnt = -1
        self.bidedmg = 0
        self.wrapped = 0
        self.thrashing = -1
        self.rage = False
        #TODO what to do with payday
        self.payday = 0
        self.confused = 0
        self.bide = False













class move(object):
    def __init__(self,name,pp):
        conn = connect('shawn')
        c = conn.cursor()
        tmp = c.execute("SELECT * from moves where move = '{0}'".format(name)).fetchone()
        self.name = str(name)
        self.type_ = str(tmp[1])
        self.pp = int(tmp[2]) + pp
        self.maxpp = int(tmp[2]) + pp
        try:
            self.power = int(tmp[3])
        except ValueError:
            self.power = None
        try:
            self.acc = int(tmp[4])
        except ValueError:
            self.acc = None

        self.high_crit = False
        if self.name in ['Crabhammer','Slash','Karate Chop','Razor lear']:
            self.high_crit = True
        self.disabled = False

    def usepp(self):
        self.pp -= 1

    def has_pp(self):
        return self.pp > 0


class trainer(object):
    def __init__(self, name, pkmn):
        self.name = name
        self.pkmn = pkmn
        self.current = pkmn[0]
        self.items = []
        self.items.append(item('POKEBALL',count = 1))
        self.items.append(item('ULTRABALL',count = 9))
        self.items.append(item('GREATBALL',count = 888))
        self.items.append(item('MASTERBALL',count = 1))
        self.items.append(item('CANCEL'))
        self.shownitems = self.items[:4]
        self.used = [self.current]

    def alive(self):
        for mon in self.pkmn:
            if mon.hp > 0:
                return True
        return False

    def set_current(self, pkmn):
        if pkmn < len(self.pkmn):
            self.current = self.pkmn[pkmn]

    def num_fainted(self):
        count = 0
        for mon in self.pkmn:
            if mon.hp == 0:
                count += 1
        return count


    def get_next_pkmn(self):
        self.set_current(self.get_current_index() + 1)


    def get_current_index(self):
        return self.pkmn.index(self.current)

    def get_payday(self):
        cash = 0
        for i in pkmn:
            cash += i.payday

    def shift_items_right(self):
        y = self.items.index(self.shownitems[1])
        self.shownitems = self.items[y:y+4]

    def shift_items_left(self):
        y = self.items.index(self.shownitems[0])
        self.shownitems = self.items[y-1:y+3]

class item(object):
    def __init__(self, item, count = None):
        self.item = item
        self.count = count

    def use(self, me):
        #TODO write to DB
        self.count -= 1
        if self.count == 0:
            me.items.remove(self)
            try:
                me.shownitems.remove(self)
                me.shift_items_right()
                me.shift_items_left()
            except:
                pass
