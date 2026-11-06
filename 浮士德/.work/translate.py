from pathlib import Path
import json,re,sys,urllib.request,urllib.parse,time,concurrent.futures,hashlib,threading,random,difflib

sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parent
PAGES=json.loads(ROOT.joinpath('source_layout.json').read_text(encoding='utf-8'))
TERMS=json.loads(ROOT.joinpath('glossary.json').read_text(encoding='utf-8'))
CACHE=ROOT/'cache';CACHE.mkdir(exist_ok=True)

CHAPTERS=[
(16,'DEDICATION','题献'),(17,'PRELUDE IN THE THEATER','剧院序幕'),(25,'PROLOGUE IN HEAVEN','天上序曲'),(29,'NIGHT','夜'),(47,'OUTSIDE THE CITY GATE','城门外'),(61,'FAUST’S STUDY (a)','浮士德的书斋 一'),(74,'FAUST’S STUDY (b)','浮士德的书斋 二'),(96,'AUERBACH’S WINE CELLAR IN LEIPZIG','莱比锡的奥尔巴赫酒窖'),(112,'WITCH’S KITCHEN','女巫的厨房'),(125,'STREET','街道'),(128,'EVENING','傍晚'),(134,'PROMENADE','散步道'),(136,'THE NEIGHBOR’S HOUSE','邻居的家'),(145,'A STREET','一条街道'),(147,'GARDEN','花园'),(155,'A SMALL SUMMER ARBOR','花园中的小凉亭'),(157,'FOREST AND CAVERN','森林与岩洞'),(163,'GRETCHEN’S ROOM','格蕾琴的房间'),(164,'MARTHA’S GARDEN','玛尔特的花园'),(171,'AT THE WELL','井边'),(173,'BY THE CITY WALL','城墙边'),(174,'NIGHT','夜'),(181,'CATHEDRAL','大教堂'),(183,'WALPURGIS NIGHT','瓦尔普吉斯之夜'),(197,'GLOOMY DAY. A FIELD','阴沉的白昼 田野'),(201,'NIGHT. OPEN COUNTRY','夜 空旷的原野'),(202,'DUNGEON','地牢'),
(214,'A PLEASANT LANDSCAPE, TWILIGHT','幽美的风景 曙光初现'),(218,'IMPERIAL PALACE','皇宫'),(232,'A SPACIOUS HALL','宽敞的大厅'),(259,'PLEASURE GARDEN','御花园'),(268,'A DARK GALLERY','幽暗的长廊'),(274,'BRIGHTLY LIGHTED HALLS','灯火通明的厅堂'),(278,'HALL OF THE KNIGHTS','骑士大厅'),(289,'A HIGH-VAULTED NARROW GOTHIC CHAMBER','穹顶高耸的狭窄哥特式房间'),(300,'LABORATORY','实验室'),(308,'THE PHARSALIAN PLAIN. DARKNESS','法萨卢斯平原 黑夜'),(312,'ON THE UPPER PENEIOS','珀涅俄斯河上游'),(320,'ON THE LOWER PENEIOS','珀涅俄斯河下游'),(330,'ON THE UPPER PENEIOS AS BEFORE','珀涅俄斯河上游 先前的地方'),(351,'ROCKBOUND BAYS OF THE AEGEAN SEA','爱琴海的岩石海湾'),(371,'INNER COURTYARD OF FAUST’S CASTLE','浮士德城堡的内院'),(382,'ARCADIA','阿卡狄亚'),(402,'HIGH MOUNTAINS','高山'),(415,'IN THE FOOTHILLS','山麓'),(433,'THE RIVAL EMPEROR’S TENT','敌对皇帝的营帐'),(445,'OPEN COUNTRY','空旷的原野'),(449,'PALACE','宫殿'),(454,'DEEP NIGHT','深夜'),(457,'MIDNIGHT','午夜'),(463,'GREAT FORECOURT OF THE PALACE','宫殿前的大庭院'),(468,'INTERMENT','安葬'),(478,'MOUNTAIN GORGES','山峡')]
ROLES={
'DIRECTOR':'剧院经理','POET':'诗人','JESTER':'丑角','THE LORD':'上帝','RAPHAEL':'拉斐尔','GABRIEL':'加百列','MICHAEL':'米迦勒','FAUST':'浮士德','MEPHISTOPHELES':'梅菲斯特','SPIRIT':'地灵','SPIRITS':'众精灵','WAGNER':'瓦格纳','CHOIR OF ANGELS':'天使合唱队','CHOIR OF WOMEN':'妇女合唱队','CHOIR OF DISCIPLES':'门徒合唱队','SOME APPRENTICES':'几个学徒','OTHERS':'其他人','FIRST GROUP':'第一群人','SECOND GROUP':'第二群人','ONE APPRENTICE':'一个学徒','SECOND APPRENTICE':'第二个学徒','THIRD APPRENTICE':'第三个学徒','FOURTH APPRENTICE':'第四个学徒','FIFTH APPRENTICE':'第五个学徒','SERVANT GIRL':'女仆','ANOTHER':'另一个人','FIRST GIRL':'第一个姑娘','SECOND GIRL':'第二个姑娘','FIRST STUDENT':'第一个学生','SECOND STUDENT':'第二个学生','FIRST CITIZEN':'第一个市民','SECOND CITIZEN':'第二个市民','THIRD CITIZEN':'第三个市民','FIRST CITIZEN’S DAUGHTER':'第一个市民的女儿','SECOND CITIZEN’S DAUGHTER':'第二个市民的女儿','A BEGGAR':'乞丐','OLD WOMAN':'老妇人','SOLDIERS':'士兵们','PEASANTS':'农民们','PEASANT CROWD':'农民们','OLD PEASANT':'老农','CHORUS OF INVISIBLE SPIRITS':'无形精灵的合唱','STUDENT':'学生','FROSCH':'弗罗施','BRANDER':'勃兰德','SIEBEL':'西贝尔','ALTMAYER':'阿尔特迈尔','CHORUS':'合唱','ALL':'众人','WITCH':'女巫','MONKEYS':'猴子们','MALE MONKEY':'公猴','FEMALE MONKEY':'母猴','BOTH MONKEYS':'两只猴子','GRETCHEN':'格蕾琴','MARTHA':'玛尔特','LIESCHEN':'莉丝琴','VALENTINE':'瓦伦丁','EVIL SPIRIT':'恶灵','CHOIR':'合唱队','PEOPLE':'众人','WILL-O’-THE-WISP':'鬼火','VOICE':'声音','VOICES':'众声','WITCHES':'女巫们','WARLOCKS':'男巫们','WARLOCKS AND WITCHES':'男女巫师们','HALF-WITCH':'半个女巫','HUCKSTER WITCH':'卖杂货的女巫','THE PRETTY ONE':'年轻漂亮的女巫','THE OLD ONE':'老女巫','ARIEL':'阿里埃尔','CHORUS OF ELVES':'小精灵合唱队','EMPEROR':'皇帝','SQUIRE':'侍从','SECOND SQUIRE':'第二个侍从','FOOL':'弄臣','CHANCELLOR':'宰相','COMMANDER-IN-CHIEF':'统帅','TREASURER':'财政大臣','STEWARD':'宫廷总管','ASTROLOGER':'占星师','HERALD':'传令官','FLOWER GIRLS':'卖花姑娘们','GARDENERS':'园丁们','MOTHER':'母亲','WOODCUTTERS':'伐木工们','PULCINELLI':'普尔钦内拉丑角们','PARASITES':'食客们','DRUNKARD':'醉汉','AGLAIA':'阿格莱亚','HEGEMONE':'赫革摩涅','EUPHROSYNE':'欧弗洛绪涅','ZOILO-THERSITES':'佐伊洛斯忒耳西忒斯','BOY DRIVER':'驾车少年','BOY CHARIOTEER':'驾车少年','PLUTUS':'普路托斯','STARVELING':'瘦饿鬼','WOMEN GOSSIPS':'闲谈的妇女们','LEADER OF THE WOMEN':'妇女领头人','CROWD OF WOMEN':'妇女们','MURMURS FROM THE CROWD':'人群中的低语','CRIES FROM THE CROWD':'人群中的呼喊','THE CROWD':'人群','MISER':'吝啬鬼','TUMULT AND SINGING':'喧闹与歌声','WILD MEN SINGING':'野人们的歌','FAUNS':'法乌恩牧神们','SATYR':'萨堤尔','GNOMES':'地精们','NYMPHS IN CHORUS':'仙女们合唱','DEPUTATION OF GNOMES TO GREAT PAN':'晋见大神潘的地精代表团','FIRST PAGE':'第一个侍童','SECOND PAGE':'第二个侍童','FIRST CHAMBERLAIN':'第一个侍从官','SECOND CHAMBERLAIN':'第二个侍从官','FIRST BANNERET':'第一个旗骑士','SECOND BANNERET':'第二个旗骑士','CHAMBERLAIN':'侍从官','BLONDE':'金发女子','BRUNETTE':'黑发女子','LADY':'贵妇','PAGE':'侍童','ARCHITECT':'建筑师','FIRST LADY':'第一位贵妇','SECOND LADY':'第二位贵妇','FOURTH LADY':'第四位贵妇','FIFTH LADY':'第五位贵妇','SIXTH LADY':'第六位贵妇','FIRST KNIGHT':'第一个骑士','SECOND KNIGHT':'第二个骑士','A KNIGHT':'一个骑士','A LADY':'一位贵妇','ANOTHER LADY':'另一位贵妇','YOUNG LADY':'年轻贵妇','YOUNGER LADY':'较年轻的贵妇','OLDER LADY':'年长贵妇','OLDEST LADY':'最年长的贵妇','COURTIER':'廷臣','DIPLOMAT':'外交官','DUENNA':'女监护人','PEDANT':'学究','FAMULUS':'助手','BACCALAUREATE':'学士','HOMUNCULUS':'荷蒙库鲁斯','ERICHTHO':'厄里克托','GRIFFIN':'狮鹫','GRIFFINS':'狮鹫们','GIANT ANTS':'巨蚁们','ARIMASPS':'阿里马斯波独眼人','SPHINX':'斯芬克斯','SPHINXES':'斯芬克斯们','FIRST GRIFFIN':'第一只狮鹫','SECOND GRIFFIN':'第二只狮鹫','BOTH GRIFFINS':'两只狮鹫','SIRENS':'塞壬们','PENEIOS':'珀涅俄斯河神','NYMPHS':'仙女们','CHIRON':'喀戎','MANTO':'曼托','SEISMOS':'塞斯摩斯','CHORUS OF GIANT ANTS':'巨蚁合唱队','PYGMIES':'俾格米侏儒们','DACTYLS':'达克堤尔指精们','PYGMY ELDERS':'侏儒长老们','PYGMY GENERALISSIMO':'侏儒大元帅','GIANT ANTS AND DACTYLS':'巨蚁与指精们','THE CRANES OF IBYKUS':'伊比库斯的鹤群','LAMIAE':'拉弥亚女妖们','EMPUSA':'恩普萨','OREAD':'山岳仙女','DRYAD':'树木仙女','ANAXAGORAS':'阿那克萨戈拉','THALES':'泰勒斯','PHORKYAS':'福耳库阿斯','ONE':'其中一个','THE OTHERS':'其余的人','PROTEUS':'普罗透斯','NEREUS':'涅柔斯','CHORUS OF TELCHINES':'忒尔喀涅斯众神的合唱','TELCHINES':'忒尔喀涅斯众神','DORIDS':'多里斯众女','THE YOUTHS':'青年们','GALATEA':'伽拉忒亚','ALL AS ONE':'全体齐声','CHORUS OF CAPTIVE TROJAN WOMEN':'被俘的特洛伊妇女合唱队','PANTHALIS':'潘塔莉丝','HELEN':'海伦','LYNCEUS THE WATCHMAN':'守望人林叩斯','LYNCEUS':'林叩斯','HELEN, FAUST, CHORUS':'海伦 浮士德 合唱队','EUPHORION':'欧福里翁','GIRL':'姑娘','EUPHORION’S VOICE':'欧福里翁的声音','FULL CHORUS':'全体合唱','PART OF THE CHORUS':'一部分合唱队','A SECOND PART':'第二部分合唱队','A THIRD PART':'第三部分合唱队','A FOURTH PART':'第四部分合唱队','BRAWLER':'好斗者','GRABBER':'抢夺者','HOARDER':'囤积者','BODYGUARDS':'侍卫们','FIRST SCOUT':'第一个侦察兵','SECOND SCOUT':'第二个侦察兵','HERALDS':'传令官们','QUICKLOOT':'快掠女','IMPERIAL GUARDS':'皇帝的卫兵们','FIRST GUARD':'第一个卫兵','SECOND GUARD':'第二个卫兵','THIRD GUARD':'第三个卫兵','FOURTH GUARD':'第四个卫兵','LORD MARSHALL':'宫廷元帅','LORD CHAMBERLAIN':'内侍总管','LORD STEWARD':'御膳总管','LORD CUPBEARER':'御酒总管','CHANCELLOR-ARCHBISHOP':'宰相兼大主教','WANDERER':'旅人','BAUCIS':'鲍西丝','PHILEMON':'菲勒蒙','THE THREE VIOLENT GIANTS':'三个凶暴的巨人','FIRST WOMAN':'第一个老妇','SECOND WOMAN':'第二个老妇','THIRD WOMAN':'第三个老妇','FOURTH WOMAN':'第四个老妇','WANT':'匮乏','DEBT':'负债','NEED':'困顿','CARE':'忧愁','WANT, DEBT, NEED':'匮乏 负债 困顿','LEMURS':'勒穆尔亡灵们','LEMUR':'一个勒穆尔亡灵','LEMUR CHORUS':'勒穆尔亡灵合唱队','THE HEAVENLY HOST':'天上众军','CHORUS OF ANGELS':'天使合唱队','THE ANGELS':'众天使','CHORUS AND ECHO':'合唱与回声','PATER ECSTATICUS':'Pater Ecstaticus（狂喜的神父）','PATER PROFUNDUS':'Pater Profundus（沉思的神父）','PATER SERAPHICUS':'Pater Seraphicus（炽爱的神父）','CHOIR OF BLESSED BOYS':'蒙福男童合唱队','THE BLESSED BOYS':'蒙福的男童们','CHORUS OF BLESSED BOYS':'蒙福男童合唱队','ANGELS':'天使们','THE YOUNGER ANGELS':'年轻的天使们','THE MORE PERFECT ANGELS':'更臻完善的天使们','DOCTOR MARIANUS':'玛利亚博士','CHORUS OF PENITENT WOMEN':'忏悔妇女合唱队','MAGNA PECCATRIX':'Magna Peccatrix（罪孽深重的女人）','MULIER SAMARITANA':'Mulier Samaritana（撒马利亚妇人）','MARIA AEGYPTIACA':'Maria Aegyptiaca（埃及的玛利亚）','ALL THREE':'三人齐声','ONE OF THE PENITENTS':'一位忏悔的女子','THE SINGLE PENITENT':'那位忏悔的女子','MATER GLORIOSA':'Mater Gloriosa（荣光圣母）','CHORUS MYSTICUS':'Chorus Mysticus（神秘的合唱）'
}
OCR_ROLES={'POEL':'POET','POEM':'POET','JES CER':'JESTER','THEILORD':'THE LORD','JAELORD':'THE LORD','THEO':'THE LORD','THESLORD)':'THE LORD','MEPEOSTOPHELES':'MEPHISTOPHELES','MEPHISTOPTMEVES':'MEPHISTOPHELES','MEPHISTOPHELESs':'MEPHISTOPHELES','PAUST':'FAUST','PAUSE':'FAUST','PAUSI':'FAUST','FAUSIL':'FAUST','BAUS T':'FAUST','PAUS I':'FAUST','BAUST':'FAUST','PAUSTI':'FAUST','SPIRED':'SPIRIT','SPIRMI':'SPIRIT','SPIRIMS':'SPIRITS','CHOIR OF DISGIPLES':'CHOIR OF DISCIPLES','STUDENE':'STUDENT','SLUDEN TE':'STUDENT','SEUDENT':'STUDENT','FROSGH':'FROSCH','PROSCH':'FROSCH','EROSCH':'FROSCH','SIEBELE':'SIEBEL','SEBEL':'SIEBEL','SIEDEE':'SIEBEL','SLEBEL':'SIEBEL','SIEBEE':'SIEBEL','ALT MAYER':'ALTMAYER','GRETGHEN':'GRETCHEN','GRETCHENS':'GRETCHEN','GRELCHEN':'GRETCHEN','GREITGHEN':'GRETCHEN','IME SCHEN':'LIESCHEN','DIESGHEN':'LIESCHEN','BYTE SPURITs':'EVIL SPIRIT','THE PREITY ONE':'THE PRETTY ONE','GHORUS':'CHORUS','ZOILO-THERSET ES':'ZOILO-THERSITES','CHOIR OFANSEGIS':'CHOIR OF ANGELS','DAGIYES':'DACTYLS','HALES':'THALES','FLHALES':'THALES','EELALES':'THALES','LL':'ALL','TOMUNCULUS':'HOMUNCULUS','EIELEN':'HELEN','ELEN':'HELEN','COMMANDER-IN-CHIEE':'COMMANDER-IN-CHIEF','DEBE':'DEBT'}
ROLES.update({'NEREIDS AND TRITONS':'涅瑞伊得斯海仙女与特里同们','PSYLLI AND MARSI':'普叙利人与马耳西人','HELEN AND FAUST':'海伦与浮士德','MEPHISTOPHELES AND THE THREE':'梅菲斯特与三个巨人'})

FOREIGN={
'“Eritis sicut Deus, scientes bonum et malum.”':'“Eritis sicut Deus, scientes bonum et malum.”\n“你们便如上帝一样，能够辨别善恶。”',
'Sancta simplicitas!':'Sancta simplicitas!\n多么神圣的天真啊！',
'Dies irae, dies illa,':'Dies irae, dies illa,\n震怒之日，那审判之日，',
'Solvet saeclum in favilla.':'Solvet saeclum in favilla.\n将把尘世化作灰烬。',
'Judex ergo cum sedebit,':'Judex ergo cum sedebit,\n当审判者登上宝座，',
'Quidquid latet adparebit,':'Quidquid latet adparebit,\n一切隐情都将显露，',
'Nil inultum remanebit.':'Nil inultum remanebit.\n没有罪恶可以逃脱惩罚。',
'Quid sum miser tunc dicturus?':'Quid sum miser tunc dicturus?\n那时，我这可怜的人还能说什么？',
'Quem patronum rogaturus?':'Quem patronum rogaturus?\n我又能请求谁为我辩护？',
'Cum vix justus sit securus.':'Cum vix justus sit securus.\n连义人也难以保全自身。'
}

def glossary(s):
    # Replace longest names first to keep compounds intact. Case-sensitive common words are excluded.
    for a,b in sorted(TERMS.items(),key=lambda x:-len(x[0])):
        if a=='Paris':continue # Paris can mean either the city or the Trojan prince.
        s=re.sub(r'(?<![A-Za-z])'+re.escape(a)+r'(?![A-Za-z])',b,s,flags=re.I)
    for a,b in [('Care','忧愁'),('Mater Dolorosa','Mater Dolorosa（痛苦圣母）'),('Knittelvers','Knittelvers（克尼特尔诗体）'),('Sorge','Sorge（忧愁）'),('Logos','Logos（逻各斯）')]:
        s=s.replace(a,b)
    return s

def clean_lines(page):
    n=page['pdf_page'];lines=[re.sub(r'\s{2,}',' ',l.strip()) for l in page['text'].splitlines() if l.strip()]
    # Verified against the laid-out scan: all numbered play pages end in page furniture.
    if 16<=n<=488 and n!=213 and lines:lines=lines[:-1]
    # Running page number / author / book-title lines are not book content.
    def is_footer(l,i):
        if re.fullmatch(r'[\d\W]+',l):return True
        if 'GOETHE' in l and len(l)<55 and i>len(lines)-5:return True
        if re.search(r'\bPART\s+(ONE|TWO|Twi|alw|TWION)',l,re.I) and i>len(lines)-5:return True
        if i>len(lines)-5 and len(l)<85 and (re.search(r'G[O0]?\s*[ER][T7]?\s*[HNI]?[Eis]?\b',l,re.I) or re.search(r'\bGOETHE\b',l)) and not re.search(r'[a-z]{4}',l):return True
        if i>len(lines)-3 and len(l)<70 and re.search(r'[A-Z]{2}',l) and re.search(r'\d',l) and not re.search(r'[a-z]{3}',l):return True
        return False
    lines=[l for i,l in enumerate(lines) if not is_footer(l,i)]
    # Last OCR lines are title/author page furniture on most narrative pages.
    while lines and 16<=n<=488:
        l=lines[-1]
        if (len(l)<75 and not re.search(r'[a-z]{3}',l) and not l.endswith((':','!','?','.',';','—'))
            and (sum(c.isupper() for c in l)>3 or re.search(r'\d',l))):
            if l in ROLES or l.rstrip(':;.') in ROLES:break
            lines.pop()
        else:break
    replacements={"youre":"you're","youve":"you've","youll":"you'll","youd":"you'd","were":"were","Dont":"Don't","dont":"don't","isnt":"isn't","werent":"weren't","couldnt":"couldn't","Pll":"I'll","Pl ":"I'll ","Im ":"I'm ","lve":"I've","we ll":"we'll","Biichner":"Büchner","cletis":"clefts"}
    out=[]
    for l in lines:
        for a,b in replacements.items():l=re.sub(r'\b'+re.escape(a),lambda m:b,l)
        if l.startswith('(Io '):l='(To '+l[4:]
        for a,b in [('(Jo ','(To '),('(Zo ','(To '),('(fo ','(To '),('(1o ','(To '),('(7o ','(To '),('(Jn ','(In '),('(/n ','(In '),('(Szngs.)','(Sings.)'),('(Aszde.)','(Aside.)'),('(/ronically.)','(Ironically.)'),('(A¢ ','(At '),('(Afier ','(After '),('(Odserving ','(Observing ')]:l=l.replace(a,b)
        if l in ['ANUS, FRASRET TONE:','ASUIRID) LANDING','SVB CO GOR GEE','SO eon aeip','267 een eC Or ETE']:continue
        if l=='a aes :':continue
        if l=='PAW oa:':l='FAUST:'
        for a,b in [('NEREIDS and TRITONS:','NEREIDS AND TRITONS:'),('PSYLLI and MARSI:','PSYLLI AND MARSI:'),('HELEN and FAUST:','HELEN AND FAUST:'),('MEPHISTOPHELES and THE THREE:','MEPHISTOPHELES AND THE THREE:'),('i LADY:','A LADY:'),('NEPTUNE: trident',"NEPTUNE'S trident"),('The EMPEROR: tent',"The EMPEROR'S tent"),('HELEN’: clothes',"HELEN'S clothes")]:l=l.replace(a,b)
        l=l.replace('GRETG@GHEN:','GRETCHEN:').replace('FAUS«:','FAUST:').replace('CHORUS OFANSEGIS:','CHOIR OF ANGELS:').replace('-ROTEUS:','PROTEUS:').replace('CHORUS and ECHO:','CHORUS AND ECHO:').replace('clefis','clefts')
        for a,b in [('MEPHIS TOPHELES','MEPHISTOPHELES'),('MEPHIS TOPHELES','MEPHISTOPHELES')]:l=l.replace(a,b)
        if n==289 and l=='GOTHIC CHAMBER':continue
        out.append(l)
    return out

def make_units():
    units=[];unknown=set();chapter_lookup={n:(i+1,a,b) for i,(n,a,b) in enumerate(CHAPTERS)}
    for pg in PAGES:
        n=pg['pdf_page']
        if not (16<=n<=488):continue
        lines=clean_lines(pg)
        buf=[];preface=False
        def flush():
            if buf:
                s='\n'.join(buf);units.append({'page':n,'kind':'stage' if preface else 'verse','source':s});buf.clear()
        for i,l in enumerate(lines):
            ch=chapter_lookup.get(n)
            if ch and re.match(r'^[XLIVTU]{1,8}\s+[x~=«<\-\s]+',l) and len(l)>7:
                flush();units.append({'page':n,'kind':'heading','source':l,'translation':f'第{ch[0]}场  {ch[2]}'});preface=True;continue
            if l.startswith('ACT '):
                flush();act={214:'第一幕',289:'第二幕',371:'第三幕',402:'第四幕',445:'第五幕'}.get(n)
                if act:units.append({'page':n,'kind':'act','source':l,'translation':act})
                continue
            if l=='CLASSICAL WALPURGIS NIGHT':
                flush();units.append({'page':n,'kind':'subheading','source':l,'translation':'古典的瓦尔普吉斯之夜'});continue
            if l in FOREIGN:
                flush();units.append({'page':n,'kind':'foreign','source':l,'translation':FOREIGN[l]});continue
            m=re.match(r'^([A-Z][A-Z ,’\x27\-]*[A-Za-z)]?)(?:[:;.]|(?=\s*\())(?:\s*(.*))?$',l)
            cand=m.group(1).strip() if m else l
            key=OCR_ROLES.get(cand,cand)
            if key not in ROLES and key.startswith('ME') and len(key)>11 and key.upper()==key:
                key='MEPHISTOPHELES'
            if key not in ROLES and m and len(key)>6:
                close=difflib.get_close_matches(key,ROLES,n=1,cutoff=.84)
                if close:key=close[0]
            if key in ROLES and not (preface and not re.search(r'[:;]',l)):
                flush();preface=False;units.append({'page':n,'kind':'speaker','source':cand,'translation':ROLES[key],'role':key})
                rest=m.group(2).strip() if m and m.group(2) else ''
                if rest:units.append({'page':n,'kind':'stage','source':rest})
                continue
            if l.upper()==l and len(l)>3 and not re.search(r'[a-z]',l):unknown.add((n,l))
            if l.startswith('(') and l.endswith(')'):
                flush();units.append({'page':n,'kind':'stage','source':l});continue
            buf.append(l)
        flush()
    # A header split by OCR should still appear exactly once.
    for n,(i,en,zh) in chapter_lookup.items():
        if not any(u['kind']=='heading' and u['page']==n for u in units):
            at=next(i for i,u in enumerate(units) if u['page']==n)
            units.insert(at,{'page':n,'kind':'heading','source':en,'translation':f'第{i}场  {zh}'})
    for i,u in enumerate(units):u['id']=i
    ROOT.joinpath('units.json').write_text(json.dumps(units,ensure_ascii=False,indent=2),encoding='utf-8')
    ROOT.joinpath('unknown_caps.json').write_text(json.dumps(sorted(unknown),ensure_ascii=False,indent=2),encoding='utf-8')
    return units

def fetch(s):
    key=hashlib.sha256(s.encode()).hexdigest();path=CACHE/(key+'.json')
    if path.exists():return json.loads(path.read_text(encoding='utf-8'))['translation']
    params={'client':'gtx','sl':'en','tl':'zh-CN','dt':'t','q':s}
    url='https://translate.googleapis.com/translate_a/single?'+urllib.parse.urlencode(params)
    for attempt in range(7):
        try:
            req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
            with urllib.request.urlopen(req,timeout=45) as r:data=json.load(r)
            t=''.join(x[0] or '' for x in data[0])
            if not t.strip():raise ValueError('empty translation')
            path.write_text(json.dumps({'source':s,'translation':t},ensure_ascii=False),encoding='utf-8')
            return t
        except Exception:
            if attempt==6:raise
            time.sleep(min(2**attempt,20)+random.random())

def translate_batch(batch):
    def source_text(u):
        s=re.sub(r'(?<=[A-Za-z])-\s*\n\s*(?=[a-z])','',u['source'])
        s=s.replace('|','I').replace('I I','I')
        for a,b in [("[ve","I've"),("[’ll","I'll"),("[ll","I'll"),("Pm","I'm"),("Pve","I've"),("Vd","I'd"),("Vl","I'll"),("VII","I'll"),("P’ve","I've"),("V’ll","I'll"),("T believe","I believe"),("T don't","I don't")]:s=s.replace(a,b)
        s=s.replace('\n',' ')
        s=s.replace('HOMUNCULWUS','HOMUNCULUS').replace('FAUS 1','FAUST')
        return glossary(s)
    s='\n\n'.join(f'@@U{u["id"]:05d}@@\n'+source_text(u) for u in batch)
    t=fetch(s)
    matches=list(re.finditer(r'@\s*@\s*U\s*(\d{5})\s*@\s*@',t,re.I))
    result={}
    for i,m in enumerate(matches):result[int(m.group(1))]=t[m.end():matches[i+1].start() if i+1<len(matches) else len(t)].strip()
    if set(result)!=set(u['id'] for u in batch):
        result={u['id']:fetch(source_text(u)) for u in batch}
    return result

if __name__=='__main__':
    oldmap={}
    if ROOT.joinpath('translated.json').exists():
        for u in json.loads(ROOT.joinpath('translated.json').read_text(encoding='utf-8')):
            if 'translation' in u:oldmap[(u['page'],u['kind'],u['source'])]=u['translation']
    units=make_units()
    for u in units:
        k=(u['page'],u['kind'],u['source'])
        repair=('--repair-pronouns' in sys.argv and re.search(r"\||\[(?:[’']?ll|ve|m|d)|\b(?:Pm|Pve|Vd|Vl|VII)\b|P’ve|V’ll|\bT (?:believe|don't)",u['source']))
        if k in oldmap and 'translation' not in u and '--reflow' not in sys.argv and not repair:u['translation']=oldmap[k]
    if '--prepare-only' in sys.argv:
        print('prepared',len(units),'units',len(CHAPTERS),'chapters');sys.exit()
    batches=[];b=[];size=0
    for u in units:
        if 'translation' in u:continue
        x=len(u['source'])+25
        if b and (size+x>2500 or b[-1]['page']!=u['page']):batches.append(b);b=[];size=0
        b.append(u);size+=x
    if b:batches.append(b)
    print('translation_batches',len(batches),'units',len(units),flush=True)
    done=0;errors=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        jobs={pool.submit(translate_batch,b):b for b in batches}
        for f in concurrent.futures.as_completed(jobs):
            b=jobs[f]
            try:
                d=f.result()
                for u in b:u['translation']=d[u['id']]
            except Exception as e:errors.append((b[0]['page'],str(e)))
            done+=1
            if done%20==0 or done==len(batches):
                print('completed',done,'/',len(batches),'errors',len(errors),flush=True)
                ROOT.joinpath('translated.json').write_text(json.dumps(units,ensure_ascii=False,indent=2),encoding='utf-8')
                ROOT.joinpath('progress.json').write_text(json.dumps({'done':done,'total':len(batches),'errors':errors},ensure_ascii=False),encoding='utf-8')
    print('finished',len(errors),'errors',errors,flush=True)
