#TODO remove when done testing
from time import sleep
sleep(1)
from logic import *
from models import Trainer
from util import *
from redis import StrictRedis
from models import *
import zmq
import vlc

def main():
    #TODO set to True on opposite table
    client = False
    #TODO set to actual IP
    r = StrictRedis(host = '127.0.0.1')
    r.delete('lock')
    poss = [1,4,7,25,143,132,129,123,95,92,77,13,17,21,35]
    possible = []
    for p in poss:
        pkmn = loadimg('fronts/{0}.PNG'.format(p)).convert()
        pkmn.set_colorkey((255,255,255))
        possible.append(pkmn)
        if p == 4:
            current = pkmn
    socket = None
    mode = ''
    count = 0
    king = None
    new_game = True
    me = None
    while True:
        oldmode = mode
        mode = r.get('mode')
        if not mode:
            mode = 'pong'
            r.set('mode','pong')
        elif mode != oldmode:
            me = None
            opp = None
            count = 0
        if mode != 'wild' and new_game:
            r.incr('count')
            while r.get('count') < 2:
                sleep(1)
            context = zmq.Context()
            socket = context.socket(zmq.PAIR)
            if client:
                socket.connect("tcp://127.0.0.1:7777")
            else:
                socket.bind("tcp://*:7777")
            r.delete('count')
        if new_game or (not king and mode != 'wild'):
            intro(current)
            #TODO uncomment for PROD
            #sleep(5)
        while new_game or mode != 'wild':
            tmp = None
            try:
                tmp = json.loads(r.lpop('lineup'))
            except:
                pass
            if tmp:
                myname = tmp['name']
                mypkmnlist = tmp['pokemon']
                if mode != 'wild':
                        send_team(myname, mypkmnlist, socket, client)
                break
            current = scrolling(current, possible)
            #TODO uncomment for PROD
            #sleep(5)
        if mode != 'pong':
            me = Trainer.query.filter(Trainer.name == myname).one()
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
                me.pkmn.append(Owned.query.get(mon))
                me.current = me.pkmn[0]
                me.used = set()
                me.used.add(me.current)

        while mode != 'wild':
            try:
                oppname, opppkmnlist = get_teams(socket, client)
                opp = Trainer.query.filter(Trainer.name == oppname).one()
                opp.pkmn = []
                for mon in opppkmnlist:
                    opp.pkmn.append(Owned.get(mon))
                opp.current = opp.pkmn[0]
                break
            except:
                current = scrolling(current, possible)
                #TODO uncomment for PROD
                #sleep(5)
        if mode == 'wild':
            loc = choose_loc()
            if loc == 'PALLET TOWN':
                shop(me)
                new_game = False
                continue
            else:
                opp = Trainer('')
                opp.pkmn = [get_wild_mon(loc)]
                opp.current = opp.pkmn[0]
        opp.initialize()
        if mode == 'wild':
            music = Sound("sounds/wild_battle.ogg")
            music_vict = Sound("sounds/wild_victory.ogg")
        else:
            music = Sound("sounds/trainer_battle.ogg")
            music_vict = Sound("sounds/trainer_victory.ogg")
        music.play()
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
                send_move(move,socket)
                tmp = battle_logic(me, opp, move, True)
                r.delete('lock')
            if tmp == 0:
                run_opp_faint(opp)
                if mode == 'random' or mode == 'wild':
                    gain_exp(me,opp,[1.5,1][mode == 'wild'])
                if opp.alive():
                    opp_next_mon(me, opp, mode, socket)
                else:
                    music.stop()
                    music_vict.play()
                    win(me, opp, mode)
                    music_vict.stop()
            elif tmp == 1:
                run_me_faint(me)
                if me.alive():
                    me_next_mon(me, opp, mode, socket)
                else:
                    music.stop()
                    lost(me,mode)
            elif tmp == 3:
                pass
                break
            elif tmp == 5:
                break
        if mode == 'pong':
            if play_again(me.alive()):
                if me.alive():
                    king = 'me'
                else:
                    king = 'opp'
                count = 1
            else:
                king = None
        new_game = False
        #TODO should only evolve when leveled
        for mon in me.pkmn:
            mon.clean()
            tmp = mon.check_evolve()
            if tmp:
                evolve(me, mon, tmp)


