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
from bs4 import BeautifulSoup
import requests

##targets.csvファイルから検索対象のURLをインポート
targets = []
with open('./Bitbacket/scraping/emiratesracing/targets.csv', newline='', encoding='utf-8-sig') as csvfile:
    rows = csv.reader(csvfile, delimiter=',', quotechar='|')
    reader = csv.reader(csvfile)
    for row in reader:
        ##取得した馬名をリストに格納
        targets.append(row[0])
csvfile.close()
print('対象URL')
print(targets)
print('\n')

##今日の日付（生成するCSVファイル名に使用）
dateToday = datetime.datetime.now().strftime("%Y%m%d")

option = Options()
option.add_argument('--incognito')
driver = webdriver.Chrome(options=option)

##対象リストの要素数だけ繰り返し処理
for s in range(len(targets)):

    ##対象ページに遷移
    driver.get(targets[s])
    driver.implicitly_wait(5)

    ##馬名（生産国）
    try:
        h_name = driver.find_element_by_css_selector('h1').text
        print('馬名（生産国）: ' + h_name)
    except:
        print('h_name ERROR')

    ##馬齢
    try:
        h_age = driver.find_element_by_css_selector('.horseDetails:nth-of-type(1)').text
        print('馬齢: ' + h_age)
    except:
        print('h_age ERROR')

    ##毛色
    try:
        h_color = driver.find_element_by_css_selector('.horseDetails:nth-of-type(2)').text
        print('毛色: ' + h_color)
    except:
        print('h_color ERROR')

    ##性別
    try:
        h_gender = driver.find_element_by_css_selector('.horseDetails:nth-of-type(3)').text
        print('性別: ' + h_gender)
    except:
        print('h_gender ERROR')

    ##父、母、母父名
    try:
        h_Pedigree = driver.find_element_by_css_selector('.horseInfo p:nth-of-type(2)').text
        print('父、母、母父名: ' + h_Pedigree)
    except:
        print('h_Pedigree ERROR')

    ##オーナー
    try:
        h_owner = driver.find_element_by_css_selector('.horseInfo p:nth-of-type(3) a').text
        print('オーナー: ' + h_owner)
    except:
        print('h_owner ERROR')

    ##生産者
    try:
        h_breeder = driver.find_element_by_css_selector('.horseInfo p:nth-of-type(4)').text
        h_breeder = h_breeder.replace('Breeder:','')
        print('生産者: ' + h_breeder)
    except:
        print('h_breeder ERROR')

    ##調教師
    try:
        h_trainer = driver.find_element_by_css_selector('.horseInfo p:nth-of-type(5) a').text
        print('調教師: ' + h_trainer)
    except:
        print('h_trainer ERROR')

    ##出走回数
    try:
        h_value = driver.find_elements_by_css_selector('.formTable:first-child tbody tr')
        print('出走回数: ' + str(len(h_value)))
    except:
        print('h_value ERROR')

    ############################
    ##     CSV生成
    ############################
    genFileName = './Desktop/' + h_name + '_' + dateToday + ".csv"
    f = open(genFileName, 'w', encoding="utf_8_sig")
    writer = csv.writer(f, lineterminator='\n')
    
    label01 = ['馬名（生産国）','馬齢','毛色','性別','父、母、母父名','オーナー','生産者','調教師','出走回数']
    writer.writerow(label01)
    record01 = [h_name,h_age,h_color,h_gender,h_Pedigree,h_owner,h_breeder,h_trainer,str(len(h_value))]
    writer.writerow(record01)

    ##1行空ける
    writer.writerow('')

    ##一覧リストのラベルを生成
    label02 = ['日付','競馬場コード','馬場','馬場状態','レース条件（格）','距離','1位タイム','斤量','ゲート番号','騎手','着順','着差','優勝（2着）馬']
    writer.writerow(label02)

    h_date_urls = []
    for i in range(len(h_value)):
        ##日付
        try:
            h_date = h_value[i].find_element_by_css_selector('td:nth-of-type(1)').text
        except:
            print('h_date ERROR')

        ##競馬場コード
        try:
            h_course = h_value[i].find_element_by_css_selector('td:nth-of-type(2)').text
        except:
            print('h_course ERROR')
        
        ##馬場
        try:
            h_ts = h_value[i].find_element_by_css_selector('td:nth-of-type(3)').text
        except:
            print('h_ts ERROR')
        
        ##馬場状態
        try:
            h_tc = h_value[i].find_element_by_css_selector('td:nth-of-type(4)').text
        except:
            print('h_tc ERROR')
        
        ##レース条件（格）
        try:
            h_rt = h_value[i].find_element_by_css_selector('td:nth-of-type(5)').text
        except:
            print('h_rt ERROR')

        ##距離
        try:
            h_distance = h_value[i].find_element_by_css_selector('td:nth-of-type(6)').text
        except:
            print('h_distance ERROR')

        ##1位タイム
        try:
            h_time = h_value[i].find_element_by_css_selector('td:nth-of-type(7)').text
        except:
            print('h_time ERROR')

        ##斤量
        try:
            h_weight = h_value[i].find_element_by_css_selector('td:nth-of-type(8)').text
        except:
            print('h_weight ERROR')

        ##ゲート番号
        try:
            h_gate = h_value[i].find_element_by_css_selector('td:nth-of-type(9)').text
        except:
            print('h_gate ERROR')

        ##騎手
        try:
            h_jockey = h_value[i].find_element_by_css_selector('td:nth-of-type(10)').text
        except:
            print('h_jockey ERROR')

        ##着順
        try:
            h_num = h_value[i].find_element_by_css_selector('td:nth-of-type(11)').text
        except:
            print('h_num ERROR')

        ##着差
        try:
            h_margin = h_value[i].find_element_by_css_selector('td:nth-of-type(12)').text
        except:
            print('h_margin ERROR')

        ##優勝（2着）馬
        try:
            h_horse = h_value[i].find_element_by_css_selector('td:nth-of-type(13)').text
        except:
            print('h_horse ERROR')

        ##日付（詳細URL）
        try:
            h_date_url = h_value[i].find_element_by_css_selector('td:nth-of-type(1) a').get_attribute('href')
            h_date_urls.append(h_date_url)
        except:
            h_date_url = ''
        
        record02 = [h_date,h_course,h_ts, h_tc,h_rt,h_distance,h_time,h_weight,h_gate,h_jockey,h_num,h_margin,h_horse]
        writer.writerow(record02)
        print(record02)

    ##1行空ける
    writer.writerow('')
    
    label03 = ['競馬場','日付','レース番号','レース名','馬種','レース格','距離','馬場','総賞金','馬場状態','1位入線タイム','各着順の賞金','出走条件','着順','着差','ゲート番号','馬名','斤量','補助馬具','調教師','騎手']
    writer.writerow(label03)

    ##一覧の中から日付にリンクのあるものだけを残す
    h_date_urls = [x for x in h_date_urls if x != '']

    ##リンクの数だけ繰り返し処理
    for l in range(len(h_date_urls)):

        res = requests.get(h_date_urls[l])
        soup = BeautifulSoup(res.text, 'html.parser')

        targetNum = h_date_urls[l]
        targetNum = targetNum.split('tab=')[1]
        targetNum = int(targetNum)
        targetTabNum = targetNum + 1

        ##競馬場
        try:
            d_racecourseName = soup.find('p',{'class':'racecourseName'}).get_text(strip=True)
        except:
            print('d_racecourseName ERROR')

        ##レース番号
        try:
            print(str(targetTabNum))
        except:
            print('targetTabNum ERROR')

        ##レース名
        try:
            d_raceName = soup.select('.detailInfo h1')
            d_raceName = [x.text.strip() for x in d_raceName]
            d_raceName = d_raceName[targetNum]
        except:
            print('d_raceName ERROR')

        ##馬種
        try:
            d_horseType = soup.select('.shortConditions p:nth-of-type(2)')
            d_horseType = [x.text.strip() for x in d_horseType]
            d_horseType = d_horseType[targetNum]
        except:
            print('d_horseType ERROR')

        ##距離
        try:
            d_distanceType = soup.select('.shortConditions p:nth-of-type(3)')
            d_distanceType = [x.text.strip() for x in d_distanceType]
            d_distanceType = [x.split(' - ') for x in d_distanceType]
            d_distance = d_distanceType[targetNum][0]
        except:
            print('d_distance ERROR')

        ##馬場
        try:
            d_courseType = d_distanceType[targetNum][1]
        except:
            print('d_courseType ERROR')

        ##総賞金
        try:
            d_prizeMoney = soup.select('.prizeMoney')
            d_prizeMoney = [x.text.strip().replace('                  ',' ') for x in d_prizeMoney]
            d_prizeMoney = d_prizeMoney[targetNum]
        except:
            print('d_prizeMoney ERROR')

        ##馬場状態
        try:
            d_condition = soup.select('.railSafety p:nth-of-type(2)')
            d_condition = [x.text.strip().replace('Track Condition: ','') for x in d_condition]
            d_condition = d_condition[targetNum]
        except:
            print('d_condition ERROR')

        ##1位入線タイム
        try:
            d_finishTime = soup.select('.finishTime')
            d_finishTime = [x.text.strip() for x in d_finishTime]
            d_finishTime = [x.replace('Running Time','').strip() for x in d_finishTime]
            d_finishTime = d_finishTime[targetNum]
        except:
            print('d_finishTime ERROR')

        ##results
        try:
            d_result = soup.select('.resultsTable')
            d_result = d_result[targetNum]
        except:
            print('d_result ERROR')

        ##着順
        try:
            d_result_num = d_result.select('tbody .resultRows td:nth-of-type(1)')
            d_result_num = [x.text for x in d_result_num]
        except:
            print('d_result_num ERROR')

        ##着差
        try:
            d_result_margin = d_result.select('tbody .resultRows td:nth-of-type(2)')
            d_result_margin = [x.text for x in d_result_margin]
        except:
            print('d_result_margin ERROR')

        ##ゲート番号
        try:
            d_result_gate = d_result.select('tbody .resultRows td:nth-of-type(3) small')
            d_result_gate = [x.text.replace('(','').replace(')','') for x in d_result_gate]
        except:
            print('d_result_gate ERROR')

        ##馬名
        try:
            d_result_hName = d_result.select('tbody .resultRows td:nth-of-type(5)')
            d_result_hName = [x.text.strip() for x in d_result_hName]
        except:
            print('d_result_hName ERROR')

        ##斤量
        try:
            d_result_weight = d_result.select('tbody .resultRows td:nth-of-type(6)')
            d_result_weight = [x.text.strip() for x in d_result_weight]
        except:
            print('d_result_weight ERROR')

        ##補助馬具
        try:
            d_result_equipment = d_result.select('tbody .resultRows td:nth-of-type(7)')
            d_result_equipment = [x.text.strip() for x in d_result_equipment]
        except:
            print('d_result_equipment ERROR')

        ##調教師
        try:
            d_result_trainer = d_result.select('tbody .resultRows td:nth-of-type(8)')
            d_result_trainer = [x.text.strip() for x in d_result_trainer]
        except:
            print('d_result_trainer ERROR')

        ##騎手
        try:
            d_result_jockey = d_result.select('tbody .resultRows td:nth-of-type(9)')
            d_result_jockey = [x.text.strip() for x in d_result_jockey]
        except:
            print('d_result_jockey ERROR')
        
        for o in range(len(d_result_num)):
            record03 = [d_racecourseName,'',str(targetTabNum),d_raceName,d_horseType,'',d_distance,d_courseType,d_prizeMoney,d_condition,d_finishTime,'','']
            record04 = [d_result_num[o], d_result_margin[o],d_result_gate[o],d_result_hName[o],d_result_weight[o],d_result_equipment[o],d_result_trainer[o],d_result_jockey[o]]
            writer.writerow(record03 + record04)
            print(record03)
            print(record04)

driver.quit()