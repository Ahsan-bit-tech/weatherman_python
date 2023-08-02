from datetime import datetime
import argparse
import calendar
from colorama import Fore
import csv
import os


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

    @staticmethod
    def date_format_validity(pass_date):
        date_format = "%Y-%m-%d"
        res = True
        try:
            bool(datetime.strptime(pass_date, date_format))
            return res
        except ValueError:
            return False

    def compare_minmax_n_average(self, read_file_in_Dict, temp, pass_flag_argument):
        if self.date_format_validity(temp) and read_file_in_Dict['Max TemperatureC'] != '' and read_file_in_Dict['Max Humidity'] != '' and read_file_in_Dict['Min TemperatureC'] != '':
            if pass_flag_argument.average:
                self.sum_max_temp += int(read_file_in_Dict['Max TemperatureC'])
                self.counter_max_temp += 1
                self.sum_max_humid += int(read_file_in_Dict['Max Humidity'])
                self.counter_max_humid += 1
                self.sum_min_temp += int(read_file_in_Dict['Min TemperatureC'])
                self.counter_min_temp += 1
                self.avg_min_temp = self.sum_min_temp / self.counter_min_temp
                self.avg_max_temp = self.sum_max_temp / self.counter_max_temp
                self.avg_max_humid = self.sum_max_humid / self.counter_max_humid
            elif pass_flag_argument.compare_min_max:
                if self.max_temp < int(read_file_in_Dict['Max TemperatureC']):
                    self.date_of_max_temp = temp
                    self.max_temp = int(read_file_in_Dict['Max TemperatureC'])
                if self.max_humid < int(read_file_in_Dict['Max Humidity']):
                    self.date_of_max_humid = temp
                    self.max_humid = int(read_file_in_Dict['Max Humidity'])
                if self.min_temp >= int(read_file_in_Dict['Min TemperatureC']):
                    self.date_of_min_temp = temp
                    self.min_temp = int(read_file_in_Dict['Min TemperatureC'])

    def directory_read(self, file_name):
        pass_flag_argument = add_flag_argument_()
        with open(file_name, 'r') as in_file:
            stripped = (line.strip() for line in in_file)
            lines = (line.split(",") for line in stripped if line)
            file_name = file_name.split('.')
            file_name[1] = "csv"
            file_name = '.'.join(file_name)
            with open(file_name, 'w') as out_file:
                writer = csv.writer(out_file)
                writer.writerows(lines)
            with open(file_name, 'r') as out_file:
                csvreader = csv.DictReader(out_file)
                for read_file_in_Dict in csvreader:
                    if "PKT" in read_file_in_Dict:
                        self.compare_minmax_n_average(read_file_in_Dict, read_file_in_Dict["PKT"], pass_flag_argument)
                    elif "PKST" in read_file_in_Dict:
                        self.compare_minmax_n_average(read_file_in_Dict, read_file_in_Dict["PKST"], pass_flag_argument)
            out_file.close()
        os.remove(file_name)
        in_file.close()


def add_flag_argument_():
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
        self.sum_max_temp = 0
        self.sum_min_temp = 0
        self.sum_max_humid = 0
        self.counter_max_temp = 0
        self.counter_min_temp = 0
        self.counter_max_humid = 0
        self.avg_max_temp = 0
        self.avg_min_temp = 0
        self.avg_max_humid = 0

    @staticmethod
    def print_date_month(temp):  # to print the name of the month with the date
        date_format = datetime.strptime(temp, '%Y-%m-%d')
        temp = date_format.strftime('%B %d')
        return temp

    def compare_min_max(self):
        if len(MinMax.year_format(self)) != 4:
            print(f"Invalid year input {MinMax.year_format(self.year_number)}")
            quit()
        month_number = 1
        while month_number < 13:
            file_name = MinMax.pass_month_in_file_name(self, month_number)
            MinMax.directory_read(self, file_name)
            month_number += 1
        print("Highest temperature:", self.max_temp, "C on", self.print_date_month(self.date_of_max_temp))
        print("Lowest temperature: ", self.min_temp, "C on", self.print_date_month(self.date_of_min_temp))
        print("Highest humid:", self.max_humid, "% on", self.print_date_month(self.date_of_max_humid))

    def calculate_average(self):
        file_name = self.constant_file_name()
        self.directory_read(file_name)
        print("Highest Average:", round(self.avg_max_temp, 2), "C")
        print("lowest Average:", round(self.avg_min_temp, 2), "C")
        print("Average Humidity:", round(self.avg_max_humid, 2), "%")


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
        graph_index = 1
        while graph_index <= limit:
            print(Fore.RED + '+', end="")
            graph_index += 1

    @staticmethod
    def print_blue_lines(limit):
        graph_index = 1
        while graph_index <= limit:
            print(Fore.BLUE + '+', end="")
            graph_index += 1

    def print_date_n_graph(self, temp, max_temp=None, min_temp=None):
        flag_argument = add_flag_argument_()
        date_of_max_temp = datetime.strptime(temp, '%Y-%m-%d')
        print_dates = int(date_of_max_temp.strftime('%d'))
        print(print_dates, end='')
        if max_temp != None and min_temp != None:
            if flag_argument.Two_bar_graphs:
                self.print_red_lines(max_temp)
                print(Fore.RESET, max_temp, "C")
                print(print_dates, end='')
                self.print_blue_lines(min_temp)
                print(Fore.RESET, min_temp, "C")
            elif flag_argument.One_bar_graphs:
                self.print_red_lines(max_temp)
                self.print_blue_lines(min_temp)
                print(Fore.RESET, max_temp, "C - ", min_temp, "c")

    def generate_bar_graph(self):
        file_name = self.generate_file_name()
        with open(file_name, 'r') as in_file:
            stripped = (line.strip() for line in in_file)
            lines = (line.split(",") for line in stripped if line)
            file_name = file_name.split('.')
            file_name[1] = "csv"
            file_name = '.'.join(file_name)
            with open(file_name, 'w') as out_file:
                writer = csv.writer(out_file)
                writer.writerows(lines)
            with open(file_name, 'r') as out_file:
                csvreader = csv.DictReader(out_file)
                for read_file_in_Dict in csvreader:
                    if "PKT" in read_file_in_Dict:
                        if ReadFile.date_format_validity(read_file_in_Dict["PKT"]) and read_file_in_Dict['Max TemperatureC'] != '' and read_file_in_Dict['Min TemperatureC'] != '':
                            self.print_date_n_graph(read_file_in_Dict["PKT"],
                                                    int(read_file_in_Dict['Max TemperatureC']),
                                                    int(read_file_in_Dict['Min TemperatureC']))
                        elif ReadFile.date_format_validity(read_file_in_Dict["PKT"]):
                            self.print_date_n_graph(read_file_in_Dict["PKT"])
                            print("-->no data")
                    elif "PKST" in read_file_in_Dict:
                        if ReadFile.date_format_validity(read_file_in_Dict["PKST"]) and read_file_in_Dict['Max TemperatureC'] != '' and read_file_in_Dict['Min TemperatureC'] != '':
                            self.print_date_n_graph(read_file_in_Dict["PKST"],
                                                    int(read_file_in_Dict['Max TemperatureC']),
                                                    int(read_file_in_Dict['Min TemperatureC']))
                        elif ReadFile.date_format_validity(read_file_in_Dict["PKST"]):
                            self.print_date_n_graph(read_file_in_Dict["PKST"])
                            print("-->no data")
            out_file.close()
        os.remove(file_name)
        in_file.close()


def main():
    argument_parser = add_flag_argument_()

    if argument_parser.compare_min_max:  # passing the flags to give output depending on the commandline
        class_object = MinMax(argument_parser.passing_date, argument_parser.passing_path)
        class_object.compare_min_max()

    elif argument_parser.average:  # passing the flags to give output depending on the commandline
        class_object = MinMax(argument_parser.passing_date, argument_parser.passing_path)
        class_object.calculate_average()

    elif argument_parser.Two_bar_graphs or argument_parser.One_bar_graphs:
        class_object = BarGraph(argument_parser.passing_date, argument_parser.passing_path)
        class_object.generate_bar_graph()


if __name__ == "__main__":
    main()
