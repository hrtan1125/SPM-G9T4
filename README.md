# SPM-G9T4
This application is implemented using node.js and flask, follows the steps to setup the application

A. Installation

    1. Download node.js from https://nodejs.org/en/download/

    2. In the terminal, run the following if you do not have that modules
        pip install Flask
        pip install flask-sqlalchemy
        pip install flask_cors
        pip install flask_testing
        pip install mysql-connector
        pip install python-dotenv

----------------------------------------------                                        

B. Database Setup

    1. Loads testDB.sql to setup the database
        This is the main data set for this LJPS application which contains all the data needed, including LMS data
    2. Only if want to test empty, loads testDB_empty.sql
    3. Start the Database Server if using localhost

----------------------------------------------

C. Run Backend

    1. Make sure .env exists in the folder
    2. Change the SQLALCHEMY_DATABASE_URI to your database url
    3. Run the following files in the terminal:
        a. roles.py
        b. skills.py
        c. learning_journey.py

----------------------------------------------

D. Run Frontend
    
    1. In the terminal, run:
        cd frontend
        npm install
        npm start

----------------------------------------------

E. Staff Accounts for Testing

    1. Admin - 130001
    2. Manager - 150008
    3. User/Learner - 150166