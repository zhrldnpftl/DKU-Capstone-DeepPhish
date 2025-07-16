from flask import Blueprint, request, jsonify
from datetime import datetime
from pymongo import MongoClient

# 🔧 Blueprint 객체 생성
report_bp = Blueprint('report', __name__)

# ✅ MongoDB 연결
client = MongoClient("mongodb://localhost:27017")
db = client["voicephishing_db"]
collection = db["reports"]

@report_bp.route('/report', methods=['POST'])
def report_entry():
    data = request.get_json()
    data["reported_at"] = datetime.utcnow().isoformat() + "Z"
    collection.insert_one(data)
    return jsonify({"message": "신고가 접수되었습니다."}), 201
