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
            
        elif "N" not in sample[0]:
            print("Line data is invalid, because data not contain N\n")
            print(sample, '\n')
            return False

        return True
            
#file_name = str(input("Enter a file name you want to statitic (i.e class1.txt): "))
score_calculator = TestGradeCalculator("class2")
score_calculator.read_file()
