# Recipe Processing Pipeline

## Overview

This Python script is designed to process recipe data stored in a JSON file, perform data cleaning and normalization, filter recipes based on specific criteria, calculate the difficulty level of each recipe, and save the processed data to a CSV file. The script uses various functionalities from the `pandas`, `re`, and `os` libraries to accomplish these tasks.

## Instructions

### Python Version

Make sure you have Python 3.11.4 installed on your system. You can download Python from the official website: [Python Downloads](https://www.python.org/downloads/)

### Third-Party Modules

Before running the script, you need to install the required third-party modules, these modules are listed in the `requirements.txt` file. Open your terminal or command prompt, navigate to the directory where the `requirements.txt` file is located, and run the following command:

```bash
pip install -r requirements.txt
```
This command will install all the necessary libraries listed in the `requirements.txt` file. If you prefer to install the modules individually, you can install them using the following command:

```bash
pip install pandas
```

This command will install the `pandas` library, which is used for data manipulation and analysis.

### Running the Script

1. Download the script file (`main.py`) and the recipe data file (`recipes.json`) to your local machine.

2. Open your terminal or command prompt and navigate to the directory where the script and data files are located.

3. Run the script using the following command:

```bash
python3 main.py
```

The script will execute the main pipeline function, process the recipe data, calculate difficulty levels, and generate a CSV file named `filtered_recipes.csv` containing the processed data.

## Code Explanation Overview

Here's a breakdown of what the script does and how it accomplishes each step:

1. **Load Data**: The script loads recipe data from a JSON file into a pandas DataFrame.

2. **Clean Duration**: It cleans and normalizes ISO 8601 duration strings in the 'cookTime' and 'prepTime' columns using the `clean_duration` function.

4. **Filter Recipes**: It filters recipes containing specific words (e.g., 'chilies') in the 'ingredients' column using the `find_words` function.

5. **Calculate Difficulty**: The script calculates the difficulty level of each recipe based on the total time in minutes using the `calculate_difficulty` function.

6. **Save to CSV**: Finally, it saves the filtered and processed data to a CSV file named `filtered_recipes.csv`.

### Module Versions

- Python 3.11.4 
- Pandas 2.2.2 
- re: Python's built-in module, no specific version needed
- os: Python's built-in module, no specific version needed

## Code Deep Dive
In this section you will find a deep dive into each function's technical details. 

#### Load Data

```python
def pipeline():
    ...
    df = pd.read_json(os.path.abspath(__file__).replace('main.py', 'recipes.json'), lines=True)
    ...
```

This function uses pandas (`pd`) to load data from a JSON file into a DataFrame (`df`). The `pd.read_json` function reads the JSON file specified by the file path generated using `os.path.abspath(__file__)`, which represents the absolute path of the current script file. The `replace` method is used to replace the script file name (`main.py`) with the data file name (`recipes.json`) in the file path. The `lines=True` parameter indicates that each line in the JSON file represents a separate JSON object.

#### Clean Duration

```python
def clean_duration(duration_str):
    try:
        return pd.to_timedelta(duration_str)  
    except ValueError:
        cleaned_str = re.sub(r'[^PYMDTHS\d]', '', duration_str)
        try:
            return pd.to_timedelta(cleaned_str)  
        except ValueError:
            return None  
```

The `clean_duration` function is used to clean and normalize ISO 8601 duration strings, which represent time durations in a standardized format. The function takes an input duration string (`duration_str`) and attempts to parse it using `pd.Timedelta`. If the parsing succeeds, it returns the original string (`duration_str`), indicating that it's already in a valid format. If parsing fails due to a `ValueError`, the function cleans up the string by removing any characters that are not part of the ISO 8601 format using regular expressions (`re`), specifically `re.sub(r'[^PYMDTHS\d]', '', duration_str)` which replaces any character that is not a valid ISO 8601 character with an empty string. After cleaning, it attempts to parse the cleaned string again, and if successful, returns the cleaned string; otherwise, it returns `None` to indicate an invalid format.


#### Filter Recipes

```python
def find_words(df, column, word):
    regex_pattern = rf'\b{word}[a-z]*\b'
    search_pattern = df[column].str.contains(regex_pattern, case=False, na=False, regex=True)
    return df[search_pattern]

```

The `find_words` function filters DataFrame rows based on specific words (`word`) in a specified column (`column`). It uses regular expressions (`regex`) to create a search pattern that matches words with optional characters after the specified word. It then applies this pattern to the specified column (`df[column]`) using `str.contains` to create a boolean mask (`search_pattern`) that identifies rows containing the target word. Finally, it uses this mask to filter the DataFrame and returns the filtered DataFrame containing rows with the specified word in the specified column.

#### Calculate Difficulty

```python
def calculate_difficulty(total_time):
    total_minutes = pd.to_timedelta(total_time).total_seconds() // 60 
    if total_minutes > 60:  
        return 'Hard'
    elif 30 <= total_minutes <= 60: 
        return 'Medium'
    elif total_minutes < 30:  
        return 'Easy'
    else:
        return 'Unknown' 
```

The `calculate_difficulty` function determines the difficulty level of a recipe based on its total time. It converts the total time to minutes using `pd.to_timedelta` and then calculates the total time in minutes using `total_seconds() // 60`. Based on the total time in minutes, it assigns a difficulty level ('Hard', 'Medium', 'Easy', or 'Unknown').

#### Save to CSV

This function saves a DataFrame (`df`) to a CSV file with the specified filename (`filename`). It uses `to_csv` from pandas to write the DataFrame to a CSV file without including the index column.

## Conclusion

The script's functions work together to process recipe data, clean time durations, filter recipes based on specific criteria, calculate difficulty levels, and save the processed data to a CSV file. Each function serves a specific purpose in the data processing pipeline, contributing to the overall functionality of the script.
