# -*- coding: utf-8 -*-
from math import isinf
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

##############################
# CSV生成
##############################
FileName = savePath + 'racingAustralia03_' + t + ".csv"
logFileName = savePath + 'Err_racingAustralia01_' + t + ".txt"
f = open(FileName, 'w', encoding="utf_8_sig")
writer = csv.writer(f, lineterminator='\n')
label = [\
    '発走時刻','競馬場コード','競馬場','クラブ','開催日','距離','レース名','レース格','レースNo','レースその他','出走条件（クラス）','出走条件（年齢）',\
    '馬場の種類','馬番号','ゲート番号','馬名','生産国','生年月日','馬齢','毛色','性別',\
    '父名','父生産国','母名','母生産国','母の父','母父生産国'\
    ]
writer.writerow(label)
targetCountry = [\
    'https://racingaustralia.horse/FreeFields/Calendar.aspx?State=NSW',\
    'https://racingaustralia.horse/FreeFields/Calendar.aspx?State=VIC',\
    'https://racingaustralia.horse/FreeFields/Calendar.aspx?State=QLD',\
    'https://racingaustralia.horse/FreeFields/Calendar.aspx?State=WA',\
    'https://racingaustralia.horse/FreeFields/Calendar.aspx?State=SA',\
    'https://racingaustralia.horse/FreeFields/Calendar.aspx?State=TAS',\
    'https://racingaustralia.horse/FreeFields/Calendar.aspx?State=ACT',\
    'https://racingaustralia.horse/FreeFields/Calendar.aspx?State=NT'\
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
        if re.search(r'\(Trial\)$',tr.select('td')[1].get_text()):
            pass
        else:
            xii.append(tr)
    xi = xii
    xii = []
    for tr in xi:
        # 開催簿を日付型に変換
        d = datetime.datetime.strptime(tr.select('td')[0].get_text(strip=True),\
            '%a %d-%b').strftime('%m/%d').split('/')
        if int(d[0]) >= toDay.month:
            Y = toDay.year
        else:
            Y = toDay.year + 1
        D = datetime.date(Y,int(d[0]),int(d[1]))
        # URL取得
        try:
            L = 'https://' + dmn + tr.select('td')[5].select('a')[0].get('href')
            if ' ' in L:
                L = L.replace(' ','%20')
        except:
            L = ''
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
for tidy in range(len(tgt)):
    xi.append(tgt[tidy][0])
for results in range(len(xi)):
    if '' == xi[results]:
        pass
    else:
        print('>> ' + str(results + 1) + ' / ' + str(len(xi)))
        print('>> ' + xi[results])
        res = requests.get(xi[results])
        soup = BeautifulSoup(res.text, 'html.parser')
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
        # 競馬場 / クラブ
        elem = obj.get_text().split(xii)[0].split(':',1)
        rc_name = elem[0].strip()
        rcClub = elem[1].strip()
        obj01 = soup.select('table.race-title')
        obj02 = soup.select('table.race-strip-fields')
        obj03 = soup.select('table.horse-form-table')
        head = []
        foot = []
         # レースNo / 発走時刻 / レース名 / 距離 / 馬場 / レース条件
        for i in range(len(obj01)):
            elem = obj01[i].select('th span')[0].get_text(strip=True).split('-',1)
            # レース番号
            try:
                r_num = elem[0].strip().split(' ')[-1]
            except:
                r_num = ''
            elem = obj01[i].select('th')[0].get_text(strip=True)
            # 発走時刻
            if re.search(r'\dAM ',elem):
                r_begin = re.sub('AM ','AM*sub*',elem).split('*sub*')[0].split('-')[1].strip()
            elif re.search(r'\dPM ',elem):
                r_begin = re.sub('PM ','PM*sub*',elem).split('*sub*')[0].split('-')[1].strip()
            else:
                r_begin = ''
            # レース名 / 距離
            try:
                elObj = elem.split(r_begin)[1].split(' METRES)',1)[0]
                r_name = elObj.rsplit('(',1)[0].strip()
                r_dist = elObj.rsplit('(',1)[1].strip() + 'm'
            except:
                r_name = ''
                r_dist = ''
            # レース格 / レースその他 /出走条件（クラス） / 出走条件（年齢） / 馬場の種類
            elem = obj01[i].select('.race-info')[0]
            # レース格
            r_text = elem.get_text(strip=True)
            # レース格
            termsGrade = ''
            for list in aus_grade:
                if list in r_text:
                    termsGrade = list
                else:
                    pass
            # 出走条件（年齢）
            termsAge = ''
            for list in aus_age:
                if list in r_text:
                    termsAge = list
                else:
                    pass
            # 馬場の種類
            tracktype = str(elem).split('<b>Track Type:</b>')[1].split('<b')[0].strip()
            # 出走馬数
            h_value = len(obj02[i].select('tr')) - 1
            # Head
            head.append([r_begin,rcCode,rc_name,rcClub,rcDate,r_dist,r_name,\
                termsGrade,r_num,'','',termsAge,tracktype,h_value])
        for i in range(len(obj03)):
            # 馬番号
            h_num = obj03[i].select('.horse-number')[0].get_text(strip=True)
            # 馬名
            h_name = obj03[i].select('.horse-name')[0].get_text(strip=True)
            # 生産国
            h_origin = 'AUS'
            if '(' in h_name:
                h_origin = h_name.split('(')[1].split(')')[0].strip()
                h_name = h_name.split('(')[0].strip()
            # 年齢 / 毛色 / 性別
            h_info = obj03[i].select('.plain')[0].get_text(strip=True)
            h_age = h_info.split('year old')[0].strip()
            h_sex = h_info.split('year old')[1].split('(')[0].strip().split(' ')[-1]
            h_color = h_info.split(h_sex)[0].split('year old')[1].strip()
            h_birth = h_info.split('(',1)[1].split(')')[0].split('-')
            h_birth = h_birth[2] + '/' + h_birth[1] + '/' + h_birth[0]
            # 父名
            h_sire = obj03[i].select('a.GreenLink')[1].get_text(strip=True)
            h_sire_origin = 'AUS'
            if '(' in h_sire:
                h_sire_origin = h_sire.split('(')[1].split(')')[0].strip()
                h_sire = h_sire.split('(')[0].strip()
            # 母名
            h_dam = obj03[i].select('a.GreenLink')[2].get_text(strip=True)
            h_dam_origin = 'AUS'
            if '(' in h_dam:
                h_dam_origin = h_dam.split('(')[1].split(')')[0].strip()
                h_dam = h_dam.split('(')[0].strip()
            # 母父名
            h_bms = obj03[i].select('a.GreenLink')[3].get_text(strip=True)
            h_bms_origin = 'AUS'
            if '(' in h_bms:
                h_bms_origin = h_bms.split('(')[1].split(')')[0].strip()
                h_bms = h_bms.split('(')[0].strip()
            # ゲート番号
            elms = obj03[i].select('tr')
            h_gate = ''
            for ii in range(len(elms)):
                subObj = elms[ii].get_text(strip=True)
                if 'Barrier:' in subObj:
                    h_gate = subObj.split('Barrier:')[1].split('Record')[0].strip()
            # Scratched
            if(len(obj03[i].select('td.Scratched')) > 0):
                h_num = 'SCR'
                h_gate = 'SCR'
            foot.append([h_num,h_gate,h_name,h_origin,h_birth,h_age,h_color,h_sex,\
                h_sire,h_sire_origin,h_dam,h_dam_origin,h_bms,h_bms_origin])
        # head + foot
        for i in range(len(head)):
            k = int(head[i][-1])
            hd =  head[i][0:13]
            print(hd)
            for ii in range(k):
                fix = hd + foot[ii]
                writer.writerow(fix)
            del foot[0:k]

##終了時刻をエポック秒で取得（処理時間の計算用）
e_time = time.time()
p_time = e_time - s_time
##処理時間の表示
print('処理時間（秒）: ' + str(p_time))
sys.exit()