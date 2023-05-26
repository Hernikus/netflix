#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 25 14:55:52 2023

@author: hernikusuma
"""

import pandas as pd
import requests
import csv
from io import StringIO

url = 'https://raw.githubusercontent.com/kedeisha1/Challenges/main/netflix_titles.csv'
response = requests.get(url)
data = response.text

# Parse the CSV data
reader = csv.reader(StringIO(data))
rows = list(reader)

output_file = 'netflix_titles_converted.csv'

with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(rows)


# Import csv files to data frame
netflix_data = pd.read_csv('netflix_titles_converted.csv', sep=',')

#check for missing value
column_missing_data = netflix_data.columns[netflix_data.isnull().any()]
missing_values_count = netflix_data.isnull().sum()

# drop missing date value 
netflix_data = netflix_data.dropna(subset=['date_added'])

# fill missing data value
netflix_data = netflix_data.fillna('Not Available')


# Split 'date_added' column
netflix_data['month_added'] = pd.to_datetime(netflix_data['date_added']).dt.strftime('%B')
netflix_data['year_added'] = pd.to_datetime(netflix_data['date_added']).dt.strftime('%Y')
netflix_data['date_added'] = pd.to_datetime(netflix_data['date_added']).dt.strftime('%d')

# Cek all data type
netflix_data.info()

# Change data type of 'year_added' and 'date_added' column to integer
netflix_data['date_added'] = netflix_data['date_added'].astype(int)
netflix_data['year_added'] = netflix_data['year_added'].astype(int)

# Count the number of data for each year
year_count = netflix_data['year_added'].value_counts()

# Split column to genre
split_col = netflix_data['listed_in'].str.split(',', expand=True)
netflix_data['genre'] = split_col[0]

# make a new csv for cleaned data
netflix_data.to_csv('netflix_cleaned.csv', index=False)

# Filter the DataFrame based on the color
movie = netflix_data[netflix_data['type'] == 'Movie'] 
tv_show = netflix_data[netflix_data['type'] == 'TV Show'] 

# Find the longest data in the filtered DataFrame Movie
longest_data = movie['title'].str.len().idxmax()
longest_value = movie.loc[longest_data, 'title']

# Find the longest data in the filtered DataFrame Tv Show
longest_show = tv_show['title'].str.len().idxmax()
longest_valueshow = tv_show.loc[longest_show, 'title']

