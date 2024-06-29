#little thing i use in dev to reset db, please ignore
from model.basics import db
from model.match import DbMatch
from model.player import DbPlayer

db.create_tables([DbMatch, DbPlayer])
