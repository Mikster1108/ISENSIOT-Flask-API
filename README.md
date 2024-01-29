# This is the readme for the Flask API of the ISENSIOT security camera project

## Installing dependencies
Install the dependencies from the requirements.txt using ```pip install -r requirements```. 

## Adding dependencies
If you install new dependencies for this project, add them to the requirements.txt using ```pip freeze > requirements.txt```.
####Make sure to be in a venv environment!

## Env setup
Make a copy of the env.example.txt and name it .env. After that, fill in the missing fields, 
the database fields are dependent on your database user settings. The access code can be whatever you like.

## Database setup
Create a database and name it ```isensiot_security_camera```. After that, run the flask app and the tables
will be created automatically.

