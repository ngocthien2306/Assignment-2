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
            
#file_name = str(input("Enter a file name you want to statitic (i.e class1.txt): "))
score_calculator = TestGradeCalculator("class2")
score_calculator.read_file()
