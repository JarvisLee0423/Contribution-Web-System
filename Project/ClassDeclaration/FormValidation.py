#=============================================================================================#
#       Copyright:      Seed
#       Date:           2020/5/10
#       File Name:      FormValidation.py
#       Description:    This file is used to declare all the form validation class.
#=============================================================================================#
from wtforms import Form, StringField, PasswordField, SubmitField, FileField, validators
from flask_login import UserMixin
from collections import Counter
import math

#=============================================================================================#
#       Login
#=============================================================================================#
# Create a class for login.
class UserLogin(UserMixin):
    # Initialize the user login class.
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
# Create a class for student login form.
class StudentLoginForm(Form):
    # Get each of the value.
    Username = StringField('Username', [validators.DataRequired(), validators.Length(min = 1)])
    Password = PasswordField('Password', [validators.DataRequired(), validators.Length(min = 6, max = 16)])
    Student = SubmitField('Student', [validators.DataRequired()])
# Create a class for teacher login form.
class TeacherLoginForm(Form):
    # Get each of the value.
    Username = StringField('Username', [validators.DataRequired(), validators.Length(min = 1)])
    Password = PasswordField('Password', [validators.DataRequired(), validators.Length(min = 5, max = 16)])
    Teacher = SubmitField('Teacher', [validators.DataRequired()])

#=============================================================================================#
#       Change Password
#=============================================================================================#
# Create a class for modify password form.
class ModifyPasswordForm(Form):
    # Get each of the value.
    Password = PasswordField('Password', [validators.DataRequired(), validators.Length(min = 8, max = 16)])
    Modify = SubmitField('Modify', [validators.DataRequired()])

#=============================================================================================#
#       Assess Leader
#=============================================================================================#
# Create a class for assess leader.
class AssessLeaderForm(Form):
    # Get each of the value.
    Course = StringField('Course', [validators.DataRequired()])
    Leader = SubmitField('Leader', [validators.DataRequired()])
# Create a class for update bonus.
class UpdateBonusForm(Form):
    # Get each of the value.
    Assessment = StringField('Assessment', [validators.DataRequired()])
    Confirm = SubmitField('Confirm', [validators.DataRequired()])

#=============================================================================================#
#       Select Leader
#=============================================================================================#
# Create a class for select leader.
class SelectLeaderForm(Form):
    # Get each of the value.
    Course = StringField('Course', [validators.DataRequired()])
    Vote = SubmitField('Vote', [validators.DataRequired()])
# Create a class for update leader.
class UpdateLeaderForm(Form):
    # Get each of the value.
    Leader = StringField('Leader', [validators.DataRequired()])
    Confirm = SubmitField('Confirm', [validators.DataRequired()])

#=============================================================================================#
#       Import and Export File
#=============================================================================================#
# Create a class for import file.
class ImportFileForm(Form):
    # Get each of the value.
    Course = StringField('Course', [validators.DataRequired()])
    Import = SubmitField('Import', [validators.DataRequired()])
# Create a class for export file.
class ExportFileForm(Form):
    # Get each of the value.
    Course = StringField('Course', [validators.DataRequired()])
    Export = SubmitField('Export', [validators.DataRequired()])

#=============================================================================================#
#       Add Extra Student Info
#=============================================================================================#
# Create a class for add extra student info.
class AddExtraStudentInfo(Form):
    # Get each of the value.
    Course = StringField('Course', [validators.DataRequired()])
    Add = SubmitField('Add', [validators.DataRequired()])
# Create a class for check student info.
class CheckStudentInfo(Form):
    # Get each of the value.
    ID = StringField('ID', [validators.DataRequired()])
    Name = StringField('Name', [validators.DataRequired(), validators.Length(min = 1, max = 8)])
    Email = StringField('Email', [validators.DataRequired()])
    GPA = StringField('GPA', [validators.DataRequired()])
    Confirm = SubmitField('Confirm', [validators.DataRequired()])

#=============================================================================================#
#       Edit Submission
#=============================================================================================#
# Create a class for edit submission.
class EditSubmissionForm(Form):
    # Get each of the value.
    Course = StringField('Course', [validators.DataRequired()])
    Edit = SubmitField('Edit', [validators.DataRequired()])
# Create a class for add submission.
class AddSubmissionForm(Form):
    # Get each of the value.
    Title = StringField('Title', [validators.DataRequired()])
    Percentage = StringField('Percentage', [validators.DataRequired()])
    Confirm = SubmitField('Confirm', [validators.DataRequired()])

#=============================================================================================#
#       Assess Member
#=============================================================================================#
# Create a class for submission showing.
class SubmissionShowingForm(Form):
    # Get each of the value.
    Course = StringField('Course', [validators.DataRequired()])
    Contribution = SubmitField('Contribution', [validators.DataRequired()])

#=============================================================================================#
#       Form Team
#=============================================================================================#
# Create a class for forming team.
class FormTeamForm(Form):
    # Get each of the value.
    Course = StringField('Course', [validators.DataRequired()])
    Form = SubmitField('Form', [validators.DataRequired()])
# Create a class for choose team.
class ChooseTeamForm(Form):
    # Get each of the value.
    Course = StringField('Course', [validators.DataRequired()])
    Choose = SubmitField('Choose', [validators.DataRequired()])
# Create a class for choose team by method A.
class ChooseTeamByAForm(Form):
    # Get each of the value.
    Team = StringField('Team', [validators.DataRequired()])
    Confirm = SubmitField('Confirm', [validators.DataRequired()])
# Create a class for choose a pair.
class ChoosePairForm(Form):
    # Get each of the value.
    Student = StringField('Student', [validators.DataRequired()])
    Send = SubmitField('Send', [validators.DataRequired()])