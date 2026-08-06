'''this is a top level script to let flask know where the instance of the app is
this script is what should be defined while letting flask know which instance of the app to run
e.g; export FLASK_APP=microblog.py'''
from app import app, db
import sqlalchemy as sa
import sqlalchemy.orm as so
from app.models import User, Post


'''configuring flask shell context, which is a list of other symbols to pre-import
it helps to test things out in the terminal without having to explicitly import everything
the below function creates a shell context that adds the database instance and models to the shell session:
'''

#When the flask shell command runs, it will invoke this function and register the items returned by it in the shell session.
@app.shell_context_processor #this decorator registers the function as a shell context function.
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Post': Post}