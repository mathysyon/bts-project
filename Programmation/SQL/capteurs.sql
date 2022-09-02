CREATE DATABASE IF NOT EXISTS RELEVES;
/*Si on veut reinitialiser l'auto incrementation (l'id), on fait : */
ALTER TABLE Alarme AUTO_INCREMENT = 1;
ALTER TABLE Releve AUTO_INCREMENT = 1;
ALTER TABLE Capteur AUTO_INCREMENT = 1;

DROP TABLE IF EXISTS Alarme;
CREATE TABLE Alarme (a_id_Alarme INT AUTO_INCREMENT NOT NULL,
                     a_dateheure_Alarme DATETIME,
                     c_id_Capteur INT, 
                     PRIMARY KEY (a_id_Alarme));

DROP TABLE IF EXISTS Capteur;
CREATE TABLE Capteur (c_id_Capteur INT AUTO_INCREMENT NOT NULL,
                      c_type_Capteur VARCHAR(25),
                      c_addr_Capteur VARCHAR(4),
                      c_unite_Capteur VARCHAR(25), 
                      PRIMARY KEY (c_id_Capteur));

DROP TABLE IF EXISTS Releve; 
CREATE TABLE Releve (r_id_Releve INT AUTO_INCREMENT NOT NULL,
                     r_dateheure_Releve DATETIME, 
                     r_valeur_Releve INT, 
                     c_id_Capteur INT, 
                     PRIMARY KEY (r_id_Releve));

ALTER TABLE Alarme ADD CONSTRAINT FK_Alarme_c_id_Capteur FOREIGN KEY (c_id_Capteur) REFERENCES Capteur (c_id_Capteur);
ALTER TABLE Releve ADD CONSTRAINT FK_Releve_c_id_Capteur FOREIGN KEY (c_id_Capteur) REFERENCES Capteur (c_id_Capteur);

/*-------------Ajout des capteurs-------------*/

INSERT INTO Capteur (c_type_Capteur, c_addr_Capteur, c_unite_Capteur) VALUES ('luminosity', '1b2f', 'lm');
INSERT INTO Capteur (c_type_Capteur, c_addr_Capteur) VALUES ('presence', '1b2f');
INSERT INTO Capteur (c_type_Capteur, c_addr_Capteur, c_unite_Capteur) VALUES ('humidity', 'd0d0', '%');
INSERT INTO Capteur (c_type_Capteur, c_addr_Capteur, c_unite_Capteur) VALUES ('temperature', 'd0d0', '°C');