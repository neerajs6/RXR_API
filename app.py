from flask import Flask
from flaskext.mysql import MySQL
import json
import pymysql

app = Flask(__name__)
mysql = MySQL(app)

conn = pymysql.connect(
    host='database-1.cbhzog3pc3ub.us-east-2.rds.amazonaws.com',
    port=3306,
    user='admin',
    password='RxR12345',
    #db='RxR',

)

@app.route('/')
def hello_world():
    return 'Hello World xxx!'

@app.route('/get_311')
def get_311():

    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM RxR.
    SampleTable''')
    row_headers = [x[0] for x in cursor.description]
    rv = cursor.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    return json.dumps(json_data)

@app.route('/get_dob')
def get_dob():
    year = request.args.get("year")
    bble = request.args.get("bbl")

    cursor = conn.cursor()

    q = """
    SELECT * FROM cleaned_dob WHERE YEAR = {} and BBLE = {}
    """.format(year, bble)

    rv = cursor.execute(q)
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    return json.dumps(json_data)


if __name__ == '__main__':
    app.run()
'http://domain.com/get_311?year=2018&bbl=some number'
