import json
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)
charset = 'utf-8'

@app.route('/')
def index():
    data = []
    with open('processing/processing_results.json', 'r') as f:
        result = json.load(f)
        data = result

    return render_template('index.html', data=data)

@app.route('/queries/<string:video>')
def get_query(video):
    return send_from_directory('queries', video)

@app.route('/database/<string:video>')
def get_database(video):
    return send_from_directory('database', video)

@app.route('/processing/<int:index>')
def get_result(index):
    with open('processing/processing_results.json', r) as f:
        pass


    return 0

if __name__ == '__main__':
    app.run()