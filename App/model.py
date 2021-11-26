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
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.Algorithms.Graphs import scc
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import prim as pr
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
                    'rutas_idayretorno': None,
                    'infoaeropuertos': None,
                    'componentes_grafo_dirigdo': None,
                    'rutasconaerolineas': None
                }

    analyzer['rutas'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=9100,
                                              comparefunction=compareStopIds)

    analyzer['rutas_idayretorno'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=9100,
                                              comparefunction=compareStopIds)
    
    analyzer["infoaeropuertos"] = mp.newMap(9100,
                                   maptype='CHAINING',
                                   loadfactor=4.0)
    
    analyzer['ciudades'] = lt.newList('ARRAY_LIST',compareCiudades)

    analyzer['rutasconaerolineas'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=9100,
                                              comparefunction=compareStopIds)

    analyzer['aeropuertosinfolista'] = lt.newList('ARRAY_LIST',compareCiudades)

    return analyzer

# Funciones para agregar informacion al catalogo

def addVerticeGrafo(analyzer, aeropuerto):

    addStop(analyzer, aeropuerto['IATA'])
    mp.put(analyzer["infoaeropuertos"], aeropuerto['IATA'], aeropuerto)
    lt.addLast(analyzer['aeropuertosinfolista'], aeropuerto)

def addStop(analyzer, aeropuerto_identificador):

    if not gr.containsVertex(analyzer['rutas'], aeropuerto_identificador):
        gr.insertVertex(analyzer['rutas'], aeropuerto_identificador)

    if not gr.containsVertex(analyzer['rutasconaerolineas'], aeropuerto_identificador):
        gr.insertVertex(analyzer['rutasconaerolineas'], aeropuerto_identificador)

def addStopidayvuelta(analyzer, aeropuerto_identificador):

    if not gr.containsVertex(analyzer['rutas_idayretorno'], aeropuerto_identificador):
        gr.insertVertex(analyzer['rutas_idayretorno'], aeropuerto_identificador)

def addRuta(analyzer, aeropuerto_identificador):
    
    gr.addEdge(analyzer['rutas'],aeropuerto_identificador['Departure'],aeropuerto_identificador['Destination'],float(aeropuerto_identificador['distance_km']))
    existe_arco_ida = gr.getEdge(analyzer['rutasconaerolineas'],aeropuerto_identificador['Departure'],aeropuerto_identificador['Destination'])
    existe_arco_vuelta = gr.getEdge(analyzer['rutasconaerolineas'],aeropuerto_identificador['Destination'],aeropuerto_identificador['Departure'])
    if existe_arco_ida is None and existe_arco_vuelta is None:
        gr.addEdge(analyzer['rutasconaerolineas'],aeropuerto_identificador['Departure'],aeropuerto_identificador['Destination'],float(aeropuerto_identificador['distance_km']))


def addRutaidayvuleta(analyzer):

    vertices_total = gr.vertices(analyzer['rutas'])
    for vertices in lt.iterator(vertices_total):
        lista_adjacentes = gr.adjacents(analyzer['rutas'],vertices)
        for vertice in lt.iterator(lista_adjacentes):
            lista_arcos = gr.adjacentEdges(analyzer['rutas'],vertice)
            for arco in lt.iterator(lista_arcos):
                if arco['vertexB'] == vertices:
                    addStopidayvuelta(analyzer,arco['vertexA'])
                    addStopidayvuelta(analyzer,arco['vertexB'])
                    existe_arco = gr.getEdge(analyzer['rutas_idayretorno'],arco['vertexA'],arco['vertexB'])
                    if existe_arco is None:
                        gr.addEdge(analyzer['rutas_idayretorno'],arco['vertexA'],arco['vertexB'],float(arco['weight']))

def addCiudad(analyzer,ciudad):

    lt.addLast(analyzer['ciudades'], ciudad)

# Funciones para creacion de datos

# Funciones de consulta

def infoaeropuerto(analyzer,codigoAita):

    llave_valor = mp.get(analyzer['infoaeropuertos'],codigoAita)
    informacion = me.getValue(llave_valor)
    return informacion

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

def compareCiudades(id1, id2):
    """
    Compara dos ids de dos libros
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1

# Funciones de ordenamiento

#Funciones de requerimientos

def primer_req(analyzer):

#GRAFO DIRIGIDO
    vertices_total = gr.vertices(analyzer['rutasconaerolineas'])
    mayor_numero1 = 0
    mayor_aeropuerto1 = None
    for vertice in lt.iterator(vertices_total):
        entran = gr.indegree(analyzer['rutasconaerolineas'],vertice)
        salen = gr.outdegree(analyzer['rutasconaerolineas'],vertice)
        total_rutas = entran + salen
        if float(total_rutas) > mayor_numero1:
            mayor_numero1 = float(total_rutas)
            mayor_aeropuerto1 = vertice
    llave_valor_vertice = mp.get(analyzer['rutasconaerolineas']['vertices'], mayor_aeropuerto1)
    lst1 = me.getValue(llave_valor_vertice)
    info_mayor1 = me.getValue(mp.get(analyzer['infoaeropuertos'],mayor_aeropuerto1))

#GRAFO NO DIRIGIDO
    vertices_total_no = gr.vertices(analyzer['rutas_idayretorno'])
    mayor_numero2 = 0
    mayor_aeropuerto2 = None
    for vertice_no in lt.iterator(vertices_total_no):
        total_rutas1 = gr.degree(analyzer['rutas_idayretorno'],vertice_no)
        if float(total_rutas1) > mayor_numero2:
            mayor_numero2 = float(total_rutas1)
            mayor_aeropuerto2 = vertice_no
    llave_valor_vertice1 = mp.get(analyzer['rutas_idayretorno']['vertices'], mayor_aeropuerto2)
    lst2 = me.getValue(llave_valor_vertice1)
    info_mayor2 = me.getValue(mp.get(analyzer['infoaeropuertos'],mayor_aeropuerto2))
    return mayor_numero1,info_mayor1,mayor_numero2,info_mayor2

def segundo_req(analyzer,codigo1,codigo2):

    analyzer['componentes_grafo_dirigdo'] = scc.KosarajuSCC(analyzer['rutas'])
    numero_componentes = scc.connectedComponents(analyzer['componentes_grafo_dirigdo'])
    conectados = scc.stronglyConnected(analyzer['componentes_grafo_dirigdo'],codigo1,codigo2)
    return numero_componentes,conectados

def cuarto_req(analyzer,codigo1,millas):

#Respuesta maxima para recorrer
    kilometros = float(millas) * 1.60
    caminos = djk.Dijkstra(analyzer['rutas'], codigo1)
    nodos = mp.size(caminos['visited'])
    vertices_mapa = mp.keySet(caminos['visited'])
    respuesta = None
    mayor = 0
    total = 0
    mayor_lista = 0
    for c in lt.iterator(caminos['iminpq']['elements']):
        total += float(c['index'])
        if djk.hasPathTo(caminos, c['key']) is True:
            camino_revisar = djk.pathTo(caminos, c['key'])
            cantidad = lt.size(camino_revisar)
            if float(c['index']) > mayor and kilometros > float(c['index']) and cantidad > mayor_lista:
                mayor = float(c['index']) 
                respuesta = c['key']
                mayor_lista = cantidad

#camino mas largo
    camino = djk.pathTo(caminos, respuesta)
    mayor_distacnia = 0
    lista = None
    for j in lt.iterator(vertices_mapa):
        if djk.hasPathTo(caminos, j) is True:
            camino_revisar = djk.pathTo(caminos, j)
            cantidad = lt.size(camino_revisar)
            if cantidad > mayor_distacnia:
                mayor_distacnia =  cantidad
                lista = camino_revisar

#informacion de ciudades

    ciudades = lt.newList('ARRAY_LIST')
    for aeropuerto in lt.iterator(camino):
        informacion = me.getValue(mp.get(analyzer['infoaeropuertos'],aeropuerto['vertexB']))
        ciudad = informacion['City']
        lt.addLast(ciudades,ciudad)

    return nodos,total,lista,ciudades

def quinto_req(analyzer,codigo1):

    entran = gr.indegree(analyzer['rutasconaerolineas'],codigo1)
    salen = gr.outdegree(analyzer['rutasconaerolineas'],codigo1)
    total_rutas = entran + salen

    arcos_totales = gr.edges(analyzer['rutasconaerolineas'])

    lista_aeropuetos = lt.newList('ARRAY_LIST')
    for c in lt.iterator(arcos_totales):
        if c['vertexA'] == codigo1:
            lt.addLast(lista_aeropuetos,c['vertexB'])
        if c['vertexB'] == codigo1:
            lt.addLast(lista_aeropuetos,c['vertexA']) 

    return total_rutas,lista_aeropuetos