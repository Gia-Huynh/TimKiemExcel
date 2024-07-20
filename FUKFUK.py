import os
import pandas as pd
from fuzzywuzzy import process
import traceback
# Function to search for a string in an Excel file
def search_in_excel(file_path, search_string):
    try:
        df = pd.read_excel(file_path, engine='openpyxl')
        #If over 66% of a column is NaN, drop it
        df = df.dropna (axis = 1, thresh = int(df.shape[0]*0.66))
        
        # Convert all columns to string for easier searching
        df = df.map (str)
        avg_lengths = df.apply(lambda x: x.str.len().sum())
        # Find the column with the maximum sum length
        max_avg_column = avg_lengths.idxmax()        
        col = max_avg_column

        # Use fuzzy matching to find close matches
        close_matches = process.extract(search_string, df[col], limit=10)
        result = []
        for match in close_matches:
            if (match[1] >= threshold) or (len(result)<5 and (match[1] >= threshold*0.8)):
                nigga_string = df.iloc[match[2]].to_string(header=False, index=False)

                #remove tabs and spaces
                cleaned_string = ' '.join(nigga_string.split())
                #remove date format
                if cleaned_string.find ("00:00:00") != -1:
                    cleaned_string = cleaned_string [cleaned_string.find ("00:00:00")+9:]
                    
                result.append ([cleaned_string, match[1]])
                #result.append ([, match[1]])                
        return result, max_avg_column
    except Exception as e:
        traceback.print_exc()
        print(f"Error reading {file_path}: {e}")
        return None, None

def get_all_file (directory, file_extension = "xlsx", depth_max = 3):
    def search(directory, current_depth):
        gay = []
        if current_depth > depth_max:
            return gay
        try:
            for entry in os.scandir(directory):
                if entry.is_dir(follow_symlinks=False):
                    nigger = search(entry.path, current_depth + 1)
                    gay = gay + nigger
                elif entry.is_file() and entry.name.endswith('.'+file_extension):
                    gay.append (entry.path)
            return gay
        except PermissionError:
            print ("Permission Error at {directory}, skipping...")
            return gay
    return search (directory, 0)
# Function to search in all Excel files in a directory
def search_in_directory(directory, search_string):
    results = []
    for filename in os.listdir(directory):
        if filename.endswith(".xlsx"):
            file_path = os.path.join(directory, filename)
            result, column_idx = search_in_excel(file_path, search_string)
            if result is not None:
                results.append((filename, result, column_idx))
    return results

threshold = 90
directory_path = './Data'
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
