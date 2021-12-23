from flask import Flask, request, jsonify, abort
from flask.globals import request
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
    db='RxR',
)

def get_paginated_list(results, url, start, limit):
    start = int(start)
    limit = int(limit)
    count = len(results)
    if count < start or limit < 0:
        abort(404)
    # make response
    obj = {}
    obj['start'] = start
    obj['limit'] = limit
    obj['count'] = count
    # make URLs
    # make previous url
    if start == 1:
        obj['previous'] = ''
    else:
        start_copy = max(1, start - limit)
        limit_copy = start - 1
        obj['previous'] = url + '?start=%d&limit=%d' % (start_copy, limit_copy)
    # make next url
    if start + limit > count:
        obj['next'] = ''
    else:
        start_copy = start + limit
        obj['next'] = url + '?start=%d&limit=%d' % (start_copy, limit)
    # finally extract result according to bounds
    obj['results'] = results[(start - 1):(start - 1 + limit)]
    return obj

@app.route('/')
def hello_world():
    return 'Hello World xxx!'

@app.route('/311')
def get_311():
    year = request.args.get("year")
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM RxR.311_cleaned_data WHERE YEAR={} LIMIT 20'''.format(year))
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
    return jsonify(get_paginated_list(
        json_data, 
        '/311?year={}&'.format(year), 
        start=request.args.get('start', 1), 
        limit=request.args.get('limit', 5)
    ))

@app.route('/dob')
def get_dob():
    year = request.args.get("year")
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM RxR.dob_cleaned_data WHERE YEAR={} LIMIT 20'''.format(year))
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
    '''return jsonify(get_paginated_list(
        json_data, 
        '/dob?year={}&'.format(year), 
        start=request.args.get('start', 1), 
        limit=request.args.get('limit', 5)))'''
    return json.dumps(json_data)

if __name__ == '__main__':
    app.run()