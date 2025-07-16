from pymongo import MongoClient
import gridfs
import os
from datetime import datetime

def store_wav_to_gridfs(wav_path, original_filename=None):
    """
    🎯 전처리된 wav 파일을 GridFS에 저장하고 file_id 반환
    :param wav_path: 저장할 .wav 파일 경로 (Path or str)
    :param original_filename: 원래 파일 이름 (.mp4/.mp3 기준) - 선택적
    """
    # MongoDB 연결
    client = MongoClient("mongodb://localhost:27017/")
    db = client["bytebite_ai"]
    fs = gridfs.GridFS(db)

    with open(wav_path, "rb") as f:
        file_id = fs.put(
            f,
            filename=os.path.basename(wav_path),
            content_type="audio/wav",
            uploaded_at=datetime.utcnow(),
            original_filename=original_filename  # 원본 파일명을 별도 저장
        )
    print(f"📦 GridFS 저장 완료: {os.path.basename(wav_path)} → file_id: {file_id}")
    return file_id
