from flask import Flask, redirect, request #On importe le serveur flask ainsique des méthodes qui nous seront utilses comme redirect et request
import json
import sqlite3
import time
import math
import struct 
import csv
import Numpy as np


#Serveur


app = Flask(__name__) #crée un objet du serveur flask

def ReadFile(path):
    with open(path, 'rb') as f:
        return f.read()

@app.route('/')#si la route pas définie on a / alors on redirige vers index.html
def redirection():
    # Rediriger "/" vers "/index.html"
    return redirect('index.html', code = 302)

@app.route('/index.html')
def index():
    return ReadFile('index.html')

@app.route('/app.js')
def javascript():
    return ReadFile('app.js') 

@app.route('/GetMetrique', methods = [ 'POST' ])
def getmetriqueweb():
    donnees = request.get_data()
    infos = json.loads(donnees)
    result = GetMetrique(infos['dvnu'], infos['denu'], infos['surep'], infos['long'], infos['pas'], infos['quality'])
    #dvnu pour diametre vis non usiné et denu pour diametre ecrou non usiné
    return json.dumps(result)

@app.route('/GetwithGaz', methods = [ 'POST' ])
def getwithgazweb():
    donnees = request.get_data()
    infos = json.loads(donnees)
    result = GetWithGaz(infos['dvnu'], infos['denu'], infos['surep'], infos['long'])
    return json.dumps(result)

@app.route('/GetTrapeze', methods = [ 'POST' ])
def gettrapezeweb():
    donnees = request.get_data()
    infos = json.loads(donnees)
    result = GetTrapeze(infos['dvnu'], infos['denu'], infos['surep'], infos['long'])
    return json.dumps(result)

@app.route('/GetRond', methods = [ 'POST' ])
def getrondweb():
    donnees = request.get_data()
    infos = json.loads(donnees)
    result = GetRond(infos['dvnu'], infos['denu'], infos['surep'], infos['long'], infos['pas'])
    return json.dumps(result)


#CSV file

f=".../csvDB.csv"


def GetMetrique(dsup, dinf, surep, long,pas,quality):
    pasmax = long / 5 #car 5 fillets en prise minimum
    dmax = dsup - surep
    dmin = dinf + surep
    diam=[]
    pasGros=[]
    pasFin1=[]
    pasFin2=[]
    pasFin3=[]
    pasFin4=[]
    compteur=0 
    
    with open(f, 'r') as csvfile:
        reader = csv.writer(csvfile,delimiter=';')
        next(reader) #skip header line
        for row in reader:

            if quality == 0: #if we want only the col 1 values
                if pas ==0: #if we want only "pas gros"
                    if row[1]=='M' and row[3]<=dmax and row[3]>=dmin and row[4]<=pasmax and row[2]==1 and compteur<5:
                        diam.append(row[2])
                        pasGros.append(row[3])
                else: #if we want "pas gros" and "pas fin"
                    if row[1]=='M' and row[3]<=dmax and row[3]>=dmin and row[4]<=pasmax and row[2]==1 and compteur<5:
                        diam.append(row[2])
                        pasGros.append(row[3])
                        pasFin1.append(row[4])
                        pasFin2.append(row[5])
                        pasFin3.append(row[6])
                        pasFin4.append(row[7])

            else:
                if pas ==0: #if we want only "pas gros"
                    if row[1]=='M' and row[3]<=dmax and row[3]>=dmin and row[4]<=pasmax  and compteur<5:
                        diam.append(row[2])
                        pasGros.append(row[3])
                else: #if we want "pas gros" and "pas fin"
                    if row[1]=='M' and row[3]<=dmax and row[3]>=dmin and row[4]<=pasmax  and compteur<5:
                        diam.append(row[2])
                        pasGros.append(row[3])
                        pasFin1.append(row[4])
                        pasFin2.append(row[5])
                        pasFin3.append(row[6])
                        pasFin4.append(row[7])
        compteur+=1

                
#         reponse[i][0] = req[i][0]#diametre nominal
#         reponse[i][1] = req[i][1]#pas
#         reponse[i][2] = req[i][0] - 1.082 * req[i][1]#diametre de forage / percage
#         reponse[i][3] = req[i][0] - 1.226 * req[i][1]#diametre fond de filet vis
#         reponse[i][4] = 0.5 * req[i][1]#rayon
#         reponse[i][5] = req[i][0] - 1.5 * req[i][1]#diametre sortie outil vis
#         reponse[i][6] = 2 * req[i][1]#hauteur min sortie outil vis
#         reponse[i][7] = 3 * req[i][1]#hauteur max sortie outil vis
#         reponse[i][8] = 1.5 * req[i][1]#chanfrein
#         reponse[i][9] = 2 * req[i][1]#hauteur min sortie outil ecrou
#         reponse[i][10] = 4 * req[i][1]#hauteur max sortie outil ecrou
#         reponse[i][11] = req[i][0] + 0.5 * req[i][1]#diametre sortie outil ecrou
    

def GetWithGaz (dsup, dinf, surep, long):
    pasmax = long / 5 #car 5 fillets en prise minimum
    dmax = dsup - surep
    dmin = dinf + surep
    diam=[]
    pasGros=[]
    pas = 'pasgros' #typedepas == true
    with open(f, 'r') as csvfile:
        reader = csv.writer(csvfile,delimiter=';')
        for row in reader:
            if row[1]=='WG' and row[3]<=dmax and row[3]>=dmin and row[4]<=pasmax:
                diam.append(row[3])
                pasGros.append(row[4])


def GetTrapeze (dsup, dinf, surep, long):
    pasmax = long / 5 #car 5 fillets en prise minimum
    dmax = dsup - surep
    dmin = dinf + surep
    diam=[]
    pasGros=[]
    pas = 'pasgros' #typedepas == true
    with open(f, 'r') as csvfile:
        reader = csv.writer(csvfile,delimiter=';')
        for row in reader:
            if row[1]=='T' and row[3]<=dmax and row[3]>=dmin and row[4]<=pasmax:
                diam.append(row[3])
                pasGros.append(row[4])


def GetRond(dsup, dinf, surep, long):
    pasmax = long / 5 #car 5 fillets en prise minimum
    dmax = dsup - surep
    dmin = dinf + surep
    diam=[]
    pasGros=[]
    pas = 'pasgros' #typedepas == true
    with open(f, 'r') as csvfile:
        reader = csv.writer(csvfile,delimiter=';')
        for row in reader:
            if row[1]=='M' and row[3]<=dmax and row[3]>=dmin and row[4]<=pasmax and row[2]<3:
                diam.append(row[3])
                pasGros.append(row[4])


                
# #DataBase


# def OpenDatabase():
#     # Ouverture d'une base de données SQLite, en réessayant jusqu'à ce
#     # que le fichier contenant la base de données soit disponible
#     while True:
#         try:
#             return sqlite3.connect('index.sq3')
#         except Exception as e:
#             time.sleep(0.1)
#             continue   # Nouvel essai après 100 ms

# def ExecuteDatabase(db, sql, args = []):
#     cursor = db.cursor()
#     try:
#         cursor.execute(sql, args)
#         results = cursor.fetchall()
#         cursor.close()
#         return results
#     except Exception as e:
#         # On s'assure de fermer le curseur même en cas d'échec
#         cursor.close()
#         return None

# def CloseDatabase(db):
#     # Ne jamais oublier de refermer la base de données SQLite, sinon
#     # plus personne ne peut s'y connecter !
#     db.commit()
#     db.close()

# def Initialize():
#     # Initialisation de la base de données
#     db = OpenDatabase()
#     ExecuteDatabase(db, 'CREATE TABLE IF NOT EXISTS tabmetriquerond' +
#                     '(dnominal DOUBLE PRIMARY KEY, pasgros DOUBLE, section DOUBLE, pasfin DOUBLE)')
#     ExecuteDatabase(db, 'CREATE TABLE IF NOT EXISTS tabwithgaz' +
#                     '(denomination TEXT, dnominal DOUBLE PRIMARY KEY, pas DOUBLE)')
#     ExecuteDatabase(db, 'CREATE TABLE IF NOT EXISTS tabtrap' +
#                     '(dnominal DOUBLE PRIMARY KEY, pas DOUBLE, videff DOUBLE)')
#     CloseDatabase(db)

# def GetMetrique(dsup, dinf, surep, long, typedepas):

#     pasmax = long / 5 #car 5 fillets en prise minimum
#     dmax = dsup - surep
#     dmin = dinf + surep
#     pas = 'pasgros' #typedepas == true

#     if (typedepas == False):
#         pas = 'pasfin'

#     db = OpenDatabase()
#     req = ExecuteDatabase(db, 'SELECT dnominal, ? FROM tabmetriquerond WHERE dnominal >= ? AND dnominal <= ? AND ? < ?'
#                             , [ pas, dmin, dmax, pas, pasmax ])
#     db = CloseDatabase(db)

#     for i in req:
#         reponse[i][0] = req[i][0]#diametre nominal
#         reponse[i][1] = req[i][1]#pas
#         reponse[i][2] = req[i][0] - 1.082 * req[i][1]#diametre de forage / percage
#         reponse[i][3] = req[i][0] - 1.226 * req[i][1]#diametre fond de filet vis
#         reponse[i][4] = 0.5 * req[i][1]#rayon
#         reponse[i][5] = req[i][0] - 1.5 * req[i][1]#diametre sortie outil vis
#         reponse[i][6] = 2 * req[i][1]#hauteur min sortie outil vis
#         reponse[i][7] = 3 * req[i][1]#hauteur max sortie outil vis
#         reponse[i][8] = 1.5 * req[i][1]#chanfrein
#         reponse[i][9] = 2 * req[i][1]#hauteur min sortie outil ecrou
#         reponse[i][10] = 4 * req[i][1]#hauteur max sortie outil ecrou
#         reponse[i][11] = req[i][0] + 0.5 * req[i][1]#diametre sortie outil ecrou

#     return reponse

# def getwithgaz(dsup, dinf, surep, long):

#     pasmax = long / 5 #car 5 fillets en prise minimum
#     dmax = dsup - surep
#     dmin = dinf + surep

#     db = OpenDatabase()
#     req = ExecuteDatabase(db, 'SELECT denomination, dnominal, pas FROM tabwithgaz WHERE dnominal >= ? AND dnominal <= ? AND pas < ?'
#                             , [ dmin, dmax, pasmax ])
#     db = CloseDatabase(db)

#     for i in req:
#         reponse[i][0] = req[i][0]#diametre nominal vis et diametre fond filet ecrou
#         reponse[i][1] = req[i][1]#pas
#         reponse[i][2] = req[i][0] - 2 * req[i][1] / (3 * math.tan(math.radians(27.5)))#diametre fond filet vis et diametre percage / forage
#         reponse[i][3] = 0.5 * req[i][1]#rayon
#         reponse[i][4] = req[i][0] - 1.5 * req[i][1]#diametre sortie outil vis
#         reponse[i][5] = 2 * req[i][1]#hauteur min sortie outil vis
#         reponse[i][6] = 3 * req[i][1]#hauteur max sortie outil vis
#         reponse[i][7] = 1.5 * req[i][1]#chanfrein
#         reponse[i][8] = 2 * req[i][1]#hauteur min sortie outil ecrou
#         reponse[i][9] = 4 * req[i][1]#hauteur max sortie outil ecrou
#         reponse[i][10] = req[i][0] + 0.5 * req[i][1]#diametre sortie outil ecrou

#     return reponse

# def gettrapeze(dsup, dinf, surep, long):

#     pasmax = long / 5 #car 5 fillets en prise minimum
#     dmax = dsup - surep
#     dmin = dinf + surep

#     db = OpenDatabase()
#     req = ExecuteDatabase(db, 'SELECT dnominal, pas, videff FROM tabtrap WHERE dnominal >= ? AND dnominal <= ? AND pas < ?'
#                             , [ dmin, dmax, pasmax ])
#     db = CloseDatabase(db)

#     for i in req:
#         reponse[i][0] = req[i][0]#diametre nominal
#         reponse[i][1] = req[i][1]#pas
#         reponse[i][2] = req[i][0] - req[i][1] - 2 * req[i][2]#diametre fond filet vis
#         reponse[i][3] = req[i][0] + 2 * req[i][2]#diametre fond filet ecrou
#         reponse[i][4] = req[i][0] - req[i][1]#diametre forage / percage
#         reponse[i][5] = 0.5 * req[i][1]#rayon
#         reponse[i][6] = req[i][0] - 1.5 * req[i][1]#diametre sortie outil vis
#         reponse[i][7] = 2 * req[i][1]#hauteur min sortie outil vis
#         reponse[i][8] = 3 * req[i][1]#hauteur max sortie outil vis
#         reponse[i][9] = 1.5 * req[i][1]#chanfrein
#         reponse[i][10] = 2 * req[i][1]#hauteur min sortie outil ecrou
#         reponse[i][11] = 4 * req[i][1]#hauteur max sortie outil ecrou
#         reponse[i][12] = req[i][0] + 0.5 * req[i][1]#diametre sortie outil ecrou

#     return reponse

# def getrond(dsup, dinf, surep, long, typedepas):

#     pasmax = long / 5 #car 5 fillets en prise minimum
#     dmax = dsup - surep
#     dmin = dinf + surep
#     pas = 'pasgros' #typedepas == true

#     if (typedepas == False):
#         pas = 'pasfin'

#     db = OpenDatabase()
#     req = ExecuteDatabase(db, 'SELECT dnominal, ? FROM tabmetriquerond WHERE dnominal >= ? AND dnominal <= ? AND ? < ?'
#                             , [ pas, dmin, dmax, pas, pasmax ])
#     db = CloseDatabase(db)

#     for i in req:
#         reponse[i][0] = req[i][0]#diametre nominal
#         reponse[i][1] = req[i][1]#pas
#         reponse[i][2] = req[i][0] - req[i][1]#diametre fond filet vis
#         reponse[i][3] = req[i][0] + 0.1 * req[i][1]#diametre fond filet ecrou
#         reponse[i][4] = req[i][0] - 1.1 * req[i][1]#diametre forage / percage
#         reponse[i][5] = 0.5 * req[i][1]#rayon
#         reponse[i][6] = req[i][0] - 1.5 * req[i][1]#diametre sortie outil vis
#         reponse[i][7] = 2 * req[i][1]#hauteur min sortie outil vis
#         reponse[i][8] = 3 * req[i][1]#hauteur max sortie outil vis
#         reponse[i][9] = 1.5 * req[i][1]#chanfrein
#         reponse[i][10] = 2 * req[i][1]#hauteur min sortie outil ecrou
#         reponse[i][11] = 4 * req[i][1]#hauteur max sortie outil ecrou
#         reponse[i][12] = req[i][0] + 0.5 * req[i][1]#diametre sortie outil ecrou

#     return reponse




if __name__ == '__main__':
    Initialize()
    app.run(debug = True)