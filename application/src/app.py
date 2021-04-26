# Some file management code modeled after https://github.com/weirdindiankid/BostonStreetCaster

from classifier.predictions import generate_predictions

from flask import Flask, request, render_template, send_from_directory, send_file
import uuid
import os
import shutil

app = Flask(__name__, template_folder='templates')

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
USER_FILES = os.path.join(APP_ROOT, 'user_files/')
CSV_UPLOAD_PATH = os.path.join(USER_FILES, 'upload/')
OUTPUT_PATH = os.path.join(USER_FILES, 'output/')

@app.route('/')
def individual_input():
    return render_template('index.html')

@app.route('/static/input_template.csv')
def download_input_template():
    return app.send_static_file('input_template.csv')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['input_file']
    api_key = request.form['api_key']

    reset_user_files()

    upload_filepath = os.path.join(CSV_UPLOAD_PATH, str(uuid.uuid4()))
    file.save(upload_filepath)

    output_filepath = os.path.join(OUTPUT_PATH, str(uuid.uuid4()))
    generate_predictions(upload_filepath, output_filepath, api_key)

    return send_file(output_filepath, attachment_filename='output.csv', as_attachment=True)

def reset_user_files():
    if not os.path.isdir(USER_FILES):
        os.mkdir(USER_FILES)

    if not os.path.isdir(CSV_UPLOAD_PATH):
        os.mkdir(CSV_UPLOAD_PATH)
    else:
        shutil.rmtree(CSV_UPLOAD_PATH)
        os.mkdir(CSV_UPLOAD_PATH)

    if not os.path.isdir(OUTPUT_PATH):
        os.mkdir(OUTPUT_PATH)
    else:
        shutil.rmtree(OUTPUT_PATH)
        os.mkdir(OUTPUT_PATH)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
