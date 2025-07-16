from flask import Blueprint, request, Response, jsonify, stream_with_context
import os
import tempfile
import json
import time
import threading
from werkzeug.utils import secure_filename
from bson import ObjectId
from datetime import datetime
from pymongo import MongoClient
import gridfs
import logging

# 모델 import
from model.deepvoice_detection.RunPipeline import run_inference
from model.phishing_detection.RunPipeline import run_full_pipeline
from model.phishing_detection.Fifth_phone_checker import check_phone_number

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔧 MongoDB 연결 설정
client = MongoClient("mongodb://localhost:27017/")
db = client["DeepPhish"]
fs = gridfs.GridFS(db)
voice_meta = db.voice_meta
detect_results = db.detect_results  # 탐지 결과 컬렉션
detect_progress = db.detect_progress  # 진행 상황 로그 컬렉션

detect_bp = Blueprint("detect", __name__)

# 🔧 진행 상황 로그 관리 함수들
def init_progress_log(file_id):
    """진행 상황 로그 초기화"""
    detect_progress.delete_many({"file_id": file_id})
    detect_progress.insert_one({
        "file_id": file_id,
        "logs": [],
        "status": "started",
        "created_at": datetime.utcnow()
    })

def add_progress_log(file_id, message):
    """진행 상황 로그 추가"""
    detect_progress.update_one(
        {"file_id": file_id},
        {
            "$push": {
                "logs": {
                    "message": message,
                    "timestamp": datetime.utcnow()
                }
            }
        }
    )
    logger.info(f"Progress [{file_id}]: {message}")

def get_progress_logs(file_id):
    """진행 상황 로그 조회"""
    progress = detect_progress.find_one({"file_id": file_id})
    if progress:
        return progress.get("logs", [])
    return []

def set_progress_status(file_id, status):
    """진행 상황 상태 업데이트"""
    detect_progress.update_one(
        {"file_id": file_id},
        {"$set": {"status": status, "updated_at": datetime.utcnow()}}
    )

# ✅ [1] 오디오 파일 업로드 라우트 
@detect_bp.route('/upload-audio', methods=['POST'])
def upload_audio():
    try:
        logger.info("📤 파일 업로드 요청 수신")
        
        # 요청 데이터 확인
        audio_file = request.files.get('audio')
        phone_number = request.form.get('phone_number')
        
        logger.info(f"📞 전화번호: {phone_number}")
        logger.info(f"📁 파일 정보: {audio_file.filename if audio_file else 'None'}")
        
        if not audio_file:
            logger.error("❌ audio 파일이 없습니다")
            return jsonify({"error": "audio 파일이 필요합니다"}), 400
            
        if not phone_number:
            logger.error("❌ phone_number가 없습니다")
            return jsonify({"error": "phone_number가 필요합니다"}), 400

        # 파일 크기 확인
        audio_file.seek(0, os.SEEK_END)
        file_size = audio_file.tell()
        audio_file.seek(0)
        
        logger.info(f"📏 파일 크기: {file_size} bytes")
        
        if file_size == 0:
            logger.error("❌ 빈 파일입니다")
            return jsonify({"error": "빈 파일입니다"}), 400

        # 📁 안전한 파일명 생성
        original_filename = secure_filename(audio_file.filename) if audio_file.filename else "audio.mp3"
        
        # 임시 파일로 저장
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            audio_file.save(tmp.name)
            tmp_path = tmp.name
            logger.info(f"💾 임시 파일 저장: {tmp_path}")

        # GridFS에 저장
        with open(tmp_path, "rb") as f:
            file_id = fs.put(
                f, 
                filename=original_filename,
                content_type="audio/mpeg",
                metadata={
                    "original_size": file_size,
                    "upload_time": datetime.utcnow()
                }
            )

        # 메타데이터 저장
        voice_meta.insert_one({
            "file_id": file_id,
            "original_filename": original_filename,
            "phone_number": phone_number,
            "file_size": file_size,
            "uploaded_at": datetime.utcnow(),
            "processed": False
        })

        # 임시 파일 삭제
        os.remove(tmp_path)
        
        # 백그라운드에서 탐지 시작
        threading.Thread(target=run_detection_background, args=(str(file_id), phone_number)).start()
        
        return jsonify({
            "file_id": str(file_id),
            "filename": original_filename,
            "size": file_size,
            "message": "업로드 성공"
        })

    except Exception as e:
        logger.error(f"❌ 업로드 오류: {str(e)}")
        return jsonify({"error": f"업로드 실패: {str(e)}"}), 500

# 🔍 백그라운드 탐지 실행 함수
def run_detection_background(file_id, phone_number):
    """백그라운드에서 탐지 실행"""
    try:
        object_id = ObjectId(file_id)
        
        # 진행 상황 로그 초기화
        init_progress_log(file_id)
        add_progress_log(file_id, "🚀 [탐지 시작]")
        
        # 메타데이터 조회
        meta = voice_meta.find_one({"file_id": object_id})
        if not meta:
            add_progress_log(file_id, "❌ 파일 메타데이터를 찾을 수 없습니다")
            set_progress_status(file_id, "error")
            return

        add_progress_log(file_id, f"📁 파일명: {meta['original_filename']}")

        # GridFS에서 파일 읽기
        try:
            grid_out = fs.get(object_id)
        except Exception as e:
            add_progress_log(file_id, f"❌ 파일을 찾을 수 없습니다: {str(e)}")
            set_progress_status(file_id, "error")
            return

        # 임시 파일 생성
        temp_path = os.path.join(tempfile.gettempdir(), f"{file_id}.mp3")
        with open(temp_path, "wb") as f:
            f.write(grid_out.read())

        current_phone = phone_number or meta["phone_number"]

        # 1. 딥보이스 탐지
        add_progress_log(file_id, "🎤 [딥보이스 탐지 시작]")
        try:
            deepvoice_json = run_inference(temp_path)
            add_progress_log(file_id, "✅ 딥보이스 탐지 완료")
        except Exception as e:
            add_progress_log(file_id, f"❌ 딥보이스 탐지 오류: {str(e)}")
            set_progress_status(file_id, "error")
            return

        # 2. 피싱 문맥 분석
        add_progress_log(file_id, "🔍 [피싱 문맥 분석 시작]")
        try:
            phishing_json = run_full_pipeline(temp_path)
            add_progress_log(file_id, "✅ 피싱 문맥 분석 완료")
        except Exception as e:
            add_progress_log(file_id, f"❌ 피싱 문맥 분석 오류: {str(e)}")
            set_progress_status(file_id, "error")
            return

        # 3. 전화번호 조회
        add_progress_log(file_id, "📞 전화번호 조회 중...")
        try:
            phone_check_result = check_phone_number(current_phone)
            add_progress_log(file_id, "✅ 전화번호 조회 완료")
        except Exception as e:
            add_progress_log(file_id, f"❌ 전화번호 조회 오류: {str(e)}")
            phone_check_result = {"total": 0, "voice": 0, "sms": 0}

        # 4. 최종 분석
        add_progress_log(file_id, "🔍 최종 분석 중...")
        try:
            deep = json.loads(deepvoice_json)
            phish = json.loads(phishing_json)

            THRESHOLD = 0.8
            confidence = round((deep["probability"] + phish["probability"]) / 2, 4)
            is_phishing = (deep["label"] == "fake" and deep["probability"] >= THRESHOLD) and \
                         (phish["label"] == "phishing" and phish["probability"] >= THRESHOLD)

            reason = ""
            if is_phishing:
                reason = "딥보이스와 피싱 문맥 모두 기준 초과"
            elif deep["probability"] >= THRESHOLD:
                reason = "딥보이스만 기준 초과"
            elif phish["probability"] >= THRESHOLD:
                reason = "피싱 문맥만 기준 초과"
            else:
                reason = "보이스피싱으로 판단되지 않음"

            final_result = {
                "done": True,
                "deepvoice_result": {
                    "is_fake": deep["label"] == "fake",
                    "probability": deep["probability"],
                    "label": deep["label"],
                    "confidence": deep["probability"]
                },
                "phishing_result": {
                    "is_phishing": phish["label"] == "phishing",
                    "probability": phish["probability"],
                    "label": phish["label"],
                    "confidence": phish["probability"]
                },
                "phone_check": {
                    "input_number": current_phone,
                    "report": phone_check_result
                },
                "final_result": {
                    "is_phishing": is_phishing,
                    "reason": reason,
                    "confidence": confidence
                }
            }

            # 결과 저장
            detect_results.insert_one({
                **final_result,
                "filename": meta['original_filename'],
                "file_id": object_id,
                "reported": False,
                "suggest_report": final_result["deepvoice_result"]["is_fake"] or final_result["phishing_result"]["is_phishing"],
                "analyzed_at": datetime.utcnow().isoformat() + "Z"
            })

            voice_meta.update_one({"file_id": object_id}, {"$set": {"status": "done", "processed": True}})
            
            add_progress_log(file_id, "✅ 최종 분석 완료")
            set_progress_status(file_id, "completed")

        except Exception as e:
            add_progress_log(file_id, f"❌ 최종 분석 오류: {str(e)}")
            set_progress_status(file_id, "error")
            return

    except Exception as e:
        add_progress_log(file_id, f"❌ 탐지 프로세스 오류: {str(e)}")
        set_progress_status(file_id, "error")
    finally:
        # 임시 파일 삭제
        if 'temp_path' in locals() and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
                add_progress_log(file_id, "🗑️ 임시 파일 삭제 완료")
            except:
                pass

# ✅ [2] 탐지 진행 상황 및 결과 조회 라우트 (수정된 부분)
@detect_bp.route('/detect-stream/<file_id>', methods=['GET'])
def detect_stream(file_id):
    """탐지 진행 상황 및 결과 조회 (Polling용)"""
    try:
        object_id = ObjectId(file_id)
        
        # 진행 상황 로그 조회
        progress = detect_progress.find_one({"file_id": file_id})
        if not progress:
            return jsonify({"error": "진행 상황을 찾을 수 없습니다"}), 404
        
        # 완료된 경우 결과 반환
        if progress.get("status") == "completed":
            result = detect_results.find_one({"file_id": object_id})
            if result:
                # ObjectId를 문자열로 변환
                result['_id'] = str(result['_id'])
                result['file_id'] = str(result['file_id'])
                return jsonify(result)
        
        # 에러 상태인 경우
        if progress.get("status") == "error":
            return jsonify({
                "error": "탐지 중 오류가 발생했습니다",
                "logs": progress.get("logs", [])
            }), 500
        
        # 진행 중인 경우 로그 반환
        logs = progress.get("logs", [])
        latest_log = logs[-1]["message"] if logs else "처리 대기 중..."
        
        return jsonify({
            "status": progress.get("status", "processing"),
            "latest_log": latest_log,
            "all_logs": [log["message"] for log in logs],
            "done": False
        })
        
    except Exception as e:
        return jsonify({"error": f"상태 조회 실패: {str(e)}"}), 500

# 🔍 [3] 파일 상태 확인 라우트 (기존과 동일)
@detect_bp.route('/file-status/<file_id>', methods=['GET'])
def file_status(file_id):
    try:
        object_id = ObjectId(file_id)
        meta = voice_meta.find_one({"file_id": object_id})
        
        if not meta:
            return jsonify({"error": "파일을 찾을 수 없습니다"}), 404
            
        # GridFS에서 파일 존재 확인
        try:
            grid_out = fs.get(object_id)
            file_exists = True
            file_size = len(grid_out.read())
        except:
            file_exists = False
            file_size = 0
            
        return jsonify({
            "file_id": file_id,
            "filename": meta.get("original_filename"),
            "phone_number": meta.get("phone_number"),
            "uploaded_at": meta.get("uploaded_at"),
            "processed": meta.get("processed", False),
            "file_exists_in_gridfs": file_exists,
            "file_size": file_size,
            "metadata_size": meta.get("file_size")
        })
        
    except Exception as e:
        return jsonify({"error": f"상태 확인 실패: {str(e)}"}), 500

# 🔍 [4] 탐지 결과 조회 라우트 (기존과 동일)
@detect_bp.route('/detect-results', methods=['GET'])
def get_detect_results():
    """탐지 결과 목록 조회"""
    try:
        # 쿼리 파라미터
        phone_number = request.args.get('phone_number')
        limit = int(request.args.get('limit', 10))
        skip = int(request.args.get('skip', 0))
        
        # 필터 조건
        filter_query = {}
        if phone_number:
            filter_query['phone_number'] = phone_number
        
        # 결과 조회 (최신순)
        results = list(detect_results.find(filter_query)
                      .sort('analyzed_at', -1)
                      .skip(skip)
                      .limit(limit))
        
        # ObjectId를 문자열로 변환
        for result in results:
            result['_id'] = str(result['_id'])
            if 'file_id' in result:
                result['file_id'] = str(result['file_id'])
        
        total_count = detect_results.count_documents(filter_query)
        
        return jsonify({
            "results": results,
            "total_count": total_count,
            "page_info": {
                "limit": limit,
                "skip": skip,
                "has_more": skip + limit < total_count
            }
        })
        
    except Exception as e:
        return jsonify({"error": f"결과 조회 실패: {str(e)}"}), 500

# 🔍 [5] 특정 탐지 결과 조회 라우트 (기존과 동일)
@detect_bp.route('/detect-results/<result_id>', methods=['GET'])
def get_detect_result(result_id):
    """특정 탐지 결과 상세 조회"""
    try:
        object_id = ObjectId(result_id)
        result = detect_results.find_one({"_id": object_id})
        
        if not result:
            return jsonify({"error": "결과를 찾을 수 없습니다"}), 404
        
        # ObjectId를 문자열로 변환
        result['_id'] = str(result['_id'])
        if 'file_id' in result:
            result['file_id'] = str(result['file_id'])
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": f"결과 조회 실패: {str(e)}"}), 500

# 🔍 [6] 신고 상태 업데이트 라우트 (기존과 동일)
@detect_bp.route('/detect-results/<result_id>/report', methods=['PUT'])
def update_report_status(result_id):
    """신고 상태 업데이트"""
    try:
        object_id = ObjectId(result_id)
        reported = request.json.get('reported', True)
        
        result = detect_results.update_one(
            {"_id": object_id},
            {"$set": {"reported": reported, "reported_at": datetime.utcnow()}}
        )
        
        if result.matched_count == 0:
            return jsonify({"error": "결과를 찾을 수 없습니다"}), 404
        
        return jsonify({
            "message": "신고 상태가 업데이트되었습니다",
            "reported": reported
        })
        
    except Exception as e:
        return jsonify({"error": f"상태 업데이트 실패: {str(e)}"}), 500