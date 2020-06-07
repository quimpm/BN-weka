#!/bin/env python3
import csv
import argparse

# We assume there are not empty cells

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        try:
            int(s)
            return True
        except ValueError:
            return False

def type_assignment(data, attributes, cols, rows):
    col_type = [[] for _ in range(cols)]
    nominal_domain = [[] for _ in range(cols)]
    for j in range(1, rows):
        for i in range(cols):
            cell = data[j][i]
            if is_number(cell) and \
               col_type[i] != "NOMINAL":
                col_type[i] = "NUMERIC"
            else:
                if not col_type[i]:
                    col_type[i] = "NOMINAL"
                formated_cell = "'"+str(cell)+"'"
                if formated_cell not in nominal_domain[i]:
                    nominal_domain[i].append(formated_cell)

    for i in range(cols):
        real_domain = ""
        if col_type[i] == "NOMINAL":
            real_domain = ",".join(nominal_domain[i])
            col_type[i] = "{" +  real_domain + "}"
    return col_type

def open_read_csv(csv_file):
    with open(csv_file) as f:
        reader = csv.reader(f)
        all_data = list(reader)
        f.close()

    attributes = all_data[0]
    total_cols = len(attributes)
    total_rows = len(all_data)
    return all_data, attributes, total_cols, total_rows
    
def write_arff(arff_file, relation, attributes,
               col_type, rows, data):
    with open(arff_file, 'w') as f:
        f.write("@RELATION " + relation + "\n\n")
        for i in range(len(col_type)):
            f.write("@ATTRIBUTE" + " '" +   \
                    attributes[i] + "' " +  \
                    col_type[i] + "\n"      )
        f.write("\n@DATA\n")
        for i in range(1, rows):
            f.write(','.join(data[i])+"\n")

def parse_args():
    parser = argparse.ArgumentParser(prog='csv_to_arff')
    parser.add_argument('input', help='input CSV file name')
    parser.add_argument('output', help='output ARFF file name')
    parser.add_argument('-n', '-name', help="ARFF relation name")
    args = parser.parse_args()
    if args.n == None:
        args.n = "Relation"
    return args


def main():
    args = parse_args()

    data, attributes, cols, rows = open_read_csv(args.input)
    col_type= type_assignment(data, attributes, cols, rows)
    write_arff(args.output, args.n, attributes, col_type, rows, data)

if __name__=="__main__":
    main()
