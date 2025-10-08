# -*- coding: utf-8 -*-
from math import isinf
from pickle import FALSE
import requests
from bs4 import BeautifulSoup
import time
import datetime
from datetime import date, timedelta, datetime as dt
import csv
import re
import copy
import sys

##開始時刻をエポック秒で取得（処理時間の計算用）
s_time = time.time()
##今日の日付
toDay = datetime.date.today()
##############################
# function
##############################
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
        b = [x for x in b if x != '']
    except:
        print('>> ' + str(a) + ': ERROR')
        sys.exit()
    return b
# 設定ファイルロード関数01
def readFile02(a):
    try:
        c_fPath = rPath + a
        b = []
        with open(c_fPath, encoding='utf_8_sig') as f:
            reader = csv.reader(f)
            for r in reader:
                b.append(r)
        b = b[1::]
    except:
        print('>> ' + str(a) + ': ERROR')
        sys.exit()
    return b
# エラー時の空白処理
def ErPro():
    x = ''
    return x
# 指定文字列でで区切り空白の要素を削除
def BlankExc(z,str):
    z = z.split(str)
    z = [x for x in z if x != '']
    return z
##############################
# setting data
##############################
# 対象範囲
targets = readFile01('targets.txt')[0]
t = targets.replace('/','').replace(' ','')
targets = targets.split('-')
i = targets[0].split('/')
i = [int(x.strip()) for x in i]
fromDate = datetime.date(i[0],i[1],i[2])
ii = targets[1].split('/')
ii = [int(x.strip()) for x in ii]
toDate = datetime.date(ii[0],ii[1],ii[2])
print('>> target date: ' + str(fromDate) + ' -> ' + str(toDate))
# 競馬場コード
rc_aus = readFile02('racingaustralia_country.csv')
# 出走条件（性別）
aus_gender = readFile01('aus-race-gender.txt')
# 出走条件（年齢）
aus_age = readFile01('aus-race-age.txt')
# レース格
aus_grade = readFile01('aus-race-case.txt')
# 異常区分
aus_placing = readFile02('racing-australia_race-placing.csv')
# 保存場所
savePath = readFile01('save.txt')[0]
if len(savePath) == 0:
    savePath = ''
else:
    if savePath.endswith('/') or savePath.endswith('¥'):
        pass
    else:
        if '¥' in savePath:
            savePath = savePath + '¥'
        else:
            savePath = savePath + '/'
label = [\
    '競馬場コード','競馬場','クラブ','国名','レース日付','レース名','レース格','レースNo','レース Type','レース他',\
    'レース名省略','出走条件','馬場の種類','出走条件（性別）','出走条件（クラス）','出走条件（その他）','出走条件（年齢）',\
    '距離','コース回り','コース形態','コース詳細','トラックネーム','馬場状態','障害数','障害レース確認','総賞金','着賞金',\
    '確定順位','並び順位','異常区分','同着','着変更','馬番号','ゲート番号','着差1','着差2','馬名',\
    '生産国','オッズ','馬齢','馬種','馬体重','斤量','斤量特記1','斤量特記2','補助馬具','調教師',\
    '騎手','毛色','性別','父名','母名','母父名','出走頭数','優勝馬タイム','LAST600','オーナー','生産者','コメント'
    ]
targetCountry = [\
    'https://racingaustralia.horse/FreeFields/Calendar_Results.aspx?State=NSW',\
    'https://racingaustralia.horse/FreeFields/Calendar_Results.aspx?State=VIC',\
    'https://racingaustralia.horse/FreeFields/Calendar_Results.aspx?State=QLD',\
    'https://racingaustralia.horse/FreeFields/Calendar_Results.aspx?State=WA',\
    'https://racingaustralia.horse/FreeFields/Calendar_Results.aspx?State=SA',\
    'https://racingaustralia.horse/FreeFields/Calendar_Results.aspx?State=TAS',\
    'https://racingaustralia.horse/FreeFields/Calendar_Results.aspx?State=ACT',\
    'https://racingaustralia.horse/FreeFields/Calendar_Results.aspx?State=NT'\
    ]
tgt = {}
for unique in range(len(targetCountry)):
    res = requests.get(targetCountry[unique])
    soup = BeautifulSoup(res.text, 'html.parser')
    dmn = targetCountry[unique].split('https://')[1].split('/')[0].strip()

    # 末尾「(Trial)」の行除外
    xi = soup.select('.race-fields tr')[1::]
    xii = []
    for tr in xi:
        if re.search(r'\(Trial\)$',tr.select('td')[1].get_text()) or re.search(r'\(JumpOut\)$',tr.select('td')[1].get_text()):
            pass
        else:
            xii.append(tr)
    xi = xii
    xii = []
    for tr in xi:
        # 開催簿を日付型に変換
        # 閏年対応
        dFlg = tr.select('td')[0].get_text(strip=True)
        if re.search('29-Feb', dFlg):
            d = ['02', '29']
        else:
            d = datetime.datetime.strptime(tr.select('td')[0].get_text(strip=True),\
                '%a %d-%b').strftime('%m/%d').split('/')
        if int(d[0]) <= toDay.month:
            Y = toDay.year
        else:
            Y = toDay.year - 1
        D = datetime.date(Y,int(d[0]),int(d[1]))
        # URL取得
        L = 'https://' + dmn + tr.select('td')[2].select('a')[0].get('href')
        if ' ' in L:
            L = L.replace(' ','%20')
        xii.append([D,L])
    xi = xii
    # 指定範囲以外を除去
    xii = []
    for tr in xi:
        if fromDate <= tr[0] <= toDate:
           xii.append([tr[0],tr[1]])
        else:
            pass
    xi = xii
    print('>> ' + targetCountry[unique].split('=')[-1] + ' -> ' + str(len(xi)))

    for tidy in range(len(xi)):
        tgt[xi[tidy][1]] = xi[tidy][0]
tgt = sorted(tgt.items(), key=lambda x:x[1])
xi = []
xii = []
for tidy in range(len(tgt)):
    xii.append(tgt[tidy][1])
zii = sorted(set(xii))
for tidy in range(len(tgt)):
    xi.append(tgt[tidy][0])

for nm in range(len(zii)):
    ziii = []
    for tidy in range(len(tgt)):
        if zii[nm] == tgt[tidy][1]:
            ziii.append(tgt[tidy][0])
    print(str(nm + 1) + ': ')
    print(ziii)
    ##############################
    # CSV生成
    ##############################
    t = str(zii[nm])
    print(t)
    FileName = savePath + 'racingAustralia01_' + t + ".csv"
    logFileName = savePath + 'Err_racingAustralia01_' + t + ".txt"
    f = open(FileName, 'w', encoding="utf_8_sig")
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(label)
    for results in range(len(ziii)):
        print('>> ' + str(results + 1) + ' / ' + str(len(ziii)))
        print('>> ' + ziii[results])
        res = requests.get(ziii[results])
        soup = BeautifulSoup(res.text, 'html.parser')
        flg = soup.select('.race-title')
        if len(flg) > 0:
            obj = soup.select('.race-venue h2')[0]
            # 競馬場
            rcName = obj.get_text().split(':')[0].strip()
            # 競馬場コード / 国名
            xii = ['','']
            for i in rc_aus:
                if i[4] == rcName:
                    xii[0] = i[0]
                    xii[1] = i[2]
                else:
                    pass
            rcCode = xii[0]
            rcCountry = xii[1]
            # レース日付
            xii = obj.select('.race-venue-date')[0].get_text(strip=True)
            xiii = xii.replace(',','').strip().split(' ')[1::]
            xiii = (' ').join(xiii)
            rcDate = datetime.datetime.strptime(xiii, '%d %B %Y').strftime('%Y/%m/%d')
            # クラブ
            rcClub = obj.get_text().split(xii)[0].split(':',1)[1].strip()
            # レースNo / レース名 / 距離 / 総賞金 / 着順賞金 / レース格 / 出走条件（性別） / 出走条件（年齢）/
            #   トラック名 / 馬場の種類 / 馬場状態 / 優勝馬タイム / 上り600mタイム
            # 着順賞金
            obj01 = soup.select('table.race-title')
            obj02 = soup.select('table.race-strip-fields')
            for i in range(len(obj01)):
                elem = obj01[i].select('th span')[0].get_text(strip=True).split('-',1)
                # レース番号
                try:
                    r_num = elem[0].strip().split(' ')[-1]
                except:
                    r_num = ''
                # レース名
                if re.search(r'\dAM ',elem[1]):
                    r_name = re.split(r'\dAM ',elem[1])[1].split(' METRES)')[0].rsplit('(',1)[0].strip()
                elif re.search(r'\dPM ',elem[1]):
                    r_name = re.split(r'\dPM ',elem[1])[1].split(' METRES)')[0].rsplit('(',1)[0].strip()
                else:
                    r_name = ''
                if 'Large Scratched' in str(obj01[i].next_sibling.next_sibling):
                    obj02.insert(i,'')
                    print('中止レース')
                    fErr = open(logFileName, 'a', encoding="utf_8_sig")
                    fErr.write('中止レース: ' + t + ' ' + r_num + ' ' + r_name + '\n')
                    fErr.write(ziii[results] + '\n')
                else:
                    # 障害レース確認
                    hurdle = []
                    if 'Steeplechase' in r_name:
                        hurdle.append('Steeplechase')
                    elif 'Steeple' in r_name:
                        hurdle.append('Steeple')
                    if 'Hurdle' in r_name:
                        hurdle.append('Hurdle')
                    hurdle = (',').join(hurdle).strip()
                    # 距離
                    try:
                        r_dist = elem[1].rsplit(' METRES)',1)[0].rsplit('(',1)[1].strip() + 'm'
                    except:
                        r_dist = ''
                    elem = obj01[i].select('tr td')[0]
                    # 総賞金
                    try:
                        r_prize = elem.get_text(strip=True).split('.',1)[0].split('Of ')[1].strip()
                    except:
                        r_prize = ''
                    # 着順賞金を辞書型で格納
                    prDict = {}
                    try:
                        item = elem.select('b')[0].get_text(strip=True).split('.',1)[1].split(', ')
                        item = [x.strip() for x in item]
                        for ii in item:
                            if re.match(r'^\d',ii):
                                prDict[re.split(r'\D',ii)[0].strip()] = ii.split(' ')[1].strip()
                    except:
                        pass
                    # レース名省略
                    d1 = obj01[i].select('b')[0].get_text(strip=True)
                    r_text = obj01[i].get_text(strip=True).split(d1)[1].split('Track Name:')[0].strip()
                    # レース格
                    termsGrade = ''
                    for list in aus_grade:
                        if list in r_text:
                            termsGrade = list
                        else:
                            pass
                    # 出走条件（性別）
                    termsGender = ''
                    for list in aus_gender:
                        if list in r_text:
                            termsGender = list
                        else:
                            pass
                    # 出走条件（年齢）
                    termsAge = ''
                    for list in aus_age:
                        if list in r_text:
                            termsAge = list
                        else:
                            pass
                    comp = elem.select('b')[1::]
                    comp = [x.get_text(strip=True) for x in comp]
                    doc = elem.get_text(strip=True)
                    b01,b02,b03,b04,b05,b06 = '','','','','',''
                    for ii in range(len(comp)):
                        iii = ii + 1
                        # トラック名 / 馬場の種類 / 馬場状態
                        if 'Track Name:' in comp[ii]:
                            b01 = doc.split(comp[ii])[1].split(comp[iii])[0]
                        if 'Track Type:' in comp[ii]:
                            b02 = doc.split(comp[ii])[1].split(comp[iii])[0]
                        if 'Track Condition:' in comp[ii]:
                            b03 = doc.split(comp[ii])[1].split(comp[iii])[0]
                        if 'RATime:' in comp[ii] or 'Time:' == comp[ii]:
                            b04 = doc.split(comp[ii])[1].split(comp[iii])[0]
                        # 上り600m
                        if 'Last ' in comp[ii]:
                            b05 = doc.split(comp[ii])[1].split(comp[iii])[0].split('0:')[1].strip()
                            b05_ = comp[ii].split('Last ')[1].split(':')[0]
                            if b05_ == '600m':
                                pass
                            else:
                                b05 = b05 + '(' + b05_ + ')'
                        # オフィシャルコメント
                        if 'Official Comments:' in comp[ii]:
                            b06 = doc.split(comp[ii])[1].strip()
                    trackInfo = []
                    trackInfo.append(b01)
                    trackInfo.append(b02)
                    trackInfo.append(b03)
                    trackInfo.append(b04)
                    trackInfo.append(b05)
                    trackInfo.append(b06)
                    # 共通項目の整形
                    common = [\
                        rcCode,rcName,rcClub,rcCountry,rcDate,r_name,termsGrade,r_num,'','',r_text,'',trackInfo[1],termsGender,'','',termsAge,\
                            r_dist,'','','',trackInfo[0],trackInfo[2],'',hurdle,r_prize
                        ]
                    # テーブル取得
                    try:
                        elem = obj02[i].select('tr')[1::]
                        value = len(elem)
                        # 着順 / 同着
                        h_num, dht = [],[]
                        for ii in range(len(elem)):
                            if 'Scratched' in elem[ii].get('class'):
                                h_num.append('SCR')
                                value = value -1
                            else:
                                h_num.append(elem[ii].select('td')[1].get_text(strip=True))
                        try:
                            dup = [x for x in set(h_num) if h_num.count(x) > 1]
                            for ii in range(len(h_num)):
                                if h_num[ii] in dup and re.match(r'^[0-9]', h_num[ii]):
                                    dht.append('dht')
                                else:
                                    dht.append('')
                        except:
                            for i in range(len(h_num)):
                                h_num.append('')
                        for ii in range(len(elem)):
                            # 着順と着順賞金を照合
                            if h_num[ii] in prDict:
                                numPr = prDict[h_num[ii]]
                            else:
                                numPr = ''
                            # 異常区分
                            h_str = ''
                            for i in aus_placing:
                                if h_num[ii] == i[0]:
                                    h_str = i[1]
                                else:
                                    pass
                            # 関数定義
                            comp = elem[ii].select('td')
                            def getTD(n):
                                try:
                                    a = comp[n].get_text(strip=True)
                                except:
                                    a = ''
                                return a
                            # 馬番号
                            r_hRun = getTD(2)
                            # 馬名
                            h_name = getTD(3)
                            if '(' in h_name:
                                h_name = h_name.split('(')[0].strip()
                            # 調教師
                            h_trainer = getTD(4)
                            # 騎手
                            h_jockey = getTD(5)
                            if '(' in h_jockey:
                                h_jockey = h_jockey.split('(')[0].strip()
                            # 着差
                            h_margin = getTD(6)
                            # ゲート番号
                            h_gate = getTD(7)
                            # 斤量
                            r_wgt01 = getTD(8)
                            # 斤量特記1
                            if '(cd' in r_wgt01:
                                r_wgt = r_wgt01.split('(cd',1)
                                r_wgt01 = r_wgt[1].replace(')','').strip()
                                r_wgt02 = r_wgt[0].strip()
                            else:
                                r_wgt02 = ''
                            # オッズ
                            h_odds = getTD(10)
                            # 個別レコード
                            record = [numPr,h_num[ii],ii+1,h_str,dht[ii],'',r_hRun,h_gate,h_margin,'',\
                                h_name,'',h_odds,'','','',r_wgt01,r_wgt02,'','',\
                                h_trainer,h_jockey,'','','','','',value]
                            fixRecord = common + record + [trackInfo[3],trackInfo[4],'','',trackInfo[5]]
                            writer.writerow(fixRecord)
                    except:
                        pass
        else:
            pass
##終了時刻をエポック秒で取得（処理時間の計算用）
e_time = time.time()
p_time = e_time - s_time
##処理時間の表示
print('処理時間（秒）: ' + str(p_time))
sys.exit()