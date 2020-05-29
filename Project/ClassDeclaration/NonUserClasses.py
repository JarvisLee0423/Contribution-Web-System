#=============================================================================================#
#       Copyright:      Seed
#       Date:           2020/5/10
#       File Name:      NonUserClasses.py
#       Description:    This file is used to declare all the non user classes.
#=============================================================================================#
import re
import os
import xlrd
import xlsxwriter
import math
import random
import sys
sys.path.append(r"./Project")
from DatabaseOperation import DatabaseSetting as Database
from werkzeug.utils import secure_filename

# The class for course.
class Course():
    # Set the class variables.
    courseID = 'XXX1234'
    courseName = "XXX"
    submissionList = []
    numberOfStudent = 0
    # Set the constructor.
    def __init__(self, courseID):
        # Set the member variables.
        self.courseID = courseID
        # Connecte with the database.
        self.db = Database.DatabaseOperations()
        self.info = self.db.getCourseInfo(self.courseID)
        self.courseName = self.info[0][1]
        self.numberOfStudent = self.info[0][2]
        # Get the submission items from the database.
        self.temp = self.db.getSubmissionItemList(self.courseID)
        # Clear the submission list.
        self.submissionList = []
        for submissionID in self.temp:
            self.submissionList.append(submissionID[0])
        # Disconnect with the database.
        self.db.__del__()
    # Set the function to get the course ID.
    def getID(self):
        return self.courseID
    # Set the function to get the number of student in this course.
    def getNumOfStudent(self):
        return self.numberOfStudent
    # Set the function to get the form team method.
    def getFormMethod(self):
        # Connecte with the database.
        self.db = Database.DatabaseOperations()
        # Get the form method.
        result = self.db.getCourseInfo(self.courseID)[0][3]
        # Check whether the teacher set the method or not.
        if result:
            # Disconnect with the database.
            self.db.__del__()
            return result, True
        else:
            # Disconnect with the database.
            self.db.__del__()
            return "The teacher has not set the form team method yet!", False
    # Set the function to get the course name.
    def getCourseName(self):
        return self.courseName
    # Set the function to set the course name.
    def setCourseName(self, courseID, courseName):
        # Connecte with the database.
        self.db = Database.DatabaseOperations()
        # Test wherther the course name is valid or not.
        if re.match("^[a-zA-Z][a-zA-Z ]+$", courseName, 0):
            if courseName == self.courseName:
                # Disconnect with the database.
                self.db.__del__()
                return "The course name is the same as before.", False
            else:
                self.result = self.db.setCourseName(courseID, courseName)
                if self.result:
                    # Disconnect with the database.
                    self.db.__del__()
                    return "Modify successful!", True
                else:
                    # Disconnect with the database.
                    self.db.__del__()
                    return "Database Error!", False
        else:
            # Disconnect with the database.
            self.db.__del__()
            return "The course name could only be letters and space, and must be started with letters!", False
    # Set the function to get the submission list.
    def getSubmissionList(self):
        return self.submissionList
    # Set the function to add the submission.
    def addSubmission(self, title, percentage):
        # Test whether the course could add more submission or not.
        # Create the variables to compute the total percentage.
        self.temp = []
        # Connecte with the database.
        self.db = Database.DatabaseOperations()
        # Get the total percentage of the submission which belong to this course.
        for ID in self.submissionList:
            self.temp.append(self.db.getPercentageOfSubmission(ID)[0][0])
        # Compute the whole percentage and give the corresponding operation.
        if sum(self.temp) == 1.0:
            # Disconnect with the database.
            self.db.__del__()
            return "You can not add more submission, because all the whole percentage now is 100%.", False
        else:
            if percentage > (1-sum(self.temp)):
                # Disconnect with the database.
                self.db.__del__()
                if round(((1-sum(self.temp))*100), 2) == 0.00:
                    return "You can not add more submission please modify the exist submission's percentage to add more!", False
                else:
                    return "You can only add submission whose percentage is lower than %.1f%%" % ((1-sum(self.temp))*100), False
            else:
                self.result = self.db.addSubmission(title, percentage, self.courseID)
                if self.result:
                    # Disconnect with the database.
                    self.db.__del__()
                    return "Add Successful!", True
                else:
                    # Disconnect with the database.
                    self.db.__del__()
                    return "Database Error", False
    # Set the function to add the extra student info.
    def addExtraStudentInfo(self, name, ID, email, GPA):
        # Connecte with the database.
        self.db = Database.DatabaseOperations()
        # Test whether the student has already in the database.
        if self.db.getStudentInfo(ID): # If yes.
            # Store course info.
            result = self.db.storeStudentCourse(self.courseID, ID)
            # Check whether the storing operation is successful or not.
            if result:
                # Insert the number of student in this course.
                result = self.db.updateNumberOfStudent(self.courseID, self.db.getCourseInfo(self.courseID)[0][2] + 1)
                # Test whether the update is successful.
                if result:  # If yes.
                    # Disconnect with the database.
                    self.db.__del__()
                    return "Store Successful", True
                else:
                    # Disconnect with the database.
                    self.db.__del__()
                    return "Database Error", False
            else:
                # Disconnect with the database.
                self.db.__del__()
                return "The student has been enrolled into this course!", False
        else: # If no.
            # Store student info.
            result = self.db.storeStudentInfo(name, ID, email, GPA)
            # Check whether the storing operation is successful or not.
            if result:
                # Store course info.
                result = self.db.storeStudentCourse(self.courseID, ID)
                # Check whether the storing operation is successful or not.
                if result:
                    # Insert the number of student in this course.
                    result = self.db.updateNumberOfStudent(self.courseID, self.db.getCourseInfo(self.courseID)[0][2] + 1)
                    # Test whether the update is successful.
                    if result:  # If yes.
                        # Disconnect with the database.
                        self.db.__del__()
                        return "Store Successful", True
                    else:
                        # Disconnect with the database.
                        self.db.__del__()
                        return "Database Error", False
                else:
                    # Disconnect with the database.
                    self.db.__del__()
                    return "Database Error", False
            else:
                # Disconnect with the database.
                self.db.__del__()
                return "Database Error", False
    # Set the function to export file.
    def exportFile(self):
        # Connecte with the database.
        self.db = Database.DatabaseOperations()
        # Check whether the course has form the team or not.
        self.teamID = self.db.getAllTeamID(self.courseID)
        if self.teamID:
            # Check whether all the course has the leader.
            leaderState = []
            for each in self.teamID:
                leaderState.append(eval(self.db.getLeaderState(each[0])[0][0]))
            if sum(leaderState) == len(leaderState):
                # The list used to store the contribution info.
                self.contribution = []
                # Get the data.
                for each in self.db.getAllMember(self.courseID):
                    self.temp = []
                    self.result = self.db.getStudentInfo(each[0])[0][4]
                    self.temp.extend([self.result, each[0], each[3]])
                    self.result = self.db.getLeaderInfo(each[0], each[1])
                    if self.result:
                        self.temp.append(self.result[0][2])
                        self.contribution.append(self.temp)
                    else:
                        self.temp.append(0)
                        self.contribution.append(self.temp)
                # Write the data into a excel file.
                self.file = xlsxwriter.Workbook('Contribution.xlsx')
                self.sheet = self.file.add_worksheet('Contribution')
                self.sheet.write('A1', 'Name')
                self.sheet.write('B1', 'ID')
                self.sheet.write('C1', 'Contribution')
                self.sheet.write('D1', 'Bonus')
                for i, each in enumerate(self.contribution):
                    self.sheet.write('A'+str(i+2), each[0])
                    self.sheet.write('B'+str(i+2), each[1])
                    self.sheet.write('C'+str(i+2), each[2])
                    self.sheet.write('D'+str(i+2), each[3])
                self.file.close()
                # Disconnect with the database.
                self.db.__del__()
                # Return the excel file.
                return self.file, True
            else:
                # Disconnect with the database.
                self.db.__del__()
                return "There are some team has not selected the leader!", False
        else:
            # Disconnect with the database.
            self.db.__del__()
            return "This course has not formed any team!", False
    # Set the function to import file.
    def importFile(self, form):
        # Connecte with the database.
        self.db = Database.DatabaseOperations()
        # Get the file.
        self.file = form['StudentInfo']
        # Test whether the file name is the correct name.
        if self.file and self.file.filename.rsplit('.', 1)[1] in ['xls', 'xlsx']:
            # Get the secure filename.
            self.name = secure_filename(self.file.filename)
            # Get the suffix name.
            self.suffix = self.name.rsplit('.', 1)[1]
            # Modify the file name.
            self.newName = 'StudentInfo' + '.' + self.suffix
            # Save the file.
            self.file.save(os.path.join('./TemperaryFile', self.newName))
            # Open the file.
            self.data = xlrd.open_workbook("./TemperaryFile/" + self.newName)
            # Get the table.
            self.table = self.data.sheets()[0]
            # Get the number of rows.
            self.nrows = self.table.nrows
            # Check the info in files.
            for i in range(0, self.nrows):
                self.info = self.table.row_values(i)
                if self.info[1] and self.info[2]:
                    continue
                else:
                    # Disconnect with the database.
                    self.db.__del__()
                    return "Please Check the information in the file, there may lack of some necessary information such as ID and Email!", False
            # Store the data into database.
            for i in range(0, self.nrows):
                self.info = self.table.row_values(i)
                # Test whether the student has already in the database.
                if self.db.getStudentInfo(self.info[1]): # If yes.
                    # Store course info.
                    result = self.db.storeStudentCourse(self.courseID, self.info[1])
                    # Check whether the storing operation is successful or not.
                    if result:
                        continue
                    else:
                        # Disconnect with the database.
                        self.db.__del__()
                        return "There are some students have already enrolled in this course, if you want to add more students, please click 'Add Extra Student' in Main page!", False
                else: # If no.
                    # Check whether the GPA info is given.
                    if self.info[3] == '':
                        gpa = 3.0
                    else:
                        gpa = self.info[3]
                    # Store student info.
                    result = self.db.storeStudentInfo(self.info[0], self.info[1], self.info[2], gpa)
                    # Check whether the storing operation is successful or not.
                    if result:
                        # Store course info.
                        result = self.db.storeStudentCourse(self.courseID, self.info[1])
                        # Check whether the storing operation is successful or not.
                        if result:
                            continue
                        else:
                            # Disconnect with the database.
                            self.db.__del__()
                            return "Database Error", False
                    else:
                        # Disconnect with the database.
                        self.db.__del__()
                        return "Database Error", False
            # Insert the number of student in this course.
            result = self.db.updateNumberOfStudent(self.courseID, self.nrows)
            # Test whether the update is successful.
            if result:  # If yes.
                # Disconnect with the database.
                self.db.__del__()
                return "Store Successful", True
            else:
                # Disconnect with the database.
                self.db.__del__()
                return "Database Error", False
        else:
            # Disconnect with the database.
            self.db.__del__()
            # Return the result.
            return "Please input the excel file.", False
    # Set the function to form the team.
    def formTeam(self, methodInfo):
        # Connecte with the database.
        self.db = Database.DatabaseOperations()
        # Get the form team method.
        self.method = eval(methodInfo)[0]
        # Get the GPA bound.
        self.gpaBound = eval(methodInfo)[1]
        # Get the number of member for a team.
        self.memberNum = eval(methodInfo)[2]
        # Indicate which method is used.
        if self.method == 'A':
            # Test whether the member number is valid or not.
            if self.memberNum >= self.numberOfStudent or self.memberNum == 1:
                # Disconnected the database.
                self.db.__del__()
                return "Please input a valid member number, the member number could not equal to 1 or larger than the number of student who has enrolled in this course!", False
            else:
                # Get the number of team.
                self.numOfteam = int(math.ceil(self.numberOfStudent / self.memberNum))
                # Get the number of member in last team.
                self.lastTeamMember = self.numberOfStudent % self.memberNum
                # Check whether the last team has enough student or not.
                if self.lastTeamMember >= math.ceil(self.memberNum / 2) or self.lastTeamMember == 0:
                    # Store the team info into the database.
                    for i in range(1, self.numOfteam + 1):
                        if self.lastTeamMember != 0 and i == self.numOfteam:
                            self.result = self.db.storeTeamInfo(i, self.lastTeamMember, self.courseID)
                        else:
                            self.result = self.db.storeTeamInfo(i, self.memberNum, self.courseID)
                        # Check whether store successful or not.
                        if self.result:
                            continue
                        else:
                            # Disconnected the database.
                            self.db.__del__()
                            return "Database Error", False
                else:
                    # Disconnected the database.
                    self.db.__del__()
                    return "Please decrease the member number, the last team don't has enough student with this member number!", False
        elif self.method == 'B':
            # Test whether the member number is valid or not.
            if self.memberNum >= self.numberOfStudent or self.memberNum == 1:
                # Disconnected the database.
                self.db.__del__()
                return "Please input a valid member number, the member number could not equal to 1 or larger than the number of student who has enrolled in this course!", False
            else:
                # Get the number of team.
                self.numOfteam = int(math.ceil(self.numberOfStudent / self.memberNum))
                # Get the number of member in last team.
                self.lastTeamMember = self.numberOfStudent % self.memberNum
                # Check whether the last team has enough student or not.
                if self.lastTeamMember >= math.ceil(self.memberNum / 2) or self.lastTeamMember == 0:
                    # Set the dict to store the number of member in this team.
                    self.teamMemberCount = {}
                    # Store the team info into the database.
                    for i in range(1, self.numOfteam + 1):
                        if self.lastTeamMember != 0 and i == self.numOfteam:
                            self.result = self.db.storeTeamInfo(i, self.lastTeamMember, self.courseID)
                        else:
                            self.result = self.db.storeTeamInfo(i, self.memberNum, self.courseID)
                        # Check whether store successful or not.
                        if self.result:
                            self.teamMemberCount[self.result] = 0
                        else:
                            # Disconnected the database.
                            self.db.__del__()
                            return "Database Error", False
                    # Get ID of all student who enrolled into this course.
                    self.studentList = []
                    for each in self.db.getAllStudentID(self.courseID):
                        self.studentList.append(each[0])
                    # Get the first team's ID.
                    self.stratID = list(self.teamMemberCount.keys())[0]
                    # Get the last team's ID.
                    self.endID = self.stratID + self.numOfteam - 1
                    # Randomly set the member.
                    for each in self.studentList:
                        # Store the member info into the database.
                        while True:
                            # Randomly select the team ID.
                            self.teamID = random.randint(self.stratID, self.endID)
                            # Check whether the team ID is the last team.
                            if self.teamID == self.endID:
                                # Check whether the last team is special.
                                if self.lastTeamMember != 0:
                                    # Check whether the team is full.
                                    if self.teamMemberCount[self.teamID] == self.lastTeamMember:
                                        continue
                                    else:
                                        # Store the member info.
                                        self.result = self.db.storeMemberInfo(each, self.teamID, self.courseID)
                                        # Check whether store successful or not.
                                        if self.result:
                                            # Reset the member number of this team.
                                            self.teamMemberCount[self.teamID] = self.teamMemberCount[self.teamID] + 1
                                            break
                                        else:
                                            # Disconnected the database.
                                            self.db.__del__()
                                            return "Database Error", False
                                else:
                                    # Check whether the team is full.
                                    if self.teamMemberCount[self.teamID] == self.memberNum:
                                        continue
                                    else:
                                        # Store the member info.
                                        self.result = self.db.storeMemberInfo(each, self.teamID, self.courseID)
                                        # Check whether store successful or not.
                                        if self.result:
                                            # Reset the member number of this team.
                                            self.teamMemberCount[self.teamID] = self.teamMemberCount[self.teamID] + 1
                                            break
                                        else:
                                            # Disconnected the database.
                                            self.db.__del__()
                                            return "Database Error", False
                            else:
                                # Check whether the team is full.
                                if self.teamMemberCount[self.teamID] == self.memberNum:
                                    continue
                                else:
                                    # Store the member info.
                                    self.result = self.db.storeMemberInfo(each, self.teamID, self.courseID)
                                    # Check whether store successful or not.
                                    if self.result:
                                        # Reset the member number of this team.
                                        self.teamMemberCount[self.teamID] = self.teamMemberCount[self.teamID] + 1
                                        break
                                    else:
                                        # Disconnected the database.
                                        self.db.__del__()
                                        return "Database Error", False
                else:
                    # Disconnected the database.
                    self.db.__del__()
                    return "Please decrease the member number, the last team don't has enough student with this member number!", False
        elif self.method == 'C':
            # Test whether the member number is valid or not.
            if self.memberNum >= self.numberOfStudent or self.memberNum == 1 or self.memberNum % 2 != 0:
                # Disconnected the database.
                self.db.__del__()
                return "Please input a valid member number, the member number could not equal to 1 or larger than the number of student who has enrolled in this course and also if you want to use method C and E to form team, the number of member must be even!", False
            else:
                # Get the number of team.
                self.numOfteam = int(math.ceil(self.numberOfStudent / self.memberNum))
                # Get the number of member in last team.
                self.lastTeamMember = self.numberOfStudent % self.memberNum
                # Check whether the last team has enough student or not.
                if self.lastTeamMember >= math.ceil(self.memberNum / 2) or self.lastTeamMember == 0:
                    # Store the team info into the database.
                    for i in range(1, self.numOfteam + 1):
                        if self.lastTeamMember != 0 and i == self.numOfteam:
                            self.result = self.db.storeTeamInfo(i, self.lastTeamMember, self.courseID)
                        else:
                            self.result = self.db.storeTeamInfo(i, self.memberNum, self.courseID)
                        # Check whether store successful or not.
                        if self.result:
                            continue
                        else:
                            # Disconnected the database.
                            self.db.__del__()
                            return "Database Error", False
                else:
                    # Disconnected the database.
                    self.db.__del__()
                    return "Please decrease the member number, the last team don't has enough student with this member number!", False
        elif self.method == 'D':
            # Check whether the GPA bound is valid.
            if self.gpaBound > 2:
                # Disconnected the database.
                self.db.__del__()
                return "Please input a valid GPA bound, the GPA bound can not larger than 2", False
            else:
                # Test whether the member number is valid or not.
                if self.memberNum >= self.numberOfStudent or self.memberNum == 1:
                    # Disconnected the database.
                    self.db.__del__()
                    return "Please input a valid member number, the member number could not equal to 1 or larger than the number of student who has enrolled in this course!", False
                else:
                    # Get the number of team.
                    self.numOfteam = int(math.ceil(self.numberOfStudent / self.memberNum))
                    # Get the number of member in last team.
                    self.lastTeamMember = self.numberOfStudent % self.memberNum
                    # Check whether the last team has enough student or not.
                    if self.lastTeamMember >= math.ceil(self.memberNum / 2) or self.lastTeamMember == 0:
                        # Set the dict to store the number of member in this team.
                        self.teamMemberCount = {}
                        # Set the dict to store the sum of gpa of all members in the same team.
                        self.teamAvgGPA = {}
                        # Store the team info into the database.
                        for i in range(1, self.numOfteam + 1):
                            if self.lastTeamMember != 0 and i == self.numOfteam:
                                self.result = self.db.storeTeamInfo(i, self.lastTeamMember, self.courseID)
                            else:
                                self.result = self.db.storeTeamInfo(i, self.memberNum, self.courseID)
                            # Check whether store successful or not.
                            if self.result:
                                self.teamMemberCount[self.result] = 0
                                self.teamAvgGPA[self.result] = []
                            else:
                                # Disconnected the database.
                                self.db.__del__()
                                return "Database Error", False
                        # Get ID and GPA of all student who enrolled into this course.
                        self.studentList = []
                        self.studentGPA = []
                        for each in self.db.getAllStudentID(self.courseID):
                            self.studentList.append(each[0])
                            # Get the student GPA.
                            self.GPA = self.db.getStudentInfo(each[0])[0][7]
                            # Check whether the GPA is valid.
                            if str(self.GPA) == '' or self.GPA == 0 or self.GPA == None or str(self.GPA) == 'NULL':
                                self.GPA = 3.0
                                # Store the gpa.
                                self.studentGPA.append(self.GPA)
                            else:
                                # Store the gpa.
                                self.studentGPA.append(self.GPA)
                        # Get the standard gpa value for system to form team.
                        self.gpaStandard = round((sum(self.studentGPA) / len(self.studentGPA)), self.gpaBound)
                        # Get the first team's ID.
                        self.stratID = list(self.teamMemberCount.keys())[0]
                        # Get the last team's ID.
                        self.endID = self.stratID + self.numOfteam - 1
                        # Randomly set the member.
                        for i, each in enumerate(self.studentList):
                            # Store the member info into the database.
                            while True:
                                # Randomly select the team ID.
                                self.teamID = random.randint(self.stratID, self.endID)
                                # Check whether the team ID is the last team.
                                if self.teamID == self.endID:
                                    # Check whether the last team is special.
                                    if self.lastTeamMember != 0:
                                        # Check whether the team is full.
                                        if self.teamMemberCount[self.teamID] == self.lastTeamMember:
                                            continue
                                        else:
                                            # Indicate whether the student is the first member in this team.
                                            if self.teamMemberCount[self.teamID] == 0:
                                                # Store the member info.
                                                self.result = self.db.storeMemberInfo(each, self.teamID, self.courseID)
                                                # Check whether store successful or not.
                                                if self.result:
                                                    # Reset the member number of this team.
                                                    self.teamMemberCount[self.teamID] = self.teamMemberCount[self.teamID] + 1
                                                    # Stpre the student GPA.
                                                    self.teamAvgGPA[self.teamID].append(self.studentGPA[i])
                                                    break
                                                else:
                                                    # Disconnected the database.
                                                    self.db.__del__()
                                                    return "Database Error", False
                                            else:
                                                # Calculate the team gpa when this student add into this team.
                                                self.testGPA = round((sum(self.teamAvgGPA[self.teamID]) + self.studentGPA[i]) / (len(self.teamAvgGPA[self.teamID]) + 1), self.gpaBound)
                                                # Check whether the GPA is valid.
                                                if abs(self.testGPA - self.gpaStandard) <= 0.3:
                                                    # Store the member info.
                                                    self.result = self.db.storeMemberInfo(each, self.teamID, self.courseID)
                                                    # Check whether store successful or not.
                                                    if self.result:
                                                        # Reset the member number of this team.
                                                        self.teamMemberCount[self.teamID] = self.teamMemberCount[self.teamID] + 1
                                                        # Stpre the student GPA.
                                                        self.teamAvgGPA[self.teamID].append(self.studentGPA[i])
                                                        break
                                                    else:
                                                        # Disconnected the database.
                                                        self.db.__del__()
                                                        return "Database Error", False
                                                else:
                                                    continue
                                    else:
                                        # Check whether the team is full.
                                        if self.teamMemberCount[self.teamID] == self.memberNum:
                                            continue
                                        else:
                                            # Indicate whether the student is the first member in this team.
                                            if self.teamMemberCount[self.teamID] == 0:
                                                # Store the member info.
                                                self.result = self.db.storeMemberInfo(each, self.teamID, self.courseID)
                                                # Check whether store successful or not.
                                                if self.result:
                                                    # Reset the member number of this team.
                                                    self.teamMemberCount[self.teamID] = self.teamMemberCount[self.teamID] + 1
                                                    # Stpre the student GPA.
                                                    self.teamAvgGPA[self.teamID].append(self.studentGPA[i])
                                                    break
                                                else:
                                                    # Disconnected the database.
                                                    self.db.__del__()
                                                    return "Database Error", False
                                            else:
                                                # Calculate the team gpa when this student add into this team.
                                                self.testGPA = round((sum(self.teamAvgGPA[self.teamID]) + self.studentGPA[i]) / (len(self.teamAvgGPA[self.teamID]) + 1), self.gpaBound)
                                                # Check whether the GPA is valid.
                                                if abs(self.testGPA - self.gpaStandard) <= 0.3:
                                                    # Store the member info.
                                                    self.result = self.db.storeMemberInfo(each, self.teamID, self.courseID)
                                                    # Check whether store successful or not.
                                                    if self.result:
                                                        # Reset the member number of this team.
                                                        self.teamMemberCount[self.teamID] = self.teamMemberCount[self.teamID] + 1
                                                        # Stpre the student GPA.
                                                        self.teamAvgGPA[self.teamID].append(self.studentGPA[i])
                                                        break
                                                    else:
                                                        # Disconnected the database.
                                                        self.db.__del__()
                                                        return "Database Error", False
                                                else:
                                                    continue
                                else:
                                    # Check whether the team is full.
                                    if self.teamMemberCount[self.teamID] == self.memberNum:
                                        continue
                                    else:
                                        # Indicate whether the student is the first member in this team.
                                        if self.teamMemberCount[self.teamID] == 0:
                                            # Store the member info.
                                            self.result = self.db.storeMemberInfo(each, self.teamID, self.courseID)
                                            # Check whether store successful or not.
                                            if self.result:
                                                # Reset the member number of this team.
                                                self.teamMemberCount[self.teamID] = self.teamMemberCount[self.teamID] + 1
                                                # Stpre the student GPA.
                                                self.teamAvgGPA[self.teamID].append(self.studentGPA[i])
                                                break
                                            else:
                                                # Disconnected the database.
                                                self.db.__del__()
                                                return "Database Error", False
                                        else:
                                            # Calculate the team gpa when this student add into this team.
                                            self.testGPA = round((sum(self.teamAvgGPA[self.teamID]) + self.studentGPA[i]) / (len(self.teamAvgGPA[self.teamID]) + 1), self.gpaBound)
                                            # Check whether the GPA is valid.
                                            if abs(self.testGPA - self.gpaStandard) <= 0.3:
                                                # Store the member info.
                                                self.result = self.db.storeMemberInfo(each, self.teamID, self.courseID)
                                                # Check whether store successful or not.
                                                if self.result:
                                                    # Reset the member number of this team.
                                                    self.teamMemberCount[self.teamID] = self.teamMemberCount[self.teamID] + 1
                                                    # Stpre the student GPA.
                                                    self.teamAvgGPA[self.teamID].append(self.studentGPA[i])
                                                    break
                                                else:
                                                    # Disconnected the database.
                                                    self.db.__del__()
                                                    return "Database Error", False
                                            else:
                                                continue
                    else:
                        # Disconnected the database.
                        self.db.__del__()
                        return "Please decrease the member number, the last team don't has enough student with this member number!", False
        else:
            # Check whether the GPA bound is valid.
            if self.gpaBound > 2:
                # Disconnected the database.
                self.db.__del__()
                return "Please input a valid GPA bound, the GPA bound can not larger than 2", False
            else:
                # Test whether the member number is valid or not.
                if self.memberNum >= self.numberOfStudent or self.memberNum == 1 or self.memberNum % 2 != 0:
                    # Disconnected the database.
                    self.db.__del__()
                    return "Please input a valid member number, the member number could not equal to 1 or larger than the number of student who has enrolled in this course and also if you want you want to use C and E to form a team, the number of member must be even!", False
                else:
                    # Get the number of team.
                    self.numOfteam = int(math.ceil(self.numberOfStudent / self.memberNum))
                    # Get the number of member in last team.
                    self.lastTeamMember = self.numberOfStudent % self.memberNum
                    # Check whether the last team has enough student or not.
                    if self.lastTeamMember >= math.ceil(self.memberNum / 2) or self.lastTeamMember == 0:
                        # Store the team info into the database.
                        for i in range(1, self.numOfteam + 1):
                            if self.lastTeamMember != 0 and i == self.numOfteam:
                                self.result = self.db.storeTeamInfo(i, self.lastTeamMember, self.courseID)
                            else:
                                self.result = self.db.storeTeamInfo(i, self.memberNum, self.courseID)
                            # Check whether store successful or not.
                            if self.result:
                                continue
                            else:
                                # Disconnected the database.
                                self.db.__del__()
                                return "Database Error", False
                    else:
                        # Disconnected the database.
                        self.db.__del__()
                        return "Please decrease the member number, the last team don't has enough student with this member number!", False
        # Update the form team method.
        self.result = self.db.updateFormTeamMethod(methodInfo, self.courseID)
        # Check whether update successful or not.
        if self.result:
            # Disconnected the database.
            self.db.__del__()
            return "Form Successful", True
        else:
            # Disconnected the database.
            self.db.__del__()
            return "Database Error", False

# The class for submission item.
class SubmissionItem():
    # Set the class varaibles.
    title = "None"
    percentage = 1.0
    submissionID = 1
    # Set the constructor.
    def __init__(self, submissionID):
        # Connecte with the database.
        self.db = Database.DatabaseOperations()
        # Get the submission info.
        self.info = self.db.getSubmissionInfo(submissionID)
        # Set the member variables.
        self.submissionID = submissionID
        self.title = self.info[0][1]
        self.percentage = self.info[0][2]
        # Disconnect with the database.
        self.db.__del__()
    # Set the function to get the submission ID.
    def getSubmissionID(self):
        return self.submissionID
    # Set the function to get title.
    def getTitle(self):
        return self.title
    # Set the function to get percentage.
    def getPercentage(self):
        return self.percentage
    # Set the function to set the title.
    def setTitle(self, title, submissionID):
        # Connecte with the database.
        self.db = Database.DatabaseOperations()
        # Test whether the title is valid or not.
        if re.match(r"^[a-zA-Z0-9 ]+$", title, 0):
            result = self.db.setSubmissionTitle(title, submissionID)
            # Check whether the modify successful or not.
            if result: # If yes.
                # Disconnect with the database.
                self.db.__del__()
                return "Modify Successful!", True
            else:
                # Disconnect with the database.
                self.db.__del__()
                return "Database Error!", False
        else:
            # Disconnect with the database.
            self.db.__del__()
            return "The title of the submission title must be letters and numbers.", False
    # Set the function to set the percentage.
    def setPercentage(self, percentage, submissionID):
        # Connecte with the database.
        self.db = Database.DatabaseOperations()
        result = self.db.setSubmissionPercentage(percentage, submissionID)
        # Check whether the modify successful or not.
        if result: # If yes.
            # Disconnect with the database.
            self.db.__del__()
            return "Modify Successful!", True
        else:
            # Disconnect with the database.
            self.db.__del__()
            return "Database Error!", False
    # Set the function to set contribution.
    def setContribution(self, userID, contribution):
        # Connecte with the database.
        self.db = Database.DatabaseOperations()
        self.result = self.db.saveContribution(userID, self.submissionID, contribution)
        # Check whether the save successful or not.
        if self.result: # If yes.
            # Disconnect with the database.
            self.db.__del__()
            return "Modify Successful!", True
        else:
            self.result = self.db.updateContribution(userID, self.submissionID, contribution)
            if self.result:
                # Disconnect with the database.
                self.db.__del__()
                return "Modify Successful!", True
            else:
                # Disconnect with the database.
                self.db.__del__()
                return "Database Error!", False

# The class for team.
class Team():
    # Set the class variables.
    teamID = -1
    teamNumber = -1
    teamName = ""
    numOfMember = 0
    memberList = []
    leader = ""
    # Set the constructor.
    def __init__(self, teamID):
        # Set the member variables.
        self.teamID = teamID
        # Connecte with the database.
        self.db = Database.DatabaseOperations()
        # Get the team information from the database.
        self.info = self.db.getTeamInfo(self.teamID)
        # Get the member list from the database.
        self.member = self.db.getMemberList(self.teamID)
        # Set the remaining member variables.
        self.teamNumber = self.info[0][1]
        self.teamName = self.info[0][2]
        self.numOfMember = self.info[0][3]
        self.memberList = []
        for each in self.member:
            self.memberList.append(each[0])
        # Check whether there is a leader in this team.
        if self.db.getLeaderID(self.teamID):
            self.leader = self.db.getLeaderID(self.teamID)[0][0]
        # Disconnect with the database.
        self.db.__del__()
    # Set the function to get the team ID.
    def getTeamID(self):
        return self.teamID
    # Set the function to get the team name.
    def getTeamName(self):
        return self.teamName
    # Set the function to get the team number.
    def getTeamNumber(self):
        return self.teamNumber
    # Set the function to get the number of member.
    def getNumOfMember(self):
        return self.numOfMember
    # Set the function to get the member list.
    def getMember(self):
        return self.memberList
    # Set the function to get the leader.
    def getLeader(self):
        return self.leader
    # Set the function to set the leader.
    def setLeader(self, userID):
        # Connecte with the database.
        self.db = Database.DatabaseOperations()
        # Set the leader.
        result = self.db.setLeader(userID, self.teamID)
        # Disconnect with th database.
        self.db.__del__()
        if result:
            return "Set Successful!", True
        else:
            return "Database Error!", False
    # Set the function to get the leader state.
    def getLeaderState(self):
        # Connecte with the database.
        self.db = Database.DatabaseOperations()
        # Get the leader state.
        self.state = self.db.getTeamInfo(self.teamID)[0][4]
        # Disconnect with the database.
        self.db.__del__()
        # Return the state.
        return self.state
    # Set the function to set the leader state.
    def setLeaderState(self, leaderState):
        # Connecte with the database.
        self.db = Database.DatabaseOperations()
        # Set the leader state.
        self.result = self.db.setLeaderState(self.teamID, leaderState)
        # Disconnect with the database.
        self.db.__del__()
        # Return the state.
        return self.result