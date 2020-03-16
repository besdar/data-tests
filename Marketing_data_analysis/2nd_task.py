import pandas as pd
import datetime
import matplotlib.pyplot as plt

pd.set_option('display.width', 320)
pd.set_option('display.max_columns', 10)

fixed_df = pd.read_csv('2_experiment_result.csv',
                       sep=',', encoding='utf-8', parse_dates=['enter_experiment'], date_parser = lambda x: pd.datetime.strptime(x, '%Y-%m-%d %H:%M:%S'), dayfirst=True)
fixed_df.fillna(0, inplace=True)
fixed_df['deposits'] = fixed_df['deposits'].replace('\$','',regex=True).replace('\,','',regex=True).astype(float)
fixed_df['binary_PNL'] = fixed_df['binary_PNL'].replace('\$','',regex=True).replace('\,','',regex=True).astype(float)
fixed_df['instrument_PNL'] = fixed_df['instrument_PNL'].replace('\$','',regex=True).replace('\,','',regex=True).astype(float)

print(fixed_df.head(10)) # print what we have
print('---------------------')
print()

# Посчитать количество строк disabled, min_10, min_20.
print(fixed_df[fixed_df['state'] == 'disabled'].shape[0])
print(fixed_df[fixed_df['state'] == 'min_10'].shape[0])
print(fixed_df[fixed_df['state'] == 'min_20'].shape[0])
print('---------------------')
print()

# Посчитать количество уникальных user_id для каждой из этих 3 групп
print(fixed_df.groupby('state')['user_id'].nunique())
print('---------------------')
print()

# После этого посчитать сумму стоблца deposits по стоблцу state (там всего 3 значения disabled, min_10, min_20).
print(fixed_df.groupby('state').agg({'deposits' : 'sum'}))
print('---------------------')
print()

# После этого посчитать сумму стоблца binary_PNL по стоблцу state (там всего 3 значения disabled, min_10, min_20).
print(fixed_df.groupby('state').agg({'binary_PNL' : 'sum'}))
print('---------------------')
print()

# После этого посчитать сумму стоблца instrument_PNL по стоблцу state (там всего 3 значения disabled, min_10, min_20).
print(fixed_df.groupby('state').agg({'instrument_PNL' : 'sum'}))
print('---------------------')
print()
