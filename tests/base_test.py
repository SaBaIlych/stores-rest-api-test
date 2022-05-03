"""
BaseTest

This class should be the parent class to each non-unit test.
It allows for instantiation of the database dynamically
and makes sure that it is a new, blank database each time.
"""

from unittest import TestCase
from app import app
from db import db


class BaseTest(TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        app.config['DEBUG'] = False # we change config debug to false so we get all tests are passed during testing
        app.config['PROPAGATE_EXCEPTIONS'] = True #  long description about it in line 37
        with app.app_context():
            db.init_app(app)

    def setUp(self):
        # Make sure database exists
        with app.app_context():
            db.create_all()
        # Get a test client
        self.app = app.test_client
        self.app_context = app.app_context

    def tearDown(self):
        # Database is blank
        with app.app_context():
            db.session.remove()
            db.drop_all()

# Propagate exceptions makes it so that when an exception happens in your code it is bubbled up through the flask hierarchy
# and it is caught by the error handlers
# OK, if propagate exceptions is set for you automatically when debug is true, but as we set debug to false
# propagate exceptions becomes false and the error handlers start failing.
# And as soon as an exception happens in flask, it automatically responds with a five hundred error, internal server error.
# And it does that so that any unhandled exceptions don't give any clients information about your system.
# And because that can happen as well. So in this case, we can set propagate exceptions and they'll be fine.

# You may wonder then what happens when we set debug to false in our main application and we get a JWT error?
# Well, this error handler won't and won't show an error.
# Instead, you'll get a five hundred error.
# So we'll have to handle that error differently in our rest API.