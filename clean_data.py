import pandas as pd
import numpy as np

try:
    # Load the data
    df = pd.read_csv('messy_population_data.csv')
    print(f"Data loaded successfully. Rows: {df.shape[0]}, Columns: {df.shape[1]}")

    # Drop duplicate rows
    df = df.drop_duplicates()
    print(f"Rows after dropping duplicates: {df.shape[0]}")

    # Handle missing values by dropping rows with any null values
    df = df.dropna()
    print(f"Rows after dropping missing values: {df.shape[0]}")

    # Handle outliers
    # Remove future years (year > 2024)
    df = df[df['year'] <= 2024]
    print(f"Rows after removing future years (year > 2024): {df.shape[0]}")

    # Handle outliers in the 'population' column using IQR method
    Q1 = df['population'].quantile(0.25) # Identify Q1
    Q3 = df['population'].quantile(0.75) # Identify Q3
    IQR = Q3 - Q1 # Calculate the IQR
    df = df[~((df['population'] < (Q1 - 1.5 * IQR)) | (df['population'] > (Q3 + 1.5 * IQR)))]
    print(f"Rows after handling outliers in 'population': {df.shape[0]}")

    # Handle outliers in the 'age' column using IQR method
    Q1 = df['age'].quantile(0.25) # Identify Q1
    Q3 = df['age'].quantile(0.75) # Identify Q3
    IQR = Q3 - Q1 # Calculate the IQR
    df = df[~((df['age'] < (Q1 - 1.5 * IQR)) | (df['age'] > (Q3 + 1.5 * IQR)))]
    print(f"Rows after handling outliers in 'age': {df.shape[0]}")

    # Handle invalid 'gender' values
    df = df[df['gender'] != 3] # Remain the records with Gender = 1 or 2
    print(f"Rows after handling invalid 'gender' values: {df.shape[0]}")

    # Fix inconsistencies in the 'income_groups' column by removing '_typo'
    df['income_groups'] = df['income_groups'].str.replace('_typo', '', regex=False) # Replace '_typo' to ''
    print("Removing '_typo' in the 'income_groups' column.")

    # Change the data type of gender from float to category
    df['gender'] = df['gender'].astype('category')

    # Reset index
    df = df.reset_index(drop=True)

    # Save the cleaned data
    df.to_csv('cleaned_population_data.csv', index=False)
    print("Saving the cleaned data to 'cleaned_population_data.csv'.")

except Exception as e:
    print(f"Error during the data cleaning process: {e}")
