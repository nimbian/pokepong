# TODO remove when done testing
from pygame import display, joystick
from pokepong.util import send_move, recv_move, MyMoveOccuring, OppMoveOccuring
from pokepong.util import send_team, get_team, loadimg, set_client, get_client
from pokepong.util import Sound, GYMS, get_prize, write_btm, sleep
from pokepong.logic import shop, get_wild_mon, draw_all_opp, draw_all_me, enter_pin
from pokepong.logic import win, lost, opp_next_mon, gain_exp, evolve, play_again
from pokepong.logic import battle_logic, run_opp_faint, run_me_faint, get_badge
from pokepong.logic import me_next_mon, new_game_start, clear, conf, recv_prize
from pokepong.logic import draw_choice, scrolling, choose_loc, intro, trainer_intro
from pokepong.logic import clearbtm, run_game, get_trainers, get_mon, wild_intro, overtime
from pokepong.models import Trainer, Owned
from redis import StrictRedis
from .config import _cfg
import json
import zmq
joystick.init()
sleep(1)
try:
        tmp = joystick.Joystick(0)
        tmp.init()
except:
        pass

MINI = Sound("sounds/miniOpening.ogg")
OPENING = Sound("sounds/intro.ogg")


def main():
    if int(_cfg('table-number')) == 1:
        set_client(False)
    else:
        set_client(True)
    # TODO set to actual IP
    r = StrictRedis(host=_cfg('redis'))
    r.delete('lock')
    r.delete('leader')
    poss = [1, 4, 7, 25, 143, 132, 129, 123, 95, 92, 77, 13, 17, 21, 35]
    possible = []
    for p in poss:
        pkmn = loadimg('fronts/{0}.PNG'.format(p)).convert()
        pkmn.set_colorkey((255, 255, 255))
        possible.append(pkmn)
        if p == 4:
            current = pkmn
    socket = None
    mode = ''
    count = 0
    king = None
    new_game = True
    me = None
    remember = 0
    r.incr('count')
    while int(r.get('count')) < 2:
        sleep(.5)
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    if get_client():
        socket.connect("tcp://{0}:7777".format(_cfg('zmq')))
    else:
        socket.bind("tcp://*:7777")
    sleep(1)
    socket.send('')
    socket.recv()
    r.delete('count')
    while True:
        gym = False
        oldmode = mode
        mode = r.get('mode')
        if not mode:
            mode = 'pong'
            r.set('mode', 'pong')
        elif mode != oldmode:
            me = None
            opp = None
            count = 0
            if mode == 'wild':
                music = Sound("sounds/wild_battle.ogg")
                music_vict = Sound("sounds/wild_victory.ogg")
            else:
                music = Sound("sounds/trainer_battle.ogg")
                music_vict = Sound("sounds/trainer_victory.ogg")
        if new_game or (not king and mode != 'wild'):
            MINI.play()
            intro(current)
            MINI.stop()
            # TODO uncomment for PROD
            # sleep(5)
        OPENING.play(-1)
        while new_game or mode != 'wild':
            if r.get('leader'):
                gym = True
                break
            tmp = None
            try:
                if king != 'me':
                    tmp = json.loads(r.lpop('lineup'))
                else:
                    tmp = {'name':myname, 'pokemon':mypkmnlist}
            except TypeError:
                pass
            if tmp:
                myname = tmp['name']
                mypkmnlist = tmp['pokemon']
                if mode != 'wild':
                    send_team(myname, mypkmnlist, socket, get_client())
                break
            current = scrolling(current, possible)
            # TODO uncomment for PROD
            # sleep(5)
        if not gym:
            if mode == 'wild' or mode == 'battle':
                me = Trainer.query.filter(Trainer.name == myname).one()
                try:
                    me.pkmn
                except AttributeError:
                    me.pkmn = []
                    for mon in mypkmnlist:
                        me.pkmn.append(Owned.query.get(mon))
                me.current = me.pkmn[0]
                me.used = set()
                me.used.add(me.current)
            else:
                me = Trainer(myname)
                me.initialize()
                me.pkmn = []
                for mon in mypkmnlist:
                    me.pkmn.append(Owned(mon, lvl=10))
                    me.current = me.pkmn[0]
                me.used = set()
                me.used.add(me.current)

        while mode != 'wild':
            try:
                oppname, opppkmnlist = get_team(socket, get_client())
                if mode != 'pong':
                    opp = Trainer.query.filter(Trainer.name == oppname).one()
                else:
                    opp = Trainer(oppname)
                opp.pkmn = []
                if mode != 'pong':
                    for mon in opppkmnlist:
                        opp.pkmn.append(Owned.query.get(mon))
                else:
                    for mon in opppkmnlist:
                        opp.pkmn.append(Owned(mon, lvl=10))
                opp.current = opp.pkmn[0]
                break
            except zmq.Again:
                current = scrolling(current, possible)
                # TODO uncomment for PROD
                # sleep(5)
        if mode == 'wild':
            if not gym:
                loc, wild, remember = choose_loc(remember, me)
                if loc == False:
                    new_game = True
                    continue
            else:
                wild = 'leader'
            if wild == 'leader':
                mode = 'gym'
                challenger = False
                tmp = r.get('leader')
                name = GYMS[tmp][0]
                ret = enter_pin(name)
                if ret:
                    socket.send('ok')
                else:
                    socket.send('bad')
                    continue
                team = GYMS[tmp][1]
                send_team(name, team, socket, get_client())
                me = Trainer(name)
                me.initialize()
                me.pkmn = []
                for mon in team:
                    me.pkmn.append(Owned.query.get(mon))
                    me.current = me.pkmn[0]
                me.used = set()
                me.used.add(me.current)
                while True:
                    try:
                        oppname, opppkmnlist = get_team(socket, get_client())
                        opp = Trainer.query.filter(Trainer.name == oppname).one()
                        opp.pkmn = []
                        for mon in opppkmnlist:
                            opp.pkmn.append(Owned.query.get(mon))
                        opp.current = opp.pkmn[0]
                        break
                    except zmq.Again:
                        pass
            else:
                new_game = False
                OPENING.stop()
                if loc == 'PALLET TOWN':
                    shop(me)
                    continue
                elif loc in GYMS:
                    if conf():
                        mode = 'gym'
                        r.set('leader', loc)
                        if socket.recv() == 'bad':
                            continue
                        r.delete('ptable1')
                        r.delete('ptable2')
                        challenger = True
                        send_team(myname, mypkmnlist, socket, get_client())
                        while True:
                            try:
                                oppname, opppkmnlist = get_team(socket, get_client())
                                opp = Trainer(oppname)
                                opp.money = 2400
                                opp.pkmn = []
                                for mon in opppkmnlist:
                                    opp.pkmn.append(Owned.query.get(mon))
                                opp.current = opp.pkmn[0]
                                break
                            except zmq.Again:
                                pass
                    else:
                        continue
                else:
                    if wild == 'wild':
                        opp = Trainer('')
                        opp.pkmn = [get_wild_mon(loc)]
                        opp.current = opp.pkmn[0]
                        wild_intro()
                    else:
                        mode = 'random'
                        trainer = get_trainers(loc)
                        opp = Trainer(trainer[0])
                        opp.money = trainer[1]
                        opp.pkmn = []
                        for i in trainer[2]:
                            opp.pkmn.append(get_mon(i[0], i[1]))
                        opp.current = opp.pkmn[0]
                        trainer_intro()
        if mode != 'wild' and mode != 'random':
            socket.send('')
            socket.recv()
        OPENING.stop()
        opp.initialize()
        music.play()
        if mode == 'battle':
            prize = get_prize(me, opp)
            clear()
            write_btm('You are playing', 'for a {0}'.format(prize))
            display.flip()
            sleep(2)
        r.delete('table1')
        r.delete('table2')
        r.delete('ptable1')
        r.delete('ptable2')
        for mon in me.pkmn:
            mon.haze
            mon.hp = mon.maxhp
        for mon in opp.pkmn:
            mon.haze
            mon.hp = mon.maxhp

        new_game_start(me, opp, mode)
        while me.alive() and opp.alive():
            try:
                clearbtm()
                draw_choice(0)
                tmp = run_game(me, opp, mode, socket)
            except OppMoveOccuring:
                clear()
                display.flip()
                draw_all_opp(opp.current)
                draw_all_me(me.current)
                move = recv_move(socket)
                tmp = battle_logic(me, opp, move, False)
            except MyMoveOccuring as move:
                clear()
                display.flip()
                draw_all_opp(opp.current)
                draw_all_me(me.current)
                send_move(move, socket)
                tmp = battle_logic(me, opp, move, True)
                r.delete('lock')
            if tmp == 0:
                run_opp_faint(opp)
                if mode == 'random' or mode == 'wild':
                    gain_exp(me, opp, [1.5, 1][mode == 'wild'])
                if opp.alive():
                    opp_next_mon(me, opp, mode, socket)
                else:
                    if mode == 'pong':
                        if overtime(me.alive(), me, opp, socket):
                            new_game_start(me, opp, mode)
                            continue
                    music.stop()
                    #TODO fade in
                    music_vict.play()
                    win(me, opp, mode)
                    if mode == 'gym' and challenger:
                        get_badge(me, opp)
                    elif mode == 'battle':
                        recv_prize(me, prize)
                    music_vict.stop()
            elif tmp == 1:
                run_me_faint(me)
                if me.alive():
                    me_next_mon(me, opp, mode, socket)
                else:
                    if mode == 'pong':
                        if overtime(me.alive(), me, opp, socket):
                            new_game_start(me, opp, mode)
                            continue
                    music.stop()
                    if mode == 'gym' and challenger:
                        if not(me.e1 == me.e2 == me.e3 == me.e4):
                            me.e1 = me.e2 = me.e3 = me.e4 = False
                            db.commit()
                    lost(me, opp, mode)
            elif tmp == 3:
                break
            elif tmp == 5:
                break
        music.stop()
        if mode == 'pong':
            if play_again(me.alive(), socket):
                if me.alive():
                    king = 'me'
                else:
                    king = 'opp'
                count = 1
            else:
                king = None
            socket.send('')
            socket.recv()
            intro(current)
        new_game = False
        if mode == 'random':
            mode = 'wild'
        if mode == 'gym':
            mode = 'wild'
            r.delete('leader')
        if mode == 'wild':
            for mon in me.pkmn:
                mon.clean()
                tmp = mon.check_evolve()
                if tmp:
                    evolve(mon, tmp)
