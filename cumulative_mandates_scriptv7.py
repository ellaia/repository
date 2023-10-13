
import pandas as pd
import matplotlib.pyplot as plt

# Sample code for reading the Excel file and preprocessing (the actual code will be more detailed)
df = pd.read_excel('D:\StatsHaouz\PP_PAY_MAD_PROVINCE.xlsx')
date_columns = ['DATE_CREATION', 'DATE_UPDATE_STATUT', 'DATE_EXPIRATION']
for col in date_columns:
    df[col] = pd.to_datetime(df[col], format="%d/%m/%Y %H:%M:%S,%f", errors='coerce')




# Sample code for generating the global 'PAYE' curve (the actual code will be more detailed)
df_filtered = df[df['CURRENT_STATUT'].isin(['GENERE', 'PAYE'])]
df_filtered_paye = df_filtered[df_filtered['CURRENT_STATUT'] == 'PAYE']
df_filtered_paye_global = df_filtered_paye.resample('H', on='DATE_UPDATE_STATUT').size().cumsum().reset_index(name='Cumul_PAYE_Global')

# Code for generating province-specific curves

# Generate the cumulative count of 'PAYE' status over time (per hour) for each of the top 6 provinces
province_dfs = {
}
top_6_provinces = ['AL HAOUZ', 'TAROUDANNT', 'CHICHAOUA', 'OUARZAZATE', 'MARRAKECH', 'AZILAL']
for province in top_6_provinces:
    df_province = df_filtered_paye[df_filtered_paye['PROVINCE'] == province]
    province_dfs[province] = df_province.resample('H', on='DATE_UPDATE_STATUT').size().cumsum().reset_index(name=f'Cumul_PAYE_'+str(province))

# Plotting with distinct colors
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
fig, ax = plt.subplots(figsize=(14, 8))

# Plot the global curve
ax.plot(df_filtered_paye_global['DATE_UPDATE_STATUT'], df_filtered_paye_global['Cumul_PAYE_Global'], label='Global', color=colors[0])

# Plot the curves for each of the top 6 provinces
for i, province in enumerate(top_6_provinces):
    ax.plot(province_dfs[province]['DATE_UPDATE_STATUT'], province_dfs[province][f'Cumul_PAYE_'+str(province)], label=str(province), color=colors[i + 1])

# Add titles and labels
ax.set_title('Cumulative Count of Paid Mandates Over Time')
ax.set_xlabel('Time')
ax.set_ylabel('Cumulative Count')
ax.legend()
plt.show()


# Sample code for plotting (the actual code will be more detailed)
# ...
