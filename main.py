from flask import Flask, redirect, request 
import json
import math
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
                        print(compteur)
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
                            compteur+=1
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
                            compteur+=1
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
                            compteur+=1
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
                            compteur+=1
                        else :
                            compteur+=1
                            continue

    print (result)
    return result.tolist()






if __name__ == '__main__':
    app.run(debug = True)