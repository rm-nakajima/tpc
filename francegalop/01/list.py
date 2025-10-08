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
# ChromeDriver
############################
# Chrome展開
driver = webdriver.Chrome()
options = Options()
driver.set_window_size(1300,768)
driver.get('https://www.france-galop.com/fr/courses/toutes-les-courses')
driver.implicitly_wait(10)

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
    try:
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
        # レース結果 / 出馬表の判定
        if flg01 == '' and 'Parts' in flg02:
            # 出馬表の場合
            xii.insert(0,'01')
            xii.insert(1,xiii)
        elif len(flg01) > 0:
            # レース結果の場合
            xii.insert(0,'02')
            xii.insert(1,xiii)
        xii.insert(2,linklist[z][0])
    except:
        pass
    if xii[0] == '01' or xii[0] == '02':
        pass
    else:
        xii = []
    rc_links.append(xii)

# 出馬表URLリスト
rc_links01 = []
# レース結果URLリスト
rc_links02 = []

for z in rc_links:
    x = z[3::]
    if z[0] == '01':
        for loop in x:
            rc_links01.append([z[2],z[1],loop])
    elif z[0] == '02':
        for loop in x:
            rc_links02.append([z[2],z[1],loop])


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

print('>> 出馬表URL:')
if len(rc_links01) < 1:
    print('0')
else:
    #cateDate01 = inDate(rc_links01)
    #fixlinks01 = inLinks(rc_links01,cateDate01)
    #print(fixlinks01)
    print('しゅつばひょー')

print('>> レース結果URL:')
if len(rc_links02) < 1:
    print('0')
else:
    print('れーすけっか')
    xi = getDate(rc_links02)
    cateDate02 = xi[0]
    print(xi)
    print(len(xi))
    #cateDate02 = inDate(rc_links02)
    #fixlinks02 = inLinks(rc_links02,cateDate02)
    #print(fixlinks02)
## 日付別に各レースを統合
#def inDate(tg):
#    cateDate = []
#    for i in tg:
#        cateDate.append(i[0])
#    cateDate = list(dict.fromkeys(cateDate))
#    return cateDate
#def inLinks(tg,cateDate):
#    fixlinks = []
#    for i in cateDate:
#        fixlinks.append([])
#    for i in range(len(tg)):
#        for ii in range(len(cateDate)):
#            if tg[i][0] == cateDate[ii]:
#                fixlinks[ii].append(tg[i][1])
#    return fixlinks
#
#print('>> 出馬表URL:')
#if len(rc_links01) < 1:
#    print('0')
#else:
#    cateDate = inDate(rc_links01)
#    fixlinks01 = inLinks(rc_links01,cateDate)
#    print(fixlinks01)
#    print(len(fixlinks01))
#print('>> レース結果URL:')
#if len(rc_links02) < 1:
#    print('0')
#else:
#    cateDate = inDate(rc_links02)
#    fixlinks02 = inLinks(rc_links02,cateDate)
#    print(fixlinks02)
#    print(len(fixlinks02))
#