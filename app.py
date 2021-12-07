from flask import Flask
import pymysql
import json
app = Flask(__name__)

conn = pymysql.connect(
    host = 'endpoint link',
    port = '3306',
    user = 'master username',
    password = 'master password',
    db = 'db name'
)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/get_311')
def get_311():
    year = request.args.get("year")
    bble = request.args.get("bbl")

    cursor = conn.cursor()

    q = """
    SELECT * FROM cleaned_311 WHERE YEAR = {} and BBLE = {}
    """.format(year, bble)

    rv = cursor.execute(q)
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    return json.dumps(json_data)

@app.route('/get_dob')
def get_311():
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
