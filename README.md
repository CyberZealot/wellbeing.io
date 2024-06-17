# wellbeing.io
https://cyberzealot.github.io/wellbeing.io/

A measurement of wellbeing for local authorities utilising a data-driven approach.

Consists of two Python scripts.

## Wellbeing.py

### YEAR_Data.csv

### YEAR_Index_Output.csv
The full data output is written to this .csv file. 

### YEAR_Data.json
The .json file is formatted as to be readable to the Dashboard.

### Value
````
Indicator data * median
````
### Component
````
Value - Min / (Max - Min) * 100
````
### Domain
````
Average of Components
````
### Index
````
Average of Domains
````

## Data_Update.py
| Area Code     | Indicator     | Area Code     | Indicator     | 
| ------------- | ------------- | ------------- | ------------- |
| EXXXXXXXXXXX  | Data          | EXXXXXXXXXXX  | Data          |
| EXXXXXXXXXXY  | Data          | EXXXXXXXXXXY  | Data          |

### YEAR_Update_Data.csv
Place the data into the corresponding column, ensuring to pair it with the area code of the local authority. AREA CODE | DATA
