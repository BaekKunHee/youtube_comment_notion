import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from ..schemas.models import Review
from ..config import settings
from typing import List

class CoupangService:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")  # GPU 가속 비활성화 (서버 환경)
        options.add_argument("--remote-debugging-port=9222")  # 디버깅 포트 설정
        options.add_argument("--disable-blink-features=AutomationControlled")
        
        # User Agent 설정
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # Anti-bot 설정
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        
        # 추가 설정
        options.add_argument("--disable-gpu")
        options.add_argument("--lang=ko_KR")

        chrome_driver_path = "/usr/local/bin/chromedriver"
        service = Service(chrome_driver_path)
        
        self.driver = webdriver.Chrome(options=options, service=service)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def fetch_reviews(self, product_url: str) -> List[Review]:
        """
        쿠팡 상품의 리뷰를 수집하는 메서드

        Args:
            product_url (str): 쿠팡 상품 URL

        Returns:
            List[Review]: 리뷰 목록
        """
        reviews = []
        try:
            # 페이지 로드
            self.driver.get(product_url)
            time.sleep(5)
            
            # 리뷰 섹션 찾기
            review_elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "sdp-review__article__list"))
            )[:10]
            
            print(f"Found {len(review_elements)} reviews")
            
            for review in review_elements:
                try:
                    # 별점
                    rating_div = review.find_element(By.CLASS_NAME, "js_reviewArticleRatingValue")
                    rating = int(rating_div.get_attribute("data-rating"))
                    
                    # 내용
                    content_element = review.find_element(By.CLASS_NAME, "sdp-review__article__list__review__content")
                    content = content_element.text.strip()
                    
                    # 날짜
                    date_element = review.find_element(By.CLASS_NAME, "sdp-review__article__list__info__product-info__reg-date")
                    date = date_element.text.strip()
                    
                    # 이미지
                    image_elements = review.find_elements(By.CLASS_NAME, "sdp-review__article__list__attachment__img")
                    image_urls = [img.get_attribute("src") for img in image_elements]
                    
                    if content:
                        reviews.append(Review(
                            rating=rating,
                            content=content,
                            date=date,
                            images=image_urls
                        ))
                        
                except Exception as e:
                    print(f"Error parsing review: {str(e)}")
                    continue

        except Exception as e:
            print(f"Error during review fetch: {str(e)}")
            
        finally:
            if hasattr(self, 'driver') and self.driver:
                self.driver.quit()
                
        return reviews

    def __del__(self):
        try:
            if hasattr(self, 'driver') and self.driver:
                self.driver.quit()
        except:
            pass