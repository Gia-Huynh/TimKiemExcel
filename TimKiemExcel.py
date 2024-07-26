import os
import traceback

#directory_path = '.'
# File path to the text file containing the directory path
file_with_path = 'pathfile.txt'

# Read the directory path from the file
with open(file_with_path, 'r') as file:
    directory_path = file.read().strip()

print(f"The directory path is: {directory_path}")


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
                elif entry.is_file() and entry.name.endswith('.'+file_extension) and not entry.name.startswith ("~$"):
                    gay.append (entry.path)
            return gay
        except PermissionError:
            print ("Permission Error at {directory}, skipping...")
            return gay
    return search (directory, 0)

def build_database (path_list):
    database = {}
    best_col = {}
    for path in path_list:
        print (path)
        df = pd.read_excel(path, engine='calamine') #, sheet_name = None
        #If over 66% of a column is NaN, drop it
        df = df.dropna (axis = 1, thresh = int(df.shape[0]*0.66))
        # Convert all columns to string
        df = df.map (str)
        avg_lengths = df.apply(lambda x: x.str.len().sum())
        database [path] = df
        # Find the column with the maximum sum length
        max_avg_column = avg_lengths.idxmax()        
        best_col [path] = max_avg_column
    return database, best_col

all_paths = get_all_file(directory_path)
print (all_paths[0:5])
import pandas as pd
from fuzzywuzzy import process
database, best_col = build_database (all_paths)

# Function to search for a string in an Excel file
def search_in_excel(file_path, search_string, threshold = 90):
    try:
        df = database[file_path]
        col = best_col[file_path]

        # Use fuzzy matching to find close matches
        close_matches = process.extract(search_string, df[col], limit=10)
        result = []
        for match in close_matches:
            if (match[1] >= threshold) or (len(result)<5 and (match[1] >= threshold*0.75)):
                nigga_string = df.iloc[match[2]].to_string(header=False, index=False)

                #remove tabs and spaces
                cleaned_string = ' '.join(nigga_string.split())
                #remove date format
                if cleaned_string.find ("00:00:00") != -1:
                    cleaned_string = cleaned_string [cleaned_string.find ("00:00:00")+9:]
                
                result.append ([match[2], cleaned_string])      
        return result, col
    except Exception as e:
        traceback.print_exc()
        print(f"Error reading {file_path}: {e}")
        return None, None


def search_in_directory(directory, search_string, threshold):
    results = []
    for file_path in all_paths:
        result, column_idx = search_in_excel(file_path, search_string, threshold)
        if result is not None:
            results.append((file_path, result, column_idx))
    return results

def wrapper_function (search_string, directory_path = directory_path, threshold = 90):
    print("_"*10 + "\n" + " "*10)
    search_results = search_in_directory(directory_path, search_string, threshold)
    for result in search_results:
        filename, match_result, column_idx = result
        if (match_result is not None) and (len (match_result)!=0):
            print(f"Found in {filename}:")
            for row in match_result:
                print ("    ",str(row[0]) + ":",row[1])
            print (" "*10)
search_string = 'khay'
wrapper_function (search_string)

class RedirectText(object):
    def __init__(self, text_widget):
        self.output = text_widget

    def write(self, string):
        self.output.insert(tk.END, string)
        self.output.see(tk.END)

    def flush(self):
        pass

def submit():
    try:
        value = str(entry.get())
        try:
            threshold = int(entry2.get())
        except ValueError:
            print ("Loi threshold, dung threshold mac dinh la 90")
            threshold = 90
        wrapper_function(value, threshold = threshold)
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter a valid number")
import tkinter as tk
import sys
from tkinter import messagebox, scrolledtext

def clear_output():
    output_text.delete(1.0, tk.END)

root = tk.Tk()
root.title("My App")

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
#root.rowconfigure(1, weight=0)
#root.rowconfigure(2, weight=0)

frame = tk.Frame(root)
frame.grid(sticky="nsew")

frame.columnconfigure(0, weight=2)
frame.columnconfigure(1, weight=1)
frame.rowconfigure(0, weight=0)
frame.rowconfigure(1, weight=0)
frame.rowconfigure(2, weight=0)
frame.rowconfigure(3, weight=1)

label = tk.Label(frame, text="Enter a value")
label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

entry = tk.Entry(frame)
entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

label2 = tk.Label(frame, text="Threshold (0-100):")
label2.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

entry2 = tk.Entry(frame)
entry2.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
entry2.insert(tk.END, '90')

submit_button = tk.Button(frame, text="Submit", command=submit)
submit_button.grid(row=2, column=1, padx=10, pady=10, sticky="n")
clear_button = tk.Button(frame, text="Clear Output", command=clear_output)
clear_button.grid(row=3, column=1, padx=10, pady=10, sticky="n")

output_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD)
output_text.grid(row=3, column=0, sticky="nsew")

sys.stdout = RedirectText(output_text)

root.mainloop()
