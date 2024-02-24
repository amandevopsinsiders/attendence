from flask import Flask, render_template
import csv
from flask_frozen import Freezer
import sys

app = Flask(__name__)

@app.route('/')
def display_csv():
    with open('attendance_batch14.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)
    return render_template('index.html', rows=rows)

@app.route('/batch15')
def display_batch15_csv():
    with open('attendance_batch15.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)
    return render_template('batch15.html', rows=rows)

if __name__ == '__main__':
    freezer = Freezer(app)

    if len(sys.argv) > 1 and sys.argv[1] == 'freeze':
        freezer.freeze()
    else:
        app.run(debug=True)
