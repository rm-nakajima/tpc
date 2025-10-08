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
# target.txt
##############################
targets = readFile('targets.txt')
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
##############################
# クローリング開始
##############################
for ii in range(len(targets)):

    driver.get(targets[ii])
    c_url = driver.current_url
    print(c_url)

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

    def getText(y):
        try:
            x = driver.find_element_by_class_name(y).text.strip()
        except:
            x = ''
        return x
    ##############################
    # head
    ##############################
    # 馬名
    p_horseName = getText('hp-nameRow__name')
    if ' ' in p_horseName:
        fN = p_horseName.replace(' ','_')
    else:
        fN = p_horseName
    ##############################
    # 生産国
    p_horseCountry = getText('hp-nameRow__code')
    ##############################
    # 馬齢
    p_age = getText('pp-definition__term').strip(":")
    ##############################
    # 生年月日
    try:
        p_birth = driver.find_element_by_class_name('pp-definition__description').text
        p_pedigree = p_birth.split(" ")
        p_pedigree = [x.replace("(","").replace(")","") for x in p_pedigree]
        p_Birthday = str(p_pedigree[0])
        p_Birthday = datetime.datetime.strptime(p_Birthday, '%d%b%y')
        p_pedigree[0] = str(p_Birthday).split(" ")
        p_pedigree = [str(p_pedigree[0][0]),str(p_pedigree[1]),str(p_pedigree[2])]
        p_pedigree[0] = str(p_pedigree[0]).replace("-","/")
    except:
        p_birth = ''
        p_pedigree = ['','','']
    ####################
    # 取得照合（関数）
    hd_info = driver.find_elements_by_css_selector('div.pp-definition')
    def getHdInfo(a):
        for i in range(len(hd_info)):
            hd_title = hd_info[i].find_element_by_css_selector('.pp-definition__term').text
            if hd_title == a:
                b = hd_info[i].find_element_by_css_selector('a').get_attribute('innerHTML')
                b = b.split('-->',1)[1].split('<!--',1)[0]
            else:
                pass
        b = b.replace('&amp;','&')
        return b

    def getHdInfo02(a):
        for i in range(len(hd_info)):
            hd_title = hd_info[i].find_element_by_css_selector('.pp-definition__term').text
            if hd_title == a:
                b = hd_info[i].find_element_by_css_selector('.hp-horseDefinition__country').text.strip()
            else:
                pass
        b = b.replace('&amp;','&')
        return b

    def getHdInfo03(a):
        for i in range(len(hd_info)):
            hd_title = hd_info[i].find_element_by_css_selector('.pp-definition__term').text
            if hd_title == a:
                b = hd_info[i].find_element_by_css_selector('.pp-definition__description').text.strip()
            else:
                pass
        b = b.replace('&amp;','&')
        return b
    ####################
    # 調教師
    try:
        p_trainer = getHdInfo('Trainer:')
    except:
        p_trainer = ''
    ####################
    # オーナー
    try:
        p_owner = getHdInfo('Owner:')
    except:
        p_owner = ''
    ####################
    # 過去オーナー
    try:
        p_owner_p = driver.find_element_by_class_name('hp-details__owners-list').text
        p_owner_p = p_owner_p.reolace('&amp;','&').strip()
    except:
        p_owner_p = ''
    ####################
    # 父名
    try:
        p_sireName = getHdInfo('Sire:')
    except:
        p_sireName = ''
    try:
        p_sireCountry = getHdInfo02('Sire:')
    except:
        p_sireCountry = ''
    p_sire = p_sireName + p_sireCountry
    ####################
    # 母名
    try:
        p_damName = getHdInfo('Dam:')
    except:
        p_damName = ''
    try:
        p_damCountry = getHdInfo02('Dam:')
    except:
        p_damCountry = ''
    p_dam = p_damName + p_damCountry
    ####################
    # 母父名
    try:
        p_bmsName = getHdInfo('Dam\'s Sire:')
    except:
        p_bmsName = ''
    try:
        p_bmsCountry = getHdInfo02('Dam\'s Sire:')
    except:
        p_bmsCountry = ''
    p_bms = p_bmsName + p_bmsCountry
    ####################
    # 生産者
    try:
        p_breeder = getHdInfo03('Breeder:')
    except:
        p_breeder = ''
    ####################
    # スタンディング
    try:
        p_standing = getHdInfo03('Standing:')
    except:
        p_standing = ''
    ##############################
    # Form > LIFETIME RECORD
    ##############################
    recordValue = [[],[],[],[],[],[],[]]
    # テーブルの列要素を取得してリストを作成
    lifetimeRecord = 'table.hp-raceRecords tbody tr'
    lifetimeRecord = driver.find_elements_by_css_selector(lifetimeRecord)
    #テーブルの列数の分だけ繰り返し処理
    for i in range(len(lifetimeRecord)):
        record_td = lifetimeRecord[i].find_elements_by_css_selector('td')
        record_td = [x.text for x in record_td]
        if record_td[0] == '':
            #recordValue[0] = record_td
            re_record_td = lifetimeRecord[i].find_element_by_css_selector('td button').get_attribute('value')
            if re_record_td == 'Rules Races':
                recordValue[0] = record_td
                del recordValue[0][0]
                del recordValue[0][5]
                del recordValue[0][-1]
            if re_record_td == 'All-weather':
                recordValue[2] = record_td
                del recordValue[2][0]
                del recordValue[2][5]
                del recordValue[2][-1]
        if record_td[0] == 'Flat Turf':
            recordValue[1] = record_td
            del recordValue[1][0]
            del recordValue[1][5]
            del recordValue[1][-1]
        if record_td[0] == 'All-weather':
            recordValue[2] = record_td
            del recordValue[2][0]
            del recordValue[2][5]
            del recordValue[2][-1]
        if record_td[0] == 'Chase':
            recordValue[3] = record_td
            del recordValue[3][0]
            del recordValue[3][5]
            del recordValue[3][-1]
        if record_td[0] == 'Hurdle':
            recordValue[4] = record_td
            del recordValue[4][0]
            del recordValue[4][5]
            del recordValue[4][-1]
        if record_td[0] == 'NHF':
            recordValue[5] = record_td
            del recordValue[5][0]
            del recordValue[5][5]
            del recordValue[5][-1]
        if record_td[0] == 'PTP':
            recordValue[6] = record_td
            del recordValue[6][0]
            del recordValue[6][5]
            del recordValue[6][-1]
    if len(recordValue[0]) < 1:
        recordValue[0] = ['','','','','','','','','']
    else:
        pass
    ##############################
    # Form > Form
    ##############################
    # DATE
    __date = 'table.hp-formTable tbody.ui-table__body tr.ui-table__row td:nth-child(1) .hp-formTable__dateWrapper'
    __date = driver.find_elements_by_css_selector(__date)
    for i in range(len(__date)):
        __date[i] = __date[i].text
    __date = [x.replace("hollow video icon","").strip() for x in __date]
    for i in range(len(__date)):
        __date[i] = datetime.datetime.strptime(__date[i], '%d%b%y')
        __date[i] = str(__date[i]).split(" ")
        __date[i] = str(__date[i][0])
    ##############################
    # URL
    __url = 'table.hp-formTable tbody.ui-table__body tr.ui-table__row td:nth-child(1) a'
    __url = driver.find_elements_by_css_selector(__url)
    for i in range(len(__url)):
        if re.search("videoIcon", __url[i].get_attribute('class')):
            __url[i] = ""
        else:
            __url[i] = __url[i].get_attribute('href')
    __url = [x for x in __url if x != ""]
    ##############################
    # レース名
    __raceName = 'table.hp-formTable tbody.ui-table__body tr.ui-table__row td:nth-child(1) a'
    __raceName = driver.find_elements_by_css_selector(__raceName)
    for i in range(len(__raceName)):
        if re.search("videoIcon", __raceName[i].get_attribute('class')):
            __raceName[i] = ""
        else:
            __raceName[i] = __raceName[i].get_attribute('title')
    __raceName = [x for x in __raceName if x != ""]
    ##############################
    # CCTP
    __cctp = 'table.hp-formTable tbody.ui-table__body tr.ui-table__row td:nth-child(2)'
    __cctp = driver.find_elements_by_css_selector(__cctp)
    for i in range(len(__cctp)):
        __cctp[i] = __cctp[i].text
    ##############################
    # Course_C
    __courseC = 'table.hp-formTable tbody.ui-table__body tr.ui-table__row td:nth-child(2) span a'
    __courseC = driver.find_elements_by_css_selector(__courseC)
    for i in range(len(__courseC)):
        __courseC[i] = __courseC[i].get_attribute('title')
    ##############################
    # DIST.
    __dist = 'table.hp-formTable tbody.ui-table__body tr.ui-table__row td:nth-child(3)'
    __dist = driver.find_elements_by_css_selector(__dist)
    for i in range(len(__dist)):
        __dist[i] = __dist[i].text
    ##############################
    # GNG.
    __gng = 'table.hp-formTable tbody.ui-table__body tr.ui-table__row td:nth-child(4)'
    __gng = driver.find_elements_by_css_selector(__gng)
    for i in range(len(__gng)):
        __gng[i] = __gng[i].text
    ##############################
    # WGT
    __wgt = 'table.hp-formTable tbody.ui-table__body tr.ui-table__row td:nth-child(5)'
    __wgt = driver.find_elements_by_css_selector(__wgt)
    for i in range(len(__wgt)):
        __wgt[i] = __wgt[i].text
    ##############################
    # POS.
    __pos = 'table.hp-formTable tbody.ui-table__body tr.ui-table__row td:nth-child(6)'
    __pos = driver.find_elements_by_css_selector(__pos)
    for i in range(len(__pos)):
        __pos[i] = __pos[i].text
    ##############################
    # SP
    __sp = 'table.hp-formTable tbody.ui-table__body tr.ui-table__row td:nth-child(7)'
    __sp = driver.find_elements_by_css_selector(__sp)
    for i in range(len(__sp)):
        __sp[i] = __sp[i].text
    ##############################
    # JOCKEY
    __jockey = 'table.hp-formTable tbody.ui-table__body tr.ui-table__row td:nth-child(8)'
    __jockey = driver.find_elements_by_css_selector(__jockey)
    for i in range(len(__jockey)):
        try:
            __jockey[i] = __jockey[i].find_element_by_css_selector('a').text
        except:
             __jockey[i] = ''
    ##############################
    # OR
    __or = 'table.hp-formTable tbody.ui-table__body tr.ui-table__row td:nth-child(9)'
    __or = driver.find_elements_by_css_selector(__or)
    for i in range(len(__or)):
        __or[i] = __or[i].text

    # TS
    __ts = 'table.hp-formTable tbody.ui-table__body tr.ui-table__row td:nth-child(10)'
    __ts = driver.find_elements_by_css_selector(__ts)
    for i in range(len(__ts)):
        __ts[i] = __ts[i].text

    # RPR
    __rpr = 'table.hp-formTable tbody.ui-table__body tr.ui-table__row td:nth-child(11)'
    __rpr = driver.find_elements_by_css_selector(__rpr)
    for i in range(len(__rpr)):
        __rpr[i] = __rpr[i].text

    # 出力日
    dateNow = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")

    # 取得したFormデータを日付別に二次元配列に格納
    record03 = []
    for z in range(len(__date)):
        record03.append([])
    for z in range(len(__date)):
        Summary = [__date[z],__url[z],__raceName[z],__cctp[z],__courseC[z],__dist[z],__gng[z],__wgt[z],__pos[z],__sp[z],__jockey[z],__or[z],__ts[z],__rpr[z]]
        record03[z].append(Summary)

    ############################
    # CSV生成
    ############################
    FileName = savePath + 'racingpost02_' + fN + ".csv"
    Err_FileName = savePath + 'Err_racingpost02_' + fN + ".txt"
    f = open(FileName, 'w', encoding="utf_8_sig")
    writer = csv.writer(f, lineterminator='\n')

    # エラー時のログ生成
    def Er_log(a):
        fErr = open(Err_FileName, 'a', encoding="utf_8_sig")
        fErr.write('エラー発生URL: ' + str(driver.current_url))
        fErr.write('\n' + a + ' 取得エラー\n')

    # ラベルの生成
    label01 = ["ID","Horse_name","b","age","c_s","birthday","color","sex","Trainer","Owner","Owner_p","Sire","Dam","Damsire","Breeder","Standing",'Races_Count']
    label02 = ["LIFETIME RECORD","RUNS","WINS","2NDS","3RDS","WINNINGS","EARNINGS","OR","BEST TS","BEST RPR","URL","scrape_date"]
    label03 = ["21","Date","Date_L","Race","CCTP","Course_C","dis","going","wgt","pos","sp","Jockey","OR","TS","RPR","","","","","","","","","","","","","","","","","","","","","","","","レースコメント"]

    # レコードの成形
    record01 = [p_horseName,p_horseCountry,p_age,p_birth,p_pedigree[0],p_pedigree[1],p_pedigree[2],p_trainer,p_owner,p_owner_p,p_sire,p_dam,p_bms,p_breeder,p_standing]
    record02 = recordValue[0]
    record02.append(c_url)
    record02.append(dateNow)
    record02_sub = []
    for i in range(16):
        # CSV3〜8行・2〜17列目までに空欄を設ける
        record02_sub.append('')

    # ラベルの出力（1行目）
    writer.writerow(label01 + label02)
    # レコードの出力（2行目）
    writer.writerow(['11'] + record01 + [str(len(__url))] + ['Rules Races'] + record02)
    # レコードの出力（3〜8行目）
    writer.writerow(['12'] + record02_sub + ['Flat Turf'] + recordValue[1])
    writer.writerow(['13'] + record02_sub + ['All-weather'] + recordValue[2])
    writer.writerow(['14'] + record02_sub + ['Chase'] + recordValue[3])
    writer.writerow(['15'] + record02_sub + ['Hurdle'] + recordValue[4])
    writer.writerow(['16'] + record02_sub + ['NHF'] + recordValue[5])
    writer.writerow(['17'] + record02_sub + ['PTP'] + recordValue[6])
    # レコードの出力（9行目）
    writer.writerow(['18'])

    # ラベルの出力（10行目）
    writer.writerow(label03)

    # 各レース詳細用のラベル生成
    full_label = ["競馬場コード","競馬場","国名","レース日付","レース名","レース格","レース他","レース名省略","出走条件（性別）","馬場の種類",\
        "馬場の種類（英愛）","出走条件（クラス）","出走条件（他）","出走条件（年齢）","距離","コース形態","コース詳細","馬場状態","障害数","障害レース確認",\
            "着賞金","並び順位","確定順位","異常区分","同着","着変更","ゲート番号","着差1","着差2","馬名",\
                "生産国","オッズ","馬齢","斤量","斤量特記1","斤量特記2","補助馬具","調教師","騎手","毛色",\
                    "性別","父名","母名","母父名","出走頭数","優勝馬タイム","優勝馬オーナー","優勝馬生産者","コメント"]

    # 各レース詳細の情報取得
    for s in range(len(__url)):

        driver.get(__url[s])

        # Comments
        try:
            __comments = driver.find_element_by_css_selector('.rp-raceInfo__comments').text.strip()
        except:
            __comments = ''
        raceComment = ['','','','','','','','','','','','','','','','','','','','','','','',__comments]

        # レコードの出力（11行目）
        writer.writerow(['22'] + record03[s][0] + raceComment)
        # ラベルの出力（12行目）
        writer.writerow(['31'] + full_label)

        ##############################
        # pedigreeをアクティベート
        ##############################
        pgFlg = driver.find_elements_by_css_selector('.rp-horseTable__pedigreesBtn.ui-btn_toggleActive')
        if len(pgFlg) > 0:
            pass
        else:
            driver.find_element_by_css_selector('.rp-horseTable__pedigreesBtn').click()
            time.sleep(1)
        ##############################
        # 出走頭数
        ##############################
        try:
            value = driver.find_elements_by_css_selector('.rp-horseTable__mainRow')
            value = len(value)
        except:
            value = 0
        try:
            sValue = driver.find_element_by_css_selector('.rp-raceInfo__value_black').text.strip()
            sValue = sValue.split(' ')[0]
            sValue = int(sValue)
        except:
            sValue = 0
        ##############################
        # 競馬場コード
        ##############################
        try:
            rc_code = __url[s].split('/results/')[1].split('/')[0].strip()
        except:
            rc_code = ''
        ##############################
        # 競馬場
        ##############################
        try:
            Course = driver.find_element_by_css_selector('.rp-raceTimeCourseName__name').text.strip()
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
            Date = driver.find_element_by_css_selector('.rp-raceTimeCourseName__date').text.strip()
            Date = datetime.datetime.strptime(Date, '%d %b %Y').strftime('%Y/%m/%d')
        except:
            Date = ''
        ##############################
        # レース名
        ##############################
        try:
            raceName = driver.find_element_by_css_selector('.rp-raceTimeCourseName__title').text.strip()
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
            raceClass = driver.find_element_by_css_selector('.rp-raceTimeCourseName_class')\
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
            raceRating = driver.find_element_by_css_selector('.rp-raceTimeCourseName_ratingBandAndAgesAllowed')\
                .text.replace('(','').replace(')','').strip()
        except:
            raceRating = ''
        ##############################
        # 距離
        ##############################
        try:
            Distance = driver.find_element_by_css_selector('.rp-raceTimeCourseName_distanceFull')\
                .text.replace('(','').replace(')','').strip()
        except:
            try:
                Distance = driver.find_element_by_css_selector('.rp-raceTimeCourseName_distance')\
                    .text.replace('(','').replace(')','').strip()
            except:
                Distance = ''
        ##############################
        # コース詳細
        ##############################
        try:
            courseForm = driver.find_element_by_css_selector('.rp-raceTimeCourseName_distanceDetail')\
                .text.strip()
        except:
            courseForm = ''
        ##############################
        # 馬場状態
        ##############################
        try:
            Condition = driver.find_element_by_css_selector('.rp-raceTimeCourseName_condition')\
                .text.strip()
        except:
            Condition = ''
        ##############################
        # 障害数
        ##############################
        try:
            hurdles = driver.find_element_by_css_selector('.rp-raceTimeCourseName_hurdles')\
                .text.strip()
        except:
            hurdles = ''
        ##############################
        # 賞金額（辞書型に一時格納）
        ##############################
        try:
            pDict = {}
            xi = driver.find_element_by_xpath('//div[@data-test-selector="text-prizeMoney"]').text
            xii = driver.find_elements_by_css_selector('.rp-raceTimeCourseName__prizeMoneyTitle')
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
            xi = driver.find_elements_by_css_selector('.rp-horseTable__pos__number')
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
            gate = driver.find_elements_by_css_selector('.rp-horseTable__pos__number')
            gate = [x.text.split('(')[1].replace(')','').strip() for x in gate]
        except:
            gate = Null(value)
        ##############################
        # 着差
        ##############################
        try:
            margin01 = []
            margin02 = []
            xi = driver.find_elements_by_css_selector('.rp-horseTable__pos__length')
            for i in xi:
                xii = i.find_elements_by_css_selector('span')
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
            horseName = driver.find_elements_by_css_selector('.rp-horseTable__horse__name')
            horseName = [x.get_attribute('innerHTML').split('<svg')[0].strip() for x in horseName]
        except:
            horseName = Null(value)
        ##############################
        # 生産国
        ##############################
        try:
            horseCountry = driver.find_elements_by_css_selector('.rp-horseTable__horse__country')
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
            odds = driver.find_elements_by_css_selector('.rp-horseTable__horse__price')
            odds = [x.text.strip() for x in odds]
        except:
            odds = Null(value)
        ##############################
        # 馬齢
        ##############################
        try:
            age = driver.find_elements_by_css_selector('.rp-horseTable__spanNarrow_age')
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
            xi = driver.find_elements_by_css_selector('td.rp-horseTable__wgt')
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
                    if len(xii.find_elements_by_css_selector('img')) > 0:
                        xiii = xii.find_element_by_css_selector('.rp-horseTable__extraData img').get_attribute('alt')
                    else:
                        xiii = ''
                    x = xiii + ' ' + xii.text.strip()
                    exData.append(x.strip())
                except:
                    exData.append('')
                # 斤量特記2
                try:
                    if len(i.find_elements_by_css_selector('.rp-horseTable__windOperations')) > 0:
                        x = i.find_element_by_css_selector('.rp-horseTable__windOperations').text.strip()
                    else:
                        x = ''
                    windOpe.append(x)
                except:
                    windOpe.append('')
                # 補助馬具
                try:
                    if len(i.find_elements_by_css_selector('.rp-horseTable__headGear')) > 0:
                        x = i.find_element_by_css_selector('.rp-horseTable__headGear').text.strip()
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
            trainer = driver.find_elements_by_css_selector('td.rp-horseTable__humanCell a[data-test-selector="link-trainerName"]')
            trainer = [x.text.strip() for x in trainer]
        except:
            trainer = Null(value)
        ##############################
        # 騎手
        ##############################
        try:
            jockey = driver.find_elements_by_css_selector('td.rp-horseTable__humanCell a[data-test-selector="link-jockeyName"]')
            jockey = [x.text.strip() for x in jockey]
        except:
            jockey = Null(value)
        ##############################
        # 毛色と性別
        ##############################
        try:
            coatColor = []
            gender = []
            pedigree = driver.find_elements_by_css_selector('.rp-horseTable__pedigreeRow td')
            pedigree = [x.text.strip().split(' ') for x in pedigree]
            for i in pedigree:
                coatColor.append(i[0])
                gender.append(i[1])
        except:
            coatColor = Null(value)
            gender = Null(value)
        ##############################
        # 父名
        ##############################
        try:
            sire = driver.find_elements_by_css_selector('.rp-horseTable__pedigreeRow a:nth-of-type(1)')
            sire = [x.get_attribute('innerHTML').split('<svg')[0]\
                .strip().replace('               ','').strip() for x in sire]
        except:
            sire = Null(value)
        ##############################
        # 母名
        ##############################
        try:
            mare = driver.find_elements_by_css_selector('.rp-horseTable__pedigreeRow a:nth-of-type(2)')
            mare = [x.get_attribute('innerHTML').split('<svg')[0]\
                .strip().replace('               <span>','').replace('</span>','').strip() for x in mare]
        except:
            mare = Null(value)
        ##############################
        # 母父名
        ##############################
        try:
            bms = []
            bmsDisc = driver.find_elements_by_css_selector('.rp-horseTable__pedigreeRow')
            for i in bmsDisc:
                bmsFlg = i.find_elements_by_css_selector('a:nth-child(3)')
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
        rp_info = driver.find_element_by_css_selector('.rp-raceInfo')
        rp_info_cmp = rp_info.find_elements_by_css_selector('.rp-raceInfo__value')
        rp_info_cmp = [x.text.strip() for x in rp_info_cmp]
        rp_info_cmp_a = rp_info.find_elements_by_css_selector('.ui-profileLink')
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
            xi = rp_info.find_elements_by_css_selector('li')
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
            comment = driver.find_elements_by_css_selector('.rp-horseTable__commentRow')
            comment = [x.text.strip() for x in comment]
        except:
            comment = Null(value)

        for i in range(value):
            try:
                record01 = [rc_code,Course,countryCode,Date,raceName,raceCase,raceOther,raceNameAbbr,raceType,courseType,\
                    rcType,raceClass,raceTerms,raceRating,Distance,courseShape,courseForm,Condition,hurdles,hurdleCheck]
                record02 = [prize[i],num[i],numFix[i],numCode[i],arrival[i],numChange[i],gate[i],margin01[i],margin02[i],horseName[i],horseCountry[i],\
                    odds[i],age[i],weight[i],exData[i],windOpe[i],headGear[i],trainer[i],jockey[i],\
                        coatColor[i],gender[i],sire[i],mare[i],bms[i],sValue,valueTime[i],owner[i],breeder[i],comment[i]]
                recordFix = ['32'] + record01 + record02
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