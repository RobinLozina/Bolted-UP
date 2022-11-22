from flask import Flask, redirect, request #On importe le serveur flask ainsique des méthodes qui nous seront utilses comme redirect et request
import json
import sqlite3
import time
import math


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

@app.route('/getmetrique', methods = [ 'GET' ])
def getmetriqueweb():
    donnees = request.get_data()
    infos = json.loads(donnees)
    result = getmetrique(infos['dvnu'], infos['denu'], infos['surep'], infos['long'], infos['typepas'])
    #dvnu pour diametre vis non usiné et denu pour diametre ecrou non usiné
    return json.dumps(result)

@app.route('/getwithgaz', methods = [ 'GET' ])
def getwithgazweb():
    donnees = request.get_data()
    infos = json.loads(donnees)
    result = getwithgaz(infos['dvnu'], infos['denu'], infos['surep'], infos['long'])
    return json.dumps(result)

@app.route('/gettrapeze', methods = [ 'GET' ])
def gettrapezeweb():
    donnees = request.get_data()
    infos = json.loads(donnees)
    result = gettrapeze(infos['dvnu'], infos['denu'], infos['surep'], infos['long'])
    return json.dumps(result)

@app.route('/getrond', methods = [ 'GET' ])
def getrondweb():
    donnees = request.get_data()
    infos = json.loads(donnees)
    result = getrond(infos['dvnu'], infos['denu'], infos['surep'], infos['long'], infos['typepas'])
    return json.dumps(result)


#DataBase


def OpenDatabase():
    # Ouverture d'une base de données SQLite, en réessayant jusqu'à ce
    # que le fichier contenant la base de données soit disponible
    while True:
        try:
            return sqlite3.connect('index.sq3')
        except Exception as e:
            time.sleep(0.1)
            continue   # Nouvel essai après 100 ms

def ExecuteDatabase(db, sql, args = []):
    cursor = db.cursor()
    try:
        cursor.execute(sql, args)
        results = cursor.fetchall()
        cursor.close()
        return results
    except Exception as e:
        # On s'assure de fermer le curseur même en cas d'échec
        cursor.close()
        return None

def CloseDatabase(db):
    # Ne jamais oublier de refermer la base de données SQLite, sinon
    # plus personne ne peut s'y connecter !
    db.commit()
    db.close()

def Initialize():
    # Initialisation de la base de données
    db = OpenDatabase()
    ExecuteDatabase(db, 'CREATE TABLE IF NOT EXISTS tabmetriquerond' +
                    '(dnominal DOUBLE PRIMARY KEY, pasgros DOUBLE, section DOUBLE, pasfin DOUBLE)')
    ExecuteDatabase(db, 'CREATE TABLE IF NOT EXISTS tabwithgaz' +
                    '(denomination TEXT, dnominal DOUBLE PRIMARY KEY, pas DOUBLE)')
    ExecuteDatabase(db, 'CREATE TABLE IF NOT EXISTS tabtrap' +
                    '(dnominal DOUBLE PRIMARY KEY, pas DOUBLE, videff DOUBLE)')
    CloseDatabase(db)

def getmetrique(dsup, dinf, surep, long, typedepas):

    pasmax = long / 5 #car 5 fillets en prise minimum
    dmax = dsup - surep
    dmin = dinf + surep
    pas = 'pasgros' #typedepas == true

    if (typedepas == False):
        pas = 'pasfin'

    db = OpenDatabase()
    req = ExecuteDatabase(db, 'SELECT dnominal, ? FROM tabmetriquerond WHERE dnominal >= ? AND dnominal <= ? AND ? < ?'
                            , [ pas, dmin, dmax, pas, pasmax ])
    db = CloseDatabase(db)

    for i in req:
        reponse[i][0] = req[i][0]#diametre nominal
        reponse[i][1] = req[i][1]#pas
        reponse[i][2] = req[i][0] - 1.082 * req[i][1]#diametre de forage / percage
        reponse[i][3] = req[i][0] - 1.226 * req[i][1]#diametre fond de filet vis
        reponse[i][4] = 0.5 * req[i][1]#rayon
        reponse[i][5] = req[i][0] - 1.5 * req[i][1]#diametre sortie outil vis
        reponse[i][6] = 2 * req[i][1]#hauteur min sortie outil vis
        reponse[i][7] = 3 * req[i][1]#hauteur max sortie outil vis
        reponse[i][8] = 1.5 * req[i][1]#chanfrein
        reponse[i][9] = 2 * req[i][1]#hauteur min sortie outil ecrou
        reponse[i][10] = 4 * req[i][1]#hauteur max sortie outil ecrou
        reponse[i][11] = req[i][0] + 0.5 * req[i][1]#diametre sortie outil ecrou

    return reponse

def getwithgaz(dsup, dinf, surep, long):

    pasmax = long / 5 #car 5 fillets en prise minimum
    dmax = dsup - surep
    dmin = dinf + surep

    db = OpenDatabase()
    req = ExecuteDatabase(db, 'SELECT denomination, dnominal, pas FROM tabwithgaz WHERE dnominal >= ? AND dnominal <= ? AND pas < ?'
                            , [ dmin, dmax, pasmax ])
    db = CloseDatabase(db)

    for i in req:
        reponse[i][0] = req[i][0]#diametre nominal vis et diametre fond filet ecrou
        reponse[i][1] = req[i][1]#pas
        reponse[i][2] = req[i][0] - 2 * req[i][1] / (3 * math.tan(math.radians(27.5)))#diametre fond filet vis et diametre percage / forage
        reponse[i][3] = 0.5 * req[i][1]#rayon
        reponse[i][4] = req[i][0] - 1.5 * req[i][1]#diametre sortie outil vis
        reponse[i][5] = 2 * req[i][1]#hauteur min sortie outil vis
        reponse[i][6] = 3 * req[i][1]#hauteur max sortie outil vis
        reponse[i][7] = 1.5 * req[i][1]#chanfrein
        reponse[i][8] = 2 * req[i][1]#hauteur min sortie outil ecrou
        reponse[i][9] = 4 * req[i][1]#hauteur max sortie outil ecrou
        reponse[i][10] = req[i][0] + 0.5 * req[i][1]#diametre sortie outil ecrou

    return reponse

def gettrapeze(dsup, dinf, surep, long):

    pasmax = long / 5 #car 5 fillets en prise minimum
    dmax = dsup - surep
    dmin = dinf + surep

    db = OpenDatabase()
    req = ExecuteDatabase(db, 'SELECT dnominal, pas, videff FROM tabtrap WHERE dnominal >= ? AND dnominal <= ? AND pas < ?'
                            , [ dmin, dmax, pasmax ])
    db = CloseDatabase(db)

    for i in req:
        reponse[i][0] = req[i][0]#diametre nominal
        reponse[i][1] = req[i][1]#pas
        reponse[i][2] = req[i][0] - req[i][1] - 2 * req[i][2]#diametre fond filet vis
        reponse[i][3] = req[i][0] + 2 * req[i][2]#diametre fond filet ecrou
        reponse[i][4] = req[i][0] - req[i][1]#diametre forage / percage
        reponse[i][5] = 0.5 * req[i][1]#rayon
        reponse[i][6] = req[i][0] - 1.5 * req[i][1]#diametre sortie outil vis
        reponse[i][7] = 2 * req[i][1]#hauteur min sortie outil vis
        reponse[i][8] = 3 * req[i][1]#hauteur max sortie outil vis
        reponse[i][9] = 1.5 * req[i][1]#chanfrein
        reponse[i][10] = 2 * req[i][1]#hauteur min sortie outil ecrou
        reponse[i][11] = 4 * req[i][1]#hauteur max sortie outil ecrou
        reponse[i][12] = req[i][0] + 0.5 * req[i][1]#diametre sortie outil ecrou

    return reponse

def getrond(dsup, dinf, surep, long, typedepas):

    pasmax = long / 5 #car 5 fillets en prise minimum
    dmax = dsup - surep
    dmin = dinf + surep
    pas = 'pasgros' #typedepas == true

    if (typedepas == False):
        pas = 'pasfin'

    db = OpenDatabase()
    req = ExecuteDatabase(db, 'SELECT dnominal, ? FROM tabmetriquerond WHERE dnominal >= ? AND dnominal <= ? AND ? < ?'
                            , [ pas, dmin, dmax, pas, pasmax ])
    db = CloseDatabase(db)

    for i in req:
        reponse[i][0] = req[i][0]#diametre nominal
        reponse[i][1] = req[i][1]#pas
        reponse[i][2] = req[i][0] - req[i][1]#diametre fond filet vis
        reponse[i][3] = req[i][0] + 0.1 * req[i][1]#diametre fond filet ecrou
        reponse[i][4] = req[i][0] - 1.1 * req[i][1]#diametre forage / percage
        reponse[i][5] = 0.5 * req[i][1]#rayon
        reponse[i][6] = req[i][0] - 1.5 * req[i][1]#diametre sortie outil vis
        reponse[i][7] = 2 * req[i][1]#hauteur min sortie outil vis
        reponse[i][8] = 3 * req[i][1]#hauteur max sortie outil vis
        reponse[i][9] = 1.5 * req[i][1]#chanfrein
        reponse[i][10] = 2 * req[i][1]#hauteur min sortie outil ecrou
        reponse[i][11] = 4 * req[i][1]#hauteur max sortie outil ecrou
        reponse[i][12] = req[i][0] + 0.5 * req[i][1]#diametre sortie outil ecrou

    return reponse




if __name__ == '__main__':
    Initialize()
    app.run(debug = True)