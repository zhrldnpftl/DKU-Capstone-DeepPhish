# phone_checker.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, NoSuchElementException
import time

def check_phone_number(phone_number):
    """📞 해당 전화번호의 보이스피싱 신고 건수 조회 함수"""
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--headless=new")
    service = Service()

    driver = None
    try:
        driver = webdriver.Chrome(service=service, options=options)
        wait = WebDriverWait(driver, 10)

        driver.get("https://www.counterscam112.go.kr/phishing/searchPhone.do")

        # 입력창에 번호 입력
        wait.until(EC.presence_of_element_located((By.ID, "tel_num")))
        input_box = driver.find_element(By.ID, "tel_num")
        input_box.clear()
        input_box.send_keys(phone_number)

        # 검색 버튼 클릭
        search_btn = driver.find_element(By.CLASS_NAME, "ico_sch_btn")
        search_btn.click()

        # 결과 대기
        wait.until(EC.presence_of_element_located((By.ID, "tel_num_result_data")))
        time.sleep(1)

        # 결과 추출
        total_elem = driver.find_element(By.ID, "search-totcnt")
        voice_elem = driver.find_element(By.ID, "search-voice-cnt")
        sms_elem = driver.find_element(By.ID, "search-sms-cnt")

        total_count = int(total_elem.text.strip()) if total_elem.text.strip().isdigit() else 0
        voice_count = int(voice_elem.text.strip()) if voice_elem.text.strip().isdigit() else 0
        sms_count = int(sms_elem.text.strip()) if sms_elem.text.strip().isdigit() else 0

        return {
            "total": total_count,
            "voice": voice_count,
            "sms": sms_count
        }

    except WebDriverException as e:
        print("❌ WebDriver 예외 발생:", str(e))
        return None

    except NoSuchElementException as e:
        print("❌ 요소를 찾을 수 없습니다:", str(e))
        return None

    except Exception as e:
        print("❌ 예기치 못한 오류 발생:", str(e))
        return None

    finally:
        if driver:
            driver.quit()
