import pandas as pd
import os
import re

brackets_regex1 = re.compile( " \(.*\)" )
brackets_regex2 = re.compile( " \[.*\]" )

slovnik_link = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRsEDDBEt3VXESqAgoQLUYHvsA5yMyujzGViXiamY7-yYrcORhrkEl5g6JZPorvJrgMk6sjUlFNT4Km/pub?output=xlsx'


def load_slovnik(tabela=slovnik_link, obnoviti=False):
    if obnoviti == False and os.path.isfile("slovnik_words.pkl") and os.path.isfile("slovnik_suggestions.pkl"):
        print("Found 'slovnik_words.pkl' file, using it")
        print("Found 'slovnik_suggestions.pkl' file, using it")
        dfs = {"words": pd.read_pickle("slovnik_words.pkl"),
               "suggestions": pd.read_pickle("slovnik_suggestions.pkl")}
        return dfs

    print('Dostava slovnika...')
    dfs = pd.read_excel(io=tabela, engine='openpyxl', sheet_name=['words', 'suggestions'])
        
    dfs['suggestions'].columns = dfs['suggestions'].iloc[0]
    dfs['suggestions'].reindex(dfs['suggestions'].index.drop(0))
    dfs['suggestions'].rename(columns={'ids': 'id'}, inplace=True)
        
    for i in ['words', 'suggestions']:
        for col in dfs[i].columns:
            dfs[i][col] = dfs[i][col].fillna(' ').astype(str)
        
    dfs['words'].to_pickle("slovnik_words.pkl")
    dfs['suggestions'].to_pickle("slovnik_suggestions.pkl")

    return dfs


def load_sheet(tabela_name, sheet_names: list, tabela, obnoviti):
    ispath = [os.path.isfile(f"{tabela_name}_{name}.pkl") for name in sheet_names]
    if obnoviti == False and (False not in ispath):
        dfs = {}
        for name in sheet_names:
            sheetname = f'{tabela_name}_{name}.pkl'
            dfs.update({name: pd.read_pickle(f'{sheetname}')})
        return dfs
    print(f'Dostava tabely {tabela_name}...')
    dfs = pd.read_excel(io=tabela, engine='openpyxl', sheet_name=sheet_names)
    print('Gotovo.')    
    for name in sheet_names:
        for col in dfs[name].columns:
            dfs[name][col] = dfs[name][col].fillna(' ').astype(str)
        dfs[name].to_pickle(f"{tabela_name}_{name}.pkl")
    return dfs

def load_discord_fraznik():
    discord_list = pd.read_excel(io='https://docs.google.com/spreadsheets/d/e/2PACX-1vTIevV03tPoLIILAx4DqHH6QetiiYb13xMiQ7HMvvleWLjveoJ6uayNIDLd0cKUMj9TtNsl2XDsZR8w/pub?output=xlsx',
                    engine='openpyxl',
                    sheet_name=['tabela', 'nove slova'])
    for i in ['tabela', 'nove slova']:
        for name in discord_list[i].columns:
            discord_list[i][name] = discord_list[i][name].fillna(" ").astype(str)    
    return discord_list

def iskati_discord(jezyk, slovo, sheet):
    najdene_slova = []
    for i in range(0, len(sheet.index)):      
        cell = str( sheet[jezyk][i] )
        cell = cell.lower()
        cell = re.sub(r'\[.*?\]', '', cell)
        if jezyk == 'Vse varianty v MS':
            cell = transliteracija(cell, 'isv')
        if slovo in str.split( cell, ', ' ):
            najdene_slova.append(i)
    return najdene_slova

LANGS = "isv en ru uk be pl cs sk bg mk sr hr sl de nl eo".split(' ')

trans_tables = { #'isv_to_slovianto': 'ć-č ś-s ź-z ŕ-r ĺ-l ľ-l ń-n t́-t ť-t d́-d ď-d đ-dž ȯ-o òė-e č-č š-š ž-ž ě-ě е̌-ě ě-e å-a ę-e ų-u y-i',
                 'isv_to_standard': 'ć-č ć-č ć-č ś-s ź-z ŕ-r ĺ-l ľ-l ń-n t́-t ť-t d́-d ď-d đ-dž ò-o ȯ-o ė-e è-e č-č š-š ž-ž ě-ě е̌-ě å-a ę-e ų-u',
#                 'isv_to_cyrillic': 'ń-нь nj-њ lj-љ ĺ-ль ľ-ль ć-ч ć-ч ć-ч ś-с ź-з ŕ-р t́-т ť-т d́-д ď-д đ-дж ò-о ȯ-о ė-е è-е č-ч š-ш ž-ж ě-є е̌-є ě-є å-а ę-е ų-у a-а b-б c-ц č-ч d-д e-е f-ф g-г h-х i-и j-ј k-к l-л m-м n-н o-о p-п r-р s-с š-ш t-т u-у v-в y-ы z-з ž-ж',
                 'isv_to_cyrillic': 'ń-н ľ-л nj-њ lj-љ ć-ч ć-ч ć-ч ś-с ź-з ŕ-р t́-т ť-т d́-д ď-д đ-дж ò-о ȯ-о ė-е è-е č-ч š-ш ž-ж ě-є е̌-є ě-є å-а ę-е ų-у a-а b-б c-ц č-ч d-д e-е f-ф g-г h-х i-и j-ј k-к l-л m-м n-н o-о p-п r-р s-с š-ш t-т u-у v-в y-ы z-з ž-ж',

                 'ru': 'ё-е а́-а е́-е и́-и о́-о у́-у ы́-ы э́-э ю́-ю я́-я',
                 'uk': 'ґ-г а́-а е́-е и́-и о́-о у́-у ы́-ы є́-є ю́-ю я́-я і́-і ї́-ї',  
                 'be': 'ґ-г а́-а е́-е и́-и о́-о у́-у ы́-ы э́-э ю́-ю я́-я і́-і',  
                 'bg': 'ѝ-и',
                 'mk': 'ѝ-и ѐ-е',
                 'kir_to_lat': 'ньј-ńj ь- а-a ӑ-å б-b в-v ў-v г-g ґ-g д-d дж-dž ђ-dž е-e є-ě ѣ-ě ж-ž з-z и-i ј-j ї-ji й-j к-k л-l љ-lj м-m н-n њ-nj о-o п-p р-r с-s т-t у-u ф-f х-h ц-c ч-č ш-š щ-šč ъ-ȯ ы-y ю-ju я-ja ё-e ѫ-ų ѧ-ę ћ-ć ѥ-je ꙑ-y',     
                 'kirilicna_zamena': 'ру-ru бе-be ук-uk бг-bg мк-mk ср-sr ua-uk cz-cs ms-isv мс-isv',
}

def transliteracija(text, lang):
    if lang not in trans_tables.keys():
        return text
    replaces = (trans_tables[lang] + " " + trans_tables[lang].upper())
    for i in replaces.split(' '):
        letters = i.split('-')
        print(f"'{letters[0]}' - '{letters[1]}'")
        text = text.replace(letters[0], letters[1])
    return text

# text = """
# Prošli sųt dva dnje. Dabog ščedro dari Kamenogråd svojim Sòlncem. Gråd imaje tutčas kolory mlådoj vesny. Větr radostno dvigaje modre horųgvy, na ktoryh namaljevano jest sivo, orľje pero. One stojęt gòrdo na věžah i kamennyh plotah. Glåvny gråd Zapadnogo Vladstva izględaje gòrdo, no skromno. Pomimo svojej velikosti, mentaľnosť žiteljev gråda cěly čas jest dosť seľska i prosta. Na ulicah jest mnogo ljudij, a najmnogo v centru. Trgovišče izględaje tutčas kako poljana, na ktoroj jest veliko mnogo råzlično-kolorovyh cvětov. Kvadratny prostor gladkoj zemje među budynkami izględaje cělkom drugo v dènj, než v noći. Nahoslav ne mogl by daže pomysliti, čto oni sųt byli tut několiko dněv nazad, okrųženi temnosťjų i mråkom, pòlni straha i bojaznji. Strah i bojaznj sųt tute elementy, ktore sjedinjajųt tamtų noć i tutoj dènj. Jest tako, zato čto Bělozorjanin jest trevožny i ne čuje sę dobro, kògda on hodi među trgovymi magazinami. Kto može znati, kako dobro organizovana jest tamta grupa, ktora jih tògda pohytila i zaključila v tjuŕmě? Izględaje, že jih jest vyše, než trěh råzbojnikov. Pravdivo mlådèc i děvčina sųt v grådu pŕvo-kråtno od tamtogo momenta. No tako ili inako, jest potrěbno tut sdělati několiko děl.
# Neočekyvano on čuje trgnųťje za svoj rųkav. Fialomira oglušaje jego črne myslji i vraćaje jego do reaľnosti. Ukazyvaje ona dlånjų někakovo stojišče s žeńskym ukrašeńjem. Oni idųt tam. Děvčina spokojno ględaje blěskajųće prědmety. Našijniky, krasne naušnice, pojasy i råzličnų drugų bižuterijų. Tuto jest raj za vśako děvčę iz měščańskoj klasy. Děvkų ne zajmaje ničto drugo. Možno li ona imaje pravdų? Či bųdųt li råzbojniki prijdti tut, kògda jest jasny dènj?
# Děvčina dŕži v dlånji maly prědmet. Tuto jest zaponka / broš za oblěčeńje. Ozdoba imaje formų zorjańskoj rozy. Tuto jest simbol Bogynje Večera, toj, ktora ruměni sę, kògda vidi zahod Sòlnca. Toj, ktoroj imę jest Zorja. On jest bronzovy, a v jego srědině jest črveny, pol-prozråčny kamenj. Tuta črvenosť jest kako iskra v očah Fialomiry. Ona kråtko stoji i ględaje bižuterijų, a potom bystro běži k naslědnomu stojišču. A možno li by tako…?
# Bez nikakyh slov Nahoslav i trgovèc od togo stojišča poględajųt na sebe. Kupèc pokazyvaje dlånj i několiko pŕstov. Lovitelj bystro izimaje monety iz malogo měška, podavaje on je kupcu, hovaje ozdobų do kěšenji i skoro běži do Fialomiry.
# “Ako li my uže bųdemo najdti jej dom i odčarovati Věčnų Zimų, tògda ja bųdų dati jej tuto, kako blågodarjeńje” - mysli Našèk i momentaľno ruměni sę na licu.
# “Tuto jest dobra ideja” - on trěbuje izjasniti tuto sobě samomu.
# 	Monety… monety sųt istinno krųgle porcije drågocěnnogo metala. V mnogosti drugyh, než Srědogråd, krajin tvoręt sę monety, ale Kamenogråd jest ješče dosť mlådy gråd, itak on ne imaje svoje groše.
# 	Naško uže smogl je vzęti svoje pribory iz krčmy “Pod Orľjim Perom”. On koněčno imaje svoj meč i lųk. Želězno orųžje jest na pojasu pri jego boku, a lųk jest oblěčeny tętivojų o rųkų. Lovitelj na hrebetu imaje koževy sòdŕžnik, v ktorom jest několiko-nadsęť strěl. On hvala tomu čuje sę nemnogo vyše uvěrjeno i siľno. On jest priučeny vojevnik, ktory znaje, kako sę biti, kako rųbati i rězati neprijateljev. Pravdivo on nikògda ješče ne je iměl okazijų, da by prověriti svoje uměńje v pravdivom boju, ale on jest gotovy. Veliko gotovy.
# """

    
    
def cell_normalization(cell, jezyk):
    cell = str(cell)
    cell = cell.replace( '!', '')
    cell = cell.replace( '#', '')
    cell = cell.replace( ';', ',')
    cell = cell.lower()
    cell = cell.strip()
    cell = transliteracija(cell, jezyk)
    return cell

def custom_split(s):
    s = str(s)
    if ";" in s:
        return s.split("; ")
    return s.split(", ")

def prepare_slovnik(slovnik, split=False, transliterate=True):
    sheet = slovnik.copy()
    langs = list((set(slovnik.columns) & set(LANGS) ))
    for lang in langs:
        assert sheet[sheet[lang].astype(str).apply(lambda x: "((" in sorted(x))].empty
    for lang in langs:
        slovnik[lang] = slovnik[lang].apply(lambda x: str(x) ) # в переводчике была проблема, пока эту строчку не добавил
        sheet[lang] = sheet[lang].replace(brackets_regex1, "")
        sheet[lang] = sheet[lang].replace(brackets_regex2, "")
        sheet[lang] = sheet[lang].apply(lambda x: cell_normalization(x, lang))
        if transliterate:
            sheet[lang] = sheet[lang].apply(lambda x: transliteracija(x, lang))        
        if split:
            sheet[lang] = sheet[lang].apply(lambda x: custom_split(x))
    sheet['isv'] = sheet['isv'].str.replace("!", "").str.replace("#", "").str.lower()
    return sheet




def filtr_contain(stroka, jezyk, sheet):
    stroka = re.escape(stroka)
    return sheet[ sheet[jezyk].str.contains(stroka) == True].copy()

def iskati(stroka, jezyk, sheet):
    result = sheet[ sheet[jezyk].apply( lambda text: stroka in custom_split(text))]
    return result.index.values.tolist()

def iskati_slovo(slovo, jezyk, sheet):
    najdene_slova = []
    for i, stroka in sheet.iterrows():    
        if slovo in str.split( re.sub(r'[^\w\s]','', stroka[jezyk]) ):
            najdene_slova.append(i)
    return najdene_slova

def in_dict(stroka, jezyk, sheet):
    najdeno = filtr_contain(stroka, jezyk, sheet)
    najdeno = iskati(stroka, jezyk, najdeno)
    if not najdeno:
        return []
    result = [sheet['isv'][i] for i in najdeno]
    return ", ".join(result)
    
def in_dict_light(stroka, jezyk, sheet):
    najdeno = filtr_contain(stroka, jezyk, sheet)
    najdeno = iskati(stroka, jezyk, najdeno)
    return najdeno
    # if not najdeno:
    #     return []
    #return [sheet['id'][i] for i in najdeno]
    # return", ".join(result)

def is_in_dict(stroka, jezyk, sheet):
    sheet1 = filtr_contain(stroka, jezyk, sheet)
    sheet2 = iskati(stroka, jezyk, sheet1)
    if sheet2.empty:
        return False
    return True


def search_in_sheet(slova, jezycny_kod, sheet):
    sheet = filtr_contain( slova, jezycny_kod, sheet )  
    najdene_slova = iskati(slova, jezycny_kod, sheet)
    if najdene_slova:
        return najdene_slova           
    najdene_slova = iskati_slovo(slova, jezycny_kod, sheet)
    if najdene_slova:
        return najdene_slova
    return False