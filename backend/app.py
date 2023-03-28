import json
import os
from flask import Flask, render_template, request
from flask_cors import CORS
from helpers.MySQLDatabaseHandler import MySQLDatabaseHandler

# ROOT_PATH for linking with all your files.
# Feel free to use a config.py or settings.py with a global export variable
os.environ['ROOT_PATH'] = os.path.abspath(os.path.join("..", os.curdir))

# These are the DB credentials for your OWN MySQL
# Don't worry about the deployment credentials, those are fixed
# You can use a different DB name if you want to
MYSQL_USER = "root"
MYSQL_USER_PASSWORD = ""
MYSQL_PORT = 3306
MYSQL_DATABASE = "hotels"

mysql_engine = MySQLDatabaseHandler(
    MYSQL_USER, MYSQL_USER_PASSWORD, MYSQL_PORT, MYSQL_DATABASE)

# Path to init.sql file. This file can be replaced with your own file for testing on localhost, but do NOT move the init.sql file
mysql_engine.load_file_into_db()

app = Flask(__name__)
CORS(app)

# Sample search, the LIKE operator in this case is hard-coded,
# but if you decide to use SQLAlchemy ORM framework,
# there's a much better and cleaner way to do this


def sql_search(user_input):
    query_sql = f"""
    SELECT name, avg(service),avg(cleanliness), avg(value), locality, review_text
    FROM hotel_reviews
    GROUP BY name
    HAVING
        AVG(cleanliness) >= '%s' AND
        AVG(service) >= '%s' AND
        AVG(value) >= '%s'
    ORDER BY (sum(cleanliness) + sum(service) + sum(value)) DESC
    LIMIT 10;
    """%(user_input['cleanliness'], user_input['service'], user_input['value'])

    '''
    query_sql = f"""
    SELECT name, avg(service),avg(cleanliness), avg(value), locality, review_text
    FROM hotel_reviews
    GROUP BY name
    HAVING
        MIN(cleanliness) >= '%%{user_input['cleanliness']}%%' AND
        MIN(service) >= '%%{user_input['service']}%%' AND
        MIN(value) >= '%%{user_input['value']}%%'
    ORDER BY (sum(cleanliness) + sum(service) + sum(value)) DESC
    LIMIT 10;
    """'''

    keys = ["name", "service", "cleanliness", "value", "locality","review_text"]
    data = mysql_engine.query_selector(query_sql)
    return [dict(zip(keys, i)) for i in data]


@app.route("/", methods=['GET'])
def home():
    service = request.args.get('service')
    cleanliness = request.args.get('clean')
    value = request.args.get('value')
    valid_form = service and cleanliness and value
    output = ''
    if valid_form:
        user_input = {'cleanliness': cleanliness, 'service': service, 'value': value}
        output = sql_search(user_input)
    return render_template('base.html', service=service, cleanliness=cleanliness, value=value, valid_form=valid_form, output=output)


@app.route("/hotel_reviews")
def hotels_search():
    text = request.args.get("name")
    return sql_search(text)

# app.run(debug=True)

# enter mysql shell
# /usr/local/mysql/bin/mysql -uroot -p

# show contents of table
# USE hotels;
# SHOW TABLES;
# SELECT * FROM hotel_reviews;
