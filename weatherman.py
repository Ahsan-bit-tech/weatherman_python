from datetime import datetime
import sys
import calendar
from colorama import Fore # for coloring the graph

sample = sys.argv[2].split('/') #to take arguments value from the commandline and slipt the argumets
year_num = int(sample[0]) #take the first index as an year
max_humid_list, min_temp_list, date_list, max_temp_list = [], [], [], [] #assigne 4 empty lists
const = "lahore_weather_2002_jan"
file_name = const.split('_')
month_format = file_name[3]
moth_number = datetime.strptime(month_format, '%b').month

def change_list_into_int(): #change the string values of the list into integer
    global max_humid_list, min_temp_list, max_temp_list
    max_temp_list = list(map(int, max_temp_list)) #map(a,b) It is a function to which map passes each element of given iterable b
    min_temp_list = list(map(int, min_temp_list))
    max_humid_list = list(map(int, max_humid_list))

def delete_empty_space(lst): # if the data doesnot exist then it will not delete the empty data
    empty_spaces = lst.index('')
    lst.remove(lst[empty_spaces])
    return lst

def calculate_average(lst):#function to calculate the average of required list
    total = sum(lst)
    return total//len(lst)

def print_date_month(lst, temp):#to print the name of the month with the date
    check_index_of_lst = lst.index(temp)
    date_format = datetime.strptime(date_list[check_index_of_lst], '%Y-%m-%d')
    temp2 = date_format.strftime('%B %d')
    return temp2
def join_file_format(moth_value): # to change the string into file name like file-->>>file.txt according to the date
        global month_format
        month_format = calendar.month_abbr[moth_value]
        file_name[3] = month_format
        file_name[2] = str(year_num)
        name_file_ = '_'.join(file_name)
        directory = name_file_ + '.txt'
        directory_read(directory)

def directory_read(direct):#this function helps to read the data from required file.txt  and append the data in the lists
    global max_humid_list , min_temp_list , max_temp_list
    with open(direct, 'r') as file:
        line_space = file.readline()
        line_space = file.readline()
        for line in file:
            words = line.split(',')
            if len(words) > 2:
                max_temp_list.append(str(words[1]))
                date_list.append(words[0])
                min_temp_list.append(words[3])
                max_humid_list.append((words[7]))
                if '' in min_temp_list:
                    min_temp_list = delete_empty_space(min_temp_list)
                if '' in max_temp_list:
                    max_temp_list = delete_empty_space(max_temp_list)
                if '' in max_humid_list:
                    max_humid_list = delete_empty_space(max_humid_list)
    file.close()
    return
# -----------------
if sys.argv[1] == '-e': #passing the flags to give output depending on the commandline
    while year_num < int(sample[0]) + 1:
        join_file_format(moth_number)
        if moth_number < 13:
            moth_number += 1
            if moth_number == 13:
                moth_number = 1
                year_num = year_num + 1
    change_list_into_int()
    temp_var = max(max_temp_list)
    print("Highest:", temp_var,"C on", print_date_month(max_temp_list, temp_var))
    temp_var = min(min_temp_list)
    print("Lowest:", temp_var, "C on", print_date_month(min_temp_list, temp_var))
    temp_var = max(max_humid_list)
    print("Higest:", temp_var, "% on", print_date_month(max_humid_list, temp_var))

elif sys.argv[1] == '-a':#passing the flags to give output depending on the commandline
    if len(sample) > 2:
        moth_number = int(sample[1])
        join_file_format(moth_number)
        change_list_into_int()
        print("Highest Average:", calculate_average(max_temp_list), "C")
        print("lowest Average:", calculate_average(min_temp_list), "C")
        print("Average Humidity:", calculate_average(max_humid_list), "%")
    else:
        print("invalid entery ;Enter the month number")

elif sys.argv[1] == '-c' and len(sample[1]) > 1: # passing the flags to give output depending on the commandline
    if len(sample) > 2:
        moth_number = int(sample[1])
        join_file_format(moth_number)
        change_list_into_int()
        print( calendar.month_name[moth_number], year_num)
        for i in range(len(date_list)):
            j = 0
            orignal_1 = datetime.strptime(date_list[i], '%Y-%m-%d')
            temp3 = orignal_1.strftime('%d')
            print(temp3, end="")
            if max_temp_list[i] != '':
                max_temp_list[i] = int(max_temp_list[i])
                while j < max_temp_list[i]:
                    print(Fore.RED + '+', end="")
                    j += 1
                print(Fore.RESET, j, "C")
                if min_temp_list[i] != '':
                    print(temp3, end="")
                    min_temp_list[i] = int(min_temp_list[i])
                    j = 0
                    while j < min_temp_list[i]:
                        print(Fore.BLUE + '+', end="")
                        j += 1
                    print(Fore.RESET, j, "C")
                else:
                    print(temp3, end="")
                    print("noo data")
            elif min_temp_list[i] != '':
                min_temp_list[i] = int(min_temp_list[i])
                while j < min_temp_list[i]:
                    print(Fore.BLUE + '+', end="")
                    j += 1
                print(Fore.RESET, j, "C")
                if max_temp_list[i] != '':
                    print(temp3, end="")
                    max_temp_list[i] = int(max_temp_list[i])
                    j = 0
                    while j < max_temp_list[i]:
                        print(Fore.RED + '+', end="")
                        j += 1
                    print(Fore.RESET, j, "C")
                else:
                    print(temp3, end="")
                    print("noo data")
            elif min_temp_list[i] == '':
                print("no data")
                if max_temp_list[i] == '':
                    print(temp3, end="")
                    print("no data")
    else:
        print("invalid entry ;Enter the month number")
elif sys.argv[1] == '-c' and len(sample[1]) == 1:
    if len(sample) > 2:
        moth_number = int(sample[1])
        join_file_format(moth_number)
        change_list_into_int()
        print(calendar.month_name[moth_number], year_num)
        for i in range(len(date_list)):
            j = 0
            orignal_1 = datetime.strptime(date_list[i], '%Y-%m-%d')
            temp3 = orignal_1.strftime('%d')
            print(temp3, end="")
            if max_temp_list[i] != '':
                max_temp_list[i] = int(max_temp_list[i])
                while j < max_temp_list[i]:
                    print(Fore.RED + '+', end="")
                    j += 1
                temp1 = j
                # print(Fore.RESET, j, "C")
                if min_temp_list[i] != '':
                    min_temp_list[i] = int(min_temp_list[i])
                    j = 0
                    while j < min_temp_list[i]:
                        print(Fore.BLUE + '+', end="")
                        j += 1
                    print(Fore.RESET, temp1, "C - ", j, "C")
                else:
                    print(temp3, end="")
                    print("------no data-----")
            elif min_temp_list[i] == '':
                if max_temp_list[i] == '':
                    print("------no data-----")
    else:
        print("invalid entry ;Enter the month number")

else:
    print("Invalid input")