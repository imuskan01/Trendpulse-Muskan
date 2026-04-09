# TrendPulse - Task 3: Analysis with Pandas and NumPy
# Author: Muskan
# Date: April 2026

import pandas as pd     
import numpy as np        

# STEP 1: Load the cleaned CSV from Task 2 and explore it

# Load the CSV file into a DataFrame
df = pd.read_csv("data/trends_clean.csv")

print(f"Loaded data: {df.shape}")   # shape gives (rows, columns)

# Print first 5 rows to see what the data looks like
print("\nFirst 5 rows:")
print(df.head())

# Print average score and average num_comments across all stories
avg_score    = df["score"].mean()
avg_comments = df["num_comments"].mean()

print(f"\nAverage score   : {avg_score:.3f}")
print(f"Average comments: {avg_comments:.3f}")

# STEP 2: NumPy statistics on the score column
# We convert the column to a NumPy array first for np functions

scores = df["score"].to_numpy()        # convert pandas column to numpy array
comments = df["num_comments"].to_numpy()

print("\n--- NumPy Stats ---")

# Mean = average value
mean_score = np.mean(scores)
print(f"Mean score   : {mean_score:.3f}")

# Median = middle value when sorted — less affected by outliers than mean
median_score = np.median(scores)
print(f"Median score : {median_score:.3f}")

# Standard deviation = how spread out scores are from the mean
std_score = np.std(scores)
print(f"Std deviation: {std_score:.3f}")

# Max and min scores
max_score = np.max(scores)
min_score = np.min(scores)
print(f"Max score    : {max_score}")
print(f"Min score    : {min_score}")

# value_counts() returns categories sorted by count, idxmax() gets the top one
top_category       = df["category"].value_counts().idxmax()
top_category_count = df["category"].value_counts().max()
print(f"\nMost stories in: {top_category} ({top_category_count} stories)")

# idxmax() returns the row index of the highest num_comments value
most_commented_idx   = df["num_comments"].idxmax()
most_commented_title = df.loc[most_commented_idx, "title"]
most_commented_count = df.loc[most_commented_idx, "num_comments"]
print(f"\nMost commented story: \"{most_commented_title}\" — {most_commented_count} comments")

# STEP 3: Add two new columns to the DataFrame

# engagement = num_comments / (score + 1)
# We add 1 to score to avoid division by zero if score is 0
# This tells us how much discussion a story gets per upvote
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# is_popular = True if the story's score is above the average score
# avg_score was calculated earlier using df["score"].mean()
df["is_popular"] = df["score"] > avg_score

print("\nNew columns added: engagement, is_popular")
print(f"Popular stories count: {df['is_popular'].sum()}")   # how many are True

# STEP 4: Save the updated DataFrame to a new CSV file

output_file = "data/trends_analysed.csv"

# index=False so we don't write row numbers into the CSV
df.to_csv(output_file, index=False)

print(f"\nSaved to {output_file}")