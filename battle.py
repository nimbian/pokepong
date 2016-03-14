from time import sleep
sleep(1)
from logic import *
from classes import trainer
from sqlite3 import connect
from util import send_teams, get_teams, set_seed, get_random
from util import MyMoveOccuring, OppMoveOccuring, send_move, recv_move
from redis import StrictRedis
import zmq


if __name__ == '__main__':
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
    if r.lock('client').acquire(blocking=False):
        client = False
    else:
        client = True
    r.incr('count')
    while r.get('count') < 2:
        sleep(1)
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    if client:
        socket.connect("tcp://127.0.0.1:7777")
    else:
        socket.bind("tcp://*:7777")

    #intro(current)
    #sleep(5)
    count = 0
    #while count < 2:
    #    conn = connect('shawn')
    #    c = conn.cursor()
    #    tmp = c.execute("SELECT * from teams order by ROWID").fetchone()
    #    if tmp:
    #        if count == 0:
    #            myname = tmp[0]
    #            mypkmn = tmp[1:]
    #        if count == 1:
    #            oppname = tmp[0]
    #            opppkmn = tmp[1:]
    #        c.execute("DELETE from teams where name = '{0}'".format(tmp[0]))
    #        conn.commit()
    #        count += 1
    #    current = scrolling(current, possible)
    #    sleep(5)


    sleep(2)
    r.delete('client')
    r.delete('count')
    if not client:
        mypkmn = [1,150,149,6,25,100]
        opppkmn = [7,150,149,6,25,100]
        myname = 'Player1'
        oppname = 'Player2'
        mypkmn, opppkmn, myname, oppname, seed = send_teams(mypkmn, opppkmn, myname, oppname, socket)
    else:
        mypkmn, opppkmn, myname, oppname, seed = get_teams(socket)
    r.delete(myname)
    r.delete(oppname)
    mypkmn = build_team(mypkmn, me = True)
    opppkmn = build_team(opppkmn)
    me = trainer(myname, mypkmn)
    opp = trainer(oppname, opppkmn)
    #if client:
    #    socket.send('')
    #else:
    #    socket.recv()
    set_seed(seed)
    mode = 'wild'
    #opppkmn = [1]
    #mypkmn = [9,150,149,6,25,100]
    #myname = 'ASD'
    #oppname = 'wild'
    #mypkmn = build_team(mypkmn, me = True)
    #opppkmn = build_team(opppkmn)
    #me = trainer(myname, mypkmn)
    #opp = trainer(oppname, opppkmn)
    #mode = 'wild'
    if mode != 'wild':
        new_game_start(me, opp, mode)
    else:
        loc = choose_loc()
        opp = trainer('', [get_wild_mon(loc)])


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
            print tmp
        except MyMoveOccuring as move:
            clear()
            display.flip()
            draw_all_opp(opp.current)
            draw_all_me(me.current)
            send_move(move,socket)
            tmp = battle_logic(me, opp, move, True)
            r.delete('lock')
            print tmp
        if tmp == 0:
            run_opp_faint(opp)
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
            #TODO escape





