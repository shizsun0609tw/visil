import json
import os
import subprocess
import time
from flask import Flask, render_template, send_from_directory, request, redirect, url_for
from werkzeug.utils import secure_filename

# flask run --reload --host 140.113.210.7

app = Flask(__name__)
charset = 'utf-8'

ALLOWED_EXTENSIONS = set(['mp4'])
UPLOAD_PATH = 'upload/'

@app.route('/')
def index():
    result_prefix = 'processing_results_'
    result_folder = 'processing/'
    arg = request.args.get('jsonfile')
    jsonfile = result_prefix + (arg if arg else "queries") + ".json"
    
    with open(result_folder + jsonfile, 'r') as f:
        result = json.load(f)

    files = os.listdir(result_folder)
    files = [x.split(result_prefix)[1].replace(".json", "") for x in files if result_prefix in x]

    data = {'results': result,
            'jsonfile': files}
    
    return render_template('index.html', data=data)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def exe_visil(folder_name):
    with open('command.txt', 'r') as f:
        commands = f.readlines()
        for command in commands:
            command = command.replace('$(queries_path)', 'upload/' + folder_name)
            command = command.replace('$(database_path)', 'database')
            command = command.replace('$(results)', folder_name)

            print('Start command:')
            print('\t ' + command)
            process = subprocess.Popen(command, shell=True)
            process.wait()
            print('End command')

@app.route('/', methods=['POST'])
def upload_video():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        current_time = time.strftime("%m_%d_%H_%M_%S", time.localtime())
        os.makedirs(UPLOAD_PATH + current_time + '/')
        file.save(UPLOAD_PATH + current_time + '/' + filename)
        exe_visil(current_time)

    return index()

@app.route('/upload/<string:folder>/<string:video>')
def get_upload(folder, video):
    return send_from_directory('upload/' + folder, video)
            
@app.route('/queries/<string:video>')
def get_query(video):
    return send_from_directory('queries', video)

@app.route('/database/<string:video>')
def get_database(video):
    return send_from_directory('database', video)

if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = UPLOAD_PATH
    app.run()