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
                    
    # grading exams for each student, except for student invalid
    def calculating_score(self, correct_answer):
        self.correct_answer = correct_answer
        arr_correct_answer = np.array(correct_answer.split(','))
        scores = []
        for answers in self.arr_student:
            answers = answers[1:]
            score = 0
            for i in range(len(answers)):
                if answers[i] == arr_correct_answer[i]:
                    score += 4
                elif answers[i] == '':
                    pass
                else:
                    score -= 1
            scores.append(score)
        self.processing_data()

        # create DataFrame to analysis 
        list_student = pd.DataFrame(self.arr_student)
        list_student["score"] = scores
        self.dataFrame_student = list_student
        return list_student
    
    # print the question that most people skip
    def most_question_skip(self, new_dataFrame):
        
        # count the number of question that student skip
        n_missing_value = new_dataFrame.isna().sum()
        # count the number of question that student answered 
        n_not_missing_value = new_dataFrame.notna().sum()
        # calculating percentage of question skip
        percent_missing_value = (n_missing_value / n_not_missing_value )*100
        # create skip question DataFrame
        missing_data = pd.concat([n_missing_value, percent_missing_value], keys=['Null Count','Null Percentage'], axis=1)
      
        show_graph = str(input("Show statistic the question that most people skip (y or n):"))
        # visualize data
        if show_graph == "y":
            plt.figure(figsize=(12, 7))
            missing_data["Null Count"].plot(kind="bar")
            plt.title("List answer skip: " + str(self.filename))
            plt.ylabel("n_missing")
            plt.xlabel("question")
            plt.savefig("Images/" + self.filename + '_skip.png')
            plt.show()

        max_question_skip = max(n_missing_value)
        list_question_skip = ""
        
        for i in range(1, len(n_missing_value) - 1):
            if n_missing_value[i] == max_question_skip:
                list_question_skip += str(i) + " - " + str(max_question_skip) + " - " + str((max_question_skip/25)) + ' , '

        print("The question that most people skip: ", list_question_skip +'\n')

    # print question that most student answer incorrectly
    def most_question_incorrect(self, new_dataFrame):
        n_missing_value = new_dataFrame.isna().sum()
        check_question = ((new_dataFrame != np.array(self.correct_answer.split(",")))).sum()
        n_question_correct = ((new_dataFrame == np.array(self.correct_answer.split(",")))).sum()
        n_question_incorect = check_question - n_missing_value

        list_question = pd.concat([n_question_correct, n_question_incorect], keys=['Correct Count','Incorrect Count'], axis=1)


        # visualize data
        show_graph = str(input("Show statistic the question that most people skip (y or n):"))
        if show_graph == "y":
            plt.figure(figsize=(12, 7))
            list_question["Correct Count"].plot(kind="bar")
            plt.title("The number of question correct: " + str(self.filename))
            plt.ylabel("n_correct")
            plt.xlabel("question")
            plt.savefig("Images/" + self.filename + '_correct.png')
            plt.show()

        max_question_incorrect = max(n_question_incorect)
        list_question_incorrect = ""
        for i in range(1, len(n_question_incorect) - 1):
            if n_question_incorect[i] == max_question_incorrect:
                list_question_incorrect += str(i) + " - " + str(max_question_incorrect) + " - " + str((max_question_incorrect/25)) + ' , '
        print("The question that most people answer incorrectly:", list_question_incorrect + "\n")
            
#file_name = str(input("Enter a file name you want to statitic (i.e class1.txt): "))
score_calculator = TestGradeCalculator("class2")
score_calculator.read_file()
count_invalid = score_calculator.check_format()
print("**** ANALYZING ****\n")
if count_invalid == 0:
    print("No errors found!\n")
else:
    print("Some lines are invalid\n")
answer_key = "B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D"
score_calculator.calculating_score(answer_key)
