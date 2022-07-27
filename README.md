# 모든 Project에 공통으로 사용된 기능

Flask

ajax콜을 통해 mongodb에 저장

## mongodbprac

-----------------------------------
```mongodbprac.py

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:1234@cluster0.9i5vz.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

# 저장 db추가 - 예시
doc = {'name':'bobby','age':21}
db.users.insert_one(doc)

# 한 개 찾기 - 예시
user = db.users.find_one({'name':'bobby'})

# 여러개 찾기 - 예시 ( _id 값은 제외하고 출력)
all_users = list(db.users.find({},{'_id':False}))

# 바꾸기 - 예시
db.users.update_one({'name':'bobby'},{'$set':{'age':19}})

# 지우기 - 예시
db.users.delete_one({'name':'bobby'})

```
-----------------------------------

# bucket
```app.py
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
 ...
```
num API에 count = len(bucket_list)+1 하여 num을 고유넘버로 넣어주고

```bucket.html
function show_bucket() { 
    ...
  if (done == 0){  
                    temp_html =`<li>  
 <h2>✅ ${bucket}</h2>  
 <button onclick="done_bucket(${num})" type="button" class="btn btn-outline-primary">완료!</button>  
 </li>`  
  }else{  
                    temp_html=`<li>  
 <h2 class="done">✅ ${bucket}</h2>  
 <button onclick="cancel_bucket(${num})" type="button" class="btn btn-outline-danger">취소</button> 
 ...
 }
```
(done == 0) 미완료상태 일때
완료버튼을 보여주고 고유 넘버마다 버튼을 부여하여 완료 취소를 관리한다.

# Moive
크롤링을 위한 **BeautifulSoup**,  사용

네이버 영화 https://movie.naver.com/ 에서 영화 url을 끌어다 넣으면

영화 **meta 데이터**의 **영화 이미지(image,url)**,

**영화 제목(title)**, **영화 줄거리(description)** 를

크롤링하여 ajax콜을 통해 mongodb에 저장

```index.html
function posting() {  
    let url = $('#url').val()  
    let star = $('#star').val()  
    let comment = $('#comment').val()  
  
    $.ajax({  
        type: 'POST',  
  url: '/movie',  
  data: {url_give: url, star_give: star, comment_give: comment},  
  success: function (response) {  
            alert(response['msg'])  
            window.location.reload()  
        }  
    });  
}
```
````app.py
@app.route("/movie", methods=["POST"])  
def movie_post():  
    url_receive = request.form['url_give']  
    star_receive = request.form['star_give']  
    comment_receive = request.form['comment_give']  
  
    headers = {  
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}  
    data = requests.get(url_receive, headers=headers)  
  
    soup = BeautifulSoup(data.text, 'html.parser')  
  
    title = soup.select_one('meta[property="og:title"]')['content']  
    image = soup.select_one('meta[property="og:image"]')['content']  
    desc = soup.select_one('meta[property="og:description"]')['content']  
  
    doc = {  
        'title':title,  
  'image':image,  
  'desc':desc,  
  'star':star_receive,  
  'comment':comment_receive  
    }  
    db.movies.insert_one(doc)  
    return jsonify({'msg':'저장 완료'})
````
