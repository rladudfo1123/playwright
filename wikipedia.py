from playwright.sync_api import sync_playwright, expect
import time
import re

HOME = "https://ko.wikipedia.org/"
font_sizes = [
    ("작음",0),
    ("표준",1),
    ("큼",2)
]

wide_case = [
    ("넓게", 0, "vector-feature-limited-width-clientpref-0"),
    ("표준", 1, "vector-feature-limited-width-clientpref-1")
]
WIDE_DESC = "콘텐츠는 브라우저 창에 맞도록 최대한 넓게 맞춥니다."


def SC1(page):  #시나리오1 홈화면 진입 시 사이드 패널 디폴트 확인
    panel = page.locator('xpath=//*[@id="vector-appearance-pinned-container"]')
    assert panel.is_visible(), "사이드 패널 미노출"
    print("사이드 패널 노출 확인")
    time.sleep(2)
    
    panel_title_desc = page.locator('xpath=//*[@id="vector-appearance"]/div[1]/div')
    panel_title = panel_title_desc.inner_text()
    assert panel_title == "보이기", "사이드 바 제목 오류"
    print("사이드 바 제목 보이기")
    time.sleep(2)

    panel_hide_btn = page. locator('xpath=//*[@id="vector-appearance"]/div[1]/button[2]')
    panel_hide_btn_com = panel_hide_btn.inner_text()
    assert panel_hide_btn_com == "숨기기", "사이드 바 숨기기 버튼 오류"
    print("사이드 바 숨기기 버튼 확인")
    time.sleep(2)

    fontsize_default_check = page.locator('xpath=//*[@id="skin-client-pref-vector-feature-custom-font-size-value-1"]')
    assert fontsize_default_check.is_checked(), "글 크기 표준 디폴트 오류"
    print("글 크기 표준 디폴트 선택 확인")
    time.sleep(2)

    fontwide_default_check = page.locator('xpath=//*[@id="skin-client-pref-vector-feature-limited-width-value-1"]')
    assert fontwide_default_check.is_checked(), "너비 표준 디폴트 오류"
    print("너비 표준 디폴트 선택 확인")
    time.sleep(2)

    fontcolor_default_check = page.locator('xpath=//*[@id="skin-client-pref-skin-theme-value-day"]')
    assert fontcolor_default_check.is_checked(), "글 색상 디폴트 오류"
    print("글 색상 라이트 디폴트 선택 확인")


def SC2(page):  #시나리오2 글 크기 라디오, 문구 선택 가능 검증 시나리오
    for name,value in font_sizes:

        sizeradio = f'xpath=//*[@id="skin-client-pref-vector-feature-custom-font-size-value-{value}"]'
        radio = page.locator(sizeradio)

        radio.check()
        expect(radio).to_be_checked()
        print(f"{name} 버튼 클릭 및 선택 성공")

        html_class = page.locator("html").get_attribute("class") or ""
        expected_keyword = f"vector-feature-custom-font-size-clientpref-{value}"
        assert expected_keyword in html_class, f"{name} 버튼 선택 오류"
        print(f"{name} 선택 사이즈 변경 확인")
        time.sleep(1)

    print("글자 크기 버튼 동작 확인")

    time.sleep(3)

    for name,value in font_sizes:
        
        label_click = page.locator(f'xpath=//*[@id="skin-client-prefs-vector-feature-custom-font-size"]/div[2]/ul/li/div/form/div[{value+1}]/label/span')
        radio = page.locator(f'xpath=//*[@id="skin-client-pref-vector-feature-custom-font-size-value-{value}"]')

        label_click.click()
        assert radio.is_checked(), f"{name} 문구 선택 오류"
        print(f"{name} 문구 선택")

        html_class = page.locator("html").get_attribute("class") or ""
        expected_keyword = f"vector-feature-custom-font-size-clientpref-{value}"
        assert expected_keyword in html_class, f"{name} 문구 선택 시 사이즈 변경 불가"
        print(f'{name} 문구 선택 시 사이즈 변경 확인')
        time.sleep(3)

    print("크기 문구 선택 시 동작 확인")


def SC3(page, context):     #시나리오3 글 크기 버튼 선택 시 새 탭 열어서 유지 확인
    for name,value in font_sizes:
        radio = page.locator(f'xpath=//*[@id="skin-client-pref-vector-feature-custom-font-size-value-{value}"]')    
        radio.click()
        expect(radio).to_be_checked()
        print(f"{name} 라디오 버튼 선택")
        time.sleep(2)

        new_page = context.new_page()
        new_page.goto(HOME)
        time.sleep(3)

        new_radio = page.locator(f'xpath=//*[@id="skin-client-pref-vector-feature-custom-font-size-value-{value}"]')
        if new_radio.is_checked():
            print(f"새탭 {name} 설정 유지")
        else:
            print(f"새탭 {name} 설정 유지 X")

        new_page.close()
        time.sleep(3)
    print("글자 크기 설정 유지 확인")


def SC4(page):   #시나리오4 글 너비 라디오, 문구 선택 가능 검증 시나리오
    for name, value, keys in wide_case:

        wideradio = page.locator(f'xpath=//*[@id="skin-client-pref-vector-feature-limited-width-value-{value}"]')
        wideradio.click()
        expect(wideradio).to_be_checked()
        html_class = page.locator("html").get_attribute("class") or ""
        assert keys in html_class, f"{name} 선택 후 반영 실패"
        print(f"{name}선택 확인")

        time.sleep(3)

        if value == 0:
            desc = page.locator(f'xpath=//*[@id="skin-client-prefs-vector-feature-limited-width"]/div[2]/span')
            text = (desc.inner_text() or "").strip()
            assert text == WIDE_DESC, "넓게 DESC 오류"
            print("넓게 desc 문구 확인")
        else:
            print("표준 선택 시 desc 미노출")
        time.sleep(3)

    for name, value, keys in wide_case:
        div_index = 2 if value == 0 else 1
        wide_label_click = page.locator(f'xpath=//*[@id="skin-client-prefs-vector-feature-limited-width"]/div[2]/ul/li/div/form/div[{div_index}]/label/span')
        wideradio = page.locator(f'xpath=//*[@id="skin-client-pref-vector-feature-limited-width-value-{value}"]')

        wide_label_click.click()
        assert wideradio.is_checked(), f"{name} 문구 선택 오류"
        print(f"{name} 선택")        
        time.sleep(3)

        html_class = page.locator("html").get_attribute("class") or ""
        expected_widekey = f'vector-feature-limited-width-clientpref-{value}'
        assert keys in html_class, f"{name} 선택 후 반영 실패"
        print(f"{name} 선택 시 너비 반영")
        time.sleep(3)


    print("너비 라디오 버튼 검증 끝")


def SC5(page, context):   #시나리오5 글 너비 선택 시 새 탭 열어서 유지 확인
    for name, value, keys in wide_case:
        radiowide = page.locator(f'xpath=//*[@id="skin-client-pref-vector-feature-limited-width-value-{value}"]')
        radiowide.click()
        expect(radiowide).to_be_checked()
        print(f"{name} 라디오 버튼 선택")
        time.sleep(2)

        new_page = context.new_page()
        new_page.goto(HOME)
        time.sleep(2)

        new_radiowide = page.locator(f'xpath=//*[@id="skin-client-pref-vector-feature-limited-width-value-{value}"]')
        if new_radiowide.is_checked():
            print(f"새탭 {name} 설정 유지")
        else:
            print(f"새탭 {name} 설정 유지 X")

        new_page.close()
        time.sleep(2)
    print("글자 너비 설정 유지 확인")

def SC6(page): #시나리오6 버튼 선택 해제 불가, 복수 선택 불가 TC
    for name, value in font_sizes:
        sizeradio = f'xpath=//*[@id="skin-client-pref-vector-feature-custom-font-size-value-{value}"]'
        radio = page.locator(sizeradio)

        radio.check()
        expect(radio).to_be_checked()
        print(f"{name} 버튼 클릭 및 선택 성공")
        
        radio = page.locator(sizeradio)
        radio.check()
        expect(radio).to_be_checked()

        html_class = page.locator("html").get_attribute("class") or ""
        expected_keyword = f"vector-feature-custom-font-size-clientpref-{value}"
        assert expected_keyword in html_class, f"{name} 버튼 선택 오류"
        print(f"{name} 재선택 해제 불가 및 폰트 사이즈 유지")

        for other_name, other_value in font_sizes:
            if other_value != value:
                other_radio = page.locator(f'xpath=//*[@id="skin-client-pref-vector-feature-custom-font-size-value-{other_value}"]')
                assert not other_radio.is_checked(), f"{name} 선택 시 {other_name}도 체크됨 (복수 선택 오류)"
                print(f"{name} 선택 시 {other_name} 체크해제")


def SC7(page):
    for name, value, keys in wide_case:
        wideradio = page.locator(f'xpath=//*[@id="skin-client-pref-vector-feature-limited-width-value-{value}"]')
        wideradio.click()
        expect(wideradio).to_be_checked()
        print(f"{name} 버튼 클릭 및 선택 성공")
        wideradio.check()
        expect(wideradio).to_be_checked()

        html_class = page.locator("html").get_attribute("class") or ""
        assert keys in html_class, f"{name} 선택 후 반영 실패"
        print(f"{name} 재선택 확인")

        for other_name, other_value, keys in wide_case:
            if other_value != value:
                other_radio = page.locator(f'xpath=//*[@id="skin-client-pref-vector-feature-limited-width-value-{other_value}"]')
                assert not other_radio.is_checked(), f"{name} 선택 시 {other_name}도 체크됨 (복수 선택 오류)"
                print(f"{name} 선택 시 {other_name} 체크해제")

        time.sleep(3)
      



# 사이드 패널 숨기기 버튼 선택
def open_appearance_button(page):
    btn = page.locator('xpath=/html/body/div[2]/div/div[3]/main/div[2]/div/nav[2]/div/div/div[1]/button[2]')
    btn.wait_for(state="visible")
    btn.click()
    time.sleep(1)

    pop = page.locator('xpath=/html/body/div[1]/header/div[2]/nav/div[1]/nav/div[2]/div[1]/div')
    pop_value = pop.get_attribute("popdesc")
    print("popdesc: ", pop_value)

    widthwide_radio = page.locator('xpath=//*[@id="skin-client-pref-vector-feature-limited-width-value-0"]')
    widthwide_radio.click()
    print("너비 넓게 선택 가능")

    # 넓게 설명문 텍스트 추출
    widthwide_desc = page.locator('xpath=//*[@id="skin-client-prefs-vector-feature-limited-width"]/div[2]/span')
    wide_desc = widthwide_desc.inner_text()
    print("desc = ",wide_desc)

    # 넓게 설명문 텍스트 확인
    if wide_desc == "콘텐츠는 브라우저 창에 맞도록 최대한 넓게 맞춥니다." :
        print("넓게 설명문 확인")
    else:
        print("넓게 설명문 오류")

with sync_playwright() as p:
    browser = p.firefox.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(HOME)
    time.sleep(3)

    #SC6(page)

    SC7(page)


    # SC1(page)    # 시나리오1 테스트케이스
    # time.sleep(3)

    # SC2(page)    # 시나리오2 테스트케이스
    # time.sleep(3)
   
    # SC3(page, context) # 시나리오3 테스트케이스
    # time.sleep(3)

    # SC4(page) # 시나리오4 테스트케이스
    # time.sleep(3)

    # SC5(page, context) # 시나리오5 테스트케이스
    # time.sleep(3)

    # open_appearance_button(page) #사이드 바 숨기기 버튼

    time.sleep(3)
    browser.close()

