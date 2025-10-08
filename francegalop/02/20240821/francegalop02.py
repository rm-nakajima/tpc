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
# france-galop_horse-type.txt（馬種）
h_type_list = readFile01('france-galop_horse-type.txt')
##############################
# corse_around.txt（コースまわり）
rc_around = readFile01('race-course.txt')
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
# Global function
############################
# cookieバナー非表示化
def bnrNone():
    try:
        dn = "document.getElementById('cf-root').style.display = 'none'"
        driver.execute_script(dn)
    except:
        pass

############################
# ChromeDriver
############################
# Chrome展開
driver = webdriver.Chrome()
options = Options()
driver.set_window_size(1300,768)
driver.implicitly_wait(10)

############################
# targetsの要素の数だけ繰り返し処理
############################
for z in range(len(targets)):
    driver.get(targets[z])
    driver.implicitly_wait(10)

    #cookieバナー
    time.sleep(3)
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
    # ラベル01
    label01 = ['ID','Horse_name','b','age','c_s','birthday','color','sex','Trainer','Owner','Owner_p',\
        'Sire','Dam','Damsire','Breeder','Standing','Races_Count','URL','scrape_date']

    # 馬名/生産国
    try:
        xi = driver.find_element_by_css_selector('h1').text.strip()
        if '(' in xi:
            a = xi.split('(')[0].strip()
            b = xi.split('(')[1].replace(')','').strip()
        if ' ' in xi:
            a = xi
            b = xi.split(' ')[-1].strip()
            if b in origin_list:
                sp = ' ' + b
                a = xi.split(sp)[0]
            else:
                b = 'FR'
        else:
            a = xi
            b = 'FR'
        h_name = a
        h_origin = b
    except:
        h_name = ''
        h_origin = ''

    # 性別
    try:
        h_sex = driver.find_element_by_css_selector('.fiche_cheval_entete .sex').text.strip()
    except:
        h_sex = ''

    #
    try:
        h_rac = driver.find_element_by_css_selector('.fiche_cheval_entete .rac').text.strip()
    except:
        h_rac = ''

    # 毛色
    try:
        h_rob = driver.find_element_by_css_selector('.fiche_cheval_entete .rob').text.strip()
    except:
        h_rob = ''

    # sex,rac,rob
    try:
        h_cs = h_sex + ',' + h_rac + ',' + h_rob
    except:
        h_cs = ''

    # 記載情報の精査
    hDict = {}
    a = driver.find_elements_by_css_selector('.fiche_cheval_entete .col-sm-4 p')
    ####################
    # func01
    ####################
    def func01(b,c):
        try:
            # 原則はXpath取得
            a = driver.find_element_by_xpath(b).text
            if c in a:
                # 文字列照合に成功した場合
                a = a.replace(c,'').strip()
            else:
                # 文字列照合に失敗した場合
                a = driver.find_elements_by_css_selector('.fiche_cheval_entete .col-sm-4 p')
                def func01sub(str,dictKey):
                    if str in a[i].find_element_by_css_selector('span').text:
                        hDict[dictKey] = a[i].text.replace(str,'').strip()
                    else:
                        pass
                for i in range(len(a)):
                    try:
                        func01sub('Né le','birth')
                        func01sub('Entraîneur','trainer')
                        func01sub('Par','pedigree')
                        func01sub('Sous les couleurs de','owner')
                        func01sub('Éleveurs','breeder')
                    except:
                        pass
                try:
                    h_birth = hDict["birth"]
                    h_pedigree = hDict["pedigree"]
                    h_trainer = hDict["trainer"]
                    h_owner = hDict["owner"]
                    h_breeder = hDict["breeder"]
                except:
                    print('情報取得エラー')
                    sys.exit()
        except:
            a = ''
        return a
    ####################
    # 原則はXpath取得、条件不一致の場合には精査処理を含める
    ####################
    # 生年月日
    h_birth = func01('/html/body/div[1]/div/div/section/div/div[1]/div[2]/p[2]','Né le')
    try:
        h_birth = h_birth.split('/')
        h_birth = h_birth[2] + '/' + h_birth[1] + '/' + h_birth[0]
    except:
        h_birth = ''

    # 父,母,母の父
    h_pedigree = func01('/html/body/div[1]/div/div/section/div/div[1]/div[2]/p[3]','Par')
    try:
        h_sire = h_pedigree.split(' et ')[0].strip()
        h_dam = h_pedigree.split(' et ')[1].split('(')[0].strip()
        h_damsire = h_pedigree.split('(')[-1].replace(')','').strip()
    except:
        h_sire = ''
        h_dam = ''
        h_damsire = ''

    # 調教師
    h_trainer = func01('/html/body/div[1]/div/div/section/div/div[1]/div[3]/p[1]','Entraîneur')

    # オーナー
    h_owner = func01('/html/body/div[1]/div/div/section/div/div[1]/div[3]/p[2]','Sous les couleurs de')

    # 生産者
    h_breeder = func01('/html/body/div[1]/div/div/section/div/div[1]/div[3]/p[3]','Éleveurs')

    # 出力日
    try:
        dateNow = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")
    except:
        dateNow = ''

    # 馬齢計算
    try:
        calcA = str(dateNow).split('/')[0]
        calcB = str(h_birth).split('/')[0]
        h_age = int(calcA) - int(calcB)
    except:
        h_age = ''

    ####################
    bnrNone()
    ####################
    # smooth scroll
    def scroll():
        targetPosition = driver.find_element_by_css_selector('#engagements h2')
        targetPositionY = targetPosition.location['y'] - 500
        targetScroll = 'window.scrollTo({top:' + str(targetPositionY) + ',left:0,behavior:"smooth"});'
        driver.execute_script(targetScroll)
        time.sleep(1)
    try:
        scroll()
    except:
        pass

    ####################
    # plus button click
    def plusBtn():
        a = driver.find_elements_by_xpath('//*[@id="performances"]/div/div[2]/div/button')
        return a
    btnflg = plusBtn()
    # plusボタンがfalseになるまでスクロール＋クリック処理を繰り返し
    try:
        while(len(btnflg) > 0):
            plusBtn()[0].click()
            time.sleep(1)
            scroll()
            btnflg = plusBtn()
        else:
            pass
    except:
        pass
    ####################

    # 各レースを取得
    try:
        pfTable = driver.find_elements_by_xpath('//table[@id="performances_cheval"]/tbody/tr')
    except:
        pfTable = []

    # 出走頭数
    try:
        h_value = len(pfTable)
    except:
        h_value = ''

    ############################
    # CSV生成
    ############################
    file_hName = h_name.replace(' ','_')
    genFileName = savePath + 'francegalop02_' + file_hName + ".csv"
    logFileName = savePath + 'Err_francegalop02_' + file_hName + ".txt"
    f = open(genFileName, 'w', encoding="utf_8_sig")
    writer = csv.writer(f, lineterminator='\n')

    # 出力情報
    record01 = ['11',h_name,h_origin,h_age,h_cs,h_birth,h_rob,h_sex,h_trainer,h_owner,'',\
        h_sire,h_dam,h_damsire,h_breeder,'',h_value,targets[z],dateNow]
    print(record01)

    label02 = ['21','Date','競馬場コード','競馬場','国名','Date_L','Video',\
        'レースNo','レース名','レース格','レースType','出走条件（性齢）','出走条件（クラス）','出走条件（その他）',\
            '距離','コース形態','コース詳細','レースタイム','着差','獲得賞金','総賞金','馬体重','斤量','騎手','着順',\
                '出走頭数','オーナー','スチュワード情報','セクショナルズ']

    writer.writerow(label01)
    writer.writerow(record01)
    writer.writerow(['12'])

    # 一覧の取得情報を格納
    baseDB = []
    ####################
    # レース数ループ処理
    ####################
    for tr in range(len(pfTable)):

        rDict = {}

        relatedPath = '//table[@id="performances_cheval"]/tbody/tr[' + str(tr + 1) + ']'
        ####################
        # func02
        ####################
        def func02(b,c):
            path = relatedPath + '/' + b
            a = driver.find_element_by_xpath(path)
            if a.get_attribute('data-label') == c:
                a = a.text.strip()
            else:
                a = ''
            return a

        # 日付
        r_date = func02('td[1]','DateReunion')
        try:
            r_date = r_date.split('/')
            r_date = r_date[2] + '/' + r_date[1] + '/' + r_date[0]
        except:
            r_date = ''
        rDict['r_date'] = r_date

        # 競馬場
        rc_name = func02('td[2]','Hippodrome')
        rDict['rc_name'] = rc_name

        # 競馬場コード/国名
        #rc_code = []
        #rc_country = []
        #xi = rc_name.split('(')[0].strip()
        #for i in rc_list:
        #    if xi == i[3]:
        #        rc_code.append(i[0])
        #        rc_country.append(i[1])
        #    else:
        #        pass
        #if len(rc_code) > 0:
        #    rc_code = rc_code[0]
        #else:
        #    rc_code = ['']
        #if len(rc_country) > 0:
        #    rc_country = rc_country[0]
        #else:
        #    rc_country = ['']
        #rDict['rc_code'] = rc_code
        #rDict['rc_country'] = rc_country

        # 競馬場が仏国内の場合はレース詳細URLを取得
        try:
            p = relatedPath + '/td[1]/a'
            if ' (' in rc_name:
                r_link = ''
            else:
                r_link = driver.find_element_by_xpath(p).get_attribute('href')
        except:
            r_link = ''
        rDict['r_url'] = r_link

        # 着順
        r_num = func02('td[3]','NbPlace')
        rDict['r_num'] = r_num

        # 距離
        r_dist = func02('td[4]','DistanceParcouru')
        rDict['r_dist'] = r_dist

        # レース形態
        r_type = func02('td[5]','Discipline')
        rDict['r_type'] = r_type

        # レース格・条件
        r_grade = func02('td[6]','Categorie')
        rDict['r_grade'] = r_grade

        # 出走条件（クラス）
        r_class = func02('td[7]','CategBlackType')
        rDict['r_class'] = r_class

        # 斤量
        r_wgt = func02('td[8]','PoidsPorte')
        r_wgt = r_wgt.replace(',','.')
        rDict['r_wgt'] = r_wgt

        # オーナー
        r_owner = func02('td[9]','NomProprietaire')
        rDict['r_owner'] = r_owner

        # 獲得賞金
        r_prize = func02('td[12]','Gains')
        rDict['r_prize'] = r_prize

        # レース映像
        try:
            r_video = driver.find_element_by_xpath(relatedPath + '/td[16]/a').get_attribute('data-nom-video')
            a = r_link.split('/')[-1]
            r_video = r_link.replace(a,r_video)
        except:
            r_video = ''
        rDict['r_video'] = r_video

        print(rDict)
        baseDB.append(rDict)

    # レース概要
    for tr in range(len(pfTable)):
        db = baseDB[tr]
        record02 = ['22',db['r_date'],'',db['rc_name'],'',db['r_url'],db['r_video'],'','',db['r_grade'],db['r_type'],\
            '',db['r_class'],'',db['r_dist'],'','','','',db['r_prize'],'','',db['r_wgt'],'',db['r_num'],'','','','']

        label03 = ['31','競馬場コード','競馬場詳細','国名','レース日付','レース名','レース格','レースNo','レース Type','レース他',\
            'レース名省略','出走条件','馬場の種類','出走条件（性別）','出走条件（クラス）','出走条件（その他）','出走条件（年齢）',\
                '距離','コース回り','コース形態','コース詳細','馬場状態','障害数','障害レース確認','総賞金','着賞金','並び順位',\
                    '確定順位','異常区分','同着','着変更','馬番号','ゲート番号','着差1','着差2','馬名','生産国','オッズ',\
                        '馬齢','馬種','馬体重','斤量','斤量特記1','斤量特記2','補助馬具','調教師','騎手','毛色','性別',\
                            '父名','母名','母父名','出走頭数','優勝馬タイム','オーナー','生産者','コメント']

        writer.writerow(label02)



        # レース詳細に遷移
        if len(db['r_url']) > 0:
            driver.get(db['r_url'])
            # cookieバナー削除
            bnrNone()
            # スチュワード情報の可視化
            def visible():
                try:
                    sc = "txt = document.querySelector('.infotip.commissaire .txt');\
                        txt.style.cssText = 'opacity:1; visibility:visible'"
                    driver.execute_script(sc)
                    time.sleep(1)
                except:
                    pass
            visible()
            ##############################
            # レース情報01
            ##############################
            try:
                r_info01 = driver.find_element_by_css_selector('.course-detail > p:nth-of-type(1)')
            except:
                r_info01 = ''
            ##############################
            # レース名*
            ##############################
            try:
                r_name = driver.find_element_by_css_selector('h1').text.strip()
            except:
                r_name = ''
            record02[8] = r_name
            ##############################
            # レースNo*
            ##############################
            try:
                r_order = r_info01.text.split('(')[0].strip()
            except:
                r_order = ''
            record02[7] = r_order
            ##############################
            # 競馬場*
            ##############################
            try:
                rc_name_dt = r_info01.text.split(',')[-1].strip()
            except:
                rc_name_dt = ''
            ##############################
            # 競馬場コード/国名
            ##############################
            try:
                print('競馬場名: ' + db['rc_name'])
                rc_code = []
                rc_country = []
                for i in rc_list:
                    if db['rc_name'] == i[3]:
                        rc_code.append(i[0])
                        rc_country.append(i[1])
                    else:
                        pass
                if len(rc_code) > 0:
                    rc_code = rc_code[0]
                else:
                    rc_code = ['']
                if len(rc_country) > 0:
                    rc_country = rc_country[0]
                else:
                    rc_country = ['']
            except:
                pass
            record02[2] = rc_code
            record02[4] = rc_country
            ##############################
            # レース条件（クラス）
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
            # 総賞金
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
            record02[20] = r_prize
            ##############################
            # 出走頭数
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
            record02[25] = h_sValue
            ##############################
            # レースタイム（結果）
            ##############################
            try:
                r_time = r_info02.text.split('Temps du 1er :')[1].split('\n')[0].strip()
            except:
                r_time = ''
            record02[17] = r_time
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
            try:
                xi = r_info02.text.split('\n')[0].strip()
                if 'Terrain ' in xi:
                    rc_condition = xi.split('Terrain ')[1].strip()
                else:
                    rc_condition = ''
            except:
                rc_condition = ''
            ##############################
            # レース情報03*
            ##############################
            try:
                r_info03 = driver.find_element_by_css_selector('.course-detail > p:nth-of-type(3)')
            except:
                r_info03 = ''
            ##############################
            # レース格（詳細）
            ##############################
            try:
                r_grade_d = r_info03.find_element_by_css_selector('strong').text.strip()
            except:
                r_grade_d = ''
            ##############################
            # 出走条件（性齢）
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
            record02[11] = r_cond01
            # 出走条件（性別）
            try:
                if ' au-dessus' in r_cond01 or ' ans' in r_cond01:
                    try:
                        r_sCond = r_cond01.split(' ans')[0].strip()
                        r_sCond = r_sCond + ' ans'
                    except:
                        r_sCond = r_cond01.split(' au-dessus')[0].strip()
                        r_sCond = r_sCond + ' au-dessus'
                else:
                    r_sCond = ''
            except:
                r_sCond = ''
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
            # スチュワード
            ##############################
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
            record02[27] = steward
            ##############################
            # セクショナルズ
            ##############################
            try:
                xi = r_info02.get_attribute('innerHTML')
                if '="pdf_course_trackee' in xi:
                    pdflink = driver.find_element_by_css_selector('.pdf_course_trackee').get_attribute('href')
                else:
                    pdflink = ''
            except:
                pdflink = ''
            record02[28] = pdflink
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
            # 出走頭数（実頭数）
            ##############################
            try:
                h_value = len(tr)
            except:
                h_value = 0
            ##############################
            # 確定着順
            ##############################
            h_num = table[0]
            h_num = [x.text.strip() for x in h_num]
            ErElem(h_num,h_value)
            ##############################
            # 並び順位
            ##############################
            num = []
            for r in range(len(h_num)):
                num.append(str(r+1))
            ##############################
            # 馬番号
            ##############################
            h_rNum = table[2]
            h_rNum = [x.text.strip() for x in h_rNum]
            ##############################
            # ゲート番号
            ##############################
            h_gate = copy.copy(table[5])
            if len(h_gate) == 0:
                h_gate = copy.copy(table[4])
            for i in range(len(h_gate)):
                try:
                    h_gate[i] = h_gate[i].text.split('Corde:')[1].replace(')','').strip()
                except:
                    h_gate[i] = ''
            ##############################
            # 異常区分
            ##############################
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
            ##############################
            # 同着
            ##############################
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
            # 確定着順と賞金を照合
            ##############################
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
            # 着差
            ##############################
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
            oriCheck01 = []
            oriCheck02 = []
            for i in table[12]:
                oriCheck01.append(i.text.strip())
            for i in table[13]:
                oriCheck02.append(i.text.strip())
            for i in range(h_value):
                if len(oriCheck01[i]) > 0 or len(oriCheck02[i]) > 0:
                    oriCheck.append('FR')
                else:
                    oriCheck.append('')
            ##############################
            # 馬名 / 生産国 / 性別 / 馬種 / 馬齢
            ##############################
            h_info = []
            ##############################
            # 馬齢
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
            # 馬種
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
            # 性別
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
            # 生産国
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
            # 馬名
            ##############################
            h_rName = [x.strip() for x in h_info]
            ##############################
            # 調教師
            ##############################
            h_rTrainer = table[7]
            h_rTrainer = [x.text.strip() for x in h_rTrainer]
            ##############################
            # 騎手
            ##############################
            h_rJockey = table[8]
            h_rJockey = [x.text.strip() for x in h_rJockey]
            # 該当馬の騎手名を特定
            r_jockey = ''
            try:
                for i in range(len(h_rName)):
                    if h_name == h_rName[i]:
                        r_jockey = h_rJockey[i]
                    else:
                        pass
            except:
                pass
            record02[23] = r_jockey
            ##############################
            # 生産者
            ##############################
            h_rBreeder = table[11]
            h_rBreeder = [x.text.strip() for x in h_rBreeder]
            ##############################
            # オーナー
            ##############################
            h_rOwner = table[6]
            h_rOwner = [x.text.strip() for x in h_rOwner]
            ##############################
            # 斤量（結果）
            ##############################
            h_wgt = table[9]
            h_wgt = [x.text.strip().replace(',','.') for x in h_wgt]
            ##############################
            # 斤量特記1（結果）
            ##############################
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


            writer.writerow(record02)
            writer.writerow(label03)
            ##############################
            # レコード出力
            ##############################
            for r in range(len(h_rName)):
                if re.match(r'\d', h_old[r]):
                    pass
                else:
                    h_old[r] = ''
                record03 = ['32',rc_code,rc_name_dt,rc_country,db['r_date'],r_name,r_grade_d,r_order,r_type_d,'','',\
                    r_cond01,rc_type,'',r_dClass,r_kCond,'',r_dist_d,rc_way,'','',rc_condition,'','','',num_prize[r],num[r],h_num[r],h_status[r],r_dht[r],'',\
                        h_rNum[r],h_gate[r],h_margin[r],'',h_rName[r],h_rOrigin[r],'',h_old[r],h_type[r],'',h_wgt[r],h_wgt1[r],'',h_aid[r],\
                            h_rTrainer[r],h_rJockey[r],'',h_rSex[r],h_rSire[r],h_rDam[r],h_rDamsire[r],h_sValue,r_time,h_rOwner[r],h_rBreeder[r],'']
                writer.writerow(record03)
                print(record03)

        else:
            writer.writerow(record02)


driver.quit()
##終了時刻をエポック秒で取得（処理時間の計算用）
e_time = time.time()
p_time = e_time - s_time
##処理時間の表示
print('処理時間（秒）: ' + str(p_time))
sys.exit()