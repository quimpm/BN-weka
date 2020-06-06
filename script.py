import csv
import sys
import math

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
        for entries,row in enumerate(csvReader):
            data.append(row)
    return data, entries

def make_dataset_partition(data, entries, division):
    pass

def main():
    """Read Data"""
    filename, learning_file, evaluation_file = param_treatment(sys.argv)
    data, entries = get_data(filename)
    division = entries//4 * 3
    "Get divisions of data"  
    learing_data, evaluation_data = make_dataset_partition(division, data)

if __name__=="__main__":
    main()