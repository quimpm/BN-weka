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

""" This function ensures a good usage of the script """
def param_treatment(args):
    if len(args) != 4:
        print("Usage: python3 script.py <data_file> <learning_file> <evaluation_file>") 
        exit()
    return args[1], args[2], args[3]

""" Function to get all the data of the csv file """
def get_data(filename):
    with open(filename) as f:
        reader = csv.reader(f)
        data = list(reader)
    attributes = data[0]
    total_cols = len(attributes)
    total_rows = len(data)-1
    return data[1:], attributes, total_cols, total_rows

""" Function to split the dataset into to sets, the learning set and the 
evaluation set. The selection of the rows is random. """
def make_dataset_partition(data_set, entries, division):
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

""" Get quartiles from the mean """
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

"""Convert continuous values into discrete values"""
def continuous_to_discrete(data):
    lat_q1, lat_q2, lat_q3, lon_q1, lon_q2, lon_q3 = get_quartiles(data)
    for row in data:
        row[3] = overall_satisfaction[row[3]]
        #Latitude
        if float(row[7]) < lat_q1:
            row[7] = "1"
        elif float(row[7]) < lat_q2:
            row[7] = "2"
        elif float(row[7]) < lat_q3:
            row[7] = "3"
        else:
            row[7] = "4"
        #Longitude
        if float(row[8]) < lon_q1:
            row[8] = "1"
        elif float(row[8]) < lon_q2:
            row[8] = "2"
        elif float(row[8]) < lon_q3:
            row[8] = "3"
        else:
            row[8] = "4"
    return data

def write_arff(arff_file, attributes,
               col_type, rows, data):
    with open(arff_file, 'w') as f:
        f.write("@RELATION " + " RELATION" + "\n\n")
        for i in range(len(col_type)):
            f.write("@ATTRIBUTE" + " '" +   \
                    attributes[i] + "' " +  \
                    col_type[i] + "\n"      )
        f.write("\n@DATA\n")
        for i in range(len(data)):
            line = ["'" + cell + "'" for cell in data[i]]
            f.write(','.join(line)+"\n")

def type_assignment(data, attributes, cols):
    col_type = [[] for _ in range(cols)]
    domain = [[] for _ in range(cols)]

    for j in range(len(data)):
        for i in range(cols):
            cell = data[j][i]
            formated_cell = "'"+str(cell)+"'"
            if formated_cell not in domain[i]:
                domain[i].append(formated_cell)

    for i in range(len(col_type)):
        col_type[i] = "{ "+ ",".join(domain[i]) + "}"
    return col_type


def find_value(data, searching):
    for row in data:
        for value in row:
            if value == searching:
                print(value)

def main():
    """Read Data"""
    filename, learning_file, evaluation_file = param_treatment(sys.argv)
    data, attributes, total_cols, total_rows = get_data(filename)
    entries = len(data)
    division = entries//4 * 3
    

    "Get divisions of data"  
    discrete_data = continuous_to_discrete(data)
    col_type = type_assignment(discrete_data, attributes, total_cols)

    learning_data, evaluation_data = make_dataset_partition(discrete_data, entries, division)


    write_arff(learning_file, attributes, col_type, total_rows, learning_data)
    write_arff(evaluation_file, attributes, col_type, total_rows, evaluation_data)

if __name__=="__main__":
    main()









