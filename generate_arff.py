#!/bin/env python3
import csv
import sys
import math
import random

DNI_DIGITS = 83707 #DNI Quim
overall_satisfaction = {
        "1.0" : "1",
        "1.5" : "2",
        "2.0" : "3",
        "2.5" : "4",
        "3.0" : "5",
        "3.5" : "6",
        "4.0" : "7",
        "4.5" : "8",
        "5.0" : "9"
    }

''' 
    Trata los parámetros de entrada 

    Retorna
        sys.argv[1] Primer argumento, corresponde al archivo csv con el dataset
        sys.argv[2] Segundo argumento, corresponde al archivo donde se desea
                    guardar el archivo ARFF de aprendizaje para la red Bayesiana
        sys.argv[3] Tercer argumento, corresponde al archivo donde se desea 
                    guardar el archivo ARFF de evaluación  de la red Bayesiana
'''
def param_treatment():
    if len(sys.argv) != 4:
        print("Usage: python3 script.py <data_file> <learning_file> <evaluation_file>") 
        exit()
    return sys.argv[1], sys.argv[2], sys.argv[3]


''' 
    Utiliza el módulo csv para leer todos los datos del dataset y retornar su
    información útil.
    
    Parámetos
        filename Nombre del archivo csv con la base de datos
    Retorna
        data[1:]    Datos del archivo csv sin la fila de atributos
        attributes  Lista con el nombre de los atributos de la base de datos 
        total_cols  Número de columnas del dataset
        total_rows  Número de filas del dataset
'''
def get_data(filename):
    with open(filename) as f:
        reader = csv.reader(f)
        data = list(reader)
    attributes = data[0]
    total_cols = len(attributes)
    total_rows = len(data)-1
    return data[1:], attributes, total_cols, total_rows

""" 
    Divide el dataset en 2 subsets, el set de aprendizaje y el set de 
    evaluación. La selección de las columnas es aleatoria

    Parámetros
        data_set    Dataset que se dividirá
        entries     Número de atributos del dataset
    Retorna
        learning_data       Dataset de aprendizaje
        evaluation_data     Dataset de evaluación
"""
def make_dataset_partition(data_set, entries):
    division = entries//4 * 3
    random.seed(DNI_DIGITS)
    n = 0
    learning_data = []
    evaluation_data = []
    for i in range(entries):
        if n < division:
            index = random.randint(0,len(data_set)-1)
            elem = data_set.pop(index)
            learning_data.append(elem)
        else:
            evaluation_data = data_set
        n +=1
    return learning_data, evaluation_data


"""
    Genera la división por la que se harán los cuartiles que 
    comprimirán la latitud y longitud. Primero ordena el dataset
    según ese parámetro (latitud y longitud), y luego elige
    el valor que hará de frontera superior para cada cuartil.

    Parámetros
        data_set    Dataset sobre la que se calcularán los cuartiles
    Retorna
        lat_qi      Delimitador superior del quartil i de latitud, 0 < i < 4
        lon_qi      Delimitador superior del quartil i de longitud, 0 < i < 4
"""
def get_quartiles(data_set):
    data_set = sorted(data_set, key=lambda data: data[7])
    lat_q1 = float(data_set[(len(data_set)+1)//4][7])
    lat_q3 = float(data_set[(len(data_set)+1)*3//4][7])
    lat_q2 = float(data_set[((len(data_set)+1)*2//4)][7])
    data_set = sorted(data_set, key=lambda data: data[8])
    lon_q1 = float(data_set[(len(data_set)+1)//4][8])
    lon_q3 = float(data_set[(len(data_set)+1)*3//4][8])
    lon_q2 = float(data_set[(len(data_set)+1)*2//4][8])
    return lat_q1, lat_q2, lat_q3, lon_q1, lon_q2, lon_q3

'''
    Dado un dataset (data_set) y un índice (i), convierte los valores
    contínuos de longitud y latitud a valores discretos de dicha fila
    del dataset. La conversión se hará según los quartiles especificados
    en los parámetros por lat_qi y lon_qi.

    Parámetros
        data_set    Dataset sobre el que se hará la conversión
        i           Índice de la fila sobre la que se quiere aplicar la reducción
        lat_qi      Delimitador superior del quartil i de latitud, 0 < i < 4
        lon_qi      Delimitador superior del quartil i de longitud, 0 < i < 4
'''
def lat_lon_discrete(data_set, i, lat_q1, lat_q2, lat_q3, lon_q1, lon_q2, lon_q3):
    #Latitude
    if float(data_set[i][7]) < lat_q1:
        data_set[i][7] = "1"
    elif float(data_set[i][7]) < lat_q2:
        data_set[i][7] = "2"
    elif float(data_set[i][7]) < lat_q3:
        data_set[i][7] = "3"
    else:
        data_set[i][7] = "4"
    #Longitude
    if float(data_set[i][8]) < lon_q1:
        data_set[i][8] = "1"
    elif float(data_set[i][8]) < lon_q2:
        data_set[i][8] = "2"
    elif float(data_set[i][8]) < lon_q3:
        data_set[i][8] = "3"
    else:
        data_set[i][8] = "4"


'''
    Transforma los valores de el dataset de contínuos a discretos.
    Recorre todas las filas del dataset, a cada fila le aplica las
    transformaciones: traducir la satisfacción, latitud, longitud,
    precio y reviews.

    Parámetros:
        data_set    Dataset sobre el que se quiere aplicar la reducción
    Retorna:
        data_set    Dataset sobre el que se ha aplicado la reducción
    
'''
def continuous_to_discrete(data_set):
    lat_q1, lat_q2, lat_q3, lon_q1, lon_q2, lon_q3 = get_quartiles(data_set)
    for i,row in enumerate(data_set):
        data_set[i][3] = overall_satisfaction[data_set[i][3]]
        lat_lon_discrete(data_set, i, lat_q1, lat_q2, lat_q3, lon_q1, lon_q2, lon_q3)
        price_review_discrete(data_set, i)
    return data_set


'''
    Dado un dataset (data_set) y un índice (i), traduce los valores
    de dicha fila del dataset de contínuos a discretos. Los valores
    sobre los que aplica la reducción son los que hacen referencia
    al precio y a las reviews. Reduce aplicando una división entera.
    No retorna nada ya que nos aprovechamos de la mutabilidad del
    dataset.

    Parámetros
        data_set    Dataset sobre el que se aplicará la reducción
        i           Índice de la fila sobre la que se quiere aplicar
                    la reducción
'''
def price_review_discrete(data_set, i):
    data_set[i][6] = str(float(data_set[i][6])//20)
    data_set[i][2] = str(float(data_set[i][2])//20)

'''
    Escribe un documento en formato ARFF dada la información necesaria sobre
    el dataset.

    Parámetros
        arff_file   Nombre del archivo sobre el cual se escribirán los datos
        attributes  Lista con el nombre de atributos del dataset
        att_domain  Lista con el dominio de cada atributo
        rows        Número de filas del dataset
        data        Dataset sin la fila de atributos
        relation    Nombre de la relación
'''
def write_arff(arff_file, attributes, att_domain, rows, data, relation):
    with open(arff_file, 'w') as f:
        f.write("@RELATION " + " " + str(relation) + "\n\n")
        for i in range(len(att_domain)):
            f.write("@ATTRIBUTE" + " '" +   \
                    attributes[i] + "' " +  \
                    att_domain[i] + "\n"      )
        f.write("\n@DATA\n")
        for i in range(len(data)):
            line = ["'" + cell + "'" for cell in data[i]]
            f.write(','.join(line)+"\n")


'''
    Genera una lista con el dominio de cada atributo, es decir, cada
    valor diferente del atributo. 

    Parámetros
        data        Dataset sobre el que generar los dominios
        attributes  Lista con los atributos del dataset
        cols        Número de columnas del dataset
    Retorna
        att_domain  Lista con el dominio de cada atributo
'''
def domain_assignment(data, attributes, cols):
    att_domain = [[] for _ in range(cols)]
    specific_domain = [[] for _ in range(cols)]

    for j in range(len(data)):
        for i in range(cols):
            cell = data[j][i]
            formated_cell = "'"+str(cell)+"'"
            if formated_cell not in specific_domain[i]:
                specific_domain[i].append(formated_cell)

    for i in range(len(att_domain)):
        att_domain[i] = "{ "+ ",".join(specific_domain[i]) + "}"
    return att_domain

'''
    Acarrea toda la lógica del programa.
    Trata los parámetros, interpreta el csv, transforma
    de contínuo a discreto, parte el dataset en aprendizaje
    y evaluación y escribe su pertinente ARFF.
'''
def main():
    ''' Tratar parámetros y interpretar csv '''
    filename, learning_file, evaluation_file = param_treatment()
    data, attributes, total_cols, total_rows = get_data(filename)
    

    ''' Transforma de contínuo a discreto y parte el dataset '''
    discrete_data = continuous_to_discrete(data)
    att_domain = domain_assignment(discrete_data, attributes, total_cols)
    learning_data, evaluation_data = make_dataset_partition(discrete_data, total_rows)

    ''' Escribe los archivos ARFF '''
    write_arff(learning_file, attributes, att_domain, total_rows, learning_data, "LEARNING")
    write_arff(evaluation_file, attributes, att_domain, total_rows, evaluation_data, "EVALUATION")


'''
    Punto de entrada del programa
'''
if __name__=="__main__":
    main()



