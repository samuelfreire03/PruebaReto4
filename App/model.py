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
from DISClib.Algorithms.Sorting import mergesort as merge
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import prim as pr
from DISClib.Utils import error as error
assert config
import math

def haversine(lat1, lon1, lat2, lon2):
    rad=math.pi/180
    dlat=lat2-lat1
    dlon=lon2-lon1
    R=6372.795477598
    a=(math.sin(rad*dlat/2))**2 + math.cos(rad*lat1)*math.cos(rad*lat2)*(math.sin(rad*dlon/2))**2
    distancia=2*R*math.asin(math.sqrt(a))
    return distancia

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

    analyzer["infociudadesrepetidas"] = mp.newMap(9100,
                                   maptype='CHAINING',
                                   loadfactor=4.0)

    analyzer["aeropuertosenciudades"] = mp.newMap(9100,
                                   maptype='CHAINING',
                                   loadfactor=4.0)

    return analyzer

# Funciones para agregar informacion al catalogo

def addVerticeGrafo(analyzer, aeropuerto):

    addStop(analyzer, aeropuerto['IATA'])
    addStopidayvuelta(analyzer,aeropuerto['IATA'])
    mp.put(analyzer["infoaeropuertos"], aeropuerto['IATA'], aeropuerto)
    lt.addLast(analyzer['aeropuertosinfolista'], aeropuerto)
    addaeropuertoenciudad(analyzer,aeropuerto['City'],aeropuerto)

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
                    existe_arco = gr.getEdge(analyzer['rutas_idayretorno'],arco['vertexA'],arco['vertexB'])
                    if existe_arco is None:
                        gr.addEdge(analyzer['rutas_idayretorno'],arco['vertexA'],arco['vertexB'],float(arco['weight']))

def addCiudad(analyzer, ciudad):

    lt.addLast(analyzer['ciudades'], ciudad)
    addCiudadRepetida(analyzer, ciudad['city'].strip(), ciudad)

def addCiudadRepetida(analyzer, ciudad_nombre, ciudad):
    """
    Esta función adiciona un libro a la lista de libros publicados
    por un autor.
    Cuando se adiciona el libro se actualiza el promedio de dicho autor
    """
    authors = analyzer['infociudadesrepetidas']
    existauthor = mp.contains(authors, ciudad_nombre)
    if existauthor:
        entry = mp.get(authors, ciudad_nombre)
        author = me.getValue(entry)
    else:
        author = newciudad(ciudad_nombre)
        mp.put(authors, ciudad_nombre, author)
    lt.addLast(author['repetidas'], ciudad)

def addaeropuertoenciudad(analyzer, aeropuerto_nombre, aeropuerto):
    """
    Esta función adiciona un libro a la lista de libros publicados
    por un autor.
    Cuando se adiciona el libro se actualiza el promedio de dicho autor
    """
    authors = analyzer['aeropuertosenciudades']
    existauthor = mp.contains(authors, aeropuerto_nombre)
    if existauthor:
        entry = mp.get(authors, aeropuerto_nombre)
        author = me.getValue(entry)
    else:
        author = newciudad(aeropuerto_nombre)
        mp.put(authors, aeropuerto_nombre, author)
    lt.addLast(author['repetidas'], aeropuerto)

# Funciones para creacion de datos

def newciudad(pubyear):
    """
    Esta funcion crea la estructura de libros asociados
    a un año.
    """
    entry = {'Ciudad': "", "repetidas": None}
    entry['Ciudad'] = pubyear
    entry['repetidas'] = lt.newList('ARRAY_LIST', compareYears)
    return entry

def newaeropuerto(pubyear,distancia):
    """
    Esta funcion crea la estructura de libros asociados
    a un año.
    """
    entry = {'aeropuerto': "", "distancias": ''}
    entry['aeropuerto'] = pubyear
    entry['distancias'] = distancia
    return entry

def newcantidad(aeropuerto,total,entrada,salida):
    """
    Esta funcion crea la estructura de libros asociados
    a un año.
    """
    entry = {'aeropuerto': "", "distancias": ''}
    entry['aeropuerto'] = aeropuerto
    entry['cantidadtotal'] = total
    entry['cantidadentrada'] = entrada
    entry['cantidadsalida'] = salida
    return entry

# Funciones de consulta

def infoaeropuerto(analyzer,codigoAita):

    llave_valor = mp.get(analyzer['infoaeropuertos'],codigoAita)
    informacion = me.getValue(llave_valor)
    return informacion

def opciones_ciudades(analyzer,ciudad):

    lista_opciones_origen = mp.get(analyzer['infociudadesrepetidas'],ciudad)

    return lista_opciones_origen

def aeropuertoopciones(analyzer,ciudad):

    longitud = float(ciudad['lng'])
    latitud = float(ciudad['lat'])
    lista_distancias = lt.newList('ARRAY_LIST')
    llave_valor = mp.get(analyzer['aeropuertosenciudades'],ciudad['city'])
    lista_aeropuertos = me.getValue(llave_valor)['repetidas']
    for c in lt.iterator(lista_aeropuertos):
        lat_aeropuerto = float(c['Latitude'])
        long_aeropuerto = float(c['Longitude'])
        distancia = haversine(latitud,longitud,lat_aeropuerto,long_aeropuerto)
        aeropuerto_dist = newaeropuerto(c['IATA'],distancia)
        lt.addLast(lista_distancias,aeropuerto_dist)
    orden = sortcomparedistancias(lista_distancias)
    aeropuerto_cercano = lt.firstElement(orden)
    return aeropuerto_cercano

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

def compareYears(year1, year2):
    if (int(year1) == int(year2)):
        return 0
    elif (int(year1) > int(year2)):
        return 1
    else:
        return 0

def comparedistancias(ciudad1, ciudad2):
    fecha1 = ciudad1['distancias']
    fecha2 = ciudad2['distancias']
    return float(fecha1) < float(fecha2)

def comparecantidad(ciudad1, ciudad2):
    fecha1 = ciudad1['cantidadtotal']
    fecha2 = ciudad2['cantidadtotal']
    return float(fecha1) > float(fecha2)

# Funciones de ordenamiento

def sortcomparedistancias(catalog):

    sorted_list = merge.sort(catalog, comparedistancias)
    return sorted_list

def sortcomparecanitdades(catalog):

    sorted_list = merge.sort(catalog, comparecantidad)
    return sorted_list

#Funciones de requerimientos

def primer_req(analyzer):

#GRAFO DIRIGIDO
    vertices_total = gr.vertices(analyzer['rutas'])
    lista_final = lt.newList('ARRAY_LIST')
    lista_canitdad_digrafo = lt.newList('ARRAY_LIST')
    for vertice in lt.iterator(vertices_total):
        entran = gr.indegree(analyzer['rutas'],vertice)
        salen = gr.outdegree(analyzer['rutas'],vertice)
        total_rutas = entran + salen
        cantidad = newcantidad(vertice,total_rutas,entran,salen)
        lt.addLast(lista_canitdad_digrafo,cantidad)
        lt.addLast(lista_final,cantidad)
    orden = sortcomparecanitdades(lista_canitdad_digrafo)
    primeros5 = lt.subList(orden,1,5)
    conectados_numero_interno = lt.newList('ARRAY_LIST')
    for c in lt.iterator(orden):
        if c['cantidadtotal'] != 0:
            lt.addLast(conectados_numero_interno,c)

#GRAFO NO DIRIGIDO
    vertices_total_no = gr.vertices(analyzer['rutas_idayretorno'])
    lista_canitdad_grafo = lt.newList('ARRAY_LIST')
    for vertice_no in lt.iterator(vertices_total_no):
        entran = gr.degree(analyzer['rutas_idayretorno'],vertice_no)
        salen = gr.degree(analyzer['rutas_idayretorno'],vertice_no)
        total_rutas = entran + salen
        cantidad = newcantidad(vertice_no,total_rutas,entran,salen)
        lt.addLast(lista_canitdad_grafo,cantidad)
        lt.addLast(lista_final,cantidad)
    orden_no = sortcomparecanitdades(lista_canitdad_grafo)
    primeros5_no = lt.subList(orden_no,1,5)
    conectados_numero_interno_no = lt.newList('ARRAY_LIST')
    for c in lt.iterator(orden_no):
        if c['cantidadtotal'] != 0:
            lt.addLast(conectados_numero_interno_no,c)

#Orden total

    orden_final = sortcomparecanitdades(lista_final)
    primeros5_final = lt.subList(orden_final,1,5)
    conectados_numero_interno_final = lt.newList('ARRAY_LIST')
    for c in lt.iterator(orden_final):
        if c['cantidadtotal'] != 0:
            lt.addLast(conectados_numero_interno_final,c)

    return conectados_numero_interno,primeros5,conectados_numero_interno_no,primeros5_no,conectados_numero_interno_final,primeros5_final

def segundo_req(analyzer,codigo1,codigo2):

    analyzer['componentes_grafo_dirigdo'] = scc.KosarajuSCC(analyzer['rutas'])
    numero_componentes = scc.connectedComponents(analyzer['componentes_grafo_dirigdo'])
    conectados = scc.stronglyConnected(analyzer['componentes_grafo_dirigdo'],codigo1,codigo2)
    return numero_componentes,conectados

def cuarto_req(analyzer,codigo1,millas):

    kilometros = float(millas) * 1.60

#Respuesta maxima para recorrer

    search = pr.PrimMST(analyzer['rutas_idayretorno'])
    edge = pr.edgesMST(analyzer['rutas_idayretorno'], search)
    nodos_red_expansion = lt.size(edge['mst'])

    suma = 0
    for c in lt.iterator(mp.valueSet(edge['distTo'])):
        suma += c

#camino mas largo

    caminos = djk.Dijkstra(analyzer['rutas_idayretorno'], codigo1)
    vertices_mapa = mp.keySet(caminos['visited'])
    mayor_distacnia = 0
    lista = None
    for j in lt.iterator(vertices_mapa):
        if djk.hasPathTo(caminos, j) is True:
            camino_revisar = djk.pathTo(caminos, j)
            cantidad = lt.size(camino_revisar)
            if cantidad > mayor_distacnia:
                mayor_distacnia = cantidad
                lista = camino_revisar
#FALTANTE O RESTANTE

    costo_total = 0
    for arcos in lt.iterator(lista):
        costo_total += arcos['weight']

    if kilometros > float(costo_total):
        resta = (kilometros - float(costo_total))/1.6
        respuesta = 'sobran ' + str(resta) + ' '

    if float(costo_total) > kilometros:
        resta = (float(costo_total) - kilometros)/1.6
        respuesta = 'faltan ' + str(resta) + ' '

    return nodos_red_expansion,round(suma,2),lista,respuesta

def quinto_req(analyzer,codigo):


    lista_total = lt.newList('ARRAY_LIST')
#Grafo no dirigido

    numero_afectados_nodiri = lt.size(gr.adjacents(analyzer['rutas_idayretorno'],codigo))
    afectados_nodiri = gr.adjacents(analyzer['rutas_idayretorno'],codigo)

    for c in lt.iterator(afectados_nodiri):
        lt.addLast(lista_total,c)

#Grafo dirigido

    entran = gr.indegree(analyzer['rutas'],codigo)
    salen = gr.outdegree(analyzer['rutas'],codigo)
    total_afectados_diri = entran + salen
    afectados_diri = lt.newList('ARRAY_LIST')
    arcos_total = gr.edges(analyzer['rutas'])
    for c in lt.iterator(arcos_total):
        if c['vertexA'] == codigo:
            existe = lt.isPresent(afectados_diri,c['vertexB'])
            if existe == 0:
                lt.addLast(afectados_diri,c['vertexB'])
                lt.addLast(lista_total,c['vertexB'])
        if c['vertexB'] == codigo:
            existe = lt.isPresent(afectados_diri,c['vertexA'])
            if existe == 0:
                lt.addLast(afectados_diri,c['vertexA'])
                lt.addLast(lista_total,c['vertexA'])
    numero_afectados_diri = lt.size(afectados_diri)

#restantes
    restantes_digrafo = gr.numEdges(analyzer['rutas'])-total_afectados_diri
    restantes_grafo = gr.numEdges(analyzer['rutas_idayretorno'])-numero_afectados_nodiri

#impresion no dirigido
    if lt.size(afectados_nodiri) >= 6:
        primeros_nodiri = lt.subList(afectados_nodiri,1,3)
        ultimos_nodiri = lt.subList(afectados_nodiri,lt.size(afectados_nodiri)-2,3)
    else: 
        primeros_nodiri = afectados_nodiri
        ultimos_nodiri = afectados_nodiri

#impresion dirigido
    if lt.size(afectados_diri) >= 6:
        primeros_diri = lt.subList(afectados_diri,1,3)
        ultimos_diri = lt.subList(afectados_diri,lt.size(afectados_diri)-2,3)
    else: 
        primeros_diri = afectados_diri
        ultimos_diri = afectados_diri

#total

    numero_afectados_toal = numero_afectados_diri + numero_afectados_nodiri

#impresion total
    if lt.size(lista_total) >= 6:
        primeros_total = lt.subList(lista_total,1,3)
        ultimos_total = lt.subList(lista_total,lt.size(lista_total)-2,3)
    else: 
        primeros_total = lista_total
        ultimos_total = lista_total


    return restantes_digrafo,restantes_grafo,numero_afectados_nodiri,primeros_nodiri,ultimos_nodiri,numero_afectados_diri,primeros_diri,ultimos_diri,numero_afectados_toal,primeros_total,ultimos_total