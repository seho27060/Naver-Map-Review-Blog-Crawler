import re
import time
from pprint import pprint

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from bs4 import BeautifulSoup

import blogCrawler


# opt0 기본
# searchName = "상호명"
# *nameCnt = "호점"/ 옵션으로
# adress = "도로명주소"
# opt1 그냥 밥집
# searchName = "국수찾아닭만리"
# adress = " 서울특별시 종로구 낙원동"
# # opt2 프랜차이즈 밥집
# searchName = "바른치킨"
# adress = "서울특별시 강남구 선릉로86길 17"
# # opt3 감성밥집
# searchName = "비지트"
# adress = "서울 서초구 동광로18길 82"
#
# searchKeyword = searchName + " " + adress  # 검색어


def crawler(storeIdxGet,name, adress):
    name = name.rstrip()
    adress = adress.rstrip()
    searchWord = name + " " + adress

    # --크롬창을 숨기고 실행-- driver에 options를 추가해주면된다
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    url = 'https://map.naver.com/v5/search'
    driver = webdriver.Chrome('./chromedriver')  # 드라이버 경로
    # driver = webdriver.Chrome('./chromedriver',chrome_options=options) # 크롬창 숨기기
    driver.get(url)

    # xpath 찾을때 까지 num초대기
    def time_wait(num, codeType, code):
        wait = 0
        # codeType = "xpath","class","css"
        if codeType == "xpath":
            try:
                wait = WebDriverWait(driver, num).until(
                    EC.presence_of_element_located((By.XPATH, code)))
            except:
                pass
        elif codeType == "class":
            try:
                wait = WebDriverWait(driver, num).until(
                    EC.presence_of_element_located((By.CLASS_NAME, code)))
            except:
                pass
        elif codeType == "css":
            try:
                wait = WebDriverWait(driver, num).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, code)))
            except:
                pass
        if wait:
            print(code, "찾음")
            return True
        else:
            print(code, '태그를 찾지 못하였습니다.')
            return False

    # frame 변경 메소드
    def switch_frame(frame):
        driver.switch_to.default_content()  # frame 초기화
        driver.switch_to.frame(frame)  # frame 변경

    # 페이지 다운
    def page_down(num):
        body = driver.find_element_by_css_selector('body')
        body.click()
        for i in range(num):
            body.send_keys(Keys.PAGE_DOWN)

    # css를 찾을때 까지 10초 대기
    time_wait(10, "xpath",
              '/html/body/app/layout/div[3]/div[2]/shrinkable-layout/div/app-base/search-input-box/div/div/div/input')

    # 검색창 찾기
    search = driver.find_element_by_css_selector('div.input_box > input.input_search')
    search.send_keys(searchWord)  # 검색어 입력
    search.send_keys(Keys.ENTER)  # 엔터버튼 누르기

    res = driver.page_source  # 페이지 소스 가져오기
    soup = BeautifulSoup(res, 'html.parser')  # html 파싱하여  가져온다

    sleep(1)
    storeIdx = storeIdxGet
    storeName = name
    storeRating = ""
    storeTell = ""
    reviewList = []
    reviewCnt = ""
    blogUrlList = []
    blogReviewList = []
    blogCnt = ""
    keywordReviewDict = {}
    foodCategory = ""

    storeTellRegex = re.compile("\d{1,5}-\d{1,5}-\d{1,5}")

    result = {
        "storeIdx" : storeIdx,
        "searchKeyword": name + " " + adress,
        "name": storeName,  # 처음 검색할때 상호명으로 저장
        "foodCategory": foodCategory,
        "rating": storeRating,
        "tell": storeTell,
        "reviews": reviewList,
        "reviewCnt": reviewCnt,
        "blogUrls": blogUrlList,
        "blogReviews": blogReviewList,
        "blogCnt": blogCnt,
        "keywordReviewDict": keywordReviewDict,
    }
    # frame 변경
    # iframes = driver.find_elements_by_css_selector('nm-external-frame-bridge > nm-iframe > iframe') # 창에 있는 모든 iframe 출력
    # for iframe in iframes:
    #     print(iframe.get_attribute('id'))
    driver.switch_to.default_content()
    iframes = driver.find_elements_by_css_selector('iframe')  # 창에 있는 모든 iframe 출력
    print("프레임 개수:", len(iframes))
    for iframe in iframes:
        print(iframe.get_attribute('id'))

    # 시작시간
    start = time.time()
    print("크롤링 시도")
    # sleep(3)
    try:
        time_wait(10, 'xpath',
                  '/html/body/app/layout/div[3]/div[2]/shrinkable-layout/div/app-base/search-layout/div[2]/entry-layout/entry-place-bridge/div/nm-external-frame-bridge/nm-iframe/iframe')
        switch_frame("entryIframe")
        print("entryIframe find")
    except:
        print("entryIframe 못찾음")
        driver.quit()  # 작업이 끝나면 창을닫는다.
        return result
    # page_down(40)

    sleep(2)


    try:
        # 검색된 상호명/ 음식 카테고리
        try:
            if time_wait(3, "class","YouOG"):
                storeTitle = driver.find_element_by_class_name("YouOG")
                try:
                    storeName = storeTitle.find_element_by_class_name("Fc1rA").text
                except:
                    storeName = ""
                try:
                    foodCategory = storeTitle.find_element_by_class_name("DJJvD").text
                except:
                    foodCategory = ""
        except:
            print("검색 상호명/ 음식 카테고리 에러")

        print("데이터 확인. 크롤링 시작 :", storeName)
        print("별점")
        if time_wait(3, 'xpath', '/html/body/div[3]/div/div/div/div[2]/div[1]/div[2]'):
            ratingReviewBlogCnt = driver.find_elements_by_xpath(
                '/html/body/div[3]/div/div/div/div[2]/div[1]/div[2]/span')
            for idx in range(len(ratingReviewBlogCnt)):
                if idx == 0:
                    try:
                        storeRating = driver.find_element_by_xpath("/html/body/div[3]/div/div/div/div[2]/div[1]/div[2]/span[1]/em").text
                    except:
                        pass
                if idx == 1:
                    try:
                        reviewCnt = driver.find_element_by_xpath("/html/body/div[3]/div/div/div/div[2]/div[1]/div[2]/span[2]/a/em").text
                    except:
                        pass
                if idx == 2:
                    try:
                        blogCnt = driver.find_element_by_xpath("/html/body/div[3]/div/div/div/div[2]/div[1]/div[2]/span[3]/a/em").text
                    except:
                        pass
        else:
            print("평점 없음")
        print("점수 :", storeRating)

        # -----전화번호 가져오기-----
        print("전화번호")
        if time_wait(3, 'xpath', '/html/body/div[3]/div/div/div/div[6]/div/div[2]/div/ul/li[3]/div/span[1]'):
            storeTell = driver.find_element_by_xpath(
                '/html/body/div[3]/div/div/div/div[6]/div/div[2]/div/ul/li[3]/div/span[1]').text
            storeTellValidation = storeTellRegex.search(storeTell.replace(" ",""))
            if not storeTellValidation:
                storeTell = ""
            # store_tel = driver.find_element_by_css_selector("#app-root > div > div > div > div:nth-child(6) > div > div.place_section.no_margin.vKA6F > div > ul > li.SF_Mq.SjF5j > div > span.dry01").text
        else:
            print("전화번호 없음")
        print("전화번호", storeTell)

        # 방문자 리뷰
        try:
            tabBtns = driver.find_elements_by_xpath("/html/body/div[3]/div/div/div/div[5]/div/div/div/div/a")
            # tabBtns = driver.find_elements_by_class_name("tpj9w _tab-menu")
            sleep(1)
            for tab in tabBtns:
                if tab.text == "리뷰":
                    tab.click()
                    print("리뷰 탭 클릭")
                    break
            sleep(1)


            for clickIdx in range(5):
                # page_down(40)
                sleep(0.5)
                if time_wait(3, 'xpath', "/html/body/div[3]/div/div/div/div[7]/div[2]/div[3]/div[2]/a"):
                    print("리뷰 리스트 더보기 클릭")
                    driver.find_element_by_xpath("/html/body/div[3]/div/div/div/div[7]/div[2]/div[3]/div[2]/a").click()
                else:
                    print("더보기없음 리뷰 수집시작")
                    break
            sleep(2)
            # 리뷰 크ㅜㄹ래스로?
            # 굴세상 /html/body/div[3]/div/div/div/div[7]/div[2]/div[2]/div[1]/ul/li
            # 은진이네 /html/body/div[3]/div/div/div/div[7]/div/div[3]/div[1]/ul/li YeINN
            # 흥부보쌈 /html/body/div[3]/div/div/div/div[7]/div[2]/div[2]/div[1]/ul/li[32]
            # reviews = driver.find_elements_by_xpath("/html/body/div[3]/div/div/div/div[7]/div[2]/div[3]/div[1]/ul/li")
            if time_wait(5,"class","YeINN"):
                reviews = driver.find_elements_by_class_name("YeINN")
            else:
                reviews = []

            print("리뷰 개수 :", len(reviews))
            for idx in range(len(reviews)):
                # 리뷰 찾고, 리뷰 더보기 클릭 후 리뷰 수집
                review = 0
                try:
                    reviews[idx].find_element_by_class_name("rvCSr").click()
                    sleep(0.2)
                except:
                    # print("상세 더보기 없음")
                    pass
                sleep(0.2)
                try:
                    review = reviews[idx].find_element_by_class_name("ZZ4OK").text.replace("\n", " ")
                    # review = reviews[idx].text.replace("\n", " ")
                except:
                    print("리뷰 못찾음")
                if review:
                    reviewList.append(review)
                    # print(review)
            print("찾은 리뷰 개수 :", len(reviewList))
        except:
            print("방문자 리뷰 에러")

        try:
            # 키워드 리뷰
            for clickIdx in range(4):
                if time_wait(3,"class","Tvx37"):
                        keywordBtn = driver.find_element_by_class_name('Tvx37')  # 키워드가 담긴 리스트 클릭
                        print("키워드 더보기 클릭")
                        keywordBtn.send_keys(Keys.ENTER)
                else:
                    print('키워드리뷰 더보기 없음' )
                    break

            if time_wait(3,"class","nbD78"):
                keywordList = driver.find_elements_by_class_name('nbD78')  # 리뷰 리스트
                sleep(1)
                for keywordIdx in range(len(keywordList)):
                    keywordTitle = keywordList[keywordIdx].find_element_by_class_name('nWiXa').text  # 키워드리뷰
                    keywordCount = keywordList[keywordIdx].find_element_by_class_name('TwM9q').text  # 리뷰를 선택한 수

                    # db에 넣을 때 편의를 위해 요청하였음
                    title_re = re.sub('"', '', keywordTitle) \
                        .replace('양이 많아요', '1').replace('음식이 맛있어요', '2').replace('재료가 신선해요', '3') \
                        .replace('가성비가 좋아요', '4').replace('특별한 메뉴가 있어요', '5').replace('화장실이 깨끗해요', '6') \
                        .replace('주차하기 편해요', '7').replace('친절해요', '8').replace('특별한 날 가기 좋아요', '9').replace(
                        '매장이 청결해요',
                        '10') \
                        .replace('인테리어가 멋져요', '11').replace('단체모임 하기 좋아요', '12').replace('뷰가 좋아요', '13').replace(
                        '매장이 넓어요',
                        '14') \
                        .replace('혼밥하기 좋아요', '15')

                    title_num = list(map(str, range(1, 16)))  # 1~15만 리스트에추가 (이외에 다른 키워드들은 추가하지않음)
                    keywordCount = re.sub('이 키워드를 선택한 인원\n', '', keywordCount)
                    if title_re in title_num:
                        keywordReviewDict[str(title_re)] = keywordCount
                    else:
                        pass
                print("키워드 리뷰 개수", len(keywordList))
            else:
                print("키워드 리뷰 없음")
        except:
            print("키워드 리뷰 에러")


        # 블로그 리뷰
        try:
            reviewTabBtn = driver.find_elements_by_class_name("YGvdM")
            sleep(1)
            for reviewTab in reviewTabBtn:
                if reviewTab.text == "블로그리뷰":
                    print(reviewTab.text, "찾았다")
                    reviewTab.send_keys(Keys.ENTER)
                    break

            print("블로그 리뷰 탭 전환")
            for clickIdx in range(5):
                # page_down(40)
                if time_wait(3, 'xpath', "/html/body/div[3]/div/div/div/div[7]/div[2]/div[2]/div[2]/a"):
                    print("블로그 리스트 더보기 클릭")
                    sleep(1)
                    try:
                        driver.find_element_by_xpath("/html/body/div[3]/div/div/div/div[7]/div[2]/div[2]/div[2]/a").click()
                    except:
                        print("더보기 클릭 실패")
                else:
                    print("더보기없음 블로그 url 수집시작")
                    break

            sleep(2)
            #/html/body/div[3]/div/div/div/div[7]/div[2]/div[3]/div[1]/ul/li[1]
            if time_wait(3, "class", "xg2_q"):
                blogUrls = driver.find_elements_by_class_name("xg2_q")
            else:
                blogUrls = []
            print("블로그 url 개수: ", len(blogUrls))
            for blogUrlIdx in range(len(blogUrls)):
                sleep(0.07)
                aTag = blogUrls[blogUrlIdx].find_element_by_tag_name("a")
                getUrl = aTag.get_attribute("href")
                # print(getUrl)
                blogReview = blogCrawler.blogCrawler(getUrl)
                blogUrlList.append(getUrl)
                blogReviewList.append(blogReview)
        except:
            print("블로그 리뷰 에러")

        # ---- dict에 데이터 집어넣기----
        # { 상호명, 별점, 키워드리스트, 지도리뷰리스트, 블로그리뷰리스트}

    except:
        print(searchWord,"ERROR ERROR")
    print("수집 결과")
    result = {
        "storeIdx": storeIdx,
        "searchKeyword" : name + " " + adress,
        "name": storeName,
        "foodCategory": foodCategory,
        "rating": storeRating,
        "tell": storeTell,
        "reviews": reviewList,
        "reviewCnt" : reviewCnt,
        "blogUrls": blogUrlList,
        "blogReviews": blogReviewList,
        "blogCnt" : blogCnt,
        "keywordReviewList": keywordReviewDict,
    }
    pprint(result)
    print(f'{searchWord} ...완료')
    print('[데이터 수집 완료]\n소요 시간 :', time.time() - start)
    print(
        f"리뷰 개수 : {len(result['reviews'])} 블로그 url 개수 : {len(result['blogUrls'])} 블로그 리뷰 개수 : {len(result['blogReviews'])}")
    driver.quit()  # 작업이 끝나면 창을닫는다.
    return result


# n = "옥돌영양탕"
# a = "서울특별시 광진구 긴고랑로36길 24"
# # n = "도전최강달인왕만두"
# # a = "서울 강동구 고덕로 353"
# crawler(n, a)
