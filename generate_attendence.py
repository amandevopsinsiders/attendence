import os
import pandas as pd
from datetime import datetime
import re


# Function to read CSV files in the 'down' folder
def read_csv_files(folder_path):
    data = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            filepath = os.path.join(folder_path, filename)
            df = pd.read_csv(filepath)
            if len(df) > 50:
                data[filename] = df
    return data


# Function to combine data from multiple CSV files
def combine_data(csv_data):
    combined_data = {}
    for filename, df in csv_data.items():
        date_str = filename[:10]  # Extract the first 10 characters as the date
        date = datetime.strptime(date_str, "%Y-%m-%d")
        day_name = date.strftime("%A")  # Extract the day name directly
        date_formatted = date.strftime("%A %d %b")
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
            combined_data[name][date_formatted] = duration
    return combined_data



# Function to filter columns to only include Saturdays and Sundays
def filter_weekend_columns(df):
    weekend_columns = [col for col in df.columns if "Saturday" in col or "Sunday" in col]
    return df[weekend_columns]

def generate_csv(data, filename):
    combined_data = combine_data(data)
    df = pd.DataFrame(combined_data).T  
    df = filter_weekend_columns(df)

    # Assuming the day names in the filenames are correct and should not be changed
    # Remove the conversion to datetime and back to string
    # Just sort the columns based on the day names assuming they follow the correct order

    # Sort the columns based on the day names
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    #df.columns = sorted(df.columns, key=lambda x: days_order.index(x.split(' ')[0]))
    df.columns = sorted(df.columns, key=lambda x: (days_order.index(x.split(' ')[0]), -datetime.strptime(' '.join(x.split(' ')[1:]), "%d %b").timestamp()))


    df.to_csv(filename)


def main():
    batch14 = read_csv_files("b14_down")
    generate_csv(batch14, "attendance_batch14.csv")

    batch15 = read_csv_files("b15_down")
    generate_csv(batch15, "attendance_batch15.csv")

if __name__ == "__main__":
    main()
