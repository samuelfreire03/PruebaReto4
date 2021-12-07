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
from DISClib.DataStructures import mapentry as me
from prettytable import PrettyTable
from DISClib.Algorithms.Graphs import prim as pr

sys.setrecursionlimit(20000)

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

def print_opciones(author):
    """
    Imprime la información del autor seleccionado
    """
    if author:
        print("\n")
        x = PrettyTable(["Opcion","Ciudad", "Pais",'Admin','Latitud','Longitud'])
        x._max_width = {"Opcion" : 20,"Ciudad" : 20, "Pais" : 20, "Admin" : 20,"Latitud" : 20,"Longitud" : 20}
        numero = 1
        for artistas in lt.iterator(me.getValue(author)['repetidas']):
            x.add_row([numero, artistas['city'],artistas['country'],artistas['admin_name'],artistas['lat'],artistas['lng']])
            numero += 1
        print(x)
        print("\n")
    else:
        print('No se encontro el autor.\n')

def print_ciudades_opciones(author):
    """
    Imprime la información del autor seleccionado
    """
    if author == '':
        print('No se encontraron artistas nacidos en el rango dado')
    elif author:
        print("\n")
        x = PrettyTable(["Nombre","Pais","Admin","Poblacion", 'Latitud','Longitud'])
        x._max_width = {"Nombre" : 20,"Pais" : 20,"Admin" : 20, "Poblacion" : 20,"Latitud" : 20, "Longitud" : 20}
        x.add_row([author['city']+'\n', author['country'],author['admin_name'],author['population'], author['lat'],author['lng']])
        print(x)
        print("\n")
    else:
        print('No se encontro el autor.\n')

def print_aaeropuertos_conectados(aeropuertos):
    """
    Imprime la información del autor seleccionado
    """
    if aeropuertos == '':
        print('No se encontraron artistas nacidos en el rango dado')
    elif aeropuertos:
        print("\n")
        x = PrettyTable(["Nombre", "Ciudad", 'Pais','AITA','Total','Inbound','Outbound'])
        x._max_width = {"Nombre" : 20, "Ciudad" : 20,"Pais" : 20, "AITA" : 20,"Total" : 20,"Inbound" : 20,"Outbound" : 20}
        for aeropuerto in lt.iterator(aeropuertos):
            valor = me.getValue(mp.get(cont['infoaeropuertos'],aeropuerto['aeropuerto']))
            x.add_row([valor['Name']+'\n', valor['City'], valor['Country'],valor['IATA'],aeropuerto['cantidadtotal'],aeropuerto['cantidadentrada'],aeropuerto['cantidadsalida']])
        print(x)
        print("\n")
    else:
        print('No se encontro el autor.\n')

def print_aeropuerto_LISTA(aeropuertos):
    """
    Imprime la información del autor seleccionado
    """
    if aeropuertos == '':
        print('No se encontraron artistas nacidos en el rango dado')
    elif aeropuertos:
        print("\n")
        x = PrettyTable(["IATA",'Nombre','Ciudad','Pais'])
        x._max_width = {"IATA" : 20, "Nombre" : 20,"Ciudad" : 20, "Pais" : 20}
        for aeropuerto in lt.iterator(aeropuertos):
            info_aeropuerto = me.getValue(mp.get(cont['infoaeropuertos'],aeropuerto))
            x.add_row([info_aeropuerto['IATA']+'\n', info_aeropuerto['Name'], info_aeropuerto['City'],info_aeropuerto['Country']])
        print(x)
        print("\n")
    else:
        print('No se encontro el autor.\n')

def print_camino(aeropuertos):
    """
    Imprime la información del autor seleccionado
    """
    if aeropuertos == '':
        print('No se encontraron artistas nacidos en el rango dado')
    elif aeropuertos:
        print("\n")
        x = PrettyTable(["Salida",'Llegada','Distancia'])
        x._max_width = {"Salida" : 20, "Llegada" : 20,"Distancia" : 20}
        for aeropuerto in lt.iterator(aeropuertos):
            x.add_row([aeropuerto['vertexA']+'\n', aeropuerto['vertexB'], aeropuerto['weight']])
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
    print("5- ----------------ADELANTO REQUERIMIENTO TRES---------")
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

    elif int(inputs[0]) == 2:

        controller.loadAirportsRutes(cont)
        print('\n' +('-'*20)+ 'Informacion grafo dirigido' +('-'*20)+ '\n')
        print('Numero de aeropuertos: ' + str(gr.numVertices(cont['rutas'])))
        print('Numero de rutas: ' + str(gr.numEdges(cont['rutas'])))
        print('\n' + 'Primer aeropuerto del grafo' + '\n')
        print_aeropuerto(controller.infoaeropuerto(cont,lt.firstElement(gr.vertices(cont['rutas']))))
        print('\n' + 'Ultimo aeropuerto del grafo' + '\n')
        print_aeropuerto(controller.infoaeropuerto(cont,lt.lastElement(gr.vertices(cont['rutas']))))

        print('\n' +('-'*20)+ 'Informacion grafo no dirigido' +('-'*20)+ '\n')
        print('Numero de aeropuertos: ' + str(gr.numVertices(cont['rutas_idayretorno'])))
        print('Numero de rutas: ' + str(gr.numEdges(cont['rutas_idayretorno'])))
        print('\n' + 'Primer aeropuerto del grafo' + '\n')
        print_aeropuerto(controller.infoaeropuerto(cont,lt.firstElement(gr.vertices(cont['rutas_idayretorno']))))
        print('\n' + 'Ultimo aeropuerto del grafo' + '\n')
        print_aeropuerto(controller.infoaeropuerto(cont,lt.lastElement(gr.vertices(cont['rutas_idayretorno']))))

        print('\n' +('-'*20)+ 'Informacion ciudades' +('-'*20)+ '\n')
        print('Total de ciudades: ' + str(lt.size(cont['ciudades'])))
        print('\n' + 'Primera ciudad cargada' + '\n')
        print_ciudades(lt.firstElement(cont['ciudades']))
        print('\n' + 'Ultima ciudad cargada' + '\n')
        print_ciudades(lt.lastElement(cont['ciudades']))

    elif int(inputs[0]) == 3:

        respuesta = controller.primer_req(cont)
        print('\n' + 'El numero de aeropuertos conectados es de:' + str(lt.size(respuesta[0])))
        print('aqui se ve a presentar la lista de areopuertos y el numero de aeropuertos conectados del grafo dirigido')
        print_aaeropuertos_conectados(respuesta[1])

        print('\n' + 'El numero de aeropuertos conectados es de:' + str(lt.size(respuesta[2])))
        print('aqui se ve a presentar la lista de areopuertos y el numero de aeropuertos conectados del grafo no dirigido')
        print_aaeropuertos_conectados(respuesta[3])

        print('\n' + 'El numero de aeropuertos conectados es de:' + str(lt.size(respuesta[4])))
        print('aqui se ve a presentar la lista de areopuertos y el numero de aeropuertos conectados en totalidad en ambos grafos')
        print_aaeropuertos_conectados(respuesta[5])

    elif int(inputs[0]) == 4:
        
        print('aqui se ve a presentar el cluster prsente en la red de aeropuertos y una comparacion')
        codigo1 = input('Escriba el codigo del primer aeropuerto')
        codigo2 = input('Escriba el codigo del segundo aeropuerto')
        respuesta = controller.segundo_req(cont,codigo1,codigo2)
        print('\n' + 'El numero de elementos fuertemente conectados es de:' + str(respuesta[0]))
        print('\n' + 'Los dos vertices pertenecen al mismo cluster:' + str(respuesta[1]))

    elif int(inputs[0]) == 5:
        
        print('aqui se ve a presentar lla ruta mas corta entre dos ciudades')
#ORIGEN -------------------------------------------------------------------------------------------------
        ciudad1 = input('Escriba el nombre de la ciudad de origen')
        opcion_origen = controller.opciones_ciudades(cont,ciudad1)
        print_opciones(opcion_origen)
        ciudad_origen = input('Escriba la opcion de la tabla de arriba que desea buscar')
        info_ciudad_origen = lt.getElement(me.getValue(opcion_origen)['repetidas'],int(ciudad_origen))
        print_ciudades_opciones(info_ciudad_origen)
        aeropuerto1 = controller.aeropuertoopciones(cont,info_ciudad_origen)
        print('\n' + 'El aeropuerto de salida seleccionado es:' + str(aeropuerto1['aeropuerto']))

#DESTINO-------------------------------------------------------------------------------------------------
        ciudad2 = input('Escriba el nombre de la ciudad de destino')
        opcion_destino = controller.opciones_ciudades(cont,ciudad2)
        print_opciones(opcion_destino)
        ciudad_destino = input('Escriba la opcion de la tabla de arriba que desea buscar')
        info_ciudad_destino = lt.getElement(me.getValue(opcion_destino)['repetidas'],int(ciudad_destino))
        print_ciudades_opciones(info_ciudad_destino)
        aeropuerto2 = controller.aeropuertoopciones(cont,info_ciudad_destino)
        print('\n' + 'El aeropuerto de destino seleccionado es:' + str(aeropuerto2['aeropuerto']))

    elif int(inputs[0]) == 6:
        
        print('aqui se ve a presentar la red expansion minima')
        ciudad1 = input('Escriba el nombre de la ciudad de origen')
        opcion_origen = controller.opciones_ciudades(cont,ciudad1)
        print_opciones(opcion_origen)
        ciudad_origen = input('Escriba la opcion de la tabla de arriba que desea buscar')
        info_ciudad_origen = lt.getElement(me.getValue(opcion_origen)['repetidas'],int(ciudad_origen))
        print_ciudades_opciones(info_ciudad_origen)
        aeropuerto1 = controller.aeropuertoopciones(cont,info_ciudad_origen)
        millas = input('Escriba la cantidad de millas qeu tiene')
        respuesta = controller.cuarto_req(cont,aeropuerto1['aeropuerto'],millas)
        print('\n' + 'El numero de nodos conectados es:' + str(respuesta[0]))
        print('\n' + 'El costo total de la red de expansion es de:' + str(respuesta[1]))
        print_camino(respuesta[2])
        print('\n' + respuesta[3] + 'millas para la ruta mas larga')

    elif int(inputs[0]) == 7:
        
        codigo1 = input('Escriba el codigo del primer aeropuerto')
        respuesta = controller.quinto_req(cont,codigo1)
        print('\n' + 'El numero de rutas restantes es de (en el digrafo):' + str(respuesta[0]))
        print('\n' + 'El numero de rutas restantes es de (en el grafo no dirigido):' + str(respuesta[1]))

        print('\n' + 'El numero de aeropuertos afectados en totalidad:' + str(respuesta[8]))
        print('\n' + 'La lista de los primeros 3 aeropuertos son los siguientes:')
        print_aeropuerto_LISTA(respuesta[9])
        print('\n' + 'La lista de los ultimos 3 aeropuertos son los siguientes:')
        print_aeropuerto_LISTA(respuesta[10])

        print('\n' + 'El numero de aeropuertos afectados en el grafo no dirigido:' + str(respuesta[2]))
        print('\n' + 'La lista de los primeros 3 aeropuertos son los siguientes:')
        print_aeropuerto_LISTA(respuesta[3])
        print('\n' + 'La lista de los ultimos 3 aeropuertos son los siguientes:')
        print_aeropuerto_LISTA(respuesta[4])

        print('\n' + 'El numero de aeropuertos afectados en el grafo dirigido:' + str(respuesta[5]))
        print('\n' + 'La lista de los primeros 3 aeropuertos son los siguientes:')
        print_aeropuerto_LISTA(respuesta[6])
        print('\n' + 'La lista de los ultimos 3 aeropuertos son los siguientes:')
        print_aeropuerto_LISTA(respuesta[7])

    else:
        sys.exit(0)
sys.exit(0)
