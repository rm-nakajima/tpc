# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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
driver = webdriver.Chrome()
options = Options()
driver.set_window_size(1300,768)

target = []
for z in range(len(targetDate)):
    target.append('https://www.racingpost.com/racecards/' + targetDate[z])
print('対象URL:')
print(target)

for z in range(len(target)):
    ##############################
    # 対象日の一覧に遷移
    ##############################
    driver.get(target[z])
    #cookieバナー
    try:
        cookie = driver.find_element_by_css_selector('.trustarc-banner-container')
        btn = cookie.find_elements_by_css_selector('button')
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
    FileName = savePath + 'racingpost03_' + str(targetDate[z]) + ".csv"
    Err_FileName = savePath + 'Err_racingpost03_' + str(targetDate[z]) + ".txt"
    f = open(FileName, 'w', encoding="utf_8_sig")
    writer = csv.writer(f, lineterminator='\n')

    label = ["発走時刻","競馬場","開催日","距離","レース名","レース格","レースその他","出走条件（クラス）","出走条件（年齢）","馬場の種類",\
        "番号","馬名","馬齢","毛色","性別","父名","母名","母の父"]
    writer.writerow(label)

    # レース別のURLをリストで取得
    url = driver.find_elements_by_css_selector('.RC-meetingItem__link')
    url = [x.get_attribute('href') for x in url]
    print('>> ' + str(targetDate) + ': ' + str(len(url)) + 'レース')

    ##############################
    # レース詳細
    ##############################
    for y in range(len(url)):
        # エラー時のログ生成
        def Er_log(a):
            fErr = open(Err_FileName, 'a', encoding="utf_8_sig")
            fErr.write('エラー発生URL: ' + url[y])
            fErr.write('\n' + a + ' 取得エラー\n')

        driver.get(url[y])

        ##############################
        # JavaScript
        ##############################
        script = 'elem01 = document.querySelector(".RC-raceCondition");\
            elem02 = document.querySelectorAll(".RC-pedigree_hidden");\
                elem01.style.cssText = "display:block";\
            for(i = 0; i < elem02.length; i++) {\
                elem02[i].style.cssText = "display:block";\
            }'
        ##############################
        # 出走頭数の取得
        ##############################
        try:
            runCount = driver.find_elements_by_css_selector('.RC-runnerRow')
            runCount = len(runCount)
            if runCount < 40:
                driver.execute_script(script)
            else:
                time.sleep(5)
                driver.execute_script(script)
        except:
            runCount = 0
        ##############################
        # 発走時刻
        ##############################
        try:
            courseTime = driver.find_element_by_css_selector('.RC-courseHeader__time').text.strip()
        except:
            courseTime = ''
            Er_log('発走時刻')
        ##############################
        # 競馬場
        ##############################
        try:
            courseName = driver.find_element_by_css_selector('h1.RC-courseHeader__name').text.strip()
        except:
            courseName = ''
            Er_log('競馬場')
        ##############################
        # レースその他
        ##############################
        try:
            courseSurface = driver.find_element_by_css_selector('.RC-courseHeader__surface').text.strip()
        except:
            courseSurface = ''
        ##############################
        # 開催日
        ##############################
        try:
            courseDate = driver.find_element_by_css_selector('.RC-courseHeader__date').text.strip()
            courseDate = courseDate.split('\n')[0].strip()
            courseDate = datetime.datetime.strptime(courseDate, '%d %b %Y').strftime('%Y/%m/%d')
        except:
            courseDate =''
            Er_log('開催日')
        ##############################
        # レース情報
        ##############################
        rpHead = driver.find_element_by_css_selector('.RC-cardHeader__courseDetails.RC-cardHeader__courseDetails--desktop')
        rpInfo = driver.find_element_by_css_selector('.RC-raceCondition')
        ##############################
        # 距離
        ##############################
        try:
            courseDist = rpHead.find_element_by_css_selector('*[data-test-selector="RC-header__raceDistance"]').text.strip()
        except:
            try:
                courseDist = rpHead.find_element_by_css_selector('*[data-test-selector="RC-header__raceDistanceRound"]').text.strip()
            except:
                courseDist = ''
                Er_log('距離')
        courseDist = courseDist.replace('(','').replace(')','')
        ##############################
        # レース名
        ##############################
        try:
            raceTitle = rpHead.find_element_by_css_selector('span[data-test-selector="RC-header__raceInstanceTitle"]').text.strip()
        except:
            raceTitle = ''
            Er_log('レース名')
        ##############################
        # レース格
        ##############################
        raceCase = []
        try:
            for i in range(len(race_h_case)):
                if race_h_case[i] in raceTitle:
                    h_case = raceTitle.split(')')
                    for c in range(len(h_case)):
                        if race_h_case[i] in h_case[c]:
                            h_case[c] = h_case[c].split('(')[1]
                            raceCase.append(h_case[c])
                        else:
                            raceCase.append('')
                        raceCase = [x for x in raceCase if x != '']
                else:
                    raceCase.append('')
            raceCase = raceCase[0]
        except:
            raceCase = ''
        ##############################
        # 出走条件（クラス）
        ##############################
        try:
            raceClass = rpHead.find_element_by_css_selector('*[data-test-selector="RC-header__raceClass"]')
            raceClass = raceClass.text.replace('(','').replace(')','').strip()
        except:
            raceClass = ''
        ##############################
        # 出走条件（年齢）
        ##############################
        try:
            rpAges = rpHead.find_element_by_css_selector('*[data-test-selector="RC-header__rpAges"]')
            rpAges = rpAges.text.replace('(','').replace(')','').strip()
        except:
            rpAges = ''
        ##############################
        # 馬場の種類
        ##############################
        try:
            ## レース名を「(」で区切り、各括弧内の文字列をリストで取得
            raceSlice = raceTitle.split('(')
            raceSlice = [x.replace(')', '').strip() for x in raceSlice]
            del raceSlice[0]
            ## 分割した各要素内に「Turf」「Dirt」「All-Weather」「Polytrack」いずれかの文字列が含まれる場合は
            ## その要素を馬場の種類として出力
            courseType = ''
            for sl in range(len(raceSlice)):
                if re.search('Turf', raceSlice[sl]) or re.search('Dirt', raceSlice[sl]) or re.search('All-Weather', raceSlice[sl]) or re.search('Polytrack', raceSlice[sl]):
                    courseType = raceSlice[sl]
                else:
                    pass
        except:
            courseType = ''
        ##############################
        # 関数
        ##############################
        def getRunInfo(a):
            xi = driver.find_elements_by_css_selector(a)
            xi = [x.text.strip() for x in xi]
            return xi
        ##############################
        # 番号
        ##############################
        try:
            runNum = getRunInfo('.RC-runnerNumber__no')
        except:
            runNum = Null(runCount)
            Er_log('番号')
        ##############################
        # 馬名
        ##############################
        try:
            runName = getRunInfo('.RC-runnerName')
        except:
            runName = Null(runCount)
            Er_log('馬名')
        ##############################
        # 馬齢
        ##############################
        try:
            runAge = getRunInfo('.RC-runnerAge')
        except:
            runAge = Null(runCount)
            Er_log('馬齢')
        ##############################
        # 毛色と性別
        ##############################
        try:
            runPedigree = getRunInfo('*[data-test-selector="RC-pedigree__color-sex"]')
            runColor = []
            runSex = []
            for i in range(len(runPedigree)):
                runColor.append(runPedigree[i].split(' ')[0])
                runSex.append(runPedigree[i].split(' ')[-1])
        except:
            runColor = Null(runCount)
            runSex = Null(runCount)
            Er_log('毛色 / 性別')
        ##############################
        # 父名
        ##############################
        try:
            runSire = getRunInfo('*[data-test-selector="RC-pedigree__sire"]')
            runSire = [x.replace(') right',')') for x in runSire]
        except:
            runSire = Null(runCount)
            Er_log('父名')
        ##############################
        # 母名
        ##############################
        try:
            runDam = getRunInfo('*[data-test-selector="RC-pedigree__dam"]')
            runDam = [x.replace(') right',')') for x in runDam]
        except:
            runDam = Null(runCount)
            Er_log('母名')
        ##############################
        # 母の父
        ##############################
        try:
            runBms = getRunInfo('*[data-test-selector="RC-pedigree__damsire"]')
            runBms = [x.replace(') right',')') for x in runBms]
            for i in range(len(runBms)):
                if re.match(r'^\(', runBms[i]):
                    runBms[i] = runBms[i].split('(',1)[1].replace('))',')').strip()
                else:
                    runBms[i] = runBms[i].replace('))',')').strip()
        except:
            runBms = Null(runCount)
            Er_log('母の父')
        ##############################
        # 成形
        ##############################
        try:
            for i in range(runCount):
                record01 = [courseTime,courseName,courseDate,courseDist,raceTitle,raceCase,courseSurface,raceClass,rpAges,courseType]
                record02 = [runNum[i],runName[i],runAge[i],runColor[i],runSex[i],runSire[i],runDam[i],runBms[i]]
                recordFix = record01 + record02
                writer.writerow(recordFix)
                print(recordFix)
            xi = '>> ' + courseDate + ' ' + courseName + ' ' + courseTime + ' exported'
            print(xi)
        except:
            Er_log('CSV生成')

driver.quit()
##終了時刻をエポック秒で取得（処理時間の計算用）
e_time = time.time()
p_time = e_time - s_time
##処理時間の表示
print('処理時間（秒）: ' + str(p_time))
sys.exit()