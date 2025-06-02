# backend/app.py

from flask import Flask
from flask_cors import CORS

# ✅ Blueprint 라우트들 임포트
from routes.phone_check_routes import phone_check_bp
from routes.detect_routes import detect_bp
from routes.report_routes import report_bp

# ✅ Flask 앱 초기화
app = Flask(__name__)
CORS(app)

# ✅ 기능별 라우터 등록
app.register_blueprint(phone_check_bp)   # 전화번호 조회 API
app.register_blueprint(detect_bp)        # 탐지 모델 API
app.register_blueprint(report_bp)        # 신고 처리 API

# ✅ 서버 실행
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
