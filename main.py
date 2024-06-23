# Import necessary libraries
import pandas as pd
import re
import os

def pipeline():
    """
    Main pipeline function to process recipe data.
    
    Steps:
    1. Load JSON data into a DataFrame.
    2. Clean and normalize ISO 8601 duration strings in 'cookTime' and 'prepTime' columns.
    3. Calculate the total time by summing 'cookTime' and 'prepTime'.
    4. Filter recipes containing specific words in the 'ingredients' column.
    5. Calculate difficulty level based on total time.
    6. Print filtered DataFrame and save it to CSV.

    Returns:
    None
    """
    # Load JSON data directly into a DataFrame
    print(os.path.abspath(__file__))
    df = pd.read_json(os.path.abspath(__file__).replace('main.py', 'recipes.json'), lines=True)
    
    # Clean and normalize ISO 8601 duration strings in 'cookTime' and 'prepTime' columns
    for c in ['cookTime', 'prepTime']:
        df[c] = df[c].apply(clean_duration)

    # Calculate the sum of 'cookTime' and 'prepTime' to get 'totalTime'
    df['totalTime'] = df['cookTime'] + df['prepTime']
    
    # Filter recipes containing specific words in the 'ingredients' column
    filter_recipes = find_words(df, 'ingredients', 'chilies')
    
    # Apply the calculate_difficulty function to create the 'difficulty' column
    filter_recipes['difficulty'] = filter_recipes['totalTime'].apply(calculate_difficulty)
    
    # Print the filtered DataFrame with relevant columns and save to CSV
    print(filter_recipes)
    filter_recipes.to_csv('filtered_recipes.csv', index=True)
    print("CSV Generated.")

# Function to find rows containing specific words in a column
def find_words(df, column, word):
    """
    Function to filter DataFrame rows containing specific words in a column.

    Parameters:
    df (DataFrame): Input DataFrame.
    column (str): Name of the column to search.
    word (str): Word to search for.

    Returns:
    DataFrame: Filtered DataFrame containing rows with the specified word in the specified column.
    """
    regex_pattern = rf'\b{word}[a-z]*\b'
    search_pattern = df[column].str.contains(regex_pattern, case=False, na=False, regex=True)
    return df[search_pattern]

def clean_duration(duration_str):
    """
    Clean and normalize ISO 8601 duration strings.

    Parameters:
    duration_str (str): Input ISO 8601 duration string.

    Returns:
    str: Cleaned and normalized duration string, or None if invalid format.
    """
    try:
        # Parse the duration string to check for validity
        return pd.to_timedelta(duration_str)  # Return the input string if it's already in valid format
    except ValueError:
        # Clean up the string by removing any non-ISO-8601 characters
        cleaned_str = re.sub(r'[^PYMDTHS\d]', '', duration_str)
        try:
            # Try parsing the cleaned string
            return pd.to_timedelta(cleaned_str)  # Return the cleaned string if it's valid after cleaning
        except ValueError:
            return None  # Return None for invalid format

def calculate_difficulty(total_time):
    """
    Calculate difficulty level based on total time in minutes.

    Parameters:
    total_time (Timedelta): Total time of the recipe.

    Returns:
    str: Difficulty level ('Hard', 'Medium', 'Easy', or 'Unknown').
    """
    total_minutes = pd.to_timedelta(total_time).total_seconds() // 60  # Calculate total time in minutes
    if total_minutes > 60:  # Check if total time is greater than 60 minutes
        return 'Hard'
    elif 30 <= total_minutes <= 60:  # Check if total time is between 30 and 60 minutes
        return 'Medium'
    elif total_minutes < 30:  # Check if total time is less than 30 minutes 
        return 'Easy'
    else:
        return 'Unknown'  # Default case if conditions are not met

if __name__ == '__main__':
    pipeline()
