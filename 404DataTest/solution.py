# task 3
# from restcountries import RestCountryApiV2 as rapi
#
# VN = rapi.get_countries_by_name('Viet Nam')[0]
# SG = rapi.get_country_by_country_code('SG')
# countries_list = {VN.name : VN.alpha2_code, SG.name : SG.alpha2_code}

# task 2
import pandas as pd
import datetime
import numpy as np
pd.set_option('display.width', 320)
pd.set_option('display.max_columns', 20)

df_1 = pd.read_csv('test - 1.csv', sep=',', encoding='utf-8')
df_1['date'] = pd.to_datetime(df_1['date'], format='%Y.%m.%d')
df_2 = pd.read_csv('test - 2.csv', sep=',', encoding='utf-8')
df_2['date'] = pd.to_datetime(df_2['date'], format='%Y.%m.%d')
df_3 = pd.read_csv('test - 3.csv', sep=',', encoding='utf-8')

# a.
df_23 = pd.merge(df_2, df_3, on='id')
print(df_23)

# b.
df_1 = df_1[['id', 'date', 'invest', 'registrations', 'manager', 'device', 'channel']]
df_all = df_23.append(df_1, ignore_index=True)
print(df_all)

# c.
df_january = df_all[(df_all.date > pd.Timestamp(datetime.date(2019, 1, 1))) & (df_all.date < pd.Timestamp(datetime.date(2019, 2, 1)))]
print(df_january)

# d.
df_sum = df_all
df_grouped_by_manager = df_sum.groupby('manager').agg({'invest': 'sum', 'registrations': 'sum'})
print(df_grouped_by_manager)

# e.
# стоимость = цена * количество. В этом датасете предполагаю что под стоимоcтью имеется ввиду invest * registrations
df_cost = df_all
df_cost['cost'] = (df_all.invest / df_all.registrations).replace({np.inf : None})
print(df_cost)