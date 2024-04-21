#importamos las librerías que vamos a utilizar
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from geopy.distance import geodesic

#cargamos nuestro csv que muestra por cada día y hora, la cantidad de peatones de algunas calles de Madrid junto con su latitud, longitud...
df = pd.read_csv('PEATONES_2021.csv', sep=';')
calles = df['NOMBRE_VIAL'].unique()
dia = input('Escriba el día y la hora de ahora pero poniendo de año 2021, por ejemplo 01/01/2021 0:00 : ')
hora = input('Escriba la hora qué es pero aproximando a la hora en punto que esté más cerca, es decir, si son las 12:40 pon la 13:00 : ')
calle = input('Escriba el nombre de la calle en la que se encuentra: ')

grafo_calles = {} #en este diccionario almacenaremos por cada calle, otro diccionario en el que cada clave serán sus vecinos y el valor será (peatonescalle1 + peatonescalle2)/(distanciaentrecalle1ycalle2)
#vamos a construir este diccionario
for calle1 in calles:
    grafo_calles[calle1]={}
    for calle2 in calles:
        if calle1 != calle2: #para no calcular el valor entre una calle y ella misma
            latitud_calle1 = df[df['NOMBRE_VIAL'] == calle1]['LATITUD'].values[0].replace(',', '.')
            longitud_calle1 = df[df['NOMBRE_VIAL'] == calle1]['LONGITUD'].values[0].replace(',', '.')
            latitud_calle2 = df[df['NOMBRE_VIAL'] == calle2]['LATITUD'].values[0].replace(',', '.')
            longitud_calle2 = df[df['NOMBRE_VIAL'] == calle2]['LONGITUD'].values[0].replace(',', '.')

            #mediante la librería Geopy, vamos a calcular la distancia geodésica entre calle1 y calle2
            distancia_entre_calle1ycalle2 = geodesic((float(latitud_calle1), float(longitud_calle1)), (float(latitud_calle2), float(longitud_calle2))).kilometers
            numero_peatones_calle1 = df.loc[(df['HORA'] == hora) & (df['NOMBRE_VIAL'] == calle1) & (df['FECHA'] == dia)]['PEATONES'].iloc[0]
            numero_peatones_calle2 = df.loc[(df['HORA'] == hora) & (df['NOMBRE_VIAL'] == calle2) & (df['FECHA'] == dia)]['PEATONES'].iloc[0]
            #vamos a asignar el valor que tendrá cada arista en nuestro diccionario, siendo el valor (peatonescalle1 + peatonescalle2)/(distanciaentrecalle1ycalle2)
            grafo_calles[calle1][calle2] = (numero_peatones_calle1 + numero_peatones_calle2)/distancia_entre_calle1ycalle2