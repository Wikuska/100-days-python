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