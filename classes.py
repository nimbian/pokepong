from sqlite3 import connect
from random import randint,random
from util import loadalphaimg

normal=['Bug','Dragon','Fighting','Flying','Grass','Ground','Normal','Rock']
special=['Electric','Fire','Ghost','Ice','Poison','Psychic','Water']
stat_stages=[1/4., 2/7., 2/6., 2/5., 1/2., 2/3., 1, 3/2., 2, 5/2., 3, 7/2., 4]

from math import floor
class pokemon:
    def __init__(self, number, owned = False):
        self.attack_stage = self.defense_stage = self.speed_stage = self.special_stage = 0
        self.accuracy_stage = self.evasion_stage = 0
        self.buffs = []
        self.ttick = 0
        self.sleep = -1
        conn = connect('shawn')
        c = conn.cursor()
        tmp = c.execute("SELECT * from pkmn where id = '{0}'".format(number)).fetchone()
        self.name = tmp[1]
        self.hp = self.calchp(tmp[2])
        self.maxhp = self.hp
        self.attack = tmp[3]
        self.defense = tmp[4]
        self.speed = tmp[5]
        self.special = tmp[6]
        self.lvl = 50
        self.type1 = 'Normal'
        self.type2 = None
        self.moves = [move('Tackle'),move('Water Gun'),move('Hydro Pump'),move('Bubblebeam')]
        self.sprite1 = self.set_sprite1()
        self.sprite2 = self.set_sprite2()


    def set_sprite1(self):
        return loadalphaimg('mon1.png')

    def set_sprite2(self):
        return loadalphaimg('mon2.png')

    def calchp(self, hp, lvl = 50, E = 0, I = randint(0,15)):
        hp = floor((2 * hp + I + E) * lvl / 100. + lvl + 10)
        return int(hp)

    def calcstat(self, stat, lvl = 50, E = 0, I = randint(0,15)):
        stat = floor((2 * stat + I + E) * lvl / 100. + 5)
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
        if valid_stat(new_attack):
            return False
        self.attack_stage = new_attack
        return True

    def raise_defense(self, diff):
        new_defense = self.defense_stage + diff
        if valid_stat(new_defense):
            return False
        self.defense_stage = new_defense
        return True

    def raise_speed(self, diff):
        new_speed = self.speed_stage + diff
        if valid_stat(new_speed):
            return False
        self.speed_stage = new_speed
        return True

    def raise_special(self, diff):
        new_special = self.special_stage + diff
        if valid_stat(new_special):
            return False
        self.special_stage = new_special
        return True

    def raise_accuracy(self, diff):
        new_accuracy = self.accuracy_stage + diff
        if valid_stat(new_accuracy):
            return False
        self.accuracy_stage = new_accuracy
        return True

    def raise_evasion(self, diff):
        new_evasion = self.evasion_stage + diff
        if valid_stat(new_evasion):
            return False
        self.evasion_stage = new_evasion
        return True

    def haze(self):
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

    def do_status(self, opppkmn):
        if 'BRN' in self.buffs:
            self.hp -= self.maxhp*(1/8.)
        if 'PSN' in self.buffs:
            self.hp -= self.maxhp*(1/8.)
        if 'seed' in self.buffs:
            opppkmn.heal(max(self.hp, self.maxhp*(1/16.)))
            self.hp -= self.maxhp*(1/16.)
        if 'toxic' in self.buffs:
            self.hp -= self.maxhp*(tticks/8.)
            tticks += 1

    def attempt_move(self):
        #TODO keep sleep a bit OP?
        if 'FRZ' in self.buffs:
            return 'FRZ'
        if 'PAR' in self.buffs:
            if random() < .5:
                return True
            else:
                return 'PAR'
        if 'SLP' in self.buffs:
            if self.sleep == 0:
                self.buffs.pop(self.buffs.index('SLP'))
                self.sleep -= 1
                return 'WOKE'
            else:
                self.sleep -= 1
                return 'SLP'
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
            return -1
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
            return -1
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
        conn = connect('/home/brian.j.ramsel/shawn/shawn')
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
        return [crit, type_ > 1, int(dmg)]


    def hit_or_miss(self, opppkmn, move):
        if move.name == 'Swift':
            return random() < move.acc/256.
        if 'fly' in opppkmn.buffs or 'dig' in opppkmn.buffs:
            return False
        acc = move.acc * self.calc_accuracy() * opppkmn.calc_evasion()
        chance = acc/256.
        if chance > 255/256.:
            chance = 255/256.
        return random() < chance

    def pp_left(self):
        return sum(i.pp for i in self.moves) > 0

    def alive(self):
        return self.hp > 0



class move:
    def __init__(self,name):
        conn = connect('/home/brian.j.ramsel/shawn/shawn')
        c = conn.cursor()
        tmp = c.execute("SELECT * from moves where move = '{0}'".format(name)).fetchone()
        self.name = name
        self.type_ = tmp[1]
        self.pp = tmp[2]
        self.maxpp = tmp[2]
        self.power = tmp[3]
        self.acc = tmp[4]
        self.high_crit = False

    def usepp(self):
        self.pp -= 1

    def has_pp(self):
        return self.pp > 0


class trainer:
    def __init__(self, name, pkmn):
        self.name = name
        self.pkmn = pkmn
        self.current = pkmn[0]

    def alive(self):
        for mon in self.pkmn:
            if mon.hp > 0:
                return True
        return False

    def set_current(self, pkmn):
        if pkmn < len(self.pkmn):
            self.current = self.pkmn[pkmn]


    def get_next_pkmn(self):
        self.set_current(self.get_current_index() + 1)


    def get_current_index(self):
        return self.pkmn.index(self.current)
