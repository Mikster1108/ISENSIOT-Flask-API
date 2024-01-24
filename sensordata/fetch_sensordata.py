from app_setup import SensorData, db, Video


def fetch_video_sensordata(video_name):
    video = db.session.query(Video).filter(Video.filename == video_name).first()

    if video:
        return db.session.query(SensorData).filter(SensorData.video_id == video.id).all()
    else:
        return []
