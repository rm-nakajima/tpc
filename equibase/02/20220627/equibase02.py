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
# save.txt
##############################
# 保存先の設定ファイル
try:
    f = open('save.txt', 'r', encoding='UTF-8')
    savePath = f.read()
    savePath = savePath.split('\n')[0]
    savePath = savePath + '/'
    savePath = savePath.replace('//','/')
except:
    savePath = ''
print('Save Path: ' + str(savePath))
##############################
#targets.txt
##############################
f = open('targets.txt', 'r', encoding='UTF-8')
targetHorses = f.read().split('\n')
targetHorses = [x for x in targetHorses if x != '']
##############################
# usa_race-case.txt
##############################
# レース格の設定ファイル
raceCase_f = open('usa_race-case.txt', 'r', encoding='UTF-8')
race_C_type = raceCase_f.read()
race_C_type = race_C_type.split('\n')
race_C_type = [x for x in race_C_type if x != '']
##############################
# usa_race-case-other.txt
##############################
# 出走条件（その他）の設定ファイル
raceType_f = open('usa_race-case-other.txt', 'r', encoding='UTF-8')
race_T_type = raceType_f.read()
race_T_type = race_T_type.split('\n')
race_T_type = [x for x in race_T_type if x != '']
############################
# 今日の日付（ファイル名に使用）
############################
# 現在の時刻含む日付
output_date = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
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
# 「Today」と「Tomorrow」のリンクを取得
# 繰り返し処理時に使用
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
# Chromeを起動
option = Options()
option.add_argument('--incognito')
driver = webdriver.Chrome(options=option)
for s in range(len(targetHorses)):
    # 対象ページに遷移
    driver.get(targetHorses[s])
    # 現在のURLを取得
    c_url = driver.current_url
    # CAPTCHA判定
    captha_check()

    # 馬名、生産国
    try:
        h_name_row = driver.find_element_by_css_selector('.horse-name-header').text.strip()
        h_name = h_name_row
        h_origin = ''
        if '(' in h_name:
            h_name = h_name_row.split('(')[0].strip()
            h_origin = h_name_row.split('(')[1]
            h_origin = '(' + h_origin
    except:
        err_log('馬名・生産国 取得エラー')
        h_name = ''
        h_origin = ''

    # 馬種、毛色、性、生年月日
    try:
        h_info01 = driver.find_element_by_css_selector('.horse-profile-top-bar-headings').text
        h_infoElem01 = h_info01.split(',')
        # 毛色
        h_color = h_infoElem01[1].strip()
        # 性
        h_sex = h_infoElem01[2].strip()
        # 生年月日
        h_birth = h_infoElem01[3].strip().split(' ',1)[1]
        h_birth = h_infoElem01[4] + h_birth
        # 生年月日を成形
        h_birth = h_birth.replace('JANUARY','/1/').replace('FEBRUARY','/2/').replace('MARCH','/3/')\
            .replace('APRIL','/4/').replace('MAY ','/5/').replace('JUNE','/6/')\
                .replace('JULY','/7/').replace('AUGUST','/8/').replace('SEPTEMBER','/9/')\
                    .replace('OCTOBER','/10/').replace('NOVEMBER','/11/').replace('DECEMBER','/12/')
        h_birth = h_birth.replace(' ','').strip()
    except:
        err_log('馬種・毛色・性・生年月日 取得エラー')
        h_info = ''
        h_color = ''
        h_sex = ''
        h_birth = ''

    # 生年月日から馬齢を算出して成形
    try:
        # 現在時刻から西暦を生成
        b_data = output_date.split('/',1)[0]
        b_data = int(b_data)
        # 生年を抽出
        c_data = h_birth.split('/',1)[0]
        c_data = int(c_data)
        # 現年 - 生年
        h_age = b_data - c_data
        h_age = str(h_age) + 'yo'
    except:
        err_log('馬齢 取得エラー')
        h_age = ''

    # 血統
    try:
        h_info02 = driver.find_element_by_css_selector('.horse-profile-top-bar-headings:nth-of-type(2)').text
        h_infoElem02 = h_info02.split('-')
        # 父馬
        h_sire = h_infoElem02[0].replace('( ','').strip()
        # 母馬
        h_dam = h_infoElem02[1].split(',')[0].strip()
        # 母父馬
        h_damsire = h_infoElem02[1].split(',')[1].replace('BY ','',1).replace(' )','').strip()
    except:
        err_log('父馬・母馬・母父馬 取得エラー')
        h_sire = ''
        h_dam = ''
        h_damsire = ''

    # 調教師、オーナー、生産者
    try:
        h_relation = driver.find_element_by_css_selector('.horse-profile-top-bar-para').text
        h_relation = h_relation.strip().split('\n')
        h_trainer = ''
        h_owner = ''
        h_breeder = ''
        for i in range(len(h_relation)):
            # 調教師
            if 'Trainer:' in h_relation[i]:
                h_trainer = h_relation[i].split(':')[1].strip()
            # オーナー
            if 'Owner:' in h_relation[i]:
                h_owner = h_relation[i].split(':')[1].strip()
            # 生産者
            if 'Breeder:' in h_relation[i]:
                h_breeder = h_relation[i].split(':')[1].strip()
    except:
        err_log('調教師・オーナー・生産者 取得エラー')

    # 「Results」タブをクリック
    try:
        driver.find_element_by_css_selector('#Hresults').click()
    except:
        try:
            driver.find_element_by_css_selector('.tab-group profile-tab-group li:nth-of-type(3)').click()
        except:
            err_log('Results クリックエラー')

    # 通算出走回数
    try:
        h_results = driver.find_elements_by_css_selector('#results table.results tbody tr')
        r_count = len(h_results)
    except:
        r_count = 0
        err_log('通算出走回数 取得エラー')

    # 成績統計
    try:
        h_score = driver.find_elements_by_css_selector('#horseProfileInfo table.table-compressed')
        if len(h_score) < 2:
            # Current Year Score
            CurrScore = ['0','0','0','0','0']
            # Carrier Score
            CarrScore = h_score[0].find_elements_by_css_selector('tbody tr td')
            CarrScore = [x.text for x in CarrScore]
        elif len(h_score) > 1:
            # Current Year Score
            CurrScore = h_score[0].find_elements_by_css_selector('tbody tr td')
            CurrScore = [x.text for x in CurrScore]
            # Carrier Score
            CarrScore = h_score[1].find_elements_by_css_selector('tbody tr td')
            CarrScore = [x.text for x in CarrScore]
    except:
        err_log('成績統計 取得エラー')
        CurrScore = ['','','','','']
        CarrScore = ['','','','','']

    # 抽出データを出力するためのCSVを作成
    FileName = savePath + 'equibase02_' + h_name.replace(' ','-') + '.csv'
    logFileName = savePath + 'Err_equibase02_' + h_name.replace(' ','-') + ".txt"
    f = open(FileName, 'w', encoding="utf_8_sig")
    writer = csv.writer(f, lineterminator='\n')

    # CSVの一行目に各見出しを出力
    label = ['ID','Horse_name','b','age','c_s','birthday','color','sex','Trainer','Owner','Sire','Dam','Damsire','Breeder','Races_Count','Stats','Starts','Firsts','Seconds','Thirds','EARNINGS','URL','scrape_date']
    writer.writerow(label)

    # CSVの二行目に出力
    record01 = ['11',h_name,h_origin,h_age,h_info01,h_birth,h_color,h_sex,h_trainer,h_owner,h_sire,h_dam,h_damsire,h_breeder,r_count,'Current year'] + CurrScore + [c_url,output_date]
    writer.writerow(record01)
    print(record01)
    # CSVの三行目に出力
    record02 =['12','','','','','','','','','','','','','','','Carrier'] + CarrScore
    writer.writerow(record02)
    # 空行を設ける
    writer.writerow(['18'])

    label02 = ['21','Date','競馬場コード','競馬場','国名','Date_L','Race','Race Type','レース格','出走条件（その他）','Finish']
    writer.writerow(label02)
    # 出走回数の分だけ繰り返し処理
    for i in range(r_count):
        # 競馬場、競馬場コード、国名
        try:
            rc_track = h_results[i].find_element_by_css_selector('td.track')
            rc_name = rc_track.text
            try:
                rc_track = rc_track.find_element_by_css_selector('a').get_attribute('href')
                rc_code = rc_track.split('&trk=')[1].split('&cy=')[0].strip()
                try:
                    rc_country = rc_track.split('&cy=')[1]
                except:
                    rc_country = ''
            except:
                rc_code = ''
                rc_country = ''
        except:
            err_log('競馬場 取得エラー')
            rc_name = ''
            rc_code = ''
            rc_country = ''

        # 日付
        try:
            rc_b_date = h_results[i].find_element_by_css_selector('td.date').text.strip()
            rc_b_date = rc_b_date.split('/')
            rc_date = rc_b_date[2] + '/' + rc_b_date[0] + '/' + rc_b_date[1]
        except:
            err_log('日付 取得エラー')
            rc_date = ''

        # レース番号
        try:
            r_num = h_results[i].find_element_by_css_selector('td.race').text.strip()
        except:
            err_log('レース番号 取得エラー')
            r_num = ''

        # レース名、レース格、出走条件
        r_class = []
        r_other = []
        try:
            r_type = h_results[i].find_element_by_css_selector('td.type').text.strip()
            try:
                for c in range(len(race_C_type)):
                    if race_C_type[c] in r_type:
                        r_classElem = race_C_type[c].replace('(','').replace(')','').strip()
                        r_class.append(r_classElem)
                r_class = r_class[0]
            except:
                r_class = ''

            try:
                for c in range(len(race_T_type)):
                    if race_T_type[c] in r_type:
                        r_other.append(race_T_type[c])
                r_other = r_other[0]
            except:
                r_other = ''
        except:
            err_log('レース名、レース格、出走条件（その他） 取得エラー')
            r_type = ''

        # 確定着順
        try:
            rankNum = h_results[i].find_element_by_css_selector('td.finish').text.strip()
        except:
            err_log('確定着順 取得エラー')
            rankNum = ''

        #PDFリンク
        try:
            c_link = h_results[i].find_element_by_css_selector('td.chart')
            try:
                c_link = c_link.find_element_by_css_selector('a').get_attribute('href')
            except:
                c_link = ''
        except:
            c_link = ''

        rc_record = ['22',rc_date,rc_code,rc_name,rc_country,c_link,r_num,r_type,r_class,r_other,rankNum]
        writer.writerow(rc_record)
    time.sleep(ranCount02())
    f.close()
driver.quit()