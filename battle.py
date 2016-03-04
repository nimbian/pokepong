from logic import *
from classes import trainer
from sqlite3 import connect
import argparse

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
    parser.add_argument("moveset1")
    parser.add_argument("moveset2")
    parser.add_argument("moveset3")
    parser.add_argument("moveset4")
    parser.add_argument("moveset5")
    parser.add_argument("moveset6")
    args = parser.parse_args()
    moveset = [args.moveset1,args.moveset2,args.moveset3,args.moveset4,args.moveset5,args.moveset6]
    mypkmn = [1,150,149,6,25,100]
    opppkmn = [7,150,149,6,25,100]
    myname = 'Player1'
    oppname = 'Player2'
    mypkmn = build_team(mypkmn, me = True, moveset = moveset)
    opppkmn = build_team(opppkmn)
    me = trainer(myname, mypkmn)
    opp = trainer(oppname, opppkmn)
    mode = 'random'

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
        tmp = run_game(me, opp, mode)
        if tmp == 0:
            run_opp_faint(opp)
            if opp.alive():
                opp_next_mon(me, opp, mode)
            else:
                win(me, opp, mode)
        elif tmp == 1:
            run_me_faint(me)
            if me.alive():
                me_next_mon(me, opp, mode)
            else:
                lost(me,mode)
        elif tmp == 3:
            pass
            #TODO escape





