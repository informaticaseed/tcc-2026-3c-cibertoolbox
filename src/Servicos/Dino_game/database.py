from peewee import *
import os
Diretorio_Principal = os.path.dirname(__file__)
db = SqliteDatabase(os.path.join(Diretorio_Principal, 'Record.db'))
class Pontuação(Model):
    record = CharField(unique=True)
    class Meta:
        database = db