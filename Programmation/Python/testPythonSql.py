import mariadb
from datetime import datetime

db = mariadb.connect(user="root", password="conceptball", host='localhost', database='releve_conceptball') #connexion à bdd

# Get Cursor
cursor = db.cursor()

#cursor.execute("SHOW DATABASES")
#for x in cur:
#    print(x) #Print la base de données

#cursor.execute("SHOW TABLES")
#for x in cur:
#    print(x) #Print les tables de "releve_conceptball"

#now = datetime.now()
#formatted_date = now.strftime('%Y/%m/%d %H:%M:%S')
#insert = "INSERT INTO Releve (r_dateheure_Releve, r_valeur_Releve, c_id_Capteur) VALUES ('{}', {}, '{}')".format(formatted_date, "15", "f2a5") #requête sql

#cursor.execute(insert) #éxecute et transmet la requête SQL
#db.commit() #valide la transaction

#select = "SELECT c_id_Capteur FROM Capteur WHERE c_type_Capteur='temperature'"
#cursor.execute(select)
#result = cursor.fetchone() 
#c_id_Capteur = result[0]
#print(c_id_Capteur)

now = datetime.now()
cursor = db.cursor()
select = "SELECT c_id_Capteur FROM Capteur WHERE c_type_Capteur='luminosity' LIMIT 1"
cursor.execute(select)
result = cursor.fetchone() 
c_id_Capteur = result[0]
print(c_id_Capteur)

#Récupère la dernière date à laquelle la dernière valeur à été mise
selectDatePrecedente = "SELECT MAX(r_dateheure_Releve) FROM Releve WHERE c_id_Capteur={} LIMIT 1".format(c_id_Capteur)
cursor.execute(selectDatePrecedente)
resultDate = cursor.fetchone() 
precedenteDate = resultDate[0]  

if precedenteDate is None: #Si il n'y a aucune valeur dans la bdd pour éviter une erreur 
    precedenteDate=now
    print(precedenteDate)

    insert = "INSERT INTO Releve (r_dateheure_Releve, r_valeur_Releve, c_id_Capteur) VALUES ('{}', {}, '{}')".format(now.strftime('%Y/%m/%d %H:%M:%S'), 668, c_id_Capteur) #requête sql
    cursor.execute(insert) #éxecute et transmet la requête SQL
    db.commit() #valide la transaction
    print(cursor.rowcount, "ligne(s) insérée(s) dans la table Capteur")

difDateTime = now - precedenteDate
difDateTime = difDateTime.total_seconds()/60
print(difDateTime)

#Insert les données seulement si la précédente date de il y a 10 min
if((difDateTime > 6) and (precedenteDate != now)):  
        insert = "INSERT INTO Releve (r_dateheure_Releve, r_valeur_Releve, c_id_Capteur) VALUES ('{}', {}, '{}')".format(now.strftime('%Y/%m/%d %H:%M:%S'), 668, c_id_Capteur) #requête sql
        cursor.execute(insert) #éxecute et transmet la requête SQL
        db.commit() #valide la transaction

print(cursor.rowcount, "ligne(s) insérée(s) dans la table Capteur")

