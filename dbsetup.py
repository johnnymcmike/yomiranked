from model.basics import db
from model.match import ModeledMatch
from model.player import ModeledPlayer

db.create_tables([ModeledMatch, ModeledPlayer])
