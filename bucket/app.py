from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
from datetime import datetime


from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:1234@cluster0.9i5vz.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def bucket():
    return render_template('bucket.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form['bucket_give']

    bucket_list = list(db.bucket.find({}, {'_id': False}))
    count = len(bucket_list)+1

    doc = {

        'num':count,
        'bucket':bucket_receive,
        'done':0

    }
    db.bucket.insert_one(doc)
    return jsonify({'msg': '등록 완료!'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive = request.form['num_give']
    db.bucket.update_one({'num':int(num_receive)}, {'$set': {'done': 1}})

    return jsonify({'msg': '완료 되었습니다!'})

@app.route("/bucket/cancel", methods=["POST"])
def bucket_cancel():
    num_receive = request.form['num_give']
    db.bucket.update_one({'num':int(num_receive)}, {'$set': {'done': 0}})

    return jsonify({'msg': '취소 되었습니다!'})


@app.route("/bucket", methods=["GET"])
def bucket_get():
    bucket_list = list(db.bucket.find({}, {'_id': False}))

    return jsonify({'bucket':bucket_list})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)