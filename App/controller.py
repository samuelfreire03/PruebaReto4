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
 """

import config as cf
import model
import csv
from DISClib.ADT import list as lt


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # analyzer es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer

def loadAirportsRutes(analyzer):
    """
    Carga los datos de los archivos CSV en el modelo.
    Se crea un arco entre cada par de estaciones que
    pertenecen al mismo servicio y van en el mismo sentido.

    addRouteConnection crea conexiones entre diferentes rutas
    servidas en una misma estación.
    """
    airportsfile = cf.data_dir + 'Vuelos/airports_full.csv'
    rutasfile = cf.data_dir + 'Vuelos/routes_full.csv'
    ciudaesfile = cf.data_dir + 'Vuelos/worldcities.csv'

    input_file_aeropuertos = csv.DictReader(open(airportsfile, encoding="utf-8"),
                                delimiter=",")

    input_file_rutas = csv.DictReader(open(rutasfile, encoding="utf-8"),
                                delimiter=",")

    input_file_ciudades = csv.DictReader(open(ciudaesfile, encoding="utf-8"),
                                delimiter=",")

    for aeropuerto in input_file_aeropuertos:
        model.addVerticeGrafo(analyzer,aeropuerto)

    for ruta in input_file_rutas:
        model.addRuta(analyzer,ruta)

    for ciudad in input_file_ciudades:
        model.addCiudad(analyzer,ciudad)

    model.addRutaidayvuleta(analyzer)

# Funciones para la carga de datos

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def infoaeropuerto(analyzer,codigoAita):
    informacion = model.infoaeropuerto(analyzer,codigoAita)
    return informacion

def primer_req(analyzer):
    """
    Retorna los libros que fueron publicados
    en un año
    """
    mayorruta = model.primer_req(analyzer)
    return mayorruta

def segundo_req(analyzer,codigo1,codigo2):
    """
    Retorna los libros que fueron publicados
    en un año
    """
    conectados = model.segundo_req(analyzer,codigo1,codigo2)
    return conectados
