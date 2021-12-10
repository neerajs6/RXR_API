from flask import Flask
from flaskext.mysql import MySQL
import json
import pymysql

from datetime import datetime

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
    cursor.execute('''SELECT CREATED_DATE, CLOSED_DATE, BBL FROM RxR.311_cleaned_data LIMIT 20''')
    row_headers = [x[0] for x in cursor.description]
    rv = cursor.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    for i in json_data:
        if 'CREATED_DATE' in i.keys() and type(i['CREATED_DATE']) == datetime:
            i['CREATED_DATE'] = i['CREATED_DATE'].strftime("%Y/%m/%d")
        if 'CLOSED_DATE' in i.keys() and type(i['CLOSED_DATE']) == datetime:
            i['CLOSED_DATE'] = i['CLOSED_DATE'].strftime("%Y/%m/%d")
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