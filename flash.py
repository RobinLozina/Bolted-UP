from flask import Flask, redirect, request #On importe le serveur flask ainsique des méthodes qui nous seront utilses comme redirect et request
import json
import sqlite3
import time
import math
import struct 
import csv
import numpy as np


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
    print("into getmetrique")
    if infos['element'] ==0:
        print("vis")
        result = GetMetriqueVis((infos['dvnu']), (infos['surep']), (infos['long']), int(infos['pas']), int(infos['quality']))

    elif infos['element'] ==1:
        print("ecrou")
        result = GetMetriqueEcrou((infos['denu']), (infos['surep']), (infos['long']), int(infos['pas']), int(infos['quality']))
    #dvnu pour diametre vis non usiné et denu pour diametre ecrou non usiné

    return json.dumps(result)

@app.route('/GetWithGaz', methods = [ 'POST' ])
def getwithgazweb():
    donnees = request.get_data()
    infos = json.loads(donnees)
    print("into getwithgaz")
    if infos['element'] ==0:
        print("vis")
        result = GetwithGazVis((infos['dvnu']), (infos['surep']), (infos['long']))
    elif infos['element'] ==1:
        print("ecrou")
        result = GetWithGazEcrou((infos['denu']), (infos['surep']), (infos['long']))
    return json.dumps(result)

@app.route('/GetTrapeze', methods = [ 'POST' ])
def gettrapezeweb():
    donnees = request.get_data()
    infos = json.loads(donnees)
    print("into gettrapeze")
    if infos['element'] ==0:
        print("vis")
        result = GetTrapezeVis((infos['dvnu']), (infos['surep']), (infos['long']), int(infos['pas']), int(infos['quality']))
    elif infos['element'] ==1:
        print("ecrou")
        result = GetTrapezeEcrou((infos['denu']), (infos['surep']), (infos['long']), int(infos['pas']), int(infos['quality']))
    return json.dumps(result)

@app.route('/GetRond', methods = [ 'POST' ])
def getrondweb():
    donnees = request.get_data()
    infos = json.loads(donnees)
    print("into getrond")
    if infos['element'] ==0:
        print("vis")
        result = GetRondVis((infos['dvnu']), (infos['surep']), (infos['long']), int(infos['pas']), int(infos['quality']))
    elif infos['element'] ==1:
        print("ecrou")
        result = GetRondEcrou((infos['denu']), (infos['surep']), (infos['long']), int(infos['pas']), int(infos['quality']))
    return json.dumps(result)


#CSV file

f="csvDB.csv"


def GetMetriqueVis(dsup, surep, long,pas,quality):
    dsup=float(dsup)
    surep=float(surep)
    long=float(long)
    pasmax = long / 5 #car 5 fillets en prise minimum
    dmax = dsup - surep
    compteur = 0
    result=np.empty((0,12)) #empty array( to store the results and return it
    with open(f, 'r') as csvfile:
        reader = csv.reader(csvfile,delimiter=';')
        next(reader) #skip header line
        for row in reversed(list(reader)):
            
            row[3]=float(row[3])
            row[4]=float(row[4])   
            row[2]=int(row[2])

            if quality == 0: #if we want only the col 1 values
                if pas == 0: #if we want only "pas gros"

                    if (row[1]=='M' and row[4]<=pasmax and row[2]==1 and compteur<4 and row[3]<=dmax):
                        cal=np.array([[row[3],row[4],row[3]-1.082*row[4],row[3]-1.226*row[4],0.5*row[4],row[3]-1.5*row[4],2*row[4],3*row[4],1.5*row[4],2*row[4],4*row[4],row[3]+0.5*row[4]]])
                        result=np.append(result,cal,axis=0)
                        compteur+=1


                else: #if we want "pas gros" and "pas fin"

                    if (row[1]=='M' and row[4]<=pasmax and row[2]==1 and compteur<4 and row[3]<=dmax):

                        if row[4] != "0":
                            cal=np.array([[row[3],row[4],row[3]-1.082*row[4],row[3]-1.226*row[4],0.5*row[4],row[3]-1.5*row[4],2*row[4],3*row[4],1.5*row[4],2*row[4],4*row[4],row[3]+0.5*row[4]]])
                            result=np.append(result,cal,axis=0)

                        row[5]=float(row[5])
                        cal1=np.array([[row[3],row[5],row[3]-1.082*row[5],row[3]-1.226*row[5],0.5*row[5],row[3]-1.5*row[5],2*row[5],3*row[5],1.5*row[5],2*row[5],4*row[5],row[3]+0.5*row[5]]])
                        result=np.append(result,cal1,axis=0)

                        if row[6] != "":
                            row[6]=float(row[6])
                            cal2=np.array([[row[3],row[6],row[3]-1.082*row[6],row[3]-1.226*row[6],0.5*row[6],row[3]-1.5*row[6],2*row[6],3*row[6],1.5*row[6],2*row[6],4*row[6],row[3]+0.5*row[6]]])
                            result=np.append(result,cal2,axis=0)
                        else :
                            compteur+=1
                            continue

                        if row[7] != "":
                            row[7]=float(row[7])
                            cal3=np.array([[row[3],row[7],row[3]-1.082*row[7],row[3]-1.226*row[7],0.5*row[7],row[3]-1.5*row[7],2*row[7],3*row[7],1.5*row[7],2*row[7],4*row[7],row[3]+0.5*row[7]]])
                            result=np.append(result,cal3,axis=0)
                        else :
                            compteur+=1
                            continue

                        if row[8] != "" :
                            row[8]=float(row[8])
                            cal4=np.array([[row[3],row[8],row[3]-1.082*row[8],row[3]-1.226*row[8],0.5*row[8],row[3]-1.5*row[8],2*row[8],3*row[8],1.5*row[8],2*row[8],4*row[8],row[3]+0.5*row[8]]])
                            result=np.append(result,cal4,axis=0)
                            compteur+=1
                        else :
                            compteur+=1
                            continue


            else: #if we want all the qualities

                if pas ==0: #if we want only "pas gros"

                    if (row[1]=='M' and row[4]<=pasmax  and compteur<4 and row[3]<=dmax and row[4]!=0):

                        cal=np.array([[row[3],row[4],row[3]-1.082*row[4],row[3]-1.226*row[4],0.5*row[4],row[3]-1.5*row[4],2*row[4],3*row[4],1.5*row[4],2*row[4],4*row[4],row[3]+0.5*row[4]]])
                        result=np.append(result,cal,axis=0)
                        compteur+=1

                else: #if we want "pas gros" and "pas fin"

                    if (row[1]=='M' and row[4]<=pasmax and compteur<4 and row[3]<=dmax):

                        if row[4] != "0":
                            cal=np.array([[row[3],row[4],row[3]-1.082*row[4],row[3]-1.226*row[4],0.5*row[4],row[3]-1.5*row[4],2*row[4],3*row[4],1.5*row[4],2*row[4],4*row[4],row[3]+0.5*row[4]]])
                            result=np.append(result,cal,axis=0)

                        row[5]=float(row[5])
                        cal1=np.array([[row[3],row[5],row[3]-1.082*row[5],row[3]-1.226*row[5],0.5*row[5],row[3]-1.5*row[5],2*row[5],3*row[5],1.5*row[5],2*row[5],4*row[5],row[3]+0.5*row[5]]])
                        result=np.append(result,cal1,axis=0)

                        if row[6] != "":
                            row[6]=float(row[6])
                            cal2=np.array([[row[3],row[6],row[3]-1.082*row[6],row[3]-1.226*row[6],0.5*row[6],row[3]-1.5*row[6],2*row[6],3*row[6],1.5*row[6],2*row[6],4*row[6],row[3]+0.5*row[6]]])
                            result=np.append(result,cal2,axis=0)
                        else :
                            compteur+=1
                            continue

                        if row[7] != "":
                            row[7]=float(row[7])
                            cal3=np.array([[row[3],row[7],row[3]-1.082*row[7],row[3]-1.226*row[7],0.5*row[7],row[3]-1.5*row[7],2*row[7],3*row[7],1.5*row[7],2*row[7],4*row[7],row[3]+0.5*row[7]]])
                            result=np.append(result,cal3,axis=0)
                        else :
                            compteur+=1
                            continue

                        if row[8] != "" :
                            row[8]=float(row[8])
                            cal4=np.array([[row[3],row[8],row[3]-1.082*row[8],row[3]-1.226*row[8],0.5*row[8],row[3]-1.5*row[8],2*row[8],3*row[8],1.5*row[8],2*row[8],4*row[8],row[3]+0.5*row[8]]])
                            result=np.append(result,cal4,axis=0)
                            compteur+=1
                        else :
                            compteur+=1
                            continue
    print (result)
    return result.tolist()




def GetMetriqueEcrou(dinf, surep, long,pas,quality):
    dinf=float(dinf)
    surep=float(surep)
    long=float(long)
    pasmax = long / 5 #car 5 fillets en prise minimum
    # dmax = dsup - surep
    dmin = dinf + surep
    compteur=0
    result=np.empty((0,12)) #empty array( to store the results and return it
    with open(f, 'r') as csvfile:
        reader = csv.reader(csvfile,delimiter=';')
        next(reader) #skip header line
        for row in reader:
            row[3]=float(row[3])
            row[4]=float(row[4])   
            row[2]=int(row[2])

            if quality == 0: #if we want only the col 1 values

                if pas == 0: #if we want only "pas gros"
            
                    if (row[1]=='M' and row[4]<=pasmax and row[2]==1 and row[3]>=dmin and compteur<4):
                        cal=np.array([[row[3],row[4],row[3]-1.082*row[4],row[3]-1.226*row[4],0.5*row[4],row[3]-1.5*row[4],2*row[4],3*row[4],1.5*row[4],2*row[4],4*row[4],row[3]+0.5*row[4]]])
                        result=np.append(result,cal,axis=0)
                        compteur+=1

                else: #if we want "pas gros" and "pas fin"

                    if (row[1]=='M' and row[4]<=pasmax and row[2]==1 and row[3]>=dmin and compteur<4):

                        if row[4] != "0":
                            cal=np.array([[row[3],row[4],row[3]-1.082*row[4],row[3]-1.226*row[4],0.5*row[4],row[3]-1.5*row[4],2*row[4],3*row[4],1.5*row[4],2*row[4],4*row[4],row[3]+0.5*row[4]]])
                            result=np.append(result,cal,axis=0)

                        row[5]=float(row[5])
                        cal1=np.array([[row[3],row[5],row[3]-1.082*row[5],row[3]-1.226*row[5],0.5*row[5],row[3]-1.5*row[5],2*row[5],3*row[5],1.5*row[5],2*row[5],4*row[5],row[3]+0.5*row[5]]])
                        result=np.append(result,cal1,axis=0)

                        if row[6] != "":
                            row[6]=float(row[6])
                            cal2=np.array([[row[3],row[6],row[3]-1.082*row[6],row[3]-1.226*row[6],0.5*row[6],row[3]-1.5*row[6],2*row[6],3*row[6],1.5*row[6],2*row[6],4*row[6],row[3]+0.5*row[6]]])
                            result=np.append(result,cal2,axis=0)
                        else :
                            compteur+=1
                            continue

                        if row[7] != "":
                            row[7]=float(row[7])
                            cal3=np.array([[row[3],row[7],row[3]-1.082*row[7],row[3]-1.226*row[7],0.5*row[7],row[3]-1.5*row[7],2*row[7],3*row[7],1.5*row[7],2*row[7],4*row[7],row[3]+0.5*row[7]]])
                            result=np.append(result,cal3,axis=0)
                        else :
                            compteur+=1
                            continue

                        if row[8] != "" :
                            row[8]=float(row[8])
                            cal4=np.array([[row[3],row[8],row[3]-1.082*row[8],row[3]-1.226*row[8],0.5*row[8],row[3]-1.5*row[8],2*row[8],3*row[8],1.5*row[8],2*row[8],4*row[8],row[3]+0.5*row[8]]])
                            result=np.append(result,cal4,axis=0)
                            compteur+=1
                        else :
                            compteur+=1
                            continue


                 
            else: #if we want all the qualities

                if pas ==0: #if we want only "pas gros"

                    if (row[1]=='M' and row[4]<=pasmax and row[3]>=dmin and compteur<4 and row[4]!=0):
                        cal=np.array([[row[3],row[4],row[3]-1.082*row[4],row[3]-1.226*row[4],0.5*row[4],row[3]-1.5*row[4],2*row[4],3*row[4],1.5*row[4],2*row[4],4*row[4],row[3]+0.5*row[4]]])
                        result=np.append(result,cal,axis=0)
                        compteur+=1

                else: #if we want "pas gros" and "pas fin"

                    if (row[1]=='M' and row[4]<=pasmax and row[3]>=dmin and compteur<4):

                        if row[4] != "0":
                            cal=np.array([[row[3],row[4],row[3]-1.082*row[4],row[3]-1.226*row[4],0.5*row[4],row[3]-1.5*row[4],2*row[4],3*row[4],1.5*row[4],2*row[4],4*row[4],row[3]+0.5*row[4]]])
                            result=np.append(result,cal,axis=0)
                        
                        row[5]=float(row[5])
                        cal1=np.array([[row[3],row[5],row[3]-1.082*row[5],row[3]-1.226*row[5],0.5*row[5],row[3]-1.5*row[5],2*row[5],3*row[5],1.5*row[5],2*row[5],4*row[5],row[3]+0.5*row[5]]])
                        result=np.append(result,cal1,axis=0)

                        if row[6] != "":
                            row[6]=float(row[6])
                            cal2=np.array([[row[3],row[6],row[3]-1.082*row[6],row[3]-1.226*row[6],0.5*row[6],row[3]-1.5*row[6],2*row[6],3*row[6],1.5*row[6],2*row[6],4*row[6],row[3]+0.5*row[6]]])
                            result=np.append(result,cal2,axis=0)
                        else :
                            compteur+=1  
                            continue

                        if row[7] != "":
                            row[7]=float(row[7])
                            cal3=np.array([[row[3],row[7],row[3]-1.082*row[7],row[3]-1.226*row[7],0.5*row[7],row[3]-1.5*row[7],2*row[7],3*row[7],1.5*row[7],2*row[7],4*row[7],row[3]+0.5*row[7]]])
                            result=np.append(result,cal3,axis=0)
                        else :
                            compteur+=1 
                            continue

                        if row[8] != "" :
                            row[8]=float(row[8])
                            cal4=np.array([[row[3],row[8],row[3]-1.082*row[8],row[3]-1.226*row[8],0.5*row[8],row[3]-1.5*row[8],2*row[8],3*row[8],1.5*row[8],2*row[8],4*row[8],row[3]+0.5*row[8]]])
                            result=np.append(result,cal4,axis=0)
                            compteur+=1
                        else :
                            compteur+=1
                            continue
                        
                    
    print (result)
    return result.tolist()


def GetwithGazVis (dsup, surep, long):
    dsup=float(dsup)
    surep=float(surep)
    long=float(long)
    pasmax = long / 5 #car 5 fillets en prise minimum
    dmax = dsup - surep
    compteur=0
    result=np.empty((0,11)) #empty array( to store the results and return it
    with open(f, 'r') as csvfile:
        reader = csv.reader(csvfile,delimiter=';')
        next(reader) #skip the first line
        for row in reversed(list(reader)):

            row[3]=float(row[3])
            row[4]=float(row[4])   
            row[2]=int(row[2])

            if row[1]=='WG' and row[3]<=dmax and row[4]<=pasmax and compteur<3:
                diamForage = row[3] - (2 * row[4] / (3 * math.tan(math.radians(27.5))))
                cal=np.array([[row[3],row[4],diamForage,0.5*row[4],row[3]-1.5*row[4],2*row[4],3*row[4],1.5*row[4],2*row[4],4*row[4],row[3]+0.5*row[4]]])
                result=np.append(result,cal,axis=0)
                compteur+=1

    print (result)
    return result.tolist()

def GetWithGazEcrou (dinf, surep, long):
    dinf=float(dinf)
    surep=float(surep)
    long=float(long)
    pasmax = long / 5 #car 5 fillets en prise minimum
    dmin = dinf + surep
    compteur=0
    result=np.empty((0,11)) #empty array to store the results and return it
    with open(f, 'r') as csvfile:
        reader = csv.reader(csvfile,delimiter=';')
        next(reader) #skip the first line
        for row in reader:
            row[3]=float(row[3])
            row[4]=float(row[4])   
            row[2]=int(row[2])

            if row[1]=='WG' and row[3]>=dmin and row[4]<=pasmax and compteur<3:
                diamForage = row[3] - (2 * row[4] / (3 * math.tan(math.radians(27.5))))
                cal=np.array([[row[3],row[4],diamForage,0.5*row[4],row[3]-1.5*row[4],2*row[4],3*row[4],1.5*row[4],2*row[4],4*row[4],row[3]+0.5*row[4]]])
                result=np.append(result,cal,axis=0)
                compteur+=1

    print (result)
    return result.tolist()


def GetTrapezeVis (dsup, surep, long,pas,quality):
    dsup=float(dsup)
    surep=float(surep)
    long=float(long)
    pasmax = long / 5 #car 5 fillets en prise minimum
    dmax = dsup - surep
    compteur=0
    result=np.empty((0,14)) #empty array to store the results and return it
    with open(f, 'r') as csvfile:
        reader = csv.reader(csvfile,delimiter=';')
        next(reader) #skip the header

        for row in reversed(list(reader)):
           row[3]=float(row[3])
           row[4]=float(row[4])   
           row[2]=int(row[2])

           if quality == 0: #if we want only the col 1 values
                if pas == 0: #if we want only "pas gros"
                    if row[1]=='T' and row[3]<=dmax and row[4]<=pasmax and row[2]==1 and compteur<3:

                        if row[4]==1.5 :
                            a=0.15
                        elif row[4]<=5 :
                            a=0.25
                        elif row[4]<=12 :
                            a=0.5
                        else:
                            a=1

                        cal=np.array([[row[3],row[4],row[3]-2*((row[4]/2)+a),row[3]+2*a,row[3]-2*(row[4]/2),row[4]*0.5,a/2,row[3]-1.5*row[4],2*row[4],3*row[4],1.5*row[4],2*row[4],4*row[4],row[3]+0.5*row[4]]])
                        result=np.append(result,cal,axis=0)
                        compteur+=1

                else: #if we want "pas gros" and "pas fin"

                    if row[1]=='T' and row[3]<=dmax and row[4]<=pasmax and row[2]==1 and compteur<3:
            
                        if row[4]==1.5 :
                            a=0.15
                        elif row[4]<=5 :
                            a=0.25
                        elif row[4]<=12 :
                            a=0.5
                        else:
                            a=1
                        
                        cal=np.array([row[3],row[4],row[3]-2*((row[4]/2)+a),row[3]+2*a,row[3]-2*(row[4]/2),row[4]*0.5,a/2,row[3]-1.5*row[4],2*row[4],3*row[4],1.5*row[4],2*row[4],4*row[4],row[3]+0.5*row[4]])
                        result=np.append(result,cal,axis=0)
                        if row[5] != "":
                            row[5]=float(row[5])
                            cal1=np.array([[row[3],row[5],row[3]-2*((row[5]/2)+a),row[3]+2*a,row[3]-2*(row[5]/2),row[4]*0.5,a/2,row[3]-1.5*row[5],2*row[5],3*row[5],1.5*row[5],2*row[5],4*row[5],row[3]+0.5*row[5]]])
                            result=np.append(result,cal1,axis=0)
                            compteur+=1
                        else :
                            compteur+=1
                            continue

           else:
                if pas ==0: #if we want only "pas gros"

                    if row[1]=='T' and row[3]<=dmax and row[4]<=pasmax and compteur<3:
                        
                        if row[4]==1.5 :
                            a=0.15
                        elif row[4]<=5 :
                            a=0.25
                        elif row[4]<=12 :
                            a=0.5
                        else:
                            a=1

                        cal=np.array([[row[3],row[4],row[3]-2*((row[4]/2)+a),row[3]+2*a,row[3]-2*(row[4]/2),row[4]*0.5,a/2,row[3]-1.5*row[4],2*row[4],3*row[4],1.5*row[4],2*row[4],4*row[4],row[3]+0.5*row[4]]])
                        result=np.append(result,cal,axis=0)
                        compteur+=1

                else: #if we want "pas gros" and "pas fin"

                    if row[1]=='T' and row[3]<=dmax and row[4]<=pasmax and compteur<3:
            
                        if row[4]==1.5 :
                            a=0.15
                        elif row[4]<=5 :
                            a=0.25
                        elif row[4]<=12 :
                            a=0.5
                        else:
                            a=1
                        
                        cal=np.array([[row[3],row[4],row[3]-2*((row[4]/2)+a),row[3]+2*a,row[3]-2*(row[4]/2),row[4]*0.5,a/2,row[3]-1.5*row[4],2*row[4],3*row[4],1.5*row[4],2*row[4],4*row[4],row[3]+0.5*row[4]]])
                        result=np.append(result,cal,axis=0)
                        if row[5] != "":
                            row[5]=float(row[5])
                            cal1=np.array([[row[3],row[5],row[3]-2*((row[5]/2)+a),row[3]+2*a,row[3]-2*(row[5]/2),row[4]*0.5,a/2,row[3]-1.5*row[5],2*row[5],3*row[5],1.5*row[5],2*row[5],4*row[5],row[3]+0.5*row[5]]])
                            result=np.append(result,cal1,axis=0)
                            compteur+=1
                        else :
                            compteur+=1
                            continue

    print (result)
    return result.tolist()                


def GetTrapezeEcrou (dinf, surep, long,pas,quality):
    dinf=float(dinf)
    surep=float(surep)
    long=float(long)
    pasmax = long / 5 #car 5 fillets en prise minimum
    dmin = dinf + surep
    compteur=0
    result=np.empty((0,14)) #empty array to store the results and return it
    with open(f, 'r') as csvfile:
        reader = csv.reader(csvfile,delimiter=';')
        next(reader) #skip the header

        for row in reader:
           row[3]=float(row[3])
           row[4]=float(row[4])   
           row[2]=int(row[2])

           if quality == 0: #if we want only the col 1 values
                if pas == 0: #if we want only "pas gros"
                    if row[1]=='T'and row[3]>=dmin and row[4]<=pasmax and row[2]==1 and compteur<3:
                        
                        if row[4]==1.5 :
                            a=0.15
                        elif row[4]<=5 :
                            a=0.25
                        elif row[4]<=12 :
                            a=0.5
                        else:
                            a=1

                        cal=np.array([[row[3],row[4],row[3]-2*((row[4]/2)+a),row[3]+2*a,row[3]-2*(row[4]/2),row[4]*0.5,a/2,row[3]-1.5*row[4],2*row[4],3*row[4],1.5*row[4],2*row[4],4*row[4],row[3]+0.5*row[4]]])
                        result=np.append(result,cal,axis=0)
                        compteur+=1

                else: #if we want "pas gros" and "pas fin"

                    if row[1]=='T'and row[3]>=dmin and row[4]<=pasmax and row[2]==1 and compteur<3:
            
                        if row[4]==1.5 :
                            a=0.15
                        elif row[4]<=5 :
                            a=0.25
                        elif row[4]<=12 :
                            a=0.5
                        else:
                            a=1
                        
                        cal=np.array([[row[3],row[4],row[3]-2*((row[4]/2)+a),row[3]+2*a,row[3]-2*(row[4]/2),row[4]*0.5,a/2,row[3]-1.5*row[4],2*row[4],3*row[4],1.5*row[4],2*row[4],4*row[4],row[3]+0.5*row[4]]])
                        result=np.append(result,cal,axis=0)
                        if row[5] != "":
                            row[5]=float(row[5])
                            cal1=np.array([[row[3],row[5],row[3]-2*((row[5]/2)+a),row[3]+2*a,row[3]-2*(row[5]/2),row[4]*0.5,a/2,row[3]-1.5*row[5],2*row[5],3*row[5],1.5*row[5],2*row[5],4*row[5],row[3]+0.5*row[5]]])
                            result=np.append(result,cal1,axis=0)
                            compteur+=1
                        else :
                            compteur+=1
                            continue

           else:
                if pas ==0: #if we want only "pas gros"

                    if row[1]=='T'and row[3]>=dmin and row[4]<=pasmax and compteur<3:
                        
                        if row[4]==1.5 :
                            a=0.15
                        elif row[4]<=5 :
                            a=0.25
                        elif row[4]<=12 :
                            a=0.5
                        else:
                            a=1

                        cal=np.array([[row[3],row[4],row[3]-2*((row[4]/2)+a),row[3]+2*a,row[3]-2*(row[4]/2),row[4]*0.5,a/2,row[3]-1.5*row[4],2*row[4],3*row[4],1.5*row[4],2*row[4],4*row[4],row[3]+0.5*row[4]]])
                        result=np.append(result,cal,axis=0)
                        compteur+=1

                else: #if we want "pas gros" and "pas fin"

                    if row[1]=='T'and row[3]>=dmin and row[4]<=pasmax and compteur<3:
            
                        if row[4]==1.5 :
                            a=0.15
                        elif row[4]<=5 :
                            a=0.25
                        elif row[4]<=12 :
                            a=0.5
                        else:
                            a=1
                        
                        cal=np.array([[row[3],row[4],row[3]-2*((row[4]/2)+a),row[3]+2*a,row[3]-2*(row[4]/2),row[4]*0.5,a/2,row[3]-1.5*row[4],2*row[4],3*row[4],1.5*row[4],2*row[4],4*row[4],row[3]+0.5*row[4]]])
                        result=np.append(result,cal,axis=0)
                        if row[5] != "":
                            row[5]=float(row[5])
                            cal1=np.array([[row[3],row[5],row[3]-2*((row[5]/2)+a),row[3]+2*a,row[3]-2*(row[5]/2),row[4]*0.5,a/2,row[3]-1.5*row[5],2*row[5],3*row[5],1.5*row[5],2*row[5],4*row[5],row[3]+0.5*row[5]]])
                            result=np.append(result,cal1,axis=0)
                            compteur+=1
                        else :
                            compteur+=1
                            continue

    print (result)
    return result.tolist()
                

def GetRondVis(dsup, surep, long, pas,quality):
    dsup=float(dsup)
    surep=float(surep)
    long=float(long)
    pasmax = long / 5 #car 5 fillets en prise minimum
    dmax = dsup - surep
    result=np.empty((0,13))
    compteur=0
    with open(f, 'r') as csvfile:
        reader = csv.reader(csvfile,delimiter=';')
        next(reader)
        for row in reversed(list(reader)):
            row[3]=float(row[3])
            row[4]=float(row[4])   
            row[2]=int(row[2])
            if quality == 0: #if we want only the col 1 values
                if pas == 0: #if we want only "pas gros"
                    if row[1]=='M' and row[3]<=dmax and row[4]<=pasmax and row[2]==1 and compteur<3:

                        cal=np.array([[row[3],row[4],row[3]-row[4],row[3]+(row[4]/10),row[3]-row[4]+(row[4]/10),0.5*row[4],row[3]-1.5*row[4],2*row[4],3*row[4],1.5*row[4],2*row[4],4*row[4],row[3]+0.5*row[4]]])
                        result=np.append(result,cal,axis=0)
                        compteur+=1

                else: #if we want "pas gros" and "pas fin"

                    if row[1]=='M' and row[3]<=dmax and row[4]<=pasmax and row[2]==1 and compteur<3:
                        if row[4] != "0":
                            cal=np.array([[row[3],row[4],row[3]-row[4],row[3]+(row[4]/10),row[3]-row[4]+(row[4]/10),0.5*row[4],row[3]-1.5*row[4],2*row[4],3*row[4],1.5*row[4],2*row[4],4*row[4],row[3]+0.5*row[4]]])
                            result=np.append(result,cal,axis=0)

                        row[5]=float(row[5])
                        cal1=np.array([[row[3],row[5],row[3]-row[5],row[3]+(row[5]/10),row[3]-row[5]+(row[5]/10),0.5*row[5],row[3]-1.5*row[5],2*row[5],3*row[5],1.5*row[5],2*row[5],4*row[5],row[3]+0.5*row[5]]])
                        result=np.append(result,cal1,axis=0)

                        if row[6] != "":
                            row[6]=float(row[6])
                            cal2=np.array([[row[3],row[6],row[3]-row[6],row[3]+(row[6]/10),row[3]-row[6]+(row[6]/10),0.5*row[6],row[3]-1.5*row[6],2*row[6],3*row[6],1.5*row[6],2*row[6],4*row[6],row[3]+0.5*row[6]]])
                            result=np.append(result,cal2,axis=0)
                        else :
                            compteur+=1
                            continue
                        if row[7] != "":
                            row[7]=float(row[7])
                            cal3=np.array([[row[3],row[7],row[3]-row[7],row[3]+(row[7]/10),row[3]-row[7]+(row[7]/10),0.5*row[7],row[3]-1.5*row[7],2*row[7],3*row[7],1.5*row[7],2*row[7],4*row[7],row[3]+0.5*row[7]]])
                            result=np.append(result,cal3,axis=0)
                        else :
                            compteur+=1
                            continue
                        if row[8] != "":
                            row[8]=float(row[8])
                            cal4=np.array([[row[3],row[8],row[3]-row[8],row[3]+(row[8]/10),row[3]-row[8]+(row[8]/10),0.5*row[8],row[3]-1.5*row[8],2*row[8],3*row[8],1.5*row[8],2*row[8],4*row[8],row[3]+0.5*row[8]]])
                            result=np.append(result,cal4,axis=0)
                        else :
                            compteur+=1
                            continue


            else:
                if pas ==0: #if we want only "pas gros"

                    if row[1]=='M' and row[3]<=dmax and row[4]<=pasmax and row[2]<3 and compteur<3:
                        cal=np.array([[row[3],row[4],row[3]-row[4],row[3]+(row[4]/10),row[3]-row[4]+(row[4]/10),0.5*row[4],row[3]-1.5*row[4],2*row[4],3*row[4],1.5*row[4],2*row[4],4*row[4],row[3]+0.5*row[4]]])
                        result=np.append(result,cal,axis=0)
                        compteur+=1

                else: #if we want "pas gros" and "pas fin"

                    if row[1]=='M' and row[3]<=dmax and row[4]<=pasmax and row[2]<3 and compteur<3:
                        if row[4] != "0":
                            cal=np.array([[row[3],row[4],row[3]-row[4],row[3]+(row[4]/10),row[3]-row[4]+(row[4]/10),0.5*row[4],row[3]-1.5*row[4],2*row[4],3*row[4],1.5*row[4],2*row[4],4*row[4],row[3]+0.5*row[4]]])
                            result=np.append(result,cal,axis=0)

                        row[5]=float(row[5])
                        cal1=np.array([[row[3],row[5],row[3]-row[5],row[3]+(row[5]/10),row[3]-row[5]+(row[5]/10),0.5*row[5],row[3]-1.5*row[5],2*row[5],3*row[5],1.5*row[5],2*row[5],4*row[5],row[3]+0.5*row[5]]])
                        result=np.append(result,cal1,axis=0)

                        if row[6] != "":
                            row[6]=float(row[6])
                            cal2=np.array([[row[3],row[6],row[3]-row[6],row[3]+(row[6]/10),row[3]-row[6]+(row[6]/10),0.5*row[6],row[3]-1.5*row[6],2*row[6],3*row[6],1.5*row[6],2*row[6],4*row[6],row[3]+0.5*row[6]]])
                            result=np.append(result,cal2,axis=0)
                        else :
                            compteur+=1
                            continue
                        if row[7] != "":
                            row[7]=float(row[7])
                            cal3=np.array([[row[3],row[7],row[3]-row[7],row[3]+(row[7]/10),row[3]-row[7]+(row[7]/10),0.5*row[7],row[3]-1.5*row[7],2*row[7],3*row[7],1.5*row[7],2*row[7],4*row[7],row[3]+0.5*row[7]]])
                            result=np.append(result,cal3,axis=0)
                        else :
                            compteur+=1
                            continue
                        if row[8] != "" :
                            row[8]=float(row[8])
                            cal4=np.array([[row[3],row[8],row[3]-row[8],row[3]+(row[8]/10),row[3]-row[8]+(row[8]/10),0.5*row[8],row[3]-1.5*row[8],2*row[8],3*row[8],1.5*row[8],2*row[8],4*row[8],row[3]+0.5*row[8]]])
                            result=np.append(result,cal4,axis=0)
                        else :
                            compteur+=1
                            continue

    print (result)
    return result.tolist()


def GetRondEcrou (dinf, surep, long, pas,quality):
    dinf=float(dinf)
    surep=float(surep)
    long=float(long)
    pasmax = long / 5 #car 5 fillets en prise minimum
    dmin = dinf + surep
    result=np.empty((0,13))
    compteur=0
    with open(f, 'r') as csvfile:
        reader = csv.reader(csvfile,delimiter=';')
        next(reader)
        for row in reader:
            row[3]=float(row[3])
            row[4]=float(row[4])   
            row[2]=int(row[2])
            if quality == 0: #if we want only the col 1 values
                if pas == 0: #if we want only "pas gros"
                    if row[1]=='M'and row[3]>=dmin and row[4]<=pasmax and row[2]==1 and compteur<3:

                        cal=np.array([[row[3],row[4],row[3]-row[4],row[3]+(row[4]/10),row[3]-row[4]+(row[4]/10),0.5*row[4],row[3]-1.5*row[4],2*row[4],3*row[4],1.5*row[4],2*row[4],4*row[4],row[3]+0.5*row[4]]])
                        result=np.append(result,cal,axis=0)
                        compteur+=1

                else: #if we want "pas gros" and "pas fin"

                    if row[1]=='M' and row[3]>=dmin and row[4]<=pasmax and row[2]==1 and compteur<3:
                        if row[4] != "0":
                            cal=np.array([[row[3],row[4],row[3]-row[4],row[3]+(row[4]/10),row[3]-row[4]+(row[4]/10),0.5*row[4],row[3]-1.5*row[4],2*row[4],3*row[4],1.5*row[4],2*row[4],4*row[4],row[3]+0.5*row[4]]])
                            result=np.append(result,cal,axis=0)

                        row[5]=float(row[5])
                        cal1=np.array([[row[3],row[5],row[3]-row[5],row[3]+(row[5]/10),row[3]-row[5]+(row[5]/10),0.5*row[5],row[3]-1.5*row[5],2*row[5],3*row[5],1.5*row[5],2*row[5],4*row[5],row[3]+0.5*row[5]]])
                        result=np.append(result,cal1,axis=0)

                        if row[6] != "":
                            row[6]=float(row[6])
                            cal2=np.array([[row[3],row[6],row[3]-row[6],row[3]+(row[6]/10),row[3]-row[6]+(row[6]/10),0.5*row[6],row[3]-1.5*row[6],2*row[6],3*row[6],1.5*row[6],2*row[6],4*row[6],row[3]+0.5*row[6]]])
                            result=np.append(result,cal2,axis=0)
                        else :
                            compteur+=1
                            continue
                        if row[7] != "":
                            row[7]=float(row[7])
                            cal3=np.array([[row[3],row[7],row[3]-row[7],row[3]+(row[7]/10),row[3]-row[7]+(row[7]/10),0.5*row[7],row[3]-1.5*row[7],2*row[7],3*row[7],1.5*row[7],2*row[7],4*row[7],row[3]+0.5*row[7]]])
                            result=np.append(result,cal3,axis=0)
                        else :
                            compteur+=1
                            continue
                        if row[8] != "":
                            row[8]=float(row[8])
                            cal4=np.array([[row[3],row[8],row[3]-row[8],row[3]+(row[8]/10),row[3]-row[8]+(row[8]/10),0.5*row[8],row[3]-1.5*row[8],2*row[8],3*row[8],1.5*row[8],2*row[8],4*row[8],row[3]+0.5*row[8]]])
                            result=np.append(result,cal4,axis=0)
                        else :
                            compteur+=1
                            continue


            else:
                if pas ==0: #if we want only "pas gros"

                    if row[1]=='M' and row[3]>=dmin and row[4]<=pasmax and row[2]<3 and compteur<3:
                        cal=np.array([[row[3],row[4],row[3]-row[4],row[3]+(row[4]/10),row[3]-row[4]+(row[4]/10),0.5*row[4],row[3]-1.5*row[4],2*row[4],3*row[4],1.5*row[4],2*row[4],4*row[4],row[3]+0.5*row[4]]])
                        result=np.append(result,cal,axis=0)
                        compteur+=1

                else: #if we want "pas gros" and "pas fin"

                    if row[1]=='M'and row[3]>=dmin and row[4]<=pasmax and row[2]<3 and compteur<3:
                        if row[4] != "0":
                            cal=np.array([[row[3],row[4],row[3]-row[4],row[3]+(row[4]/10),row[3]-row[4]+(row[4]/10),0.5*row[4],row[3]-1.5*row[4],2*row[4],3*row[4],1.5*row[4],2*row[4],4*row[4],row[3]+0.5*row[4]]])
                            result=np.append(result,cal,axis=0)

                        row[5]=float(row[5])
                        cal1=np.array([[row[3],row[5],row[3]-row[5],row[3]+(row[5]/10),row[3]-row[5]+(row[5]/10),0.5*row[5],row[3]-1.5*row[5],2*row[5],3*row[5],1.5*row[5],2*row[5],4*row[5],row[3]+0.5*row[5]]])
                        result=np.append(result,cal1,axis=0)

                        if row[6] != "":
                            row[6]=float(row[6])
                            cal2=np.array([[row[3],row[6],row[3]-row[6],row[3]+(row[6]/10),row[3]-row[6]+(row[6]/10),0.5*row[6],row[3]-1.5*row[6],2*row[6],3*row[6],1.5*row[6],2*row[6],4*row[6],row[3]+0.5*row[6]]])
                            result=np.append(result,cal2,axis=0)
                        else :
                            compteur+=1
                            continue
                        if row[7] != "":
                            row[7]=float(row[7])
                            cal3=np.array([[row[3],row[7],row[3]-row[7],row[3]+(row[7]/10),row[3]-row[7]+(row[7]/10),0.5*row[7],row[3]-1.5*row[7],2*row[7],3*row[7],1.5*row[7],2*row[7],4*row[7],row[3]+0.5*row[7]]])
                            result=np.append(result,cal3,axis=0)
                        else :
                            compteur+=1
                            continue
                        if row[8] != "":
                            row[8]=float(row[8])
                            cal4=np.array([[row[3],row[8],row[3]-row[8],row[3]+(row[8]/10),row[3]-row[8]+(row[8]/10),0.5*row[8],row[3]-1.5*row[8],2*row[8],3*row[8],1.5*row[8],2*row[8],4*row[8],row[3]+0.5*row[8]]])
                            result=np.append(result,cal4,axis=0)
                        else :
                            compteur+=1
                            continue

    print (result)
    return result.tolist()




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

#         Mais du coup 12 en tout

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

#           Mais du coup 11 en tout
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
#         reponse[i][6]          RAYON 2
#         reponse[i][7] = req[i][0] - 1.5 * req[i][1]#diametre sortie outil vis
#         reponse[i][8] = 2 * req[i][1]#hauteur min sortie outil vis
#         reponse[i][9] = 3 * req[i][1]#hauteur max sortie outil vis
#         reponse[i][10] = 1.5 * req[i][1]#chanfrein
#         reponse[i][11] = 2 * req[i][1]#hauteur min sortie outil ecrou
#         reponse[i][12] = 4 * req[i][1]#hauteur max sortie outil ecrou
#         reponse[i][13] = req[i][0] + 0.5 * req[i][1]#diametre sortie outil ecrou

#           Mais du coup 14 en tout

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

#           Mais du coup 13 en tout
#     return reponse




if __name__ == '__main__':
    app.run(debug = True)