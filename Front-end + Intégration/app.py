import imghdr
import os
from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png']
app.config['UPLOAD_PATH'] = 'uploads'

#=========================validation image=========================================

def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413

#========================mise de l'image dans le dossier============================
@app.route('/')
def home():
    return render_template('/home.html')

@app.route('/app.html')
def index():
    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('app.html', files=files)

@app.route('/app.html', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
            file_ext != validate_image(uploaded_file.stream):
            return "Invalid image", 400
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    return '', 204

@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)

#===========mateo===================================================================
@app.route("/analyse")
def solutions():# fonction lancée au moment de l'appuye sur le bouton 
    #ici analyse uniquement 
    return render_template("solution1.html")

@app.route('/home.html')
def home1():
    return render_template('home.html')
