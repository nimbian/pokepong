from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from .config import _cfg
engine = create_engine(_cfg('connection-string'))
db = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db.query_property()

def init_db(tmp = None):
    import pokepong.models
    if tmp:
        Base.metadata.create_all(bind=tmp)
    else:
        Base.metadata.create_all(bind=engine)
    with engine.begin() as conn:
        result = conn.execute("SELECT id FROM pokemon")
        if result.first() is None:
            with open('pokepong/pokemon.sql', 'r') as file_:
                with conn.begin() as trans:
                    if engine.name == 'sqlite':
                        conn.execute('PRAGMA foreign_keys=OFF;')
                    elif engine.name == 'postgresql':
                        conn.execute('ALTER TABLE pokemon DISABLE TRIGGER ALL;')
                    for line in file_:
                        conn.execute(line)
                    if engine.name == 'postgresql':
                        conn.execute('ALTER TABLE pokemon ENABLE TRIGGER ALL;')
                        conn.execute('alter sequence owned_id_seq restart with 152;')
    from pokepong.models import Owned
    db.add(Owned(74, lvl=12))
    db.add(Owned(95, lvl=14))

    db.add(Owned(120, lvl=18))
    db.add(Owned(121, lvl=21))

    db.add(Owned(100, lvl=21))
    db.add(Owned(25, lvl=18))
    db.add(Owned(26, lvl=24))

    db.add(Owned(71, lvl=29))
    db.add(Owned(114, lvl=24))
    db.add(Owned(45, lvl=29))

    db.add(Owned(64, lvl=38))
    db.add(Owned(122, lvl=37))
    db.add(Owned(49, lvl=38))
    db.add(Owned(65, lvl=43))

    db.add(Owned(109, lvl=37))
    db.add(Owned(89, lvl=39))
    db.add(Owned(109, lvl=37))
    db.add(Owned(110, lvl=43))

    db.add(Owned(58, lvl=42))
    db.add(Owned(77, lvl=40))
    db.add(Owned(78, lvl=42))
    db.add(Owned(59, lvl=47))

    db.add(Owned(111, lvl=45))
    db.add(Owned(51, lvl=42))
    db.add(Owned(31, lvl=44))
    db.add(Owned(34, lvl=45))
    db.add(Owned(112, lvl=50))
    #ELITE 4
    db.add(Owned(87, lvl=52))
    db.add(Owned(91, lvl=51))
    db.add(Owned(80, lvl=52))
    db.add(Owned(124, lvl=54))
    db.add(Owned(131, lvl=54))

    db.add(Owned(95, lvl=51))
    db.add(Owned(107, lvl=53))
    db.add(Owned(106, lvl=53))
    db.add(Owned(95, lvl=54))
    db.add(Owned(68, lvl=56))

    db.add(Owned(94, lvl=54))
    db.add(Owned(42, lvl=54))
    db.add(Owned(93, lvl=53))
    db.add(Owned(24, lvl=56))
    db.add(Owned(94, lvl=58))

    db.add(Owned(130, lvl=58))
    db.add(Owned(148, lvl=56))
    db.add(Owned(148, lvl=56))
    db.add(Owned(142, lvl=60))
    db.add(Owned(149, lvl=62))
    db.commit()
