"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf
from DISClib.ADT.graph import gr
from DISClib.ADT import map as mp
from prettytable import PrettyTable

def print_aeropuerto(author):
    """
    Imprime la información del autor seleccionado
    """
    if author == '':
        print('No se encontraron artistas nacidos en el rango dado')
    elif author:
        print("\n")
        x = PrettyTable(["Nombre", "Ciudad", 'Pais','Latitud','Longitud'])
        x._max_width = {"Nombre" : 20, "Ciudad" : 20,"Pais" : 20, "Latitud" : 20,"Longitud" : 20}
        x.add_row([author['Name']+'\n', author['City'], author['Country'],author['Latitude'],author['Longitude']])
        print(x)
        print("\n")
    else:
        print('No se encontro el autor.\n')

def print_ciudades(author):
    """
    Imprime la información del autor seleccionado
    """
    if author == '':
        print('No se encontraron artistas nacidos en el rango dado')
    elif author:
        print("\n")
        x = PrettyTable(["Nombre", "Poblacion", 'Latitud','Longitud'])
        x._max_width = {"Nombre" : 20, "Poblacion" : 20,"Latitud" : 20, "Longitud" : 20}
        x.add_row([author['city']+'\n', author['population'], author['lat'],author['lng']])
        print(x)
        print("\n")
    else:
        print('No se encontro el autor.\n')


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de archivos de vuelos")
    print("3- Encontrar puntos de interconexión aérea")
    print("4- Encontrar clústeres de tráfico aéreo")
    print("5- Encontrar la ruta más corta entre ciudades")
    print("6- Utilizar las millas de viajero")
    print("7- Cuantificar el efecto de un aeropuerto cerrado")
    print("0- Salir")
    print("*******************************************")

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:

        print("Cargando información de los archivos ....")
        cont = controller.init()
        controller.loadAirportsRutes(cont)

    elif int(inputs[0]) == 2:

        print('\n' + 'Informacion grafo dirigido' + '\n')
        print('Numero de aeropuertos: ' + str(gr.numVertices(cont['rutas'])))
        print('Numero de rutas: ' + str(gr.numEdges(cont['rutas'])))
        print_aeropuerto(controller.infoaeropuerto(cont,lt.firstElement(gr.vertices(cont['rutas']))))

        print('\n' + 'Informacion grafo no dirigido' + '\n')
        print('Numero de aeropuertos: ' + str(gr.numVertices(cont['rutas_idayretorno'])))
        print('Numero de rutas: ' + str(gr.numEdges(cont['rutas_idayretorno'])))
        print_aeropuerto(controller.infoaeropuerto(cont,lt.firstElement(gr.vertices(cont['rutas_idayretorno']))))

        print('\n' + 'Informacion ciudades' + '\n')
        print('Total de ciudades: ' + str(lt.size(cont['ciudades'])))
        print_ciudades(lt.lastElement(cont['ciudades']))

    elif int(inputs[0]) == 3:
        
        print('aqui se ve a presentar la lista de areopuertos y el numero de aeropuertos conectados')

    elif int(inputs[0]) == 4:
        
        print('aqui se ve a presentar el cluster prsente en la red de aeropuertos y una comparacion')

    elif int(inputs[0]) == 5:
        
        print('aqui se ve a presentar lla ruta mas corta entre dos ciudades')

    elif int(inputs[0]) == 6:
        
        print('aqui se ve a presentar la red expansion minima')

    elif int(inputs[0]) == 7:
        
        print('aqui se ve a presentar la afectacion de un vuelo')

    else:
        sys.exit(0)
sys.exit(0)
