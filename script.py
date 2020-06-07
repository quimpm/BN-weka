import csv
import sys
import math
import random

DNI_DIGITS = 83707
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
    data = []
    with open(filename) as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            if row[0] != "room_type":
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

"""Get the mean of latitude and longitude columns on the dataset"""
def get_lat_lon_mean(data_set):
    first_row = data_set.pop()
    lat_mean = float(first_row[7])
    lon_mean = float(first_row[8])
    for row in data_set:
        lat_mean = (lat_mean + float(row[7]))/2
        lon_mean = (lon_mean + float(row[8]))/2
    return lat_mean, lon_mean

""" Get quartiles from the mean """
def get_quartiles(mean):
    return mean/2, mean, mean + mean/2

"""Convert continous values into discrete values"""
def continous_to_discrete(data):
    lat_mean, lon_mean = get_lat_lon_mean(data)
    lat_q1, lat_q2, lat_q3 = get_quartiles(lat_mean)
    lon_q1, lon_q2, lon_q3 = get_quartiles(lon_mean)
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

def main():
    """Read Data"""
    filename, learning_file, evaluation_file = param_treatment(sys.argv)
    data = get_data(filename)
    entries = len(data)
    division = entries//4 * 3

    "Get divisions of data"  
    learning_data, evaluation_data = make_dataset_partition(data, entries, division)
    learning_data = continous_to_discrete(learning_data)
    evaluation_data = continous_to_discrete(evaluation_data)
    write_arff(learning_data, learning_file)
    write_arff(evaluation_data, evaluation_file)

if __name__=="__main__":
    main()