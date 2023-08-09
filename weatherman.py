from datetime import datetime
import argparse
import calendar
from colorama import Fore
import csv

class ReadFile:
    def __init__(self, year_number, file_path):
        self.year_number = year_number
        self.passing_path = file_path
        self.max_parameter3 = 0
        self.min_parameter2 = 100
        self.max_parameter1 = 0
        self.date_of_parameter1 = ''
        self.date_of_parameter2 = ''
        self.date_of_parameter3 = ''

    def year_format(self):
        if len(self.year_number) != 4:
            raise TypeError(f"the type {self.year_number} is wrong . the digits should be 0000 format")
        return self.year_number

    def year_n_month_format(self):
        date_month_lst = self.year_number.split('/')
        month = int(date_month_lst[1])
        if month >= 13:
            raise TypeError(f"the type {self.year_number} is wrong")
        return date_month_lst

    def pass_month_in_file_name(self, month_number):
        month_value = int(month_number)
        year = self.year_format()
        Month_Name = calendar.month_abbr[month_value]
        return self.passing_path + "\lahore_weather_" + year + '_' + Month_Name + '.txt'

    def constant_file_name(self):
        year_month = self.year_n_month_format()
        year = year_month[0]
        month = int(year_month[1])
        Month_Name = calendar.month_abbr[month]
        return self.passing_path + "\lahore_weather_" + year + '_' + Month_Name + '.txt'

    @staticmethod
    def date_format_validity(pass_date):
        date_format = "%Y-%m-%d"
        res = True
        try:
            bool(datetime.strptime(pass_date, date_format))
            return res
        except ValueError:
            return False

    def compare_minmax(self, date_parameter, parameter1, parameter2, parameter3):
        if self.date_format_validity(date_parameter) and parameter1 != '' and parameter3 != '' and parameter2 != '':
            if self.max_parameter1 < int(parameter1):
                self.date_of_parameter1 = date_parameter
                self.max_parameter1 = int(parameter1)
            if self.max_parameter3 < int(parameter3):
                self.date_of_parameter3 = date_parameter
                self.max_parameter3 = int(parameter3)
            if self.min_parameter2 >= int(parameter2):
                self.date_of_parameter2 = date_parameter
                self.min_parameter2 = int(parameter2)

    def compare_average(self, date_paramter, parameter1, parameter2, parameter3):
        if self.date_format_validity(date_paramter) and parameter1 != '' and parameter3 != '' and parameter2 != '':
            self.sum_parameter1 += int(parameter1)
            self.count_parameter1 += 1
            self.sum_parameter2 += int(parameter2)
            self.count_parameter2 += 1
            self.sum_parameter3 += int(parameter3)
            self.count_parameter3 += 1
            self.avg_parameter1 = self.sum_parameter1 / self.count_parameter1
            self.avg_parameter2 = self.sum_parameter2 / self.count_parameter2
            self.avg_parameter3 = self.sum_parameter3 / self.count_parameter3

    def directory_read(self, file_name):
        pass_flag_argument = add_flag_argument()
        with open(file_name, 'r') as csvfile:
            if csvfile.readline() == '':
                next(csvfile)
            csvreader = csv.DictReader(csvfile)
            for read_file_in_Dict in csvreader:
                if "PKT" in read_file_in_Dict:
                    if pass_flag_argument.compare_min_max:
                        self.compare_minmax(read_file_in_Dict["PKT"], read_file_in_Dict["Max TemperatureC"], read_file_in_Dict["Min TemperatureC"], read_file_in_Dict["Max Humidity"])
                    elif pass_flag_argument.average:
                        self.compare_average(read_file_in_Dict["PKT"],read_file_in_Dict["Max TemperatureC"],read_file_in_Dict["Min TemperatureC"],read_file_in_Dict["Max Humidity"])
                elif "PKST" in read_file_in_Dict:
                    if pass_flag_argument.compare_min_max:
                        self.compare_minmax(read_file_in_Dict["PKST"], read_file_in_Dict["Max TemperatureC"], read_file_in_Dict["Min TemperatureC"], read_file_in_Dict["Max Humidity"])
                    elif pass_flag_argument.average:
                        self.compare_average(read_file_in_Dict["PKST"],read_file_in_Dict["Max TemperatureC"],read_file_in_Dict["Min TemperatureC"],read_file_in_Dict["Max Humidity"])
        csvfile.close()


def add_flag_argument():
    parser = argparse.ArgumentParser(description="Check data from the dataset")
    parser.add_argument('passing_date', help="pass the date as string ", type=str)
    parser.add_argument('passing_path', help="path of the file", type=str)
    parser.add_argument('-e', '--compare_min_max', action="store_true", help="For comparison ")
    parser.add_argument('-a', '--average', action="store_true", help="For calculating average")
    parser.add_argument('-c', '--Two_bar_graphs', help="For plotting graph", action="store_true")
    parser.add_argument('-b', '--One_bar_graphs', help="For plotting graph", action="store_true")
    argument_pass = parser.parse_args()
    return argument_pass


class MinMax(ReadFile):

    def __init__(self, year_number, file_path):
        super().__init__(year_number, file_path)
        self.year_number = year_number
        self.file_path = file_path
        self.sum_parameter1 = 0
        self.sum_parameter2 = 0
        self.sum_parameter3 = 0
        self.count_parameter1 = 0
        self.count_parameter2 = 0
        self.count_parameter3 = 0
        self.avg_parameter1 = 0
        self.avg_parameter2 = 0
        self.avg_parameter3 = 0

    @staticmethod
    def print_date_month(date_format):  # to print the name of the month with the date
        date_format = datetime.strptime(date_format, '%Y-%m-%d')
        date_format = date_format.strftime('%B %d')
        return date_format

    def generate_min_max(self):
        month_number = 1
        while month_number < 13:
            file_name = MinMax.pass_month_in_file_name(self, month_number)
            MinMax.directory_read(self, file_name)
            month_number += 1
        print("Highest temperature:", self.max_parameter1, "C on", self.print_date_month(self.date_of_parameter1))
        print("Lowest temperature: ", self.min_parameter2, "C on", self.print_date_month(self.date_of_parameter2))
        print("Highest humid:", self.max_parameter3, "% on", self.print_date_month(self.date_of_parameter3))

    def calculate_average(self):
        file_name = self.constant_file_name()
        self.directory_read(file_name)
        print("Highest Average:", round(self.avg_parameter1, 2), "C")
        print("lowest Average:", round(self.avg_parameter2, 2), "C")
        print("Average Humidity:", round(self.avg_parameter3, 2), "%")


class BarGraph:
    def __init__(self, year_number, file_path):
        self.year_number = year_number
        self.passing_path = file_path

    def generate_file_name(self):
        year_month_lst = ReadFile.year_n_month_format(self)
        month = int(year_month_lst[1])
        year = year_month_lst[0]
        print(calendar.month_name[month], year)
        month_name = calendar.month_abbr[month]
        if self.year_number != '':
            File_name = self.passing_path + "\lahore_weather_" + year + '_' + month_name + '.txt'
            return File_name

    @staticmethod
    def print_red_lines(limit):
        limit = int(limit)
        graph_index = 1
        while graph_index <= limit:
            print(Fore.RED + '+', end="")
            graph_index += 1

    @staticmethod
    def print_blue_lines(limit):
        limit = int(limit)
        graph_index = 1
        while graph_index <= limit:
            print(Fore.BLUE + '+', end="")
            graph_index += 1

    def print_date_n_graph(self, date_format, parameter1, parameter2):
        flag_argument = add_flag_argument()
        date_parameter = datetime.strptime(date_format, '%Y-%m-%d')
        print_dates = int(date_parameter.strftime('%d'))
        print(print_dates, end='')
        if flag_argument.Two_bar_graphs:
            if parameter1 != '' and parameter2 != '':
                self.print_red_lines(parameter1)
                print(Fore.RESET, parameter1, "C")
                print(print_dates, end='')
                self.print_blue_lines(parameter2)
                print(Fore.RESET, parameter2, "C")
            else:
                print("-->no data")
                print(print_dates, end='')
                print("-->no data")
        elif flag_argument.One_bar_graphs:
            if parameter1 != '' and parameter2 != '':
                self.print_red_lines(parameter1)
                self.print_blue_lines(parameter2)
                print(Fore.RESET, parameter1, "C - ", parameter2, "c")
            else:
                print("-->no data")


    def generate_bar_graph(self):
        file_name = self.generate_file_name()
        with open(file_name, 'r') as csvfile:
            if csvfile.readline() == '':
                next(csvfile)
            csvreader = csv.DictReader(csvfile)
            for read_file_in_Dict in csvreader:
                if "PKT" in read_file_in_Dict and ReadFile.date_format_validity(read_file_in_Dict["PKT"]):
                    self.print_date_n_graph(read_file_in_Dict["PKT"],read_file_in_Dict['Max TemperatureC'],read_file_in_Dict['Min TemperatureC'])
                elif "PKST" in read_file_in_Dict and ReadFile.date_format_validity(read_file_in_Dict["PKST"]) :
                    self.print_date_n_graph(read_file_in_Dict["PKST"],read_file_in_Dict['Max TemperatureC'],read_file_in_Dict['Min TemperatureC'])



def main():
    pass_argument = add_flag_argument()

    if pass_argument.compare_min_max:  # passing the flags to give output depending on the commandline
        class_object = MinMax(pass_argument.passing_date, pass_argument.passing_path)
        class_object.generate_min_max()

    elif pass_argument.average:  # passing the flags to give output depending on the commandline
        class_object = MinMax(pass_argument.passing_date, pass_argument.passing_path)
        class_object.calculate_average()

    elif pass_argument.Two_bar_graphs or pass_argument.One_bar_graphs:
        class_object = BarGraph(pass_argument.passing_date, pass_argument.passing_path)
        class_object.generate_bar_graph()


if __name__ == "__main__":
    main()
