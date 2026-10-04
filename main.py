from flask import Flask, redirect, request
from itertools import takewhile
import csv
import json
import math

# Serveur


app = Flask(__name__)  # crée un objet du serveur flask


def ReadFile(path):
    with open(path, "rb") as f:
        return f.read()


@app.route("/")  # si la route pas définie on a / alors on redirige vers index.html
def redirection():
    # Rediriger "/" vers "/index.html"
    return redirect("index.html", code=302)


@app.route("/index.html")
def index():
    return ReadFile("index.html")


@app.route("/app.js")
def javascript():
    return ReadFile("app.js")


@app.route("/GetMetrique", methods=["POST"])
def getmetriqueweb():
    return Find("M", Metrique, maxDiam=4, nbPasFins=4, colMax=3)


@app.route("/GetWithGaz", methods=["POST"])
def getwithgazweb():
    return Find("WG", WithGaz, maxDiam=3, nbPasFins=0, colMax=1)


@app.route("/GetTrapeze", methods=["POST"])
def gettrapezeweb():
    return Find("T", Trapeze, maxDiam=3, nbPasFins=1, colMax=3)


@app.route("/GetRond", methods=["POST"])
def getrondweb():
    return Find("M", Rond, maxDiam=3, nbPasFins=4, colMax=2)


# CSV file : ID;type;col;diam;pas gros;pas fin 1;...;pas fin 4, trié par diamètre croissant

with open("csvDB.csv", "r") as csvfile:
    LIGNES = list(csv.reader(csvfile, delimiter=";"))[1:]  # skip header line


def Find(typeCsv, calcul, maxDiam, nbPasFins, colMax):
    """Calcule les dimensions pour les maxDiam diamètres normalisés les plus proches du brut.
    colMax : dernière colonne de qualité acceptée en "Tout type" (sinon col 1 uniquement).
    """
    infos = json.loads(request.get_data())
    surep = float(infos["surep"])
    pasmax = float(infos["long"]) / 5  # car 5 fillets en prise minimum
    if int(infos.get("quality", 0)) == 0:
        colMax = 1
    if (
        infos["element"] == 1
    ):  # ecrou : les plus petits diamètres >= diametre ecrou non usiné + surep
        dmin = float(infos["denu"]) + surep
        lignes = [row for row in LIGNES if float(row[3]) >= dmin]
    else:  # vis : les plus grands diamètres <= diametre vis non usiné - surep
        dmax = float(infos["dvnu"]) - surep
        lignes = [row for row in reversed(LIGNES) if float(row[3]) <= dmax]

    result = []
    compteur = 0
    for row in lignes:
        diam, pasgros = float(row[3]), float(row[4])
        if row[1] != typeCsv or pasgros > pasmax or int(row[2]) > colMax:
            continue
        pas = [pasgros]
        if int(infos.get("pas", 0)) == 1:  # "pas gros" et "pas fin"
            pas += [float(p) for p in takewhile(bool, row[5 : 5 + nbPasFins])]
        pas = [
            p for p in pas if p != 0
        ]  # certains diamètres col 3 n'ont pas de pas gros
        if not pas:
            continue
        result += [calcul(diam, p, pasgros) for p in pas]
        compteur += 1
        if compteur == maxDiam:
            break
    return json.dumps(result)


# Une ligne de résultat par (diamètre, pas), colonnes dans l'ordre attendu par app.js


def Outil(d, p):
    # sortie/entrée d'outil et chanfrein, communs à tous les filets
    return [d - 1.5 * p, 2 * p, 3 * p, 1.5 * p, 2 * p, 4 * p, d + 0.5 * p]


def Metrique(d, p, pasgros):
    return [d, p, d - 1.082 * p, d - 1.226 * p, 0.5 * p] + Outil(d, p)


def WithGaz(d, p, pasgros):
    diamForage = d - (2 * p / (3 * math.tan(math.radians(27.5))))
    return [d, p, diamForage, 0.5 * p] + Outil(d, p)


def Trapeze(d, p, pasgros):
    if pasgros == 1.5:
        a = 0.15
    elif pasgros <= 5:
        a = 0.25
    elif pasgros <= 12:
        a = 0.5
    else:
        a = 1
    return [
        d,
        p,
        d - 2 * ((p / 2) + a),
        d + 2 * a,
        d - 2 * (p / 2),
        pasgros * 0.5,
        a / 2,
    ] + Outil(d, p)


def Rond(d, p, pasgros):
    return [d, p, d - p, d + (p / 10), d - p + (p / 10), 0.5 * p] + Outil(d, p)


if __name__ == "__main__":
    app.run(debug=True)
