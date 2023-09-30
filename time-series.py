import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Assume 'df' is your DataFrame containing Spotify data
df = pd.read_csv('spotify-data.csv')

# Convert the release_date column to datetime format
df['release_date'] = pd.to_datetime(df['release_date'])

# Extract the year from the release_date
df['release_year'] = df['release_date'].dt.year

# Group by release year and count the number of songs released each year
time_series_data = df['release_year'].value_counts().sort_index()

# Plotting the time series
plt.figure(figsize=(12, 6))
sns.lineplot(x=time_series_data.index, y=time_series_data.values, marker='o')
plt.title('Number of Songs Released Over the Years (2000-2010)')
plt.xlabel('Release Year')
plt.ylabel('Number of Songs')
plt.grid(True)
plt.show()
