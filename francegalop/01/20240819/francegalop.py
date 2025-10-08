# -*- coding: utf-8 -*-
from selenium import webdriver
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
import sys

##開始時刻をエポック秒で取得（処理時間の計算用）
s_time = time.time()
############################
# 照合リスト
############################
# 設定ファイルロード関数01
rPath = 'setting/'
def readFile01(a):
    try:
        f = open(rPath + a, 'r', encoding='UTF-8')
        b = f.read()
        if '\n' in b:
            b = b.split('\n')
        else:
            b = [b]
    except:
        print('>> ' + str(a) + ': ERROR')
        sys.exit()
    return b

# 設定ファイルロード関数02
def readFile02(a):
    try:
        c_fPath = rPath + a
        b = []
        with open(c_fPath, encoding='utf_8_sig') as f:
            reader = csv.reader(f)
            for r in reader:
                b.append(r)
    except:
        print('>> France-galop_country.csv: ERROR')
        sys.exit()
    return b

##############################
# save.txt（保存先）
savePath = readFile01('save.txt')
savePath = savePath[0]
if savePath.endswith('/') or savePath.endswith('¥'):
    pass
else:
    if '¥' in savePath:
        savePath = savePath + '¥'
    else:
        savePath = savePath + '/'
##############################
# targets.txt（対象馬URL）
targets = readFile01('targets.txt')
##############################
# origin.txt（生産馬表記）
origin_list = readFile01('origin.txt')
##############################
# corse_around.txt（コースまわり）
rc_around = readFile01('race-course.txt')
##############################
# france-galop_horse-type.txt（馬種）
h_type_list = readFile01('france-galop_horse-type.txt')
############################
# 競馬場コード
rc_list = readFile02('France-galop_country.csv')
############################
# 異常区分
st_list = readFile02('France-galop_race-placing.csv')
############################
# 馬種
hk_list = readFile02('kinds.csv')
############################
# function
############################
def ErRef():
    obj = driver.find_elements_by_css_selector('.tec')
    if len(obj) > 0:
        driver.refresh()
        print('refresh')
############################
# ChromeDriver
############################
# Chrome展開
driver = webdriver.Chrome()
options = Options()
driver.set_window_size(1300,768)
driver.get('https://www.france-galop.com/fr/courses/toutes-les-courses')
driver.implicitly_wait(10)
ErRef()

#cookieバナー
try:
    cookie = driver.find_element_by_css_selector('.cookiefirst-root')
    btn = cookie.find_elements_by_css_selector('button')
    for i in range(len(btn)):
        el = btn[i].get_attribute('innerHTML')
        if 'Accepter tout' in el:
            btn[i].click()
        else:
            pass
except:
    pass

# 日付入力
try:
    sDate = driver.find_element_by_css_selector('#frglp_start_date')
    xi = sDate.clear()
    xi = sDate.send_keys(targets[0])
    eDate = driver.find_element_by_css_selector('#frglp_end_date')
    xi = eDate.clear()
    xi = eDate.send_keys(targets[1])
    time.sleep(2)
    xi = driver.find_element_by_css_selector('#all_races_filter').click()
    time.sleep(1)
except:
    print('>> ERROR: 01')
    sys.exit()


# 結果を取得して日付を追加
xi = [0]
xTable = []
try:
    xii = driver.find_elements_by_css_selector('#all_races__list tbody tr')
    for i in range(len(xii)):
        a = xii[i].find_element_by_css_selector('td:nth-of-type(1)').text.strip()
        b = xii[i].find_element_by_css_selector('td:nth-of-type(2) a').text.strip()
        c = xii[i].find_element_by_css_selector('td:nth-of-type(2) a').get_attribute('href')
        xTable.append([a,b,c])
         # 日付記載のあるTR番号を取得してxiに格納
        if 'jour' in xii[i].get_attribute('class'):
            xi.append(xii.index(xii[i]) + 1)
    del xi[-1]
    for i in range(len(xTable)):
        if xTable[i][0] == '':
            pass
        else:
            s = xTable[i][0]
        xTable[i][0] = s
except:
    print('ERROR')

#日付表記を和式に変更
try:
    for i in range(len(xTable)):
        a = xTable[i][0].split('/')
        xTable[i][0] = a[2] + '/' + a[1] + '/' + a[0]
except:
    pass

# フランス競馬場を選定
linklist = []
for i in range(len(xTable)):
    for rc in rc_list:
        if xTable[i][1] == rc[3]:
            if rc[2] == 'FR':
                linklist.append(xTable[i])
            else:
                pass

# レース結果 or 出馬表のURLを格納するリスト
rc_links = []

for z in range(len(linklist)):
    driver.get(linklist[z][2])
    # レース結果 or 出馬表の精査
    def flow01():
        try:
            # 1行目8列目に文字列があればレース結果
            # 1行目8列目に文字列が無く7列目に「Parts」を含む文字列があれば出馬表
            xi = driver.find_elements_by_css_selector('div.table.course tbody tr')
            xii = [x.find_element_by_css_selector('td:nth-of-type(3) a')\
                .get_attribute('href') for x in xi]
            flg01 = xi[0].find_element_by_css_selector('td:nth-of-type(8)').text.strip()
            flg02 = xi[0].find_element_by_css_selector('td:nth-of-type(7)').text.strip()
            # 競馬場名の取得
            try:
                xiii = driver.find_element_by_css_selector('h1').text.split(' - ')[1].strip()
            except:
                xiii = ''
            if flg01 == '' and 'Parts' in flg02:
                # 出馬表の場合
                xii.insert(0,'01')
                xii.insert(1,xiii)
            elif len(flg01) > 0:
                # レース結果の場合
                xii.insert(0,'02')
                xii.insert(1,xiii)
            else:
                xii.insert(0,'03')
                xii.insert(1,xiii)
            xii.insert(2,linklist[z][0])
        except:
            pass
        if xii[0] == '01' or xii[0] == '02' or xii[0] == '03':
            pass
        else:
            xii = []
        rc_links.append(xii)
    try:
        flow01()
    except:
        ErRef()
        flow01()

# 出馬表URLリスト
rc_links01 = []
# レース結果URLリスト
rc_links02 = []
# その他のURLリスト
rc_links03 = []
# 不要なリストを削除
#rc_links = [x for x in rc_links if x != []]

print(rc_links)
for z in rc_links:
    x = z[3::]
    if z[0] == '01':
        for loop in x:
            rc_links01.append([z[2],z[1],loop])
    elif z[0] == '02':
        for loop in x:
            rc_links02.append([z[2],z[1],loop])
    elif z[0] == '03':
        for loop in x:
            rc_links03.append([z[2],z[1],loop])
    else:
        pass

# 日付 / 競馬場でリストを精査
def getDate(a):
    cateDate = []
    for i in a:
        cateDate.append(i[0])
    cateDate = list(dict.fromkeys(cateDate))
    for i in range(len(cateDate)):
        cateDate[i] = [cateDate[i]]
    cate = []
    for i in cateDate:
        for ii in a:
            if i[0] == ii[0]:
                i.append(ii[1::])
        cate.append(i)
    return cate


label01 = ['競馬場コード','競馬場','競馬場詳細','国名','レース日付','レース名','レース格','レースNo','発走時刻',\
    'レース Type','レース他','レース名省略','出走条件','馬場の種類','距離','コース回り','出走条件（性別）','出走条件（クラス）','出走条件（その他）','総賞金',\
        '馬番号','ゲート番号','馬名','生産国','馬齢','馬種','調教師','騎手','毛色','性別','父名','母名','母父名']
label02 = ['31','競馬場コード','競馬場','競馬場詳細','国名','レース日付','Date_L','Video','スチュワード情報','セクショナルズ',\
    'レース名','レース格','レースNo','レース Type','レース他','レース名省略','出走条件','馬場の種類','出走条件（性別）',\
        '出走条件（クラス）','出走条件（その他）','出走条件（年齢）','距離','コース回り','コース形態','コース詳細',\
            '馬場状態','障害数','障害レース確認','総賞金','着賞金','並び順位','確定順位','異常区分','同着','着変更',\
                '馬番号','ゲート番号','着差1','着差2','馬名','生産国','オッズ','馬齢','馬種','馬体重','斤量',\
                    '斤量特記1','斤量特記2','補助馬具','調教師','騎手','毛色','性別','父名','母名','母父名',\
                        '出走頭数','優勝馬タイム','オーナー','生産者','コメント']

############################
# スクレイピング処理
############################
def scraping(xxx):

    r_fmt = xxx
    print('flg: ' + r_fmt)

    ##############################
    # レース情報01
    ##############################
    try:
        r_info01 = driver.find_element_by_css_selector('.course-detail > p:nth-of-type(1)')
    except:
        r_info01 = ''
    ##############################
    # 競馬場*
    ##############################
    try:
        rc_name = r_info01.text.split(',')[-1].strip()
    except:
        rc_name = ''
    ##############################
    # 競馬場コード* / 国名*
    ##############################
    try:
        for i in rc_list:
            if rc_codeName == i[3]:
                rc_code = i[0]
                rc_country = i[1]
            else:
                pass
    except:
        rc_code = ''
        rc_country = ''
    ##############################
    # レース日付*
    ##############################
    try:
        r_date = r_info01.text.split('—')[1].strip().split(' ')[0]
        r_date = r_date.split('/')
        r_date = r_date[2] + '/' + r_date[1] + '/' + r_date[0]
    except:
        r_date = ''
    ##############################
    # レース名*
    ##############################
    try:
        r_name = driver.find_element_by_css_selector('h1').text.strip()
    except:
        r_name = ''
    ##############################
    # レースNo*
    ##############################
    try:
        r_order = r_info01.text.split('(')[0].strip()
    except:
        r_order = ''
    ##############################
    # 発走時刻（出馬表）
    ##############################
    try:
        r_start = r_info01.text.split('—')[1].strip().split(' ')[1].split(',')[0]
    except:
        r_start = ''
    ##############################
    # 出走条件（クラス）
    ##############################
    try:
        r_dClass = r_info01.text.split(',')[1].split('—')[0].strip()
    except:
        r_dClass = ''
    ##############################
    # レース情報02*
    ##############################
    try:
        r_info02 = driver.find_element_by_css_selector('.course-detail > p:nth-of-type(2)')
    except:
        r_info02 = ''
    if 'PROCES VERBAL NON PARVENU' in r_info02.text.strip():
        pass
    else:
        ##############################
        # レースType*
        ##############################
        try:
            r_type_d = r_info02.find_element_by_css_selector('strong').text.split(',')[0].strip()
        except:
            r_type_d = ''
        ##############################
        # 距離*
        ##############################
        try:
            r_dist_d = r_info02.find_element_by_css_selector('strong').text.split(',')[1].strip()
        except:
            r_dist_d = ''
        ##############################
        # コース回り*
        ##############################
        try:
            rc_way = ''
            xi = r_info02.text.split('\n')[0].split(', ')
            for i in xi:
                i = i.strip()
                if i in rc_around:
                #if re.match(r'Corde', i):
                    rc_way = i
        except:
            rc_way = ''
        ##############################
        # 馬場状態
        ##############################
        if r_fmt == '02':
            try:
                xi = r_info02.text.split('\n')[0].strip()
                if 'Terrain ' in xi:
                    rc_condition = xi.split('Terrain ')[1].strip()
                else:
                    rc_condition = ''
            except:
                rc_condition = ''
        ##############################
        # 総賞金*
        ##############################
        try:
            r_prize = ''
            xi = r_info02.text.split('\n')
            for i in xi:
                i = i.strip()
                if re.match(r'^\(', i):
                    i = i.replace('(','').replace(')','').strip()
                    r_prize = i
        except:
            r_prize = ''
        ##############################
        # 出走頭数（表記）
        ##############################
        h_sValue = ''
        try:
            xi = r_info02.text.split('.')
            for i in xi:
                if re.search(r'\d Partants', i):
                    h_sValue = i
                else:
                    pass
            xii = h_sValue.split(' Partants')[0].strip()
            if re.match(r'^\d', xii):
                h_sValue = xii
            else:
                h_sValue = ''
        except:
            pass
        ##############################
        # レースタイム（結果）
        ##############################
        if r_fmt == '02':
            try:
                r_time = r_info02.text.split('Temps du 1er :')[1].split('\n')[0].strip()
            except:
                r_time = ''
        ##############################
        # スチュワード（結果）
        ##############################
        if r_fmt == '02':
            # スチュワード情報の可視化
            def visible():
                try:
                    sc = "txt = document.querySelector('.infotip.commissaire .txt');\
                        txt.style.cssText = 'opacity:1; visibility:visible'"
                    driver.execute_script(sc)
                    time.sleep(1)
                except:
                    pass
            try:
                xi = driver.find_elements_by_css_selector('.infotip.commissaire .txt')
                if len(xi) > 0:
                    visible()
                    steward = xi[0].text.strip()
                    steward = steward.replace('|','')
                else:
                    steward = ''
            except:
                steward = ''
            if steward == '':
                try:
                    visible()
                    steward = xi[0].text.strip()
                    steward = steward.replace('|','')
                except:
                    steward = ''
        ##############################
        # セクショナルズ（結果）
        ##############################
        if r_fmt == '02':
            try:
                xi = r_info02.get_attribute('innerHTML')
                if '="pdf_course_trackee' in xi:
                    pdflink = driver.find_element_by_css_selector('.pdf_course_trackee').get_attribute('href')
                else:
                    pdflink = ''
            except:
                pdflink = ''
        ##############################
        # レース情報03*
        ##############################
        try:
            r_info03 = driver.find_element_by_css_selector('.course-detail > p:nth-of-type(3)')
        except:
            r_info03 = ''
        ##############################
        # レース格*
        ##############################
        try:
            r_grade_d = r_info03.find_element_by_css_selector('strong').text.strip()
        except:
            r_grade_d = ''
        ##############################
        # 出走条件*
        ##############################
        try:
            r_cond01 = []
            xi = r_info03.text.split('\n')
            for i in xi:
                i = i.strip()
                if re.match(r'^Pour ', i):
                    i = i.split('.')[0]
                    i = i + '.'
                    r_cond01.append(i)
                else:
                    pass
            if len(r_cond01) > 0:
                r_cond01 = r_cond01[0]
            else:
                r_cond01 =''
        except:
            r_cond01 = ''
        ##############################
        # 出走条件（馬種）
        ##############################
        r_kCond = ''
        try:
            for i in hk_list:
                if i[0] in r_cond01:
                    r_kCond = i[1]
                else:
                    pass
        except:
            r_kCond = ''
        ##############################
        # 馬場の種類
        ##############################
        try:
            rc_type = 'Turf'
            xi = r_info02.text.split('\n')[0].split(',')
            for i in xi:
                if 'PSF' in i:
                    rc_type = 'AW'
                else:
                    pass
        except:
            rc_type = ''
        ##############################
        # 出走馬情報
        ##############################
        th = driver.find_elements_by_css_selector('.raceTable thead tr th')
        tr = driver.find_elements_by_css_selector('.raceTable tbody tr')
        tr = [x.find_elements_by_css_selector('td') for x in tr]
        ##############################
        # テーブル成形
        ##############################
        # [0]着順[1]馬名[2]馬番号[3]血統[4]着差/ゲート番号[5]ゲート番号
        # [6]オーナー[7]調教師[8]騎手[9]斤量[10]補助馬具[11]生産者
        def mkT(x,y):
            if th[i].text.strip() == x:
                for ii in range(len(tr)):
                    table[y].append(tr[ii][i])
        def ErElem(x,y):
            if len(x) == 0:
                for i in range(y):
                    x.append('')
            else:
                pass
        table = []
        for i in range(14):
            table.append([])
        for i in range(len(th)):
            mkT('Place',0)
            mkT('Cheval',1)
            mkT('N°',2)
            mkT('Père/Mère',3)
            mkT('Écart au précédent',4)
            mkT('Corde',5)
            mkT('Propriétaire',6)
            mkT('Entraîneur',7)
            mkT('Entraineur',7)
            mkT('Jockey',8)
            mkT('Poids',9)
            mkT('Equipement(s)',10)
            mkT('Éleveurs',11)
            mkT('Prim. prop.',12)
            mkT('Prim. elev.',13)
        ##############################
        # 出走頭数（結果）
        ##############################
        try:
            h_value = len(tr)
        except:
            h_value = 0
        ##############################
        # 着順（結果）
        ##############################
        if r_fmt == '02':
            h_num = table[0]
            h_num = [x.text.strip() for x in h_num]
            ErElem(h_num,h_value)
        ##############################
        # 並び順位（結果）
        ##############################
        if r_fmt == '02':
            num = []
            for r in range(len(h_num)):
                num.append(str(r+1))
        ##############################
        # 馬番号*
        ##############################
        h_rNum = table[2]
        h_rNum = [x.text.strip() for x in h_rNum]
        ##############################
        # ゲート番号*
        ##############################
        if r_fmt == '01':
            h_gate = copy.copy(table[4])
            if len(h_gate) == 0:
                h_gate = copy.copy(table[5])
        elif r_fmt == '02':
            h_gate = copy.copy(table[5])
            if len(h_gate) == 0:
                h_gate = copy.copy(table[4])
        for i in range(len(h_gate)):
            try:
                h_gate[i] = h_gate[i].text.split('Corde:')[1].replace(')','').strip()
            except:
                h_gate[i] = ''
        ##############################
        # 異常区分（結果）
        ##############################
        if r_fmt == '02':
            # 異常区分
            h_status = []
            try:
                for i in h_num:
                    if re.match(r'^\D', i):
                        for ii in st_list:
                            if i == ii[0]:
                                h_status.append(ii[1])
                            else:
                                pass
                    else:
                        h_status.append('')
            except:
                for i in h_num:
                    h_status.append('')
            if len(h_status) < len(h_num):
                k = len(h_num) - len(h_status)
                for i in range(k):
                    h_status.append('')
        ##############################
        # 同着（結果）
        ##############################
        if r_fmt == '02':
            r_dht = []
            try:
                # 重複する要素を抽出
                dup = [x for x in set(h_num) if h_num.count(x) > 1]
                for i in range(len(h_num)):
                    if h_num[i] in dup and re.match(r'^[0-9]', h_num[i]):
                        r_dht.append('dht')
                    else:
                        r_dht.append('')
            except:
                r_dht = ErElem(h_value)
        ##############################
        # 確定着順と賞金を照合（結果）
        ##############################
        if r_fmt == '02':
            # 賞金を辞書型に格納
            pDict = {}
            try:
                xi = r_prize.split(',')
                for i in range(len(xi)):
                    xnum = str(i + 1)
                    pDict[xnum] = xi[i].strip()
            except:
                pass
            num_prize = []
            try:
                # 出走頭数の分だけ要素を追加
                for i in range(len(h_num)):
                    num_prize.append('')
                # 確定着順と賞金（辞書Key）を照合して賞金額を格納
                for i in range(len(h_num)):
                    if h_num[i] in pDict.keys():
                        x = h_num[i]
                        num_prize[i] = pDict[x]
                    else:
                        pass
            except:
                num_prize.append('')
        ##############################
        # 着差（結果）
        ##############################
        if r_fmt == '02':
            xi = copy.copy(table[4])
            h_margin = []
            for i in range(len(xi)):
                try:
                    xii = xi[i].text.split('Corde:')[0].replace('(','').strip()
                    h_margin.append(xii)
                except:
                    h_margin.append('')
        ##############################
        # 生産国照合用
        ##############################
        oriCheck = []
        if r_fmt == '02':
            oriCheck01 = []
            oriCheck02 = []
            for i in table[12]:
                oriCheck01.append(i.text.strip())
            for i in table[13]:
                oriCheck02.append(i.text.strip())
            for i in range(h_value):
                try:
                    if len(oriCheck01[i]) > 0 or len(oriCheck02[i]) > 0:
                        oriCheck.append('FR')
                    else:
                        oriCheck.append('')
                except:
                    oriCheck.append('')
        else:
            for i in range(h_value):
                oriCheck.append('')
        ##############################
        # 馬名 / 生産国 / 性別 / 馬種 / 馬齢
        ##############################
        h_info = []
        ##############################
        # 馬齢*
        ##############################
        h_old = []
        xi = table[1]
        xi = [x.text for x in xi]
        for i in xi:
            i = i.split('.')
            i = [x.strip() for x in i]
            i = [x for x in i if x != '']
            if len(i[-1]) < 2:
                del i[-1]
            if re.match(r'\d+ ', i[-1]):
                h_old.append(i[-1].split(' ')[0].strip())
                del i[-1]
            else:
                try:
                    if re.match(r'\d+ ', i[-2]):
                        h_old.append(i[-2].split(' ')[0].strip())
                        del i[-2]
                    elif re.match(r'\d+ ', i[-3]):
                        h_old.append(i[-3].split(' ')[0].strip())
                        del i[-3]
                    else:
                        h_old.append('')
                except:
                    h_old.append('')
            try:
                if re.search('Sup',i[-1]) or re.search('sup',i[-1]) or re.search('SUP',i[-1]) or re.search('%',i[-1]):
                    del i[-1]
                if re.search('Sup',i[-1]) or re.search('sup',i[-1]) or re.search('SUP',i[-1]) or re.search('%',i[-1]):
                    del i[-1]
            except:
                pass
            h_info.append(('. ').join(i))
        ##############################
        # 馬種*
        ##############################
        h_type = []
        for i in range(len(h_info)):
            ii = h_info[i].split('.')
            ii = [x.strip() for x in ii]
            if ii[-1] in h_type_list:
                h_type.append(ii[-1])
                del ii[-1]
            else:
                h_type.append('')
            h_info[i] = ('. ').join(ii)
        ##############################
        # 性別*
        ##############################
        h_rSex = []
        for i in range(len(h_info)):
            if re.match(r'.* \D$', h_info[i]):
                ii = h_info[i].split(' ')
                h_rSex.append(ii[-1])
                del ii[-1]
                h_info[i] = (' ').join(ii)
            else:
                h_rSex.append('')
        ##############################
        # 生産国*
        ##############################
        h_rOrigin = []
        for i in range(len(h_info)):
            if '(' in h_info[i]:
                ii = h_info[i].replace('(','').replace(')','')
                ii = ii.split(' ')
                if ii[-1] in origin_list:
                    h_rOrigin.append(ii[-1])
                    del ii[-1]
                else:
                    h_rOrigin.append('FR')
                h_info[i] = (' ').join(ii)
            else:
                if len(oriCheck[i]) > 0:
                    h_rOrigin.append('FR')
                else:
                    ii = h_info[i].split(' ')
                    if ii[-1] in origin_list:
                        h_rOrigin.append(ii[-1])
                        del ii[-1]
                    else:
                        h_rOrigin.append('FR')
                    h_info[i] = (' ').join(ii)
        ##############################
        # 馬名*
        ##############################
        h_rName = [x.strip() for x in h_info]
        ##############################
        # 調教師（結果）
        ##############################
        h_trainer = table[7]
        h_trainer = [x.text.strip() for x in h_trainer]
        ##############################
        # 騎手（結果）
        ##############################
        h_jockey = table[8]
        h_jockey = [x.text.strip() for x in h_jockey]
        ##############################
        # 生産者（結果）
        ##############################
        if r_fmt == '02':
            h_breeder = table[11]
            h_breeder = [x.text.strip() for x in h_breeder]
        ##############################
        # オーナー（結果）
        ##############################
        if r_fmt == '02':
            h_owner = table[6]
            h_owner = [x.text.strip() for x in h_owner]
        ##############################
        # 毛色*
        ##############################
        ##############################
        # 斤量（結果）
        ##############################
        if r_fmt == '02':
            h_wgt = table[9]
            h_wgt = [x.text.strip().replace(',','.') for x in h_wgt]
        ##############################
        # 斤量特記1（結果）
        ##############################
        if r_fmt == '02':
            h_wgt1 = []
            try:
                for i in range(len(h_wgt)):
                    if '(' in h_wgt[i]:
                        x = h_wgt[i].split('(')
                        h_wgt1.append(x[1].split(')')[0].strip())
                        h_wgt[i] = x[0].strip()
                    else:
                        h_wgt1.append('')
            except:
                for i in h_wgt:
                    h_wgt1.append('')
        ##############################
        # 補助馬具（結果）
        ##############################
        if r_fmt == '02':
            h_aid = []
            xi = table[10]
            for i in range(len(xi)):
                a = xi[i].get_attribute('innerHTML')
                if '<span' in a:
                    xii = xi[i].find_elements_by_css_selector('span')
                    xii = [x.get_attribute('data-title').strip() for x in xii]
                    xii = ','.join(xii)
                    h_aid.append(xii)
                else:
                    h_aid.append('')
        ##############################
        # 父名*
        ##############################
        h_rSire = []
        xi = table[3]
        for i in xi:
            try:
                i = i.text.split('Par:')[1].split(' et ')[0].strip()
                h_rSire.append(i)
            except:
                h_rSire.append('')
        ##############################
        # 母名*
        ##############################
        h_rDam = []
        xi = table[3]
        for i in xi:
            try:
                i = i.text.split(' et ')[1].split('(')[0].strip()
                h_rDam.append(i)
            except:
                h_rDam.append('')
        ##############################
        # 母父名*
        ##############################
        h_rDamsire = []
        xi = table[3]
        for i in xi:
            try:
                i = i.text.split('(')[1].split(')')[0].strip()
                h_rDamsire.append(i)
            except:
                h_rDamsire.append('')
        ##############################
        # レコード成形
        ##############################
        record = []
        for r in range(len(h_rName)):
            if re.match(r'\d', h_old[r]):
                pass
            else:
                h_old[r] = ''
            if r_fmt == '01':
                x = [rc_code,rc_codeName,rc_name,rc_country,r_date,r_name,r_grade_d,r_order,r_start,r_type_d,'','',\
                    r_cond01,rc_type,r_dist_d,rc_way,'',r_dClass,r_kCond,r_prize,\
                    h_rNum[r],h_gate[r],h_rName[r],h_rOrigin[r],h_old[r],h_type[r],h_trainer[r],h_jockey[r],'',\
                    h_rSex[r],h_rSire[r],h_rDam[r],h_rDamsire[r]]
            elif r_fmt == '02':
                x = ['32',rc_code,rc_codeName,rc_name,rc_country,r_date,'','',steward,pdflink,r_name,r_grade_d,r_order,r_type_d,'','',\
                    r_cond01,rc_type,'',r_dClass,r_kCond,'',r_dist_d,rc_way,'','',rc_condition,'','','',\
                    num_prize[r],num[r],h_num[r],h_status[r],r_dht[r],'',\
                    h_rNum[r],h_gate[r],h_margin[r],'',h_rName[r],h_rOrigin[r],'',h_old[r],h_type[r],'',h_wgt[r],h_wgt1[r],'',h_aid[r],\
                    h_trainer[r],h_jockey[r],'',h_rSex[r],h_rSire[r],h_rDam[r],h_rDamsire[r],h_sValue,r_time,h_owner[r],h_breeder[r],'']
            record.append(x)
            print(record)
        return record


##############################
# 出馬表ページのスクレイピング
##############################
if len(rc_links01) > 0:
    fix = getDate(rc_links01)
    print('>> 出馬表ページのクローリング')
    for i in range(len(fix)):
        cateDate = fix[i][0]
        del fix[i][0]
        print('Date: ' + cateDate)
        # CSV生成
        f_Name = savePath + 'francegalop03_' + cateDate.replace('/','') + ".csv"
        e_Name = savePath + 'francegalop03_' + cateDate.replace('/','') + ".txt"
        f = open(f_Name, 'w', encoding="utf_8_sig")
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(label01)
        for ii in range(len(fix[i])):
            rc_codeName = fix[i][ii][0]
            print(rc_codeName)
            # 遷移
            driver.get(fix[i][ii][1])
            ErRef()
            x = scraping('01')
            try:
                for iii in x:
                    writer.writerow(iii)
            except:
                pass

##############################
# レース結果ページのスクレイピング
##############################
if len(rc_links02) > 0:
    fix = getDate(rc_links02)
    print(fix)
    print('>> レース結果ページのクローリング')
    for i in range(len(fix)):
        cateDate = fix[i][0]
        del fix[i][0]
        print('Date: ' + cateDate)
        # CSV生成
        f_Name = savePath + 'francegalop01_' + cateDate.replace('/','') + ".csv"
        e_Name = savePath + 'francegalop01_' + cateDate.replace('/','') + ".txt"
        f = open(f_Name, 'w', encoding="utf_8_sig")
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(label02)
        for ii in range(len(fix[i])):
            rc_codeName = fix[i][ii][0]
            print(rc_codeName)
            # 遷移
            driver.get(fix[i][ii][1])
            ErRef()
            x = scraping('02')
            try:
                for iii in x:
                    writer.writerow(iii)
            except:
                pass

##############################
# その他URLリストの処理
##############################
if len(rc_links03) > 0:
    fix = getDate(rc_links03)
    print(fix)
    print('>> 不明リストのログ生成')
    for i in range(len(fix)):
        cateDate = fix[i][0]
        del fix[i][0]
        print('Date: ' + cateDate)
        e_Name = savePath + 'francegalop_' + cateDate.replace('/','') + ".txt"
        fErr = open(e_Name, 'a', encoding="utf_8_sig")
        for ii in range(len(fix[i])):
            fErr.write('▼ ' + fix[i][ii][0] + '\n')
            fErr.write('>> ' + str(fix[i][ii][1]) + '\n')

driver.quit()
##終了時刻をエポック秒で取得（処理時間の計算用）
e_time = time.time()
p_time = e_time - s_time
##処理時間の表示
print('処理時間（秒）: ' + str(p_time))
sys.exit()