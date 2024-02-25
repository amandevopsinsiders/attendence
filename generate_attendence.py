import os
import pandas as pd
from datetime import datetime

# Function to read CSV files in the 'down' folder
def read_csv_files_for_batch14(folder_path):
    data = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            filepath = os.path.join(folder_path, filename)
            df = pd.read_csv(filepath)
            if len(df) > 50 & len(df) < 130:
                data[filename] = df
    return data

def read_csv_files_for_batch15(folder_path):
    data = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            filepath = os.path.join(folder_path, filename)
            df = pd.read_csv(filepath)
            if len(df) > 130:
                data[filename] = df
    return data


# Function to combine data from multiple CSV files
def combine_data(csv_data):
    combined_data = {}
    for filename, df in csv_data.items():
        date = datetime.strptime(filename.split()[0], "%Y-%m-%d").strftime("%A %d %b")
        for index, row in df.iterrows():
            first_name = row['First name']
            last_name = row['Last name']
            if pd.isna(last_name):
                name = first_name
            else:
                name = first_name + ' ' + last_name
            duration = row['Duration']
            if name not in combined_data:
                combined_data[name] = {}
            combined_data[name][date] = duration
    return combined_data

# Function to filter columns to only include Saturdays and Sundays
def filter_weekend_columns(df):
    weekend_columns = [col for col in df.columns if "Saturday" in col or "Sunday" in col]
    return df[weekend_columns]

def generate_csv(data, filename):
    combined_data = combine_data(data)
    df = pd.DataFrame(combined_data).T  
    df = filter_weekend_columns(df)
    df.columns = pd.to_datetime(df.columns, format='%A %d %b')
    
    df = df.sort_index(axis=1, ascending=False)
    df.columns = df.columns.strftime('%A %d %b')

    df.to_csv(filename)

def main():
    folder_path = "down"

    batch14 = read_csv_files_for_batch14(folder_path)
    generate_csv(batch14, "attendance_batch14.csv")

    batch15 = read_csv_files_for_batch15(folder_path)
    generate_csv(batch15, "attendance_batch15.csv")

if __name__ == "__main__":
    main()