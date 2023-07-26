from datetime import datetime
import argparse
import calendar
from colorama import Fore


def split_month_year():
    year_num = argparse.passing_date
    if len(year_num) > 4:
        date_month_lst = year_num.split('/')  # to take arguments value from the commandline and split the arguments
        if date_month_lst[1] != '' and int(date_month_lst[1]) < 13:
            return date_month_lst
        else:
            print(f"This format is wrong {year_num}")
            quit()
    else:
        return year_num


def print_date_month(temp):  # to print the name of the month with the date
    date_format = datetime.strptime(temp, '%Y-%m-%d')
    temp = date_format.strftime('%B %d')
    return temp


def join_file_format(month_value):  # to change the string into file name like file-->>>file.txt according to the date
    Month_Name = calendar.month_abbr[month_value]
    if argparse.passing_path != '':
        if len(split_month_year()) == 4:
            return argparse.passing_path + "\lahore_weather_" + split_month_year() + '_' + Month_Name + '.txt'
        else:
            date_lst = split_month_year()
            return argparse.passing_path + "\lahore_weather_" + date_lst[0] + '_' + Month_Name + '.txt'
    else:
        print("File path is not defined")
        quit()


def directory_read(file_name, min_temp = None, max_temp= None, max_humid=None, date_of_max_humid= None, date_of_max_temp= None, date_of_min_temp= None):
    sum_max_temp = sum_min_temp = sum_max_humid = 0
    counter_max_temp = counter_min_temp = counter_max_humid = 0
    with open(file_name, 'r') as File:
        if File.readline() == '':
            next(File)  # skip the line
        next(File)  # skip the line
        for Line in File:
            file_argument = Line.split(',')
            if len(file_argument) > 2:
                if file_argument[1] != '':
                    if argparse.average:
                        sum_max_temp += int(file_argument[1])
                        counter_max_temp += 1
                    elif argparse.comparison:
                        if max_temp < int(file_argument[1]):
                            date_of_max_temp = file_argument[0]
                            max_temp = int(file_argument[1])
                if file_argument[7] != '':
                    if argparse.average:
                        sum_max_humid += int(file_argument[7])
                        counter_max_humid += 1
                    elif argparse.comparison:
                        if max_humid < int(file_argument[7]):
                            date_of_max_humid = file_argument[0]
                            max_humid = int(file_argument[7])
                if file_argument[3] != '':
                    if argparse.average:
                        sum_min_temp += int(file_argument[3])
                        counter_min_temp += 1
                    elif argparse.comparison:
                        if min_temp >= int(file_argument[3]):
                            date_of_min_temp = file_argument[0]
                            min_temp = int(file_argument[3])
    File.close()

    if argparse.average:
        avg_max_temp = round(sum_max_temp / counter_max_temp, 2)
        avg_max_humid = round(sum_max_humid / counter_max_humid, 2)
        avg_min_temp = round(sum_min_temp / counter_min_temp, 2)
        print("Highest Average:", avg_max_temp, "C")
        print("lowest Average:", avg_min_temp, "C")
        print("Average Humidity:", avg_max_humid, "%")
    elif argparse.comparison:
        return max_temp,min_temp,max_humid , date_of_max_temp,date_of_min_temp,date_of_max_humid


def main():
    max_humid, min_temp, max_temp = 0, 100, 0
    date_of_max_temp = date_of_min_temp = date_of_max_humid = ''
    if argparse.comparison:  # passing the flags to give output depending on the commandline
        if len(split_month_year()) == 4:
            month_number = 1
            while month_number < 13:
                a = join_file_format(month_number)
                max_temp ,min_temp,max_humid,date_of_max_temp,date_of_min_temp,date_of_max_humid = directory_read(a,min_temp,max_temp,max_humid,date_of_max_humid,date_of_max_temp,date_of_min_temp)
                month_number += 1
        else:
            print(f"Invalid year input {split_month_year()}")
            quit()
        print("Highest temperature:", max_temp, "C on", print_date_month(date_of_max_temp))
        print("Lowest temperature: ", min_temp, "C on", print_date_month(date_of_min_temp))
        print("Highest humid:", max_humid, "% on", print_date_month(date_of_max_humid))

    elif argparse.average:  # passing the flags to give output depending on the commandline
        if len(split_month_year()) == 2:
            lst = split_month_year()
            file = join_file_format(int(lst[1]))
            directory_read(file)
        else:
            print(f"The date format {split_month_year()} is not correct")

    elif argparse.Two_bar_graphs or argparse.One_bar_graphs:  # passing the flags to give output depending on the commandline
        month_lst = split_month_year()
        month_number = int(month_lst[1])
        print(calendar.month_name[month_number], month_lst[0])
        month_format = calendar.month_abbr[month_number]
        if argparse.passing_path != '':
            File_name = argparse.passing_path + "\lahore_weather_" + month_lst[0] + '_' + month_format + '.txt'
            with open(File_name, 'r') as file:
                if file.readline() == '':
                    next(file)  # skip the line
                next(file)  # skip the line
                for Line_of_File in file:
                    File_arguments = Line_of_File.split(',')
                    if len(File_arguments) > 2:
                        if argparse.Two_bar_graphs:
                            date_of_max_temp = datetime.strptime(File_arguments[0], '%Y-%m-%d')
                            print_dates = int(date_of_max_temp.strftime('%d'))
                            print(print_dates, end='')
                            max_temp = int(File_arguments[1])
                            min_temp = int(File_arguments[3])
                            graph_index = 1
                            while graph_index <= max_temp:
                                print(Fore.RED + '+', end="")
                                graph_index += 1
                            print(Fore.RESET, graph_index, "C")
                            print(print_dates, end='')
                            graph_index = 1
                            while graph_index <= max_temp:
                                print(Fore.BLUE + '+', end="")
                                graph_index += 1
                            print(Fore.RESET, graph_index, "C")
                        elif argparse.One_bar_graphs:
                            date_of_max_temp = datetime.strptime(File_arguments[0], '%Y-%m-%d')
                            print_dates = int(date_of_max_temp.strftime('%d'))
                            print(print_dates, end='')
                            max_temp = int(File_arguments[1])
                            min_temp = int(File_arguments[3])
                            graph_index = 1
                            while graph_index <= max_temp:
                                print(Fore.RED + '+', end="")
                                graph_index += 1
                            graph_index = 1
                            while graph_index <= min_temp:
                                print(Fore.BLUE + '+', end="")
                                graph_index += 1
                            print(Fore.RESET, max_temp, "C - ", min_temp, "c")
            file.close()


if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Check data from the dataset")
    parser.add_argument('passing_date', help="pass the date as string ", type=str)
    parser.add_argument('passing_path', help="path of the file", type=str)
    parser.add_argument('-e', '--comparison', action="store_true", help="For comparison ")
    parser.add_argument('-a', '--average', action="store_true", help="For calculating average")
    parser.add_argument('-c', '--Two_bar_graphs', help="For plotting graph", action="store_true")
    parser.add_argument('-b', '--One_bar_graphs', help="For plotting graph", action="store_true")
    argparse = parser.parse_args()
    main()
