
import pandas as pd
import matplotlib.pyplot as plt

# Lire le fichier Excel
df = pd.read_excel('D:\StatsHaouz\PP_PAY_MAD.xlsx', dtype={'DATE_CREATION': str, 'DATE_UPDATE_STATUT': str, 'DATE_EXPIRATION': str})

# Convertir les colonnes de date en datetime, en spécifiant le format
df['DATE_CREATION'] = pd.to_datetime(df['DATE_CREATION'], forma
                                     t="%d/%m/%Y %H:%M:%S,%f", errors='coerce')
df['DATE_UPDATE_STATUT'] = pd.to_datetime(df['DATE_UPDATE_STATUT'], format="%d/%m/%Y %H:%M:%S,%f", errors='coerce')
df['DATE_EXPIRATION'] = pd.to_datetime(df['DATE_EXPIRATION'], format="%d/%m/%Y %H:%M:%S,%f", errors='coerce')

# Filtrer le DataFrame pour inclure seulement les statuts 'GENERE' et 'PAYE'
df_filtered = df[df['CURRENT_STATUT'].isin(['GENERE', 'PAYE'])]

# Générer le compte cumulatif des statuts 'PAYE' au fil du temps (par heure)
df_filtered_paye = df_filtered[df_filtered['CURRENT_STATUT'] == 'PAYE']
df_filtered_paye = df_filtered_paye.resample('H', on='DATE_UPDATE_STATUT').size().cumsum().reset_index(name='Cumul_PAYE')

# Générer le compte cumulatif des mandats créés (par heure)
creation_dates = df_filtered['DATE_CREATION'].dropna().unique()
created_count_by_date = {date: len(df_filtered[df_filtered['DATE_CREATION'] == date]) for date in creation_dates}
created_cumulative = []
total_created = 0
for date in sorted(creation_dates):
    total_created += created_count_by_date[date]
    created_cumulative.append((date, total_created))

df_created = pd.DataFrame(created_cumulative, columns=['DATE_CREATION', 'Cumul_Créés'])
df_created['DATE_CREATION'] = pd.to_datetime(df_created['DATE_CREATION'])
df_created = df_created.resample('H', on='DATE_CREATION').max().fillna(method='ffill').reset_index()

# Tracé
fig, ax = plt.subplots()
ax.plot(df_filtered_paye['DATE_UPDATE_STATUT'], df_filtered_paye['Cumul_PAYE'], label='Evol. Mandats payés', color='g')
ax.plot(df_created['DATE_CREATION'], df_created['Cumul_Créés'], label='Evol. Mandats crées', color='b')

ax.set(xlabel='Temps', ylabel='Nombre cumulatif des Mandats',
       title='Évolution Cumulative des Mandats payés')
ax.legend()

plt.show()
