import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Read data from Excel
df = pd.read_excel('D:\\StatsHaouz\\PP_PAY_MAD_PROVINCE.xlsx')

# Convert to datetime
df['DATE_CREATION'] = pd.to_datetime(df['DATE_CREATION'], format='%d/%m/%Y %H:%M')
df['DATE_UPDATE_STATUT'] = pd.to_datetime(df['DATE_UPDATE_STATUT'], format='%d/%m/%Y %H:%M')

# Filter data for "PAYE"
df_filtered_paye_global = df[df['CURRENT_STATUT'] == 'PAYE'].copy()

# Extract the date and time
df_filtered_paye_global['DATE_ONLY'] = df_filtered_paye_global['DATE_UPDATE_STATUT'].dt.date
df_filtered_paye_global['TIME_ONLY'] = df_filtered_paye_global['DATE_UPDATE_STATUT'].dt.time

# Sort the DataFrame
df_filtered_paye_global = df_filtered_paye_global.sort_values('DATE_UPDATE_STATUT')

# Unique days for plotting
unique_days = df_filtered_paye_global['DATE_ONLY'].unique()

# Initialize the plot
fig, ax = plt.subplots()

# Iterate through each unique day and plot
for day in unique_days:
    df_day = df_filtered_paye_global[df_filtered_paye_global['DATE_ONLY'] == day]
    df_day['HOUR'] = df_day['DATE_UPDATE_STATUT'].dt.hour
    df_day_count = df_day.groupby('HOUR').size().reset_index(name='PAYE')
    ax.plot(df_day_count['HOUR'], df_day_count['PAYE'], label=f'{day}')

# Add labels and title
ax.set_xlabel('Heure de la Journée')
ax.set_ylabel('Nombre de Mandats Payés')
ax.set_title('Comparaison du Rythme de Paiement des Mandats par Heure au Cours de Différents Jours')

# Add grid
ax.grid(True)

# Add legend and adjust its position to avoid overlapping
ax.legend(title='Jour', bbox_to_anchor=(1.05, 1), loc='upper left')

# Show the plot with a layout adjustment
plt.tight_layout()
plt.show()
