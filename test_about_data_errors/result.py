import pandas as pd
import matplotlib.pyplot as plt


pd.set_option('display.width', 400)
pd.set_option('display.max_columns', 20)

fixed_df = pd.read_csv('Bloomy.xls', encoding='utf-8')
fixed_df['@timestamp'] = pd.to_datetime(fixed_df['@timestamp'], format='%Y-%m-%d %H:%M:%S.%f')
fixed_df['profile_created'] = pd.to_datetime(fixed_df['profile_created']).dt.tz_convert('UTC').dt.tz_convert(None)

print(fixed_df.head(10)) # print what we have
print('---------------------')
print()

# NULL Type
print(str(int((fixed_df['agency'].isnull().sum() / fixed_df['agency'].shape[0])*100)) + "% in agency is NULL")
print(str(int((fixed_df['app_version'].isnull().sum() / fixed_df['app_version'].shape[0])*100)) + "% in app_version is NULL")
print(str(int((fixed_df['build'].isnull().sum() / fixed_df['build'].shape[0])*100)) + "% in build is NULL")
print(str(int((fixed_df['payment_atype'].isnull().sum() / fixed_df['build'].shape[0])*100)) + "% in payment_atype is NULL")
print('---------------------')
print()

# Small coutries and other values
print(fixed_df.groupby('country').size().reset_index(name='counts').sort_values(by=['counts'], ascending=True))
print()
print(fixed_df.groupby('agency').size().reset_index(name='counts').sort_values(by=['counts'], ascending=True))
print()
print(fixed_df.groupby('@key').size().reset_index(name='counts').sort_values(by=['counts'], ascending=True))
print()
print(fixed_df.groupby('profile_type').size().reset_index(name='counts').sort_values(by=['counts'], ascending=True))
print()
print(fixed_df.groupby('gender').size().reset_index(name='counts').sort_values(by=['counts'], ascending=True))
print()
print(fixed_df.groupby('payment_atype').size().reset_index(name='counts').sort_values(by=['counts'], ascending=True))
print('---------------------')
print()

# too old dates or future dates
err_date = min(fixed_df['profile_created'])
print(err_date)
print(max(fixed_df['profile_created']))
print('---------------------')
print()

# lines where err dates
print(fixed_df[fixed_df.profile_created == err_date].reset_index())
print('---------------------')
print()

# where agency is not null create plot from '@timestamp'
fixed_df[fixed_df.agency.notnull()].sort_values(by=['@timestamp'], ascending=True).plot(kind='line', x='@timestamp', y='agency', ax=plt.gca())
plt.show()
