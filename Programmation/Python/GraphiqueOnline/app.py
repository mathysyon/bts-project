from typing import final
from flask import Flask, render_template
import mariadb
from datetime import datetime
import json

db = mariadb.connect(user="root", password="conceptball", host='localhost', database='releve_conceptball') #connexion à bdd

app = Flask(__name__)
#def recupTemp():

@app.route('/')
def index():
    cursor = db.cursor()
    try:
        cursor.execute("SELECT r_dateheure_Releve FROM `Releve` WHERE c_id_Capteur = 4") #A refaire pour récup l'id du capteur voir //SELECT r_dateheure_Releve FROM Releve ORDER BY ABS( DATEDIFF( r_dateheure_Releve, NOW())) LIMIT 3
        result = cursor.fetchall() 
        dateHeureTemp = list()
        i = 0
        for row in result:
            DateTimeTemp = row[i].strftime("%d/%m/%Y %H:%M:%S")
            dateHeureTemp.append(DateTimeTemp)

        cursor.execute("SELECT r_valeur_Releve FROM `Releve` WHERE c_id_Capteur = 4") #A refaire pour récup l'id du capteur
        result = cursor.fetchall() 
        valeurTemp = list()
        i = 0
        for row in result:
            valeurTemp.append(row[i])
        cursor.close()

    except:
        print("Error: unable to fetch items")

    return render_template('index.tpl', labels=dateHeureTemp, data=valeurTemp)

app.run(debug=True, host='0.0.0.0', port=5001)