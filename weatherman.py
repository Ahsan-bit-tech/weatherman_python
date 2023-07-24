from datetime import datetime
import argparse
import calendar
import csv
from colorama import Fore

max_humid, min_temp, date_list, max_temp = [], [], [], []
parser = argparse.ArgumentParser(description="Check data from the dataset")
parser.add_argument('passing_date', help="pass the date as string ", type=str)
parser.add_argument('passing_path', help="path of the file", type=str)
parser.add_argument('-e', '--comparison', action="store_true", help="For comparison ")
parser.add_argument('-a', '--average',action="store_true", help="For calculating average")
parser.add_argument('-c', '--Two_bar_graphs', help="For ploting graph", action="store_true")
parser.add_argument('-b', '--One_bar_graphs', help="For ploting graph", action="store_true")
argparse = parser.parse_args()
year_num = argparse.passing_date

if len(year_num) > 4:
    date_month_lst = year_num.split('/')  # to take arguments value from the commandline and slipt the argumets
    year_num = int(date_month_lst[0])
    if date_month_lst[1] !='':
        month_number = int(date_month_lst[1])  # starting of the month as jan
elif len(year_num) == 4:
    date_month_lst = year_num
else:
    print("Invalid year")


def calculate_average(lst):  # function to calculate the average of required list
    total = sum(lst)
    round_ =round(total / len(lst),2)
    return round_


def print_date_month(lst, temp):  # to print the name of the month with the date
    check_index_of_lst = lst.index(temp)
    date_format = datetime.strptime(date_list[check_index_of_lst], '%Y-%m-%d')
    temp = date_format.strftime('%B %d')
    return temp


def join_file_format(month_value):  # to change the string into file name like file-->>>file.txt according to the date
    month_format = calendar.month_abbr[month_value]
    if argparse.passing_path != '':
        directory_read(argparse.passing_path+"\lahore_weather_" + str(year_num) + '_' + month_format + '.csv')
    else:
        print("File path is not defined")


def directory_read(direct):
    global max_humid, min_temp, max_temp
    with open(direct, 'r') as file:
        csvreader = csv.reader(file)
        line_space = file.readline()
        for line in csvreader:
            if line[1] != '':
                max_temp.append(float(line[1]))
            if line[3] != '':
                min_temp.append(float(line[3]))
            if line[7] != '':
                max_humid.append(float(line[7]))
            date_list.append(str(line[0]))

    file.close()
    return


if argparse.comparison:  # passing the flags to give output depending on the commandline
    if len(year_num) == 4:
        month_number = 1
        while month_number < 13:
            join_file_format(month_number)
            month_number += 1
    else:
        year_num = int(year_num)
        join_file_format(month_number)
    print("Highest Temperature:", max(max_temp), "C on", print_date_month(max_temp, max(max_temp)))
    print("Lowest Temperature:", min(min_temp), "C on", print_date_month(min_temp, min(min_temp)))
    print("Higest Humid:", max(max_humid), "% on", print_date_month(max_humid, max(max_humid)))

elif argparse.average:  # passing the flags to give output depending on the commandline
    if len(date_month_lst) == 2:
        join_file_format(month_number)
        print("Highest Average:", calculate_average(max_temp), "C")
        print("lowest Average:", calculate_average(min_temp), "C")
        print("Average Humidity:", calculate_average(max_humid), "%")
    else:
        print("invalid entery ;Enter the month number")

elif argparse.Two_bar_graphs :
    if len(date_month_lst) >= 2:
        moth_number = int(date_month_lst[1])
        join_file_format(moth_number)
        print(calendar.month_name[moth_number], year_num)
        for i in range(len(date_list)):
            j = 0
            orignal_1 = datetime.strptime(date_list[i], '%Y-%m-%d')
            temp3 = orignal_1.strftime('%d')
            print(temp3, end="")
            if max_temp[i] != '':
                max_temp[i] = int(max_temp[i])
                while j < max_temp[i]:
                    print(Fore.RED + '+', end="")
                    j += 1
                print(Fore.RESET, j, "C")
                if min_temp[i] != '':
                    print(temp3, end="")
                    min_temp[i] = int(min_temp[i])
                    j = 0
                    while j < min_temp[i]:
                        print(Fore.BLUE + '+', end="")
                        j += 1
                    print(Fore.RESET, j, "C")
                else:
                    print(temp3, end="")
                    print("noo data")
            elif min_temp[i] != '':
                min_temp[i] = int(min_temp[i])
                while j < min_temp[i]:
                    print(Fore.BLUE + '+', end="")
                    j += 1
                print(Fore.RESET, j, "C")
                if max_temp[i] != '':
                    print(temp3, end="")
                    max_temp[i] = int(max_temp[i])
                    j = 0
                    while j < max_temp[i]:
                        print(Fore.RED + '+', end="")
                        j += 1
                    print(Fore.RESET, j, "C")
                else:
                    print(temp3, end="")
                    print("noo data")
            elif min_temp[i] == '':
                print("no data")
                if max_temp[i] == '':
                    print(temp3, end="")
                    print("no data")
    else:
        print("invalid entry ;Enter the month number")
elif argparse.One_bar_graphs:
    if len(date_month_lst) >= 2:
        moth_number = int(date_month_lst[1])
        join_file_format(moth_number)
        print(calendar.month_name[moth_number], year_num)
        for i in range(len(date_list)):
            j = 0
            orignal_1 = datetime.strptime(date_list[i], '%Y-%m-%d')
            temp3 = orignal_1.strftime('%d')
            print(temp3, end="")
            if max_temp[i] != '':
                max_temp[i] = int(max_temp[i])
                while j < max_temp[i]:
                    print(Fore.RED + '+', end="")
                    j += 1
                temp1 = j
                # print(Fore.RESET, j, "C")
                if min_temp[i] != '':
                    min_temp[i] = int(min_temp[i])
                    j = 0
                    while j < min_temp[i]:
                        print(Fore.BLUE + '+', end="")
                        j += 1
                    print(Fore.RESET, temp1, "C - ", j, "C")
                else:
                    print(temp3, end="")
                    print("------no data-----")
            elif min_temp[i] == '':
                if max_temp[i] == '':
                    print("------no data-----")
    else:
        print("invalid entry ;Enter the month number")
else:
    print("Invalid input")
