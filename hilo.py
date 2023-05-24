import pandas as pd
import threading

class Nodo:
    def __init__(self, clave, datos):
        self.clave = clave
        self.datos = datos
        self.siguiente = None

class TablaHash:
    def __init__(self, tamaño):
        self.tamaño = tamaño
        self.tabla = [None] * tamaño

    def _obtener_indice(self, clave):
        indice = hash(clave) % self.tamaño
        return indice

    def insertar(self, clave, datos):
        indice = self._obtener_indice(clave)
        nodo_actual = self.tabla[indice]

        while nodo_actual is not None:
            if nodo_actual.clave == clave:
                nodo_actual.datos.append(datos)
                return
            nodo_actual = nodo_actual.siguiente

        nuevo_nodo = Nodo(clave, [datos])
        nuevo_nodo.siguiente = self.tabla[indice]
        self.tabla[indice] = nuevo_nodo

    def obtener(self, clave):
        indice = self._obtener_indice(clave)
        nodo_actual = self.tabla[indice]

        while nodo_actual is not None:
            if nodo_actual.clave == clave:
                return nodo_actual.datos
            nodo_actual = nodo_actual.siguiente

        raise KeyError("Clave no encontrada en la tabla hash")

    def mostrar(self):
        for i in range(self.tamaño):
            nodo_actual = self.tabla[i]
            while nodo_actual is not None:
                print(f"Clave: {nodo_actual.clave}, Datos: {nodo_actual.datos}")
                nodo_actual = nodo_actual.siguiente

tabla = TablaHash(139000)

class MiHilo(threading.Thread):
    def __init__(self,inicio, tamano,user,movie,rating):
        super().__init__()
        self.inicio = inicio
        self.tamano = tamano
        self.user = user
        self.movie = movie
        self.rating = rating

    def run(self):
        for i in range(self.inicio,self.tamano):
            tabla.insertar(self.user[i],(self.movie[i],self.rating[i]))

def leerDatos():
    nombre_archivo = "20m.csv"
    dataframe = pd.read_csv(nombre_archivo)

    user = dataframe['userId']
    movie = dataframe['movieId']
    rating = dataframe['rating']

    # Crear instancias de la clase MiHilo
    hilo1 = MiHilo(0 ,35000,user,movie,rating)
    hilo2 = MiHilo(350000,70000,user,movie,rating)
    hilo3 = MiHilo(70001,105000,user,movie,rating)
    hilo4 = MiHilo(105000,len(dataframe),user,movie,rating)  

    # Iniciar los hilos
    hilo1.start()
    hilo2.start()
    hilo3.start()
    hilo4.start()

    # Esperar a que los hilos finalicen
    hilo1.join()
    hilo2.join()
    hilo3.join()
    hilo4.join()

leerDatos()
tabla.mostrar()
