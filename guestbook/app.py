from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:1234@cluster0.9i5vz.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

#==============hy===============#

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/homework", methods=["POST"])
def homework_guest():
    now = datetime.now()
    name_receive = request.form['name_give']
    post_receive = request.form['post_give']

    doc = {
        'name':name_receive,
        'post':post_receive,
        'year':now.year,
        'month':now.month,
        'day':now.day,
        'hour': now.hour,
        'minute': now.minute
    }
    db.guest.insert_one(doc)

    return jsonify({'msg': '남기기 성공!'})

@app.route("/homework", methods=["GET"])
def homework_get():
    post_list = list(db.guest.find({}, {'_id': False}))
    return jsonify({'post': post_list})
#==============hy===============#

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)