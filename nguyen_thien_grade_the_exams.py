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
        self.total_valid = 0
    
    # open file
    def read_file(self):
        try:
            with open(self.filename + '.txt', 'r') as file:
                print("\nOpen {} successful! \n".format(self.filename))
                self.data_from_file = file.readlines()       
        except:
            print("Can not open file, please check file name or file format \n")

    # count the number of line in file
    def count_total_sample(self):
        # convert all line to array
        self.total_sample = np.array(self.data_from_file).size
        return self.total_sample

    # check length 
    def validate_length_answer(self, sample):
        try:
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
        except:
            print("Error Validate Length Answer! (tip: check data format) \n")

    # check student id
    def validate_student_id(self, sample):
        try:
            sample = np.array(sample)
            """
                A valid line containing a list of 26 comma-separated values
                N# for a student is the first item on the line. 
                It must contain the character “N” followed by 8 numeric characters.
            """
            # check student id contain N or not
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
        except:
            print("Error Validate Student ID! (tip: check data format) \n")

    # check invalid line
    def check_format(self):
        try:
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

            self.arr_student = arr_student
            self.arr_invalid_student = arr_invalid_student
            self.total_valid = self.total_sample - count_invalid

            print("**** REPORT ****\n")
            print("Total valid lines of data: {} \n".format(self.total_valid))
            print("Total invalid lines of data: {} \n".format(count_invalid))

            return count_invalid
        except:
            print("Error System, please check check_format() function \n")

    # convert '' to NAN 
    def processing_data(self):
        for i in range(len(self.arr_student)):
            for j in range(len(self.arr_student[i])):
                if self.arr_student[i][j] == '':
                    self.arr_student[i][j] = np.NAN
                
    # grading exams for each student, except for student invalid
    def calculating_score(self, correct_answer):
        try:
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

            # create DataFrame to analysis data more convenience 
            list_student = pd.DataFrame(self.arr_student)
            list_student["score"] = scores
            self.dataFrame_student = list_student
            return list_student
        except:
            print("Error System, please check calculating_score() function \n")

    
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
      
        show_graph = 'y' # str(input("Show statistic the question that most people skip (y or n):"))
        # visualize data
        if show_graph == "y":
            plt.figure(figsize=(12, 7))
            missing_data["Null Count"].plot(kind="bar")
            plt.title("List answer skip: " + str(self.filename))
            plt.ylabel("n_missing")
            plt.xlabel("question")
            plt.savefig("Images/" + self.filename + '_skip.png')
            plt.show()

        #get highest skip question 
        max_question_skip = max(n_missing_value)
        list_question_skip = ""
        
        for i in range(1, len(n_missing_value) - 1):
            if n_missing_value[i] == max_question_skip:
                rate = max_question_skip/self.total_valid
                list_question_skip += str(i) + " - " + str(max_question_skip) + " - {:.2f}".format(rate)  + ' , '

        print("The question that most people skip: ", list_question_skip +'\n')

    # print question that most student answer incorrectly
    def most_question_incorrect(self, new_dataFrame):
        n_missing_value = new_dataFrame.isna().sum()
        check_question = ((new_dataFrame != np.array(self.correct_answer.split(",")))).sum()
        n_question_correct = ((new_dataFrame == np.array(self.correct_answer.split(",")))).sum()
        n_question_incorect = check_question - n_missing_value

        list_question = pd.concat([n_question_correct, n_question_incorect], keys=['Correct Count','Incorrect Count'], axis=1)


        # visualize data
        show_graph = 'y' #str(input("Show statistic the question that most people skip (y or n):"))
        if show_graph == "y":
            plt.figure(figsize=(12, 7))
            list_question["Correct Count"].plot(kind="bar")
            plt.title("The number of question correct: " + str(self.filename))
            plt.ylabel("n_correct")
            plt.xlabel("question")
            plt.savefig("Images/" + self.filename + '_correct.png')
            plt.show()

        # get highest incorrect question 
        max_question_incorrect = max(n_question_incorect)
        list_question_incorrect = ""
        for i in range(1, len(n_question_incorect) - 1):
            if n_question_incorect[i] == max_question_incorrect:
                
                rate = (max_question_incorrect/self.total_valid)
                # set line data incorrect
                list_question_incorrect += str(i) + " - " + str(max_question_incorrect) + " - {:.2f}".format(rate) + " , "
        print("\nThe question that most people answer incorrectly:", list_question_incorrect + "\n")
   
    # statistic data of student
    def statistic_list_student(self):
        # get the number of student higher score than 80
        number_high_score = (self.dataFrame_student["score"] > 80).sum()
        print("Total student have score higher than 80 is {} \n".format(number_high_score))
        
        avg_score = self.dataFrame_student['score'].mean()
        max_score = self.dataFrame_student['score'].max()
        min_score = self.dataFrame_student['score'].min()
        domain_value_score = max_score - min_score
        media_score = self.dataFrame_student['score'].median()

        print("Mean (average) score of list student is {:.2f} \n".format(avg_score))
        print("Max score of list student is {} \n".format(max_score))
        print("Min score of list student is {} \n".format(min_score))
        print("Range of score is {} \n".format(domain_value_score))
        print("Media score of list student is {} \n".format(media_score))

        new_list_student = self.dataFrame_student.drop([0, "score"], axis=1)
        self.most_question_skip(new_list_student)
        self.most_question_incorrect(new_list_student)


        print("------- LIST STUDENT ------- \n")
        # analysis data
        print(self.dataFrame_student)
        print(self.dataFrame_student.describe())




    # print file txt student and score of them
    def print_result_score(self):
        try:
            keys = self.dataFrame_student.keys()
            df_score = self.dataFrame_student.drop(keys[1:26], axis=1)
            path_full_txt = 'Result/' + self.filename + '_grades.txt'
            with open(path_full_txt, "w") as file:
                for score in df_score.values:
                    write_score = score[0] + "," + str(score[1]) + '\n'
                    file.writelines(write_score)
                print("\nSave file " + path_full_txt + " successfull\n")
                file.truncate()
                file.close() 
            path_full_csv = "Data/" + self.filename + '.csv'
            self.dataFrame_student.to_csv(path_full_csv)
            print("\nSave file " + path_full_csv + " successfull\n")

        except:
            print("Error System, please check print_result_score() fucntion \n")
            

def main(file_name):
    try:
        # create instance
        score_calculator = TestGradeCalculator(file_name)
        # Task 1
        score_calculator.read_file()
        # Task 2
        count_invalid = score_calculator.check_format()
        print("**** ANALYZING ****\n")
        if count_invalid == 0:
            print("No errors found!\n")
        else:
            print("Some lines are invalid\n")
        # Task 3
        answer_key = "B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D"
        score_calculator.calculating_score(answer_key)
        score_calculator.statistic_list_student()
        # Task 4
        score_calculator.print_result_score()
    except: 
        print("Error system, please contact administrator")

if __name__ == "__main__":
    while True:
        print("\nFill q to quit program \n")
        file_name = str(input("Enter a file name you want to statitic (i.e class1): "))
        if file_name == "q":
            print("Exited program\ns")
            break
        main(file_name)
        print(">>> ================================ RESTART ================================")