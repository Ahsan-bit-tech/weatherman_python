from datetime import datetime
import argparse
import calendar
from colorama import Fore


class ReadFile:
    def __init__(self, year_number, file_path):
        self.year_number = year_number
        self.passing_path = file_path
        self.max_humid = 0
        self.min_temp = 100
        self.max_temp = 0
        self.date_of_max_temp = ''
        self.date_of_min_temp = ''
        self.date_of_max_humid = ''

    def year_format(self):
        if len(self.year_number) != 4:
            print(f"This format is wrong {self.year_number}")
            quit()
        return self.year_number

    def year_n_month_format(self):
        date_month_lst = self.year_number.split('/')
        month = int(date_month_lst[1])
        if month >= 13:
            print(f"This format is wrong {self.year_number}")
            quit()
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

    def directory_read(self, file_name, argument_parser):
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
                        if argument_parser.average:
                            sum_max_temp += int(file_argument[1])
                            counter_max_temp += 1
                        elif argument_parser.comparing_data_:
                            if self.max_temp < int(file_argument[1]):
                                self.date_of_max_temp = file_argument[0]
                                self.max_temp = int(file_argument[1])
                    if file_argument[7] != '':
                        if argument_parser.average:
                            sum_max_humid += int(file_argument[7])
                            counter_max_humid += 1
                        elif argument_parser.comparing_data_:
                            if self.max_humid < int(file_argument[7]):
                                self.date_of_max_humid = file_argument[0]
                                self.max_humid = int(file_argument[7])
                    if file_argument[3] != '':
                        if argument_parser.average:
                            sum_min_temp += int(file_argument[3])
                            counter_min_temp += 1
                        elif argument_parser.comparing_data_:
                            if self.min_temp >= int(file_argument[3]):
                                self.date_of_min_temp = file_argument[0]
                                self.min_temp = int(file_argument[3])
        File.close()
        if argument_parser.average:
            avg_max_temp = round(sum_max_temp / counter_max_temp, 2)
            avg_max_humid = round(sum_max_humid / counter_max_humid, 2)
            avg_min_temp = round(sum_min_temp / counter_min_temp, 2)
            print("Highest Average:", avg_max_temp, "C")
            print("lowest Average:", avg_min_temp, "C")
            print("Average Humidity:", avg_max_humid, "%")


def argument_parser_():
    parser = argparse.ArgumentParser(description="Check data from the dataset")
    parser.add_argument('passing_date', help="pass the date as string ", type=str)
    parser.add_argument('passing_path', help="path of the file", type=str)
    parser.add_argument('-e', '--comparison', action="store_true", help="For comparison ")
    parser.add_argument('-a', '--average', action="store_true", help="For calculating average")
    parser.add_argument('-c', '--Two_bar_graphs', help="For plotting graph", action="store_true")
    parser.add_argument('-b', '--One_bar_graphs', help="For plotting graph", action="store_true")
    argument_pass = parser.parse_args()
    return argument_pass


class CompariingDataOfFiles(ReadFile):
    def __init__(self, year_number, file_path):
        super().__init__(year_number, file_path)
        self.year_number = year_number
        self.file_path = file_path

    @staticmethod
    def print_date_month(temp):  # to print the name of the month with the date
        date_format = datetime.strptime(temp, '%Y-%m-%d')
        temp = date_format.strftime('%B %d')
        return temp

    def comparing_data_(self):
        argument_parser = argument_parser_()
        if len(CompariingDataOfFiles.year_format(self)) != 4:
            print(f"Invalid year input {CompariingDataOfFiles.year_format(self.year_number)}")
            quit()
        month_number = 1
        while month_number < 13:
            file_name = CompariingDataOfFiles.pass_month_in_file_name(self, month_number)
            CompariingDataOfFiles.directory_read(self, file_name, argument_parser)
            month_number += 1
        print("Highest temperature:", self.max_temp, "C on", self.print_date_month(self.date_of_max_temp))
        print("Lowest temperature: ", self.min_temp, "C on", self.print_date_month(self.date_of_min_temp))
        print("Highest humid:", self.max_humid, "% on", self.print_date_month(self.date_of_max_humid))


class AverageCalculation(ReadFile):
    def __init__(self, year_number, file_path):
        super().__init__(year_number, file_path)
        self.year_number = year_number
        self.file_path = file_path

    def average_calculation(self):
        file = AverageCalculation.constant_file_name(self)
        AverageCalculation.directory_read(self, file, argument_parser_())


class BarGraph():
    def __init__(self, year_number, file_path):
        self.year_number = year_number
        self.passing_path = file_path

    def file_name(self):
        year_month_lst = ReadFile.year_n_month_format(self)
        month = int(year_month_lst[1])
        year = year_month_lst[0]
        print(calendar.month_name[month], year)
        month_name = calendar.month_abbr[month]
        if self.year_number != '':
            File_name = self.passing_path + "\lahore_weather_" + year + '_' + month_name + '.txt'
            return  File_name

    def generating_bar_graph(self):
        File_name = self.file_name()
        with open(File_name, 'r') as file:
            if file.readline() == '':
                next(file)  # skip the line
            next(file)  # skip the line
            for Line_of_File in file:
                File_arguments = Line_of_File.split(',')
                if len(File_arguments) > 2:
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
                    while graph_index <= min_temp:
                        print(Fore.BLUE + '+', end="")
                        graph_index += 1
                    print(Fore.RESET, graph_index, "C")
        file.close()

    def generating_histogram(self):
        File_name = self.file_name()
        with open(File_name, 'r') as file:
            if file.readline() == '':
                next(file)  # skip the line
            next(file)  # skip the line
            for Line_of_File in file:
                File_arguments = Line_of_File.split(',')
                if len(File_arguments) > 2:
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


def main():
    argument_parser = argument_parser_()

    if argument_parser.comparison:  # passing the flags to give output depending on the commandline
        instance_object = CompariingDataOfFiles(argument_parser.passing_date, argument_parser.passing_path)
        instance_object.comparing_data_()

    elif argument_parser.average:  # passing the flags to give output depending on the commandline
        instance_object = AverageCalculation(argument_parser.passing_date, argument_parser.passing_path)
        instance_object.average_calculation()

    elif argument_parser.Two_bar_graphs:
        instance_object = BarGraph(argument_parser.passing_date, argument_parser.passing_path)
        instance_object.generating_bar_graph()

    elif argument_parser.One_bar_graphs:
        instance_object = BarGraph(argument_parser.passing_date, argument_parser.passing_path)
        instance_object.generating_histogram()


if __name__ == "__main__":
    main()
