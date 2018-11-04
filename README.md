# SER-515 Project: **Online Airplane Reservation System** 
## Group: Virat

## Members: 
1.Harshita Kajal
2.Rakesh Mohan
3.Sakshi Chaudhary
4.Shashidhar Reddy Vanteru
5.Shubham Vyas
6.Srivan Reddy Gutha

### Sprint 1: 
16 Sep 2018 to 30 Sep 2018

Wesite Homepage launched and deployed on heroku. Following is the website URL as a deliverable for sprint 1.

### Sprint 2:
01 Oct 2018 to 15 Oct 2018

The user should be able to search for the flight details and browse through the flight and select one as part of deliverable for sprint 2.


### Sprint 3:
18 Oct 2018 to 31 Oct 2018

The user should be able to search and book any flight of their convenience as part of deliverable for sprint 3.




**https://sampleamigo.herokuapp.com/**


 # Instruction To Locally Setup The Application :


1. Git clone the repository from GitHub (https://github.com/svanter1/virat.git).
2. Install python 3.6 from https://www.python.org/downloads/, if not installed.
3. Install virtual environment by typing "pip install virtualenv" in Terminal/Command Prompt, if not installed.
4. Make sure that repository is pointed to master and change directory to project directory (virat).
5. Inside the project folder create a virtual environment venv by executing command "virtualenv venv" in Terminal/Command Prompt.
6. Activate the virtual environment by executing command "venv/Scripts/activate" in windows or "source venv/bin/activate" in mac.
7. Once in virtual environment venv install django and django-herouku by executing command "pip install django" and "pip install django-heroku" in Terminal/Command Prompt.
8. Install postgres Homebrew brew install postgres(for mac, for windows please follow the instruction in postgres website).
9. Start the postgres server and create a database called virat
    - Open the psql
    - CREATE DATABASE virat;
    - Then quit the psql using \q
    - Then import the data from the virat_db.txt script using psql virat < path of the file/virat_db.txt;
    - Create user id and password using CREATE USER postgres WITH PASSWORD 'postgres';
    - If you don't wish to create the new user and password the same can be modified in reservationSystem/settings.py at DATABASES.
10. Then execute command "python manage.py runserver" in the virtual environment to locally host the application, the application can be seen in the link http://127.0.0.1:8000.
11. If there is any error while running the application it might be due to the missing dependencies, please confirm if all the modules in requirements.txt exist in the system, if not please install them and try again.

