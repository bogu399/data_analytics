import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime as dt
import re
from tqdm import tqdm

def getOut_list(lista:list,sep:str,indice:int):
    lista[indice] = lista[indice].split(sep)
    for i in lista[indice]:
        lista.append(i)
    lista.pop(indice)

def organize_athletes(lista):
    for i in lista:
        for j in i:
            if ' in ' in j:
                m = re.match('^.*(?=( in))',j)
                string = m.group(0)
                ind = i.index(j)
                i[ind] = string

def sub_list(lista:list,ind:int):
    return [lista[n:n+ind] for n in range(0, len(lista), ind)]
                
#RESULTS
url = 'http://www.olympedia.org/editions/61/sports/' #OLYMPEDIA ROOT LINK
sport_list = [
    'BK3','ARC','GYM','SWA','BDM','BSB','BAS','BVO','BOX','CSL',
    'CAN','BMF','BMX','MTB','CYC','CTR','DIV','EDR','EVE','EQU',
    'FEN','FTB','GOL','HAN','HOK','JUD','KTE','OWS','MOP','RGY',
    'ROW','RGS','SAI','SHO','SKB','SOF','CLB','SRF','SWI','TTN',
    'TKW','TEN','TMP','TRI','VOL','WAP','WLT','WRE'
    ]
equip = ['BK3','BSB','BAS','BVO','SWA','HAN','HOK','RGS','SOF','VOL','WAP','FTB','ATH']

"""
ATH - Atletismo ainda não tem dados, será retirado da lista de coleta
"""

result_dic = {}
for i in tqdm(sport_list):
    if i not in equip:
        page = requests.get(url + i)
        soup = BeautifulSoup(page.text, 'html.parser')
        root = soup.find(class_= "container")
        links = []
        for j in root.find_all('a',href=True):
            links.append(j['href'])
        resul = 'results'
        results = [string for string in links if resul in string]
        if i == 'JUD' or i == 'ATH' or i == 'TRI' or i == 'EVE' or i == 'EDR' or i == 'EQU' or i == 'RGY':
            results = list(dict.fromkeys(results))
            results = results[:-1] 
            result_dic[i] = results
        elif i == 'ARC' or i == 'BDM' or i == 'TTN' or i == 'TEN':
            results = list(dict.fromkeys(results))
            results = [results[0],results[2]]
            result_dic[i] = results
        elif i == 'GYM':
            results = list(dict.fromkeys(results))
            results2 = results[2:9] + results[10:]
            results2.insert(0,results[0])
            result_dic[i] = results2
        elif i == 'CAN':
            results = list(dict.fromkeys(results))
            results = [results[0], results[1], results[4], results[6], results[7], results[10]]
            result_dic[i] = results
        elif i == 'CTR':
            results = list(dict.fromkeys(results))
            results = [results[0], results[1], results[5], results[6], results[7], results[11]]
            result_dic[i] = results
        elif i == 'DIV':
            results = list(dict.fromkeys(results))
            results = [results[0], results[1], results [4], results[5]]
            result_dic[i] = results
        elif i == 'FEN':
            results = list(dict.fromkeys(results))
            results = [results[0], results[2], results[4], results[6], results[8], results[10]]            
            result_dic[i] = results
        elif i == 'ROW':
            results = list(dict.fromkeys(results))
            results = [results[0], results[7]]
            result_dic[i] = results
        elif i == 'SAI':
            results = list(dict.fromkeys(results))
            results = [results[0], results[1], results[4], results[5], results[6]]
            result_dic[i] = results
        elif i == 'SHO':
            results = list(dict.fromkeys(results))
            results = results[0:12]
            result_dic[i] = results
        elif i == 'SWI':
            results = list(dict.fromkeys(results))
            results = results[0:6] + results[8:16] + results[17:23] + results[25:33]
            result_dic[i] = results
        else:
            results = list(dict.fromkeys(results))
            result_dic[i] = results

#CLASSIFICATION
url = 'http://www.olympedia.org' #OLYMPEDIA ROOT LINK
cla_4 = ['BOX','JUD','TTN','ARC','BDM']
cla_5 = ['GYM','CSL','CAN','BMF','DIV','KTE','RGY','ROW','SAI','SRF','SWI','TKW','TEN','TMP','CLB']
cla_6 = ['EDR','EQU','FEN','MOP','TRI']
cla_7 = 'EVE'
cla_8 = 'WLT' #SE LIGAR AQUI, CASO MUITÍSSIMO ESPECIAL
cla_9 = ['BMX','OWS','WRE']
cla_11 = 'GOL'
cla_13 = 'MTB'

sete_CTR = ['/results/19005073','/results/19004957','/results/19005016','/results/19004900']
oito_CTR = ['/results/19005008','/results/19005124']

nove_SHO = ['/results/18000720','/results/18000728','/results/18000743','/results/18000751']
sete_SHO = ['/results/18000723','/results/18000731','/results/18000737','/results/18000740','/results/18000746','/results/18000754','/results/18000760','/results/18000763']

nove_SKB = ['/results/18000370','/results/18000377']
sete_SKB = ['/results/18000384','/results/18000391']

oito_CYC = ['/results/19001700','/results/19001702']
doze_CYC = ['/results/19001701','/results/19001703']

final_list = []
for key,value in tqdm(result_dic.items()):
    for l in value:
        page = requests.get(url + l)
        soup = BeautifulSoup(page.text, 'html.parser')
        root = soup.find(class_= "container")
        event = root.find("h1").text
        root = soup.find(class_="table table-striped")
        td_tags = root.find_all("td")

        links = []
        for i in root.find_all('a',href=True):
            links.append(i['href'])
        
        ath = 'athletes'
        athletes = [string for string in links if ath in string]
        
        rows = []
        for i in td_tags:
            rows.append(i.text)
            
        if key in cla_4:
            lista = sub_list(rows,6)
            for j in lista: 
                j.append(event)
                j.append(key)
            df = pd.DataFrame(lista, columns=['Position','Athlete','NOC','Nr','Medal','Nr2','Event','Sport']) #BOX #JUD ARC TTN BDM
            df = df.drop(columns=['Nr','Nr2']) #BOX JUD ARC TTN BDM
            df = df.replace('','NA')
        
        elif key in cla_5:
            lista = sub_list(rows,7)
            for j in lista: 
                j.append(event)
                j.append(key)
            
            if key == cla_5[8] or key == cla_5[10]:
                df = pd.DataFrame(lista, columns=['Position','Athlete','NOC','Nr','Medal','Nr2','Nr3','Event','Sport']) #SAI SWI
                df = df.drop(columns=['Nr','Nr2','Nr3'])
                df = df.replace('','NA')
        
            elif key == cla_5[11]:
                df = pd.DataFrame(lista, columns=['Position','Nr','Athlete','NOC','Nr2','Medal','Nr3','Event','Sport']) #TKW
                df = df.drop(columns=['Nr','Nr2','Nr3'])
                df = df.replace('','NA')
            
            else:
                df = pd.DataFrame(lista, columns=['Position','Nr','Athlete','NOC','Medal','Nr2','Nr3','Event','Sport']) #GYM CSL CAN BMF DIV KTE RGY ROW SRF TEN TMP CLB
                df = df.drop(columns=['Nr','Nr2','Nr3'])
                df = df.replace('','NA')
        
        elif key in cla_6:
            if key == cla_6[0] or key == cla_6[1]:
                lista = sub_list(rows,8)
                for j in lista: 
                    j.append(event)
                    j.append(key)
                df = pd.DataFrame(lista, columns=['Position','Nr','Athlete','Nr2','NOC','Medal','Nr3','Nr4','Event','Sport']) #EDR EQU
                df = df.drop(columns=['Nr','Nr2','Nr3','Nr4'])
                df = df.replace('','NA')
            
            elif key == cla_6[4] or key == cla_6[2]:
                lista = sub_list(rows,8)
                for j in lista: 
                    j.append(event)
                    j.append(key)
                df = pd.DataFrame(lista, columns=['Position','Nr','Athlete','NOC','Nr2','Medal','Nr3','Nr4','Event','Sport']) #TRI FEN
                df = df.drop(columns=['Nr','Nr2','Nr3','Nr4'])
                df = df.replace('','NA')
            
            elif key == cla_6[3]:
                lista = sub_list(rows,8)
                for j in lista: 
                    j.append(event)
                    j.append(key)
                df = pd.DataFrame(lista, columns=['Position','Nr','Athlete','NOC','Nr2','Nr3','Medal','Nr4','Event','Sport']) #MOP
                df = df.drop(columns=['Nr','Nr2','Nr3','Nr4'])
                df = df.replace('','NA')

        elif key == cla_7:
            lista = sub_list(rows,9)
            for i in lista: 
                i.append(event)
                i.append(key)
            df = pd.DataFrame(lista, columns=['Position','Nr','Athlete','Nr2','NOC','Nr3','Medal','Nr4','Nr5','Event','Sport'])
            df = df.drop(columns=['Nr','Nr2','Nr3','Nr4','Nr5'])
            df = df.replace('','NA')
        
        elif key == cla_8:
            lista = sub_list(rows,9)
            for j in lista: 
                j.append(event)
                j.append(key)
            df = pd.DataFrame(lista, columns=['Position','Nr','Athlete','NOC','Nr2','Nr3','Nr4','Medal','Nr5','Event','Sport']) #WLT
            df = df.drop(columns=['Nr','Nr2','Nr3','Nr4','Nr5']) #WLT
            df  = df.replace('','NA')
        
        elif key in cla_9:
            lista = sub_list(rows,11)
            for j in lista: 
                j.append(event)
                j.append(key)
            
            if key == cla_9[0] or key == cla_9[1]:
                df = pd.DataFrame(lista, columns=['Position','Nr','Athlete','NOC','Nr2','Nr3','Nr4','Nr5','Medal','Nr6','Nr7','Event', 'Sport']) #BMX OWS
                df = df.drop(columns=['Nr','Nr2','Nr3','Nr4','Nr5','Nr6','Nr7'])
                df = df.replace('','NA')
            
            elif key == cla_9[2]:
                df = pd.DataFrame(lista, columns=['Position','Athlete','NOC','Nr','Nr2','Nr3','Nr4','Nr5','Nr6','Medal','Nr7','Event','Sport']) #WRE
                df = df.drop(columns=['Nr','Nr2','Nr3','Nr4','Nr5','Nr6','Nr7'])
                df = df.replace('','NA')
        
        elif key == cla_11:
            lista = sub_list(rows,13)
            for j in lista: 
                j.append(event)
                j.append(key)
            df = pd.DataFrame(lista, columns=['Position','Athlete','NOC','Nr','Nr2','Nr3','Nr4','Nr5','Nr6','Nr7','Nr8','Medal','Nr9','Event','Sport'])
            df = df.drop(columns=['Nr','Nr2','Nr3','Nr4','Nr5','Nr6','Nr7','Nr8','Nr9'])
            df = df.replace('','NA')

        elif key == 'MTB':
            if l == '/results/19001704':
                lista = sub_list(rows,15)
                for j in lista: 
                    j.append(event)
                    j.append(key)
                df = pd.DataFrame(lista, columns=['Position','Nr','Athlete','NOC','Nr2','Nr3','Nr4','Nr5','Nr6','Nr7','Nr8','Nr9','Medal','Nr10','Nr11','Event','Sport'])
                df = df.drop(columns=['Nr','Nr2','Nr3','Nr4','Nr5','Nr6','Nr7','Nr8','Nr9','Nr10','Nr11'])
                df = df.replace('','NA')
            elif l == '/results/19001705':
                lista = sub_list(rows,14)
                for j in lista: 
                    j.append(event)
                    j.append(key)
                df = pd.DataFrame(lista, columns=['Position','Nr','Athlete','NOC','Nr2','Nr3','Nr4','Nr5','Nr6','Nr7','Nr8','Medal','Nr9','Nr10','Event','Sport'])
                df = df.drop(columns=['Nr','Nr2','Nr3','Nr4','Nr5','Nr6','Nr7','Nr8','Nr9','Nr10'])
                df = df.replace('','NA')
        
        elif key == 'CYC':
            if l in oito_CYC:
                lista = sub_list(rows,8)
                for j in lista: 
                    j.append(event)
                    j.append(key)
                df = pd.DataFrame(lista, columns=['Position','Nr','Athlete','NOC','Nr2','Medal','Nr3','Nr4','Event','Sport'])
                df = df.drop(columns=['Nr','Nr2','Nr3','Nr4'])
                df = df.replace('','NA')
            
            elif l == '/results/19001701':
                lista = sub_list(rows,12)
                for j in lista: 
                    j.append(event)
                    j.append(key)
                df = pd.DataFrame(lista, columns=['Position','Nr','Athlete','NOC','Nr2','Nr3','Nr4','Nr5','Nr6','Medal','Nr7','Nr8','Event','Sport'])
                df = df.drop(columns=['Nr','Nr2','Nr3','Nr4','Nr5','Nr6','Nr7','Nr8'])
                df = df.replace('','NA')
            elif l == '/results/19001703':
                lista = sub_list(rows,10)
                for j in lista: 
                    j.append(event)
                    j.append(key)
                df = pd.DataFrame(lista, columns=['Position','Nr','Athlete','NOC','Nr2','Nr3','Nr4','Medal','Nr5','Nr6','Event','Sport'])
                df = df.drop(columns=['Nr','Nr2','Nr3','Nr4','Nr5','Nr6'])
                df = df.replace('','NA')

        elif key == 'CTR':
            if l in sete_CTR:
                lista = sub_list(rows,7)
                for j in lista: 
                    j.append(event)
                    j.append(key)
                df = pd.DataFrame(lista, columns=['Position','Nr','Athlete','NOC','Medal','Nr2','Nr3','Event','Sport'])
                df = df.drop(columns=['Nr','Nr2','Nr3'])
                df = df.replace('','NA')
            elif l in oito_CTR:
                lista = sub_list(rows,8)
                for j in lista: 
                    j.append(event)
                    j.append(key)
                df = pd.DataFrame(lista, columns=['Position','Nr','Athlete','NOC','Nr2','Medal','Nr3','Nr4','Event','Sport'])
                df = df.drop(columns=['Nr','Nr2','Nr3','Nr4'])
                df = df.replace('','NA')
        
        elif key == 'SHO':
            if l in nove_SHO:
                lista = sub_list(rows,9)
                for j in lista: 
                    j.append(event)
                    j.append(key)
                df = pd.DataFrame(lista, columns=['Position','Nr','Athlete','NOC','Nr2','Nr3','Medal','Nr4','Nr5','Event','Sport'])
                df = df.drop(columns=['Nr','Nr2','Nr2','Nr3','Nr4','Nr5'])
                df = df.replace('','NA')
            
            elif l in sete_SHO:
                lista = sub_list(rows,7)
                for j in lista: 
                    j.append(event)
                    j.append(key)
                df = pd.DataFrame(lista, columns=['Position','Nr','Athlete','NOC','Medal','Nr2','Nr3','Event','Sport'])
                df = df.drop(columns=['Nr','Nr2','Nr3'])
                df = df.replace('','NA')
        
        elif key == 'SKB':
            if l in nove_SKB:
                lista = sub_list(rows,9)
                for j in lista: 
                    j.append(event)
                    j.append(key)
                df = pd.DataFrame(lista, columns=['Position','Nr','Athlete','NOC','Nr2','Nr3','Medal','Nr4','Nr5','Event','Sport'])
                df = df.drop(columns=['Nr','Nr2','Nr3','Nr4','Nr5'])
                df = df.replace('','NA')
            elif l in sete_SKB:
                lista = sub_list(rows,7)
                for j in lista: 
                    j.append(event)
                    j.append(key)
                df = pd.DataFrame(lista, columns=['Position','Nr','Athlete','NOC','Medal','Nr2','Nr3','Event','Sport'])
                df = df.drop(columns=['Nr','Nr2','Nr3'])
                df = df.replace('','NA')
        
        every_ath = []
        for m in athletes:
            page2 = requests.get(url + m)
            soup2 = BeautifulSoup(page2.text, 'html.parser')
            root2 = soup2.find(class_= "biodata")
            td_th_tags = root2.find_all(["td","th"])
            rows2 = []
            for i in td_th_tags:
                rows2.append(i.text)
            rows3 = []
            for i in rows2:
                sex1 = rows2.index('Sex')
                sex2 = rows2.index('Sex') + 1
                rows3.append(sex1)
                rows3.append(sex2)
                born1 = rows2.index('Born')
                born2 = rows2.index('Born') + 1
                rows3.append(born1)
                rows3.append(born2)
                try:
                    measure1 = rows2.index('Measurements')
                    measure2 = rows2.index('Measurements') + 1
                    rows3.append(measure1)
                    rows3.append(measure2)
                except:
                    rows3.append(0)
                    rows3.append(0)
            rows4 = [rows3[1],rows3[3],rows3[5]]
            rows5 = []
            for i in rows4:
                rows5.append(rows2[i])
            every_ath.append(rows5)
        
        for i in every_ath:
            if i[2] == 'Type':
                i[2] = '0/0'
        
        for i in every_ath:
            i[2] = re.sub('[a-z ]','', i[2])
        
        for i in every_ath:
            getOut_list(i, '/', 2)
        
        organize_athletes(every_ath)
        ath = pd.DataFrame(every_ath, columns=['Sex','Birth','Height','Weight'])

        df_sport = pd.concat([df.reset_index(drop=True), ath.reset_index(drop=True)], axis=1)

        final_list.append(df_sport)

df_medals = pd.concat(final_list)

#EXPORT TABLE
df_medals.to_csv(r'olympic_data.csv')
print('<<<<< DONE! >>>>>')