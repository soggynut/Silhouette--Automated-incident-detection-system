from flask import Flask, render_template, Response, jsonify, request, session
from flask_mail import Mail, Message
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired
import os
import cv2
from yol import video_detection

app = Flask(__name__)

app.config['SECRET_KEY'] = 'aleena'
app.config['UPLOAD_FOLDER'] = 'static/files'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'adityapillai992@gmail.com'
# replace with the password
app.config['MAIL_PASSWORD'] = '**** **** **** ****'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Run")


def generate_frames(path_x=''):
    yolo_output = video_detection(path_x)
    detection_flag = False  # Initialize detection_flag here
    for detection_ in yolo_output:
        frame, detection_flag = detection_
        ref, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    if detection_flag:
        with app.app_context():
            send_email()


@app.route('/send_email', methods=['POST'])
def send_email():
    msg = Message("Alert", sender='s77800542@gmail.com',
                  recipients=['aleena.csa2024@saintgits.org'])
    msg.body = "Incident detected"
    mail.send(msg)


def generate_frames_web(path_x):
    yolo_output = video_detection(path_x)
    for detection_ in yolo_output:
        ref, buffer = cv2.imencode('.jpg', detection_)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    session.clear()
    return render_template('indexproject.html')


@app.route("/webcam", methods=['GET', 'POST'])
def webcam():
    session.clear()
    return render_template('ui.html')


@app.route('/FrontPage', methods=['GET', 'POST'])
def front():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                               secure_filename(file.filename)))
        session['video_path'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                                             secure_filename(file.filename))
    return render_template('videoprojectnew.html', form=form)


@app.route('/video')
def video():
    return Response(generate_frames(path_x=session.get('video_path', None)), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/webapp')
def webapp():
    return Response(generate_frames_web(path_x=0), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)
