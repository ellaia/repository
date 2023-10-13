
import pandas as pd
import matplotlib.pyplot as plt

# Read the Excel file (replace 'your_file_path' with the path to your Excel file)
df = pd.read_excel('D:\StatsHaouz\PP_PAY_MAD.xlsx', parse_dates=['DATE_CREATION', 'DATE_UPDATE_STATUT', 'DATE_EXPIRATION'])

# Sort the DataFrame by 'DATE_CREATION' and 'DATE_UPDATE_STATUT'
sorted_df = df.sort_values(by=['DATE_CREATION', 'DATE_UPDATE_STATUT'])

# Generate time bins of 1-hour intervals
start_date = sorted_df['DATE_CREATION'].min()
end_date = sorted_df['DATE_UPDATE_STATUT'].max()
time_bins_1H = pd.date_range(start_date, end_date + pd.Timedelta(hours=12), freq='1H')

# Initialize an empty list to hold the cumulative number of paid mandates over time for 1-hour intervals
cumulative_paid_mandates_1H = []
cumulative_counter_1H = 0

# Loop through each 1-hour time bin to calculate the cumulative number of paid mandates
for i in range(len(time_bins_1H) - 1):
    start_time = time_bins_1H[i]
    end_time = time_bins_1H[i + 1]
    paid_mandates_in_interval = sorted_df[(sorted_df['CURRENT_STATUT'] == 'PAYE') & 
                                          (sorted_df['DATE_UPDATE_STATUT'] >= start_time) & 
                                          (sorted_df['DATE_UPDATE_STATUT'] < end_time)]
    cumulative_counter_1H += len(paid_mandates_in_interval)
    cumulative_paid_mandates_1H.append(cumulative_counter_1H)

# Manually set the cumulative values based on the information provided
manual_cumulative_values = [5000, 10000, 15000, 20000, 23298]

# Extend the last point of the step function to the current date for better visibility
final_extended_dates = list(pd.to_datetime(['05/10/2023 18:24:12', '06/10/2023 11:53:13', '08/10/2023 07:47:31', '09/10/2023 08:24:03', '10/10/2023 00:42:26'])) + [pd.Timestamp.now().normalize() + pd.Timedelta(days=1)]
final_cumulative_values = manual_cumulative_values + [manual_cumulative_values[-1]]

# Create a single plot showing both the cumulative number of mandates paid and the cumulative number of mandates created
plt.figure(figsize=(15, 7))

# Plot the cumulative number of paid mandates over time with 1-hour intervals
plt.plot(time_bins_1H[:-1], cumulative_paid_mandates_1H, marker='', linestyle='-', color='g', label='Nombre Cumulatif de Mandats Payés')

# Plot the manually corrected cumulative number of mandates created on each unique creation date as step function extended to the current date
plt.step(final_extended_dates, final_cumulative_values, where='post', marker='o', linestyle='-', color='b', label='Nombre Cumulatif de Mandats Créés')

plt.xlabel('Date')
plt.ylabel('Nombre Cumulatif')
plt.title('Évolution Cumulative des Mandats Créés et Payés, Étendu à la Date Actuelle')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.show()
