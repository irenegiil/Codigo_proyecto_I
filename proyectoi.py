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
numero_calles = int(input('Escriba el número de cuántas calles quieres visitar: '))

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

#creamos una función en la que implementaremos el algoritmo de Dijkstra
def camino_optimo_dijkstra(grafo, calle_inicio, num_calles_visitar):
    valor = {}
    camino_optimo = []

    for calle in grafo:
        valor[calle] = float('-inf') #inicializamos todos los valores a -oo, y ponemos -inf ya que queremos que haga justo lo contrario de lo que haría el algoritmo de Dijkstra
    valor[calle_inicio] = 0

    calles = [calle for calle in grafo]
    calles_visitadas = 0
    while calles and calles_visitadas < num_calles_visitar:
        calle_1=max(calles, key=valor.get)
        calles.remove(calle_1)
        camino_optimo.append(calle_1)
        calles_visitadas += 1

        for vecino in grafo[calle_1]:
            if vecino in calles and valor[vecino] < valor[calle_1] + grafo[calle_1][vecino]:
                valor[vecino] = valor[calle_1] + grafo[calle_1][vecino]

    #vamos a dibujar nuestro camino mediante un grafo, para que se vea de una manera más visual utilizando la librería networkx
    G = nx.DiGraph()
    plt.figure(figsize=(11,8))
    calles_camino = []
    for i in camino_optimo:
        calles_camino.append(i)
    G.add_nodes_from(calles_camino) #añadimos a nuestro grafo las calles como vértices (nodos)

    for i in range(len(camino_optimo) - 1): #así recorremos cada calle
        nodo_actual = camino_optimo[i]
        vecino_actual = camino_optimo[i + 1]
        valor_arista = grafo[nodo_actual][vecino_actual] #vemos por cada calle, el valor asociado con su vecino
        G.add_edge(nodo_actual, vecino_actual, weight=valor_arista) #añadimos la arista con el valor calculado anteriormente

    #dibujamos el grafo
    nx.draw(G, nx.spring_layout(G), with_labels=True)
    plt.show()

print(camino_optimo_dijkstra(grafo_calles, calle, numero_calles))