import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import re

class TestGradeCalculator():
    def __init__(self, filename=None):
        self.filename = filename 
        self.data_from_file = None
        self.total_sample = 0
        self.arr_student = None
        self.arr_invalid_student = None
        self.correct_answer = None
        self.dataFrame_student = None
        
    def read_file(self):
        try:
            with open(self.filename + '.txt') as file:
                print("\nOpen {} successful! \n".format(self.filename))
                self.data_from_file = file.readlines()
                
        except:
            print("Can not open file, please check file name or file format \n")
            
    def validate_length_answer(self, sample):
        sample = np.array(sample)
        if sample.shape[0] > 26:
            print('Line data is invalid, because length of this line = {} larger than 26 \n'.format(sample.shape[0]))
            print(sample, '\n')
            return False

        elif sample.shape[0] < 26:
            print('Line data is invalid, because length of this line = {} lesser than 26 \n'.format(sample.shape[0]))
            print(sample, '\n')
            return False

        return True

    def validate_student_id(self, sample):
        sample = np.array(sample)
        if sample[0][0] == "N":
            if len(str(sample[0])) > 9:
                print("Line data is invalid, because length of student id = {} larger than 9 \n".format(len(str(sample[0]))))
                print(sample, '\n')
                return False

            elif len(str(sample[0])) < 9:
                print("Line data is invalid, because length of student id = {} lesser than 9 \n".format(len(str(sample[0]))))
                print(sample, '\n')
                return False
            
           # check the amount of character after N
            elif any(c.isalpha() for c in sample[0][1:]):
                print("Line data is invalid: N# incorrect format \n")
                print(sample, '\n')
                return False
            
        elif "N" not in sample[0]:
            print("Line data is invalid, because data not contain N\n")
            print(sample, '\n')
            return False

        return True
    
    # check invalid line
    def check_format(self):
        self.count_total_sample()
        count_invalid = 0
        # valid line 
        arr_student = []
        # invalid line
        arr_invalid_student = []

        for i in self.data_from_file:
            # separate string by ","
            sample = i.split(",")
            check_length = self.validate_length_answer(sample)
            check_student_id = self.validate_student_id(sample)

            if check_length and check_student_id:
                sample[25] = re.sub("\n", '', sample[25])
                # add line data to list valid student
                arr_student.append(sample)
            else:
                # add line data to list invalid student
                arr_invalid_student.append(sample)
                count_invalid += 1

        print("**** REPORT ****\n")
        print("Total valid lines of data: {} \n".format(self.total_sample - count_invalid))
        print("Total invalid lines of data: {} \n".format(count_invalid))

        self.arr_student = arr_student
        self.arr_invalid_student = arr_invalid_student
    
        return count_invalid
    
    
    # convert '' to NAN 
    def processing_data(self):
        for i in range(len(self.arr_student)):
            for j in range(len(self.arr_student[i])):
                if self.arr_student[i][j] == '':
                    self.arr_student[i][j] = np.NAN
            
#file_name = str(input("Enter a file name you want to statitic (i.e class1.txt): "))
score_calculator = TestGradeCalculator("class2")
score_calculator.read_file()
count_invalid = score_calculator.check_format()
print("**** ANALYZING ****\n")
if count_invalid == 0:
    print("No errors found!\n")
else:
    print("Some lines are invalid\n")
