import pandas as pd

def update_data_csv(input_csv, update_csv):
    df_input = pd.read_csv(input_csv)
    df_update = pd.read_csv(update_csv)

    columns = list(df_update.columns)
    pairs = [(columns[i], columns[i+1]) for i in range(0, len(columns), 2)]
    
    for area_code_col, new_value_col in pairs:
        if area_code_col not in df_update.columns or new_value_col not in df_update.columns:
            continue
        
        for _, update_row in df_update.iterrows():
            area_code = update_row[area_code_col]
            new_value = update_row[new_value_col]
            
            if area_code in df_input['Area Code'].values and pd.notna(new_value):
                df_input.loc[df_input['Area Code'] == area_code, new_value_col] = new_value

    df_input.to_csv(input_csv, index=False)
    print(f"Updated columns for matching area codes from {update_csv}.")

year_input = input("Please enter the year to update: ")
update_file = f'{year_input}_update_data.csv'
input_file = f'{year_input}_data.csv'

update_data_csv(input_file, update_file)