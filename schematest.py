from model.match import *
from model.basics import db

match_schema = MatchSchema()
with open('test.json', 'r') as file:
    data = file.read()
    match = match_schema.loads(data)
    db.connect()
    dbMatch = match.ToDBObject()
    knownMatch = DbMatch.get_or_none(DbMatch.rngSeed == dbMatch.rngSeed)
    if knownMatch is None:
        print(dbMatch.save(force_insert=True))
        print("saved")
    else:
        print(knownMatch == dbMatch)
    db.close()