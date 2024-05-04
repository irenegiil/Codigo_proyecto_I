#importamos las librerías que vamos a utilizar
import pandas as pd #mediante esta librería, cargaremos nuestro csv
import matplotlib.pyplot as plt #mediante esta librería, junto con networkx dibujaremos nuestro grafo
import networkx as nx #mediante esta librería, junto con matplotlib dibujaremos nuestro grafo
from geopy.distance import geodesic #mediante esta librería, calcularemos las distancias en kilómetros entre cada par de calles

df = pd.read_csv('C:\Git\Codigo_proyecto_I\PEATONES_2021.csv', sep=';') #cargamos nuestro csv que muestra por cada día y hora, la cantidad de peatones de algunas calles, plazas... y distintos lugares de Madrid junto con su latitud, longitud de dicho sitio.
df = df.drop(columns = ['IDENTIFICADOR', 'NÚMERO_DISTRITO', 'NÚMERO', 'CÓDIGO_POSTAL', 'OBSERVACIONES_DIRECCION']) #eliminamos las columnas que no vamos a utlizar
df['NOMBRE_VIAL'] = df['NOMBRE_VIAL'].replace('Madrid Río. Puente de Segovia con Paseo Ermita del Santo Senda peatonal', 'Puente de Segovia con Paseo Ermita del Santo') #cambiamos el nombre de ese lugar de Madrid por otro que hace referencia al mismo sitio pero es más corto, lo que nos facilita después la visualización del grafo

def quitar_2021_y_hora_en_primera_columna(elemento): #creamos una función, con la que vamos a borrar el año 2021 y la hora de todos los elementos de la columna df['FECHA'], lo que hace que nuestra implementación del csv a nuestro proyecto, tenga más sentido
    horaa=elemento.split(":")[0]
    if len(horaa)==12: #esta condición es para los casos en las que la hora está formada por una cifra (por ejemplo, 9:00, 0:00...)
        return elemento[:-10] #en estos casos, tendremos que eliminar los últimos 10 elementos del objeto de cadena
    else:
        return elemento[:-11] #en estos casos, tendremos que eliminar los últimos 11 elementos del objeto de cadena

df['FECHA'] = df['FECHA'].apply(quitar_2021_y_hora_en_primera_columna) #le aplicamos la función a cada elemento que forma la columna 'FECHA'
calles = df['NOMBRE_VIAL'].unique() #en la variable calles, guardamos el nombre de todas las distintas calles
dia = input('Escriba el día actual, por ejemplo 01/01: ') #solicitamos al taxista que introduzca el día en el que se encuentra
hora = input('Escriba la hora qué es pero aproximando a la hora en punto que esté más cerca, es decir, si son las 12:40 pon las 13:00 : ') #solicitamos al taxista que introduzca la hora en la que se encuentra (aproximada)
calle = input('Escriba el nombre de la calle en la que se encuentra: ') #solicitamos al taxista que introduzca la calle en la que se encuentra, solos siendo posible si la calle pertenece a una de las 18 calles con las que estamos trabajando

#Lanzamos errores manuales mediante la instrucción raise
if dia not in df['FECHA'].values:
    raise KeyError('La fecha proporcionada o no está bien escrita o no es válida')
elif hora not in df['HORA'].values:
    raise KeyError('La hora proporcionada o no está bien escrita o no es válida')
elif calle not in df['NOMBRE_VIAL'].values:
    raise KeyError('Tu calle inicio no es una calle válida para este algoritmo o la has escrito mal')

grafo_calles = {} #en este diccionario almacenaremos por cada calle, otro diccionario en el que cada clave serán las restantes 17 calles y el valor será (peatonescalle2)/(distanciaentrecalle1ycalle2)
grafo_distancias = {} #este diccionario es igual que el de grafo_calles, solo que el valor que almacena la clave del diccionario (que este diccionario es el valor de la primera clave), es (distanciaentrecalle1ycalle2)
for calle1 in calles: #recorremos cada calle
    grafo_calles[calle1]={} #el valor de la clave calle1 es un diccionario
    grafo_distancias[calle1]={} #el valor de la clave calle1 es un diccionario
    for calle2 in calles:
        if calle1 != calle2: #para no calcular el valor entre una calle y ella misma
            latitud_calle1 = df[df['NOMBRE_VIAL'] == calle1]['LATITUD'].values[0].replace(',', '.') #accedemos a la latitud de la calle1 en nuestro csv
            longitud_calle1 = df[df['NOMBRE_VIAL'] == calle1]['LONGITUD'].values[0].replace(',', '.') #accedemos a la longitud de la calle1 en nuestro csv
            latitud_calle2 = df[df['NOMBRE_VIAL'] == calle2]['LATITUD'].values[0].replace(',', '.') #accedemos a la latitud de la calle2 en nuestro csv
            longitud_calle2 = df[df['NOMBRE_VIAL'] == calle2]['LONGITUD'].values[0].replace(',', '.') #accedemos a la longitud de la calle2 en nuestro csv

            #mediante la librería Geopy, vamos a calcular la distancia geodésica entre calle1 y calle2
            distancia_entre_calle1ycalle2 = geodesic((float(latitud_calle1), float(longitud_calle1)), (float(latitud_calle2), float(longitud_calle2))).kilometers #calculamos la distancia geodésica en kilómetros entre calle1 y calle2 gracias a los valores de latitud y longitud de cada una de estas 2 calles
            numero_peatones_calle2 = df.loc[(df['HORA'] == hora) & (df['NOMBRE_VIAL'] == calle2) & (df['FECHA'] == dia)]['PEATONES'].iloc[0] #accedemos al número de peatones de la calle2 en función de la hora y el día
            grafo_calles[calle1][calle2] = (numero_peatones_calle2)/distancia_entre_calle1ycalle2 #vamos a asignar el valor que tendrá la clave del diccionario (que este diccionario es el valor de la primera clave), siendo el valor (peatonescalle2)/(distanciaentrecalle1ycalle2)
            grafo_distancias[calle1][calle2] = distancia_entre_calle1ycalle2 #vamos a asignar el valor que tendrá cada arista en nuestro diccionario, siendo el valor (distanciaentrecalle1ycalle2)

#creamos una función en la que implementaremos el algoritmo de Dijkstra, pero con su funcionamiento inverso (calcula el camino más largo)
def camino_optimo_dijkstra(grafo, calle_inicio):
    valor = {}
    camino_optimo = [] #en esta lista almacenaremos el camino óptimo

    for calle in grafo:
        valor[calle] = float('-inf') #inicializamos todos los valores a -oo, y ponemos -inf ya que queremos que haga justo lo contrario de lo que haría el algoritmo de Dijkstra
    valor[calle_inicio] = 0

    calles = [calle for calle in grafo] #lista con todas las calles

    while calles: #mientras haya calles disponibles que recorrer
        calle_1=max(calles, key=valor.get) #cogemos la calle con el máximo valor
        calles.remove(calle_1) #quitamos esa calle de la lista de calles disponibles para recorrer
        camino_optimo.append(calle_1) #añadimos esa calle al camino óptimo

        for vecino in grafo[calle_1]: #recorremos los vecinos de la calle en concreto
            if vecino in calles and valor[vecino] < valor[calle_1] + grafo[calle_1][vecino]: #aquí comprobamos si el vecino está en la lista calles y si su valor es menor al de la calle en la que se encontraría más el valor de (peatonescalle2)/(distanciaentrecalle1ycalle2)
                valor[vecino] = valor[calle_1] + grafo[calle_1][vecino] #actualizamos el valor del vecino

    return camino_optimo #devolvemos la lista con el camino óptimo

def dibujar_grafo(grafo, camino): #creamos una función que nos dibujará en forma de grafo nuestro camino más óptimo, siendo de una manera más visible el camino que el taxista deberá de seguir
    G = nx.DiGraph()
    plt.figure(figsize=(20,10)) #creamos la figura en la que se dibujará el grafo, con 20 pulgadas de anchura y 10 pulgadas de altura
    calles_camino = []
    for i in camino:
        calles_camino.append(i) #añadimos las 18 calles a la lista calles_camino, en el orden que va a ser nuestro camino representado con el grafo
    G.add_nodes_from(calles_camino) #añadimos a nuestro grafo las calles como vértices (nodos)

    for i in range(len(camino) - 1): #así, recorremos cada calle
        nodo_actual = camino[i]
        vecino_actual = camino[i + 1]
        valor_arista = grafo[nodo_actual][vecino_actual] #la longitud de la arista será proporcional a la distancia geodésica en kilómetros entre el nodo actual y el vecino actual
        G.add_edge(nodo_actual, vecino_actual, weight=valor_arista) #añadimos la arista con el valor calculado anteriormente entre esas 2 calles

    #dibujamos el grafo, en el que la disposición de los nodos siguen el algoritmo Fruchterman Reingold
    nx.draw(G, nx.fruchterman_reingold_layout(G, k=0.1), with_labels=True, node_color='lightskyblue', edge_color = 'navy', font_size=10)
    plt.show()

dibujar_grafo(grafo_distancias, camino_optimo_dijkstra(grafo_calles, calle)) #dibujamos dicho camino óptimo mediante un grafo