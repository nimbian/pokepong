from __future__ import absolute_import, print_function
from math import floor
from sqlalchemy import (Column,
                        Integer,
                        String,
                        Unicode,
                        Boolean,
                        DateTime,
                        ForeignKey,
                        Float)
from sqlalchemy.orm import relationship, backref, reconstructor
import random
from pokepong.database import Base
from datetime import datetime
import bcrypt
from pokepong.util import *

normal=['Normal','Fighting','Poison','Ground','Flying','Bug','Rock','Ghost']
special=['Fire','Water','Electric','Grass','Ice','Psychic','Dragon']

stat_stages=[1/4., 2/7., 2/6., 2/5., 1/2., 2/3., 1, 3/2., 2, 5/2., 3, 7/2., 4]


class LearnableHm(Base):
    __tablename__ = 'learnablehm'
    id = Column(Integer, primary_key=True)
    pokemon_id = Column(Integer, ForeignKey('pokemon.id'), nullable=False)
    pokemon = relationship('Pokemon', backref='learnablehms')
    tmhm_id = Column(Integer, ForeignKey('tmhm.id'), nullable=False)
    hm = relationship('TmHm')

class LearnableTm(Base):
    __tablename__ = 'learnabletm'
    id = Column(Integer, primary_key=True)
    pokemon_id = Column(Integer, ForeignKey('pokemon.id'), nullable=False)
    pokemon = relationship('Pokemon', backref='learnabletms')
    tmhm_id = Column(Integer, ForeignKey('tmhm.id'), nullable=False)
    tm = relationship('TmHm')

class TmHm(Base):
    __tablename__ = 'tmhm'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    move_id = Column(Integer, ForeignKey('move.id'), nullable=False)
    move = relationship('Move', backref=backref('TmHm', uselist=False))

class Type(Base):
    __tablename__ = 'type'
    id = Column(Integer, primary_key=True)
    type_ = Column(String, nullable=False)
    bug = Column(Float, nullable=False)
    dragon = Column(Float, nullable=False)
    electric = Column(Float, nullable=False)
    fighting = Column(Float, nullable=False)
    fire = Column(Float, nullable=False)
    flying = Column(Float, nullable=False)
    ghost = Column(Float, nullable=False)
    grass = Column(Float, nullable=False)
    ground = Column(Float, nullable=False)
    ice = Column(Float, nullable=False)
    normal = Column(Float, nullable=False)
    poison = Column(Float, nullable=False)
    psychic = Column(Float, nullable=False)
    rock = Column(Float, nullable=False)
    water = Column(Float, nullable=False)

class Pokedex(Base):
    __tablename__ = 'pokedex'
    id = Column(Integer, primary_key=True)
    pokemon_id = Column(Integer, ForeignKey('pokemon.id'), nullable=False)
    pokemon = relationship('Pokemon', backref=backref('pokedex', uselist=False))
    height = Column(String, nullable=False)
    weight = Column(String, nullable=False)
    entry = Column(String, nullable=False)

class LearnableMove(Base):
    __tablename__ = 'learnablemove'
    id = Column(Integer, primary_key=True)
    pokemon_id = Column(Integer, ForeignKey('pokemon.id'), nullable=False)
    pokemon = relationship('Pokemon', backref='learns')
    move_id = Column(Integer, ForeignKey('move.id'),  nullable=False)
    move = relationship('Move')
    learnedat = Column(Integer, nullable=False)

class Move(Base):
    __tablename__ = 'move'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type_id = Column(String, ForeignKey('type.id'), nullable=False)
    type_ = relationship('Type', backref='moves')
    maxpp = Column(Integer, nullable=False)
    power = Column(Integer)
    acc = Column(Integer)

    def __init__(self, move, ppup):
        self.name = move.name
        self.type_id = move.type_id
        self.type_ = move.type_
        self.maxpp = move.maxpp + ppup
        self.power = move.power
        self.acc = move.acc
        self.pp = self.maxpp
        self.high_crit = False
        if self.name in ['Crabhammer','Slash','Karate Chop','Razor lear']:
            self.high_crit = True
        self.disabled = False

    def usepp(self):
        self.pp -= 1

    def has_pp(self):
        return self.pp > 0


class Trainer(Base):
    __tablename__ = 'trainer'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    @reconstructor
    def initialize(self):
        self.battle = []
        self.usable = []
        for i in self.items:
            if i.battle:
                self.battle.append(i)
            else:
                self.usable.append(i)
        self.shownitems = self.items[:4]
        self.usable_items = self.usable[:4]

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

    def shift_usable_right(self):
        y = self.usable.index(self.shown_usable[1])
        self.shown_usable = self.usable[y:y+4]

    def shift_usable_left(self):
        y = self.usable.index(self.shown_usable[0])
        self.shown_usable = self.usable[y-1:y+3]

class Pokemon(Base):
    __tablename__ = 'pokemon'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    hp = Column(Integer)
    attack = Column(Integer)
    defence = Column(Integer)
    speed = Column(Integer)
    special = Column(Integer)
    exp = Column(Integer)
    type1 = Column(String)
    type2 = Column(String)
    lvlspeed = Column(String, nullable=False)
    evolves_to_id = Column(Integer, ForeignKey('pokemon.id'))
    evolves_at = Column(Integer)
    evolves_to = relationship('Pokemon',
                              lazy='joined',
                              join_depth=1)
    @reconstructor
    def initialize(self):
        self.struggle = Move.query.filter(Move.name == 'Struggle').one()

class Owned(Base):
    __tablename__ = 'owned'
    id = Column(Integer, primary_key=True)
    trainer_id = Column(Integer, ForeignKey('trainer.id'))
    owner = relationship('Trainer', backref='pokemon')
    base_id = Column(Integer, ForeignKey('pokemon.id'))
    base = relationship('Pokemon')
    name = Column(String)
    move1_id = Column(Integer, ForeignKey('move.id'))
    move1 = relationship('Move', foreign_keys='Owned.move1_id')
    move2_id = Column(Integer, ForeignKey('move.id'))
    move2 = relationship('Move', foreign_keys='Owned.move2_id')
    move3_id = Column(Integer, ForeignKey('move.id'))
    move3 = relationship('Move', foreign_keys='Owned.move3_id')
    move4_id = Column(Integer, ForeignKey('move.id'))
    move4 = relationship('Move', foreign_keys='Owned.move4_id')
    lvl = Column(Integer, nullable=False)
    hpev = Column(Integer, default=0)
    attackev = Column(Integer, default=0)
    defenseev = Column(Integer, default=0)
    speedev = Column(Integer, default=0)
    specialev = Column(Integer, default=0)
    attackiv = Column(Integer, default=random.randint(0,15))
    defenseiv = Column(Integer, default=random.randint(0,15))
    speediv = Column(Integer, default=random.randint(0,15))
    specialiv = Column(Integer, default=random.randint(0,15))
    exp = Column(Integer, default=0)
    pp1 = Column(Integer, default=0)
    pp2 = Column(Integer, default=0)
    pp3 = Column(Integer, default=0)
    pp4 = Column(Integer, default=0)

    @property
    def maxhp(self):
        I = [0, 8][self.attackiv % 2] + [0, 4][self.defenseiv % 2] + \
            [0, 2][self.speediv % 2] + [0, 1][self.specialiv % 2]
        E = min(63, int(floor(floor((max(0, self.hpev-1)**.5)+1)/4.)))
        stat = floor((2 * self.base.hp + I + E) * self.lvl / 100. + 5)
        return int(stat)

    def __init__(self, base_id, lvl=5):
        self.base = Pokemon.query.get(base_id)
        self.lvl = lvl
        self.name = self.base.name
        x = LearnableMove.query.filter(LearnableMove.learnedat < self.lvl) \
                               .filter(LearnableMove.pokemon_id == self.base_id).all()
        move1,move2,move3,move4 = (x[-4:]+([None] * 4))[:4]
        frontimg = loadimg('fronts/{0}.PNG'.format(base_id)).convert()
        backimg = loadimg('backs/{0}.PNG'.format(base_id)).convert()
        frontimg.set_colorkey((255,255,255))
        backimg.set_colorkey((255,255,255))
        self.frontimg = frontimg
        self.backimg = backimg
        self.moves = [move1,move2,move3,move4]
        self.hpev = 0
        self.attackev = 0
        self.defenseev = 0
        self.speedev =   0
        self.specialev = 0
        self.attackiv =  random.randint(0,15)
        self.defenseiv = random.randint(0,15)
        self.speediv =   random.randint(0,15)
        self.specialiv = random.randint(0,15)
        self.hp = self.maxhp

    @reconstructor
    def initialize(self):
        frontimg = loadimg('fronts/{0}.PNG'.format(self.base_id)).convert()
        backimg = loadimg('backs/{0}.PNG'.format(self.base_id)).convert()
        frontimg.set_colorkey((255,255,255))
        backimg.set_colorkey((255,255,255))
        self.frontimg = frontimg
        self.backimg = backimg
        self.hp = self.maxhp
        self.moves = [Move(self.move1)]
        if self.move2:
            self.moves.append(Move(self.move2))
        if self.move3:
            self.moves.append(Move(self.move3))
        if self.move4:
            self.moves.append(Move(self.move4))
        self.attack_stage = self.defense_stage = self.speed_stage = self.special_stage = 0
        self.accuracy_stage = self.evasion_stage = 0
        self.buffs = []
        self.ttick = 0
        self.sleep = -1
        self.fleecount = 0
        self.lastmove = ''
        self.lastcount = 0
        self.controllable = True
        self.disabled = 0
        self.substitute = 0
        self.bidedmg = 0
        self.wrapped = 0
        self.thrashing = -1
        self.rage = False
        #TODO what to do with payday
        self.payday = 0
        self.confused = 0
        self.bide = False
        self.bidecnt = -1

    def check_evolve(self):
        conn = connect('shawn')
        c = conn.cursor()
        query = 'select evolveto from evolve where lvl < {0} and id = {1}'.format(self.lvl,self.baseid)
        tmp = c.execute(query).fetchone()
        if tmp:
            x = c.execute("select pokemon from pokemon where id = {0}".format(tmp[0])).fetchone()
            return [tmp[0], x[0]]
        else:
            return False




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
            return 4
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
            return 4
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
            return 4
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
            moves.append("'" + i.name + "'")
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
            d = [self.lvl+c] + self.evs + [self.exp, self.id_]
            r.rpush('queue', json.dumps(['gain',d]))
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
        for i in self.moves:
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


class OwnedItem(Base):
    __tablename__ = 'owneditem'
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('items.id'))
    trainer_id = Column(Integer, ForeignKey('trainer.id'))
    owner = relationship('Trainer', backref='items')
    count = Column(Integer)

class Items(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    battle = Column(Integer)
    buyable = Column(Integer)
    buyprice = Column(Integer)
    sellprice = Column(Integer)

class shoppe(object):
    def __init__(self):
        self.items = Items.query.filter(Items.buyable == 1).all()
        self.shownitems = self.items[:4]

    def shift_items_right(self):
        y = self.items.index(self.shownitems[1])
        self.shownitems = self.items[y:y+4]

    def shift_items_left(self):
        y = self.items.index(self.shownitems[0])
        self.shownitems = self.items[y-1:y+3]

