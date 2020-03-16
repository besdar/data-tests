import pandas as pd
import datetime
import matplotlib.pyplot as plt

pd.set_option('display.width', 320)
pd.set_option('display.max_columns', 10)

fixed_df = pd.read_csv('1_trading_activity.csv',
                       sep=',', encoding='utf-8', parse_dates=['deal_open_time', 'deal_close_time'], date_parser = lambda x: pd.datetime.strptime(x, '%Y-%m-%d %H:%M:%S'), dayfirst=True)
fixed_df['deal_result'] = fixed_df['deal_result'].map(lambda x: x.replace(",", ""))
fixed_df.deal_result = fixed_df.deal_result.astype(float)
fixed_df['deal_investment'] = fixed_df['deal_investment'].map(lambda x: x.replace(",", ""))
fixed_df.deal_investment = fixed_df.deal_investment.astype(float)

print(fixed_df.head(10)) # print what we have
print('---------------------')
print()

fixed_df['PNL'] = (fixed_df.deal_investment - fixed_df.deal_result) # 1.3 count a PNL
fixed_df['CountOfUsing'] = 1 # 1.1 count the most popular instrument

# 1.4
# Вначале берем только те строки, где даты deal_close_time в марте, потом суммируем PNL по пользователям, сортируем по возрастанию (самое большое отрицательное первое),
# берем первое и выводим айди и его суммарный ПНЛ
print("Best user of march:")
print(fixed_df[(fixed_df.deal_close_time > pd.Timestamp(datetime.date(2019, 3, 1))) & (fixed_df.deal_close_time < pd.Timestamp(datetime.date(2019, 4, 1)))].groupby('user_id').agg({'PNL': 'sum'}).sort_values(by=['PNL'], ascending=True).head(1)) # 1.3 answer
print('---------------------')
print()

# 1.3
PNL_group_by_assets = fixed_df.groupby('asset').agg({'PNL': 'sum'}).sort_values(by=['PNL'], ascending=False)
# По твоей формуле из примера беру самое большое число и делю его на сумму всего остального без этого числа.
max_PNL_by_asset = PNL_group_by_assets.values[0][0]
print("Percentages by asset " + PNL_group_by_assets.index[0] + " " + str(int(max_PNL_by_asset * 100 / (PNL_group_by_assets['PNL'].sum() - max_PNL_by_asset))) + "%")

# Тут я решил показать пример, что этот процент можно высчитывать для каждой категории, например для каждого инструмента.
# Если тебе нужно именно так, то сделай по аналогии, но имей ввиду, что в примере (для assets) 210 сгруппированных строк
PNL_group_by_instrument = fixed_df.groupby('instrument_type').agg({'PNL': 'sum'}).sort_values(by=['PNL'], ascending=False).reset_index()
for row in PNL_group_by_instrument[['instrument_type', 'PNL']].values:
    print("Percentages by instrument type " + str(row[0]) + " " + str(int(row[1] * 100 / (PNL_group_by_instrument['PNL'].sum() - row[1]))) + "%")

# старый вариант предыдущего примера с инструментами:
# PNL_group_by_instrument = fixed_df.groupby('instrument_type').agg({'PNL': 'sum'}).sort_values(by=['PNL'], ascending=False).query('PNL > 0')
# max_PNL_by_instrument = PNL_group_by_instrument.values[0][0]
# print("Percentages by instrument type " + PNL_group_by_instrument.index[0] + " " + str(int(max_PNL_by_instrument * 100 / (PNL_group_by_instrument['PNL'].sum() - max_PNL_by_instrument))) + "%")

PNL_group_by_platform = fixed_df.groupby('platform').agg({'PNL': 'sum'}).sort_values(by=['PNL'], ascending=False)
max_PNL_by_platform = PNL_group_by_platform.values[0][0]
print("Percentages by platform " + PNL_group_by_platform.index[0] + " " + str(int(max_PNL_by_platform * 100 / (PNL_group_by_platform['PNL'].sum() - max_PNL_by_platform))) + "%")

PNL_group_by_region = fixed_df.groupby('region_name').agg({'PNL': 'sum'}).sort_values(by=['PNL'], ascending=False)
max_PNL_by_region = PNL_group_by_region.values[0][0]
print("Percentages by region " + PNL_group_by_region.index[0] + " " + str(int(max_PNL_by_region * 100 / (PNL_group_by_region['PNL'].sum() - max_PNL_by_region))) + "%")
print('---------------------')
print()

# 1.1
print("Most popular instruments:")
print(fixed_df.groupby('instrument_type').agg({'CountOfUsing': 'sum'}).sort_values(by=['CountOfUsing'], ascending=False)) # 1.1 answer
print('---------------------')
print()

# 1.2
print("Most popular instruments by region:")
print(fixed_df.groupby(['instrument_type', 'region_name']).agg({'CountOfUsing': 'sum'}).sort_values(by=['region_name', 'CountOfUsing'], ascending=False)) # 1.2 answer
print('---------------------')
print()

# 1.5 - count the SystemPercent
TradingVolume = fixed_df.groupby(by=['user_id']).agg({'deal_investment' : 'sum'}).reset_index().rename(columns={'deal_investment' : 'TradingVolume'})
df_withTradingVolume = pd.merge(fixed_df[['user_id', 'PNL', 'deal_close_time']], TradingVolume, on='user_id')
df_withTradingVolume['SystemPercent'] = df_withTradingVolume.PNL / df_withTradingVolume.TradingVolume
print(df_withTradingVolume.head(5)) # some example of data

df_withTradingVolume.sort_values(by=['deal_close_time'], ascending=True).plot(kind='line', x='deal_close_time', y='SystemPercent', ax=plt.gca())
plt.show() #