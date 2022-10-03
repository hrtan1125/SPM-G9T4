# SPM-G9T4

HOW TO RUN

In Python files:

Make sure SQLALCHEMY_DATABASE_URI is correct, yours might be mysql+mysqlconnector://root:root (if root is your password)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:' + \
                                        '@localhost:3306/projectDB'
                                        
FRONTEND
cd/frontend
npm install
npm start
