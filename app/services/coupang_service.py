from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..schemas.models import Review
from typing import List
import time
import random

class CoupangService:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Headless 모드로 실행
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--window-size=1920,1080")

        
        # User Agent 설정 - 따옴표 제거하여 수정
        options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # 추가적인 anti-bot 우회 설정
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        
        # 추가 설정으로 봇 감지 회피
        options.add_argument("--disable-gpu")
        options.add_argument("--lang=ko_KR")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')

        
        
        self.driver = None  # 초기화는 fetch_reviews에서 수행
        self.options = options  # options 저장

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
            # 드라이버 초기화
            self.driver = webdriver.Chrome(options=self.options)
            
            # 웹드라이버 속성 변경으로 봇 감지 회피
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            # 쿠키 및 캐시 초기화
            self.driver.delete_all_cookies()
            
            # 페이지 로드
            self.driver.get(product_url)
            time.sleep(5)
            
            # 랜덤한 마우스 움직임 시뮬레이션
            self.simulate_human_behavior()
            
            # 리뷰 탭으로 이동
            try:
                review_tab = self.driver.find_element(By.ID, "pdpReviewSection")
                self.driver.execute_script("arguments[0].scrollIntoView(true);", review_tab)
                time.sleep(2)
            except Exception as e:
                print(f"Error finding review tab: {str(e)}")

            # 리뷰 섹션 찾기 - 여러 선택자 시도
            try:
                review_section = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "sdp-review__article__list"))
                )
                print("Found review section")
            except:
                print("Trying alternative selector...")
                review_section = self.driver.find_element(By.CSS_SELECTOR, "section.js_reviewArticleListContainer")
                print("Found review section with alternative selector")
            
            # 모든 리뷰 article 요소 찾기
            review_elements = self.driver.find_elements(By.TAG_NAME, "article")[:10]
            print(f"Found {len(review_elements)} reviews")
            
            for review in review_elements:
                try:
                    # 별점 추출
                    rating_div = review.find_element(By.CLASS_NAME, "sdp-review__article__list__info__product-info__star-orange")
                    rating_style = rating_div.get_attribute("style")
                    rating = int(float(rating_style.split("width: ")[1].split("%")[0]) / 20)

                    # 리뷰 내용
                    content_element = review.find_element(By.CLASS_NAME, "sdp-review__article__list__review__content")
                    content = content_element.text.strip()

                    # 작성 날짜
                    date_element = review.find_element(By.CLASS_NAME, "sdp-review__article__list__info__product-info__reg-date")
                    date = date_element.text.strip()

                    # 리뷰 이미지 가져오기
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
            try:
                if self.driver:
                    self.driver.quit()
                    self.driver = None
            except Exception as e:
                print(f"Error closing driver: {str(e)}")
        
        return reviews

    def simulate_human_behavior(self):
        """사람처럼 보이는 행동 시뮬레이션"""
        try:
            # 랜덤한 위치로 스크롤
            for _ in range(3):
                random_scroll = f"window.scrollTo(0, {random.randint(100, 700)});"
                self.driver.execute_script(random_scroll)
                time.sleep(random.uniform(0.5, 1.5))
            
            # 페이지 중간까지 스크롤
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
            time.sleep(2)
            
            # 리뷰 섹션까지 스크롤
            try:
                review_section = self.driver.find_element(By.ID, "pdpReviewSection")
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", review_section)
                time.sleep(2)
            except:
                print("Review section not found during scrolling")
            
        except Exception as e:
            print(f"Error in human behavior simulation: {str(e)}")

    def __del__(self):
        """소멸자에서 드라이버 정리"""
        try:
            if self.driver:
                self.driver.quit()
        except:
            pass 