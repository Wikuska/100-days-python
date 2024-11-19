import pandas as pd
df = pd.read_csv("salaries_by_college_major.csv")

# Show 5 first rows of dataframe
print(df.head())

# See number of rows and columns - 51 rows 6 columns
print(df.shape)

# See column names
print(df.columns)

# Look for missing values and junk data
print(df.isna())
# See 5 last rows of dataframe
print(df.tail())

# Delete row with blank values
clean_df = df.dropna()
clean_df.tail()

# Find the highest starting salary
print(clean_df["Starting Median Salary"].max())

# Find which college major earn that much
print(clean_df["Starting Median Salary"].idxmax())
print(clean_df["Undergraduate Major"].loc[43])

# Find what college major has the highest mid-career salary and how much they earn
print(clean_df["Undergraduate Major"].loc[clean_df["Mid-Career Median Salary"].idxmax()])
print(clean_df["Mid-Career Median Salary"].max())

# Find which college major has the lowest starting salary and how much do graduates earn
print(clean_df["Undergraduate Major"].loc[clean_df["Starting Median Salary"].idxmin()])
print(clean_df["Starting Median Salary"].min())

# Find which college major has the lowest mid-career salary and how much can people expect to earn through years
print(clean_df.loc[clean_df["Mid-Career Median Salary"].idxmin()])

# Count difference between two columns and present results as new column in df
spread_col = clean_df["Mid-Career 90th Percentile Salary"] - clean_df["Mid-Career 10th Percentile Salary"]
clean_df.insert(1, 'Spread', spread_col)

# Sorting by the lowest spread
low_risk = clean_df.sort_values('Spread')
print(low_risk[['Undergraduate Major', 'Spread']].head())

# Sorting by highest spread
high_risk = clean_df.sort_values('Spread', ascending = False)
print(high_risk[['Undergraduate Major', 'Spread']].head())

# Sorting by highest values in the 90th percentile
high_potential = clean_df.sort_values("Mid-Career 90th Percentile Salary", ascending = False)
print(high_potential[['Undergraduate Major', 'Mid-Career 90th Percentile Salary']].head())
