import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the CSV file into a DataFrame
df = pd.read_csv('spotify-data.csv')

# Convert release_date to datetime format, handling cases where it's just the year
df['release_date'] = df['release_date'].apply(lambda x: pd.to_datetime(x, format='%m/%d/%Y') if len(str(x)) > 4 else pd.to_datetime(x, format='%Y'))

# Extract year from release_date and create a new column release_year
df['release_year'] = df['release_date'].dt.year

# Plotting the distribution of valence over the years
plt.figure(figsize=(12, 6))
sns.boxplot(x='release_year', y='valence', data=df)
plt.title('Distribution of Valence Over the Years (2000-2010)')
plt.xlabel('Release Year')
plt.ylabel('Valence')
plt.grid(True)
plt.show()
