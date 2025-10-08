# -*- coding: utf-8 -*-
from multiprocessing.sharedctypes import Array
from os import dup
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
    fErr.write('>> ' + str(driver.current_url))
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
    # ローディング完了まで繰り返し処理（5秒待機×最大36回）
    try:
        loopCount = 1
        while(a > 0):
            print('>> loading..')
            time.sleep(5)
            loopCount = loopCount + 1
            a = loadFlg()
            if loopCount > 36:
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
except:
    savePath = 'ERROR'
if savePath[-1] != '\\':
    savePath = savePath + '\\'
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
#sa_race-placing.txt
# ==============================
try:
    f = open('setting/sa_race-placing.txt', 'r', encoding='UTF-8')
    r_placing = f.read().split('\n')
    r_placing = [x.strip() for x in r_placing if x != '']
except:
    print('sa_race-placing.txt: ERROR')
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
# コース形態_設定
# ==============================
s_rcShape = readFile('sa_race-course.txt')
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
base = 'https://elturf.com/carreras-ultimos-resultados?fechaSel='
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
    FileName = savePath + 'elturf01_' + tarDate[d] + ".csv"
    ErFileName = savePath + 'Err_elturf01_' + tarDate[d] + ".txt"
    f = open(FileName, 'w', encoding="utf_8_sig")
    writer = csv.writer(f, lineterminator='\n')
    label = ["31","競馬場コード","競馬場","国名","レース日付","Date_L","Video","レース名","レース格","レースNo","レース Type","レース他",\
    "レース名省略","出走条件","馬場の種類","出走条件（性別）","出走条件（その他）","出走条件（年齢）","距離","コース形態","コース詳細","馬場状態","障害数",\
        "障害レース確認","総賞金","着賞金","並び順位","取得着順","異常区分","同着","着変更","馬番号","着差1","着差2",\
            "馬名","生産国","オッズ","馬齢","馬体重","斤量","斤量特記1","斤量特記2","補助馬具","調教師","騎手","毛色","性別",\
                "父名","母名","母父名","出走頭数","優勝馬タイム","オーナー","生産者","コメント"]
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
        consoleLog('進捗',str(dd + 1) + '/' + str(len(tarNum)))
        btnObj = driver.find_elements_by_css_selector('.table-condensed')[1::]
        btnObj[tarNum[dd]].find_element_by_css_selector('thead tr:nth-of-type(3) th:last-child a.btn').click()
        loadFlg()
        rcCount = driver.find_elements_by_xpath('//*[@id="app-elt"]/div[8]/div/div[3]/div/div/a')
        rcLinks = []
        for i in rcCount:
            obj = i.get_attribute('href').split('_')[-1]
            obj = 'https://elturf.com/carreras-resultado-ver?id_carrera=' + obj
            rcLinks.append(obj)
        rcCount = len(rcCount) - 1
        # ==============================
        # レースNo.
        # ==============================
        try:
            r_num = driver.find_elements_by_css_selector('table h1')
            if len(r_num) < rcCount:
                print('>> try again...')
                loadFlg()
                r_num = driver.find_elements_by_css_selector('table h1')
            r_num = [x.text.strip() for x in r_num]
            r_num = [x for x in r_num if x != '']
        except:
            r_num = ''
            er_msg('レースNo: ERROR')
        # ==============================
        # レース結果URL
        # ==============================
        #linkBtn = driver.find_elements_by_xpath('//*[@id="app-elt"]/div[8]/div/div/div/div[4]/a[3]')
        #rcLink = []
        #for i in range(len(r_num)):
        #    try:
        #        linkBtn[i].click()
        #        time.sleep(1)
        #        rcLink.append(pyperclip.paste())
        #    except:
        #        rcLink.append('')
        #        er_msg('レース結果URL: ERROR')
        #consoleLog('URL',rcLink)
        # ==============================
        # 競馬場 / 競馬場コード / 開催日
        # ==============================
        hdText = driver.find_element_by_css_selector('.col-xs-6.col-sm-6.col-md-6.col-lg-6.text-left')
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
            rc_date_M = rc_date_M.replace('01','1').replace('02','2').replace('03','3').replace('04','4').replace('05','5')\
                .replace('06','6').replace('07','7').replace('08','8').replace('09','9')
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
        # レース名
        # ==============================
        try:
            r_name = driver.find_elements_by_xpath('//*[@id="app-elt"]/div[8]/div/div/div/table[1]/tbody/tr[1]/td[4]/strong')
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
            obj = driver.find_elements_by_xpath('//*[@id="app-elt"]/div[8]/div/div/div/table[1]/tbody/tr[2]/td[1]')
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
            obj = driver.find_elements_by_xpath('//*[@id="app-elt"]/div[8]/div/div/div/table[1]/tbody/tr[2]/td[1]')
            r_type = [x.text.split('|')[0].split('(')[1].split(')')[0].strip() for x in obj]
        except:
            r_type = []
            for i in range(len(r_num)):
                r_type.append('')
            er_msg('レースType取得: ERROR')
        consoleLog('レースType',r_type)
        # ==============================
        # video
        # ==============================
        try:
            video = driver.find_elements_by_xpath('//*[@id="app-elt"]/div[8]/div/div/div/div[3]/div/div/div[1]')
            for i in range(len(video)):
                try:
                    video[i] = video[i].find_element_by_css_selector('button').get_attribute('href')
                except:
                    video[i] = ''
        except:
            video = []
            for i in range(len(r_num)):
                video.append('')
            er_msg('video取得: ERROR')
        consoleLog('video',video)
        # ==============================
        # 出走条件
        # ==============================
        try:
            r_info = driver.find_elements_by_xpath('//*[@id="app-elt"]/div[8]/div/div/div/table[1]/tbody/tr[2]/td[1]')
            r_info = [x.text.split('|')[1].strip() for x in r_info]
        except:
            r_info = []
            for i in range(len(r_num)):
                r_info.append('')
            er_msg('出走条件取得: ERROR')
        # ==============================
        # 馬場の種類、馬場状態
        # ==============================
        try:
            rc_type = driver.find_elements_by_xpath('//*[@id="app-elt"]/div[8]/div/div/div/table[1]/tbody/tr[2]/td[2]')
            rc_type = [x.text.strip() for x in rc_type]
            rc_cond = [x.split('(')[1].replace(')','').strip() for x in rc_type]
            rc_type = [x.split('(')[0].strip() for x in rc_type]
        except:
            rc_cond = ''
            rc_type = ''
            er_msg('馬場の種類・馬場状態取得: ERROR')
        consoleLog('馬場の種類',rc_type)
        consoleLog('馬場状態',rc_cond)
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
        # 出走条件（年齢）
        # ==============================
        rc_age = []
        try:
            for i in range(len(r_num)):
                rc_age.append(r_info[i].rsplit('(',1)[1].replace(')','').strip())
        except:
            for i in range(len(r_num)):
                rc_age.append('')
            er_msg('出走条件（年齢）: ERROR')
        # ==============================
        # 距離
        # ==============================
        try:
            rc_dist = driver.find_elements_by_xpath('//*[@id="app-elt"]/div[8]/div/div/div/table[1]/tbody/tr[1]/td[6]/strong')
            rc_dist = [x.text.strip() for x in rc_dist]
        except:
            rc_dist = []
            for i in range(len(r_num)):
                rc_dist.append('')
            er_msg('距離取得: ERROR')
        # ==============================
        # コース形態
        # ==============================
        rc_shape = []
        for i in range(len(r_num)):
            rc_shape.append('')
        for i in range(len(r_num)):
            for ii in s_rcShape:
                if ii in r_info[i]:
                    rc_shape[i] = ii
        # ==============================
        # 総賞金
        # ==============================
        try:
            r_tPrize = driver.find_elements_by_xpath('//*[@id="app-elt"]/div[8]/div/div/div/table[1]/tbody/tr[1]/td[5]/span/strong')
            r_tPrize = [x.text.strip() for x in r_tPrize]
        except:
            r_tPrize
            for i in range(len(r_num)):
                r_tPrize.append('')
            er_msg('総賞金取得: ERROR')
        # ==================================================
        # 出走馬リストテーブル
        # ==================================================
        try:
            h_table = driver.find_elements_by_xpath('//*[@id="app-elt"]/div[8]/div/div/div/table[2]')
        except:
            er_msg('出走馬リスト取得: ERROR')
            sys.exit()
        # ==============================
        # 出走馬数
        # ==============================
        h_value = []
        try:
            for i in range(len(h_table)):
                elem = h_table[i].find_elements_by_css_selector('tbody tr:last-child')
                h_value.append(len(elem))
        except:
            er_msg('出走頭数取得: ERROR')
            sys.exit()
        consoleLog('出走頭数',h_value)
        # ==============================
        # 着賞金
        # ==============================
        h_prize = []
        try:
            elem = driver.find_elements_by_xpath('//*[@id="app-elt"]/div[8]/div/div/div/table[1]/tbody/tr[3]/td[1]')
            for i in range(len(elem)):
                e = elem[i].find_elements_by_css_selector('span strong')
                e = [x.text.strip() for x in e]
                arr = []
                for ii in range(len(e)):
                    if re.search(r'^-',e[ii]):
                        e[ii] = e[ii].split('-',1)[1].strip()
                    arr.append(e[ii])
                h_prize.append(arr)
        except:
            for i in range(len(r_num)):
                h_prize.append('')
            er_msg('着賞金取得: ERROR')
        # ==============================
        # 並び順
        # ==============================
        r_listNum = []
        try:
            for i in range(len(r_num)):
                arr = []
                for ii in range(h_value[i]):
                    arr.append(ii+1)
                r_listNum.append(arr)
        except:
            er_msg('出走馬リスト取得: ERROR')
        # ==============================
        # 取得着順
        # ==============================
        hs_num = []
        try:
            for i in range(len(r_num)):
                e = h_table[i].find_elements_by_css_selector('tbody tr:last-child td:nth-of-type(1)')
                e = [x.text.split('°')[0].strip() for x in e]
                hs_num.append(e)
        except:
            for i in range(len(r_num)):
                for ii in range(h_value[i]):
                    hs_num.append('')
            er_msg('着順取得: ERROR')
        consoleLog('取得着順',hs_num)
        # ==============================
        # 同着
        # ==============================
        arrival = []
        try:
            for i in range(len(r_num)):
                arr = []
                # 重複要素を抽出
                dupNum = [x for x in set(hs_num[i]) if hs_num[i].count(x) > 1]
                # 重複要素が英字の場合は削除
                for ii in range(len(dupNum)):
                    if dupNum[ii].isalpha() != False:
                        dupNum[ii] = ''
                    else:
                        pass
                dupNum = [x for x in dupNum if x != '']
                # 重複要素と取得着順を照合
                for ii in range(len(hs_num[i])):
                    if hs_num[i][ii] in dupNum:
                        arr.append('dht')
                    else:
                        arr.append('')
                arrival.append(arr)
        except:
            er_msg('同着取得: ERROR')
        consoleLog('同着',arrival)
        print(arrival)
        # ==============================
        # 同着の賞金調整
        # ==============================
        h_prizeFix = []
        try:
            for i in range(len(r_num)):
                arr = []
                a = []
                for ii in range(len(h_prize[i])):
                    a.append([str(ii+1),h_prize[i][ii]])
                a = dict(a)
                for ii in range(len(hs_num[i])):
                    if ii < len(a):
                        try:
                            arr.append(a[hs_num[i][ii]])
                        except:
                            arr.append('')
                    else:
                        arr.append('')
                h_prizeFix.append(arr)
        except:
            for i in range(len(r_num)):
                h_prizeFix.append('')
            er_msg('同着賞金取得: ERROR')
        consoleLog('賞金',h_prizeFix)
        # ==============================
        # 馬番号
        # ==============================
        hs_gNum = []
        try:
            getTableText(hs_gNum,'tbody tr:last-child td:nth-of-type(2)')
        except:
            for i in range(len(r_num)):
                hs_gNum.append('')
            er_msg('馬番号取得: ERROR')
        consoleLog('馬番号',hs_gNum)
        # ==============================
        # 着差
        # ==============================
        hs_dist = []
        try:
            getTableText(hs_dist,'tbody tr:last-child td:nth-of-type(6)')
        except:
            for i in range(len(r_num)):
                hs_dist.append('')
            er_msg('着差取得: ERROR')
        consoleLog('着差',hs_dist)
        # ==============================
        # 異常区分
        # ==============================
        abClass = []
        try:
            for i in range(len(r_num)):
                arr = []
                for rp in range(len(hs_dist[i])):
                    if hs_dist[i][rp] in r_placing:
                        for ii in range(len(r_placing)):
                            if hs_dist[i][rp] == r_placing[ii]:
                                arr.append(r_placing[ii])
                            else:
                                pass
                    else:
                        arr.append('')
                abClass.append(arr)
        except:
            er_msg('異常区分取得: ERROR')
        consoleLog('異常区分',abClass)
        # ==============================
        # 馬名
        # ==============================
        hs_name = []
        try:
            getTableText(hs_name,'tbody tr:last-child td:nth-of-type(3) strong')
        except:
            for i in range(len(r_num)):
                hs_name.append('')
            er_msg('馬名取得: ERROR')
        consoleLog('馬名',hs_name)
        # ==============================
        # オッズ
        # ==============================
        hs_odds = []
        try:
            getTableText(hs_odds,'tbody tr:last-child td:last-child')
        except:
            for i in range(len(r_num)):
                hs_odds.append('')
            er_msg('オッズ取得: ERROR')
        consoleLog('オッズ',hs_odds)
        # ==============================
        # 馬齢
        # ==============================
        hs_age = []
        try:
            getTableText(hs_age,'tbody tr:last-child td:nth-of-type(4)')
        except:
            for i in range(len(r_num)):
                hs_age.append('')
            er_msg('馬齢取得: ERROR')
        consoleLog('馬齢',hs_age)
        # ==============================
        # 馬体重
        # ==============================
        hs_weight = []
        try:
            getTableText(hs_weight,'tbody tr:last-child td:nth-of-type(5)')
        except:
            for i in range(len(r_num)):
                hs_weight.append('')
            er_msg('馬体重取得: ERROR')
        consoleLog('馬体重',hs_weight)
        # ==============================
        # 斤量
        # ==============================
        j_weight = []
        try:
            getTableText(j_weight,'tbody tr:last-child td:nth-of-type(7) strong')
        except:
            for i in range(len(r_num)):
                j_weight.append('')
            er_msg('斤量取得: ERROR')
        consoleLog('斤量',j_weight)
        # ==============================
        # 調教師
        # ==============================
        h_trainer = []
        try:
            getTableText(h_trainer,'tbody tr:last-child td:nth-of-type(9)')
        except:
            for i in range(len(r_num)):
                h_trainer.append('')
            er_msg('調教師取得: ERROR')
        consoleLog('調教師',h_trainer)
        # ==============================
        # 騎手
        # ==============================
        h_jockey = []
        try:
            getTableText(h_jockey,'tbody tr:last-child td:nth-of-type(8)')
        except:
            for i in range(len(r_num)):
                h_jockey.append('')
            er_msg('騎手取得: ERROR')
        consoleLog('騎手',h_jockey)
        # ==============================
        # 父名
        # ==============================
        hs_sire = []
        try:
            for i in range(len(r_num)):
                e = h_table[i].find_elements_by_css_selector('tbody tr:last-child td:nth-of-type(3)')
                e = [x.text.split('(')[1].replace(')','').strip() for x in e]
                hs_sire.append(e)
        except:
            for i in range(len(r_num)):
                hs_sire.append('')
            er_msg('父名取得: ERROR')
        consoleLog('父名',hs_sire)
        # ==============================
        # オーナー
        # ==============================
        h_owner = []
        try:
            getTableText(h_owner,'tbody tr:last-child td:nth-of-type(10)')
        except:
            for i in range(len(r_num)):
                h_owner.append('')
            er_msg('オーナー取得: ERROR')
        consoleLog('オーナー',h_owner)
        # ==============================
        # 優勝馬タイム, 生産者
        # ==============================
        r_time = []
        hs_breeder = []
        try:
            a = driver.find_elements_by_css_selector('.well.well-sm.text-left')
            for i in range(len(a)):
                # 文字列による照合処理
                b = a[i].find_elements_by_css_selector('strong')
                b = [x.text for x in b]
                for z in range(len(b)):
                    # 優勝馬タイム
                    if 'Tiempo:' in b[z]:
                        c = a[i].text.split('Tiempo:')[1].strip()
                        c = re.split(r'\d+[m]', c)[0].strip()
                        r_time.append(c)
                    # 生産者
                    elif 'Criadores :' in b[z]:
                        c = a[i].text.split('Criadores :')[1].split(', (')
                        c = [x.split(')',1)[1].strip() for x in c]
                        hs_breeder.append(c)
        except:
            er_msg('優勝場タイム・生産者取得: ERROR')
        consoleLog('優勝馬タイム',r_time)
        consoleLog('生産者',hs_breeder)
        # ==================================================
        # データ成形 + 出力
        # ==================================================
        for z in range(len(r_num)):
            record01 = ['32',rc_code,rc_name,rc_country,rc_date,rcLinks[z],video[z],r_name[z],r_class[z][0],r_num[z],r_type[z],'','',\
                        r_info[z],rc_type[z],r_gender[z],r_other[z],rc_age[z],rc_dist[z],rc_shape[z],'',rc_cond[z],'']
            for zz in range(h_value[z]):
                if zz == 0:
                    var_time = r_time[z]
                else:
                    var_time = ''
                record02 = ['',r_tPrize[z],h_prizeFix[z][zz],r_listNum[z][zz],hs_num[z][zz],abClass[z][zz],arrival[z][zz],'',hs_gNum[z][zz],hs_dist[z][zz],\
                    '',hs_name[z][zz],'',hs_odds[z][zz],hs_age[z][zz],hs_weight[z][zz],j_weight[z][zz],'','','',h_trainer[z][zz],h_jockey[z][zz],\
                    '','',hs_sire[z][zz],'','',h_value[z],var_time,h_owner[z][zz],hs_breeder[z][zz]]
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