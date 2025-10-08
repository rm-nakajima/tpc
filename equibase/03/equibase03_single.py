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
import sys

##############################
# targets.txt
##############################
targets = []
try:
    f = open('targets.txt', 'r', encoding='UTF-8')
    targetUrl = f.read()
    if '\n' in targetUrl:
        targets = targetUrl.split('\n')
    else:
        targets.append(targetUrl.strip())
except:
    targets = []
print(str(targets))
##############################
# save.txt
##############################
try:
    f = open('save.txt', 'r', encoding='UTF-8')
    savePath = f.read()
    savePath = savePath.split('\n')[0]
    savePath = savePath + '/'
    savePath = savePath.replace('//','/')
except:
    savePath = ''
print('Save Path: ' + str(savePath))
############################
# 今日の日付（ファイル名に使用）
############################
dateToday = datetime.datetime.now().strftime("%Y%m%d")
############################
# function
############################
# 待機時間用の乱数を生成（2〜5秒）
def ranCount01():
    return random.randint(2, 5)
# 待機時間用の乱数を生成（6〜10秒）
def ranCount02():
    return random.randint(6, 10)
# CAPTCHA判別
def captha_check():
    # ページ内のID「contentwrapper」要素を検索
    judg = driver.find_elements_by_css_selector('#contentwrapper')
    judg = len(judg)
    # 検索した要素があれば次の処理に進む
    if judg > 0:
        pass
    # 検索した要素が無ければCHAPTCHA画面と判定し、
    # 解除までの待機時間を設ける
    else:
        try:
            loopCount = 1
            while(judg != 1):
                print('CAPTCHA認証中')
                ## 30秒待機後、再度検索
                time.sleep(30)
                judg = driver.find_elements_by_css_selector('#contentwrapper')
                judg = len(judg)
                loopCount = loopCount + 1
                # 上記処理を最大10回（最大300秒）まで繰り返す
                if loopCount > 10:
                    break
                else:
                    pass
        except:
            # 300秒後も「contentwrapper」要素が見つからなければ処理を強制終了
            driver.quit()
            sys.exit( )
# エラーログ処理
def err_log(e):
    fErr = open(logFileName, 'a', encoding="utf_8_sig")
    fErr.write('エラー発生URL: ' + str(driver.current_url))
    fErr.write('\n' + e + '\n')
    print(e)
############################
# STEP.1
############################
##Chromeを起動
option = Options()
option.add_argument('--incognito')
driver = webdriver.Chrome(options=option)
driver.set_window_size(1400,1000)

############################
# STEP.2
############################
# 抽出データを出力するためのCSVを作成
FileName = savePath + 'equibase03_single_' + str(dateToday) + '.csv'
logFileName = savePath + 'Err_equibase03_single' + str(dateToday) + ".txt"
f = open(FileName, 'w', encoding="utf_8_sig")
writer = csv.writer(f, lineterminator='\n')

# CSVの一行目に各見出しを出力
label = ['競馬場','開催日','レースNo','レース名','レース格','発走時刻','距離','芝orダートorAW','補欠馬','P#','PP','Horse','A','S','血統情報（父）','血統情報（母）','血統情報（母の父）','URL','Track_URL']
writer.writerow(label)

############################
# STEP.4
############################
for s in range(len(targets)):

    ##対象ページに遷移
    driver.get(targets[s])
    #######CAPTCH判定#####
    captha_check()
    #######CAPTCH判定#####
    # 現在のURL
    curURL = [driver.current_url]
    # Track URL
    trURL = ['?' + driver.find_element_by_css_selector('.track-name').get_attribute('href').rsplit('?')[-1].strip()]

    # 競馬場を取得
    try:
        trackName = driver.find_element_by_css_selector('.track-name').text
    except:
        err_log('競馬場 取得エラー')
        trackName = ''

    # 日付を取得して書式を変換
    try:
        raceDate = driver.find_element_by_css_selector('.race-date').text
        raceDate = raceDate.replace('January','Jan').replace('February','Feb').replace('March','Mar')\
            .replace('April','Apr').replace('May','May').replace('June','Jun').replace('July','Jul')\
                .replace('August','Aug').replace('September','Sep').replace('October','Oct')\
                    .replace('November','Nov').replace('December','Dec')
        raceDate = datetime.datetime.strptime(raceDate, '%b %d, %Y').strftime('%Y/%m/%d')
    except:
        err_log('日付 取得エラー')
        raceDate = ''

    # 各レースごとの要素をリストで取得
    try:
        raceBlock = driver.find_elements_by_css_selector('.entryRace')
    except:
        err_log('個別レース 取得エラー')
        raceBlock = []

    # レースの数だけ繰り返し処理
    for l in range(len(raceBlock)):
        # レースNo,レース名,レース格,発走時刻を取得
        try:
           raceTitle = raceBlock[l].find_element_by_css_selector('h4')
        except:
            err_log('レース見出し 取得エラー')
            raceTitle = ''
        # レースNo, 発走時刻, レース格
        try:
            raceLabel = raceTitle.find_elements_by_css_selector('span')
            raceLabel = [x.text for x in raceLabel]
            raceNum = ''
            raceTime = ''
            raceGrade = ''
            for i in range(len(raceLabel)):
                # レースNo
                if re.search('RACE ', raceLabel[i]):
                    raceNum = raceLabel[i].replace('-','').strip()
                # 発走時刻
                elif re.search('POST TIME', raceLabel[i]):
                    raceTime = raceLabel[i].split('-')[1].strip()
                elif re.search('POST Time', raceLabel[i]):
                    raceTime = raceLabel[i].split('-')[1].strip()
                elif re.search('\(Grade ', raceLabel[i]):
                    raceGrade = raceLabel[i].split('(Grade ')[1].split(')')[0].strip()
                    raceGrade = 'Grade ' + raceGrade
                elif re.search('\(GRADE ', raceLabel[i]):
                    raceGrade = raceLabel[i].split('(GRADE')[1].split(')')[0].strip()
                    raceGrade = raceGrade.replace('III','3').replace('II','2').replace('I','1')
                    raceGrade = 'LG' + raceGrade
                else:
                    pass
        except:
            err_log('レースNo. or 発走時刻 or レース格 取得エラー')
        # レース名
        try:
            raceName = raceTitle.find_element_by_css_selector('.raceNameLink').text
        except:
            try:
                 for i in range(len(raceLabel)):
                    if re.search('POST TIME',raceLabel[i]) or re.search('RACE \d+',raceLabel[i]):
                         pass
                    else:
                        raceName = raceLabel[i]
                        if '(Grade ' in raceName:
                            raceName = raceName.split('(Grade')[0]
                        elif '(GRADE ' in raceName:
                            raceName = raceName.split('(GRADE')[0]
                        raceName = raceName.strip()

            except:
                raceName = ''


        # 距離と馬場種類
        try:
            raceInfo = raceBlock[l].find_element_by_css_selector('.race-info .entries-race-conditions .conditions-text').text
            raceInfo01 = raceInfo.split('.')[1].strip()
            try:
                raceInfo02 = raceInfo.split('.',1)[1].split('(')[1].split(')')[0].strip()
            except:
                raceInfo02 = raceInfo.split('.',1)[1].strip()
            if 'All Weather Track' in raceInfo02:
                raceInfo02 = 'All Weather'
            elif 'Downhill turf' in raceInfo02 or 'Turf Rail at' in raceInfo02 or 'Inner turf' in raceInfo02 or 'Outer turf' in raceInfo02 or 'Turf' in raceInfo02:
                raceInfo02 = 'Turf'
            elif 'Hurdle' in raceInfo02:
                raceInfo02 = 'Hurdle'
            elif 'Timber' in raceInfo02:
                raceInfo02 = 'Timber'
            else:
                raceInfo02 = 'Dirt'
        except:
            err_log('距離と馬場種類 取得エラー')
            raceInfo01 = ''
            raceInfo02 = ''

        # レースのテーブル表（ヘッダー部）を取得して精査
        try:
            race_info_head = raceBlock[l].find_elements_by_css_selector('table thead tr th')
            race_info_head = [x.text for x in race_info_head]
            # 一番最初のラベルが「P#」の場合
            if race_info_head[0] == 'P#':
                del race_info_head[5:] # ラベルの5列目以降を削除
                del race_info_head[3] # ラベルの3列目を削除
            # 一番最初のラベルが「PP」の場合
            elif race_info_head[0] == 'PP':
                del race_info_head[4:] # ラベルの4列目以降を削除
                del race_info_head[2] # ラベルの2列目を削除
            # いずれも「Med」以降と「Virtual Stable」を削除の想定
            else:
                err_log('レース表のヘッダー 取得エラー')
        except:
            err_log('レース表のヘッダー 取得エラー')

        # レースのテーブル表（ボディー部）を列ごとに取得
        try:
            race_info_table = raceBlock[l].find_elements_by_css_selector('table tbody tr')
        except:
            err_log('レース表のテーブル 取得エラー')


        # 補欠馬表記が何列目にあるかを照合
        alsoCheckList = []
        try:
            for i in range(len(race_info_table)):
                # レコードの1列目を取得
                alsoCheck = race_info_table[i].find_elements_by_css_selector('td:nth-of-type(1)')
                alsoCheck =[x.text for x in alsoCheck]
                for z in range(len(alsoCheck)):
                    # レコードの1列目が「Also Eligibles」の場合
                    if re.search('Also Eligibles', alsoCheck[z]):
                        alsoCheckList.append('0') # 照合リストに「0」を追加
                    # レコードの1列目が「Also Eligibles」以外の場合
                    else:
                        alsoCheckList.append('1')  # 照合リストに「1」を追加
            # 照合リストに「0」が含まれる = レース表内に補欠馬表記が存在する場合
            if '0' in alsoCheckList:
                alsoCheck = alsoCheckList.index('0')
                del race_info_table[alsoCheck]
            else:
                alsoCheck = 9999
        except:
            pass

        # テーブルのボディー部から必要な情報を精査
        for i in range(len(race_info_table)):
            race_info_tbody = race_info_table[i].find_elements_by_css_selector('td')
            race_info_tbody = [x.text.strip() for x in race_info_tbody]

            if i >= alsoCheck:
                race_info_tbody.insert(0, 'Also Eligibles')
            else:
                race_info_tbody.insert(0, '')

            if race_info_tbody[1] == 'SCR':
                race_info_tbody.insert(2, '')

            if race_info_head[0] == 'PP':
                race_info_tbody.insert(0,'')
            del race_info_tbody[6:]
            del race_info_tbody[4]

            ##年齢/性別
            try:
                if race_info_tbody[1] == 'SCR':
                    h_age = race_info_tbody[3].split('/')[0]
                    h_sex = race_info_tbody[3].split('/')[1]
                else:
                    h_age = race_info_tbody[4].split('/')[0]
                    h_sex = race_info_tbody[4].split('/')[1]
            except:
                h_age = ''
                h_sex = ''

            race_info_tbody[4] = h_age
            race_info_tbody.append(h_sex)

            ##血統情報
            try:
                h_data_ttl = race_info_table[i].find_element_by_css_selector('td b a').get_attribute('data-original-title')
                h_data_ttl = h_data_ttl.split(' - ')
                h_data_ttl_s = h_data_ttl[0].strip()
                if re.match('\(', h_data_ttl_s):
                    h_data_ttl_s = h_data_ttl_s.replace('(','',1)
                h_data_ttl_m = h_data_ttl[1].split(',')[0].strip()
                h_data_ttl_d = h_data_ttl[1].split(',')[1]
                if re.match(' by ', h_data_ttl_d):
                    h_data_ttl_d = h_data_ttl_d.split('by',1)[1].strip()
                if re.search('\(', h_data_ttl_d):
                    h_data_ttl_d = h_data_ttl_d.replace(')','',1)
                else:
                    h_data_ttl_d = h_data_ttl_d.replace(')','')
                race_info_tbody.append(h_data_ttl_s)
                race_info_tbody.append(h_data_ttl_m)
                race_info_tbody.append(h_data_ttl_d)
            except:
                race_info_tbody.append('')


            record = [str(trackName),str(raceDate),str(raceNum),str(raceName),str(raceGrade),str(raceTime),str(raceInfo01),str(raceInfo02)]
            writer.writerow(record + race_info_tbody + curURL + trURL)
            print(record + race_info_tbody)

driver.quit()
sys.exit()