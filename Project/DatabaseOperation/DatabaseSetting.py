#=============================================================================================#
#       Copyright:      Seed
#       Date:           2020/5/10
#       File Name:      DatabaseSetting.py
#       Description:    This file is used to set the database operation.
#=============================================================================================#
import pymysql

# Create a class of the database.
class DatabaseOperations():
    # Set the class variables.
    __db_url = "localhost"
    __db_username = "root"
    __db_password = ""
    __db_name = "SEED"
    __db = ""
    # Create the constructor.
    def __init__(self):
        # Create the database connection.
        self.__db = self.db_connect()
    # Set the function to do the database connection.
    def db_connect(self):
        self.__db = pymysql.connect(self.__db_url, self.__db_username, self.__db_password, self.__db_name)
        return self.__db
    # Set the function to delete the database connection.
    def __del__(self):
        self.__db.close()
    
    #=============================================================================================#
    #       Login Operation
    #=============================================================================================#
    # Set the function to check the student login.
    def studentLoginCheck(self, userID, password):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = """SELECT * FROM student WHERE email = '%s' AND password = '%s' """ % (userID, password)
        # Execute the sql.
        cursor.execute(test)
        # Fetch the result.
        result = cursor.fetchall()
        # Check whether fetch the data.
        if result: # If yes.
            # Return the result.
            return result, True
        else: # If not.
            return result, False
    # Set the function to check the teacher login.
    def teacherLoginCheck(self, userID, password):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = """SELECT * FROM teacher WHERE userID = '%s' AND password = '%s' """ % (userID, password)
        # Execute the sql.
        cursor.execute(test)
        # Fetch the result.
        result = cursor.fetchall()
        # Check whether fetch the data.
        if result: # If yes.
            # Return the result.
            return result, True
        else: # If not.
            return result, False
    
    #=============================================================================================#
    #       Course Operation
    #=============================================================================================#
    # Set the function to get the course info.
    def getCourseInfo(self, courseID):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = """SELECT * FROM course WHERE courseID = '%s' """ % (courseID)
        # Execute the sql.
        cursor.execute(test)
        # Fetch the result.
        result = cursor.fetchall()
        # Return the result.
        return result
    # Set the function to update the number of student enrolled into this course.
    def updateNumberOfStudent(self, courseID, numOfStudent):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = """UPDATE course SET numOfStudent = %d WHERE courseID = '%s' """ % (numOfStudent, courseID)
        # Execute the sql.
        try:
            cursor.execute(test)
            # Change the table.
            self.__db.commit()
            # Get the result.
            result = True
        except:
            # If the change is not legal, rollback to the original table.
            self.__db.rollback()
            # Return Value.
            result = False
        # Return the result.
        return result
    # Set the function to set the course name.
    def setCourseName(self, courseID, courseName):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = """UPDATE course SET courseName = '%s' WHERE courseID = '%s' """ % (courseName, courseID)
        # Execute the sql.
        try:
            cursor.execute(test)
            # Change the table.
            self.__db.commit()
            # Get the result.
            result = True
        except:
            # If the change is not legal, rollback to the original table.
            self.__db.rollback()
            # Return Value.
            result = False
        # Return the result.
        return result
    # Set the function to store the student info.
    def storeStudentInfo(self, name, ID, email, GPA):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = """INSERT INTO student VALUES('%s', '%s', '11111111', '', '%s', '%s', '', %f) """ % (ID, name, name, email, GPA)
        # Execute the sql.
        try:
            cursor.execute(test)
            # Change the table.
            self.__db.commit()
            # Get the result.
            result = True
        except:
            # If the change is not legal, rollback to the original table.
            self.__db.rollback()
            # Return Value.
            result = False
        # Return the result.
        return result
    # Set the function to store which course the student taken by.
    def storeStudentCourse(self, courseID, userID):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = """INSERT INTO takenby VALUES('%s', '%s') """ % (courseID, userID)
        # Execute the sql.
        try:
            cursor.execute(test)
            # Change the table.
            self.__db.commit()
            # Get the result.
            result = True
        except:
            # If the change is not legal, rollback to the original table.
            self.__db.rollback()
            # Return Value.
            result = False
        # Return the result.
        return result
    # Set the function to get the submission info.
    def getSubmissionItemList(self, courseID):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = """SELECT submissionID FROM ownedby WHERE courseID = '%s' """ % (courseID)
        # Execute the sql.
        cursor.execute(test)
        # Fetch the result.
        result = cursor.fetchall()
        # Return the result.
        return result
    # Set the function to get the percentage of the submission.
    def getPercentageOfSubmission(self, submissionID):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = """SELECT percentage FROM submission WHERE submissionID = '%s' """ % (submissionID)
        # Execute the sql.
        cursor.execute(test)
        # Fetch the result.
        result = cursor.fetchall()
        # Return the result.
        return result
    # Set the function to add the submission.
    def addSubmission(self, title, percentage, courseID):
        # Set the variable to get the new ID for the submission.
        submissionID = -1
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test1 = """INSERT INTO submission VALUES (null, '%s', %f)""" % (title, percentage)
        try:
            # Execute the sql.
            cursor.execute(test1)
            # Change the table.
            self.__db.commit()
            # Get the ID.
            submissionID = cursor.lastrowid
        except:
            # If the change is not legal, rollback to the original table.
            self.__db.rollback()
            # Return Value.
            result = False
        # Create the sql.
        test2 = """INSERT INTO ownedby VALUES('%s', %d)""" % (courseID, submissionID)
        try:
            # Execute the sql.
            cursor.execute(test2)
            # Change the table.
            self.__db.commit()
            # Return Value.
            result = submissionID
        except:
            # If the change is not legal, rollback to the original table.
            self.__db.rollback()
            # Return Value.
            result = False
        return result
    # Set the function to get the team ID for a course.
    def getAllTeamID(self, courseID):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = """SELECT teamID FROM has WHERE courseID = '%s' """ % (courseID)
        # Execute the sql.
        cursor.execute(test)
        # Fetch the result.
        result = cursor.fetchall()
        # Return the result.
        return result
    # Set the function to get the student ID for a course.
    def getAllStudentID(self, courseID):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = """SELECT userID FROM takenby WHERE courseID = '%s' """ % (courseID)
        # Execute the sql.
        cursor.execute(test)
        # Fetch the result.
        result = cursor.fetchall()
        # Return the result.
        return result
    # Set the function to update the form team method.
    def updateFormTeamMethod(self, methodInfo, courseID):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = """UPDATE course SET formTeamMethod = "%s" WHERE courseID = '%s'""" % (methodInfo, courseID)
        # Execute the sql.
        try:
            cursor.execute(test)
            # Change the table.
            self.__db.commit()
            # Get the result.
            result = True
        except:
            # If the change is not legal, rollback to the original table.
            self.__db.rollback()
            # Return Value.
            result = False
        # Return the result.
        return result
    # Set the function to store the team info.
    def storeTeamInfo(self, teamNumber, numOfMember, courseID):
        # Set the variable to get the new ID for the team.
        teamID = -1
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test1 = """INSERT INTO team VALUES (null, %d, null, %d, '0')""" % (teamNumber, numOfMember)
        try:
            # Execute the sql.
            cursor.execute(test1)
            # Change the table.
            self.__db.commit()
            # Get the ID.
            teamID = cursor.lastrowid
        except:
            # If the change is not legal, rollback to the original table.
            self.__db.rollback()
            # Return Value.
            result = False
        # Create the sql.
        test2 = """INSERT INTO has VALUES('%s', %d, %d)""" % (courseID, teamID, numOfMember)
        try:
            # Execute the sql.
            cursor.execute(test2)
            # Change the table.
            self.__db.commit()
            # Return Value.
            result = teamID
        except:
            # If the change is not legal, rollback to the original table.
            self.__db.rollback()
            # Return Value.
            result = False
        return result
    # Set the function to store the member info.
    def storeMemberInfo(self, userID, teamID, courseID):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = """SELECT * FROM member WHERE userID = '%s' AND courseID = '%s' """ % (userID, courseID)
        # Execute the sql.
        cursor.execute(test)
        # Fetch the result.
        result = cursor.fetchall()
        # Test whether the student is a member.
        if result:
            # Create the sql.
            test = """UPDATE member SET teamID = %d WHERE userID = '%s' AND courseID = '%s'""" % (teamID, userID, courseID)
            # Execute the sql.
            try:
                cursor.execute(test)
                # Change the table.
                self.__db.commit()
                # Get the result.
                result = True
            except:
                # If the change is not legal, rollback to the original table.
                self.__db.rollback()
                # Return Value.
                result = False
        else:
            # Create the sql.
            test = """INSERT INTO member VALUES('%s', %d, '%s', 1, 0) """ % (userID, teamID, courseID)
            # Execute the sql.
            try:
                cursor.execute(test)
                # Change the table.
                self.__db.commit()
                # Get the result.
                result = True
            except:
                # If the change is not legal, rollback to the original table.
                self.__db.rollback()
                # Return Value.
                result = False
        # Return the result.
        return result
    
    #=============================================================================================#
    #       Student Operation
    #=============================================================================================#
    # Set the function to get the course list for a student.
    def getCourseListForStudent(self, userID):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = """SELECT courseID FROM takenby WHERE userID = '%s' """ % (userID)
        # Execute the sql.
        cursor.execute(test)
        # Fetch the result.
        result = cursor.fetchall()
        # Return the result.
        return result
    # Set the function to modify the password for a student.
    def modifyPasswordForStudent(self, userID, password):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = """UPDATE student SET password = '%s' WHERE userID = '%s' """ % (password, userID)
        # Execute the sql.
        try:
            cursor.execute(test)
            # Change the table.
            self.__db.commit()
            # Get the result.
            result = True
        except:
            # If the change is not legal, rollback to the original table.
            self.__db.rollback()
            # Return Value.
            result = False
        # Return the result.
        return result
    # Set the function to get the information of student.
    def getStudentInfo(self, userID):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = """SELECT * FROM student WHERE userID = '%s' """ % (userID)
        # Execute the sql.
        cursor.execute(test)
        # Fetch the result.
        result = cursor.fetchall()
        # Return the result.
        return result
    
    #=============================================================================================#
    #       Teacher Operation
    #=============================================================================================#
    # Set the function to get the course list for a teacher.
    def getCourseListForTeacher(self, userID):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = """SELECT courseID FROM taught WHERE userID = '%s' """ % (userID)
        # Execute the sql.
        cursor.execute(test)
        # Fetch the result.
        result = cursor.fetchall()
        # Return the result.
        return result
    # Set the function to get the information of teacher.
    def getTeacherInfo(self, userID):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = """SELECT * FROM teacher WHERE userID = '%s' """ % (userID)
        # Execute the sql.
        cursor.execute(test)
        # Fetch the result.
        result = cursor.fetchall()
        # Return the result.
        return result
    
    #=============================================================================================#
    #       Team Operation
    #=============================================================================================#
    # Set the function to get the team ID.
    def getTeamID(self, userID, courseID):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = """SELECT teamID FROM member WHERE userID = '%s' AND courseID = '%s' """ % (userID, courseID)
        # Execute the sql.
        cursor.execute(test)
        # Fetch the result.
        result = cursor.fetchall()
        # Return the result.
        return result
    # Set the function to get the leader ID.
    def getLeaderID(self, teamID):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = """SELECT userID FROM leader WHERE teamID = %d """ % (teamID)
        # Execute the sql.
        cursor.execute(test)
        # Fetch the result.
        result = cursor.fetchall()
        # Return the result.
        return result
    # Set the function to get the member list of the team.
    def getMemberList(self, teamID):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = """SELECT userID FROM member WHERE teamID = %d """ % (teamID)
        # Execute the sql.
        cursor.execute(test)
        # Fetch the result.
        result = cursor.fetchall()
        # Return the result.
        return result
    # Set the function to get all the info of team.
    def getTeamInfo(self, teamID):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = """SELECT * FROM team WHERE teamID = %d """ % (teamID)
        # Execute the sql.
        cursor.execute(test)
        # Fetch the result.
        result = cursor.fetchall()
        # Return the result.
        return result
    # Set the function to set the leader state.
    def setLeaderState(self, teamID, leaderState):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = """UPDATE team SET leaderState = "%s" WHERE teamID = %d """ % (leaderState, teamID)
        # Execute the sql.
        try:
            cursor.execute(test)
            # Change the table.
            self.__db.commit()
            # Get the result.
            result = True
        except:
            # If the change is not legal, rollback to the original table.
            self.__db.rollback()
            # Return Value.
            result = False
        # Return the result.
        return result
    # Set the function to get the leader state.
    def getLeaderState(self, teamID):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = """SELECT leaderState FROM team WHERE teamID = %d """ % (teamID)
        # Execute the sql.
        cursor.execute(test)
        # Fetch the result.
        result = cursor.fetchall()
        # Return the result.
        return result
    
    #=============================================================================================#
    #       Member Operation
    #=============================================================================================#
    # Set the function to get the contribution of the members.
    def getMemberInfo(self, userID, teamID):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = """SELECT * FROM member WHERE userID = '%s' AND teamID = %d """ % (userID, teamID)
        # Execute the sql.
        cursor.execute(test)
        # Fetch the result.
        result = cursor.fetchall()
        # Return the result.
        return result
    # Set the function to get all member of a course.
    def getAllMember(self, courseID):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = """SELECT * FROM member WHERE courseID = '%s' """ % (courseID)
        # Execute the sql.
        cursor.execute(test)
        # Fetch the result.
        result = cursor.fetchall()
        # Return the result.
        return result
    
    #=============================================================================================#
    #       Leader Operation
    #=============================================================================================#
    # Set the function to get the bonus of the leader.
    def getLeaderInfo(self, userID, teamID):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = """SELECT * FROM leader WHERE userID = '%s' AND teamID = %d """ % (userID, teamID)
        # Execute the sql.
        cursor.execute(test)
        # Fetch the result.
        result = cursor.fetchall()
        # Return the result.
        return result
    # Set the function to set the bonus of the leader.
    def setLeaderBonus(self, userID, teamID, bonus):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = """UPDATE leader SET bonus = %.2f WHERE userID = '%s' AND teamID = %d """ % (bonus, userID, teamID)
        # Execute the sql.
        try:
            cursor.execute(test)
            # Change the table.
            self.__db.commit()
            # Get the result.
            result = True
        except:
            # If the change is not legal, rollback to the original table.
            self.__db.rollback()
            # Return Value.
            result = False
        # Return the result.
        return result
    # Set the function to set the temparay state for the leader.
    def setTempBonus(self, userID, teamID, tempBonus):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = """UPDATE leader SET tempBonus = "%s" WHERE userID = '%s' AND teamID = %d """ % (tempBonus, userID, teamID)
        # Execute the sql.
        try:
            cursor.execute(test)
            # Change the table.
            self.__db.commit()
            # Get the result.
            result = True
        except:
            # If the change is not legal, rollback to the original table.
            self.__db.rollback()
            # Return Value.
            result = False
        # Return the result.
        return result
    # Set the function to set the leader.
    def setLeader(self, userID, teamID):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = """INSERT INTO leader VALUES('%s', %d, '', '0') """ % (userID, teamID)
        # Execute the sql.
        try:
            cursor.execute(test)
            # Change the table.
            self.__db.commit()
            # Get the result.
            result = True
        except:
            # If the change is not legal, rollback to the original table.
            self.__db.rollback()
            # Return Value.
            result = False
        # Return the result.
        return result
    
    #=============================================================================================#
    #       Submission Operation
    #=============================================================================================#
    # Set the function to get the info of submission.
    def getSubmissionInfo(self, submissionID):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = """SELECT * FROM submission WHERE submissionID = %d """ % (submissionID)
        # Execute the sql.
        cursor.execute(test)
        # Fetch the result.
        result = cursor.fetchall()
        # Return the result.
        return result
    # Set the function to set the title of the submission.
    def setSubmissionTitle(self, title, submissionID):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = """UPDATE submission SET title = '%s' WHERE submissionID = %d """ % (title, submissionID)
        # Execute the sql.
        try:
            cursor.execute(test)
            # Change the table.
            self.__db.commit()
            # Get the result.
            result = True
        except:
            # If the change is not legal, rollback to the original table.
            self.__db.rollback()
            # Return Value.
            result = False
        # Return the result.
        return result
    # Set the function to set the percentage of the submission.
    def setSubmissionPercentage(self, percentage, submissionID):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = """UPDATE submission SET percentage = %f WHERE submissionID = %d """ % (percentage, submissionID)
        # Execute the sql.
        try:
            cursor.execute(test)
            # Change the table.
            self.__db.commit()
            # Get the result.
            result = True
        except:
            # If the change is not legal, rollback to the original table.
            self.__db.rollback()
            # Return Value.
            result = False
        # Return the result.
        return result

    #=============================================================================================#
    #       Contribution Operation
    #=============================================================================================#
    # Set the function to save the contirbution for a submission.
    def saveContribution(self, userID, submissionID, contribution):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = """INSERT INTO belongto VALUES('%s', %d, %.2f) """ % (userID, submissionID, contribution)
        # Execute the sql.
        try:
            cursor.execute(test)
            # Change the table.
            self.__db.commit()
            # Get the result.
            result = True
        except:
            # If the change is not legal, rollback to the original table.
            self.__db.rollback()
            # Return Value.
            result = False
        # Return the result.
        return result
    # Set the function to update the contribution for a submission.
    def updateContribution(self, userID, submissionID, contribution):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = """UPDATE belongto SET contribution = %.2f WHERE userID = '%s' AND submissionID = %d """ % (contribution, userID, submissionID)
        try:
            cursor.execute(test)
            # Change the table.
            self.__db.commit()
            # Get the result.
            result = True
        except:
            # If the change is not legal, rollback to the original table.
            self.__db.rollback()
            # Return Value.
            result = False
        # Return the result.
        return result
    # Set the function to save the contirbution for a member.
    def calculateContribution(self, userID, teamID, contribution):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = """UPDATE member SET contribution = %.2f, state = %d WHERE userID = '%s' AND teamID = %d """ % (contribution, 1, userID, teamID)
        # Execute the sql.
        try:
            cursor.execute(test)
            # Change the table.
            self.__db.commit()
            # Get the result.
            result = True
        except:
            # If the change is not legal, rollback to the original table.
            self.__db.rollback()
            # Return Value.
            result = False
        # Return the result.
        return result
    # Set the function to get the submission info for a student.
    def checkBelongTo(self, userID, submissionID):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = """SELECT * FROM belongto WHERE userID = '%s' AND submissionID = %d """ % (userID, submissionID)
        # Execute the sql.
        cursor.execute(test)
        # Fetch the result.
        result = cursor.fetchall()
        # Return the result.
        return result
    
    #=============================================================================================#
    #       Contribution Operation
    #=============================================================================================#
    # Set the function to get the invitation state info.
    def getInvitationStateInfo(self, userID, courseID):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = """SELECT inviteeID, state FROM pairs WHERE inviterID = '%s' AND courseID = '%s' """ % (userID, courseID)
        # Execute the sql.
        cursor.execute(test)
        # Fetch the result.
        result = cursor.fetchall()
        # Return the result.
        return result
    # Set the function to get the invitation info.
    def getInvitationInfo(self, userID, courseID):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = """SELECT * FROM pairs WHERE inviteeID = '%s' AND courseID = '%s' AND state = %d """ % (userID, courseID, 0)
        # Execute the sql.
        cursor.execute(test)
        # Fetch the result.
        result = cursor.fetchall()
        # Return the result.
        return result
    # Set the function to delete the invitation which the inviter has been rejected.
    def deleteRejectedInviationForInviter(self, userID, courseID):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = "DELETE FROM pairs WHERE inviterID = '%s' AND courseID = '%s' """ % (userID, courseID)
        # Execute the sql.
        try:
            cursor.execute(test)
            # Change the table.
            self.__db.commit()
            # Get the result.
            result = True
        except:
            # If the change is not legal, rollback to the original page.
            self.__db.rollback()
            # Get the result.
            result = False
        # Return the result.
        return result
    # Set the function to update the invitation state.
    def updateInvitationState(self, userID, courseID, state, avgGPA):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = """UPDATE pairs SET avgGPA = %.2f, state = %d WHERE inviterID = '%s' AND courseID = '%s' """ % (avgGPA, state, userID, courseID)
        # Execute the sql.
        try:
            cursor.execute(test)
            # Change the table.
            self.__db.commit()
            # Get the result.
            result = True
        except:
            # If the change is not legal, rollback to the original table.
            self.__db.rollback()
            # Return Value.
            result = False
        # Return the result.
        return result
    # Set the function to get all the pairs.
    def getAllPairs(self, courseID):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = """SELECT * FROM pairs WHERE courseID = '%s' AND state = %d """ % (courseID, 1)
        # Execute the sql.
        cursor.execute(test)
        # Fetch the result.
        result = cursor.fetchall()
        # Return the result.
        return result
    # Set the function to store the invitation.
    def storeInvitation(self, inviterID, inviteeID, courseID, avgGPA):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = """INSERT INTO pairs VALUES(null, '%s', '%s', '%s', %.2f, %d) """ % (inviterID, inviteeID, courseID, avgGPA, 0)
        # Execute the sql.
        try:
            cursor.execute(test)
            # Change the table.
            self.__db.commit()
            # Get the result.
            result = True
        except:
            # If the change is not legal, rollback to the original table.
            self.__db.rollback()
            # Return Value.
            result = False
        # Return the result.
        return result
    # Set the function to check whether the user form a pair.
    def checkPair(self, userID):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = """SELECT inviteeID FROM pairs WHERE inviterID = '%s' AND state = %d """ % (userID, 1)
        # Execute the sql.
        cursor.execute(test)
        # Fetch the result.
        result = cursor.fetchall()
        # Check invitee again.
        if result:
            return result
        else:
            # Create the sql.
            test = """SELECT inviterID FROM pairs WHERE inviteeID = '%s' AND state = %d """ % (userID, 1)
            # Execute the sql.
            cursor.execute(test)
            # Fetch the result.
            result = cursor.fetchall()
            # Return the result.
            if result:
                return result
            else:
                return False
    # Set the function to delete all pairs.
    def deleteAllPairs(self, courseID):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = "DELETE FROM pairs WHERE courseID = '%s' """ % (courseID)
        # Execute the sql.
        try:
            cursor.execute(test)
            # Change the table.
            self.__db.commit()
            # Get the result.
            result = True
        except:
            # If the change is not legal, rollback to the original page.
            self.__db.rollback()
            # Get the result.
            result = False
        # Return the result.
        return result