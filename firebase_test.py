import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
 
 
#Firebase database 인증 및 앱 초기화
cred = credentials.Certificate('naco-bot-firebase-adminsdk-yrm0i-1b91a9db3f.json')
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://naco-bot-default-rtdb.asia-southeast1.firebasedatabase.app/'
})
 
dir = db.reference() #기본 위치 지정
dir.update({'battle_tag':'Naco#0801'})