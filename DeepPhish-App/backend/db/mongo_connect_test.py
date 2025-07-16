from pymongo import MongoClient
import time

# ✅ MongoDB 연결
client = MongoClient("mongodb://localhost:27017/")
db = client["DeepPhish"]
collection = db["voice_meta"]

# ✅ 테스트용 문서 삽입
doc = {
    "file_id": "test1234",
    "file_name": "test_audio.mp3",
    "saved_path": "/path/to/test_audio.mp3",
    "phone_number": "01012345678",
    "status": "uploaded",
    "created_at": time.time()
}
collection.insert_one(doc)

# ✅ 확인용 출력
print("✅ voice_meta 첫 데이터:")
print(collection.find_one({"file_id": "test1234"}))
