1.Running this project should have the following environment
flask
flask_login
werkzeug
wtforms
xlrd
xlsxwriter
pymysql
xampp to set the local database.

2.The database setting is in the Database Folder.
The Seed.sql just contains the course and teacher info.
The Seed_demo.sql contains all the info that the demo required.

3.The student info is stored in the Student.xlsx file.

4.There are three different teacher account, for each teacher we set different course for them.
Username	Password
Adam		Adam1001
Jim		Jim1002
Nina		Nina1001

5. For running this project. You can import the original database and running as you like.
You can also import the demo database and running with the following order.
Login as a teacher by using Nina's account.
Check all the buttons in the teacher's main page.
Then login as a student by using any accounts in the student database.
Check all the buttons in the student's main page.
If you want to check as a member, please click one of the student ID in the member database to get the member's password and email.
If you want to check as a leader, please click one of the student ID in the leader database to get the leader's password and email.
Then using that information to login.

6. If you compress the zip and the zip create a new folder which contains the folder named project.
Please copy the project and paste it outside of the zip folder, then running the systemAPI.py.