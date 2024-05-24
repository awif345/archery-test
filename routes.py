from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from models import db, User, Video
from config import Config
import os

routes = Blueprint('routes', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "User already exists"}), 400

    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "User registered successfully"}), 201

@routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        return jsonify({"msg": "Invalid credentials"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

@routes.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    if 'file' not in request.files:
        return jsonify({"msg": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"msg": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        user_id = User.query.filter_by(username=get_jwt_identity()).first().id
        file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(file_path)

        video = Video(title=filename, file_path=file_path, user_id=user_id)
        db.session.add(video)
        db.session.commit()

        return jsonify({"msg": "File uploaded successfully"}), 200

    return jsonify({"msg": "File not allowed"}), 400

@routes.route('/videos', methods=['GET'])
@jwt_required()
def get_videos():
    user_id = User.query.filter_by(username=get_jwt_identity()).first().id
    videos = Video.query.filter_by(user_id=user_id).all()
    return jsonify([{'title': video.title, 'date_uploaded': video.date_uploaded, 'file_path': video.file_path} for video in videos])
