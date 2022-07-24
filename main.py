# Title:    Convert CSV File To MD File
# By:       Mehmet Yilmaz
# Date:     12-8-2021
# Sources:
#   1) https://thispointer.com/python-read-csv-into-a-list-of-lists-or-tuples-or-dictionaries-import-csv-to-list/
#   2) https://stackoverflow.com/questions/33686747/save-a-list-to-a-txt-file
# Format:
#   python3 csv_to_md.py example.csv
#     |             \              \
#   [run python]  [script name]  [csv file to convert]

from csv import reader
import os.path
import sys

# print list, line by lines
def print_list(data):
    for rows in data:
        print(rows)

# read csv to list of lists
def csv_to_lists(filename):
    to_list = []
    with open(filename, 'r') as rows:
        csv_reader = reader(rows)
        to_list = list(csv_reader)
    return to_list

# find largest char count for a str in EACH column
def largest_strings(data):
    lrg_col_str = []
    colms = {}
    for i in range(len(data)):
        for j in range(len(data[i])):
            colms[j] = []
    for i in range(len(data)):
        for j in range(len(data[i])):
            colms[j].append(len(data[i][j]))
    for key in colms:
        lrg_col_str.append(max(colms[key]))
        
    return lrg_col_str

# evenly space characters for table
def space_character(str_input, ideal_size):
    str_input_len = len(str_input)
    if(str_input_len > ideal_size):
        print("-ERROR: Invalid, string is bigger then ideal string size (max size)")
        print("-Values: ")
        print("   -inputed string: " + str(str_input))
        print("   -ideal_max_size: " + str(ideal_size) + "\n")
        return
    else:
        diff = ideal_size - len(str(str_input))

        for i in range(diff):
            str_input = str_input + " "
        return str_input

# TODO: clean up code, its a bit messy

def main(input_csv_filename):
    # load csv file into a list of lists
    csv_data = csv_to_lists(input_csv_filename)

    # store final string values (lines)
    csv_converted_to_md = []

    # if a label is empty, add a space (1 char) to that label
    for i in range(len(csv_data[0])):
        if(len(csv_data[0][i]) == 0):
            csv_data[0][i] = " "

    # calculate largest string value PER column
    cl = largest_strings(csv_data)

    # convert csv labels from csv to md
    labels = csv_data[0]
    csv_data.pop(0)
    label_md = "|"
    for i in range(len(labels)):
        labels[i] = space_character(labels[i], cl[i])
        label_md = label_md + labels[i] + "|"
    csv_converted_to_md.append(label_md)

    # create spreadsheet md line (required for md)
    def_line = ""
    for i in range(len(label_md)):
        if(label_md[i] != "|"):
            def_line = def_line + "-"
        else:
            def_line = def_line + "|"
    csv_converted_to_md.append(def_line)

    # covert the rest of the rows, not label row, to md format
    for i in range(len(csv_data)):
        row_md = "|"
        for j in range(len(csv_data[i])):
            row_md = row_md + space_character(csv_data[i][j], cl[j]) + "|"
        csv_converted_to_md.append(row_md)

    # save converted csv to a md file
    output_filename = input_csv_filename.split(".")[0] + ".md" # "converted_csv.md"
    with open(output_filename, 'w') as output:
        for row in csv_converted_to_md:
            output.write(str(row) + '\n')

    print("Converted csv to md file. File: " + str(output_filename))

# main calls, with input validation
if __name__ == "__main__":
    args = list(sys.argv)

    try:
    
        if(len(args) == 2):
            usr_csv = str(args[1])

            if(os.path.isfile(usr_csv)):
                md_name = usr_csv.split(".")[0] + ".md"
                if(os.path.isfile(md_name) == False):
                    main(usr_csv)
                else:
                    print("-ERROR: The md name for your inputted csv file already exists = " + str(usr_csv) + " -> " + str(md_name))
            else:
                print("-ERROR: Inputted file does not exist!")
                
        else:
            print("-ERROR: Invalid arugments")
            print("-Valid Format: python3 csv_to_md.py example.csv")
    
    except:
        print("-ERROR: Unknown error occurred!")

