import pandas as pd
import matplotlib.pyplot as plt

# Load the data from the Excel file (replace 'your_file_path_here' with the actual path to your Excel file)
df = pd.read_excel('D:\StatsHaouz\PP_PAY_MAD_PROVINCE.xlsx')
df['DATE_CREATION'] = pd.to_datetime(df['DATE_CREATION'], format='%d/%m/%Y %H:%M:%S,%f', errors='coerce')
df['DATE_UPDATE_STATUT'] = pd.to_datetime(df['DATE_UPDATE_STATUT'], format='%d/%m/%Y %H:%M:%S,%f', errors='coerce')

# Filter the DataFrame to include only rows with 'PAYE' or 'GENERE' status
df_filtered = df[df['CURRENT_STATUT'].isin(['PAYE', 'GENERE'])]

# Create separate DataFrames for 'PAYE' and 'GENERE' status
df_filtered_paye = df_filtered[df_filtered['CURRENT_STATUT'] == 'PAYE']
df_filtered_genere = df_filtered[df_filtered['CURRENT_STATUT'] == 'GENERE']

# Generate the global cumulative count of 'PAYE' status over time (per hour)
df_filtered_paye_global = df_filtered_paye.resample('H', on='DATE_UPDATE_STATUT').size().cumsum().reset_index(name='Cumul_PAYE_Global')

# Calculate the top 6 provinces based on the number of 'PAYE' status
top_6_provinces = df_filtered_paye['PROVINCE'].value_counts().index[:6]

# Generate the cumulative counts for each of the top 6 provinces with 'PAYE' status (per hour)
province_dfs = {}
colors = ['blue', 'green', 'red', 'purple', 'orange', 'brown', 'pink']

for province in top_6_provinces:
    df_province = df_filtered_paye[df_filtered_paye['PROVINCE'] == province]
    province_dfs[province] = df_province.resample('H', on='DATE_UPDATE_STATUT').size().cumsum().reset_index(name=f'Cumul_PAYE_{province}')

# Calculate the cumulative count of 'GENERE' status based on 'DATE_CREATION' (per hour)
df_genere_grouped_by_creation_date = df_filtered_genere.groupby('DATE_CREATION').size().reset_index(name='COUNT')
df_genere_grouped_by_creation_date['Cumul_GENERE_Creation'] = df_genere_grouped_by_creation_date['COUNT'].cumsum()

# Extend the DataFrame to include all hours up to the current time
current_time = pd.Timestamp.now().floor('H')
all_hours = pd.date_range(df_filtered_genere['DATE_CREATION'].min(), current_time, freq='H')
df_all_hours = pd.DataFrame({'DATE_CREATION': all_hours})
df_genere_extended = pd.merge_asof(df_all_hours.sort_values('DATE_CREATION'), df_genere_grouped_by_creation_date.sort_values('DATE_CREATION'), on='DATE_CREATION', direction='backward')

# Plotting
fig, ax = plt.subplots(figsize=(14, 8))

# Plot the global 'PAYE' curve
ax.plot(df_filtered_paye_global['DATE_UPDATE_STATUT'], df_filtered_paye_global['Cumul_PAYE_Global'], label='PAYE Global', color=colors[0])

# Plot the "staircase" 'GENERE' curve based on 'DATE_CREATION'
ax.step(df_genere_extended['DATE_CREATION'], df_genere_extended['Cumul_GENERE_Creation'], label='GENERE Creation Global (Staircase)', color=colors[-1], where='post')

# Plot the curves for each of the top 6 provinces with 'PAYE' status
for i, province in enumerate(top_6_provinces):
    ax.plot(province_dfs[province]['DATE_UPDATE_STATUT'], province_dfs[province][f'Cumul_PAYE_{province}'], label=f'PAYE {province}', color=colors[i + 1])

# Add titles and labels
ax.set_title('Cumulative Count of Paid and Created Mandates Over Time')
ax.set_xlabel('Time')
ax.set_ylabel('Cumulative Count')
ax.legend()

# Show the plot
plt.show()
