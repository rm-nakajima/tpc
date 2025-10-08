# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time
from datetime import date, timedelta, datetime as dt
import datetime
import chromedriver_binary
import re
import csv
import random
import copy
import sys

##開始時刻をエポック秒で取得（処理時間の計算用）
s_time = time.time()
##############################

def readFile(FILENAME):
    xi = open(FILENAME, 'r', encoding='UTF-8')
    xii = xi.read()
    if '\n' in xii:
        xii = xii.split('\n')
        xii = [x for x in xii if x != '']
    else:
        xii = [xii]
    return xii

def Null(X):
    x = []
    for i in range(X):
        x.append('')
    return x
##############################
# 本日の日付を取得
##############################
today = date.today()
##############################
# data.txt
##############################
targetDate = readFile('date.txt')
##############################
# race-name.txt
##############################
race_h_type = readFile('race-name.txt')
##############################
# race-case.txt
##############################
race_h_case = readFile('race-case.txt')
##############################
# race-course.txt
##############################
race_h_course = readFile('race-course.txt')
##############################
# save.txt
##############################
savePath = readFile('save.txt')
savePath = savePath[0]
if savePath.endswith('/') or savePath.endswith('¥'):
    pass
else:
    if '¥' in savePath:
        savePath = savePath + '¥'
    else:
        savePath = savePath + '/'
############################
# ChromeDriver
############################
# Chrome展開
option = Options()
option.add_argument('--incognito')
driver = webdriver.Chrome(options=option)
driver.set_window_size(1920,1080)

target = []
for i in range(len(targetDate)):
    target.append('https://www.racingpost.com/results/' + targetDate[i])
print('対象URL:')
print(target)
for z in range(len(target)):
    ##############################
    # 対象日の一覧に遷移
    ##############################
    driver.get(target[z])
    #cookieバナー
    try:
        cookie = driver.find_element(By.CSS_SELECTOR, '.trustarc-banner-container')
        btn = cookie.find_elements(By.CSS_SELECTOR, 'button')
        for i in range(len(btn)):
            el = btn[i].get_attribute('innerHTML')
            if 'Accept All' in el:
                btn[i].click()
            else:
                pass
    except:
        pass
    ############################
    # CSV生成
    ############################
    FileName = savePath + 'racingpost01_' + str(targetDate[z]) + ".csv"
    Err_FileName = savePath + 'Err_racingpost01_' + str(targetDate[z]) + ".txt"
    f = open(FileName, 'w', encoding="utf_8_sig")
    writer = csv.writer(f, lineterminator='\n')

    # エラー時のログ生成
    def Er_log(a):
        fErr = open(Err_FileName, 'a', encoding="utf_8_sig")
        fErr.write('エラー発生URL: ' + url[y])
        fErr.write('\n' + a + ' 取得エラー\n')

    label = ["競馬場コード","競馬場","国名","レース日付","レース名","レース格","レース他","レース名省略","出走条件（性別）","馬場の種類",\
        "馬場の種類（英愛）","出走条件（クラス）","出走条件（他）","出走条件（年齢）","距離","コース形態","コース詳細","馬場状態","障害数","障害レース確認",\
            "着賞金","並び順位","確定順位","異常区分","同着","着変更","ゲート番号","着差1","着差2","馬名",\
                "生産国","オッズ","馬齢","斤量","斤量特記1","斤量特記2","補助馬具","調教師","騎手","毛色",\
                    "性別","父名","母名","母父名","出走頭数","優勝馬タイム","優勝馬オーナー","優勝馬生産者","コメント"]
    writer.writerow(label)

    ##############################
    # 日付の照合
    ##############################
    #try:
    #    if targetDate[z] > today:
    #        print('対象日時: ERROR')
    #        sys.exit()
    #    elif targetDate[z] <= today:
    #        pass
    #except:
    #    sys.exit()
    ##############################
    # レース別の結果URLをリストで取得
    url = driver.find_elements(By.CSS_SELECTOR, '.rp-raceCourse__panel__race__info__buttons__link')
    url = [x.get_attribute('href') for x in url]
    print('>> ' + str(targetDate[z]) + ': ' + str(len(url)) + 'レース')

    ##############################
    #
    ##############################
    for y in range(len(url)):
        driver.get(url[y])
        # JavaScriptで直接オーバーレイを非表示にする
        driver.execute_script('''
            const overlay = document.getElementById("trustarc-banner-overlay");
            if (overlay) overlay.style.display = "none";
            const blackout = document.querySelector(".consent_blackbar");
            if (blackout) blackout.style.display = "none";
        ''')

        wait = WebDriverWait(driver, 10)
        # オーバーレイが消えるのを待つ
        wait.until(EC.invisibility_of_element_located((By.ID, "trustarc-banner-overlay")))
        # クリック対象の要素がクリック可能になるまで待つ
        element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".rp-horseTable__pedigreesBtn")))
        element.click()
        ##############################
        # pedigreeをアクティベート
        ##############################
        time.sleep(1)
        pgFlg = driver.find_elements(By.CSS_SELECTOR, '.rp-horseTable__pedigreesBtn.ui-btn_toggleActive')
        if len(pgFlg) > 0:
            pass
        else:
            driver.find_element(By.CSS_SELECTOR, '.rp-horseTable__pedigreesBtn').click()
            time.sleep(1)
        ##############################
        # 出走頭数
        ##############################
        try:
            value = driver.find_elements(By.CSS_SELECTOR, '.rp-horseTable__mainRow')
            value = len(value)
        except:
            value = 0
        try:
            sValue = driver.find_element(By.CSS_SELECTOR, '.rp-raceInfo__value_black').text.strip()
            sValue = sValue.split(' ')[0]
            sValue = int(sValue)
        except:
            sValue = 0
        ##############################
        # 競馬場コード
        ##############################
        try:
            rc_code = url[y].split('/results/')[1].split('/')[0].strip()
        except:
            rc_code = ''
        ##############################
        # 競馬場
        ##############################
        try:
            Course = driver.find_element(By.CSS_SELECTOR, '.rp-raceTimeCourseName__name').text.strip()
        except:
            Course = ''
        ##############################
        # 国名、馬場の種類（英愛）
        ##############################
        try:
            countryCode = ''
            rcType = ''
            with open('Racingpost_Country.csv', encoding="utf_8") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[1] == rc_code:
                        countryCode = row[0]
                        rcType = row[3]
                    else:
                        pass
        except:
            countryCode = ''
            rcType = ''
        ##############################
        # レース日付
        ##############################
        try:
            Date = driver.find_element(By.CSS_SELECTOR, '.rp-raceTimeCourseName__date').text.strip()
            Date = datetime.datetime.strptime(Date, '%d %b %Y').strftime('%Y/%m/%d')
        except:
            Date = ''
        ##############################
        # レース名
        ##############################
        try:
            raceName = driver.find_element(By.CSS_SELECTOR, '.rp-raceTimeCourseName__title').text.strip()
        except:
            raceName = ''
        ##############################
        # コース形態
        ##############################
        courseShape = ''
        try:
            for i in race_h_course:
                if i in raceName:
                    courseShape = i.replace('(','').replace(')','')
        except:
            pass
        ##############################
        # 出走条件（他）
        ##############################
        if 'Maiden' in raceName:
            raceTerms = 'Maiden'
        else:
            raceTerms = ''
        ##############################
        # 障害レース確認
        ##############################
        if 'Hurdle' in raceName:
            hurdleCheck = 'Hurdle'
        elif 'Chase' in raceName:
            hurdleCheck = 'Chase'
        else:
            hurdleCheck = ''
        ##############################
        # レース格
        ##############################
        raceCase = ''
        try:
            for i in race_h_case:
                if i in raceName:
                    h_case = raceName.split(')')
                    for ii in h_case:
                        if i in ii:
                            raceCase = ii.split('(')[1]
        except:
            pass
        ##############################
        # 出走条件（性別）
        ##############################
        raceType = ''
        try:
            for i in race_h_type:
                if i in raceName:
                    raceType = i
        except:
            pass
        ##############################
        # 馬場の種類
        ##############################
        courseType = ''
        try:
            xi = raceName.split('(')
            xi = [x.replace(')', '').strip() for x in xi]
            del xi[0]
            xii = []
            for i in xi:
                if 'Turf' in i or 'Dirt' in i or 'All-Weather' in i or 'Polytrack' in i:
                    xii.append(i)
            courseType = (',').join(xii)
        except:
            pass
        ##############################
        # レース他
        ##############################
        raceOther = []
        try:
            xi = raceName.split('(')
            del xi[0]
            xi = [x.replace(')','').strip() for x in xi]
            xii = []
            for i in xi:
                if i == raceCase or i == raceType or i == courseType:
                    pass
                else:
                    xii.append(i)
            for i in xii:
                raceOther.append("'" + i + "'")
            raceOther = (',').join(raceOther)
        except:
            raceOther = ''
        ##############################
        # 出走条件（クラス）
        ##############################
        try:
            raceClass = driver.find_element(By.CSS_SELECTOR, '.rp-raceTimeCourseName_class')\
                .text.replace('(','').replace(')','').strip()
        except:
            raceClass = ''
        ##############################
        # レース名省略
        ##############################
        try:
            raceNameAbbr = raceName.split('(')
            raceNameAbbr = raceNameAbbr[0].strip()
        except:
            raceNameAbbr = raceName
        ##############################
        # 出走条件（年齢）
        ##############################
        try:
            raceRating = driver.find_element(By.CSS_SELECTOR, '.rp-raceTimeCourseName_ratingBandAndAgesAllowed')\
                .text.replace('(','').replace(')','').strip()
        except:
            raceRating = ''
        ##############################
        # 距離
        ##############################
        try:
            Distance = driver.find_element(By.CSS_SELECTOR, '.rp-raceTimeCourseName_distanceFull')\
                .text.replace('(','').replace(')','').strip()
        except:
            try:
                Distance = driver.find_element(By.CSS_SELECTOR, '.rp-raceTimeCourseName_distance')\
                    .text.replace('(','').replace(')','').strip()
            except:
                Distance = ''
        ##############################
        # コース詳細
        ##############################
        try:
            courseForm = driver.find_element(By.CSS_SELECTOR, '.rp-raceTimeCourseName_distanceDetail')\
                .text.strip()
        except:
            courseForm = ''
        ##############################
        # 馬場状態
        ##############################
        try:
            Condition = driver.find_element(By.CSS_SELECTOR, '.rp-raceTimeCourseName_condition')\
                .text.strip()
        except:
            Condition = ''
        ##############################
        # 障害数
        ##############################
        try:
            hurdles = driver.find_element(By.CSS_SELECTOR, '.rp-raceTimeCourseName_hurdles')\
                .text.strip()
        except:
            hurdles = ''
        ##############################
        # 賞金額（辞書型に一時格納）
        ##############################
        try:
            pDict = {}
            xi = driver.find_element_by_xpath('//div[@data-test-selector="text-prizeMoney"]').text
            xii = driver.find_elements(By.CSS_SELECTOR, '.rp-raceTimeCourseName__prizeMoneyTitle')
            xii = [x.text for x in xii]
            for i in xii:
                xi = xi.replace(i,'')
            xi = xi.split('  ')
            xi = [x.strip() for x in xi]
            for i in xii:
                i = re.split(r'\D',i)[0].strip()
                if re.match(r'^\d', i):
                    pDict[i] = ''
            if len(xi) == len(pDict):
                for i in range(len(xi)):
                    pDict[str(i + 1)] = xi[i]
        except:
            pDict = {}
        ##############################
        # 並び順位 / 確定着順 / 異常区分
        ##############################
        try:
            num = []
            numFix = []
            numCode = []
            xi = driver.find_elements(By.CSS_SELECTOR, '.rp-horseTable__pos__number')
            xi = [x.text.split('(')[0].strip() for x in xi]
            # 並び順位
            for i in range(value):
                num.append(str(i + 1))
            # 確定順位 / 異常区分
            for i in range(value):
                if "BD" in xi[i] or "REF" in xi[i] or "RO" in xi[i] or "SU" in xi[i]:
                    numFix.append('100')
                    numCode.append(xi[i])
                elif "DSQ" in xi[i]:
                    numFix.append('95')
                    numCode.append(xi[i])
                elif "UR" in xi[i] or "RR" in xi[i] or "PU" in xi[i] or "F" in xi[i]:
                    numFix.append('94')
                    numCode.append(xi[i])
                elif xi[i].isalpha() != False:
                    numFix.append('101')
                    numCode.append(xi[i])
                else:
                    numFix.append(xi[i])
                    numCode.append('')

        except:
            num = Null(value)
            numFix = Null(value)
            numCode = Null(value)
        ##############################
        # 確定着順と賞金額を照合
        ##############################
        try:
            prize = []
            for i in numFix:
                if i in pDict.keys():
                    prize.append(pDict[i])
                else:
                    prize.append('')
        except:
            prize = Null(value)
        ##############################
        # 同着
        ##############################
        try:
            arrival = []
            for i in range(len(numFix)):
                arrival.append('')
                # 重複する確定順位を抽出
                dupNum = [x for x in set(numFix) if numFix.count(x) > 1]
                if len(dupNum) > 0:
                    for i in range(value):
                        for ii in range(len(numFix)):
                            try:
                                if numFix[ii] == dupNum[i] and int(numFix[ii]) < 94 and int(numFix[ii]) != 0:
                                    arrival[ii] = 'dht'
                            except:
                                pass
        except:
            arrival = Null(value)
        ##############################
        # 　着順変更
        ##############################
        try:
            numChange = []
            for i in range(value):
                if arrival[i] == 'dht' and num[i] != numFix[i]:
                    numChange.append('*')
                else:
                    numChange.append('')
        except:
            numChange = Null(value)
        ##############################
        # ゲート番号
        ##############################
        try:
            gate = driver.find_elements(By.CSS_SELECTOR, '.rp-horseTable__pos__number')
            gate = [x.text.split('(')[1].replace(')','').strip() for x in gate]
        except:
            gate = Null(value)
        ##############################
        # 着差
        ##############################
        try:
            margin01 = []
            margin02 = []
            xi = driver.find_elements(By.CSS_SELECTOR, '.rp-horseTable__pos__length')
            for i in xi:
                xii = i.find_elements(By.CSS_SELECTOR, 'span')
                if len(xii) == 1:
                    margin01.append(xii[0].text.replace('[','').replace(']','').strip())
                    margin02.append('')
                elif len(xii) > 1:
                    margin01.append(xii[0].text.replace('[','').replace(']','').strip())
                    margin02.append(xii[1].text.replace('[','').replace(']','').strip())
        except:
            margin01 = Null(value)
            margin02 = Null(value)
        ##############################
        # 馬名
        ##############################
        try:
            horseName = driver.find_elements(By.CSS_SELECTOR, '.rp-horseTable__horse__name')
            horseName = [x.get_attribute('innerHTML').split('<svg')[0].strip() for x in horseName]
        except:
            horseName = Null(value)
        ##############################
        # 生産国
        ##############################
        try:
            horseCountry = driver.find_elements(By.CSS_SELECTOR, '.rp-horseTable__horse__country')
            horseCountry = [x.text.strip().replace('(','').replace(')','') for x in horseCountry]
            for i in range(len(horseCountry)):
                if horseCountry[i] == '':
                    horseCountry[i] = 'GB'
        except:
            horseCountry = Null(value)
        ##############################
        # オッズ
        ##############################
        try:
            odds = driver.find_elements(By.CSS_SELECTOR, '.rp-horseTable__horse__price')
            odds = [x.text.strip() for x in odds]
        except:
            odds = Null(value)
        ##############################
        # 馬齢
        ##############################
        try:
            age = driver.find_elements(By.CSS_SELECTOR, '.rp-horseTable__spanNarrow_age')
            age = [x.text.strip() for x in age]
        except:
            age = Null(value)
        ##############################
        # 斤量 / 斤量特記1 / 斤量特記2 / 補助馬具
        ##############################
        try:
            weight = []
            exData = []
            windOpe = []
            headGear = []
            xi = driver.find_elements(By.CSS_SELECTOR, 'td.rp-horseTable__wgt')
            for i in xi:
                # 斤量
                try:
                    xii = i.find_element_by_css_selector('.rp-horseTable__st').text.strip()
                    xiii = i.find_element_by_css_selector('span[data-test-selector="horse-weight-lb"]').text.strip()
                    x = xii + '-' + xiii
                    weight.append(x)
                except:
                    weight.append('')
                # 斤量特記1
                try:
                    xii = i.find_element_by_css_selector('.rp-horseTable__extraData')
                    if len(xii.find_elements(By.CSS_SELECTOR, 'img')) > 0:
                        xiii = xii.find_element_by_css_selector('.rp-horseTable__extraData img').get_attribute('alt')
                    else:
                        xiii = ''
                    x = xiii + ' ' + xii.text.strip()
                    exData.append(x.strip())
                except:
                    exData.append('')
                # 斤量特記2
                try:
                    if len(i.find_elements(By.CSS_SELECTOR, '.rp-horseTable__windOperations')) > 0:
                        x = i.find_elements(By.CSS_SELECTOR, '.rp-horseTable__windOperations').text.strip()
                    else:
                        x = ''
                    windOpe.append(x)
                except:
                    windOpe.append('')
                # 補助馬具
                try:
                    if len(i.find_elements(By.CSS_SELECTOR, '.rp-horseTable__headGear')) > 0:
                        x = i.find_elements(By.CSS_SELECTOR, '.rp-horseTable__headGear').text.strip()
                    else:
                        x = ''
                    headGear.append(x)
                except:
                    headGear.append('')
        except:
            weight = Null(value)
            exData = Null(value)
            windOpe = Null(value)
            headGear = Null(value)
        ##############################
        # 調教師
        ##############################
        try:
            trainer = driver.find_elements(By.CSS_SELECTOR, 'td.rp-horseTable__humanCell a[data-test-selector="link-trainerName"]')
            trainer = [x.text.strip() for x in trainer]
        except:
            trainer = Null(value)
        ##############################
        # 騎手
        ##############################
        try:
            jockey = driver.find_elements(By.CSS_SELECTOR, 'td.rp-horseTable__humanCell a[data-test-selector="link-jockeyName"]')
            jockey = [x.text.strip() for x in jockey]
        except:
            jockey = Null(value)
        ##############################
        # 毛色と性別
        ##############################
        try:
            coatColor = []
            gender = []
            pedigree = driver.find_elements(By.CSS_SELECTOR, '.rp-horseTable__pedigreeRow td')
            pedigree = [x.text.strip().split(' ') for x in pedigree]
            for i in pedigree:
                coatColor.append(i[0])
                gender.append(i[1])
        except:
            coatColor = Null(value)
            gender = Null(value)
        sire = []
        mare = []
        try:
            obj =  driver.find_elements(By.CSS_SELECTOR, '.rp-horseTable__pedigreeRow')
            for i in range(len(obj)):
                try:
                    elm01 = obj[i].find_element_by_css_selector('a:nth-of-type(1)').get_attribute('innerHTML')
                    elm01 = elm01.split('<svg')[0].strip()
                    if '(' in elm01:
                        elm01 = elm01.split('(')
                        elm01 = [x.strip() for x in elm01]
                        elm01[1] = '(' + elm01[1]
                        elm01 = (' ').join(elm01)
                except:
                    elm01 = ''
                sire.append(elm01)
                try:
                    elm02 = obj[i].find_element_by_css_selector('a:nth-of-type(2)').get_attribute('innerHTML')
                    elm02 = elm02.split('<svg')[0].strip()
                    if '<span>' in elm02:
                        elm02 = elm02.split('</span>')[0].split('<span>')
                        elm02 = [x.strip() for x in elm02]
                        elm02 = (' ').join(elm02)
                except:
                    elm02 = ''
                mare.append(elm02)
        except:
           sire = Null(value)
           mare = Null(value)
        ##############################
        # 母父名
        ##############################
        try:
            bms = []
            bmsDisc = driver.find_elements(By.CSS_SELECTOR, '.rp-horseTable__pedigreeRow')
            for i in bmsDisc:
                bmsFlg = i.find_elements(By.CSS_SELECTOR, 'a:nth-child(3)')
                bmsFlg = [x.get_attribute('innerHTML').split('<svg')[0].strip().replace("))","-*)") for x in bmsFlg]
                bmsFlg = [x.strip("()").replace("-*",")") for x in bmsFlg]
                if len(bmsFlg) != 0:
                    bms.append(str(bmsFlg[0]))
                else:
                    bms.append('')
        except:
            bms = Null(value)
        ##############################
        # 下部レース情報
        ##############################
        rp_info = driver.find_element(By.CSS_SELECTOR, '.rp-raceInfo')
        rp_info_cmp = rp_info.find_elements(By.CSS_SELECTOR, '.rp-raceInfo__value')
        rp_info_cmp = [x.text.strip() for x in rp_info_cmp]
        rp_info_cmp_a = rp_info.find_elements(By.CSS_SELECTOR, '.ui-profileLink')
        rp_info_cmp_a = [x.text.strip() for x in rp_info_cmp_a]
        ##############################
        # 優勝馬タイム
        ##############################
        try:
            valueTime = []
            xi = rp_info.text.split('Winning time:')[1].split('\n')[0].strip()
            for i in rp_info_cmp:
                if i in xi:
                    valueTime.append(i)
            valueTime = [valueTime[0]]
            if '(' in valueTime[0]:
                valueTime[0] = valueTime[0].split('(')[0].strip()
            for i in range(value - 1):
                valueTime.append('')
        except:
            valueTime = Null(value)
        ##############################
        # 優勝馬オーナー
        ##############################
        try:
            owner = []
            xi = rp_info.find_elements(By.CSS_SELECTOR, 'li')
            for i in xi:
                if '1st owner:' in i.text:
                    xii = i.find_element_by_css_selector('a').get_attribute('innerHTML').split('<svg')[0].strip()
                    owner.append(xii)
            for i in range(value - 1):
                owner.append('')
            owner = [x.replace('&amp;','&') for x in owner]
        except:
            owner = Null(value)
        ##############################
        # 優勝馬生産者
        ##############################
        try:
            breeder = rp_info.find_element_by_css_selector('span[data-test-selector="text-breederFullResults"]').text.strip()
            breeder = [breeder]
            for i in range(value - 1):
                breeder.append('')
        except:
            breeder = Null(value)
        ##############################
        # コメント
        ##############################
        try:
            comment = driver.find_elements(By.CSS_SELECTOR, '.rp-horseTable__commentRow')
            comment = [x.text.strip() for x in comment]
        except:
            comment = Null(value)

        ##############################
        # 成形
        ##############################
        try:
            for i in range(value):
                record01 = [rc_code,Course,countryCode,Date,raceName,raceCase,raceOther,raceNameAbbr,raceType,courseType,\
                    rcType,raceClass,raceTerms,raceRating,Distance,courseShape,courseForm,Condition,hurdles,hurdleCheck]
                record02 = [prize[i],num[i],numFix[i],numCode[i],arrival[i],numChange[i],gate[i],margin01[i],margin02[i],horseName[i],horseCountry[i],\
                    odds[i],age[i],weight[i],exData[i],windOpe[i],headGear[i],trainer[i],jockey[i],\
                        coatColor[i],gender[i],sire[i],mare[i],bms[i],sValue,valueTime[i],owner[i],breeder[i],comment[i]]
                recordFix = record01 + record02
                writer.writerow(recordFix)
                print(recordFix)
        except:
            print('ERROR')
            Er_log('CSV生成')

driver.quit()
##終了時刻をエポック秒で取得（処理時間の計算用）
e_time = time.time()
p_time = e_time - s_time
##処理時間の表示
print('処理時間（秒）: ' + str(p_time))
sys.exit()