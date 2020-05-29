#=============================================================================================#
#       Copyright:      Seed
#       Date:           2020/5/10
#       File Name:      systemAPI.py
#       Description:    This file is used to set all the api.
#=============================================================================================#
import os
import io
import sys
import random
import math
sys.path.append(r"./Project")
from ClassDeclaration import NonUserClasses as NU
from ClassDeclaration import UserClasses as UC
from ClassDeclaration import FormValidation as FV
from DatabaseOperation import DatabaseSetting as Database
from flask import Flask, render_template, request, redirect, send_file
from flask_login import LoginManager, UserMixin, login_required, logout_user, login_user
from werkzeug.contrib.cache import SimpleCache
from collections import Counter

# Create the application.
app = Flask(__name__)
# Create the login manager and initial the login manager.
login_manager = LoginManager()
login_manager.init_app(app)
# Create the secret key.
app.secret_key = os.urandom(16)
# Set the cache.
cache = SimpleCache()

# The function for load user.
@login_manager.user_loader
def load_user(user_id):
    # Get the login.
    login = cache.get('login')
    return FV.UserLogin(login.id, login.username, login.password)

# The api for login.
@app.route('/Login', methods = ['GET', 'POST'])
def Login():
    # Create a instance of login form.
    Student = FV.StudentLoginForm(request.form)
    Teacher = FV.TeacherLoginForm(request.form)
    # Indicate whether the form is posted or not.
    if request.method == 'POST':
        # Validate the input value.
        if Student.validate() and Student.Student.data:
            # Create the database connection.
            db = Database.DatabaseOperations()
            # Check whether the login is successful.
            result, test = db.studentLoginCheck(Student.Username.data, Student.Password.data)
            # Check whether the student is in the database or not.
            if test: # If yes
                # Set the value for the global variable.
                User = UC.Student(result[0][0])
                # Store the courseID value for a while.
                cache.set('User', User, 10 * 60)
                # Set the login object.
                login = FV.UserLogin(User.getID(), User.getUsername(), User.getPassword())
                # Store the courseID value for a while.
                cache.set('login', login, 10 * 60)
                # Login.
                login_user(login)
                # Get the course list. 
                courseDict = {}
                # Get the course name.
                for ID in User.getCourseList():
                    courseDict[ID] = db.getCourseInfo(ID)[0][1]
                # Close the database connection.
                db.__del__()
                # Go to the student main page.
                return render_template('Student Main Page.html', Username = User.getUsername(), courseDict = courseDict.items())
            else: # If not.
                # Close the database connection.
                db.__del__()
                # Give the error message.
                message = "Please input the correct email address or password"
                # Return the error to the page.
                return render_template('Login.html', message = message)
        elif Teacher.validate() and Teacher.Teacher.data:
            # Create the database connection.
            db = Database.DatabaseOperations()
            # Check whether the login is successful.
            result, test = db.teacherLoginCheck(Teacher.Username.data, Teacher.Password.data)
            # Check whether the teacher is in the database or not.
            if test: # If yes
                # Set the value for the global variable.
                User = UC.Teacher(result[0][0])
                # Store the courseID value for a while.
                cache.set('User', User, 10 * 60)
                # Set the login object.
                login = FV.UserLogin(User.getID(), User.getUsername(), User.getPassword())
                # Store the courseID value for a while.
                cache.set('login', login, 10 * 60)
                # Login.
                login_user(login)
                # Get the course list. 
                courseDict = {}
                # Get the course name.
                for ID in User.getCourseList():
                    courseDict[ID] = db.getCourseInfo(ID)[0][1]
                # Close the database connection.
                db.__del__()
                # Go to the student main page.
                return render_template('Teacher Main Page.html', Username = User.getUsername(), courseDict = courseDict.items())
            else: # If not.
                # Close the database connection.
                db.__del__()
                # Give the error message.
                message = "Please input the correct user name or password"
                # Return the error to the page.
                return render_template('Login.html', message = message)
        else:
            # Get the error message of the input value.
            if Student.Username.errors:
                username_error = Student.Username.errors[0]
            elif Teacher.Username.errors:
                username_error = Teacher.Username.errors[0]
            else:
                username_error = ''
            if Student.Password.errors:
                password_error = Student.Password.errors[0]
            elif Teacher.Password.errors:
                password_error = Teacher.Password.errors[0]
            else:
                password_error = ''
            # Return the error to the page.
            return render_template('Login.html', username_error = username_error, password_error = password_error)
    else:
        return render_template('Login.html')

# The api for student main page.
@app.route('/Student Main Page', methods = ['GET', 'POST'])
@login_required
def StudentMainPage():
    # Get the user.
    User = cache.get('User')
    # Create a instance of assess leader form.
    AssessLeader = FV.AssessLeaderForm(request.form)
    # Create a instance of select leader form.
    SelectLeader = FV.SelectLeaderForm(request.form)
    # Create a instance of submission showing form.
    SubmissionShowing = FV.SubmissionShowingForm(request.form)
    # Create a instance of choose team form.
    ChooseTeam = FV.ChooseTeamForm(request.form)
    # Create the database connection.
    db = Database.DatabaseOperations()
    # Get the username.
    Username = User.getUsername()
    # Get the course list.
    courseDict = {}
    # Get the course name.
    for ID in User.getCourseList():
        courseDict[ID] = db.getCourseInfo(ID)[0][1]
    # Indicate whether the form is posted or not.
    if request.method == 'POST':
        # Validate the input value.
        if AssessLeader.validate() and AssessLeader.Leader.data:
            # Check whether the course has formed a team or not.
            if db.getTeamID(User.getID(), AssessLeader.Course.data):
                # Get the teamID.
                teamID = db.getTeamID(User.getID(), AssessLeader.Course.data)[0][0]
                # Check whether there is a leader in this team.
                if db.getLeaderID(teamID):
                    # Create the team class.
                    team = NU.Team(teamID)
                    # Get the leader ID.
                    leaderID = team.getLeader()
                    # Create the member class.
                    member = UC.Member(User.getID(), teamID)
                    # Close the database connection.
                    db.__del__()
                    # Test whether the user is the leader.
                    if leaderID == User.getID():
                        # Set the message.
                        message = "Sorry you can not assess yourself for the bonus!"
                        # Return the error to the page.
                        return render_template('Student Main Page.html', Username = Username, message = message, courseDict = courseDict.items())
                    elif member.getContributionState() == 0:
                        # Set the message.
                        message = "Sorry the whole project has not been completed!"
                        # Return the error to the page.
                        return render_template('Student Main Page.html', Username = Username, message = message, courseDict = courseDict.items())
                    else:
                        # Store the courseID value for a while.
                        cache.set('courseID', AssessLeader.Course.data, 10 * 60)
                        # Get to the leader assessment page.
                        return redirect('/Leader Assessment Page')
                else:
                    # Get the message.
                    message = "Sorry this team has not selected leader yet!"
                    # Close the database connection.
                    db.__del__()
                    # Return the error to the page.
                    return render_template('Student Main Page.html', Username = Username, message = message, courseDict = courseDict.items())
            else:
                # Get the message.
                message = "Sorry this course has not formed any team yet!"
                # Close the database connection.
                db.__del__()
                # Return the error to the page.
                return render_template('Student Main Page.html', Username = Username, message = message, courseDict = courseDict.items())
        else:
            # Validate the input value.
            if SelectLeader.validate() and SelectLeader.Vote.data:
                # Check whether the course has formed a team or not.
                if len(db.getAllMember(SelectLeader.Course.data)) == len(db.getAllStudentID(SelectLeader.Course.data)):
                    # Get the teamID.
                    teamID = db.getTeamID(User.getID(), AssessLeader.Course.data)[0][0]
                    # Create the team class.
                    team = NU.Team(teamID)
                    # Check whether there is a leader in this team.
                    if team.getLeader():
                        # Get the message.
                        message = "Sorry the leader has been set already!"
                        # Close the database connection.
                        db.__del__()
                        # Return the error to the page.
                        return render_template('Student Main Page.html', Username = Username, message = message, courseDict = courseDict.items())
                    else:
                        # Store the courseID value for a while.
                        cache.set('courseID', SelectLeader.Course.data, 10 * 60)
                        # Get to the vote page.
                        return redirect('/Vote Page')
                else:
                    # Get the message.
                    message = "Sorry this course has not formed any team yet!"
                    # Close the database connection.
                    db.__del__()
                    # Return the error to the page.
                    return render_template('Student Main Page.html', Username = Username, message = message, courseDict = courseDict.items())
            else:
                # Validate the input value.
                if SubmissionShowing.validate() and SubmissionShowing.Contribution.data:
                    # Check whether the course has formed team or not.
                    if db.getTeamID(User.getID(), SubmissionShowing.Course.data):
                        # Get the team ID.
                        teamID = db.getTeamID(User.getID(), SubmissionShowing.Course.data)[0][0]
                        # Create a team object.
                        team = NU.Team(teamID)
                        # Get the leader ID.
                        leaderID = team.getLeader()
                        # Check whether the user is the leader or not.
                        if leaderID == User.getID():
                            # Store the courseID value for a while.
                            cache.set('courseID', SubmissionShowing.Course.data, 10 * 60)
                            # Store the team.
                            cache.set('team', team, 10 * 60)
                            # Close the database connection.
                            db.__del__()
                            # Get to the corresponding page.
                            return redirect('/Submission Showing Page')
                        else:
                            # Close the database connection.
                            db.__del__()
                            # Get to the corresponding page.
                            return render_template('Student Main Page.html', Username = Username, message = "You are not the leader!", courseDict = courseDict.items())
                    else:
                        # Close the database connection.
                        db.__del__()
                        # Get to the corresponding page.
                        return render_template('Student Main Page.html', Username = Username, message = "You have not formed team yet!", courseDict = courseDict.items())
                else:
                    # Validate the input value.
                    if ChooseTeam.validate() and ChooseTeam.Choose.data:
                        # Store the courseID value for a while.
                        cache.set('courseID', ChooseTeam.Course.data, 10 * 60)
                        # Store the courseDict.
                        cache.set('courseDict', courseDict, 10 * 60)
                        # Get to the vote page.
                        return redirect('/Choose Team Page')
                    else:
                        # Get the error message of the input value.
                        if AssessLeader.Course.errors:
                            message = AssessLeader.Course.errors[0]
                        elif SelectLeader.Course.errors:
                            message = SelectLeader.Course.errors[0]
                        elif SubmissionShowing.Course.errors:
                            message = SubmissionShowing.Course.errors[0]
                        elif ChooseTeam.Course.errors:
                            message = ChooseTeam.Course.errors[0]
                        else:
                            message = ''
                        # Close the database connection.
                        db.__del__()
                        # Return the error to the page.
                        return render_template('Student Main Page.html', Username = Username, message = message, courseDict = courseDict.items())
    else:
        # Close the database connection.
        db.__del__()
        return render_template('Student Main Page.html', Username = Username, courseDict = courseDict.items())

# The api for change password page.
@app.route('/Change Password Page', methods = ['GET', 'POST'])
@login_required
def ChangePasswordPage():
    # Get the user.
    User = cache.get('User')
    # Create a instance of modify password form.
    ModifyPassword = FV.ModifyPasswordForm(request.form)
    # Get the username.
    Username = User.getUsername()
    # Indicate whether the form is posted or not.
    if request.method == 'POST':
        # Validate the input value.
        if ModifyPassword.validate() and ModifyPassword.Modify.data:
            # Modify the password.
            message,test = User.setPassword(ModifyPassword.Password.data)
            # Test whether the modify is successful.
            if test: # If yes.
                # Logout the user.
                return redirect('/Logout')
            else: # If no.
                # Print the error message.
                return render_template('Change Password Page.html', Username = Username, message = message)
        else:
            # Get the error message of the input value.
            if ModifyPassword.Password.errors:
                passwordError = ModifyPassword.Password.errors[0]
            else:
                passwordError = ''
            # Print the error message.
            return render_template('Change Password Page.html', Username = Username, passwordError = passwordError)
    else:
        return render_template('Change Password Page.html', Username = Username)

# The api for assess leader.
@app.route('/Leader Assessment Page', methods = ['GET', 'POST'])
@login_required
def LeaderAssessmentPage():
    # Get the user.
    User = cache.get('User')
    # Create a instance of update bonus form.
    UpdateBonus = FV.UpdateBonusForm(request.form)
    # Create the database connection.
    db = Database.DatabaseOperations()
    # Get the username.
    Username = User.getUsername()
    # Get the teamID.
    teamID = db.getTeamID(User.getID(), cache.get("courseID"))[0][0]
    # Create the team class.
    team = NU.Team(teamID)
    # Get the leader ID.
    leaderID = team.getLeader()
    # Create the leader class.
    leader = UC.Leader(leaderID, teamID)
    # Get the leader name.
    Leadername = leader.getName()
    # Indicate whether the form is posted or not.
    if request.method == 'POST':
        # Validate the input value.
        if UpdateBonus.validate() and UpdateBonus.Confirm.data:
            # Test whether there is some ones already do the assessment.
            if type(eval(leader.getBonusState())) != int: # If no.
                # Get the temp bonus.
                tempBonus = leader.getBonusState()
                # Change the bonus state into dictionary.
                tempBonus = eval(tempBonus)
                # Update the bonus.
                tempBonus[User.getID()] = eval(UpdateBonus.Assessment.data)
                # Update the bonus.
                result = leader.setBonusState(str(tempBonus))
                # Test whether the update is successful or not.
                if result:
                    # Give the message.
                    message = "Assess Successful!"
                    # Check whether all the people has assess the leader or not.
                    if len(tempBonus) == (team.getNumOfMember()-1):
                        # Calculate the bonus for the leader.
                        leader.calculateBonus()
                    # Close the database connection.
                    db.__del__()
                    # Print the error message.
                    return redirect('/Student Main Page')
                else:
                    # Give the message.
                    message = "Database Error!"
                    # Close the database connection.
                    db.__del__()
                    # Print the error message.
                    return render_template('Leader Assessment Page.html', Username = Username, Leadername = Leadername, message = message)
            else: # If yes.
                # Set the temp bonus.
                tempBonus = {}
                tempBonus[User.getID()] = eval(UpdateBonus.Assessment.data)
                tempBonus = str(tempBonus)
                # Update the bonus.
                result = leader.setBonusState(tempBonus)
                # Test whether the update is successful or not.
                if result:
                    # Give the message.
                    message = "Assess Successful!"
                    # Close the database connection.
                    db.__del__()
                    # Print the error message.
                    return redirect('/Student Main Page')
                else:
                    # Give the message.
                    message = "Database Error!"
                    # Close the database connection.
                    db.__del__()
                    # Print the error message.
                    return render_template('Leader Assessment Page.html', Username = Username, Leadername = Leadername, message = message)
        else:
            # Get the error message of the input value.
            if UpdateBonus.Assessment.errors:
                message = UpdateBonus.Assessment.errors[0]
            else:
                message = ''
                # Close the database connection.
                db.__del__()
                # Print the error message.
                return render_template('Leader Assessment Page.html', Username = Username, Leadername = Leadername, message = message)
    else:
        # Close the database connection.
        db.__del__()
        return render_template('Leader Assessment Page.html', Username = Username, Leadername = Leadername)

# The api for select leader.
@app.route('/Vote Page', methods = ['GET', 'POST'])
@login_required
def VotePage():
    # Create the database connection.
    db = Database.DatabaseOperations()
    # Create a instance of update leader form.
    UpdateLeader = FV.UpdateLeaderForm(request.form)
    # Get the user.
    User = cache.get('User')
    # Get the course ID.
    courseID = cache.get('courseID')
    # Get the username.
    Username = User.getUsername()
    # Get the team ID.
    teamID = db.getTeamID(User.getID(), courseID)[0][0]
    # Create the team class.
    team = NU.Team(teamID)
    # Get the member list.
    memberDict = {}
    # Get the member name.
    for ID in team.getMember():
        memberDict[ID] = db.getStudentInfo(ID)[0][4]
    # Indicate whether the form is posted or not.
    if request.method == 'POST':
        # Validate the input value.
        if UpdateLeader.validate() and UpdateLeader.Confirm.data:
            # Check whether the user is the first one to vote the leader.
            if eval(team.getLeaderState()) != 0:
                # Get the leader state.
                leaderState = team.getLeaderState()
                # Change the leader state into dictionary.
                leaderState = eval(leaderState)
                # Update the leader state.
                leaderState[User.getID()] = UpdateLeader.Leader.data
                # Update the leader state.
                result = team.setLeaderState(str(leaderState))
                # Test whether the update is successful or not.
                if result:
                    # Give the message.
                    message = "Assess Successful!"
                    # Check whether all the people has assess the leader or not.
                    if len(leaderState) == team.getNumOfMember():
                        # Get the leader ID.
                        leaderID = Counter(list(leaderState.values())).most_common(1)[0][0]
                        # Set the leader.
                        result, test = team.setLeader(leaderID)
                        # Check whether the set successfully or not.
                        if test:
                            # Change the leader state in team.
                            result = team.setLeaderState('1')
                            # Check whether the set successfully or not.
                            if result:
                                # Close the database connection.
                                db.__del__()
                                # Print the error message.
                                return redirect('/Student Main Page')
                            else:
                                # Give the message.
                                message = "Database Error!"
                                # Close the database connection.
                                db.__del__()
                                # Print the error message.
                                return render_template('Leader Assessment Page.html', Username = Username, memberDict = memberDict.items(), message = message)
                        else:
                            # Close the database connection.
                            db.__del__()
                            # Print the error message.
                            return render_template('Leader Assessment Page.html', Username = Username, memberDict = memberDict.items(), message = result)
                    else:
                        # Close the database connection.
                        db.__del__()
                        # Print the error message.
                        return redirect('/Student Main Page')
                else:
                    # Give the message.
                    message = "Database Error!"
                    # Close the database connection.
                    db.__del__()
                    # Print the error message.
                    return render_template('Leader Assessment Page.html', Username = Username, memberDict = memberDict.items(), message = message)
            else:
                # Set the leader state.
                leaderState = {}
                leaderState[User.getID()] = UpdateLeader.Leader.data
                leaderState = str(leaderState)
                # Update the leader state.
                result = team.setLeaderState(leaderState)
                # Test whether the update is successful or not.
                if result:
                    # Give the message.
                    message = "Assess Successful!"
                    # Close the database connection.
                    db.__del__()
                    # Print the error message.
                    return redirect('/Student Main Page')
                else:
                    # Give the message.
                    message = "Database Error!"
                    # Close the database connection.
                    db.__del__()
                    # Print the error message.
                    return render_template('Vote Page.html', Username = Username, memberDict = memberDict.items(), message = message)
        else:
            # Get the error message of the input value.
            if UpdateLeader.Leader.errors:
                message = UpdateLeader.Leader.errors[0]
            else:
                message = ''
            # Close the database connection.
            db.__del__()
            # Print the error message.
            return render_template('Vote Page.html', Username = Username, memberDict = memberDict.items(), message = message)
    else:
        # Disconnect the database.
        db.__del__()
        return render_template('Vote Page.html', Username = Username, memberDict = memberDict.items())
    
# The api for submission showing page.
@app.route('/Submission Showing Page', methods = ['GET', 'POST'])
@login_required
def SubmissionShowingPage():
    # Create the database connection.
    db = Database.DatabaseOperations()
    # Get the user.
    User = cache.get('User')
    # Get the username.
    Username = User.getUsername()
    # Get the submission list.
    submissionDict = {}
    # Get the course ID.
    courseID = cache.get('courseID')
    # Create the course object.
    course = NU.Course(courseID)
    # Get the submission list.
    for ID in course.getSubmissionList():
        # Get the submission info.
        submissionInfo = db.getSubmissionInfo(ID)
        # Get the submission name and percentage.
        temp = [submissionInfo[0][1], submissionInfo[0][2]*100]
        submissionDict[ID] = temp
    # Indicate whether the form is posted or not.
    if request.method == 'POST':
        # Get the button.
        for key, __ in submissionDict.items():
            # Check which button has been pushed.
            try:
                if request.form[str(key)]:
                    submissionID = key
                    # Store the submission ID.
                    cache.set('submissionID', submissionID, 10 * 60)
                    # Get to the contribution page.
                    return redirect('/Contribution Showing Page')
            except:
                continue
    else:
        # Disconnect the database.
        db.__del__()
        return render_template('Submission Showing Page.html', Username = Username, submissionDict = submissionDict.items())

# The api for contribution showing page.
@app.route('/Contribution Showing Page', methods = ['GET', 'POST'])
@login_required
def ContributionShowingPage():
    # Create the database connection.
    db = Database.DatabaseOperations()
    # Get the user.
    User = cache.get('User')
    # Get the username.
    Username = User.getUsername()
    # Get the course ID.
    courseID = cache.get('courseID')
    # Get the team.
    team = cache.get('team')
    # Get the submission ID.
    submissionID = cache.get('submissionID')
    # Create the course object.
    course = NU.Course(courseID)
    # Get the submission list.
    submissionDict = {}
    # Check the total percentage.
    count = []
    # Get the submission list.
    for ID in course.getSubmissionList():
        # Get the submission info.
        submissionInfo = db.getSubmissionInfo(ID)
        # Get the submission name and percentage.
        temp = [submissionInfo[0][1], submissionInfo[0][2]]
        submissionDict[ID] = temp
        # Get the totle percentage.
        count.append(submissionInfo[0][2]*100)
    # Get the member list.
    memberDict = {}
    # Get the member name.
    for ID in team.getMember():
        memberDict[ID] = db.getStudentInfo(ID)[0][4]
    # Indicate whether the form is posted or not.
    if request.method == 'POST':
        # Create the submission object.
        submission = NU.SubmissionItem(submissionID)
        # Store the contribution.
        for key, __ in memberDict.items():
            # Get the contribution.
            result, test = submission.setContribution(key, eval(request.form[key]))
            # Check whether the insret successful or not.
            if test:
                continue
            else:
                # Disconnect the database.
                db.__del__()
                return render_template('Contribution Showing Page.html', Username = Username, memberDict = memberDict.items(), message = result)
        # Disconnect the database.
        db.__del__()
        if sum(count) == 100:
            return redirect('/Final Contribution')
        else:
            return render_template('Submission Showing Page.html', Username = Username, submissionDict = submissionDict.items())
    else:
        # Disconnect the database.
        db.__del__()
        return render_template('Contribution Showing Page.html', Username = Username, memberDict = memberDict.items())

# The api for compute final contribution.
@app.route('/Final Contribution')
@login_required
def FinalContribution():
    # Create the database connection.
    db = Database.DatabaseOperations()
    # Get the user.
    User = cache.get('User')
    # Get the username.
    Username = User.getUsername()
    # Get the course ID.
    courseID = cache.get('courseID')
    # Get the team.
    team = cache.get('team')
    # Create the course object.
    course = NU.Course(courseID)
    # Get the submission list.
    submissionDict = {}
    # Check the total percentage.
    count = []
    # Get the submission list.
    for ID in course.getSubmissionList():
        # Get the submission info.
        submissionInfo = db.getSubmissionInfo(ID)
        # Get the submission name and percentage.
        temp = [submissionInfo[0][1], submissionInfo[0][2]]
        submissionDict[ID] = temp
        # Get the totle percentage.
        count.append(submissionInfo[0][2]*100)
    # Get the member list.
    memberDict = {}
    # Get the member name.
    for ID in team.getMember():
        memberDict[ID] = db.getStudentInfo(ID)[0][4]
    # Update the contribution of member.
    for key, __ in memberDict.items():
        # Set the count to get the number of assessed submission.
        counts = 0
        # Set the value to compute the contribution.
        contribution = []
        # Check whether all the submission has been assessed.
        for ID, data in submissionDict.items():
            # Get the info.
            info = db.checkBelongTo(key, ID)
            if not info:
                info = db.checkBelongTo(key, ID)
            else:
                contribution.append(info[0][2] * data[1])
                counts = counts + 1
        if counts == len(submissionDict):
            # Store the contribution.
            member = UC.Member(key, team.getTeamID())
            result, test = member.calculateContribution(sum(contribution))
            # Check whether save successful or not.
            if test:
                continue
            else:
                # Disconnect the database.
                db.__del__()
                return render_template('Contribution Showing Page.html', Username = Username, memberDict = memberDict.items(), message = result)
    # Disconnect the database.
    db.__del__()
    return render_template('Submission Showing Page.html', Username = Username, submissionDict = submissionDict.items())

# The api for choose team.
@app.route('/Choose Team Page')
@login_required
def ChooseTeamPage():
    # Create the database connection.
    db = Database.DatabaseOperations()
    # Get the user.
    User = cache.get('User')
    # Get the username.
    Username = User.getUsername()
    # Get the course list.
    courseDict = {}
    # Get the course name.
    for ID in User.getCourseList():
        courseDict[ID] = db.getCourseInfo(ID)[0][1]
    # Get the course ID.
    courseID = cache.get('courseID')
    # Get the team ID.
    teamID = db.getTeamID(User.getID(), courseID)
    # Create the course object.
    course = NU.Course(courseID)
    # Get the choose team method.
    result, test = course.getFormMethod()
    # Check whether the teacher has set the form method or not.
    if test:
        # Get the form team method.
        methodInfo = eval(result)
        # Store the method info.
        cache.set('methodInfo', methodInfo, 10 * 60)
        method = methodInfo[0]
        # Indicate whether the student has formed the team or not.
        if teamID and method != 'A':
            # Get the member name.
            memberName = []
            # Create the team object.
            team = NU.Team(teamID[0][0])
            for ID in team.getMember():
                memberName.append(db.getStudentInfo(ID)[0][4])
            memberName = ",".join(memberName)
            # Get the message.
            message = "You have formed the team, the teamID is %d and the members are %s!" % (teamID[0][0], memberName)
            # Disconnect the database.
            db.__del__()
            return render_template('Student Main Page.html', Username = Username, courseDict = courseDict.items(), message = message)
        else:
            # Check the method.
            if method == 'A':
                # Check whether all the student has choose the team.
                if len(db.getAllStudentID(courseID)) == len(db.getAllMember(courseID)):
                    # Get the member name.
                    memberName = []
                    # Create the team object.
                    team = NU.Team(teamID[0][0])
                    for ID in team.getMember():
                        memberName.append(db.getStudentInfo(ID)[0][4])
                    memberName = ",".join(memberName)
                    # Get the message.
                    message = "You have formed the team, the teamID is %d and the members are %s!" % (teamID[0][0], memberName)
                    # Disconnect the database.
                    db.__del__()
                    return render_template('Student Main Page.html', Username = Username, courseDict = courseDict.items(), message = message)
                else:
                    # Get all the team's info of this course.
                    teamInfo = {}
                    for ID in db.getAllTeamID(courseID):
                        # Create the list for team member's name.
                        teamMember = []
                        # Create the team object.
                        team = NU.Team(ID)
                        # Get team member.
                        for memberID in team.getMember():
                            teamMember.append(db.getStudentInfo(memberID)[0][4])
                        # Get the team info.
                        teamInfo[ID] = [team.getTeamNumber(), team.getNumOfMember(), ",".join(teamMember)]
                    # Store the team Info.
                    cache.set('teamInfo', teamInfo, 10 * 60)
                    # Disconnect the database.
                    db.__del__()
                    # Send the info into the form team page.
                    return redirect('/Choose Team With A Page')
            else:
                # Check whether the user get the team or not.
                result = db.checkPair(User.getID())
                if result:
                    # Create the student object.
                    student = UC.Student(result[0][0])
                    # Get the message.
                    message = "You have formed the pairs with %s, please wait for others to form the pairs!" % (student.getName())
                    # Disconnect the database.
                    db.__del__()
                    return render_template('Student Main Page.html', Username = Username, courseDict = courseDict.items(), message = message)
                else:
                    # Get the accept and reject info.
                    accRejInfo = db.getInvitationStateInfo(User.getID(), courseID)
                    # Check the accept and reject info.
                    if accRejInfo:
                        if accRejInfo[0][1] == -1:
                            # Create the student object.
                            invitee = UC.Student(accRejInfo[0][0])
                            # Store the invitee's name.
                            cache.set('inviteeName', invitee.getName(), 10 * 60)
                            # Disconnect the database.
                            db.__del__()
                            return redirect('/Reject Confirm Page')
                        else:
                            # Create the student object.
                            invitee = UC.Student(accRejInfo[0][0])
                            # Store the invitee's name.
                            cache.set('inviteeName', invitee.getName(), 10 * 60)
                            # Disconnect the database.
                            db.__del__()
                            return redirect('/Delete Invitation Page')
                    else:
                        # Get the info of invitation from others.
                        invitationDict = {}
                        for each in db.getInvitationInfo(User.getID(), courseID):
                            # Create the inviter's object.
                            inviter = UC.Student(each[1])
                            invitationDict[each[1]] = [each[1], each[3], each[4], inviter.getName()]
                        # Check whether their are students send invitation.
                        if invitationDict:
                            # Store the invitation dict.
                            cache.set('invitationDict', invitationDict, 10 * 60)
                            # Disconnect the database.
                            db.__del__()
                            return redirect('/Invitation Checking Page')
                        else:
                            # Get all the student who enrolled in this course.
                            studentList = []
                            for each in db.getAllStudentID(courseID):
                                studentList.append(each[0])
                            # Get all the studen who has the pairs.
                            studentInPairs = []
                            for each in db.getAllPairs(courseID):
                                studentInPairs.append(each[1])
                                studentInPairs.append(each[2])
                            # Delete all the student ID in the student list which are also in the pairs.
                            temp = []
                            for each in studentList:
                                if each in studentInPairs:
                                    temp.append(each)
                            for each in temp:
                                studentList.remove(each)
                            studentList.remove(User.getID())
                            # Store this student list.
                            cache.set('studentList', studentList, 10 * 60)
                            # Disconnect the database.
                            db.__del__()
                            return redirect('Invitation Page')
    else:
        # Disconnect the database.
        db.__del__()
        return render_template('Student Main Page.html', Username = Username, courseDict = courseDict.items(), message = result)

# The api for invitation.
@app.route('/Invitation Page', methods = ['GET', 'POST'])
@login_required
def InvitationPage():
    # Create the database connection.
    db = Database.DatabaseOperations()
    # Create a instance for choose a pair.
    ChoosePair = FV.ChoosePairForm(request.form)
    # Get the user.
    User = cache.get('User')
    # Get the username.
    Username = User.getUsername()
    # Get the course ID.
    courseID = cache.get('courseID')
    # Get the student list.
    studentList = cache.get('studentList')
    # Get the student dict.
    studentDict = {}
    for each in studentList:
        # Create the student object.
        student = UC.Student(each)
        studentDict[each] = student.getName()
    # Indicate whether the form is posted or not.
    if request.method == 'POST':
        # Validate the input value.
        if ChoosePair.validate() and ChoosePair.Send.data:
            # Create the student object.
            student = UC.Student(ChoosePair.Student.data)
            # Check whether these two student has the GPA or not.
            if str(student.getGPA()) == '' or student.getGPA() == 0 or student.getGPA() == None or str(student.getGPA()) == 'NULL':
                studentGPA = 3.0
            elif str(User.getGPA()) == '' or User.getGPA() == 0 or User.getGPA() == None or str(User.getGPA()) == 'NULL':
                userGPA = 3.0
            else:
                studentGPA = student.getGPA()
                userGPA = User.getGPA()
            # Compute the average GPA of these two students.
            avgGPA = round(((studentGPA + userGPA) / 2), 2)
            # Store the invitation info.
            result = db.storeInvitation(User.getID(), student.getID(), courseID, avgGPA)
            # Check whether store successful.
            if result:
                # Disconnect the database.
                db.__del__()
                return render_template('/Student Main Page.html', Username = Username, courseDict = cache.get('courseDict').items(), message = 'Send Successful!')
            else:
                # Set the message.
                message = "Database Error!"
                # Disconnect the database.
                db.__del__()
                return render_template('Invitation Page.html', Username = Username, studentDict = studentDict.items(), message = message)
        else:
            # Get the error message of the input value.
            if ChoosePair.Student.errors:
                message = ChoosePair.Student.errors[0]
            else:
                message = ''
            # Close the database connection.
            db.__del__()
            # Print the error message.
            return render_template('Invitation Page.html', Username = Username, studentDict = studentDict.items(), message = message)
    else:
        # Disconnect the database.
        db.__del__()
        return render_template('Invitation Page.html', Username = Username, studentDict = studentDict.items())

# The api for delete invitation.
@app.route('/Delete Invitation Page', methods = ['GET', 'POST'])
@login_required
def DeleteInvitationPage():
    # Create the database connection.
    db = Database.DatabaseOperations()
    # Get the user.
    User = cache.get('User')
    # Get the username.
    Username = User.getUsername()
    # Get the course ID.
    courseID = cache.get('courseID')
    # Get the invitee name.
    inviteeName = cache.get('inviteeName')
    # Indicate whether the form is posted or not.
    if request.method == 'POST':
        # Delete the rejected invitation.
        if db.deleteRejectedInviationForInviter(User.getID(), courseID):
            # Get the message.
            message = "Delete Successful"
            # Disconnect the database.
            db.__del__()
            return render_template('Student Main Page.html', Username = Username, courseDict = cache.get('courseDict').items(), message = message)
        else:
            # Set the message.
            message = "Database Error!"
            # Disconnect the database.
            db.__del__()
            return render_template('Delete Invitation Page.html', Username = Username, message = message)
    else:
        # Get the message.
        message = "Your invitation to %s has not been checked, please wait for the student to check your invitation! You can also delete this invitation." % (inviteeName)
        # Disconnect the database.
        db.__del__()
        return render_template('Delete Invitation Page.html', Username = Username, message = message)

# The api for reject confirm.
@app.route('/Reject Confirm Page', methods = ['GET', 'POST'])
@login_required
def RejectConfirmPage():
    # Create the database connection.
    db = Database.DatabaseOperations()
    # Get the user.
    User = cache.get('User')
    # Get the username.
    Username = User.getUsername()
    # Get the course ID.
    courseID = cache.get('courseID')
    # Get the invitee name.
    inviteeName = cache.get('inviteeName')
    # Indicate whether the form is posted or not.
    if request.method == 'POST':
        # Delete the rejected invitation.
        if db.deleteRejectedInviationForInviter(User.getID(), courseID):
            # Disconnect the database.
            db.__del__()
            return redirect('/Choose Team Page')
        else:
            # Set the message.
            message = "Database Error!"
            # Disconnect the database.
            db.__del__()
            return render_template('Reject Confirm Page.html', Username = Username, inviteeName = inviteeName, message = message)
    else:
        # Disconnect the database.
        db.__del__()
        return render_template('Reject Confirm Page.html', Username = Username, inviteeName = inviteeName)

# The api for invitation checking.
@app.route('/Invitation Checking Page', methods = ['GET', 'POST'])
@login_required
def InvitationCheckingPage():
    # Create the database connection.
    db = Database.DatabaseOperations()
    # Get the user.
    User = cache.get('User')
    # Get the username.
    Username = User.getUsername()
    # Get the course ID.
    courseID = cache.get('courseID')
    # Get the invitation info.
    invitationDict = cache.get('invitationDict')
    # Get the form team method info.
    methodInfo = cache.get('methodInfo')
    # Indicate whether the form is posted or not.
    if request.method == 'POST':
        # Check the user choose accept ot reject.
        if request.form.get('Accept'):
            # Check whether choose a invitation or not.
            if request.form.get('Pairs'):
                # Get the inviter ID.
                inviterID = request.form['Pairs']
                # Create the inviter object.
                inviter = UC.Student(inviterID)
                # Check whether these two student has the GPA or not.
                if str(inviter.getGPA()) == '' or inviter.getGPA() == 0 or inviter.getGPA() == None or str(inviter.getGPA()) == 'NULL':
                    inviterGPA = 3.0
                elif str(User.getGPA()) == '' or User.getGPA() == 0 or User.getGPA() == None or str(User.getGPA()) == 'NULL':
                    userGPA = 3.0
                else:
                    inviterGPA = inviter.getGPA()
                    userGPA = User.getGPA()
                # Compute the average GPA of these two students.
                avgGPA = round(((inviterGPA + userGPA) / 2), 2)
                # Update the pairs.
                result = db.updateInvitationState(inviterID, courseID, 1, avgGPA)
                # Check whether the update successful or not.
                if result:
                    # Reject other invitations.
                    for key, each in invitationDict.items():
                        if key != inviterID:
                            # Update the pairs.
                            result = db.updateInvitationState(key, courseID, -1, 0)
                            if result:
                                continue
                            else:
                                # Set the message.
                                message = "Database Error!"
                                # Disconnect the database.
                                db.__del__()
                                return render_template('Invitation Checking Page.html', Username = Username, invitationDict = invitationDict.items(), message = message)
                    # Reject the invitations for the student send this invitation.
                    for each in db.getInvitationInfo(inviterID, courseID):
                        # Update the pairs.
                        result = db.updateInvitationState(each[1], courseID, -1, 0)
                        if result:
                            continue
                        else:
                            # Set the message.
                            message = "Database Error!"
                            # Disconnect the database.
                            db.__del__()
                            return render_template('Invitation Checking Page.html', Username = Username, invitationDict = invitationDict.items(), message = message)
                else:
                    # Set the message.
                    message = "Database Error!"
                    # Disconnect the database.
                    db.__del__()
                    return render_template('Invitation Checking Page.html', Username = Username, invitationDict = invitationDict.items(), message = message)
                # Get all the pairs at present.
                pairs = []
                for each in db.getAllPairs(courseID):
                    pairs.append([each[1], each[2], each[4]])
                # Create the course object.
                course = NU.Course(courseID)
                # Get the max number of pairs this course could have.
                maxNumPairs = math.floor((course.getNumOfStudent() / 2))
                # Check whether all the pairs for this course have been formed.
                if len(pairs) == maxNumPairs:
                    # Check the form team method.
                    if methodInfo[0] == 'C':
                        # Get the number of team.
                        numOfteam = int(math.ceil(course.getNumOfStudent() / methodInfo[2]))
                        # Get the number of member in last team.
                        lastTeamMember = course.getNumOfStudent() % methodInfo[2]
                        # Set the dict to store the number of member in this team.
                        teamMemberCount = {}
                        # Store the team info into the database.
                        for ID in db.getAllTeamID(courseID):
                            teamMemberCount[ID[0]] = 0
                        # Get the first team's ID.
                        stratID = list(teamMemberCount.keys())[0]
                        # Get the last team's ID.
                        endID = stratID + numOfteam - 1
                        # Check the number of last team member.
                        if lastTeamMember % 2 == 1:
                            # Get all the student who enrolled in this course.
                            studentList = []
                            for each in db.getAllStudentID(courseID):
                                studentList.append(each[0])
                            # Get all the studen who has the pairs.
                            studentInPairs = []
                            for each in db.getAllPairs(courseID):
                                studentInPairs.append(each[1])
                                studentInPairs.append(each[2])
                            # Delete all the student ID in the student list which are also in the pairs.
                            temp = []
                            for each in studentList:
                                if each in studentInPairs:
                                    temp.append(each)
                            for each in temp:
                                studentList.remove(each)
                            # Create the student object.
                            student = UC.Student(studentList[0])
                            # Insert this student into the last team.
                            result = db.storeMemberInfo(student.getID(), endID, courseID)
                            # Check whether store successful or not.
                            if result:
                                teamMemberCount[endID] = teamMemberCount[endID] + 1
                            else:
                                # Set the message.
                                message = "Database Error!"
                                # Disconnect the database.
                                db.__del__()
                                return render_template('Invitation Checking Page.html', Username = Username, invitationDict = invitationDict.items(), message = message)
                        # Randomly set the member.
                        for each in pairs:
                            # Store the member info into the database.
                            while True:
                                # Randomly select the team ID.
                                teamID = random.randint(stratID, endID)
                                # Check whether the team ID is the last team.
                                if teamID == endID:
                                    # Check whether the last team is special.
                                    if lastTeamMember != 0:
                                        # Check whether the team is full.
                                        if teamMemberCount[teamID] == lastTeamMember:
                                                continue
                                        else:
                                            # Store the member info.
                                            result = db.storeMemberInfo(each[0], teamID, courseID)
                                            # Check whether store successful or not.
                                            if result:
                                                # Store another member info.
                                                result = db.storeMemberInfo(each[1], teamID, courseID)
                                                # Check whether store successful or not.
                                                if result:
                                                    # Reset the member number of this team.
                                                    teamMemberCount[teamID] = teamMemberCount[teamID] + 2
                                                    break
                                                else:
                                                    # Set the message.
                                                    message = "Database Error!"
                                                    # Disconnect the database.
                                                    db.__del__()
                                                    return render_template('Invitation Checking Page.html', Username = Username, invitationDict = invitationDict.items(), message = message)
                                            else:
                                                # Set the message.
                                                message = "Database Error!"
                                                # Disconnect the database.
                                                db.__del__()
                                                return render_template('Invitation Checking Page.html', Username = Username, invitationDict = invitationDict.items(), message = message)
                                    else:
                                        # Check whether the team is full.
                                        if teamMemberCount[teamID] == methodInfo[2]:
                                                continue
                                        else:
                                            # Store the member info.
                                            result = db.storeMemberInfo(each[0], teamID, courseID)
                                            # Check whether store successful or not.
                                            if result:
                                                # Store another member info.
                                                result = db.storeMemberInfo(each[1], teamID, courseID)
                                                # Check whether store successful or not.
                                                if result:
                                                    # Reset the member number of this team.
                                                    teamMemberCount[teamID] = teamMemberCount[teamID] + 2
                                                    break
                                                else:
                                                    # Set the message.
                                                    message = "Database Error!"
                                                    # Disconnect the database.
                                                    db.__del__()
                                                    return render_template('Invitation Checking Page.html', Username = Username, invitationDict = invitationDict.items(), message = message)
                                            else:
                                                # Set the message.
                                                message = "Database Error!"
                                                # Disconnect the database.
                                                db.__del__()
                                                return render_template('Invitation Checking Page.html', Username = Username, invitationDict = invitationDict.items(), message = message)
                                else:
                                    # Check whether the team is full.
                                    if teamMemberCount[teamID] == methodInfo[2]:
                                        continue
                                    else:
                                        # Store the member info.
                                        result = db.storeMemberInfo(each[0], teamID, courseID)
                                        # Check whether store successful or not.
                                        if result:
                                            # Store another member info.
                                            result = db.storeMemberInfo(each[1], teamID, courseID)
                                            # Check whether store successful or not.
                                            if result:
                                                # Reset the member number of this team.
                                                teamMemberCount[teamID] = teamMemberCount[teamID] + 2
                                                break
                                            else:
                                                # Set the message.
                                                message = "Database Error!"
                                                # Disconnect the database.
                                                db.__del__()
                                                return render_template('Invitation Checking Page.html', Username = Username, invitationDict = invitationDict.items(), message = message)
                                        else:
                                            # Set the message.
                                            message = "Database Error!"
                                            # Disconnect the database.
                                            db.__del__()
                                            return render_template('Invitation Checking Page.html', Username = Username, invitationDict = invitationDict.items(), message = message)
                        # Delete all pairs.
                        result = db.deleteAllPairs(courseID)
                        if result:
                            # Disconnect the database.
                            db.__del__()
                            return render_template("Student Main Page.html", Username = Username, courseDict = cache.get('courseDict').items(), message = "You have already get the team, please click the 'Choose' button again to get your teammate!")
                        else:
                            # Set the message.
                            message = "Database Error!"
                            # Disconnect the database.
                            db.__del__()
                            return render_template('Invitation Checking Page.html', Username = Username, invitationDict = invitationDict.items(), message = message)
                    else:
                        # Get the number of team.
                        numOfteam = int(math.ceil(course.getNumOfStudent() / methodInfo[2]))
                        # Get the number of member in last team.
                        lastTeamMember = course.getNumOfStudent() % methodInfo[2]
                        # Set the dict to store the number of member in this team.
                        teamMemberCount = {}
                        # Set the dict to store the sum of gpa of all members in the same team.
                        teamAvgGPA = {}
                        # Store the team info into the database.
                        for ID in db.getAllTeamID(courseID):
                            teamMemberCount[ID[0]] = 0
                            teamAvgGPA[ID[0]] = 0
                        # Get the first team's ID.
                        stratID = list(teamMemberCount.keys())[0]
                        # Get the last team's ID.
                        endID = stratID + numOfteam - 1
                        # Get ID and GPA of all student who enrolled into this course.
                        studentList = []
                        studentGPA = []
                        for each in db.getAllStudentID(courseID):
                            studentList.append(each[0])
                            # Create the student object.
                            student = UC.Student(each[0])
                            # Get the student GPA.
                            GPA = student.getGPA()
                            # Check whether the GPA is valid.
                            if str(GPA) == '' or GPA == 0 or GPA == None or str(GPA) == 'NULL':
                                GPA = 3.0
                                # Store the gpa.
                                studentGPA.append(GPA)
                            else:
                                # Store the gpa.
                                studentGPA.append(GPA)
                        # Get the standard gpa value for system to form team.
                        gpaStandard = round((sum(studentGPA) / len(studentGPA)), methodInfo[1])
                        # Check the number of last team member.
                        if lastTeamMember % 2 == 1:
                            # Get all the studen who has the pairs.
                            studentInPairs = []
                            for each in db.getAllPairs(courseID):
                                studentInPairs.append(each[1])
                                studentInPairs.append(each[2])
                            # Delete all the student ID in the student list which are also in the pairs.
                            temp = []
                            for i, each in enumerate(studentList):
                                if each in studentInPairs:
                                    temp.append(each)
                                else:
                                    GPA = studentGPA[i]
                            for each in temp:
                                studentList.remove(each)
                            # Create the student object.
                            student = UC.Student(studentList[0])
                            # Insert this student into the last team.
                            result = db.storeMemberInfo(student.getID(), endID, courseID)
                            # Check whether store successful or not.
                            if result:
                                teamMemberCount[endID] = teamMemberCount[endID] + 1
                                teamAvgGPA[endID] = GPA
                            else:
                                # Set the message.
                                message = "Database Error!"
                                # Disconnect the database.
                                db.__del__()
                                return render_template('Invitation Checking Page.html', Username = Username, invitationDict = invitationDict.items(), message = message)
                        # Randomly set the member.
                        for each in pairs:
                            # Store the member info into the database.
                            while True:
                                # Randomly select the team ID.
                                teamID = random.randint(stratID, endID)
                                # Check whether the team ID is the last team.
                                if teamID == endID:
                                    # Check whether the last team is special.
                                    if lastTeamMember != 0:
                                        # Check whether the team is full.
                                        if teamMemberCount[teamID] == lastTeamMember:
                                            continue
                                        else:
                                            # Indicate whether the pair is the first pair in this team.
                                            if teamMemberCount[teamID] == 0:
                                                # Store the member info.
                                                result = db.storeMemberInfo(each[0], teamID, courseID)
                                                # Check whether store successful or not.
                                                if result:
                                                    # Store another member info.
                                                    result = db.storeMemberInfo(each[1], teamID, courseID)
                                                    # Check whether store successful or not.
                                                    if result:
                                                        # Reset the member number of this team.
                                                        teamMemberCount[teamID] = teamMemberCount[teamID] + 2
                                                        # Stpre the student GPA.
                                                        teamAvgGPA[teamID] = each[2]
                                                        break
                                                    else:
                                                        # Set the message.
                                                        message = "Database Error!"
                                                        # Disconnect the database.
                                                        db.__del__()
                                                        return render_template('Invitation Checking Page.html', Username = Username, invitationDict = invitationDict.items(), message = message)
                                                else:
                                                    # Set the message.
                                                    message = "Database Error!"
                                                    # Disconnect the database.
                                                    db.__del__()
                                                    return render_template('Invitation Checking Page.html', Username = Username, invitationDict = invitationDict.items(), message = message)
                                            else:
                                                # Calculate the team gpa when this student add into this team.
                                                testGPA = round((teamAvgGPA[teamID] * teamMemberCount[teamID] + each[2] * 2) / (teamMemberCount[teamID] + 2), methodInfo[1])
                                                # Check whether the GPA is valid.
                                                if abs(testGPA - gpaStandard) <= 0.3:
                                                    # Store the member info.
                                                    result = db.storeMemberInfo(each[0], teamID, courseID)
                                                    # Check whether store successful or not.
                                                    if result:
                                                        # Store another member info.
                                                        result = db.storeMemberInfo(each[1], teamID, courseID)
                                                        # Check whether store successful or not.
                                                        if result:
                                                            # Reset the member number of this team.
                                                            teamMemberCount[teamID] = teamMemberCount[teamID] + 2
                                                            # Stpre the student GPA.
                                                            teamAvgGPA[teamID] = testGPA
                                                            break
                                                        else:
                                                            # Set the message.
                                                            message = "Database Error!"
                                                            # Disconnect the database.
                                                            db.__del__()
                                                            return render_template('Invitation Checking Page.html', Username = Username, invitationDict = invitationDict.items(), message = message)
                                                    else:
                                                        # Set the message.
                                                        message = "Database Error!"
                                                        # Disconnect the database.
                                                        db.__del__()
                                                        return render_template('Invitation Checking Page.html', Username = Username, invitationDict = invitationDict.items(), message = message)
                                                else:
                                                    continue
                                    else:
                                        # Check whether the team is full.
                                        if teamMemberCount[teamID] == methodInfo[2]:
                                            continue
                                        else:
                                            # Indicate whether the pair is the first pair in this team.
                                            if teamMemberCount[teamID] == 0:
                                                # Store the member info.
                                                result = db.storeMemberInfo(each[0], teamID, courseID)
                                                # Check whether store successful or not.
                                                if result:
                                                    # Store another member info.
                                                    result = db.storeMemberInfo(each[1], teamID, courseID)
                                                    # Check whether store successful or not.
                                                    if result:
                                                        # Reset the member number of this team.
                                                        teamMemberCount[teamID] = teamMemberCount[teamID] + 2
                                                        # Stpre the student GPA.
                                                        teamAvgGPA[teamID] = each[2]
                                                        break
                                                    else:
                                                        # Set the message.
                                                        message = "Database Error!"
                                                        # Disconnect the database.
                                                        db.__del__()
                                                        return render_template('Invitation Checking Page.html', Username = Username, invitationDict = invitationDict.items(), message = message)
                                                else:
                                                    # Set the message.
                                                    message = "Database Error!"
                                                    # Disconnect the database.
                                                    db.__del__()
                                                    return render_template('Invitation Checking Page.html', Username = Username, invitationDict = invitationDict.items(), message = message)
                                            else:
                                                # Calculate the team gpa when this student add into this team.
                                                testGPA = round((teamAvgGPA[teamID] * teamMemberCount[teamID] + each[2] * 2) / (teamMemberCount[teamID] + 2), methodInfo[1])
                                                # Check whether the GPA is valid.
                                                if abs(testGPA - gpaStandard) <= 0.3:
                                                    # Store the member info.
                                                    result = db.storeMemberInfo(each[0], teamID, courseID)
                                                    # Check whether store successful or not.
                                                    if result:
                                                        # Store another member info.
                                                        result = db.storeMemberInfo(each[1], teamID, courseID)
                                                        # Check whether store successful or not.
                                                        if result:
                                                            # Reset the member number of this team.
                                                            teamMemberCount[teamID] = teamMemberCount[teamID] + 2
                                                            # Stpre the student GPA.
                                                            teamAvgGPA[teamID] = testGPA
                                                            break
                                                        else:
                                                            # Set the message.
                                                            message = "Database Error!"
                                                            # Disconnect the database.
                                                            db.__del__()
                                                            return render_template('Invitation Checking Page.html', Username = Username, invitationDict = invitationDict.items(), message = message)
                                                    else:
                                                        # Set the message.
                                                        message = "Database Error!"
                                                        # Disconnect the database.
                                                        db.__del__()
                                                        return render_template('Invitation Checking Page.html', Username = Username, invitationDict = invitationDict.items(), message = message)
                                                else:
                                                    continue
                                else:
                                    # Check whether the team is full.
                                    if teamMemberCount[teamID] == methodInfo[2]:
                                        continue
                                    else:
                                        # Indicate whether the pair is the first pair in this team.
                                        if teamMemberCount[teamID] == 0:
                                            # Store the member info.
                                            result = db.storeMemberInfo(each[0], teamID, courseID)
                                            # Check whether store successful or not.
                                            if result:
                                                # Store another member info.
                                                result = db.storeMemberInfo(each[1], teamID, courseID)
                                                # Check whether store successful or not.
                                                if result:
                                                    # Reset the member number of this team.
                                                    teamMemberCount[teamID] = teamMemberCount[teamID] + 2
                                                    # Stpre the student GPA.
                                                    teamAvgGPA[teamID] = each[2]
                                                    break
                                                else:
                                                    # Set the message.
                                                    message = "Database Error!"
                                                    # Disconnect the database.
                                                    db.__del__()
                                                    return render_template('Invitation Checking Page.html', Username = Username, invitationDict = invitationDict.items(), message = message)
                                            else:
                                                # Set the message.
                                                message = "Database Error!"
                                                # Disconnect the database.
                                                db.__del__()
                                                return render_template('Invitation Checking Page.html', Username = Username, invitationDict = invitationDict.items(), message = message)
                                        else:
                                            # Calculate the team gpa when this student add into this team.
                                            testGPA = round((teamAvgGPA[teamID] * teamMemberCount[teamID] + each[2] * 2) / (teamMemberCount[teamID] + 2), methodInfo[1])
                                            # Check whether the GPA is valid.
                                            if abs(testGPA - gpaStandard) <= 0.3:
                                                # Store the member info.
                                                result = db.storeMemberInfo(each[0], teamID, courseID)
                                                # Check whether store successful or not.
                                                if result:
                                                    # Store another member info.
                                                    result = db.storeMemberInfo(each[1], teamID, courseID)
                                                    # Check whether store successful or not.
                                                    if result:
                                                        # Reset the member number of this team.
                                                        teamMemberCount[teamID] = teamMemberCount[teamID] + 2
                                                        # Stpre the student GPA.
                                                        teamAvgGPA[teamID] = testGPA
                                                        break
                                                    else:
                                                        # Set the message.
                                                        message = "Database Error!"
                                                        # Disconnect the database.
                                                        db.__del__()
                                                        return render_template('Invitation Checking Page.html', Username = Username, invitationDict = invitationDict.items(), message = message)
                                                else:
                                                    # Set the message.
                                                    message = "Database Error!"
                                                    # Disconnect the database.
                                                    db.__del__()
                                                    return render_template('Invitation Checking Page.html', Username = Username, invitationDict = invitationDict.items(), message = message)
                                            else:
                                                continue
                        # Delete all pairs.
                        result = db.deleteAllPairs(courseID)
                        if result:
                            # Disconnect the database.
                            db.__del__()
                            return render_template("Student Main Page.html", Username = Username, courseDict = cache.get('courseDict').items(), message = "You have already get the team, please click the 'Choose' button again to get your teammate!")
                        else:
                            # Set the message.
                            message = "Database Error!"
                            # Disconnect the database.
                            db.__del__()
                            return render_template('Invitation Checking Page.html', Username = Username, invitationDict = invitationDict.items(), message = message)
                else:
                    # Disconnect the database.
                    db.__del__()
                    return render_template("Student Main Page.html", Username = Username, courseDict = cache.get('courseDict').items(), message = "Accept Successful!")
            else:
                # Set the message.
                message = "Please choose an invitation!"
                # Disconnect the database.
                db.__del__()
                return render_template('Invitation Checking Page.html', Username = Username, invitationDict = invitationDict.items(), message = message)
        else:
            # Reject all the invitation.
            for key, each in invitationDict.items():
                # Update the pairs.
                result = db.updateInvitationState(each[0], courseID, -1, 0)
                if result:
                    continue
                else:
                    # Set the message.
                    message = "Database Error!"
                    # Disconnect the database.
                    db.__del__()
                    return render_template('Invitation Checking Page.html', Username = Username, invitationDict = invitationDict.items(), message = message)
            # Disconnect the database.
            db.__del__()
            return render_template('Student Main Page.html', Username = Username, courseDict = cache.get('courseDict').items(), message = 'Reject Successful!')
    else:
        # Disconnect the database.
        db.__del__()
        return render_template('Invitation Checking Page.html', Username = Username, invitationDict = invitationDict.items())

# The api for choose team with method A.
@app.route('/Choose Team With A Page', methods = ['GET', 'POST'])
@login_required
def ChooseTeamWithAPage():
    # Create the database connection.
    db = Database.DatabaseOperations()
    # Create the instance for choose team by method A.
    ChooseTeam = FV.ChooseTeamByAForm(request.form)
    # Get the user.
    User = cache.get('User')
    # Get the username.
    Username = User.getUsername()
    # Get the course ID.
    courseID = cache.get('courseID')
    # Get the team info.
    teamInfo = cache.get('teamInfo')
    # Indicate whether the form is posted or not.
    if request.method == 'POST':
        # Validate the input value.
        if ChooseTeam.validate() and ChooseTeam.Confirm.data:
            # Get the team ID.
            teamID = eval(request.form['Team'])[0]
            # Creat the team object.
            team = NU.Team(teamID)
            # Check whether the team is valid.
            if len(team.getMember()) >= team.getNumOfMember():
                # Get the message.
                message = "This team is full, please choose another one!"
                # Close the database connection.
                db.__del__()
                # Print the error message.
                return render_template('Choose Team With A.html', Username = Username, teamInfo = teamInfo.items(), message = message)
            else:
                # Store the info into member page.
                result = db.storeMemberInfo(User.getID(), teamID, courseID)
                # Check whether store successful.
                if result:
                    # Close the database connection.
                    db.__del__()
                    # Print the error message.
                    return redirect('/Student Main Page')
                else:
                    # Get the error message.
                    message = "Database Error!"
                    # Close the database connection.
                    db.__del__()
                    # Print the error message.
                    return render_template('Choose Team With A.html', Username = Username, teamInfo = teamInfo.items(), message = message)
        else:
            # Get the error message of the input value.
            if ChooseTeam.Team.errors:
                message = ChooseTeam.Team.errors[0]
            else:
                message = ''
            # Close the database connection.
            db.__del__()
            # Print the error message.
            return render_template('Choose Team With A.html', Username = Username, teamInfo = teamInfo.items(), message = message)
    else:
        # Disconnect the database.
        db.__del__()
        # Send the info into the form team page.
        return render_template('Choose Team With A.html', Username = Username, teamInfo = teamInfo.items())

# The api for teacher main page.
@app.route('/Teacher Main Page', methods = ['GET', 'POST'])
@login_required
def TeacherMainPage():
    # Create the database connection.
    db = Database.DatabaseOperations()
    # Create a instance of import file form.
    ImportFile = FV.ImportFileForm(request.form)
    # Create the add extra student info form object.
    AddStudentInfo = FV.AddExtraStudentInfo(request.form)
    # Create the export file form object.
    ExportFile = FV.ExportFileForm(request.form)
    # Create the edit submission form object.
    EditSubmission = FV.EditSubmissionForm(request.form)
    # Create the form team form object.
    FormTeam = FV.FormTeamForm(request.form)
    # Get the user.
    User = cache.get('User')
    # Get the username.
    Username = User.getUsername()
    # Get the course list.
    courseDict = {}
    # Get the course name.
    for ID in User.getCourseList():
        courseDict[ID] = db.getCourseInfo(ID)[0][1]
    # Store the course dict.
    cache.set('courseDict', courseDict, 10 * 60)
    # Indicate whether the form is posted or not.
    if request.method == 'POST':
        # Validate the input value.
        if ImportFile.validate() and ImportFile.Import.data:
            # Store the course ID.
            cache.set('courseID', ImportFile.Course.data, 10 * 60)
            # Go to the import file page.
            return redirect('/Import Student Info Page')
        else:
            # Validate the input value.
            if AddStudentInfo.validate() and AddStudentInfo.Add.data:
                # Store the course ID.
                cache.set('courseID', AddStudentInfo.Course.data, 10 * 60)
                # Store the coures name.
                cache.set('courseName', courseDict[AddStudentInfo.Course.data], 10 * 60)
                # Go to the import file page.
                return redirect('/Add Extra Student Page')
            else:
                # Validate the input value.
                if ExportFile.validate() and ExportFile.Export.data:
                    # Create the course object and the team object.
                    course = NU.Course(ExportFile.Course.data)
                    # Get the result of export file.
                    result, test = course.exportFile()
                    # Check the result.
                    if test:
                        # Close the database connection.
                        db.__del__()
                        # Set the message.
                        message = "Export Successful!"
                        return send_file(result.filename, attachment_filename = 'Contribution.xlsx', as_attachment = True)
                    else:
                        # Close the database connection.
                        db.__del__()
                        # Print the error message.
                        return render_template('Teacher Main Page.html', Username = Username, courseDict = courseDict.items(), message = result)
                else:
                    # Validate the input value.
                    if EditSubmission.validate() and EditSubmission.Edit.data:
                        # Store the course ID.
                        cache.set('courseID', EditSubmission.Course.data, 10 * 60)
                        # Close the database connection.
                        db.__del__()
                        # Go to the corresponding page.
                        return redirect('/Edit Submission Page')
                    else:
                        # Validate the input value.
                        if FormTeam.validate() and FormTeam.Form.data:
                            # Check whether the course has team ot nor.
                            if db.getAllTeamID(FormTeam.Course.data):
                                # Get the message.
                                message = "This course has formed the team!"
                                # Close the database connection.
                                db.__del__()
                                # Print the error message.
                                return render_template('Teacher Main Page.html', Username = Username, courseDict = courseDict.items(), message = message)
                            else:
                                if db.getAllStudentID(FormTeam.Course.data): 
                                    # Store the course ID.
                                    cache.set('courseID', FormTeam.Course.data, 10 * 60)
                                    # Close the database connection.
                                    db.__del__()
                                    # Go to the corresponding page.
                                    return redirect('/Form Team Page')
                                else:
                                    # Get the message.
                                    message = "Please import the student info first!"
                                    # Close the database connection.
                                    db.__del__()
                                    # Print the error message.
                                    return render_template('Teacher Main Page.html', Username = Username, courseDict = courseDict.items(), message = message)
                        else:
                            # Get the error message of the input value.
                            if ImportFile.Course.errors:
                                message = ImportFile.Course.errors[0]
                            elif AddStudentInfo.Course.errors:
                                message = AddStudentInfo.Course.errors[0]
                            elif ExportFile.Course.errors:
                                message = ExportFile.Course.errors[0]
                            elif EditSubmission.Course.errors:
                                message = EditSubmission.Course.errors[0]
                            elif FormTeam.Course.errors:
                                message = FormTeam.Course.errors[0]
                            else:
                                message = ''
                            # Close the database connection.
                            db.__del__()
                            # Print the error message.
                            return render_template('Teacher Main Page.html', Username = Username, courseDict = courseDict.items(), message = message)
    else:
        # Disconnect the database.
        db.__del__()
        return render_template('Teacher Main Page.html', Username = Username, courseDict = courseDict.items())

# The api for customize teacher main page.
@app.route('/Customize Teacher Main Page', methods = ['GET', 'POST'])
@login_required
def CustomizeTeacherMainPage():
    # Create the database connection.
    db = Database.DatabaseOperations()
    # Get the user.
    User = cache.get('User')
    # Get the username.
    Username = User.getUsername()
    # Get the course list.
    courseDict = {}
    # Get the course name.
    for ID in User.getCourseList():
        courseDict[ID] = db.getCourseInfo(ID)[0][1]
    # Create a course class.
    course = NU.Course(User.getCourseList()[0])
    # Delare the result.
    result = ''
    # Indicate whether the form is posted or not.
    if request.method == 'POST':
        # Reset the course name.
        for key, __  in courseDict.items():
            # Get the reset result.
            if request.form[key] == '':
                continue
            else:
                result, test = course.setCourseName(key, request.form[key])
                if test: # If successful.
                    courseDict[key] = request.form[key]
                    continue
                else: # If fail.
                    message = result
                    # Disconnect the database.
                    db.__del__()
                    # Print the error message.
                    return render_template('Customize Teacher Main Page.html', Username = Username, courseDict = courseDict.items(), message = message)
        # Get the message.
        if result:
            message = result
        else:
            message = "You have not make any change of course name!"
        # Disconnect the database.
        db.__del__()
        # Return back to the teacher main page.
        return render_template('Teacher Main Page.html', Username = Username, courseDict = courseDict.items(), message = message)
    else:
        # Disconnect the database.
        db.__del__()
        return render_template('Customize Teacher Main Page.html', Username = Username, courseDict = courseDict.items())

# The api for import student info page.
@app.route('/Import Student Info Page', methods = ['GET', 'POST'])
@login_required
def ImportStudentInfoPage():
    # Create the database connection.
    db = Database.DatabaseOperations()
    # Get the user.
    User = cache.get('User')
    # Get the username.
    Username = User.getUsername()
    # Get the course list.
    courseDict = {}
    # Get the course ID.
    courseID = cache.get('courseID')
    # Create the course object.
    course = NU.Course(courseID)
    # Indicate whether the form is posted or not.
    if request.method == 'POST':
        # Check whether the user input the file or not.
        if request.files.get('StudentInfo'): # If yes.
            # Store the student info.
            result, test = course.importFile(request.files)
            # Test whether the storing operation is successful or not.
            if test:    # If yes.
                # Get the course name.
                for ID in User.getCourseList():
                    courseDict[ID] = db.getCourseInfo(ID)[0][1]
                # Disconnect the database.
                db.__del__()
                # Return back to the teacher main page.
                return render_template('Teacher Main Page.html', Username = Username, courseDict = courseDict.items(), message = result)
            else:
                # Disconnect the database.
                db.__del__()
                return render_template('Import Student Info Page.html', Username = Username, message = result)
        else: # If no.
            # Set the message.
            message = "Please input an excel file first."
            # Disconnect the database.
            db.__del__()
            return render_template('Import Student Info Page.html', Username = Username, message = message)
    else:
        # Disconnect the database.
        db.__del__()
        return render_template('Import Student Info Page.html', Username = Username)

# The api for add extra student page.
@app.route('/Add Extra Student Page', methods = ['GET', 'POST'])
@login_required
def AddExtraStudentPage():
    # Create the database connection.
    db = Database.DatabaseOperations()
    # Create the check info form object.
    CheckInfo = FV.CheckStudentInfo(request.form)
    # Get the user.
    User = cache.get('User')
    # Get the username.
    Username = User.getUsername()
    # Get the course list.
    courseDict = {}
    # Get the course ID.
    courseID = cache.get('courseID')
    # Create the course object.
    course = NU.Course(courseID)
    # Indicate whether the form is posted or not.
    if request.method == 'POST':
        # Validate the input value.
        if CheckInfo.validate() and CheckInfo.Confirm.data:
            result, test = course.addExtraStudentInfo(CheckInfo.Name.data, CheckInfo.ID.data, CheckInfo.Email.data, eval(CheckInfo.GPA.data))
            # Test whether the storing operation is successful or not.
            if test:    # If yes.
                # Get the course name.
                for ID in User.getCourseList():
                    courseDict[ID] = db.getCourseInfo(ID)[0][1]
                # Disconnect the database.
                db.__del__()
                # Return back to the teacher main page.
                return render_template('Teacher Main Page.html', Username = Username, courseDict = courseDict.items(), message = result)
            else:
                # Disconnect the database.
                db.__del__()
                return render_template('Add Extra Student Page.html', Username = Username, message = result)
        else:
            # Get the error message of the input value.
            if CheckInfo.ID.errors:
                message = CheckInfo.ID.errors[0]
            elif CheckInfo.Name.errors:
                message = CheckInfo.Name.errors[0]
            elif CheckInfo.Email.errors:
                message = CheckInfo.Email.errors[0]
            elif CheckInfo.GPA.errors:
                message = CheckInfo.GPA.errors[0]
            else:
                message = ''
            # Close the database connection.
            db.__del__()
            # Print the error message.
            return render_template('Add Extra Student Page.html', Username = Username, message = message)
    else:
        # Disconnect the database.
        db.__del__()
        # Return to the login page.
        return render_template('Add Extra Student Page.html', Username = Username)

# The api for edit submission page.
@app.route('/Edit Submission Page', methods = ['GET', 'POST'])
@login_required
def EditSubmissionPage():
    # Create the database connection.
    db = Database.DatabaseOperations()
    # Get the user.
    User = cache.get('User')
    # Get the username.
    Username = User.getUsername()
    # Get the submission list.
    submissionDict = {}
    # Check the total percentage.
    count = {}
    # Get the course ID.
    courseID = cache.get('courseID')
    # Create the course object.
    course = NU.Course(courseID)
    # Get the submission list.
    for ID in course.getSubmissionList():
        # Get the submission info.
        submissionInfo = db.getSubmissionInfo(ID)
        # Get the submission name and percentage.
        temp = [submissionInfo[0][1], submissionInfo[0][2]*100]
        submissionDict[ID] = temp
        # Get the totle percentage.
        count[ID] = submissionInfo[0][2]
    # Indicate whether the form is posted or not.
    if request.method == 'POST':
        # Create the submission object.
        submission = NU.SubmissionItem(course.getSubmissionList()[0])
        # Modify the submission.
        for key, value in submissionDict.items():
            # Modify the title.
            if request.form[str(key)]:
                # Set the title.
                result, test = submission.setTitle(request.form[str(key)], key)
                # Check whether modify successful or not.
                if test:
                    # Modify the percentage.
                    if request.form[value[0]]:
                        # Get the percentage.
                        count[key] = eval(request.form[value[0]]) / 100
                        # Set the percentage.
                        result, test = submission.setPercentage(eval(request.form[value[0]]) / 100, key)
                        # Check whether modify successful or not.
                        if test:
                            continue
                        else:
                            # Disconnect the database.
                            db.__del__()
                            # Get the message.
                            return render_template('Edit Submission Page.html', Username = Username, submissionDict = submissionDict.items(), message = result)
                    else:
                        continue
                else:
                    # Disconnect the database.
                    db.__del__()
                    # Get the message.
                    return render_template('Edit Submission Page.html', Username = Username, submissionDict = submissionDict.items(), message = result)
            else:
                # Modify the percentage.
                if request.form[value[0]]:
                    # Get the percentage.
                    count[key] = eval(request.form[value[0]]) / 100
                    # Set the percentage.
                    result, test = submission.setPercentage(eval(request.form[value[0]]) / 100, key)
                    # Check whether modify successful or not.
                    if test:
                        continue
                    else:
                        # Disconnect the database.
                        db.__del__()
                        # Get the message.
                        return render_template('Edit Submission Page.html', Username = Username, submissionDict = submissionDict.items(), message = result)
                else:
                    continue
        # Check whether the total percentage is invalid.
        if sum(count.values()) <= 1:
            # Get the message.
            message = "Modify Successful!"
            # Disconnect the database.
            db.__del__()
            # Get the message.
            return render_template('Teacher Main Page.html', Username = Username, courseDict = cache.get('courseDict').items(), message = message)
        else:
            for key, value in submissionDict.items():
                # Set the percentage.
                result, test = submission.setPercentage(value[1]/100, key)
                # Check whether modify successful or not.
                if test:
                    continue
                else:
                    # Disconnect the database.
                    db.__del__()
                    # Get the message.
                    return render_template('Edit Submission Page.html', Username = Username, submissionDict = submissionDict.items(), message = "Database Error!")
            # Disconnect the database.
            db.__del__()
            # Get the message.
            return render_template('Edit Submission Page.html', Username = Username, submissionDict = submissionDict.items(), message = "The total percentage larger than 100%!")
    else:
        # Disconnect the database.
        db.__del__()
        # Return to the login page.
        return render_template('Edit Submission Page.html', Username = Username, submissionDict = submissionDict.items())

# The api for add submission.
@app.route('/Add Submission', methods = ['GET', 'POST'])
@login_required
def AddSubmission():
    # Create the database connection.
    db = Database.DatabaseOperations()
    # Create the add submission form object.
    AddSubmission = FV.AddSubmissionForm(request.form)
    # Get the user.
    User = cache.get('User')
    # Get the username.
    Username = User.getUsername()
    # Get the submission list.
    submissionDict = {}
    # Get the course ID.
    courseID = cache.get('courseID')
    # Create the course object.
    course = NU.Course(courseID)
    # Get the submission list.
    for ID in course.getSubmissionList():
        # Get the submission info.
        submissionInfo = db.getSubmissionInfo(ID)
        # Get the submission name and percentage.
        temp = [submissionInfo[0][1], submissionInfo[0][2]*100]
        submissionDict[ID] = temp
    # Indicate whether the form is posted or not.
    if request.method == 'POST':
        # Check the value.
        if AddSubmission.validate() and AddSubmission.Confirm.data:
            # Get the result.
            result, test = course.addSubmission(AddSubmission.Title.data, (eval(AddSubmission.Percentage.data) / 100))
            # Check whether the add successful.
            if test:
                # Get the message.
                message = "Add Successful!"
                # Disconnect the database.
                db.__del__()
                # Get the message.
                return render_template('Teacher Main Page.html', Username = Username, courseDict = cache.get('courseDict').items(), message = message)
            else:
                # Close the database connection.
                db.__del__()
                # Print the error message.
                return render_template('Edit Submission Page.html', Username = Username, submissionDict = submissionDict.items(), message = result)
        else:
            # Get the error message of the input value.
            if AddSubmission.Percentage.errors:
                message = AddSubmission.Percentage.errors[0]
            elif AddSubmission.Title.errors:
                message = AddSubmission.Title.errors[0]
            else:
                message = ''
            # Close the database connection.
            db.__del__()
            # Print the error message.
            return render_template('Edit Submission Page.html', Username = Username, submissionDict = submissionDict.items(), message = message)
    else:
        # Disconnect the database.
        db.__del__()
        # Return to the edit submission page.
        return render_template('Edit Submission Page.html', Username = Username, submissionDict = submissionDict.items())

# The api for form team.
@app.route('/Form Team Page', methods = ['GET', 'POST'])
@login_required
def FormTeamPage():
    # Create the database connection.
    db = Database.DatabaseOperations()
    # Get the user.
    User = cache.get('User')
    # Get the username.
    Username = User.getUsername()
    # Get the course ID.
    courseID = cache.get('courseID')
    # Create the course object.
    course = NU.Course(courseID)
    # Indicate whether the form is posted or not.
    if request.method == 'POST':
        # Get the method name.
        method = request.form['Method']
        # Check whether the method concerned the GPA.
        if method == 'D' or method == 'E':
            # Check whether the gpa bound and number of member is empty.
            if request.form['GPA'] == '' or request.form['Member'] == '':
                # Set the message.
                message = "Please set the GPA's float bound and the number of member and must be an integer!"
                # Disconnect the database.
                db.__del__()
                # Return to the edit submission page.
                return render_template('Form Team Page.html', Username = Username, message = message)
            else:
                try:
                    # Get the GPA bound.
                    gpaBound = eval(request.form['GPA'])
                    # Get the number of members.
                    memberNum = eval(request.form['Member'])
                    # Check whether the get the GPA bound is set.
                    if type(gpaBound) != int or gpaBound < 0:
                        # Set the message.
                        message = "Please set the GPA's float bound and must be an integer and larger than or equal zero!"
                        # Disconnect the database.
                        db.__del__()
                        # Return to the edit submission page.
                        return render_template('Form Team Page.html', Username = Username, message = message)
                    # Check whether the number of member is set.
                    elif memberNum <= 0 or type(memberNum) != int:
                        # Set the message.
                        message = "Please set the number of member for a team and must be an integer and larger than zero!"
                        # Disconnect the database.
                        db.__del__()
                        # Return to the edit submission page.
                        return render_template('Form Team Page.html', Username = Username, message = message)
                    else:
                        # Set the method info.
                        methodInfo = str([method, gpaBound, memberNum])
                        # Form the team.
                        result, test = course.formTeam(methodInfo)
                        # Check whether the form successful or not.
                        if test:
                            # Disconnect the database.
                            db.__del__()
                            # Get the message.
                            return render_template('Teacher Main Page.html', Username = Username, courseDict = cache.get('courseDict').items(), message = result)
                        else:
                            # Disconnect the database.
                            db.__del__()
                            # Return to the edit submission page.
                            return render_template('Form Team Page.html', Username = Username, message = result)
                except:
                    # Set the message.
                    message = "Please set the GPA's float bound and the number of member and must be an integer!"
                    # Disconnect the database.
                    db.__del__()
                    # Return to the edit submission page.
                    return render_template('Form Team Page.html', Username = Username, message = message)
        else:
            # Check whether the number of member is empty.
            if request.form['Member'] == '':
                # Set the message.
                message = "Please set the number of member and must be an integer!"
                # Disconnect the database.
                db.__del__()
                # Return to the edit submission page.
                return render_template('Form Team Page.html', Username = Username, message = message)
            else:
                try:
                    # Get the number of members.
                    memberNum = eval(request.form['Member'])
                    # Check whether the number of member is set.
                    if memberNum <= 0 or type(memberNum) != int:
                        # Set the message.
                        message = "Please set the number of member for a team and must be an integer and larger than zero!"
                        # Disconnect the database.
                        db.__del__()
                        # Return to the edit submission page.
                        return render_template('Form Team Page.html', Username = Username, message = message)
                    else:
                        # Set the method info.
                        methodInfo = str([method, -1, memberNum])
                        # Form the team.
                        result, test = course.formTeam(methodInfo)
                        # Check whether the form successful or not.
                        if test:
                            # Disconnect the database.
                            db.__del__()
                            # Get the message.
                            return render_template('Teacher Main Page.html', Username = Username, courseDict = cache.get('courseDict').items(), message = result)
                        else:
                            # Disconnect the database.
                            db.__del__()
                            # Return to the edit submission page.
                            return render_template('Form Team Page.html', Username = Username, message = result)
                except:
                    # Set the message.
                    message = "Please set the number of member and must be an integer!"
                    # Disconnect the database.
                    db.__del__()
                    # Return to the edit submission page.
                    return render_template('Form Team Page.html', Username = Username, message = message)
    else:
        # Disconnect the database.
        db.__del__()
        # Return to the edit submission page.
        return render_template('Form Team Page.html', Username = Username)

# The api for logout.
@app.route('/Logout')
@login_required
def Logout():
    # Clear the cache.
    cache.clear()
    # Logout.
    logout_user()
    # Return to the login page.
    return redirect('/Login')

# Run the app.
if __name__ == '__main__':
    app.debug = True
    app.run(host = "0.0.0.0", port = 5000)