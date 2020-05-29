#=============================================================================================#
#       Copyright:      Seed
#       Date:           2020/5/10
#       File Name:      UserClasses.py
#       Description:    This file is used to declare all the user classes.
#=============================================================================================#
import re
import sys
sys.path.append(r"./Project")
from DatabaseOperation import DatabaseSetting as Database

# The class for user.
class User():
    # Set the class variables.
    userName = "Anonymous"
    password = "123456789"
    programme = "123456789"
    userID = "123456789"
    name = "Anonymous"
    email = "12345678@xxx.xxx"
    phoneNumber = "123456789"
    # Set the constructor.
    def __init__(self, userName, password, programme, userID, name, email, phoneNumber):
        # Set the member variables.
        self.userName = userName
        self.password = password
        self.programme = programme
        self.userID = userID
        self.name = name
        self.email = email
        self.phoneNumber = phoneNumber
    # Set the function to get the username.
    def getUsername(self):
        return self.userName
    # Set the function to modify the username.
    def setUsername(self, username):
        # Check whether the username is valid.
        if re.match(r'^[a-zA-Z][a-zA-Z0-9]{1,8}$', username, 0):
            self.userName = username
            return "Modify Successful!", True
        else:
            return "The username could only start with a letter and consist of numbers and letters and the length is between 1 and 8 symbols.", False
    # Set the function to get the password.
    def getPassword(self):
        return self.password
    # Set the function to modify the password.
    def setPassword(self, password):
        # Check whether the password is valid.
        if re.match(r'^[0-9A-Za-z]{6,16}$', password, 0):
            if self.password != password:
                self.password = password
                # Connecte with the database.
                self.db = Database.DatabaseOperations()
                # Change the password.
                result = self.db.modifyPasswordForStudent(self.getID(), password)
                # Test whether the modify successful or not.
                if result: # If success.
                    # Disconnect with the database.
                    self.db.__del__()
                    return "Modify Successful!", True
                else: # If fail.
                    # Disconnect with the database.
                    self.db.__del__()
                    return "Database Error", False
            else:
                return "The password is the same as before.", False
        else:
            return "The password should only be numbers and letters and the length is between 8 and 16 symbols.", False
    # Set the function to get the programme.
    def getProgramme(self):
        return self.programme
    # Set the function to modify the programme.
    def setProgramme(self, programme):
        # Check whether the programme is valid.
        if re.match(r'^[A-Z]+$', programme, 0):
            self.programme = programme
            return "Modify Successful!", True
        else:
            return "The programme could only be uppercase letters.", False
    # Set the function to get the ID.
    def getID(self):
        return self.userID
    # Set the function to get the name.
    def getName(self):
        return self.name
    # Set the function to modify the name.
    def setName(self, name):
        # Check whether the name is valid.
        if re.match(r'^[a-zA-Z ]+$', name, 0):
            self.name = name
            return "Modify Successful!", True
        else:
            return "The name could only be letters and should be your real name.", False
    # Set the function to get the email.
    def getEmail(self):
        return self.email
    # Set the function to modify the email.
    def setEmail(self, email):
        # Check whether the email is valid.
        if re.match(r'^([A-Za-z0-9_\-\.\u4e00-\u9fa5])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,8})$', email, 0):
            self.email = email
            return "Modify Successful!", True
        else:
            return "Please input the valid email format.", False
    # Set the function to get the phone number.
    def getPhone(self):
        return self.phoneNumber
    # Set the function to modify the phone number.
    def setPhone(self, phoneNumber):
        # Check whether the phone number is valid.
        if re.match(r'^[0-9]{1,11}$', phoneNumber, 0):
            self.phoneNumber = phoneNumber
            return "Modify Successful!", True
        else:
            return "Please input the valid phone number format.", False

# The class for student.
class Student(User):
    # Set the class variables.
    GPA = 4.0
    courseList = []
    # Set the constructor.
    def __init__(self, userID):
        # Connecte with the database.
        self.db = Database.DatabaseOperations()
        # Get the student info.
        self.info = self.db.getStudentInfo(userID)
        # Set the super class constructor.
        super(Student, self).__init__(self.info[0][1], self.info[0][2], self.info[0][3], self.info[0][0], self.info[0][4], self.info[0][5], self.info[0][6])
        # Set the member variables.
        self.GPA = self.info[0][7]
        # Clear the list.
        self.courseList = []
        # Get the course from the database.
        self.temp = self.db.getCourseListForStudent(self.userID)
        for courseName in self.temp:
            self.courseList.append(courseName[0])
        # Disconnect with the database.
        self.db.__del__()
    # Set the function to set the GPA.
    def setGPA(self, GPA):
        # Test whether the GPA is valid or not.
        if type(GPA).__name__ != "double":
            return "The GPA must be a double values!", False
        else:
            if GPA > 4.0 or GPA < 0.0:
                return "The upper boundary of the GPA is 4.0, and the lower boundary is 0.0!", False
            else:
                self.GPA = GPA
                return "Modify successful!", True
    # Set the function to get the GPA.
    def getGPA(self):
        return self.GPA
    # Set the function to get the course which taken by the student.
    def getCourseList(self):
        return self.courseList

# The class for teacher.
class Teacher(User):
    # Set the class variables.
    officeNumber = "12345"
    officePhoneNumber = "12345"
    courseList = []
    # Set the constructor.
    def __init__(self, userID):
        # Connecte with the database.
        self.db = Database.DatabaseOperations()
        # Get the student info.
        self.info = self.db.getTeacherInfo(userID)
        # Set the super class constructor.
        super(Teacher, self).__init__(self.info[0][1], self.info[0][2], self.info[0][3], self.info[0][0], self.info[0][4], self.info[0][5], self.info[0][6])
        # Set the member variables.
        self.officeNumber = self.info[0][7]
        self.officePhoneNumber = self.info[0][8]
        # Clear the list.
        self.courseList = []
        # Get the course from the database.
        self.temp = self.db.getCourseListForTeacher(self.userID)
        for courseName in self.temp:
            self.courseList.append(courseName[0])
        # Disconnect with the database.
        self.db.__del__()
    # Set the function to get the office number.
    def getOfficeNumber(self):
        return self.officeNumber
    # Set the function to set the office number.
    def setOfficeNumber(self, number):
        # Test whether the office number is valid or not.
        if re.match(r"^[A-Z][0-9-]+$", number, 0):
            self.officeNumber = number
            return "Modify Successful!", True
        else:
            return "The office number must start with a capital letter followed by numbers and dash.", False
    # Set the function to get the office phone number.
    def getOfficePhoneNumber(self):
        return self.officePhoneNumber
    # Set the function to set the office phone number.
    def setOfficePhoneNumber(self, phone):
        # Check whether the phone number is valid.
        if re.match(r'^[0-9]{1,11}$', phone, 0):
            self.officePhoneNumber = phone
            return "Modify Successful!", True
        else:
            return "Please input the valid phone number format.", False
    # Set the function to get the course list.
    def getCourseList(self):
        return self.courseList

# The class for member.
class Member(Student):
    # Set the class variables.
    contribution = 1.0
    teamID = 0
    # Set the constructor.
    def __init__(self, userID, teamID):
        # Set the super class constructor.
        super(Member, self).__init__(userID)
        # Get the member variables.
        self.teamID = teamID
        # Connecte with the database.
        self.db = Database.DatabaseOperations()
        # Get the contribution.
        self.contribution = self.db.getMemberInfo(userID, teamID)[0][3]
        # Disconnect with the database.
        self.db.__del__()
    # Set the function to get the bonus state.
    def getContributionState(self):
        # Connecte with the database.
        self.db = Database.DatabaseOperations()
        # Get the bonus state.
        self.state = self.db.getMemberInfo(self.userID, self.teamID)[0][4]
        # Disconnect with the database.
        self.db.__del__()
        # Return the state.
        return self.state
    # Set the function to get the contribution.
    def getContribution(self):
        return self.contribution
    # Set the function to set the contribution.
    def calculateContribution(self, contribution):
        # Connecte with the database.
        self.db = Database.DatabaseOperations()
        result = self.db.calculateContribution(self.userID, self.teamID, contribution)
        # Check whether the save successful or not.
        if result: # If yes.
            # Disconnect with the database.
            self.db.__del__()
            return "Modify Successful!", True
        else:
            # Disconnect with the database.
            self.db.__del__()
            return "Database Error!", False

# The class for leader
class Leader(Member):
    # Set the class variables.
    bonus = 0.0
    teamID = 0
    # Set the constructor.
    def __init__(self, userID, teamID):
        # Set the super class constructor.
        super(Leader, self).__init__(userID, teamID)
        # Get the member variables.
        self.teamID = teamID
        # Connecte with the database.
        self.db = Database.DatabaseOperations()
        # Get the bonus.
        self.bonus = self.db.getLeaderInfo(userID, teamID)[0][2]
        # Disconnect with the database.
        self.db.__del__()
    # Set the function to get the bonus.
    def getBonus(self):
        return self.bonus
    # Set the function to get the bonus state.
    def getBonusState(self):
        # Connecte with the database.
        self.db = Database.DatabaseOperations()
        # Get the bonus state.
        self.state = self.db.getLeaderInfo(self.userID, self.teamID)[0][3]
        # Disconnect with the database.
        self.db.__del__()
        # Return the state.
        return self.state
    # Set the function to set the bonus state.
    def setBonusState(self, teampBonus):
        # Connecte with the database.
        self.db = Database.DatabaseOperations()
        # Set the bonus state.
        self.result = self.db.setTempBonus(self.userID, self.teamID, teampBonus)
        # Disconnect with the database.
        self.db.__del__()
        # Return the result.
        return self.result
    # Set the function set the bonus.
    def calculateBonus(self):
         # Get the temp bonus.
        self.tempBonus = eval(self.getBonusState())
        # Update the bonus.
        self.bonus = sum(self.tempBonus.values()) / len(self.tempBonus)
        # Connecte with the database.
        self.db = Database.DatabaseOperations()
        result = self.db.setLeaderBonus(self.userID, self.teamID, self.bonus)
        # Test whether the update is successful.
        if result:
            # Disconnect with the database.
            self.db.__del__()
            return "Assess Successful!", True
        else:
            # Disconnect with the database.
            self.db.__del__()
            return "Database Error!", False