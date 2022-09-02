import mariadb
import datetime
import time

db = mariadb.connect(user="root", password="conceptball", host='localhost', database='releve_conceptball') #connexion à bdd

date_now = datetime.datetime.now()

cursor = db.cursor()
deleteDonnees = "DELETE FROM Releve WHERE DATEDIFF('{}', r_dateheure_Releve) > 3".format(date_now.strftime('%Y-%m-%d %H:%M:%S')) #requête sql
print(deleteDonnees)
cursor.execute(deleteDonnees) #éxecute et transmet la requête SQL
db.commit() #valide la transaction
cursor.close()