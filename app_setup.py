from flask import Flask
from flask_security import SQLAlchemyUserDatastore, RoleMixin, UserMixin, Security
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os


load_dotenv()
flask_test_env = os.getenv("FLASK_TEST_ENV")

app = Flask(__name__)

app.config['SECURITY_PASSWORD_SALT'] = '112232223'
app.config['SECRET_KEY'] = 'ISENSIOT-GROEP10'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{os.getenv("DB_USERNAME")}:' \
                                        f'{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:' \
                                        f'{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}'

app.config['SQLALCHEMY_DATABASE_URI_TEST'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Silence the deprecation warning
app.config['TESTING'] = True  # Enable testing mode
app.config['SQLALCHEMY_EXPIRE_ON_COMMIT'] = False

if flask_test_env == "test":
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=app.config['SQLALCHEMY_DATABASE_URI_TEST']
    )

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


user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

with app.app_context():
    db.create_all()


