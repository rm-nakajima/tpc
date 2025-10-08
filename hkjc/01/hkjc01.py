# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
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
# 開始時刻をエポック秒で取得（処理時間の計算用）
s_time = time.time()
# 今日の日付
toDay = datetime.date.today()
print('実行日: ' + str(toDay))
############################
# 設定ファイル
############################
pathPref = 'setting/'
def getExternal(file):
    file = pathPref + file
    try:
        if re.search(r'.csv$', file):
            #csvの処理
            xi = []
            with open(file, encoding='UTF-8') as f:
                reader = csv.reader(f)
                for r in reader:
                    xi.append(r)
        elif re.search(r'.txt$', file):
            #txtの処理
            xi = open(file, 'r', encoding='UTF-8')
            xi = xi.read() + '\n'
            xi = xi.split('\n')
            xi = [x for x in xi if x != '']
        return xi
    except:
        print('ERROR')
        sys.exit()
############################
# 保存場所
############################
savePath = getExternal('save.txt')[0]
if savePath.endswith('/') or savePath.endswith('¥'):
    pass
else:
    if '¥' in savePath:
        savePath = savePath + '¥'
    else:
        savePath = savePath + '/'
############################
# 出走ステータス
############################
excCount = getExternal('status.csv')
excCount01 = excCount[0][1::]
excCount01 = [x for x in excCount01 if x != '']
excCount02 = excCount[1][1::]
excCount02 = [x for x in excCount02 if x != '']
############################
# 対象馬
############################
targetDate = getExternal('target.txt')
############################
# その他
############################
basicInfo = {0:'Going :',1:'Course :',2:'Time :',3:'Sectional Time'}
############################
# エラー対応
############################
def er_msg(e):
    fErr = open(ErFileName, 'a', encoding="utf_8_sig")
    fErr.write('>> ' + str(driver.current_url))
    fErr.write('\n' + e + ' ERROR\n')
    print(e + 'ERROR')
############################
# LABEL
############################
head_iii = [\
            '31','競馬場コード','競馬場','国名','レース日付','Date_L','Video','Sectional','レース名','レース格','レースNo','レース他','レース名省略',\
            '出走条件（性別）','馬場の種類','障害数','障害レース確認','出走条件（クラス）','出走条件（他）','出走条件（年齢）','距離','コース形態',\
            'コース詳細','馬場状態','総賞金','着賞金','通過タイム01','通過タイム02','通過タイム03','通過タイム04','通過タイム05',\
            'finishタイム','レースSectionalタイム01','レースSectionalタイム02','レースSectionalタイム03','レースSectionalタイム04',\
            'レースSectionalタイム05','レースSectionalタイム06','レースSectionalタイム内訳01','レースSectionalタイム内訳02',\
            'レースSectionalタイム内訳03','レースSectionalタイム内訳04','馬別Sectionalタイム01','馬別Sectionalタイム02','馬別Sectionalタイム03',\
            '馬別Sectionalタイム04','馬別Sectionalタイム05','馬別Sectionalタイム06','馬別Sectionalタイム内訳01','馬別Sectionalタイム内訳02',\
            '馬別Sectionalタイム内訳03','馬別Sectionalタイム内訳04','通過順位01','通過順位02','通過順位03','通過順位04','通過順位05',\
            '入線順位','確定順位','異常区分','同着','着変更','馬番号','ゲート番号','着差1','着差2','馬名','馬ID','生産国','オッズ','馬齢','馬体重',\
            '斤量','斤量特記1','斤量特記2','補助馬具','調教師','騎手','毛色','性別','父名','母名','母父名','出走頭数','タイム','優勝馬オーナー',\
            '優勝馬生産者','コメント'
            ]
############################
# ChromeDriver
############################
driver = webdriver.Chrome()
options = Options()
driver.set_window_size(1300,768)
############################
# TARGET
############################
for T in range(len(targetDate)):
    target = []
    for i in range(len(targetDate)):
        abs = 'https://racing.hkjc.com/racing/information/english/Racing/LocalResults.aspx?RaceDate='
        target.append(abs + targetDate[i] + '&Racecourse=ST')
        target.append(abs + targetDate[i] + '&Racecourse=HV')
        target.append(abs + targetDate[i] + '&Racecourse=CH')
    for D in range(len(target)):
        ############################
        # 遷移
        ############################
        driver.get(target[D])
        driver.implicitly_wait(5)
        try:
            racecard = driver.find_element_by_css_selector('.js_racecard')
            raceCount = racecard.find_elements_by_css_selector('tr:nth-of-type(1) td a')
            raceCount = [x.get_attribute('href') for x in raceCount]
            ins = raceCount[0].split('&RaceNo')[0].strip() + '&RaceNo=1'
            raceCount.insert(0,ins)
            ############################
            # CSV生成（日付ごとにCSVを生成）
            ############################
            fileDate = targetDate[T].replace('/','').strip()
            fileName = savePath + 'hkjc01_' + fileDate + ".csv"
            ErFileName = savePath + 'Err_hkjc__' + fileDate + ".txt"
            f = open(fileName, 'w', encoding="utf_8_sig")
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(head_iii)
            ############################
            # レース数の分だけ繰り返し処理
            ############################
            for i in range(len(raceCount) - 1):
                print(raceCount[i])
                if i == 0:
                    raceCount[i] = raceCount[i]
                driver.get(raceCount[i])
                try:
                    ############################
                    # 出力要素
                    ############################
                    items = {\
                            '日付':'',\
                            'Date_L':raceCount[i],\
                            '競馬場':'',\
                            'レース番号':'',\
                            'レース格':'',\
                            '距離':'',\
                            '馬場状態':'',\
                            '馬場':'',\
                            '通過タイム':['','','','',''],\
                            'Finishタイム':'',\
                            'レースSecタイム':['','','','','',''],\
                            'セクショナルタイム':'',\
                            'Sectional':'',\
                            'レース格':'',\
                            '距離':'',\
                            'レース名':'',\
                            '総賞金':'',\
                            'video':'',\
                            '競馬場コード':'',\
                            '確定順位':[],\
                            '異常区分':[],\
                            '同着':[],\
                            '馬番号':[],\
                            '馬名':[],\
                            '馬ID':[],\
                            '騎手':[],\
                            '調教師':[],\
                            '斤量':[],\
                            '馬体重':[],\
                            'ゲート番号':[],\
                            '着差':[],\
                            '通過順位':[],\
                            '入線順位':[],\
                            '着変更':[],\
                            '入線タイム':'',\
                            'オッズ':'',\
                            'コメント':'',\
                            '馬別':[],\
                            '馬別内訳':[],\
                            }
                    # -------------------------
                    # 日付 / 競馬場
                    # -------------------------
                    try:
                        elm = driver.find_element_by_css_selector('.raceMeeting_select .f_clear .f_fl').text.strip()
                        itemDate = elm.split(':')[1].strip().split(' ')[0].strip()
                        items['競馬場'] = elm.split(itemDate)[1].strip()
                        itemDate = itemDate.split('/')
                        items['日付'] = itemDate[2] + '/' + itemDate[1] + '/' + itemDate[0]
                    except:
                        er_msg('競馬場')
                        er_msg('日付')
                    # -------------------------
                    # 国名
                    # -------------------------
                    items['国名'] = 'HK'
                    # -------------------------
                    # レース番号
                    # -------------------------
                    try:
                        elm = driver.find_element_by_css_selector('.race_tab')
                        items['レース番号'] = elm.find_element_by_css_selector('thead').text.split('(')[0].strip()
                    except:
                        er_msg('レース番号')
                    # -------------------------
                    # レース格 / 距離
                    # -------------------------
                    try:
                        el = elm.find_element_by_css_selector('tbody tr:nth-of-type(2) td:nth-of-type(1)').text.strip()
                        items['レース格'] = el.split('-')[0].strip()
                        items['距離'] = el.split('-')[1].strip()
                    except:
                        er_msg('レース格 / 競馬場')
                    # -------------------------
                    # 馬場状態
                    # -------------------------
                    try:
                        items['馬場状態'] = elm.find_element_by_css_selector('tbody tr:nth-of-type(2) td:nth-of-type(3)').text.split('(')[0].strip()
                    except:
                        er_msg('馬場状態')
                    # -------------------------
                    # レース名
                    # -------------------------
                    try:
                        items['レース名'] = elm.find_element_by_css_selector('tbody tr:nth-of-type(3) td').text.strip()
                    except:
                        er_msg('レース名')
                    # -------------------------
                    # 馬場
                    # -------------------------
                    try:
                        items['馬場'] = elm.find_element_by_css_selector('tbody tr:nth-of-type(3) td:nth-of-type(3)').text.split('-')[0].strip()
                    except:
                        er_msg('馬場')
                    # -------------------------
                    # 総賞金
                    # -------------------------
                    try:
                        items['総賞金'] = elm.find_element_by_css_selector('tbody tr:nth-of-type(4) td').text.strip()
                    except:
                        er_msg('総賞金')
                    # -------------------------
                    # 通過タイム
                    # -------------------------
                    try:
                        race_past = []
                        race_info = elm.find_element_by_css_selector('tbody tr:nth-of-type(4)').text.split('Time :')[1].strip().split(' ')
                        for ii in range(len(race_info)):
                            race_info[ii]
                        for ii in race_info:
                            ii = ii.replace('(','').replace(')','').strip()
                            race_past.append(ii)
                        # Finishタイム
                        last = race_past[-1]
                        # race_pastからFinishタイムを削除
                        race_past[-1] = ''
                        for ii in range(4):
                            race_past.append('')
                        items['通過タイム'] = race_past
                    except:
                        er_msg('通過タイム')
                    # -------------------------
                    # Finishタイム
                    # -------------------------
                    try:
                        items['Finishタイム'] = last
                    except:
                        er_msg('Finishタイム')
                    # -------------------------
                    # レースSectionalタイム
                    # -------------------------
                    race_time_sub = ['','','','']
                    try:
                        race_time = elm.find_elements_by_css_selector('tbody tr:nth-of-type(5) td')
                        race_time = race_time[2::]
                        race_time = [x.text.strip() for x in race_time]
                        arr = []
                        if len(race_time) > 0:
                            for ii in range(len(race_time)):
                                if '\n' in race_time[ii]:
                                    arr.append(race_time[ii].split('\n')[1].strip().split(' ')[0])
                                    arr.append(race_time[ii].split('\n')[1].strip().split(' ')[-1])
                                    race_time[ii] = race_time[ii].split('\n')[0]
                            if(len(arr) == 4):
                                race_time_sub = arr
                            for ii in range(5):
                                race_time.append('')
                            items['レースSecタイム'] = race_time
                        else:
                            items['レースSecタイム'] = ['','','','','','','','','','']
                    except:
                         er_msg('レースSecタイム')
                    # -------------------------
                    # Sectional
                    # -------------------------
                    try:
                        items['Sectional'] = driver.find_element_by_css_selector('.sectional_time_btn a').get_attribute('href')
                    except:
                         er_msg('Sectional')
                    # -------------------------
                    # video
                    # -------------------------
                    try:
                        items['video'] = elm.find_element_by_css_selector('.icon_link a').get_attribute('href')
                    except:
                         er_msg('video')
                    # -------------------------
                    # 競馬場コード
                    # -------------------------
                    try:
                         items['競馬場コード'] = raceCount[i].split('Racecourse=')[1].split('&')[0].strip()
                    except:
                        er_msg('競馬場コード')
                    ##############################
                    # テーブル
                    ##############################
                    table = driver.find_element_by_css_selector('.performance table')
                    def tbCell(target):
                        elm = table.find_elements_by_css_selector(target)
                        elm = [x.text.strip() for x in elm]
                        return elm
                    def erArry():
                        arr = []
                        for ii in range(items['出走頭数']):
                            arr.append('')
                        return arr
                    ##############################
                    # 確定順位 / 同着
                    try:
                        arr = []
                        items['確定順位'] = tbCell('tbody tr td:nth-of-type(1)')
                        for ii in range(len(items['確定順位'])):
                            if 'DH' in items['確定順位'][ii]:
                                items['確定順位'][ii] = items['確定順位'][ii].split('DH')[0].strip()
                                arr.append('dht')
                            else:
                                arr.append('')
                        items['同着'] = arr
                    except:
                        er_msg('確定順位／同着')
                        items['確定順位'] = erArry()
                        items['同着'] = erArry()
                    # 出走頭数
                    items['出走頭数'] = len(items['確定順位'])
                    minN = 0
                    # 異常区分
                    try:
                        arr = []
                        for ii in items['確定順位']:
                            if ii in excCount01:
                            #if ii == 'DNF' or ii == 'FE' or ii == 'U' \
                            #or ii == 'TNP' or ii == 'UR' or ii == 'PU':
                                arr.append('94')
                            elif ii == 'DISQ':
                                arr.append('95')
                            elif ii in excCount02:
                            #elif ii == 'WR' or ii == 'WV' or ii == 'WV-A' \
                            #or ii == 'WX' or ii == 'WX-A' or ii == 'WXNR':
                                arr.append('96')
                                minN = minN + 1
                            elif ii == 'VOID':
                                arr.append('101')
                                minN = minN + 1
                            else:
                                arr.append('')
                        items['異常区分'] = arr
                    except:
                        er_msg('異常区分')
                        items['異常区分'] = erArry()
                    # 馬番号
                    try:
                        items['馬番号'] = tbCell('tbody tr td:nth-of-type(2)')
                    except:
                        er_msg('馬番号')
                        items['馬番号'] = erArry()
                    # 馬名 / 馬ID
                    try:
                        elm = tbCell('tbody tr td:nth-of-type(3)')
                        items['馬名'] = [x.split('(')[0].strip() for x in elm]
                        items['馬ID'] = [x.split('(')[1].split(')')[0].strip() for x in elm]
                    except:
                        er_msg('馬名')
                        er_msg('馬ID')
                    # 騎手
                    try:
                        items['騎手'] = tbCell('tbody tr td:nth-of-type(4)')
                    except:
                        er_msg('騎手')
                        items['騎手'] = erArry()
                    # 調教師
                    try:
                        items['調教師'] = tbCell('tbody tr td:nth-of-type(5)')
                    except:
                        er_msg('調教師')
                        items['調教師'] = erArry()
                    # 斤量
                    try:
                        items['斤量'] = tbCell('tbody tr td:nth-of-type(6)')
                    except:
                        er_msg('斤量')
                        items['斤量'] = erArry()
                    # 馬体重
                    try:
                        items['馬体重'] = tbCell('tbody tr td:nth-of-type(7)')
                    except:
                        er_msg('馬体重')
                        items['馬体重'] = erArry()
                    # ゲート番号
                    try:
                        items['ゲート番号'] = tbCell('tbody tr td:nth-of-type(8)')
                    except:
                        er_msg('ゲート番号')
                        items['ゲート番号'] = erArry()
                    # 着差
                    try:
                        items['着差'] = tbCell('tbody tr td:nth-of-type(9)')
                    except:
                        er_msg('着差')
                        items['着差'] = erArry()
                    # 通過順位 / 入線順位
                    try:
                        TDflg = table.find_element_by_css_selector('thead tr td:nth-of-type(10)').text.strip()
                        if 'Running' in TDflg:
                            inNum = []
                            elm = table.find_elements_by_css_selector('tbody tr td:nth-of-type(10)')
                            for ii in range(len(elm)):
                                if '---' == elm[ii].text.strip():
                                    elm[ii] = ['','','','','','']
                                    inNum.append('')
                                else:
                                    elm[ii] = elm[ii].find_elements_by_css_selector('div div')
                                    elm[ii] = [x.text.strip() for x in elm[ii]]
                                    for iii in range(len(elm[ii])):
                                        if elm[ii][iii] == '':
                                            elm[ii][iii] = '-'
                                        else:
                                            pass
                                    inNum.append(elm[ii][-1])
                                    del elm[ii][0]
                                    del elm[ii][-1]
                                    ap = ['','','','','']
                                    elm[ii].extend(ap)
                            items['通過順位'] = elm
                            items['入線順位'] = inNum
                        else:
                                    for ii in range(items['出走頭数']):
                                        items['通過順位'].append(['','','','',''])
                                        items['入線順位'] = erArry()
                    except:
                        er_msg('通過順位 / 入線着順')
                        for ii in range(items['出走頭数']):
                            items['通過順位'].append(['','','','',''])
                            items['入線順位'] = erArry()
                    # 着変更
                    try:
                        arr = []
                        for ii in range(len(items['入線順位'])):
                            if items['入線順位'][ii] == items['確定順位'][ii]:
                                arr.append('')
                            else:
                                try:
                                    if items['異常区分'][ii] == '95' or int(items['入線順位'][ii]) < int(items['確定順位'][ii]):
                                        arr.append('*')
                                    else:
                                        arr.append('')
                                except:
                                    arr.append('')
                        items['着変更'] = arr
                    except:
                        er_msg('着変更')
                        items['着変更'] = erArry()
                    # 入線タイム
                    try:
                        items['入線タイム'] = tbCell('tbody tr td:nth-of-type(11)')
                        if len(items['入線タイム']) == 0:
                            items['入線タイム'] = erArry()
                    except:
                        er_msg('入線タイム')
                        items['入線タイム'] = erArry()
                    # オッズ
                    try:
                        items['オッズ'] = tbCell('tbody tr td:nth-of-type(12)')
                        if len(items['オッズ']) == 0:
                            items['オッズ'] = erArry()
                    except:
                        er_msg('オッズ')
                        items['オッズ'] = erArry()
                    # コメント
                    try:
                        items['コメント'] = driver.find_element_by_css_selector('.info_p').text.strip()
                    except:
                        er_msg('コメント')
                        items['コメント'] = ''
                    secItem = {\
                        '馬別':[],\
                        '馬別内訳':[]\
                    }
                    try:
                        # セクショナルタイムに遷移
                        driver.get(items['Sectional'])
                        driver.implicitly_wait(5)
                        try:
                            trs = driver.find_elements_by_css_selector('.race_table tbody tr')
                            if len(trs) > 0:
                                for ii in range(len(trs)):
                                    secTime = []
                                    secTimeSub = []
                                    tds = trs[ii].find_elements_by_css_selector('td')
                                    tds = tds[3:9]
                                    tds = [x.text.strip().split('\n')[-1] for x in tds]
                                    for iii in range(len(tds)):
                                        if ' ' in tds[iii]:
                                            arr = tds[iii].split(' ')
                                            arr = [x for x in arr if x != '']
                                            secTime.append(arr[0])
                                            secTimeSub.append(arr[1])
                                            secTimeSub.append(arr[2])
                                        else:
                                            secTime.append(tds[iii])
                                    if len(secTimeSub) < 4:
                                        secTimeSub = ['','','','']
                                    secItem['馬別'].append(secTime)
                                    secItem['馬別内訳'].append(secTimeSub)
                            else:
                                for ii in range(items['出走頭数']):
                                    secItem['馬別'].append(['','','','','',''])
                                    secItem['馬別内訳'].append(['','','',''])
                        except:
                            for ii in range(items['出走頭数']):
                                secItem['馬別'].append(['','','','','',''])
                                secItem['馬別内訳'].append(['','','',''])
                    except:
                        for ii in range(items['出走頭数']):
                            secItem['馬別'].append(['','','','','',''])
                            secItem['馬別内訳'].append(['','','',''])
                    for ii in range(items['出走頭数']):
                        body_iv = [\
                            '32',items['競馬場コード'],items['競馬場'],items['国名'],items['日付'],items['Date_L'],items['video'],\
                            items['Sectional'],items['レース名'],items['レース格'],items['レース番号'],'','','',items['馬場'],\
                            '','','','','',items['距離'],'','',items['馬場状態'],items['総賞金'],'',items['通過タイム'][0],\
                            items['通過タイム'][1],items['通過タイム'][2],items['通過タイム'][3],items['通過タイム'][4],\
                            items['Finishタイム'],items['レースSecタイム'][0],items['レースSecタイム'][1],items['レースSecタイム'][2],\
                            items['レースSecタイム'][3],items['レースSecタイム'][4],items['レースSecタイム'][5],\
                            race_time_sub[0],race_time_sub[1],race_time_sub[2],race_time_sub[3],\
                            secItem['馬別'][ii][0],secItem['馬別'][ii][1],secItem['馬別'][ii][2],secItem['馬別'][ii][3],\
                            secItem['馬別'][ii][4],secItem['馬別'][ii][5],secItem['馬別内訳'][ii][0],secItem['馬別内訳'][ii][1],\
                            secItem['馬別内訳'][ii][2],secItem['馬別内訳'][ii][3],\
                            items['通過順位'][ii][0],items['通過順位'][ii][1],items['通過順位'][ii][2],items['通過順位'][ii][3],\
                            items['通過順位'][ii][4],items['入線順位'][ii],items['確定順位'][ii],items['異常区分'][ii],items['同着'][ii],\
                            items['着変更'][ii],items['馬番号'][ii],items['ゲート番号'][ii],items['着差'][ii],\
                            '',items['馬名'][ii],items['馬ID'][ii],'',items['オッズ'][ii],'',\
                            items['馬体重'][ii],items['斤量'][ii],'','','',items['調教師'][ii],items['騎手'][ii],'','','','','',\
                            items['出走頭数'] - minN,items['入線タイム'][ii],'','',items['コメント']\
                            ]
                        print(body_iv)
                        writer.writerow(body_iv)
                except:
                    pass
        except:
            pass
driver.quit()
##終了時刻をエポック秒で取得（処理時間の計算用）
e_time = time.time()
p_time = e_time - s_time
##処理時間の表示
print('処理時間（秒）: ' + str(p_time))
sys.exit()