import sqlite3
data_file='recettes.sqlite'

ma_connexion=sqlite3.connect(data_file)
mon_curseur=ma_connexion.cursor()

global id_utilisateur

from functions import *
from gui import *



page_connexion()
app.show()
