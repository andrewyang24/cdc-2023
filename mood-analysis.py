import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the CSV file into a DataFrame
df = pd.read_csv('spotify-data.csv')

# For mood analysis, assume 'valence' is a column representing the positiveness of a track
# You may need to adapt this based on the actual structure of your data

# Plotting the distribution of valence over the years
plt.figure(figsize=(12, 6))
sns.boxplot(x='release_year', y='valence', data=df)
plt.title('Distribution of Valence Over the Years (2000-2010)')
plt.xlabel('Release Year')
plt.ylabel('Valence')
plt.grid(True)
plt.show()