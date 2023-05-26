import codecs
import math

users = {"Angelica": {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0},
         "Bill":{"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0},
         "Chan": {"Blues Traveler": 5.0, "Broken Bells": 1.0, "Deadmau5": 1.0, "Norah Jones": 3.0, "Phoenix": 5, "Slightly Stoopid": 1.0},
         "Dan": {"Blues Traveler": 3.0, "Broken Bells": 4.0, "Deadmau5": 4.5, "Phoenix": 3.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 2.0},
         "Hailey": {"Broken Bells": 4.0, "Deadmau5": 1.0, "Norah Jones": 4.0, "The Strokes": 4.0, "Vampire Weekend": 1.0},
         "Jordyn":  {"Broken Bells": 4.5, "Deadmau5": 4.0, "Norah Jones": 5.0, "Phoenix": 5.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 4.0},
         "Sam": {"Blues Traveler": 5.0, "Broken Bells": 2.0, "Norah Jones": 3.0, "Phoenix": 5.0, "Slightly Stoopid": 4.0, "The Strokes": 5.0},
         "Veronica": {"Blues Traveler": 3.0, "Norah Jones": 5.0, "Phoenix": 4.0, "Slightly Stoopid": 2.5, "The Strokes": 3.0}
        }

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
				#print(user1 , key, currentRating[key])
	sorted_desserts = dict(sorted(currentRating.items(), key=lambda item:item[1],reverse=reverse))
	currentRating={}
	#print(sorted_desserts)
	for key,valor in sorted_desserts.items():
		if aux == umbral :
			break
		else:
			currentRating[key]=valor
			#print(key,valor)
			aux +=1
	return currentRating

"""def busqueda(funcion,user1):
	temp2 = 101
	nombre = ''
	for key in data:
	    if key!=user1:
	    	temp1=funcion(data[user1],data[key])
	    	#temp1=funcion(users[user1],users[key])
	    	if temp1<temp2:
		        temp2=temp1
		        nombre=key
	return(nombre,temp2)"""

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
	f=codecs.open(path+"p.csv","a")
	usuarioAtributos = input()
	f.write(usuarioAtributos+'\n')
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
				#print("sorted_desserts" , sorted_desserts)
				for key in sorted_desserts:
						recomendar.append(key)		
						aux +=1
						if aux == numRec:
							break
	return recomendar

def loadDatabase(path=''):
    dataCsv={}

    f=codecs.open(path+"Movie_Ratings.csv",'r','utf8')

    lineset = [line for line in f]
    users = lineset[0].split(',')

    for i in range(len(users)):
        users[i]=users[i].strip('\n').strip('"')

    for i in range(1,len(lineset)):
        fields = lineset[i].split(',')
        book = fields[0].strip('"')
        currentRatingB={}

        for j in range(1,len(fields)):
            if users[j].strip('"') in dataCsv:
                currentRating=dataCsv[users[j].strip('"')]
            else:
                currentRating={}
            if fields[j].strip().strip('"'):
                currentRating[book]=float(fields[j].strip().strip('"'))
                dataCsv[users[j].strip('"')] = currentRating
    f.close()
    return dataCsv

#dataCsv=loadDatabase()

def loadData(path=''):
    data={}
    f=codecs.open(path+"10Mratings.dat",'r','utf8')
    #f=codecs.open(path+"20Mratings.csv",'r','utf8')
    lineset = [line for line in f]
    currentRating={}
    users =[]
    temp = 0
    temp1=0

    for i in range(0,len(lineset)):
        line = lineset[i].split('::')
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

#print(euclidean(dataDat['1'],dataDat['3']))
#print(manhattan(dataDat['1'],dataDat['3']))
#print(pearson(dataDat['1'],dataDat['3']))
#print(k_nn(pearson,'5',False,data))
#print(pearson(dataDat['35000'],dataDat['3011']))

#print(agregarUsuario())

#50,671,0.5,1230782626
#11,673,5.0,1230787775
#4,2574,3.0,944897877
#4,2,3.5,1112486027

#print(k_nn(pearson,'69000',True,data))
#print(recomendar('Bill',3,users))
#print(recomendar('Matt',3,dataCsv))
user1= input("Usuario a recomendar : ")
print(recomendar(user1,3,data))
user1= input("Usuario a recomendar : ")
print(recomendar(user1,3,data))

