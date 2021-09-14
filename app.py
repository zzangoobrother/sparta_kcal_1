from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.todayKcal


@app.route('/')
def main():
    return render_template("main.html")



## API 역할을 하는 부분
@app.route('/main', methods=['POST'])
def write_review():
    foodName_receive = request.form['foodName_give']
    foodDate_receive = request.form['foodDate_give']
    foodKcal_receive = request.form['foodKcal_give']

    doc = {
        'food_name':foodName_receive,
        'food_date':foodDate_receive,
        'food_kcal':foodKcal_receive
    }

    db.foodInfo.insert_one(doc)

    return jsonify({'msg': '저장 완료!'})



if __name__ == '__main__':
    app.run(debug=True)