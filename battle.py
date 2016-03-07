from logic import *
from classes import trainer
from sqlite3 import connect
from util import send_teams, get_teams, set_seed, get_random
import argparse
import zmq

if __name__ == '__main__':
    poss = [1,4,7,25,143,132,129,123,95,92,77,13,17,21,35]
    possible = []
    for p in poss:
        pkmn = loadimg('fronts/{0}.PNG'.format(p)).convert()
        pkmn.set_colorkey((255,255,255))
        possible.append(pkmn)
        if p == 4:
            current = pkmn
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
    parser = argparse.ArgumentParser()
    parser.add_argument('--client', action='store_true')
    args = parser.parse_args()
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    client = args.client
    if not client:
        socket.connect("tcp://127.0.0.1:7777")
    else:
        socket.bind("tcp://*:7777")

    sleep(2)
    if not client:
        mypkmn = [1,150,149,6,25,100]
        opppkmn = [7,150,149,6,25,100]
        myname = 'Player1'
        oppname = 'Player2'
        mypkmn, opppkmn, myname, oppname, seed = send_teams(mypkmn, opppkmn, myname, oppname, socket)
    else:
        mypkmn, opppkmn, myname, oppname, seed = get_teams(socket)
    mypkmn = build_team(mypkmn, me = True)
    opppkmn = build_team(opppkmn)
    me = trainer(myname, mypkmn)
    opp = trainer(oppname, opppkmn)
    if client:
        socket.send('')
    else:
        socket.recv()
    set_seed(seed)
    mode = 'battle'
    #opppkmn = [1]
    #mypkmn = [9,150,149,6,25,100]
    #myname = 'ASD'
    #oppname = 'wild'
    #mypkmn = build_team(mypkmn, me = True)
    #opppkmn = build_team(opppkmn)
    #me = trainer(myname, mypkmn)
    #opp = trainer(oppname, opppkmn)
    #mode = 'wild'
    new_game_start(me, opp, mode)
    while me.alive() and opp.alive():
        clearbtm()
        draw_choice(0)
        tmp = run_game(me, opp, mode, socket)
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





