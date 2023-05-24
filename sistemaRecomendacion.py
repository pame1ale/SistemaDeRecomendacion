import time
import pandas as pd

umbral = 10
class dataBase:
    def leerDatos():
        nombre_archivo = "20Mratings.csv"
        dataframe = pd.read_csv(nombre_archivo)

        user = dataframe['userId'].tolist()
        movie = dataframe['movieId'].tolist()
        rating = dataframe['rating'].tolist()

        data = {}
        for u, m, r in zip(user, movie, rating):
            if u not in data:
                data[u] = {}
            data[u][m] = r

        return data

def k_nn(funcion, user1, reverse,data):
    currentRating={}
    aux=0
    temp1 = ""
    for key in data:
        if key!=user1:
            temp1 = str(funcion(data[user1],data[key]))
            if temp1 != 'Naff' and temp1 != 'None':
                currentRating[key]=temp1
    sorted_desserts = dict(sorted(currentRating.items(), key=lambda item:item[1],reverse=reverse))
    currentRating={}
    for key,valor in sorted_desserts.items():
        if aux == umbral :
            break
        else:
            currentRating[key]=valor
            #print(key,valor)
            aux +=1
    return currentRating

def coseno(user1, user2):
    sum_xy= 0
    sum_x2 = 0
    sum_y2 = 0
    n = 0
    for key in user1:
        if key in user2:
            n +=1
            x = user1[key]
            y = user2[key]
            sum_xy += x*y
            sum_x2 += x**2
            sum_y2 += y**2
    if n == 0:
        return 'None'
    if sum_x2 == sum_y2:
        denominator = sum_x2
    else:
        denominator = round(pow(sum_x2,1/2) * pow(sum_y2,1/2),8)
    if denominator == 0:
        return 'Naff'
    else:
        return sum_xy/denominator

def agregarUsuario(path=''):
    f=codecs.open(path+"20Mratings.csv","a")
    usuarioAtributos = input()
    f.write(usuarioAtributos+'\n')
    f.close()
    return 0

def ratingMayorUser(user1,data):
    rating={}
    for key , valor in data[user1].items():
        rating[key] = valor
    sorted_rating = dict(sorted(rating.items() , key=lambda item:item[1],reverse=True))
    for key,valor in sorted_rating.items():
        ratingMayor = valor
        break
    return ratingMayor


def recomendar(user1,numRec,data):
    recomendarID = []
    recomendar = []
    aux = 0
    temp = 0
    currentRating = {}
    valorR = 0
    currentRatingR = k_nn(coseno,user1,True,data)
    ratingMayor = ratingMayorUser(user1,data)
    for user2 , valor in currentRatingR.items():
        if aux != numRec :
            valorR = float(valor)
            if valorR >= 0.8 and valorR <= 1: 
                for key,rating in data[user2].items():
                    if not key in  data[user1] and rating > ratingMayor-1:
                        currentRating[key] = rating
                sorted_desserts = dict(sorted(currentRating.items() , key=lambda item:item[1],reverse=True))
                for key in sorted_desserts:
                    if not key in recomendarID:
                        recomendar.append(BuscarId(key))
                        recomendarID.append(key)        
                        aux +=1
                        if aux == numRec:
                            break
    print(recomendarID)
    return recomendar

def BuscarId(ID):
    n = []
    nombre_archivo = "movies.csv"
    dataframe = pd.read_csv(nombre_archivo)

    movieId = dataframe['movieId'].tolist()
    title = dataframe['title'].tolist()
    genres = dataframe['genres'].tolist()

    data = {}
    for u, m in zip(movieId, title):
        if u == ID:
            n = m
            break
    return n

i = time.time()
data = dataBase
dataLocal=data.leerDatos()
f = time.time()
print("tiempoData : ",f - i)

i_rec = time.time()
print(recomendar(69000,5,dataLocal))
f_rec = time.time()
print(" tiempoRecomendar : ",f_rec - i_rec)
