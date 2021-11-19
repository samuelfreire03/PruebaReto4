"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
assert config

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newAnalyzer():
    """ Inicializa el analizador

   stops: Tabla de hash para guardar los vertices del grafo
   connections: Grafo para representar las rutas entre estaciones
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """
    analyzer = {
                    'rutas': None,
                    'rutas_idayretorno': None
                }

    analyzer['rutas'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=9100,
                                              comparefunction=compareStopIds)

    analyzer['rutas_idayretorno'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=9100,
                                              comparefunction=compareStopIds)

    return analyzer

# Funciones para agregar informacion al catalogo

def addVerticeGrafo(analyzer, aeropuerto):

    addStop(analyzer, aeropuerto['IATA'])

def addStop(analyzer, aeropuerto_identificador):

    if not gr.containsVertex(analyzer['rutas'], aeropuerto_identificador):
        gr.insertVertex(analyzer['rutas'], aeropuerto_identificador)

def addStopidayvuelta(analyzer, aeropuerto_identificador):

    if not gr.containsVertex(analyzer['rutas_idayretorno'], aeropuerto_identificador):
        gr.insertVertex(analyzer['rutas_idayretorno'], aeropuerto_identificador)

def addRuta(analyzer, aeropuerto_identificador):

    gr.addEdge(analyzer['rutas'],aeropuerto_identificador['Departure'],aeropuerto_identificador['Destination'],float(aeropuerto_identificador['distance_km']))

def addRutaidayvuleta(analyzer):

    arcos_total = gr.edges(analyzer['rutas'])
    for arco1 in lt.iterator(arcos_total):
        for arco2 in lt.iterator(arcos_total):
            primera_comparacion = arco1['vertexA'] == arco2['vertexB']
            segunda_comparacion = arco1['vertexB'] == arco2['vertexA']
            if primera_comparacion and segunda_comparacion:
                addStopidayvuelta(analyzer,arco1['vertexA'])
                addStopidayvuelta(analyzer,arco1['vertexB'])
                gr.addEdge(analyzer['rutas_idayretorno'],arco1['vertexA'],arco1['vertexB'],arco1['weight'])

# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

def compareStopIds(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1

# Funciones de ordenamiento
