import codecs
import math

umbral = 10
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

def manhattan(user1, user2):
    dist= 0
    c_Ratings = False 
    for key in user1:
    	if key in user2:
        	#print(key)
        	dist += abs(user1[key] - user2[key])
        	c_Ratings = True
    if c_Ratings:
    	return dist
    else:
    	return 'None'  

def euclidean(user1, user2):
	dist = 0
	c_Ratings = False
	for key in user1:
		if key in user2:
			dist += pow(abs(user1[key]-user2[key]),2)
			c_Ratings = True
	if c_Ratings:
		return pow(dist,1/2)
	else:
		return 'None'

def pearson(user1, user2):
	sum_xy= 0
	sum_x = 0
	sum_y = 0
	sum_x2 = 0
	sum_y2 = 0
	n = 0
	for key in user1:
		if key in user2:
			n += 1
			x = user1[key]
			y = user1[key]
			sum_xy += x*y
			sum_x += x
			sum_y += y
			sum_x2 += x**2
			sum_y2 += y**2
	if n == 0:
		return 'None'

	dif_sumx2_sum_x = pow(sum_x2 - (sum_x**2)/n,1/2)
	dif_sumy2_sum_y = pow(sum_y2 - (sum_y**2)/n,1/2)
	
	numerator =  round((sum_xy - (sum_x * sum_y)/n), 8)
	denominador = round(dif_sumx2_sum_x*dif_sumy2_sum_y, 8)

	if denominador == 0:
		return 'Naff'
	else:
		return numerator/denominador

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

def ratingMayorUser(user1):
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
	currentRatingR = k_nn(pearson,user1,True,data)
	ratingMayor = ratingMayorUser(user1)
	if len(currentRatingR) == 0:
		currentRatingR = k_nn(coseno,user1,True,data)
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
	idd= []
	idd.append(ID)
	f=codecs.open("movies.csv",'r','utf8')
	lineset = [line for line in f]
	for i in range(1,len(lineset)):
		linea = lineset[i].split(',')
		idM = linea[0].split(',')
		atributo = linea[1].split(',')
		if idM == idd:
			n = atributo
			break
	return n

def loadData(path=''):
    data={}
    f=codecs.open(path+"20Mratings.csv",'r','utf8')
    lineset = [line for line in f]
    currentRating={}
    users =[]
    temp = 0
    temp1=0

    for i in range(1,len(lineset)):
        line = lineset[i].split(',')
        book = line[1].strip('"')
        currentRatingB={}
        if temp != line[0]:
        	users.append(line[0])
        	temp = line[0]
 
        if users[temp1] == line[0]:
        	currentRating[book]=float(line[2].strip().strip('"'))
        	data[users[temp1].strip('"')] = currentRating
        else:
        	temp1 +=1
        	currentRating={}
        	currentRating[book]=float(line[2].strip().strip('"'))
        	data[users[temp1].strip('"')] = currentRating
    f.close()
    return data

data=loadData()

user1= input("Usuario a recomendar : ")
print(recomendar(user1,3,data))

