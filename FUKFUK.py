import os
import pandas as pd
from fuzzywuzzy import process
import traceback
# Function to search for a string in an Excel file
def search_in_excel(file_path, search_string):
    try:
        df = pd.read_excel(file_path, engine='openpyxl')
        # Convert all columns to string for easier searching
        df = df.map (str)
        avg_lengths = df.apply(lambda x: x.str.len().mean())
        # Find the column with the maximum average length
        max_avg_column = avg_lengths.idxmax()
        
        # Iterate over each row and search for the string
        
        col = max_avg_column
        #for index, row in df.iterrows():
            #if search_string in row[col]:
            #    return [row.tolist()], [index], [1.01]
            #else:
                # Use fuzzy matching to find close matches
        close_matches = process.extract(search_string, df[col], limit=10)
        result = []
        for match in close_matches:
            if (match[1] >= threshold) or len(result)<5:
                result.append (match)
                #best_match, score, wtf = close_matches[0]
                #if score > 85:  # Adjust the similarity threshold as needed
                #    return row.tolist(), index, f"Close match found in '{col}' column: '{best_match}' with score {score}"
        return result, max_avg_column
    except Exception as e:
        traceback.print_exc()
        print(f"Error reading {file_path}: {e}")
        return None, None

# Function to search in all Excel files in a directory
def search_in_directory(directory, search_string):
    results = []
    for filename in os.listdir(directory):
        if filename.endswith(".xlsx"):
            file_path = os.path.join(directory, filename)
            result, column_idx = search_in_excel(file_path, search_string)
            print (column_idx,' ayyyy')
            if result is not None:
                results.append((filename, result, column_idx))
    return results

threshold = 85
directory_path = 'C:/Users/za/Desktop/'
def wrapper_function (search_string, directory_path = directory_path):
    search_results = search_in_directory(directory_path, search_string)
    for result in search_results:
        filename, match_result, column_idx = result
        print(f"Found in {filename} at columnidx = {column_idx}:")
        for a in match_result:
            print ("    ",a)
    
# Example usage
#search_string = 'xe đẩy'
search_string = 'khay'
wrapper_function (search_string)
