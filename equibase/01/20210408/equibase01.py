# -*- coding: utf-8 -*-
import csv
import xml.etree.ElementTree as ET
import glob
import re
try:
    from tkinter import messagebox
except:
    pass
import sys

##############################
# setting.txt
##############################
setting_f = open('setting.txt', 'r', encoding='UTF-8')
settings = setting_f.read()
settings = settings.split('\n')
settings = [x for x in settings if x != '']
##############################
##############################
# usa_race-case-other.txt
##############################
# 出走条件（その他）の設定ファイル
raceType_f = open('usa_race-case-other.txt', 'r', encoding='UTF-8')
race_T_type = raceType_f.read()
race_T_type = race_T_type.split('\n')
race_T_type = [x for x in race_T_type if x != '']
print(race_T_type)

xmlFiles = []
fileNames = []
csvFiles = []
# importフォルダ配下のファイルを検索
files = glob.glob('import/*')
for file in files:
    # XMLファイルをxmlFilesリストに格納
    if '.xml' in file:
        xmlFiles.append(file)

for s in range(len(xmlFiles)):
    fileElem = xmlFiles[s].replace('.xml','.csv')
    csvFiles.append(fileElem)

for z in range(len(xmlFiles)):
    # XMLデータの読み込み
    try:
        tree = ET.parse(str(xmlFiles[z])) 
        root = tree.getroot()
    except:
        try:
            messagebox.showerror('ERROR', 'XMLの読み込みに失敗しました')
            sys.exit()
        except:
            print('XML読み込みエラー')
            sys.exit()

    # CSVデータの読み込み
    try:
        with open (str(csvFiles[z]), 'r' ) as f:
            reader = csv.reader(f)
            line = [row for row in reader]
    except:
        try:
            messagebox.showerror('ERROR', 'CSVの読み込みに失敗しました')
            sys.exit()
        except:
            print('CSV読み込みエラー')
            sys.exit()

    # NAME取得（XML）
    nameElems = []
    for elem in root.iter('NAME'):
        nameElem = elem.text
        nameElems.append(nameElem)
    nameElem = nameElems[0]
    if nameElem == None:
        rp_name = ''
    else:
        rp_name = nameElem + ' RACE    '

    # RACE_TEXT内の距離を取得
    distElems = []
    for elem in root.iter('RACE_TEXT'):
        distElem = elem.text.replace('    ',' ')
        distElem = re.split('RACE \d+',distElem)[1]
        for i in range(len(settings)):
            if settings[i] in distElem:
                distElem = distElem.split(settings[i])[0].strip()
        distElems.append(distElem)

    ############################
    # function
    ############################
    # root
    def getElems01(y):
        x = []
        for elem in root.iter(y):
            z = elem.text
            x.append(z)
        for i in range(len(x)):
            if x[i] == None:
                x[i] = ''
            else:
                pass
        return x

    # child
    def getElements02(y,a):
        x = []
        spElem = root.findall('RACE')
        for i in range(len(spElem)):
            elems = spElem[i].findall(y)
            x.append([])
            for k in range(len(elems)):
                z = elems[k].find(a).text
                x[i].append(z)
            for k in range(len(x[i])):
                if x[i][k] == None:
                    x[i][k] = ''
        return x

    # grandchild 
    def getElements03(y,a,b):
        x = []
        spElem = root.findall('RACE')
        for i in range(len(spElem)):
            elems = spElem[i].findall(y)
            x.append([])
            for k in range(len(elems)):
                z = elems[k].find(a)
                if z == None:
                    x[i].append('')
                else:
                    z = z.find(b)
                    if z == None:
                        pass
                    else:
                        z = z.text
                    x[i].append(z)
            for k in range(len(x[i])):
                if x[i][k] == None:
                    x[i][k] = ''
        return x

    # great grandchild
    def getElements04(y,a,b,c):
        x = []
        spElem = root.findall('RACE')
        for i in range(len(spElem)):
            elems = spElem[i].findall(y)
            x.append([])
            for k in range(len(elems)):
                z = elems[k].find(a).find(b)
                if z == None:
                    x[i].append('')
                else:
                    z = z.find(c).text
                    x[i].append(z)
        return x
    ############################
    # COURSE_ID取得
    course_id = getElems01('COURSE_ID')
    # COURSE_ID取得
    course_desc = getElems01('COURSE_DESC')
    # SURFACE取得
    surface = getElems01('SURFACE')
    # DH_DQ_FLAGS取得
    dh_dq_flags = getElements02('ENTRY','DH_DQ_FLAGS')
    # BREED取得
    breed = getElements02('ENTRY','BREED')
    # MEDS取得
    meds = getElements02('ENTRY','MEDS')
    # EQUIP取得
    equip = getElements02('ENTRY','EQUIP')
    ############################
    # JOCKEY
    ############################
    # JOCKEY > FIRST_NAME取得
    j_firstName = getElements03('ENTRY','JOCKEY','FIRST_NAME')
    # JOCKEY > MIDDLE_NAME取得
    j_middleName = getElements03('ENTRY','JOCKEY','MIDDLE_NAME')
    # JOCKEY > LAST_NAME取得
    j_lastName = getElements03('ENTRY','JOCKEY','LAST_NAME')
    # JOCKEY > SUFFIX取得
    j_suffix = getElements03('ENTRY','JOCKEY','SUFFIX')
    # JOCKEY > KEY取得
    j_key = getElements03('ENTRY','JOCKEY','KEY')
    # JOCKEY > TYPE取得
    j_type = getElements03('ENTRY','JOCKEY','TYPE')
    ############################
    # TRAINER
    ############################
    # TRAINER > FIRST_NAME取得
    t_firstName = getElements03('ENTRY','TRAINER','FIRST_NAME')
    # TRAINER > FIRST_NAME取得
    t_middleName = getElements03('ENTRY','TRAINER','MIDDLE_NAME')
    # TRAINER > LAST_NAME取得
    t_lastName = getElements03('ENTRY','TRAINER','LAST_NAME')
    # TRAINER > SUFFIX取得
    t_suffix = getElements03('ENTRY','TRAINER','SUFFIX')
    # TRAINER > KEY取得
    t_key = getElements03('ENTRY','TRAINER','KEY')
    # TRAINER > TYPE取得
    t_type = getElements03('ENTRY','TRAINER','TYPE')
    # AXCISKEY取得
    axciskey = getElements02('ENTRY','AXCISKEY')
    #WINNERS_DETAILS > COLOR > CODE取得
    colorCode = getElements04('ENTRY','WINNERS_DETAILS','COLOR','CODE')
    #WINNERS_DETAILS > COLOR > DESCRIPTION取得
    colorDesc = getElements04('ENTRY','WINNERS_DETAILS','COLOR','DESCRIPTION')
    # SIRE取得
    sire = getElements03('ENTRY','WINNERS_DETAILS','SIRE')
    # DAM取得
    dam = getElements03('ENTRY','WINNERS_DETAILS','DAM')
    # DAM_SIRE取得
    damsire = getElements03('ENTRY','WINNERS_DETAILS','DAM_SIRE')
    # BREEDER取得
    breeder = getElements03('ENTRY','WINNERS_DETAILS','BREEDER')
    #WINNERS_DETAILS > BRED_LOCATION > CODE取得
    bredCode = getElements04('ENTRY','WINNERS_DETAILS','BRED_LOCATION','CODE')
    #WINNERS_DETAILS > BRED_LOCATION > DESCRIPTION取得
    bredDesc = getElements04('ENTRY','WINNERS_DETAILS','BRED_LOCATION','DESCRIPTION')


    r_FIELD1 = []
    r_FIELD2 = []
    r_FIELD3 = []
    r_FIELD4 = []
    r_FIELD5 = []
    r_FIELD6 = []
    r_FIELD7 = []
    r_FIELD8 = []
    r_FIELD9 = []
    r_FIELD10 = []
    r_FIELD11 = []
    r_FIELD12 = []
    r_FIELD13 = []
    r_FIELD14 = []
    r_FIELD15 = []
    r_FIELD16 = []
    r_FIELD17 = []
    r_FIELD18 = []
    r_FIELD19 = []
    r_FIELD20 = []
    r_FIELD21 = []
    r_FIELD22 = []
    r_FIELD23 = []
    r_FIELD24 = []
    r_FIELD25 = []
    r_FIELD26 = []
    r_FIELD27 = []
    r_FIELD28 = []
    r_FIELD29 = []
    r_FIELD30 = []
    r_FIELD31 = []
    r_FIELD32 = []
    r_FIELD33 = []
    r_FIELD34 = []
    r_FIELD35 = []
    r_FIELD36 = []
    r_FIELD37 = []
    r_FIELD38 = []
    r_FIELD39 = []
    r_FIELD40 = []
    r_FIELD41 = []
    r_FIELD42 = []
    r_FIELD43 = []
    r_FIELD44 = []
    r_FIELD45 = []
    r_FIELD46 = []
    r_FIELD47 = []
    r_FIELD48 = []
    r_FIELD49 = []
    r_FIELD50 = []
    r_FIELD51 = []
    r_FIELD52 = []
    r_FIELD53 = []
    r_FIELD54 = []
    r_FIELD55 = []
    r_FIELD56 = []
    r_FIELD57 = []
    r_FIELD58 = []
    r_FIELD59 = []
    r_FIELD60 = []
    r_FIELD61 = []
    r_FIELD62 = []
    r_FIELD63 = []
    r_FIELD64 = []
    r_FIELD65 = []
    r_FIELD66 = []
    r_FIELD67 = []
    r_FIELD68 = []
    r_FIELD69 = []
    r_FIELD70 = []
    r_FIELD71 = []
    r_FIELD72 = []
    r_FIELD73 = []
    r_FIELD74 = []
    r_FIELD75 = []
    r_FIELD76 = []
    r_FIELD77 = []
    r_FIELD78 = []
    r_FIELD79 = []
    r_FIELD80 = []
    r_FIELD81 = []
    r_FIELD82 = []
    r_FIELD83 = []
    r_FIELD84 = []
    r_FIELD85 = []
    r_FIELD86 = []

    h_FIELD1 = []
    h_FIELD2 = []
    h_FIELD3 = []
    h_FIELD4 = []
    h_FIELD5 = []
    h_FIELD6 = []
    h_FIELD7 = []
    h_FIELD8 = []
    h_FIELD9 = []
    h_FIELD10 = []
    h_FIELD11 = []
    h_FIELD12 = []
    h_FIELD13 = []
    h_FIELD14 = []
    h_FIELD15 = []
    h_FIELD16 = []
    h_FIELD17 = []
    h_FIELD18 = []
    h_FIELD19 = []
    h_FIELD20 = []
    h_FIELD21 = []
    h_FIELD22 = []
    h_FIELD23 = []
    h_FIELD24 = []
    h_FIELD25 = []
    h_FIELD26 = []
    h_FIELD27 = []
    h_FIELD28 = []
    h_FIELD29 = []
    h_FIELD30 = []
    h_FIELD31 = []
    h_FIELD32 = []
    h_FIELD33 = []
    h_FIELD34 = []
    h_FIELD35 = []
    h_FIELD36 = []
    h_FIELD37 = []
    h_FIELD38 = []
    h_FIELD39 = []
    h_FIELD40 = []
    h_FIELD41 = []

    for s in range(len(line) - 1):
        if line[s][2].isdigit() == False:
            # race record
            r_FIELD1.append(line[s][0].strip()) # Record Indicator
            r_FIELD2.append(line[s][1].strip()) # Race Breed Type
            r_FIELD3.append(line[s][2].strip()) # 3 Char Track Code
            r_FIELD4.append(line[s][3].strip()) # Date (YYYYMMDD)
            r_FIELD5.append(line[s][4].strip()) # Race Number
            r_FIELD6.append(line[s][5].strip()) # D=Day Card E=Evening
            r_FIELD7.append(line[s][6].strip()) # Race Type
            r_FIELD8.append(line[s][7].strip()) # Purse Value
            r_FIELD9.append(line[s][8].strip()) # Race Text(1)
            r_FIELD10.append(line[s][9].strip()) # Race Text(2)
            r_FIELD11.append(line[s][10].strip()) # Race Text(3)
            r_FIELD12.append(line[s][11].strip()) # Race Text(4)
            r_FIELD13.append(line[s][12].strip()) # Abbrev. Conditions
            r_FIELD14.append(line[s][13].strip()) # Distance
            r_FIELD15.append(line[s][14].strip()) # Distance Unit
            r_FIELD16.append(line[s][15].strip()) # A= About Distance
            r_FIELD17.append(line[s][16].strip()) # Surface
            r_FIELD18.append(line[s][17].strip()) # Class Rating
            r_FIELD19.append(line[s][18].strip()) # Track Condition
            r_FIELD20.append(line[s][19].strip()) # Weather
            r_FIELD21.append(line[s][20].strip()) # Start (Post who broke)
            r_FIELD22.append(line[s][21].strip()) # Post Time
            r_FIELD23.append(line[s][22].strip()) # Daily Track Variant
            r_FIELD24.append(line[s][23].strip()) # First Fraction Time
            r_FIELD25.append(line[s][24].strip()) # Second Fraction Time
            r_FIELD26.append(line[s][25].strip()) # Third Fraction Time
            r_FIELD27.append(line[s][26].strip()) # Fourth Fraction Time
            r_FIELD28.append(line[s][27].strip()) # Fifth Fraction Time
            r_FIELD29.append(line[s][28].strip()) # Winning Time
            r_FIELD30.append(line[s][29].strip()) # Lead 1st Call Pace
            r_FIELD31.append(line[s][30].strip()) # Lead 2nd Call Pace
            r_FIELD32.append(line[s][31].strip()) # Winners Speed Rating
            r_FIELD33.append(line[s][32].strip()) # Par Time
            r_FIELD34.append(line[s][33].strip()) # Purse Split
            r_FIELD35.append(line[s][34].strip()) # Purse Split
            r_FIELD36.append(line[s][35].strip()) # Purse Split
            r_FIELD37.append(line[s][36].strip()) # Purse Split
            r_FIELD38.append(line[s][37].strip()) # Purse Split
            r_FIELD39.append(line[s][38].strip()) # Purse Split
            r_FIELD40.append(line[s][39].strip()) # Purse Split
            r_FIELD41.append(line[s][40].strip()) # Purse Split
            r_FIELD42.append(line[s][41].strip()) # Purse Split
            r_FIELD43.append(line[s][42].strip()) # Purse Split
            r_FIELD44.append(line[s][43].strip()) # Exotic Wager
            r_FIELD45.append(line[s][44].strip()) # Exotic Paid Numbers
            r_FIELD46.append(line[s][45].strip()) # Exotic Pay Out
            r_FIELD47.append(line[s][46].strip()) # Exotic Wager Pool
            r_FIELD48.append(line[s][47].strip()) # Exotic Wager
            r_FIELD49.append(line[s][48].strip()) # Exotic Paid Numbers
            r_FIELD50.append(line[s][49].strip()) # Exotic Pay Out
            r_FIELD51.append(line[s][50].strip()) # Exotic Wager Pool
            r_FIELD52.append(line[s][51].strip()) # Exotic Wager
            r_FIELD53.append(line[s][52].strip()) # Exotic Paid Numbers
            r_FIELD54.append(line[s][53].strip()) # Exotic Pay Out
            r_FIELD55.append(line[s][54].strip()) # Exotic Wager Pool
            r_FIELD56.append(line[s][55].strip()) # Exotic Wager
            r_FIELD57.append(line[s][56].strip()) # Exotic Paid Numbers
            r_FIELD58.append(line[s][57].strip()) # Exotic Pay Out
            r_FIELD59.append(line[s][58].strip()) # Exotic Wager Pool
            r_FIELD60.append(line[s][59].strip()) # Exotic Wager
            r_FIELD61.append(line[s][60].strip()) # Exotic Paid Numbers
            r_FIELD62.append(line[s][61].strip()) # Exotic Pay Out
            r_FIELD63.append(line[s][62].strip()) # Exotic Wager Pool
            r_FIELD64.append(line[s][63].strip()) # Exotic Wager
            r_FIELD65.append(line[s][64].strip()) # Exotic Paid Numbers
            r_FIELD66.append(line[s][65].strip()) # Exotic Pay Out
            r_FIELD67.append(line[s][66].strip()) # Exotic Wager Pool
            r_FIELD68.append(line[s][67].strip()) # Exotic Wager
            r_FIELD69.append(line[s][68].strip()) # Exotic Paid Numbers
            r_FIELD70.append(line[s][69].strip()) # Exotic Pay Out
            r_FIELD71.append(line[s][70].strip()) # Exotic Wager Pool
            r_FIELD72.append(line[s][71].strip()) # Exotic Wager
            r_FIELD73.append(line[s][72].strip()) # Exotic Paid Numbers
            r_FIELD74.append(line[s][73].strip()) # Exotic Pay Out
            r_FIELD75.append(line[s][74].strip()) # Exotic Wager Pool
            r_FIELD76.append(line[s][75].strip()) # Exotic Wager
            r_FIELD77.append(line[s][76].strip()) # Exotic Paid Numbers
            r_FIELD78.append(line[s][77].strip()) # Exotic Pay Out
            r_FIELD79.append(line[s][78].strip()) # Exotic Wager Pool
            r_FIELD80.append(line[s][79].strip()) # Exotic Wager
            r_FIELD81.append(line[s][80].strip()) # Exotic Paid Numbers
            r_FIELD82.append(line[s][81].strip()) # Exotic Pay Out
            r_FIELD83.append(line[s][82].strip()) # Exotic Wager Pool
            r_FIELD84.append(line[s][83].strip()) # Claims(Horse;$;Owner;)
            r_FIELD85.append(line[s][84].strip()) # Wind Direction
            r_FIELD86.append(line[s][85].strip()) # Wind Speed
        else:
            # horse record
            h_FIELD1.append(line[s][0].strip()) # Record Indicator
            h_FIELD2.append(line[s][1].strip()) # 3 Char Track Code
            h_FIELD3.append(line[s][2].strip()) # Date (YYYYMMDD)
            h_FIELD4.append(line[s][3].strip()) # Race Number
            h_FIELD5.append(line[s][4].strip()) # D=Day Card E=Evening
            h_FIELD6.append(line[s][5].strip()) # Last Race
            h_FIELD7.append(line[s][6].strip()) # Breed Type
            h_FIELD8.append(line[s][7].strip()) # Horse Name
            h_FIELD9.append(line[s][8].strip()) # Horse Weight
            h_FIELD10.append(line[s][9].strip()) # Horse Age
            h_FIELD11.append(line[s][10].strip()) # Sex (M,C,F,G,H)
            h_FIELD12.append(line[s][11].strip()) # Med / Equip
            h_FIELD13.append(line[s][12].strip()) # Jockey Name
            h_FIELD14.append(line[s][13].strip()) # Odds / $
            h_FIELD15.append(line[s][14].strip()) # Program #
            h_FIELD16.append(line[s][15].strip()) # Post Position
            h_FIELD17.append(line[s][16].strip()) # Claim Value
            h_FIELD18.append(line[s][17].strip()) # Start Call
            h_FIELD19.append(line[s][18].strip()) # 1st Call Position
            h_FIELD20.append(line[s][19].strip()) # 1st Call Lengths
            h_FIELD21.append(line[s][20].strip()) # 2nd Call Position
            h_FIELD22.append(line[s][21].strip()) # 2nd Call Lengths
            h_FIELD23.append(line[s][22].strip()) # 3rd Call Position
            h_FIELD24.append(line[s][23].strip()) # 3rd Call Lengths
            h_FIELD25.append(line[s][24].strip()) # 4th Call Position
            h_FIELD26.append(line[s][25].strip()) # 4th Call Lengths
            h_FIELD27.append(line[s][26].strip()) # Stretch Call Position
            h_FIELD28.append(line[s][27].strip()) # Stretch Call Lengths
            h_FIELD29.append(line[s][28].strip()) # Original Finish
            h_FIELD30.append(line[s][29].strip()) # Lengths Behind Leader
            h_FIELD31.append(line[s][30].strip()) # Official Finish
            h_FIELD32.append(line[s][31].strip()) # Individual Horse Time(QH Only)
            h_FIELD33.append(line[s][32].strip()) # Speed Rating
            h_FIELD34.append(line[s][33].strip()) # Trainer
            h_FIELD35.append(line[s][34].strip()) # Owner
            h_FIELD36.append(line[s][35].strip()) # Race Comments
            h_FIELD37.append(line[s][36].strip()) # Winners Information
            h_FIELD38.append(line[s][37].strip()) # Pay Win
            h_FIELD39.append(line[s][38].strip()) # Pay Place
            h_FIELD40.append(line[s][39].strip()) # Pay Show
            h_FIELD41.append(line[s][40].strip()) # Pay Show(DeadHeat)

    # 抽出データを出力するためのCSVを作成
    FileName = csvFiles[z].split('\\')[1].split('.csv')[0]
    FileName = 'export\\' + FileName + '_merge.csv'
    f = open(FileName, 'w', encoding="utf_8_sig")
    writer = csv.writer(f, lineterminator='\n')
    label01 = ['Date (YYYYMMDD)','3 Char Track Code','NAME','Race Number','Race Breed Type','D=Day Card E=Evening','Race Type'] 
    label02 = ['Purse Value','Race Text(1)','Race Text(2)','Race Text(3)','Race Text(4)','Abbrev. Conditions','Distance XML','Distance']
    label03 = ['Distance Unit','A= About Distance','COURSE_ID','COURSE_DESC','Surface','Class Rating','Track Condition','Weather']
    label04 = ['Start (Post who broke)','Post Time','Daily Track Variant','First Fraction Time','Second Fraction Time','Third Fraction Time']
    label05 = ['Fourth Fraction Time','Fifth Fraction Time','Winning Time','Lead 1st Call Pace','Lead 2nd Call Pace','Winners Speed Rating','Par Time']
    label06 = ['Purse Split_1','Purse Split_2','Purse Split_3','Purse Split_4','Purse Split_5','Purse Split_&','Purse Split_7','Purse Split_8','Purse Split_9','Purse Split_10']
    label07 = ['Exotic Wager 1','Exotic Wager Pool 1','Exotic Paid Numbers 1','Exotic Pay Out 1','Exotic Wager 2','Exotic Wager Pool 2','Exotic Paid Numbers 2','Exotic Pay Out 2']
    label08 = ['Exotic Wager 3','Exotic Wager Pool 3','Exotic Paid Numbers 3','Exotic Pay Out 3','Exotic Wager 4','Exotic Wager Pool 4','Exotic Paid Numbers 4','Exotic Pay Out 4']
    label09 = ['Exotic Wager 5','Exotic Wager Pool 5','Exotic Paid Numbers 5','Exotic Pay Out 5','Exotic Wager 6','Exotic Wager Pool 6','Exotic Paid Numbers 6','Exotic Pay Out 6']
    label10 = ['Exotic Wager 7','Exotic Wager Pool 7','Exotic Paid Numbers 7','Exotic Pay Out 7','Exotic Wager 8','Exotic Wager Pool 8','Exotic Paid Numbers 8','Exotic Pay Out 8']
    label11 = ['Exotic Wager 9','Exotic Wager Pool 9','Exotic Paid Numbers 9','Exotic Pay Out 9','Exotic Wager 10','Exotic Wager Pool 10','Exotic Paid Numbers 10','Exotic Pay Out 10']
    label12 = [' Claims(Horse;$;Owner;)','Wind Direction','Wind Speed']
    labelFix01 = label01 + label02 + label03 + label04 + label05 + label06 + label12

    label13 = ['Horse Name','DH_DQ_FLAGS','BREED8','Last Race','Horse Weight','Horse Age','Sex (M,C,F,G,H)','Med / Equip','MEDS','EQUIP','Odds / $','Program #']
    label14 = ['Post Position','Claim Value','Start Call','1st Call Position','1st Call Lengths','2nd Call Position','2nd Call Lengths']
    label15 = ['3rd Call Position','3rd Call Lengths','4th Call Position','4th Call Lengths','Stretch Call Position','Stretch Call Lengths']
    label16 = ['Original Finish','Lengths Behind Leader','Official Finish','着変更','Speed Rating']
    label17 = ['Jockey Name_CSV','Jockey Name - FIRST_NAME','Jockey Name - MIDDLE_NAME','Jockey Name - LAST_NAME','Jockey_key','Trainer_CSV','Trainer Name - FIRST_NAME','Trainer Name - MIDDLE_NAME','Trainer Name - LAST_NAME','Trainer_key']
    label18 = ['Owner','Race Comments','Winners Information','Pay Win','Pay Place','Pay Show','Pay Show(DeadHeat)','AXCISKEY']
    labelFix02 = label13 + label14 + label15 + label16 + label17 + label18

    labelFix = labelFix01 + labelFix02 + label07 + label08 + label09 + label10 + label11 + ['出走条件（他）']
    writer.writerow(labelFix)

    # 出走頭数を算出
    c_nums = []
    c_nums.append(h_FIELD4.count('1'))
    c_nums.append(h_FIELD4.count('2'))
    c_nums.append(h_FIELD4.count('3'))
    c_nums.append(h_FIELD4.count('4'))
    c_nums.append(h_FIELD4.count('5'))
    c_nums.append(h_FIELD4.count('6'))
    c_nums.append(h_FIELD4.count('7'))
    c_nums.append(h_FIELD4.count('8'))
    c_nums.append(h_FIELD4.count('9'))
    c_nums.append(h_FIELD4.count('10'))
    c_nums.append(h_FIELD4.count('11'))
    c_nums.append(h_FIELD4.count('12'))
    c_nums.append(h_FIELD4.count('13'))
    c_nums.append(h_FIELD4.count('14'))
    c_nums.append(h_FIELD4.count('15'))
    c_nums.append(h_FIELD4.count('16'))
    c_nums.append(h_FIELD4.count('17'))
    c_nums.append(h_FIELD4.count('18'))
    c_nums.append(h_FIELD4.count('19'))
    c_nums.append(h_FIELD4.count('20'))
    c_nums.append(h_FIELD4.count('21'))
    c_nums.append(h_FIELD4.count('22'))
    c_nums.append(h_FIELD4.count('23'))
    c_nums.append(h_FIELD4.count('24'))
    c_nums.append(h_FIELD4.count('25'))
    c_nums.append(h_FIELD4.count('26'))
    c_nums.append(h_FIELD4.count('27'))
    c_nums.append(h_FIELD4.count('28'))
    c_nums.append(h_FIELD4.count('29'))
    c_nums.append(h_FIELD4.count('30'))

    # レース数の精査
    for s in range(len(c_nums)):
        if c_nums[s] == 0:
            c_nums[s] = ''
    c_nums = [x for x in c_nums if x != '']

    h_f8 = [] # Horse Name
    h_f6 = [] # Last Race
    h_f9 = [] # Horse Weight
    h_f10 = [] # Horse Age
    h_f11 = [] # Sex (M,C,F,G,H)
    h_f12 = [] # Med / Equip
    h_f13 = [] # Jockey Name
    h_f14 = [] # Odds / $
    h_f15 = [] # Program #
    h_f16 = [] # Post Position
    h_f17 = [] # Claim Value
    h_f18 = [] # Start Call
    h_f19 = [] # 1st Call Position
    h_f20 = [] # 1st Call Lengths
    h_f21 = [] # 2nd Call Position
    h_f22 = [] # 2nd Call Lengths
    h_f23 = [] # 3rd Call Position
    h_f24 = [] # 3rd Call Lengths
    h_f25 = [] # 4th Call Position
    h_f26 = [] # 4th Call Lengths
    h_f27 = [] # Stretch Call Position
    h_f28 = [] # Stretch Call Lengths
    h_f29 = [] # Original Finish
    h_f30 = [] # Lengths Behind Leader
    h_f31 = [] # Official Finish
    h_f33 = [] # Speed Rating
    h_f34 = [] # Trainer
    h_f35 = [] # Owner
    h_f36 = [] # Race Comments
    h_f37 = [] # Winners Information
    h_f38 = [] # Pay Win
    h_f39 = [] # Pay Place
    h_f40 = [] # Pay Show
    h_f41 = [] # Pay Show(DeadHeat)

    a = 0
    for s in range(len(r_FIELD1)):
        b = c_nums[s]
        h_f8.append(h_FIELD8[a:a + b])
        h_f6.append(h_FIELD6[a:a + b])
        h_f9.append(h_FIELD9[a:a + b])
        h_f10.append(h_FIELD10[a:a + b])
        h_f11.append(h_FIELD11[a:a + b])
        h_f12.append(h_FIELD12[a:a + b])
        h_f13.append(h_FIELD13[a:a + b])
        h_f14.append(h_FIELD14[a:a + b])
        h_f15.append(h_FIELD15[a:a + b])
        h_f16.append(h_FIELD16[a:a + b])
        h_f17.append(h_FIELD17[a:a + b])
        h_f18.append(h_FIELD18[a:a + b])
        h_f19.append(h_FIELD19[a:a + b])
        h_f20.append(h_FIELD20[a:a + b])
        h_f21.append(h_FIELD21[a:a + b])
        h_f22.append(h_FIELD22[a:a + b])
        h_f23.append(h_FIELD23[a:a + b])
        h_f24.append(h_FIELD24[a:a + b])
        h_f25.append(h_FIELD25[a:a + b])
        h_f26.append(h_FIELD26[a:a + b])
        h_f27.append(h_FIELD27[a:a + b])
        h_f28.append(h_FIELD28[a:a + b])
        h_f29.append(h_FIELD29[a:a + b])
        h_f30.append(h_FIELD30[a:a + b])
        h_f31.append(h_FIELD31[a:a + b])
        h_f33.append(h_FIELD33[a:a + b])
        h_f34.append(h_FIELD34[a:a + b])
        h_f35.append(h_FIELD35[a:a + b])
        h_f36.append(h_FIELD36[a:a + b])
        h_f37.append(h_FIELD37[a:a + b])
        h_f38.append(h_FIELD38[a:a + b])
        h_f39.append(h_FIELD39[a:a + b])
        h_f40.append(h_FIELD40[a:a + b])
        h_f41.append(h_FIELD41[a:a + b])

        a = a + b

    for s in range(len(h_f8)):
        if len(h_f8[s]) == 0:
            h_f8[s] = ''
    h_f8 = [x for x in h_f8 if x != '']

    def mtNum(a):
        #if len(a) < 30:
        #    math = 30 - len(a)
        #    for i in range(math):
        #        a.append('')

        for s in range(len(c_nums)):
            if c_nums[s] > len(a[s]):
                math = c_nums[s] - len(a[s])
                for i in range(math):
                    a[s].append('')

    # DH_DQ_FLAGS
    mtNum(dh_dq_flags)
    # BREED
    mtNum(breed)
    # MEDS
    mtNum(meds)
    # EQUIP
    mtNum(equip)
    # 騎手
    mtNum(j_firstName)
    mtNum(j_middleName)
    mtNum(j_lastName)
    mtNum(j_key)
    # 調教師
    mtNum(t_firstName)
    mtNum(t_middleName)
    mtNum(t_lastName)
    mtNum(t_key)
    # AXCISKEY
    mtNum(axciskey)

    for s in range(len(r_FIELD1)):

        # 出走条件（他）
        r_other = []
        txtChk = str(r_FIELD9[s]) + str(r_FIELD10[s]) + str(r_FIELD11[s]) + str(r_FIELD12[s])
        for c in range(len(race_T_type)):
            if re.search(race_T_type[c], txtChk):
                r_other.append(race_T_type[c])
            else:
                r_other.append('')
        r_other = [x for x in r_other if x != '']
        r_other = ','.join(r_other).strip()

        r_record01 = [r_FIELD4[s],r_FIELD3[s],nameElem,r_FIELD5[s],r_FIELD2[s],r_FIELD6[s],r_FIELD7[s],r_FIELD8[s]]
        r_record02 = [r_FIELD9[s],r_FIELD10[s],r_FIELD11[s],r_FIELD12[s],r_FIELD13[s],distElems[s],r_FIELD14[s],r_FIELD15[s]]
        r_record03 = [r_FIELD16[s],course_id[s],course_desc[s],r_FIELD17[s],r_FIELD18[s],r_FIELD19[s],r_FIELD20[s],r_FIELD21[s]]
        r_record04 = [r_FIELD22[s],r_FIELD23[s],r_FIELD24[s],r_FIELD25[s],r_FIELD26[s],r_FIELD27[s],r_FIELD28[s],r_FIELD29[s],r_FIELD30[s]]
        r_record05 = [r_FIELD31[s],r_FIELD32[s],r_FIELD33[s],r_FIELD34[s],r_FIELD35[s],r_FIELD36[s],r_FIELD37[s],r_FIELD38[s]]
        r_record06 = [r_FIELD39[s],r_FIELD40[s],r_FIELD41[s],r_FIELD42[s],r_FIELD43[s]]
        r_record07 = [r_FIELD44[s],r_FIELD47[s],r_FIELD45[s],r_FIELD46[s],r_FIELD48[s],r_FIELD51[s],r_FIELD49[s],r_FIELD50[s]]
        r_record08 = [r_FIELD52[s],r_FIELD55[s],r_FIELD53[s],r_FIELD54[s],r_FIELD56[s],r_FIELD59[s],r_FIELD57[s],r_FIELD58[s]]
        r_record09 = [r_FIELD60[s],r_FIELD63[s],r_FIELD61[s],r_FIELD62[s],r_FIELD64[s],r_FIELD67[s],r_FIELD65[s],r_FIELD66[s]]
        r_record10 = [r_FIELD68[s],r_FIELD71[s],r_FIELD69[s],r_FIELD70[s],r_FIELD72[s],r_FIELD75[s],r_FIELD73[s],r_FIELD74[s]]
        r_record11 = [r_FIELD76[s],r_FIELD79[s],r_FIELD77[s],r_FIELD78[s],r_FIELD80[s],r_FIELD83[s],r_FIELD81[s],r_FIELD82[s]]
        r_record12 = [r_FIELD84[s],r_FIELD85[s],r_FIELD86[s]]
        r_recordFix01 = r_record01 + r_record02 + r_record03 + r_record04 + r_record05 + r_record06 + r_record12
        r_recordFix02 = r_record07 + r_record08 + r_record09 + r_record10 + r_record11 + [r_other]
        for i in range(len(h_f8[s])):
            #　着変更の照合
            if h_f29[s][i] == h_f31[s][i]:
                cc = ''
            else:
                cc = '*'
            h_record01 = [h_f8[s][i],dh_dq_flags[s][i],breed[s][i],h_f6[s][i],h_f9[s][i],h_f10[s][i],h_f11[s][i],h_f12[s][i]]
            h_record02 = [meds[s][i],equip[s][i],h_f14[s][i],h_f15[s][i],h_f16[s][i],h_f17[s][i],h_f18[s][i]]
            h_record03 = [h_f19[s][i],h_f20[s][i],h_f21[s][i],h_f22[s][i],h_f23[s][i],h_f24[s][i],h_f25[s][i],h_f26[s][i]]
            h_record04 = [h_f27[s][i],h_f28[s][i],h_f29[s][i],h_f30[s][i],h_f31[s][i],cc,h_f33[s][i]]
            h_record05 = [h_f13[s][i],j_firstName[s][i],j_middleName[s][i],j_lastName[s][i],j_key[s][i],h_f34[s][i],t_firstName[s][i],t_middleName[s][i],t_lastName[s][i],t_key[s][i]]
            h_record06 = [h_f35[s][i],h_f36[s][i],h_f37[s][i],h_f38[s][i],h_f39[s][i],h_f40[s][i],h_f41[s][i],axciskey[s][i]]
            h_recordFix = h_record01 + h_record02 + h_record03 + h_record04 + h_record05 + h_record06
            writer.writerow(r_recordFix01 + h_recordFix + r_recordFix02)
        #print(r_recordFix)
    print(str(z + 1) + ' / ' + str(len(xmlFiles)) + ' 結合完了')