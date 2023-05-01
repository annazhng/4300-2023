import json
import os
import numpy as np
import nltk
import gensim.downloader as api
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment import SentimentIntensityAnalyzer
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
    return intersection / union

nltk.download('punkt')
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

wv = api.load('glove-wiki-gigaword-50')
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))


def doc2vec(text1):
    tokens1 = word_tokenize(text1)
    tokens1 = [w.lower() for w in tokens1 if not w.lower() in stop_words and w.isalpha()]
    if len(tokens1) == 0:
        return wv['a']
    try:
        vec1 = wv[tokens1[0]]
    except:
        vec1 = wv['a']
    for token in tokens1[1:]:
        try:
            vec1 = vec1 + wv[token]
        except:
            vec1 = vec1
    vec1 = vec1 / len(tokens1)
    return vec1

def word2vec_sim(text1, text2):
    vec1 = doc2vec(text1)
    vec2 = doc2vec(text2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1)*np.linalg.norm(vec2))

def find_related(user_text, review):
    tokens = list(set(word_tokenize(review)))
    tokens = [w.lower() for w in tokens if not w.lower() in stop_words and w.isalpha()]
    scores = []
    for token in tokens:
        scores.append(word2vec_sim(user_text,token))
    arg_sort = np.argsort(scores)
    arg_sort = np.flip(arg_sort)
    return [tokens[i] for i in arg_sort[:3]]

#returns 1 if positive review, 0 if neutrial, -1 if negative 
def sentiment_analysis(text):
    score = sia.polarity_scores(text)
    if score['compound'] >= 0.05:
        return 1
    elif score['compound'] <= -0.05:
        return -1
    else:
        return 0

def sql_search(user_input):
    query_sql = f"""
    SELECT name, id, round(avg(service), 2), round(avg(cleanliness), 2), round(avg(value), 2), locality, review_text
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
    keys = ["name", "id", "service", "cleanliness", "value", "locality", "review_text"]
    data = mysql_engine.query_selector(query_sql)
    dataset = [dict(zip(keys, i)) for i in data]
   
    sim_scores = []
    for rev in dataset: 
        score = word2vec_sim(user_input["text"], rev['review_text'])
        sentiment = sentiment_analysis(rev["review_text"])
        rev['sentiment'] = sentiment
        rev['score'] = round(score,2)
        rev['related_words'] = find_related(user_input['text'],rev['review_text'])
        sim_scores.append(score)
    for rev in dataset:
        review_list = rev['review_text'].split()
        for related in rev['related_words']:
            indices = [i for i, word in enumerate(review_list) if word == related]
            for i in indices:
                review_list[i] = review_list[i].upper()
        rev['review_text'] = " ".join(review_list)
    for rev in dataset:
        for i, word in enumerate(rev['related_words']):
            rev['related_words'][i] = word.upper()
    arg_sort = np.argsort(sim_scores)
    arg_sort = np.flip(arg_sort)
    return [dataset[i] for i in arg_sort]


@app.route("/", methods=['GET'])
def home():
    service = request.args.get('service')
    cleanliness = request.args.get('clean')
    value = request.args.get('value')
    locality = request.args.get('locality')
    text = request.args.get('text')
    valid_form = service and cleanliness and value and text
    output = ''
    message = ''
    outputLen = 0
    descriptors = 1
    if valid_form:
        user_input = {'cleanliness': cleanliness, 'service': service,
                      'value': value, 'locality': locality, 'text': text}
        output = sql_search(user_input)
        outputLen = len(output)
        if text == '':
            text = 'None'
            descriptors = 0
    else:
        if service or cleanliness or value or text:
            message = 'Please fill out all fields.'
    return render_template('base.html', service=service, cleanliness=cleanliness, value=value, locality=locality,
                           valid_form=valid_form, output=output, text=text, outputLen=outputLen, descriptors=descriptors,
                           message=message)


# enter mysql shell
# /usr/local/mysql/bin/mysql -uroot -p

# show contents of table
# USE hotels;
# SHOW TABLES;
# SELECT * FROM hotel_reviews;

# SET GLOBAL sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));
