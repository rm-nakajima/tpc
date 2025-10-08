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
from selenium.webdriver.support import select

##開始時刻をエポック秒で取得（処理時間の計算用）
s_time = time.time()
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
# 設定ファイルロード関数02
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
# 対象馬
targets = readFile01('targets.txt')
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

##############################

for unique in range(len(targets)):
    # head
    label01 = ['ID','Horse_name','b','late','age','c_s','birthday','color','sex','Trainer','Owner','Owner_p',\
        'Sire','Dam','Damsire','Breeder','Standing','Races_Count','Lifetime Record',\
            'RUNS','WINS','2NDS','3RDS','URL','URL_Pedigree Report','scrape_date']
    res = requests.get(targets[unique])
    soup = BeautifulSoup(res.text, 'html.parser')
    dmn = targets[unique].split('https://')[1].split('/')[0].strip()

    # 過去馬名と馬名と生産国
    try:
        x = soup.select('.top .horse-search-details')[0]
        xi = x.select('h2.first')[0].get_text(strip=True)
    except:
        x = ''
        h_name = ErPro()
    # 過去馬名の有無を判別
    pastName = ''
    if '(Late:' in xi:
        pastName = xi.split('(Late:')[1].split(')')[0].strip()
        if '(' in pastName:
            pastName = pastName.split('(')[0].strip()
    # 馬名 / 生産国
    # 過去馬名無しのパターン
    if pastName == '':
        if '(' in xi:
            xi = xi.split('(')
            h_origin = xi[1].split(')')[0].strip()
            h_name = xi[0].strip()
        else:
            h_origin = 'AUS'
            h_name = xi.strip()
    # 過去馬名有りのパターン
    else:
        xi = xi.split('(Late:')
        # 新馬名に生産国表記
        if '(' in xi[0]:
            xi[0] = xi[0].split('(')
            h_origin = xi[0][1].split(')')[0].strip()
            h_name = xi[0][0].strip()
        else:
            h_origin = 'AUS'
            h_name = xi[0].strip()
            # 過去馬名に生産国表記
            if '(' in xi[1]:
                xi[1] = xi[1].split('(')
                h_origin = xi[1][1].split(')').strip()

    # 年齢 / 毛色 / 性別
    try:
        xi = x.select('tr')[0].get_text()
        xii = BlankExc(xi,'\n')[1].strip()
        h_age = re.split(r'\D',xii)[0].strip()
        h_sex = xii.split(' ')[-1].replace('\r','')
        h_color = xii.split(' ',1)[1].split(h_sex)[0].strip()
        c_s = h_color + ',' + h_sex
    except:
        h_age = ErPro()
        h_color = ErPro()
        h_sex = ErPro()
        c_s = ErPro()

    # 生年月日
    try:
        xi = x.select('tr')[0].get_text()
        xii = BlankExc(xi,'\n')[2].split(':')[1].strip()
        h_birth = datetime.datetime.strptime(xii, '%d-%b-%Y').strftime('%Y/%m/%d')
    except:
        h_birth = ErPro()

    # 父名 / 父の生産国 / 母名 / 母の生産国
    try:
        xi = x.select('tr')[0].get_text()
        xii = re.sub(r'^by ','',BlankExc(xi,'\n')[3].strip())
        if '(' in xii:
            h_sire = xii.split('(')[0].strip()
            h_sireOr = xii.split('(')[1].split(')')[0].strip()
        else:
            h_sire = xii.strip()
            h_sireOr = 'AUS'
        xii = re.sub(r'^from ','',BlankExc(xi,'\n')[4].strip())
        if '(' in xii:
            h_dam = xii.split('(')[0].strip()
            h_damOr = xii.split('(')[1].split(')')[0].strip()
        else:
            h_dam = xii.strip()
            h_damOr = 'AUS'
    except:
        h_sire = ErPro()
        h_sireOr = ErPro()
        h_dam = ErPro()
        h_damOr = ErPro()

    # PDF URL
    try:
        xi = xi = x.select('tr:nth-of-type(1) a.content-link')[0].get('href')
        pdflink = requests.get('https://' + dmn + xi).url
    except:
        pdflink = ErPro()

    # オーナー / 調教師 / Lifetime Record
    try:
        x = soup.select('.horse-search-details')[1]
    except:
        x = ''
    try:
        xi = x.select('tr th')
        xi = [x.get_text().strip() for x in xi]
        for i in range(len(xi)):
            if "Owner" in xi[i]:
                i01 = i
            if "Trainer" in xi[i]:
                i02 = i
            if "Career" in xi[i]:
                i03 = i
        xii = x.select('tr td')
        xii = [x.get_text().strip() for x in xii]
        # オーナー
        try:
            h_owner = xii[i01]
        except:
            h_owner = ''
        # 調教師
        try:
            if '(' in xii[i02]:
                h_trainer = xii[i02].split('(')[0].strip()
            else:
                h_trainer = xii[i02].strip()
            if re.match(r'^Mr ', h_trainer) or re.match(r'^Ms ', h_trainer):
                h_trainer = h_trainer.split(' ',1)[1].strip()
            h_trainer = h_trainer.replace(' Mr ',' ').replace(' Ms ',' ')
        except:
            h_trainer = ''
        # Lifetime Record
        try:
            h_ltr = xii[i03].split('Summary:')[1]
            h_ltr = BlankExc(h_ltr,' ')[0]
            h_ltr = h_ltr.split('Prizemoney:')[0].strip()
        except:
            h_ltr = ''
        # Lifetime Recordより回数を抽出
        try:
            h_lt0 = h_ltr.split('-')[0].strip()
            h_lt1 = h_ltr.split('-',1)[1].split(':')[0].strip()
            h_lt2 = h_ltr.split('-',1)[1].split(':')[1].strip()
            h_lt3 = h_ltr.split('-',1)[1].split(':')[-1].strip()
        except:
            h_lt1 = ''
            h_lt2 = ''
            h_lt3 = ''
    except:
        h_owner = ErPro()
        h_trainer = ErPro()
        h_ltr = ErPro()

    # 出力日時
    try:
        today = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")
    except:
        today = ''

    ############################
    # CSV生成
    ############################
    t = h_name.replace(' ','-')
    FileName = savePath + 'racingAustralia02_' + t + ".csv"
    logFileName = savePath + 'Err_racingAustralia02_' + t + ".txt"
    f = open(FileName, 'w', encoding="utf_8_sig")
    writer = csv.writer(f, lineterminator='\n')

    writer.writerow(label01)

    # Gear Changes
    flg01 = []
    flg02 = []
    b_fromDate = []
    b_toDate = []
    v_fromDate = []
    v_toDate = []
    try:
        x = soup.select('.race-form-horse-tab-menu div:nth-of-type(4) a')[0].get('href')
        x = x.replace('../','/')
        x = 'https://' + dmn + x
        res = requests.get(x)
        soup = BeautifulSoup(res.text, 'html.parser')
        xi = soup.select('.horse-search-strip-fields tr')[1::]
        for tr in range(len(xi)):
            xi[tr] = xi[tr].select('td')
            xi[tr] = [x.get_text(strip=True) for x in xi[tr]]
            xi[tr][1] = datetime.datetime.strptime(xi[tr][1], '%d-%b-%Y').strftime('%Y/%m/%d')
        def dateCV(a,b):
            try:
                for ii in a:
                    # 日付型に変換
                    ii[b] = ii[b].split('/')
                    for iii in range(3):
                        ii[b][iii] = int(ii[b][iii])
                    ii[b] = datetime.date(ii[b][0],ii[b][1],ii[b][2])
            except:
                pass
        def dateCollate(a,b,c):
            if len(a) > 0:
                if a[0][1] == 'On':
                    a.insert(0,[datetime.date.today(),'Off'])
                for i in range(len(a)):
                    if i == len(a) - 1:
                        pass
                    else:
                        ii = i + 1
                        if i % 2 == 0:
                            b.append(a[i+1][0])
                            c.append(a[i][0])
        # 補助馬具Type / 日付 / 着脱
        for i in xi:
            if 'Blinkers' in i[0]:
                flg01.append([i[1],i[2]])
            if 'Visors' in i[0]:
                flg02.append([i[1],i[2]])
        targetDay = datetime.date(2019,11,3)
        # Blinkers使用期間を算出
        dateCV(flg01,0)
        dateCollate(flg01,b_fromDate,b_toDate)
        # Visors使用期間を算出
        dateCV(flg02,0)
        dateCollate(flg02,v_fromDate,v_toDate)
    except:
        pass
    gearChange = xi

    # All From（リンク取得）
    try:
        x = soup.select('.race-form-horse-tab-menu div:nth-of-type(2) a')[0].get('href')
        x = x.replace('../','/')
        x = 'https://' + dmn + x
        res = requests.get(x)
        soup = BeautifulSoup(res.text, 'html.parser')
        xi = soup.select('.interactive-race-fields tr')
        formData = []

        for tr in range(len(xi)):
            try:
                temp = []
                temp.append(xi[tr].select('.Pos')[0].get_text(strip=True))
                temp.append(xi[tr].select('.remain')[0])
                if re.match(r'^T',temp[0]):
                    pass
                else:
                    formData.append(temp)
            except:
                pass

        # 競馬場コード / 日付 / 距離 / レース名 / レース格 / 獲得賞金 / 通過順位
        for tr in range(len(formData)):
            xi = formData[tr][1].get_text(strip=True)
            xii = formData[tr][1].select('.GreenLink')[0].get('href')
            xii = x.split('/HorseAllForm',1)[0] + '/' + xii
            xiii = formData[tr][1].select('.GreenLink')[0].get_text(strip=True)
            # 競馬場コード
            formData[tr].append(re.split(r'\d[0-9]+\D[a-z]+', xiii)[0].strip())
            # 日付
            formData[tr].append(datetime.datetime.strptime(xiii.split(' ')[-1].strip(), '%d%b%y')\
                .strftime('%Y/%m/%d'))
            # 距離
            ii = xi.split(xiii)[1].strip().split(' ')[0]
            formData[tr].append(ii)
            # レース名
            ii = xi.split(ii)[1].strip().split(' ',1)[1].split('$')[0].strip()
            formData[tr].append(ii)
            # レース格
            if 'Group 1' in ii:
                obj = 'Group 1'
            elif 'Group 2' in ii:
                obj = 'Group 2'
            elif 'Group 3' in ii:
                obj = 'Group 3'
            elif 'Listed' in ii:
                obj = 'Listed'
            else:
                obj = ''
            formData[tr].append(obj)
            # 獲得賞金
            if '($' in xi:
                ii = '$' + xi.split('($',1)[1].split(')')[0].strip()
            else:
                ii = '0'
            formData[tr].append(ii)
            # 騎手
            ii = formData[tr][1].select('.GreenLink')[1].get_text(strip=True)
            formData[tr].append(ii)
            # 斤量
            if ii == '':
                formData[tr].append(xi.split(' Barrier ')[0].strip().split(' ')[-1])
            else:
                formData[tr].append(xi.split(ii)[1].split(' Barrier ')[0].strip())
            # レースタイム
            ii = formData[tr][1].select('.GreenLink')[-1].get_text(strip=True)
            ii = xi.rsplit(ii,1)[1]
            if re.search(r'\d[0-9]kg',ii) and '(' in ii:
                ii = re.split(r'\d[0-9]kg',ii)[1].split('(')[0].strip()
            else:
                ii = ''
            formData[tr].append(ii)
            # 通過順位1 / 通過順位2
            if re.search(r'@\d', xi):
                xi = re.split(r'@\d', xi)
                xi[0] = re.split(r'@\d', xi[0])[0].split(' ')[-1]
                del xi[-1]
                xi[-1] = xi[-1].split(' ')[-1]
            else:
                xi = ['','']
            if len(xi) == 1:
                xi.insert(0,'')
            if len(xi) == 0:
                xi = ['','']
            formData[tr].append(xi[0])
            formData[tr].append(xi[1])
            del formData[tr][1]
            # 該当競馬場の国名取得
            flg = ['','']
            for i in rc_aus:
                if formData[tr][1] == i[0].strip():
                    flg = [xii,i[2]]
                else:
                    pass
            formData[tr].insert(3,flg[0])
            formData[tr].append(flg[1])

    except:
        print('ERROR')

    record01 = ['11',h_name,h_origin,pastName,h_age,c_s,h_birth,h_color,h_sex,h_trainer,h_owner,'',\
        h_sire,h_dam,'','','',len(formData),h_ltr,h_lt0,h_lt1,h_lt2,h_lt3,targets[unique],pdflink,today]
    writer.writerow(record01)
    writer.writerow(['12'])
    label02 = ['13','Gear Type','Date','Status','Comments']
    writer.writerow(label02)

    for i in range(len(gearChange)):
        writer.writerow(['14'] + gearChange[i])

    # 逆順に変換
    formData = formData[::-1]

    for fd in range(len(formData)):
        label03 = ['21','Date','競馬場コード','競馬場','クラブ','国名','Date_L','Video',\
        'レースNo','レース名','レース格','レースType','出走条件（クラス）','出走条件（その他）','距離','コース形態','コース詳細',\
            'レースタイム','着差','獲得賞金','馬体重','斤量','騎手','着順','出走頭数','通過順位＠800','通過順位＠400','オーナー']
        writer.writerow(label03)

        rc_country = formData[fd][-1]
        r_iNum = formData[fd][0].split(' of ')[0].strip()
        if re.match(r'^\d',r_iNum):
            r_iNum = re.split(r'\D',r_iNum)[0]
        else:
            pass
        r_iCount = formData[fd][0].split(' of ')[1].strip()
        rc_code = formData[fd][1]
        r_dist = formData[fd][4]
        r_title = formData[fd][5]
        r_grade = formData[fd][6]
        r_prize = formData[fd][7]
        r_jockey = formData[fd][8]
        r_wgt = formData[fd][9]
        r_hdTime = formData[fd][10]
        r_pass01 = formData[fd][11]
        r_pass02 = formData[fd][12]

        print(formData[fd])

        # 該当競馬場のレース詳細
        if re.match(r'^https://',formData[fd][3]):
            x = formData[fd][3]
            res = requests.get(x)
            soup = BeautifulSoup(res.text, 'html.parser')

            # Header情報（競馬場 / クラブ / 日付）
            xi = soup.select('.race-venue')[0]
            # 競馬場
            rc_name = xi.select('h2')[0].get_text(strip=True).split(':',1)[0].strip()
            # クラブ
            rc_club = xi.select('.race-venue h2')[0].get_text(strip=True).split(':')[1]
            xiii = xi.select('.race-venue-date')[0].get_text(strip=True)
            rc_club = rc_club.replace(xiii,'').strip()
            # 日付
            r_date = xi.select('.race-venue-date')[0].get_text(strip=True).replace(',','')
            r_date = r_date.split(' ',1)[1].strip()
            r_date = datetime.datetime.strptime(r_date, '%d %B %Y').strftime('%Y/%m/%d')
            # 補助馬具判別
            ii = r_date.split('/')
            ii = [int(x) for x in ii]
            inDate = datetime.date(ii[0],ii[1],ii[2])
            aids = []
            if len(b_fromDate) > 0:
                for i in range(len(b_fromDate)):
                    if b_fromDate[i] < inDate < b_toDate[i]:
                        aids.append('b')
                    elif inDate == b_toDate[i]:
                        aids.append('*')
                    elif inDate == b_fromDate[i]:
                        aids.append('*b')
            if len(v_fromDate) > 0:
                for i in range(len(v_fromDate)):
                    if v_fromDate[i] < inDate < v_toDate[i]:
                        aids.append('v')
                    elif inDate == v_toDate[i]:
                        aids.append('*')
                    elif inDate == v_fromDate[i]:
                        aids.append('*v')
            aids = (',').join(aids)
            # レースNo. / レース名 / 距離
            soup = BeautifulSoup(res.text,'lxml')
            xi = soup.select('.race-title')
            xx = x.split('#')[-1].replace('Race','Race ').strip()
            iD = 0
            for i in range(len(xi)):
                mc = str(xi[i].select('th')[0]).split('-')[0].split('">')[-1].strip()
                if xx == mc:
                    print(mc)
                    iD = i
                else:
                    pass
            xi = str(xi[iD].select('th')[0])
            xi = xi.split('">')[1].split('</a>')[0].strip().split('-',1)
            # レースNo.
            r_num = xi[0].split(' ')[1].strip()
            # レース名
            r_name = xi[1].rsplit('(',1)[0].strip().split(' ',1)[1]
            # 障害レース確認
            hurdle = []
            if 'Steeplechase' in r_name:
                hurdle.append('Steeplechase')
            elif 'Steeple' in r_name:
                hurdle.append('Steeple')
            if 'Hurdle' in r_name:
                hurdle.append('Hurdle')
            hurdle = (',').join(hurdle).strip()
            # レース格
            if 'Group 1' in r_name:
                r_grade = 'Group 1'
            elif 'Group 2' in r_name:
                r_grade = 'Group 2'
            elif 'Group 3' in r_name:
                r_grade = 'Group 3'
            elif 'Listed' in r_name:
                r_grade = 'Listed'
            # 距離
            rp = xi[1].replace('METRES','m')
            rc_dist = rp.rsplit('(',1)[1].strip().replace(' ','').replace(')','').strip()

            # 対象レース概要
            soup = BeautifulSoup(res.text, 'html.parser')
            xi = soup.select('.race-info')[iD].get_text()
            # 総賞金
            ii = soup.select('.race-info')[iD].select('td b')[0].get_text()
            fullPrize = ii.split('.')[0].split(' ')[-1].strip()
            # 着賞金
            numPrize = {}
            ii = ii.split('.',1)[1].strip().split(', ')
            for i in range(len(ii)):
                if re.match(r'\D',ii[i]):
                    ii[i] = ''
            ii = [x for x in ii if x != '']
            for i in range(len(ii)):
                numPrize[re.split(r'\D[a-z]',ii[i].split(' ',1)[0])[0].strip()] = \
                    ii[i].split(' ',1)[1].strip()
            # オフィシャルコメント
            ii = soup.select('.race-title')[0].get_text(strip=True)
            if 'Official Comments:' in ii:
                r_comm = ii.split('Official Comments:')[1].strip()
            else:
                r_comm = ''
            # 設定ファイルに該当する項目を照合
            ii = soup.select('.race-info')[iD].get_text()
            ii_ = soup.select('.race-info')[iD].select('b')
            ii = ii.replace(ii_[0].get_text(),'').split(ii_[1].get_text())[0].strip()
            # 出走条件（性別）
            termsGender = ''
            for i in aus_gender:
                if i in ii:
                    termsGender = i
                else:
                    pass
            # 出走条件（年齢）
            termsAge = ''
            for i in aus_age:
                if i in ii:
                    termsAge = i
                else:
                    pass
            # レース格
            termsGrade = ''
            for i in aus_grade:
                if i in ii:
                    termsGrade = i
                else:
                    pass
            # 出走条件
            r_text = ii
            # トラックネーム
            try:
                trackName = xi.split('Track Name:')[1].split('Track Type:')[0].strip()
            except:
                trackName = ''
            # 馬場の種類
            try:
                trackType = xi.split('Track Type:')[1].split('Track Condition:')[0].strip()
            except:
                trackType = ''
            # 馬場状態
            try:
                trackCondi = xi.split('Track Condition:')[1].split('RATime:')[0].strip()
            except:
                trackCondi = ''
            # レースタイム
            try:
                if 'Time:' in xi:
                    r_time = xi.split('Time:')[1].strip()
                elif 'RATime:' in xi:
                    r_time = xi.split('RATime:')[1].strip()
                try:
                    r_time = r_time.split(' ',1)[0].strip()
                except:
                    r_time = ''
            except:
                r_time = ''
            # LAST TIME
            try:
                if 'Last ' in xi:
                    ii = xi.split(' Last ')[1].split(': ')
                    ii = [x.strip() for x in ii]
                if '600m' in ii[0]:
                    ii[0] = ''
                else:
                    ii[0] = '(' + ii[0] + ')'
                try:
                    ii[1] = ii[1].split(' ')[0].strip()
                except:
                    pass
                if re.match(r'0:',ii[1]):
                    ii[1] = ii[1].split('0:',1)[1].strip()
                r_last = str(ii[1] + ii[0]).strip()
            except:
                r_last = ''

            record03 = ['22',r_date,rc_code,rc_name,rc_club,rc_country,x,'',\
                r_num,r_title,r_grade,'','','',r_dist,'','',\
                    r_hdTime,'',r_prize,'',r_wgt,r_jockey,r_iNum,r_iCount,r_pass01,r_pass02,h_owner]
            writer.writerow(record03)
            label04 = ['31','競馬場コード','競馬場','クラブ','国名','レース日付','レース名','レース格','レースNo',\
                'レース Type','レース他','レース名省略','出走条件','馬場の種類','出走条件（性別）','出走条件（クラス）',\
                    '出走条件（その他）','出走条件（年齢）','距離','コース回り','コース形態','コース詳細',\
                        'トラックネーム','馬場状態','障害数','障害レース確認','総賞金','着賞金','確定順位',\
                            '並び順位','異常区分','同着','着変更','馬番号','ゲート番号','着差1','着差2',\
                                '馬名','生産国','オッズ','馬齢','馬種','馬体重','斤量','斤量特記1','斤量特記2',\
                                    '補助馬具','調教師','騎手','毛色','性別','父名','母名','母父名',\
                                        '出走頭数','優勝馬タイム','LAST600','オーナー','生産者','コメント']
            writer.writerow(label04)
            # テーブル取得
            xi = soup.select('.race-strip-fields')[iD].select('tr')[1::]

            # 出走頭数 / 着順
            h_value = len(xi)
            h_num = []
            def trFlg(selector,i):
                if len(xi[tr].select(selector)) > 0:
                    try:
                        z = xi[tr].select(selector)[i].get_text(strip=True)
                    except:
                        z = ''
                else:
                    z = ''
                return z
            for tr in range(len(xi)):
                if 'Scratched' in xi[tr].get('class'):
                    h_value = h_value - 1
                # 着順
                ii = trFlg('span.Finish',0)
                if len(ii) < 1:
                    ii = 'SCR'
                h_num.append(ii)
            # 同着
            dht = []
            try:
                # 重複する要素を抽出
                dup = [x for x in set(h_num) if h_num.count(x) > 1]
                for i in range(len(h_num)):
                    if h_num[i] in dup and re.match(r'^[0-9]', h_num[i]):
                        dht.append('dht')
                    else:
                        dht.append('')
            except:
                for i in range(len(h_num)):
                    h_num.append('')

            # 着賞金照合 / 馬番号 / 馬名 / 調教師 / 騎手 / 着差 / 斤量 / 異常区分
            for tr in range(len(xi)):
                r_hNum = h_num[tr]
                # 異常区分
                h_str = ''
                for i in aus_placing:
                    if r_hNum == i[0]:
                        h_str = r_hNum
                        r_hNum = i[1]
                    else:
                        pass
                r_dht = dht[tr]
                h_count = str(tr + 1)
                # 着賞金と着順をマッチング
                if r_hNum in numPrize:
                    h_prize = numPrize[r_hNum]
                else:
                    h_prize = ''
                # 馬番号
                r_hRun = trFlg('td.no',0)
                # 馬名
                r_hName = trFlg('td.horse',0)
                if '(' in r_hName:
                    r_hName = r_hName.split('(')[0].strip()
                # 調教師
                r_hTrainer = trFlg('td.trainer',0)
                # 騎手
                r_hJockey = trFlg('td.jockey',0)
                if '(' in r_hJockey:
                    r_hJockey = r_hJockey.split('(')[0].strip()
                # 着差
                r_hMar = trFlg('td.barrier',0)
                # ゲート番号
                r_hGate = trFlg('td.barrier',1)
                # 斤量 / 斤量特記1
                r_hWgt = trFlg('td.weight',0)
                r_hWgt_ = ''
                if '(' in r_hWgt:
                    ii = r_hWgt.split('(')
                    r_hWgt = ii[-1].strip().split(' ')[-1].split(')')[0].strip()
                    r_hWgt_ = ii[0].strip()
                # オッズ
                r_hOdds = trFlg('td.penalty',0)
                # aids
                aidsFix = ''
                if r_hName == h_name:
                    aidsFix = aids
                else:
                    aidsFix = ''

                record04 = ['32',rc_code,rc_name,rc_club,rc_country,r_date,r_name,termsGrade,r_num,'','',r_title,r_text,trackType,\
                    termsGender,'','',termsAge,rc_dist,'','','',trackName,trackCondi,'',hurdle,fullPrize,h_prize,r_hNum,h_count,\
                        h_str,r_dht,'',r_hRun,r_hGate,r_hMar,'',r_hName,'',r_hOdds,'','','',\
                            r_hWgt,r_hWgt_,'',aidsFix,r_hTrainer,r_hJockey,'','','','','',h_value,r_time,\
                                r_last,'','',r_comm]
                writer.writerow(record04)
        else:
            r_date = formData[fd][2]
            try:
                record03 = ['22',r_date,rc_code,'','',rc_country,'','',\
                    '',r_title,r_grade,'','','',r_dist,'','',\
                        r_hdTime,'',r_prize,'',r_wgt,r_jockey,r_iNum,r_iCount,r_pass01,r_pass02,h_owner]
                writer.writerow(record03)
            except:
                pass
##終了時刻をエポック秒で取得（処理時間の計算用）
e_time = time.time()
p_time = e_time - s_time
##処理時間の表示
print('処理時間（秒）: ' + str(p_time))
sys.exit()