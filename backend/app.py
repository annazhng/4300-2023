import json
import os
import numpy as np
import nltk
from collections import defaultdict
from nltk.tokenize import word_tokenize
from flask import Flask, render_template, request
from flask_cors import CORS
from helpers.MySQLDatabaseHandler import MySQLDatabaseHandler

# ROOT_PATH for linking with all your files. 
# Feel free to use a config.py or settings.py with a global export variable
os.environ["ROOT_PATH"] = os.path.abspath(os.path.join("..", os.curdir))

# These are the DB credentials for your OWN MySQL
# Don't worry about the deployment credentials, those are fixed
# You can use a different DB name if you want to
MYSQL_USER = "root"
MYSQL_USER_PASSWORD = "MayankRao16Cornell.edu"
MYSQL_PORT = 3306
MYSQL_DATABASE = "hotels"

mysql_engine = MySQLDatabaseHandler(
    MYSQL_USER, MYSQL_USER_PASSWORD, MYSQL_PORT, MYSQL_DATABASE
)

# Path to init.sql file. This file can be replaced with your own file for testing on localhost, but do NOT move the init.sql file
mysql_engine.load_file_into_db()
app = Flask(__name__)
CORS(app)
# Sample search, the LIKE operator in this case is hard-coded,
# but if you decide to use SQLAlchemy ORM framework,
# there's a much better and cleaner way to do this

def jaccard_sim(text1, text2):
    text1_set = set(word_tokenize(text1))
    text2_set = set(word_tokenize(text2))
    intersection = len(text1_set.intersection(text2_set))
    union = len(text1_set.union(text2_set))
    return len(intersection) / len(union)

def sql_search(user_input):
    nltk.download('punkt')
    if user_input['locality'] == 'new-york':
        user_input['locality'] = 'New York City'
    query_sql = f"""
    SELECT name, avg(service),avg(cleanliness), avg(value), locality, review_text
    FROM hotel_reviews
    WHERE locality = '%s'
    GROUP BY name
    HAVING
        AVG(cleanliness) >= '%s' AND
        AVG(service) >= '%s' AND
        AVG(value) >= '%s'
    ORDER BY (sum(cleanliness) + sum(service) + sum(value)) ASC
    LIMIT 100;
    """ % (
        user_input['locality'],
        user_input["cleanliness"],
        user_input["service"],
        user_input["value"]
    )
    keys = ["name", "service", "cleanliness", "value", "locality", "review_text"]
    data = mysql_engine.query_selector(query_sql)
    dataset = [dict(zip(keys, i)) for i in data]
    jacc_scores = []
    for rev in dataset: 
        score = jaccard_sim(user_input["text"], rev['review_text'])
        jacc_scores.append(score)
    arg_sort = np.argsort(jacc_scores)
    return [dataset[i] for i in arg_sort]


@app.route("/", methods=['GET'])
def home():
    service = request.args.get('service')
    cleanliness = request.args.get('clean')
    value = request.args.get('value')
    locality = request.args.get('locality')
    text = request.args.get('text')
    valid_form = service and cleanliness and value
    output = ''
    if valid_form:
        user_input = {'cleanliness': cleanliness, 'service': service,
                      'value': value, 'locality': locality, 'text': text}
        output = sql_search(user_input)
    return render_template('base.html', service=service, cleanliness=cleanliness, value=value, locality=locality,
                           valid_form=valid_form, output=output, text=text)

@app.route("/episodes")
def episodes_search():
    text = request.args.get("title")
    return sql_search(text)


# enter mysql shell
# /usr/local/mysql/bin/mysql -uroot -p

# show contents of table
# USE hotels;
# SHOW TABLES;
# SELECT * FROM hotel_reviews;

# SET GLOBAL sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));
