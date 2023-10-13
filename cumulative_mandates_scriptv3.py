
import pandas as pd
import matplotlib.pyplot as plt

# Read the Excel file
df = pd.read_excel('D:\StatsHaouz\PP_PAY_MAD.xlsx', dtype={'DATE_CREATION': str, 'DATE_UPDATE_STATUT': str, 'DATE_EXPIRATION': str})

# Convert the date columns to datetime, specifying the format
df['DATE_CREATION'] = pd.to_datetime(df['DATE_CREATION'], format="%d/%m/%Y %H:%M:%S,%f", errors='coerce')
df['DATE_UPDATE_STATUT'] = pd.to_datetime(df['DATE_UPDATE_STATUT'], format="%d/%m/%Y %H:%M:%S,%f", errors='coerce')
df['DATE_EXPIRATION'] = pd.to_datetime(df['DATE_EXPIRATION'], format="%d/%m/%Y %H:%M:%S,%f", errors='coerce')

# Filtering the DataFrame to include only 'GENERE' and 'PAYE' statuses
df_filtered = df[df['CURRENT_STATUT'].isin(['GENERE', 'PAYE'])]

# Generate the cumulative count of 'PAYE' statuses over time (by the hour)
df_filtered_paye = df_filtered[df_filtered['CURRENT_STATUT'] == 'PAYE']
df_filtered_paye = df_filtered_paye.resample('H', on='DATE_UPDATE_STATUT').size().cumsum().reset_index(name='Cumulative_PAYE')

# Generate the cumulative count of created mandates (by the hour)
creation_dates = df_filtered['DATE_CREATION'].dropna().unique()
created_count_by_date = {date: len(df_filtered[df_filtered['DATE_CREATION'] == date]) for date in creation_dates}
created_cumulative = []
total_created = 0
for date in sorted(creation_dates):
    total_created += created_count_by_date[date]
    created_cumulative.append((date, total_created))

df_created = pd.DataFrame(created_cumulative, columns=['DATE_CREATION', 'Cumulative_Created'])
df_created['DATE_CREATION'] = pd.to_datetime(df_created['DATE_CREATION'])
df_created = df_created.resample('H', on='DATE_CREATION').max().fillna(method='ffill').reset_index()

# Plotting
fig, ax = plt.subplots()
ax.plot(df_filtered_paye['DATE_UPDATE_STATUT'], df_filtered_paye['Cumulative_PAYE'], label='Cumulative PAYE', color='r')
ax.plot(df_created['DATE_CREATION'], df_created['Cumulative_Created'], label='Cumulative Created', color='g')

ax.set(xlabel='Time', ylabel='Cumulative Count',
       title='Cumulative Count of Mandates over Time')
ax.legend()

plt.show()
