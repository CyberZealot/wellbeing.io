import pandas as pd
import json
import csv
import os
from sklearn import preprocessing

def calculate_median(column):
    return column.median()

def calculate_value(column, median):
    value = median * column
    return value

def calculate_component(column):
    worst_case = column.min()
    best_case = column.max()
    component = (column - worst_case) / (best_case - worst_case) * 100
    rounded_component = component.round(0)  
    return rounded_component

def calculate_domain(df, domain_counter):
    component_columns = [col for col in df.columns if col.endswith(f'_Score{domain_counter}')]
    df[f'Domain{domain_counter}'] = df[component_columns].mean(axis=1).round(0)
    return df

def calculate_index(df):
    domain_sum_columns = [col for col in df.columns if col.startswith('Domain')]
    df['Index Score'] = df[domain_sum_columns].mean(axis=1).round(0)
    return df

def export_json(csvFile, jsonFile, year):
    data = []
    substrings = ['Score', 'Domain', 'Index Score']  
    
    with open(csvFile, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)

        for row in csvReader:
            area_code = row['Area Code']
            area_data = {}
            for col in row:
                if any(sub in col for sub in substrings):
                    data_key_name = f"{year}_{area_code}_{col}"
                    area_data[data_key_name] = row[col]
            if area_data:  
                data.append(area_data)

    with open(jsonFile, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))

def validate_data(input_year):
    if input_year.isdigit() and len(input_year) == 4:
        return True
    else:
        return False

# Interface
print("|███Wellbeing.io████████████████████████|")
area_input = input("Please enter the area code for the Authority you wish to upload: ")
year_input = input("Please enter the year to update: ")
while not validate_data(year_input):
    print("Invalid date format. Please enter a valid year (four-digits).")
    year_input = input("Please enter the year to update: ")

input_file = f'{year_input}_data.csv'
output_file = 'index_output.csv'
df = pd.read_csv(input_file)

columns_to_normalize = ['Library', 'Voters', 'Hate Crimes', 'Heritage', 'Community', 'Sports', 'Public Transport', 
'Faith', 'Volunteering', 'Unemployment Benefits', 'Social Housing', 'Credit', 'FSM', 'Unemployment', 'Child Poverty', 
'Annual Income', 'Income After Housing', 'Homelessness', 'Home Ownership', 'Food Banks', 'Fires', 'Traffic Accidents', 
'Fly Tipping', 'Recycling Rate', 'Noise Levels', 'Park Distance', 'KS Attainment', 'Absentism', 'Youth Training', 'Obesity Rates', 
'Child Obesity', 'Teenage Pregnancy', 'Life Expectancy', 'NHS']

for col in columns_to_normalize:
    df[col] = pd.to_numeric(df[col], errors='coerce')
    if col in df.columns and df[col].notna().sum() > 0: 
        df[col] = df[col].fillna(df[col].mean())

scaler = preprocessing.MinMaxScaler()
for col in columns_to_normalize:
    if col in df.columns and df[col].notna().sum() > 0:
        df[[col]] = scaler.fit_transform(df[[col]])

# Alternative normalising method
#for col in columns_to_normalize:
 #   if col in df.columns and df[col].notna().sum() > 0:
  #      df[col] = preprocessing.normalize([df[col]])[0]

result_df = pd.DataFrame()
result_df[df.columns[0]] = df[df.columns[0]] 

domain_counter = 1
domain_dfs = []
domain_df = result_df.copy()

for col in df.columns[1:]:  
    if df[col].dropna().empty:  
        domain_df = calculate_domain(domain_df, domain_counter)
        domain_dfs.append(domain_df)
        
        domain_counter += 1
        domain_df = result_df.copy()
        continue
    
    median_value = calculate_median(df[col])
    value = calculate_value(df[col], median_value)
    domain_df[f'{col}_Median{domain_counter}'] = median_value
    domain_df[f'{col}_Value{domain_counter}'] = value
    component = calculate_component(value)
    domain_df[f'{col}_Score{domain_counter}'] = component

domain_df = calculate_domain(domain_df, domain_counter)
domain_dfs.append(domain_df)

final_result_df = pd.concat(domain_dfs, axis=1)

final_result_df = calculate_index(final_result_df)

final_result_df.to_csv(output_file, index=False)

json_output_file = f'{year_input}_data.json'
if not os.path.exists(json_output_file):
    with open(json_output_file, 'w') as jsonf:
        json.dump({}, jsonf)

export_json(output_file, json_output_file, year_input)

print(" ")
print(f'Results have been written to {output_file}, you can upload these to the GitHub [https://github.com/CyberZealot/wellbeing.io] as a pull request')
print(" ")
print("|███Wellbeing.io████████████████████████|")