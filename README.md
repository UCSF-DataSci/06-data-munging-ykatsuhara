# Data Cleaning Project: Population Dataset

## 1. Initial State Analysis

### Dataset Overview
- **Name**: messy_population_data.csv
- **Rows**: 125718
- **Columns**: 5 columns ('income_groups', 'age', 'gender', 'year', 'population')



### Column Details
| Column Name   | Data Type | Non-Null Count | Unique Values | Mean        |
|---------------|-----------|----------------|---------------|-------------|
| income_groups | object    | 119412         | 8             | N/A         |
| age           | float64   | 119495         | 101           | 50.007038   |
| gender        | float64   | 119811         | 3             | 1.578578    |
| year          | float64   | 119516         | 169           | 2025.068049 |
| population    | float64   | 119378         | 114925        | 1.112983e+08 |



### Identified Issues
1. **Duplicated values:**
- Description: Several records are duplicated
- Affected Column(s): N/A
- Example: There are 2,950 records are duplicated.
- Potential Impact: Duplicated record will skew data distribution and it cause the biased results.

2. **Null values:**
- Description: Several columns contain missing values.
- Affected Column(s): All columns contain null values.
- Example: There are 6,223 records with missing age values.
- Potential Impact: If the missing values are not randomly distributed, for example, if individuals with lower income are more likely to have missing age values, the analysis might not accurately reflect the true population. This could lead to biased outcomes.

3. **Outliers and questionable values**
- Description: Some columns contain outliers or values that seem implausible.
- Affected Column(s): Gender, Year, Population, Income_group
- Example:
     - **Gender:** The maximum value in the gender column is 3, which is unclear. Typically, gender is binary or may include a third category, but the meaning of this value is uncertain.
     - **Year:** The maximum year recorded is 2219, which is implausible given that we are currently in 2024.
     - **Population:** The some values are quite large when we plot the histgram.
     - **Income Group** Some values include '_typo'.
- Potential Impact: If the values are inaccurate, it could lead to misinterpretation of trends or incorrect model outcomes.

4. **Data type**
- Description: `gender` is set as float.
- Affected Column(s): Gender
- Example:
     - **Gender:**  The data type is float64.
- Potential Impact: If `gender` is treated as a continuous variable (float), it could lead to incorrect interpretations in analyses such as regression models. Gender should be handled as a categorical variable to ensure proper model interpretation and avoid erroneous results.


## 2. Data Cleaning Process
### Issue 1: Duplicated record
- **Cleaning Method**: Remove all duplicated records
- **Implementation**:
```python
df.drop_duplicates()  

```
- **Justification**: We remove all duplicated records because duplicated records will skew data distribution.

- **Impact**: 
  - Rows affected: 125,718 -> 122,768
  - Data distribution change: There is no significant distribution change.

### Issue 2: Null Values
- **Cleaning Method**: Remove all null values
- **Implementation**:
  ```python
  df.dropna()
  ```
- **Justification**: We chose to remove rows with null values because the possibility of Missing Not At Random (MNAR) could not be ruled out. Imputation in the case of MNAR may introduce bias, as the missingness could depend on the unobserved data itself. Sensitivity analysis might be useful to ensure that this strategy was appropriate.

- **Impact**: 
  - Rows affected: 122,768 -> 95,425
  - Data distribution change: There is no significant distribution change.

### Issue 3: Outliers and questionable values
- **Cleaning Method**: 
We applied multiple steps to handle outliers:
  - **Year**: Removed years after 2024 since these values are implausible.
  - **Population & Age**: We used the IQR method to identify and remove extreme values in both the `population` and `age` columns.
  - **Gender**: Excluded rows where `gender` was recorded as 3, since this value is unclear and likely erroneous.
  - **Income Groups**: Fixed a typo in the `income_groups` column by removing the `_typo` suffix.

- **Implementation**:
  ```python
  # Include relevant code snippet
    # Remove future years (year > 2024)
    df = df[df['year'] <= 2024]
    print(f"Rows after removing future years (year > 2024): {df.shape[0]}")

    # Handle outliers in the 'population' column using IQR method
    Q1 = df['population'].quantile(0.25)
    Q3 = df['population'].quantile(0.75)
    IQR = Q3 - Q1
    df = df[~((df['population'] < (Q1 - 1.5 * IQR)) | (df['population'] > (Q3 + 1.5 * IQR)))]
    print(f"Rows after handling outliers in 'population': {df.shape[0]}")

    # Handle outliers in the 'age' column using IQR method
    Q1 = df['age'].quantile(0.25)
    Q3 = df['age'].quantile(0.75)
    IQR = Q3 - Q1
    df = df[~((df['age'] < (Q1 - 1.5 * IQR)) | (df['age'] > (Q3 + 1.5 * IQR)))]
    print(f"Rows after handling outliers in 'age': {df.shape[0]}")

    # Handle invalid 'gender' values
    df = df[df['gender'] != 3]
    print(f"Rows after handling invalid 'gender' values: {df.shape[0]}")

    # Fix inconsistencies in the 'income_groups' column by removing '_typo'
    df['income_groups'] = df['income_groups'].str.replace('_typo', '', regex=False)
    print("Removing '_typo' in the 'income_groups' column.")
  ```
- **Justification**: 
  - The **IQR method** was chosen to handle outliers in `age` and `population` as it is a standard method to detect extreme values that are likely to be anomalies. This method is particularly effective when we don't have domain knowledge about the expected distribution but still want to ensure that the extreme values are reasonable.
  - The removal of years beyond 2024 and the exclusion of `gender = 3` are based on the implausibility of these values in the current dataset. These values could lead to skewed analysis if not handled properly.
  - Correcting the typo in the `income_groups` column ensures that categories remain consistent and meaningful, reducing potential issues in group-based analysis.

- **Impact**: 
  - Rows affected: 95,425 -> 40,438
  - Data distribution change: The distribution of age is left-skewed, while the other variables are right-skewed.

### Issue 4: Data type
- **Cleaning Method**: 
We set `gender` as category.
- **Implementation**:
  ```python
  df['gender'].astype('category')

  ```
- **Justification**: 
Gender should be handled as a categorical variable to ensure proper model interpretation and avoid erroneous results.

- **Impact**: 
  - Rows affected: No impact.
  - Data distribution change: No impact.


## 3. Final State Analysis

### Dataset Overview
- **Name**: cleaned_population_data.csv
- **Rows**: 40438
- **Columns**: 5 columns ('income_groups', 'age', 'gender', 'year', 'population')

### Column Details
| Column Name   | Data Type | Non-Null Count | #Unique Values | Mean         |
|---------------|-----------|----------------|----------------|--------------|
| income_groups | object    | 40438          | 4             | N/A          |
| age           | float64   | 40438          | 101            | 50.003       |
| gender        | category  | 40438          | 2              | 1.576        |
| year          | float64   | 40438          | 75             | 2000.5       |
| population    | float64   | 40438          | 39875         | 1.23e+06     |

### Summary of Changes
#### Major Changes:
- Null values were removed.
- Outliers were detected and removed from the `age` and `population` columns using the IQR method.
- Implausible future years were removed, and the `gender` value 3 was excluded due to uncertainty about its meaning.
- Typographical errors in the `income_groups` column were corrected.


#### Changes in Data Distribution:
- After removing outliers, the distribution of continuous variables are adjusted.
- Removing future years and correcting the income categories helped ensure that the temporal and categorical analysis will be more accurate.
- We treated gender as binary data, with values of 1 or 2. To avoid confusion, it's important to apply the appropriate labels based on the codebook (e.g., 1: Female, 2: Male).
