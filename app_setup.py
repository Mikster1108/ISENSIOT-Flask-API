from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_security import SQLAlchemyUserDatastore, RoleMixin, UserMixin, Security
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from flask_socketio import SocketIO
from dotenv import load_dotenv
import os
from common.fetch_file import get_all_file_paths
from common.error_handlers import bad_request, unauthorized, not_found, too_many_requests, internal_server_error
from db.create_user_roles import create_roles
from tests import in_testing_mode

load_dotenv()
flask_test_env = os.getenv("FLASK_TEST_ENV")

app = Flask(__name__)

CORS(app)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["30000 per day, 10000 per hour"],
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
app.config['DEFAULT_VIDEO_EXTENSION'] = 'mp4'


socketio = SocketIO(app=app, cors_allowed_origins="*")

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

    def serialize(self, token):
        return {
            'id': self.id,
            'email': self.email,
            'token': token
        }


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), unique=True)
    duration_sec = db.Column(db.Integer)
    video_data = db.relationship("SensorData", backref='video', lazy=True)


class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_found = db.Column(db.String(255))
    timestamp_ms = db.Column(db.Float)
    video_id = db.Column(db.Integer, db.ForeignKey("video.id"), nullable=False)


user_roles = db.Table('user_roles',
                      db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                      db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
                      )

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


VIDEO_FOOTAGE_PATH = os.path.join(os.getenv("NAS_DRIVE_MOUNT_PATH"), "Video-recordings")
VIDEO_PREVIEW_PATH = os.path.join(os.getenv("NAS_DRIVE_MOUNT_PATH"), "Video-previews")
RAW_FOOTAGE_PATH = os.path.join(os.getenv("NAS_DRIVE_MOUNT_PATH"), "Raw-footage")
DATASET_FACE_RECOGNITION_PATH = os.path.join(os.getenv("NAS_DRIVE_MOUNT_PATH"), "datasets-face-recognition")


app.register_error_handler(400, bad_request)
app.register_error_handler(401, unauthorized)
app.register_error_handler(404, not_found)
app.register_error_handler(429, too_many_requests)
app.register_error_handler(500, internal_server_error)


# Import here to prevent circular import
from machine_learning.object_recognition.detector_controller import run_analyzing_process
from video import fetch_all_video_paths, sort_videos, NotConnectedToNasException, InvalidFilenameException, generate_video_preview


def generate_folders():
    try:
        if not os.path.exists(RAW_FOOTAGE_PATH):
            os.mkdir(RAW_FOOTAGE_PATH)
        if not os.path.exists(VIDEO_FOOTAGE_PATH):
            os.mkdir(VIDEO_FOOTAGE_PATH)
        if not os.path.exists(VIDEO_PREVIEW_PATH):
            os.mkdir(VIDEO_PREVIEW_PATH)
        if not os.path.exists(DATASET_FACE_RECOGNITION_PATH):
            os.mkdir(DATASET_FACE_RECOGNITION_PATH)
    except FileNotFoundError:
        print("WARNING: Not connected to NAS, the Flask server cant function well without this.")


def fill_video_duration_cache():
    try:
        video_paths = fetch_all_video_paths()
        sort_videos(video_paths=video_paths, query_filter='duration')  # Fill duration cache
    except NotConnectedToNasException:
        print("WARNING: Not connected to NAS, the Flask server cant function well without this.")
    except InvalidFilenameException:
        print("WARNING: Some filenames are invalid, correct the filenames as soon as possible.")


def check_for_new_recordings():
    run_analyzing_process(raw_footage_dir_name="Raw-footage", analyzed_footage_dir_name="Video-recordings")


def generate_preview_for_recent_recordings():
    [(generate_video_preview(file)) for file in get_all_file_paths(VIDEO_FOOTAGE_PATH)]


def start_scheduler(time_interval_min):
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_for_new_recordings, trigger="interval", minutes=time_interval_min)
    scheduler.add_job(generate_preview_for_recent_recordings, trigger="interval", minutes=2)
    scheduler.start()


with app.app_context():
    db.create_all()
    create_roles()
    generate_folders()
    fill_video_duration_cache()
    start_scheduler(10)
