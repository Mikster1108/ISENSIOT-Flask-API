from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_security import SQLAlchemyUserDatastore, RoleMixin, UserMixin, Security
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os

from db.create_user_roles import create_roles
from tests import in_testing_mode

load_dotenv()
flask_test_env = os.getenv("FLASK_TEST_ENV")

app = Flask(__name__)

CORS(app)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["300 per day, 100 per hour"],
    storage_uri="memory://"
)

app.config['SECURITY_PASSWORD_SALT'] = '112232223'
app.config['SECRET_KEY'] = 'ISENSIOT-GROEP10'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{os.getenv("DB_USERNAME")}:' \
                                        f'{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:' \
                                        f'{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}'

app.config['SQLALCHEMY_DATABASE_URI_TEST'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Silence the deprecation warning
app.config['TESTING'] = True  # Enable testing mode
app.config['SQLALCHEMY_EXPIRE_ON_COMMIT'] = False

if in_testing_mode():
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=app.config['SQLALCHEMY_DATABASE_URI_TEST']
    )
    limiter.enabled = False  # Disable request limit during tests


db = SQLAlchemy(app)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    roles = db.relationship('Role', secondary='user_roles')
    fs_uniquifier = db.Column(db.String(64), unique=True)

    def serialize(self):
        return {
            'id': self.id,
            'email': self.email
        }


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), unique=True)
    duration = db.Column(db.Integer)


user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

from video import fetch_all_video_paths, sort_videos  # Import here to prevent circular import
video_paths = fetch_all_video_paths()
sort_videos(video_paths=video_paths, query_filter='duration')  # Fill duration cache

with app.app_context():
    db.create_all()
    create_roles()

