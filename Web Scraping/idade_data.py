import pandas as pd
from datetime import datetime as dt

df_medals = pd.read_csv('olympic_data.csv', sep=',')
vals = []
for i in range(0,len(df_medals['Birth'])):
    date = dt.strptime(df_medals['Birth'][i], '%d %B %Y')
    vals.append(date)

rep = {'Birth':vals}
birth_column = pd.DataFrame(rep)
df_medals['Birth'] = birth_column['Birth']

opening = dt(2021, 7, 23)
for i in range(0,len(vals)):
    lst_date = vals[i]
    ath_date = opening - lst_date
    bday = int(ath_date.days)//365
    vals[i] = bday

rep2 = {'Age':vals}
age_column = pd.DataFrame(rep2)
df_medals['Age'] = age_column['Age']
df_medals.replace('', 0, inplace=True)
df_medals.drop(df_medals.columns[0],axis=1,inplace=True)
df_medals.to_csv('olympic_final.csv')
print('<<<<< DONE! >>>>>')