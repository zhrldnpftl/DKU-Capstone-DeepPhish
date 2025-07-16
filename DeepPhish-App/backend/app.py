# backend/app.py
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, jsonify
from flask_cors import CORS

# ✅ Blueprint 라우트들 임포트
from routes.phone_check_routes import phone_check_bp
from routes.detect_routes import detect_bp
from routes.report_routes import report_bp

# ✅ Flask 앱 초기화
app = Flask(__name__)

# 🔧 CORS 설정 수정 - 모든 경로에 대해 허용
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:8081", "http://localhost:3000", "http://192.168.45.233:8081", "http://192.168.56.1:8081"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "Cache-Control", "Accept"],
        "supports_credentials": True
    }
})

# 또는 개발 환경에서는 더 간단하게
# CORS(app, origins="*")  # 모든 도메인 허용 (개발용)

# ✅ Health Check 엔드포인트 추가
@app.route('/health', methods=['GET'])
def health_check():
    """서버 상태 확인용 엔드포인트"""
    return jsonify({
        "status": "ok",
        "message": "서버가 정상적으로 실행 중입니다",
        "version": "1.0.0"
    }), 200

# ✅ 기본 라우트 (테스트용)
@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "message": "보이스피싱 탐지 API 서버",
        "endpoints": {
            "health": "/health",
            "upload": "/upload-audio",
            "detect": "/detect-stream/<file_id>",
            "phone_check": "/phone-check",
            "report": "/report"
        }
    })

# ✅ 기능별 라우터 등록
app.register_blueprint(phone_check_bp)   # 전화번호 조회 API
app.register_blueprint(detect_bp)        # 탐지 모델 API
app.register_blueprint(report_bp)        # 신고 처리 API

# ✅ 에러 핸들러 추가
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "엔드포인트를 찾을 수 없습니다"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "서버 내부 오류가 발생했습니다"}), 500

# ✅ 서버 실행
if __name__ == '__main__':
    print("🚀 서버가 시작됩니다...")
    print("📍 접속 주소:")
    print("   - 로컬: http://localhost:5000")
    print("   - 네트워크: http://192.168.45.233:5000")
    print("   - Health Check: http://192.168.56.1:5000/health")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)