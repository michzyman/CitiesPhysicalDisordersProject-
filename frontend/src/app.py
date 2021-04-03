from predictions import generate_predictions

from flask import Flask, request, render_template, send_from_directory
import uuid

app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
  return render_template('./index.html')

@app.route('/static/template_input.csv')
def download_input_template():
  return app.send_static_file('template_input.csv')

@app.route('/upload_file', methods=['POST'])
def upload_input_file():
  file = request.files['input-file']

  generated_filename = str(uuid.uuid4())
  file.save('user_files/uploads/{}'.format(generated_filename))

  generate_predictions(generated_filename)

  return send_from_directory('user_files/outputs', '{}-output.csv'.format(generated_filename))

if __name__ == '__main__':
  app.debug = True
  app.run(host='0.0.0.0')
