from redis import StrictRedis
from sqlite3 import connect
import json

if __name__ == '__main__':
    r = StrictRedis(host = '127.0.0.1')
    insert = ("INSERT INTO ownedpkmn VALUES ('{0}','{1}','{2}','{3}','{4}',"
              "'{5}','{6}',0,0,0,0,0,'{7}','{8}','{9}','{10}','{11}'")
    update = ("UPDATE ownedpkmn set lvl = {0}, hpev = {1}, attackev = {2},"
              "defenseev = {3}, speedev = {4}, specialev = {5}, exp = {6} "
              "WHERE rowid = '{7}'")
    while True:
        tmp, msg = r.blpop('queue')
        msg = json.loads(msg)
        type_ = msg[0]
        msg = msg[1]
        conn = connect('shawn')
        c = conn.cursor()
        if type_ == 'gain':
            c.execute(update.format(*msg))
        elif type_ == 'new':
            c.execute(insert.format(*msg))
        else:
            print 'unk: ' + msg
        conn.commit()
        c.close()
        conn.close()

