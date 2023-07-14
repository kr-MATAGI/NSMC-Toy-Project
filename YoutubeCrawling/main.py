import json
import os
import re
import time
from typing import Dict, List

import openai
import undetected_chromedriver as uc
from attrdict import AttrDict
from bs4 import BeautifulSoup
from selenium import webdriver  # webdriver를 이용해 해당 브라우저를 열기 위해
from selenium.webdriver import (
    ActionChains,  # 일련의 작업들을(ex.아이디 입력, 비밀번호 입력, 로그인 버튼 클릭...) 연속적으로 실행할 수 있게 하기 위해
)
from selenium.webdriver.common.by import By  # html요소 탐색을 할 수 있게 하기 위해
from selenium.webdriver.common.keys import Keys  # 키보드 입력을 할 수 있게 하기 위해
from selenium.webdriver.support import (
    expected_conditions as EC,  # html요소의 상태를 체크할 수 있게 하기 위해
)
from selenium.webdriver.support.ui import (
    WebDriverWait,  # 브라우저의 응답을 기다릴 수 있게 하기 위해
)

from xpath_def import XPath

'''
    @TODO:
        - time.sleep() 부분을 페이지 로딩이 완료되는 것을 확인하는 코드로 개선이 필요.
            > is_display(), is_enabled() 활용
        - 한국어 댓글만 구분하도록 정규식 추가 필요
        - 한 댓글에 여러 사람이 댓글 다는 것과 같은 현상 방지 필요
'''

'''
    Selenium 요소를 조작하는 것 중 많이 쓰일만한 것들
        1. tag_name
        2. text
        3. back() / forward()
        4. implicitly_wait(sec) : 최대 대기 시간을 초 단위로 지정해서 처리가 끝날때까지 대기
        5. set_page_load_timeout() : 페이지를 읽는 타임아웃 시간을 지정
        6. set_window_position(x, y, windowHandle), set_window_size(width, height)
'''

'''
    WebDriverWait 관련 예제
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "myDynamicElem"))
        )
    > WebDriverWait(driver, 10) -> 최대 10초동안 기다린다
    > until(EC.presence_of_element_located((By.ID, "myDynamicElement"))) -> ID에 해당하는 elem이 표시될때까지 기다림
'''

'''
    time.sleep(10) -> 페이지 로딩에 상관없이 무조건 10초를 기다리게 함.
    driver.implicitly_wait(10)은 페이지가 2초만에 로딩된다면, 10초를 기다리지 않고 바로 다음 코드로 넘어간다.
'''

'''
    Scroll 관련 동작
        1. 지정한 위치로 스크롤 내리기
            browser.execute_script("window.scrollTo(0, 900)")

        2. 화면의 가장 아래로 스크롤 내리기
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight))
'''

'''
    headless option
        > 웹 브라우저를 열지 않고 크롤링을 진행할때 사용한다.
        > headless 옵션을 사용할 경우, 서버측에서 접근을 차단하는 경우가 있기 때문에 option.add_argument를 통해
         UserAgent 값을 설정해야 한다.
'''

'''
    BeautifulSoup()
        > HTML과 XML 문서들의 구문을 분석하기 위한 파이썬 패키지
        > HTML로부터 데이터를 추출하기 위해 사용할 수 있는 파싱된 페이지의 parse tree를 만든다.
        e.g.
            soup = BeautifulSoup(arg_1, 'html.parser')

        > head / body tag의 정보 가져오기
            soup.head()
            soup.body()

        > 특정 태그 찾기 find()
            soup.find('p') -> 처음 발견한 p 태그를 가져온다
            soup.find_all('p') -> 모든 p 태그를 가져온다

        > find() 옵션인 clss_, {key:values}를 이용해서 자세하게 찾기
            soup.find('p', class_='inner-text first-item')
            soup.find('p', {'class': 'inner-text first-item'})

        > 태그 안에 있는 text만 가져오는 함수
            soup.find('p').text
            soup.find('p').string
            soup.find('p').get_text()

        > select_one(), select() 함수로 원하는 태그 찾기
            soup.select('#exchangeList > li') -> #은 id값을 이용해서 찾을 때 사용
            soup.select('.exchangeList > li') -> .은 class를 이용해서 찾을 때 사용
'''

'''
    iframe이 웹에 있을 경우, html의 elem에 접근이 어려움
    따라서 iframe에 먼저 접근해주고 크롤링을 해야한다.
    e.g.
        # iframe 태그로 이동
        iframe = selenium.find_element_by_css_selector('#frame_ex1')

        # 태그 이동
        driver.switch_to_frame(iframe)

'''

LOAD_TIME_SLEEP = 2
PROMPT_FORMAT = """
아래 Youtube 댓글들을 참고해서 새로운 비슷한 의미를 갖는 댓글을 생성해줘

{}
"""

#====================================
def do_google_login(
        id: str, passwd: str,
        web_driver
):
#====================================
    print(f'[do_google_login] id: {id}, passwd: {passwd}')

    web_driver.find_element(By.XPATH, XPath['login_btn']).click()

    # Write ID
    input_id_elem = web_driver.find_element(By.XPATH, XPath['input_id'])
    input_id_elem.click()
    input_id_elem.send_keys(id)

    # Next
    web_driver.find_element(By.XPATH, XPath['input_id_next']).click()
    time.sleep(LOAD_TIME_SLEEP * 3)

    # Write PW
    input_pw_elem = web_driver.find_element(By.XPATH, XPath['input_pw'])
    input_pw_elem.click()
    input_pw_elem.send_keys(passwd)

    # Login
    web_driver.find_element(By.XPATH, XPath['input_pw_next']).click()
    time.sleep(LOAD_TIME_SLEEP * 3) # gmail은 2단계 인증이 걸려있어서 폰에서 인증 필요...

#====================================
def get_ytb_video_comments(
    web_driver, config
):
#====================================
    html = web_driver.page_source
    result = BeautifulSoup(html,'html.parser')
    body = result.find("body")
    thread = body.find_all('ytd-comment-renderer', attrs={'class':'style-scope ytd-comment-thread-renderer'})
    comment_list = [] # Return value

    for items in thread:
        div_list = items.find_all('yt-formatted-string', attrs={'id':'content-text'})
        for div in div_list:
            try:
                cmt = div.string
                cmt = re.sub(r'<.+>', '', cmt)
                comment_list.append(cmt)
            except:
                continue

    return comment_list

#====================================
def make_request_prompt(config: AttrDict, comments: List[str]):
#====================================
    print(f'[make_request_prompt] comments.size: {len(comments)}, {comments}')

    '''
        @TODO: config에 따라 prompt를 더 가공할 수 있도록...
    '''
    prompt = PROMPT_FORMAT.format("\n\n".join(comments[:config.ref_comments]))

    return prompt

#====================================
def request_gpt(config: AttrDict, req_sent: str):
#====================================
    print(f'[request_gpt] req_sent: {req_sent}')

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": req_sent}]
    )

    res_gpt = str(completion['choices'][0]['message']['content']).split('\n')[0]
    print(f'[request_gpt] res_gpt: {res_gpt}')

    return res_gpt

#====================================
def write_gpt_comments(
    web_drvier, config,
    gpt_comments: str # List[str]
):
#====================================
    print(f'[write_gpt_comments] gpt_comments.size: {len(gpt_comments)}')

    add_cmt_box_elem = web_drvier.find_element(By.CLASS_NAME, 'style-scope ytd-comments-header-renderer')
    place_holder_elem = add_cmt_box_elem.find_element(By.ID, 'simplebox-placeholder')
    web_drvier.execute_script("arguments[0].click();", place_holder_elem)
    time.sleep(LOAD_TIME_SLEEP)

    creation_box_elem = web_drvier.find_element(By.ID, 'contenteditable-root')
    creation_box_elem.send_keys(Keys.ENTER)
    creation_box_elem.send_keys(gpt_comments)

    web_drvier.find_element(By.XPATH, XPath['upload_cmt_btn']).click()
    time.sleep(LOAD_TIME_SLEEP)

#====================================
def do_auto_update_comments_by_gpt(config):
#====================================
    # init
    openai.api_key = config.openai.api_key

    # Set web driver
    if 0 >= len(config.keyword):
        print('f[do_auto_update_comments_by_gpt] Keyword is NULL !')
        return

    # web_driver = webdriver.Chrome(config.web_driver_path)
    web_driver = uc.Chrome()
    web_driver.execute_cdp_cmd( # 구글 로그인을 위해서
            "Page.addScriptToEvaluateOnNewDocument",
            {"source": """ Object.defineProperty(navigator, 'webdriver', { get: () => undefined }) """}
    )
    web_driver.get('https://youtube.com')
    web_driver.implicitly_wait(3)
    web_driver.maximize_window()
    wait = WebDriverWait(web_driver, LOAD_TIME_SLEEP + 1)

    # Google login
    do_google_login(id=config.google.id, passwd=config.google.pwd, web_driver=web_driver)
    time.sleep(LOAD_TIME_SLEEP)

    # Wait search_bar
    search_bar_elem = web_driver.find_element(By.XPATH, XPath['search_input'])
    search_bar_elem.click()
    time.sleep(LOAD_TIME_SLEEP)

    search_bar_elem = web_driver.find_element(By.XPATH, XPath['input_form'])
    search_bar_elem.send_keys(config.keyword)
    search_bar_elem.send_keys(Keys.ENTER)
    time.sleep(LOAD_TIME_SLEEP)

    ''' 이제 부터 검색 결과 결과를 기준으로 동작 시작 '''
    content_list = web_driver.find_elements(By.CLASS_NAME, 'style-scope ytd-video-renderer')
    for cnt_idx, content_item in enumerate(content_list):
        if (cnt_idx + 1) > config.max_search:
            break

        video_title = content_item.find_element(By.ID, 'title-wrapper')
        video_title.click()
        time.sleep(LOAD_TIME_SLEEP)

        body = web_driver.find_element(By.TAG_NAME, "body")

        for _ in range(config.scroll_down_cnt):
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(LOAD_TIME_SLEEP)

        ''' 댓글 가져오기 '''
        ytb_cmt_list = get_ytb_video_comments(web_driver=web_driver, config=config)
        if 0 >= len(ytb_cmt_list):
            web_driver.back()
            time.sleep(LOAD_TIME_SLEEP)
            continue

        # Request to GPT
        req_prompt = make_request_prompt(config=config, comments=ytb_cmt_list)
        res_gpt = request_gpt(config=config, req_sent=req_prompt)

        # Wrtie GPT comments
        write_gpt_comments(web_drvier=web_driver, config=config, gpt_comments=res_gpt)

        web_driver.back()
        time.sleep(LOAD_TIME_SLEEP)

        # break # TEST
    # end loop ,

    print(f'[do_auto_update_comments_by_gpt] Complete !')

#====================================
def main(config_path: str):
#====================================
    print(f'[main] config_path: {config_path}')

    if not os.path.exists(config_path):
        raise Exception(f'ERR - config_path: {config_path}')

    # Read config
    config: Dict[str, str] = {}
    with open(config_path, mode='r', encoding='utf-8') as f:
        config = AttrDict(json.load(f))
    for key, val in config.items():
        print(f'[main] config.{key}: {val}')

    if not os.path.exists(config.web_driver_path):
        raise Exception(f'ERR - config.web_driver_path: {config.web_driver_path}')

    # Start Auto Comments by GPT
    do_auto_update_comments_by_gpt(config=config)

### Main ###
if '__main__' == __name__:
    print(f'[main.py] 간단한 유투브 댓글 생성기')

    main(config_path="./config.json")
