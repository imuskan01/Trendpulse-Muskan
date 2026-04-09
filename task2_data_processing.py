# TrendPulse - Task 2: Clean the data and save as CSV
# Author: [Muskan]

import pandas as pd    
import json            
import os              
import glob            

# STEP 1: Find and load the JSON file from Task 1
# We use glob to find the file without hardcoding the date in the name

# glob finds any file matching this pattern in the data/ folder
json_files = glob.glob("data/trends_*.json")

if not json_files:
    print("No JSON file found in data/ folder. Run Task 1 first.")
    exit()

# Pick the most recently modified file in case there are multiple
json_file = max(json_files, key=os.path.getmtime)

# Load JSON into a Pandas DataFrame
df = pd.read_json(json_file)

print(f"Loaded {len(df)} stories from {json_file}")

# STEP 2: Clean the data — fix all the issues one by one

# Remove duplicate rows based on post_id ---
# Same story might have been collected twice across category loops
df = df.drop_duplicates(subset="post_id")
print(f"\nAfter removing duplicates: {len(df)}")

# Drop rows where critical fields are missing ---
# A story without post_id, title, or score is useless for analysis
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")

# Fix data types ---
# score and num_comments must be integers, not floats
# (Pandas sometimes reads them as float64 when nulls were present)
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)

# --- 2d: Remove low quality stories ---
# Stories with score < 5 are not trending — remove them
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")

# --- 2e: Strip extra whitespace from title ---
# e.g. "  Hello World  " becomes "Hello World"
df["title"] = df["title"].str.strip()

# STEP 3: Save the cleaned DataFrame as a CSV file

# Make sure data/ folder exists (it should from Task 1, but just in case)
os.makedirs("data", exist_ok=True)

output_file = "data/trends_clean.csv"

# index=False means we don't write the row numbers (0,1,2...) into the CSV
df.to_csv(output_file, index=False)

print(f"\nSaved {len(df)} rows to {output_file}")

# --- Print stories per category so we can verify the spread ---
print("\nStories per category:")
category_counts = df["category"].value_counts()
for category, count in category_counts.items():
    print(f"  {category:<15} {count}")