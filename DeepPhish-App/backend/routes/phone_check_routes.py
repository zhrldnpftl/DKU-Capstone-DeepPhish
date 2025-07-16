# backend/routes/phone_check_routes.py

from flask import Blueprint, request, jsonify
from datetime import datetime
from pymongo import MongoClient
import sys
import os

# 📌 모델 경로 추가 (phishing_detection 내의 크롤링 코드 사용)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'model', 'phishing_detection')))
from Fifth_phone_checker import check_phone_number

# ✅ Blueprint 생성
phone_check_bp = Blueprint('phone_check', __name__)

# ✅ MongoDB 연결
client = MongoClient("mongodb://localhost:27017")
db = client["DeepPhish"]  
collection = db["phonecheck_logs"]

@phone_check_bp.route('/check-phone', methods=['POST'])
def check_phone():
    data = request.get_json()
    phone_number = data.get("phone_number")

    if not phone_number:
        print("🚫 [오류] 전화번호가 입력되지 않았습니다.")
        return jsonify({"error": "전화번호가 입력되지 않았습니다."}), 400

    print(f"📞 [요청 수신] 입력된 전화번호: {phone_number}")

    result = check_phone_number(phone_number)
    if result is None:
        print("❌ [조회 실패] check_phone_number에서 None 반환")
        return jsonify({"error": "조회 실패"}), 500

    # ✅ MongoDB에 로그 저장
    log_doc = {
        "phone_number": phone_number,
        "checked_at": datetime.utcnow().isoformat() + "Z",
        "report_count": result["total"],
        "voice_reported": result["voice"] > 0,
        "sms_reported": result["sms"] > 0
    }
    collection.insert_one(log_doc)

    print("✅ [MongoDB 저장 완료]")
    print("📦 저장된 로그 문서:")
    print(log_doc)

    response_data = {
        "reportCount": result["total"],
        "voiceCount": result["voice"],
        "smsCount": result["sms"],
        "risk": "⚠️ 위험 등급: 높음" if result["total"] >= 3 else "✅ 위험 등급: 낮음",
        "pattern": "사칭형 피싱" if result["voice"] > 0 else "기타"
    }

    print("📤 [클라이언트 응답 데이터]:")
    print(response_data)

    return jsonify(response_data)
