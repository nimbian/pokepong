#TODO remove when done testing
from time import sleep
sleep(1)
from logic import *
from classes import trainer
from util import *
from redis import StrictRedis
import zmq

if __name__ == '__main__':
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
            needed = 2
        else:
            needed = 1
        if new_game or (not king and mode != 'wild'):
            intro(current)
            #TODO uncomment for PROD
            #sleep(5)
        while new_game or mode != 'wild':
            if not client or mode == 'wild':
                tmp = None
                try:
                    tmp = json.loads(r.lpop('lineup'))
                except:
                    pass
                if tmp:
                    if count == 0:
                        myname = tmp['name']
                        mypkmnlist = tmp['pokemon']
                    if count == 1:
                        if king == 'opp':
                            myname = tmp['name']
                            mypkmnlist = tmp['pokemon']
                        else:
                            oppname = tmp['name']
                            opppkmnlist = tmp['pokemon']
                    count += 1
                    if count == needed:
                        break
                current = scrolling(current, possible)
                #TODO uncomment for PROD
                #sleep(5)
            else:
                try:
                    mypkmn, opppkmn, myname, oppname, seed = get_teams(socket)
                    break
                except:
                    current = scrolling(current, possible)
                    sleep(5)
        if mode == 'wild' and not me:
            if mode == 'wild':
                mypkmn, opppkmn, myname, oppname, seed = send_teams(mypkmnlist, myname)
            else:
                if client:
                    mypkmn, opppkmn, myname, oppname, seed = send_teams(mypkmnlist, myname,
                                                                        opppkmn = opppkmnlist,
                                                                        oppname = oppname,
                                                                        socket = socket)
            set_seed(seed)
            mypkmn = build_team(mypkmn, me = True)
            me = trainer(myname, mypkmn)
        else:
            for mon in me.pkmn:
                mon.clean()
        if mode == 'wild':
            for mon in me.pkmn:
                tmp = mon.check_evolve()
            if tmp:
                evolve(me, mon, tmp)
            loc = choose_loc()
            if loc == 'PALLET TOWN':
                shop(me)
                continue
            else:
                opp = trainer('', [get_wild_mon(loc)])
        else:
            opppkmn = build_team(opppkmn)
            opp = trainer(oppname, opppkmn)
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
                    win(me, opp, mode)
            elif tmp == 1:
                run_me_faint(me)
                if me.alive():
                    me_next_mon(me, opp, mode, socket)
                else:
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
            tmp = mon.check_evolve()
            if tmp:
                evolve(me, mon, tmp)

