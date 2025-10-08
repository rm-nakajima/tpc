# -*- coding: utf-8 -*-
from gettext import find
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time
from datetime import date, timedelta, datetime
import datetime
import chromedriver_binary
import re
import csv
import random
import copy
import os
import pyperclip
import sys

##開始時刻をエポック秒で取得（処理時間の計算用）
s_time = time.time()
# ==================================================
# 今日の日付（ファイル名に使用）
# ==================================================
dateToday = datetime.datetime.now().strftime("%Y%m%d")
strToday = datetime.datetime.now().strftime("%Y/%m/%d")
# ==================================================
# function
# ==================================================
# エラーログ
def er_msg(e):
    fErr = open(ErFileName, 'a', encoding="utf_8_sig")
    #fErr.write('>> ' + str(driver.current_url))
    fErr.write(str(dd + 1) + ' / ' + str(len(tarNum)))
    fErr.write('\n' + e + '\n')
    print(e)
# ==============================
# ローディング判定
# ==============================
def loadFlg():
    try:
        a = 0
        b = driver.find_elements_by_css_selector('img.img-responsive')
        b = [x.get_attribute('src') for x in b]
        for i in range(len(b)):
            if 'loading.gif' in b[i]:
                a = a + 1
            else:
                pass
    except:
        a = 0
    # ローディング完了まで繰り返し処理（5秒待機×最大120回）
    try:
        loopCount = 1
        while(a > 0):
            print('>> loading..')
            time.sleep(5)
            loopCount = loopCount + 1
            a = loadFlg()
            if loopCount > 120:
                break
            else:
                pass
    except:
        pass
# ==============================
# コメント
# ==============================
def consoleLog(text,value):
    print('# ------------------------------------')
    print('# ' + str(text))
    print('# ------------------------------------')
    print(str(value))
# ==============================
# テーブル内文字取得
# ==============================
def getTableText(arr,target):
    for i in range(len(r_num)):
        e = h_table[i].find_elements_by_css_selector(target)
        e = [x.text.strip() for x in e]
        arr.append(e)
# ==============================
# 月表記の数字置換
# ==============================
def repMonth(a):
    if 'enero' in a.lower():
        a = '01'
    elif 'febrero' in a.lower():
        a = '02'
    elif 'marzo' in a.lower():
        a = '03'
    elif 'abril' in a.lower():
        a = '04'
    elif 'mayo' in a.lower():
        a = '05'
    elif 'junio' in a.lower():
        a = '06'
    elif 'julio' in a.lower():
        a = '07'
    elif 'agosto' in a.lower():
        a = '08'
    elif 'septiembre' in a.lower():
        a = '09'
    elif 'octubre' in a.lower():
        a = '10'
    elif 'noviembre' in a.lower():
        a = '11'
    elif 'diciembre' in a.lower():
        a = '12'
    else:
        a = 'ERROR'

    return a
# ==================================================
# 各種設定ファイル
# ==================================================
#login.txt
# ==============================
try:
    f = open('setting/login.txt', 'r', encoding='UTF-8')
    loginInfo = f.read().split('\n')
    loginId = loginInfo[0].split('-->')[1].strip()
    loginPw = loginInfo[1].split('-->')[1].strip()
    print('ID: ' + loginId)
except:
    print('Login.txt ERROR')
    sys.exit()
# save.txt
try:
    f = open('setting/save.txt', 'r', encoding='UTF-8')
    savePath = f.read().strip()
    savePath = savePath.split('\n')[0]
    savePath = savePath + '/'
    savePath = savePath.replace('//','/')
except:
    savePath = ''
print('>> Save Path: ' + str(savePath))
# ==============================
# setting files
# ==============================
rPath = 'setting/'
def readFile(a):
    try:
        f = open(rPath + a, 'r', encoding='UTF-8')
        b = f.read()
        if '\n' in b:
            b = b.split('\n')
        else:
            b = [b]
    except:
        sys.exit()
    b = [x for x in b if x != '']
    return b
# ==============================
# 競馬場コード
# ==============================
try:
    c_fPath = rPath + 'sa_country.csv'
    c_list = []
    with open(c_fPath, encoding='utf_8_sig') as f:
        reader = csv.reader(f)
        for r in reader:
            c_list.append(r)
except:
    print('>> sa_country.csv: ERROR')
    sys.exit()
# ==============================
# レース格_設定
# ==============================
s_rGrade = readFile('sa_race-case.txt')
# ==============================
# 出走条件（性別）_設定
# ==============================
s_rName = readFile('sa_race-name.txt')
# ==============================
# 出走条件（その他）_設定
# ==============================
s_rOthers = readFile('sa_race-case-other.txt')
# ==============================
# 対象日
# ==============================
tarDate = readFile('targets.txt')
# ==================================================
# ChromeDriver
# ==================================================
options = Options()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.use_chromium = True
cwd = os.getcwd()
#options.binary_location = '/Applications/Google Chrome Beta.app/Contents/MacOS/Google Chrome Beta'
#driver = webdriver.Chrome(options=options)
driver = webdriver.Chrome(options=options)
driver.set_window_size(1300,768)
tar = []
base = 'https://elturf.com/carreras-proximos-programas?fechaSel='
for i in range(len(tarDate)):
    tar.append(base + tarDate[i])
print(tar)
# ==================================================
# ログイン
# ==================================================
driver.get('https://elturf.com/login')
driver.implicitly_wait(10)
try:
    x = driver.find_elements_by_css_selector('#form_contacto_login_general')
    if(len(x) > 0):
        # 入力処理/ログインクリック
        driver.find_element_by_css_selector('#form_contacto_usuario').send_keys(loginId)
        driver.find_element_by_css_selector('#form_contacto_passwd2').send_keys(loginPw)
        time.sleep(1)
        driver.find_element_by_css_selector('#Elturf_Send_Form_Login2').click()
        time.sleep(1)
except:
    print('ログインERROR')
    sys.exit()
# ==================================================
# 対象日に遷移
# ==================================================
for d in range(len(tar)):
    driver.get(tar[d])
    driver.implicitly_wait(20)
    # ==================================================
    # CSV生成
    # ==================================================
    FileName = savePath + 'elturf03_' + tarDate[d] + ".csv"
    ErFileName = savePath + 'Err_elturf03_' + tarDate[d] + ".txt"
    f = open(FileName, 'w', encoding="utf_8_sig")
    writer = csv.writer(f, lineterminator='\n')
    label = ["競馬場コード","競馬場","国","開催日","レースNo","発走時刻","レース名","レース格","レースType","レース他",\
            "レース名省略","距離","出走条件","馬場の種類","出走条件（性別）","出走条件（その他）","総賞金","賞金","馬番号","枠番号","Horse",\
            "生産国","性/毛色/年齢","馬齢","毛色","性別","父名","父生産国","母名","母生産国","母父名","母父生産国"]
    writer.writerow(label)
    # ==============================
    # 競馬場
    # ==============================
    loadFlg()
    tarDict = {}
    tarNum = []
    tarRc = driver.find_elements_by_css_selector('.tituloshome')
    tarRc = [x.text.strip().split(',')[0].split('N°')[1].split(' ',1)[1] for x in tarRc]
    for i in range(len(tarRc)):
        tarDict[i] = tarRc[i]
    for i in range(len(tarDict)):
        for ii in c_list:
            # リスト照合 アメリカ / カナダ / プエルトリコを除外
            if tarDict[i] in ii[3]:
                if ii[0] == 'Estados Unidos' or ii[0] == 'Unidos' or ii[0] == 'Canada' or ii[0] == 'Puerto Rico':
                    tarDict[i] = ''
    for i in range(len(tarDict)):
        if len(tarDict[i]) > 0:
            tarNum.append(i)
    # ==============================
    # Ver Todos取得
    # ==============================
    for dd in range(len(tarNum)):
        btnObj = driver.find_elements_by_css_selector('.table-condensed')[1::]
        rcTotal = btnObj[dd].find_element_by_css_selector('tbody:last-child tr:last-child').text.split(':')[1].strip()
        rcTotal = int(rcTotal)
        consoleLog('進捗',str(dd + 1) + '/' + str(len(tarNum)) + '(' + str(rcTotal) + ')')
        btnObj[tarNum[dd]].find_element_by_css_selector('thead tr:nth-of-type(1) th div:nth-of-type(4) div:nth-of-type(1) button').click()
        time.sleep(1)
        btnObj[tarNum[dd]].find_element_by_css_selector('thead tr:nth-of-type(1) th div:nth-of-type(4) div:nth-of-type(1) ul li a').click()
        loadFlg()
        driver.execute_script('window.scrollTo(0,0)')
        rcCount = driver.find_elements_by_xpath('//*[@id="app-elt"]/div[8]/div/div[3]/div/div/a')
        rcLinks = []
        for i in rcCount:
            obj = i.get_attribute('href').split('_')[-1]
            rcLinks.append(obj)
        rcCount = len(rcCount) - 1
        # ==============================
        # レースNo.
        # ==============================
        try:
            r_num = driver.find_elements_by_css_selector('table h1')
            if len(r_num) < rcTotal:
                print('>> try again...')
                loadFlg()
                r_num = driver.find_elements_by_css_selector('table h1')
            r_num = [x.text.strip() for x in r_num]
            r_num = [x for x in r_num if x != '']
        except:
            r_num = ''
            er_msg('レースNo: ERROR')
        consoleLog('レースNo',r_num)
        # ==============================
        # 競馬場 / 競馬場コード / 開催日
        # ==============================
        hdText = driver.find_element_by_css_selector('.hidden-xs.col-sm-6.col-md-6.col-lg-6.text-left')
        # 競馬場
        try:
            rc_name = hdText.find_element_by_css_selector('strong').text.strip()
        except:
            rc_name = ''
            er_msg('競馬場取得: ERROR')
        consoleLog('競馬場名',rc_name)
        # 競馬場コード
        rc_code = ''
        try:
            for i in range(len(c_list)):
                if c_list[i][3] == rc_name:
                    rc_code = c_list[i][2]
        except:
            er_msg('競馬場コード取得: ERROR')
        consoleLog('競馬場コード',rc_code)
        # 開催日
        try:
            rc_date = hdText.text.strip().split(' | ')[1].strip()
            rc_date_D = rc_date.split(' de ')[0].split(' ')[1].strip()
            rc_date_Y = rc_date.split(' del ')[1].strip()
            rc_date_M = rc_date.split(' de ')[1].split(' del ')[0].strip()
            rc_date_M = repMonth(rc_date)
            rc_date_M = '/' + rc_date_M + '/'
            rc_date = rc_date_Y + rc_date_M + rc_date_D
        except:
            rc_date = ''
            er_msg('開催日時取得: ERROR')
        consoleLog('開催日',rc_date)
        # ==============================
        # 国名
        # ==============================
        try:
            rc_country = hdText.text.strip()
            rc_country = rc_country.split(rc_name)[1].split(' | ')[0].strip()
        except:
            rc_country = ''
            er_msg('国名取得: ERROR')
        consoleLog('国名',rc_country)
        # ==============================
        # 発走時刻
        # ==============================
        try:
            r_td = driver.find_elements_by_xpath('//*[@id="app-elt"]/div[8]/div/div/div/table/tbody/tr[1]/td[3]/strong')
            r_td = [x.text.split(' ')[0].strip() for x in r_td]
        except:
            r_td = []
            for i in range(len(r_num)):
                r_td .append('')
            er_msg('発走時刻取得: ERROR')
        consoleLog('発走時刻',r_td)
        # ==============================
        # レース名
        # ==============================
        try:
            r_name = driver.find_elements_by_xpath('//*[@id="app-elt"]/div[8]/div/div/div/table/tbody/tr[1]/td[4]/strong')
            r_name = [x.text.replace('"','').strip() for x in r_name]
        except:
            r_name = []
            for i in range(len(r_num)):
                r_name.append('')
            er_msg('レース名取得: ERROR')
        consoleLog('レース名',r_name)
        # ==============================
        # レース格
        # ==============================
        try:
            obj = driver.find_elements_by_xpath('//*[@id="app-elt"]/div[8]/div/div/div/table/tbody/tr[2]/td[1]')
            r_class = []
            for i in range(len(r_num)):
                arr = []
                for ii in s_rGrade:
                    if ii in obj[i].text:
                        arr.append(ii.replace('(','').replace(')','').strip())
                    else:
                        arr.append('')
                arr = [x for x in arr if x != '']
                if len(arr) == 0:
                    arr = ['']
                r_class.append(arr)
        except:
            for i in range(len(r_num)):
                r_class.append('')
            er_msg('レース格: ERROR')
        consoleLog('レース格',r_class)
        # ==============================
        # レースType
        # ==============================
        try:
            obj = driver.find_elements_by_xpath('//*[@id="app-elt"]/div[8]/div/div/div/table/tbody/tr[2]/td[1]')
            r_type = [x.text.split('|')[0].split('(')[1].split(')')[0].strip() for x in obj]
        except:
            r_type = []
            for i in range(len(r_num)):
                r_type.append('')
            er_msg('レースType取得: ERROR')
        consoleLog('レースType',r_type)
        # ==============================
        # 出走条件
        # ==============================
        try:
            r_info = driver.find_elements_by_xpath('//*[@id="app-elt"]/div[8]/div/div/div/table/tbody/tr[2]/td[1]')
            r_info = [x.text.split('|')[1].strip() for x in r_info]
        except:
            r_info = []
            for i in range(len(r_num)):
                r_info.append('')
            er_msg('出走条件取得: ERROR')
        consoleLog('出走条件',r_info)
        # ==============================
        # 馬場の種類
        # ==============================
        try:
            rc_type = driver.find_elements_by_xpath('//*[@id="app-elt"]/div[8]/div/div/div/table/tbody/tr[2]/td[2]')
            rc_type = [x.text.strip() for x in rc_type]
            rc_type = [x.split('(')[0].strip() for x in rc_type]
        except:
            rc_type = []
            for i in range(len(r_num)):
                rc_type.append('')
            er_msg('馬場の種類: ERROR')
        consoleLog('馬場の種類',rc_type)
        # ==============================
        # 出走条件（性別）
        # ==============================
        r_gender = []
        for i in range(len(r_num)):
            r_gender.append('')
        for i in range(len(r_num)):
            for ii in s_rName:
                if ii in r_info[i]:
                    r_gender[i] = ii
        consoleLog('出走条件（性別）',r_gender)
        # ==============================
        # 出走条件（その他）
        # ==============================
        r_other = []
        for i in range(len(r_num)):
            r_other.append('')
        for i in range(len(r_num)):
            for ii in s_rOthers:
                if ii in r_info[i]:
                    r_other[i] = ii
        consoleLog('出走条件（その他）',r_other)
        # ==============================
        # 距離
        # ==============================
        try:
            rc_dist = driver.find_elements_by_xpath('//*[@id="app-elt"]/div[8]/div/div/div/table/tbody/tr[1]/td[6]/strong')
            rc_dist = [x.text.strip() for x in rc_dist]
        except:
            rc_dist = []
            for i in range(len(r_num)):
                rc_dist.append('')
            er_msg('距離取得: ERROR')
        # ==============================
        # 総賞金
        # ==============================
        try:
            r_tPrize = driver.find_elements_by_xpath('//*[@id="app-elt"]/div[8]/div/div/div/table/tbody/tr[1]/td[5]/span/strong')
            r_tPrize = [x.text.strip() for x in r_tPrize]
        except:
            r_tPrize
            for i in range(len(r_num)):
                r_tPrize.append('')
            er_msg('総賞金取得: ERROR')
        consoleLog('総賞金',r_tPrize)
        # ==============================
        # 賞金
        # ==============================
        try:
            r_prize = driver.find_elements_by_xpath('//*[@id="app-elt"]/div[8]/div/div/div/table/tbody/tr[3]/td[1]')
            r_prize = [x.text.strip() for x in r_prize]
        except:
            r_prize = []
            for i in range(len(r_num)):
                r_prize.append('')
            er_msg('賞金取得: ERROR')
        consoleLog('賞金',r_prize)

        # ==================================================
        # レース数
        # ==================================================
        try:
            h_table = driver.find_elements_by_css_selector('div.tab_programas.tab-content')
            if len(h_table) < len(r_num):
                print('>> try again...')
                loadFlg()
        except:
            er_msg('レース数: ERROR')
            sys.exit()
        consoleLog('レース数',str(len(r_num)))
        # ==============================
        # タブクリック
        # ==============================
        tabBtn = driver.find_elements_by_css_selector('ul[id^="tab_"]')
        # ==============================
        # 個別テーブル
        # ==============================
        h_value = []
        hObj = []
        for i in range(len(r_num)):
            elem = h_table[i].find_elements_by_css_selector('div[id^="completo_"] > .row')
            h_value.append(len(elem))
            hObj.append(elem)
        try:
            for i in range(len(r_num)):
                tab = tabBtn[i].find_element_by_css_selector('li:nth-of-type(1) a')
                tab.click()
                time.sleep(1)
                elem = h_table[i].find_elements_by_css_selector('div[id^="completo_"] > .row')
                h_value.append(len(elem))
                hObj.append(elem)
        except:
            er_msg('出走馬テーブル: ERROR')
            sys.exit()
        consoleLog('出走頭数',h_value)
        # ==================================================
        # 馬番号 / 枠番号 / 馬名 / 生産国 / 性/毛色/年齢 /
        # 父名 / 父生産国 / 母名 / 母生産国
        # ==================================================
        h_num,h_frame,h_name,h_country = [],[],[],[]
        h_type,h_age,h_color,h_sex = [],[],[],[]
        h_sire,h_sireOri,h_mare,h_mareOri = [],[],[],[]
        h_bms,h_bmsOri = [],[]
        for i in range(len(r_num)):
            arr01 = []
            arr02 = []
            arr03 = []
            arr04 = []
            arr05 = []
            arr06 = []
            arr07 = []
            arr08 = []
            arr09 = []
            arr10 = []
            arr11 = []
            arr12 = []
            arr13 = []
            arr14 = []
            for ii in range(len(hObj[i])):
                # 馬番号 / 枠番号
                elem = ['','']
                try:
                    elem = hObj[i][ii].find_element_by_css_selector('tr:nth-of-type(1) td:nth-of-type(1)')\
                        .text.split('\n')
                    if len(elem) < 2:
                        elem.append('')
                except:
                    er_msg('馬番号/枠番号取得: ERROR')
                arr01.append(elem[0].strip())
                arr02.append(elem[1].strip())
                # 馬名 / 生産国
                try:
                    elem = hObj[i][ii].find_element_by_css_selector('tr:nth-of-type(1) td:nth-of-type(5)')
                    subElem = elem.find_element_by_css_selector('a strong').text.strip()
                except:
                    er_msg('馬名/生産国取得: ERROR')
                    elem = ''
                    subElem = ''
                print(subElem)
                arr03.append(subElem)
                arr04.append(elem.text.split(subElem)[1].split('(')[1].split(')')[0].strip())
                # 性/毛色/年齢
                try:
                    elem = hObj[i][ii].find_element_by_css_selector('tr:nth-of-type(1) td:nth-of-type(5)')\
                            .text.split('\n')[1].split('(')[0].strip().replace('Dk ','Dk')
                except:
                    er_msg('性/毛色/年齢: ERROR')
                    elem = ''
                arr05.append(elem)
                try:
                    arr06.append(elem.split(' ')[1])
                except:
                    er_msg('馬齢: ERROR')
                    arr06.append('')
                try:
                    arr07.append(elem[1::].split(' ')[0].strip())
                except:
                    er_msg('毛色: ERROR')
                    arr07.append('')
                try:
                    arr08.append(elem[0])
                except:
                    er_msg('性別: ERROR')
                    arr08.append('')
                # 父名
                try:
                    elem = hObj[i][ii].find_element_by_css_selector('tr:nth-of-type(2) td:nth-of-type(3) > div:nth-of-type(1)')\
                        .text.strip()
                except:
                    elem = ''
                    er_msg('父名取得: ERROR')
                arr09.append(elem)
                # 父生産国
                elem = ''
                try:
                    elem = hObj[i][ii].find_element_by_css_selector('tr:nth-of-type(2) td:nth-of-type(3) font:nth-of-type(1)')\
                        .text.replace('(','').replace(')','').strip()
                except:
                    er_msg('父生産国取得: ERROR')
                arr10.append(elem)
                # 母名
                elem = ''
                try:
                    elem = hObj[i][ii].find_element_by_css_selector('tr:nth-of-type(2) td:nth-of-type(3) > div:nth-of-type(2)')\
                        .text.strip()
                except:
                    er_msg('母名取得: ERROR')
                arr11.append(elem)
                # 母生産国
                elem = ''
                try:
                    elem = hObj[i][ii].find_element_by_css_selector('tr:nth-of-type(2) td:nth-of-type(3) font:nth-of-type(3)')\
                        .text.replace('(','').replace(')','').strip()
                except:
                    er_msg('母生産国取得: ERROR')
                arr12.append(elem)
                # 母父名
                elem = ''
                try:
                    elem = hObj[i][ii].find_element_by_css_selector('tr:nth-of-type(2) td:nth-of-type(3) font:nth-of-type(4)')\
                        .text.split(',')[0].replace('(','').strip()
                except:
                    er_msg('母父名取得: ERROR')
                arr13.append(elem)
                # 母父生産国
                elem = ''
                try:
                    elem = hObj[i][ii].find_element_by_css_selector('tr:nth-of-type(2) td:nth-of-type(3) font:nth-of-type(4)')\
                        .text.split(',')[1].replace(')','').strip()
                except:
                    er_msg('母父生産国取得: ERROR')
                arr14.append(elem)
            h_num.append(arr01)
            h_frame.append(arr02)
            h_name.append(arr03)
            h_country.append(arr04)
            h_type.append(arr05)
            h_age.append(arr06)
            h_color.append(arr07)
            h_sex.append(arr08)
            h_sire.append(arr09)
            h_sireOri.append(arr10)
            h_mare.append(arr11)
            h_mareOri.append(arr12)
            h_bms.append(arr13)
            h_bmsOri.append(arr14)
        consoleLog('馬名',h_name)
        # ==================================================
        # データ成形 + 出力
        # ==================================================
        for z in range(len(r_num)):
            record01 = [rc_code,rc_name,rc_country,rc_date,r_num[z],r_td[z],r_name[z],r_class[z][0],r_type[z],'','',\
                        rc_dist[z],r_info[z],rc_type[z],r_gender[z],r_other[z],r_tPrize[z],r_prize[z]]
            for zz in range(h_value[z]):
                record02 = [h_num[z][zz],h_frame[z][zz],h_name[z][zz],h_country[z][zz],h_type[z][zz],h_age[z][zz],\
                            h_color[z][zz],h_sex[z][zz],h_sire[z][zz],h_sireOri[z][zz],h_mare[z][zz],h_mareOri[z][zz],\
                            h_bms[z][zz],h_bmsOri[z][zz]]
                writer.writerow(record01 + record02)
        # 一覧に戻る
        if dd < len(tarNum):
            time.sleep(1)
            driver.get(tar[d])
            driver.implicitly_wait(10)
            time.sleep(3)
            loadFlg()
driver.quit()
##終了時刻をエポック秒で取得（処理時間の計算用）
e_time = time.time()
p_time = e_time - s_time
##処理時間の表示
print('処理時間（秒）: ' + str(p_time))
sys.exit()
