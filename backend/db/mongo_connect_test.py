from pymongo import MongoClient

# ✅ 로컬 MongoDB 서버 주소
client = MongoClient("mongodb://localhost:27017/")

# ✅ 사용할 데이터베이스
db = client["DeepPhish"]

# ✅ 테스트: voice_meta 컬렉션에서 하나만 출력
doc = db.voice_meta.find_one()

print("✅ 연결 성공! voice_meta 첫 데이터:")
print(doc)
