import os
import urllib.request
from flask import Flask, request, redirect, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
import bgremove

# Start Flask App
app = Flask(__name__)

# Declare Constants
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads' )
BG = os.path.join(os.getcwd(), 'media/BGLandscape.jpg')
BGP = os.path.join(os.getcwd(), 'media/BGPortrait.jpg')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # check if the post request has the file part
    if 'file' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']

    if file.filename == '':
        resp = jsonify({'message' : 'No file selected for uploading'})
        resp.status_code = 400
        return resp

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # rotate file based on exif
        rotated = bgremove.rotate_jpeg(filepath)
         # use different backgrounds for portrait vs landscape photos
        bgToUse = BGP if rotated else BG
        print(bgToUse)

        converted = bgremove.replace_bg(filepath, bgToUse)
        converted.save('./static/output/' + filename)

        resp = jsonify({'url' : request.host + '/static/output/' + filename})
        resp.status_code = 201
        return resp
        
    else:
        resp = jsonify({'message' : 'Allowed file types are png, jpg, jpeg, gif'})
        resp.status_code = 400
        return resp

if __name__ == '__main__':
    app.run()