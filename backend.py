# coding=utf-8
import json
from flask import Flask, jsonify, request, redirect
from flask_cors import CORS
import random


def find(link):
    pic1 = str(random.randint(1, 146)) + '.jpg'
    pic2 = str(random.randint(1, 146)) + '.jpg'
    pic3 = str(random.randint(1, 146)) + '.jpg'
    pic4 = str(random.randint(1, 146)) + '.jpg'
    pic5 = str(random.randint(1, 146)) + '.jpg'
    pic6 = str(random.randint(1, 146)) + '.jpg'
    if link != '/img/click_to_upload.c55f93fa.jpg':
        return {'pic1': pic1, 'pic2': pic2, 'pic3': pic3, 'pic4': pic4, 'pic5': pic5, 'pic6': pic6}
    else:
        return {'pic1': '0.jpg', 'pic2': '0.jpg', 'pic3': '0.jpg', 'pic4': '0.jpg', 'pic5': '0.jpg', 'pic6': '0.jpg'}


app = Flask(__name__)


@app.route('/hello', methods=['GET', 'POST'])
def hello():
    if request.method == 'GET':
        return jsonify({
            'pic1': '2.jpg', 'pic2': '5.jpg', 'pic3': '11.jpg', 'pic4': '17.jpg', 'pic5': '22.jpg', 'pic6': '32.jpg'
        })
    else:
        a = request.form['imageurl']
        print(a)
        res = find(a)
        return jsonify(res)


if __name__ == '__main__':
    CORS(app, supports_credentials=True)
    app.run('0.0.0.0', port=3333)