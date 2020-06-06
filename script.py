import csv
import sys
import math
import random

DNI_DIGITS = 83707

""" This function ensures a good usage of the script """
def param_treatment(args):
    if len(args) != 4:
        print("Usage: python3 script.py <data_file> <learning_file> <evaluation_file>") 
        exit()
    return args[1], args[2], args[3]

""" Function to get all the data of the csv file """
def get_data(filename):
    data = []
    with open(filename) as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            data.append(row)
    return data

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


def main():
    """Read Data"""
    filename, learning_file, evaluation_file = param_treatment(sys.argv)
    data = get_data(filename)
    entries = len(data)
    division = entries//4 * 3

    "Get divisions of data"  
    learning_data, evaluation_data = make_dataset_partition(data, entries, division)

if __name__=="__main__":
    main()