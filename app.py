from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
import math
import requests
from datetime import datetime
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.todayKcal


@app.route('/')
def main():
    return render_template("index.html")



## API 역할을 하는 부분
@app.route('/main', methods=['POST'])
def write_review():
    foodName_receive = request.form['foodName_give']
    foodDate_receive = request.form['foodDate_give']
    foodKcal_receive = request.form['foodKcal_give']
    now_receive = request.form['now_give']

    file = request.files["file_give"]

    extension = file.filename.split('.')[-1]
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    filename = f'file-{mytime}'
    save_to = f'static/{filename}.{extension}'
    file.save(save_to)

    doc = {
        'food_name':foodName_receive,
        'food_date':foodDate_receive,
        'food_kcal':foodKcal_receive,
        'file': f'{filename}.{extension}',
        'now':now_receive,
    }

    db.foodInfo.insert_one(doc)

    return jsonify({'msg': '저장 완료!'})

@app.route('/main', methods=['GET'])
def show_diary():
    foodInfos = list(db.foodInfo.find({}, {'_id': False}).sort("now", -1))



    return jsonify({'all_foods': foodInfos})



# 오늘의프로필 페이지
@app.route('/profile')
def profile():
    return render_template("profile.html")

# 로그인페이지
@app.route('/login')
def login():
    return render_template("login.html")


#오늘의프로필등록
@app.route('/api/profile', methods=['POST'])
def save_profile():
    myid_receive = request.form['myid_give']
    height_receive = request.form['heigt_give']
    weight_receive = request.form['weight_give']
    goal_cal_receive =request.form['goal_cal_give']
    h =int(height_receive)
    w =int(weight_receive)
    bmiscore = math.trunc(w/(h*h)*10000)
    bmi=""
    if(bmiscore>30):
        bmi="비만"
    elif(bmiscore>=25):
        bmi="과체중"
    elif(bmiscore>=19):
        bmi="정상"
    else:
        bmi="저체중"

    print(bmi)
    doc ={
        'myid':myid_receive,
        'height':height_receive,
        'weight':weight_receive,
        'goal_cal':goal_cal_receive,
        'bmi': bmi,
        'bmiscore':bmiscore
    }
    db.todayKcal.insert_one(doc)

    return jsonify({'msg': '등록 완료!'})

#오늘의 프로필 리스팅
@app.route('/api/profile', methods=['GET'])
def show_profile():
    myid_receive=request.args.get("myid")
    print(myid_receive)
    profiles = list(db.todayKcal.find({"myid":myid_receive},{'_id':False}))
    print(profiles)
    return jsonify({'profiles': profiles})

#오늘의 프로필 수정
@app.route('/api/profile', methods=['POST'])
def update_profile():
    myid_receive=request.args.get("myid")
    height_receive = request.form['heigt_give']
    weight_receive = request.form['weight_give']
    goal_cal_receive = request.form['goal_cal_give']
    h = int(height_receive)
    w = int(weight_receive)
    bmiscore = math.trunc(w / (h * h) * 10000)
    bmi = ""
    if (bmiscore > 30):
        bmi = "비만"
    elif (bmiscore >= 25):
        bmi = "과체중"
    elif (bmiscore >= 19):
        bmi = "정상"
    else:
        bmi = "저체중"

    print(myid_receive)
    db.users.update_one({'myid': myid_receive}, {'$set': {'height': height_receive}})
    db.users.update_one({'myid': myid_receive}, {'$set': {'weight': weight_receive}})
    db.users.update_one({'myid': myid_receive}, {'$set': {'goal_cal': goal_cal_receive}})
    db.users.update_one({'myid': myid_receive}, {'$set': {'bmi': bmi}})
    db.users.update_one({'myid': myid_receive}, {'$set': {'bmiscore': bmiscore}})

    return jsonify({'result': 'success'})




if __name__ == '__main__':

    app.run(debug=True)

    app.run('0.0.0.0', port=5000, debug=True)

