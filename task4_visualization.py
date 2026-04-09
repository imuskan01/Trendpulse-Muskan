# task4_visualization.py
# TrendPulse - Task 4: Visualizations using Matplotlib
# Author: Muskan
# Date: April 2026

import pandas as pd               # for loading the CSV
import matplotlib.pyplot as plt   # for creating all charts
import os                         # for creating the outputs/ folder

# -------------------------------------------------------------------
# STEP 1: Load the analysed CSV from Task 3 and create outputs/ folder
# -------------------------------------------------------------------

# Load the CSV that was saved by Task 3
df = pd.read_csv("data/trends_analysed.csv")

print(f"Loaded {len(df)} stories for visualization.")

# Create outputs/ folder if it doesn't already exist
os.makedirs("outputs", exist_ok=True)


# -------------------------------------------------------------------
# CHART 1: Top 10 Stories by Score — Horizontal Bar Chart
# -------------------------------------------------------------------

# Sort by score descending and take top 10 rows
top10 = df.sort_values("score", ascending=False).head(10)

# Make a copy to avoid pandas warning when adding a new column
top10 = top10.copy()

# Shorten titles longer than 50 characters so they fit on the y-axis
top10["short_title"] = top10["title"].apply(
    lambda t: t[:50] + "..." if len(t) > 50 else t
)

# Create the figure and axes
fig1, ax1 = plt.subplots(figsize=(12, 6))

# barh = horizontal bar chart
# [::-1] reverses order so highest score appears at the TOP
ax1.barh(top10["short_title"][::-1], top10["score"][::-1], color="steelblue")

ax1.set_title("Top 10 Stories by Score", fontsize=14)
ax1.set_xlabel("Score")
ax1.set_ylabel("Story Title")

# tight_layout prevents labels from being cut off
plt.tight_layout()

# Save BEFORE show — required by the task
plt.savefig("outputs/chart1_top_stories.png")
plt.close()   # close figure to free memory

print("Saved: outputs/chart1_top_stories.png")


# -------------------------------------------------------------------
# CHART 2: Stories per Category — Bar Chart with different colours
# -------------------------------------------------------------------

# Count how many stories are in each category
category_counts = df["category"].value_counts()

# One different colour per bar
colours = ["steelblue", "tomato", "mediumseagreen", "mediumpurple", "sandybrown"]

fig2, ax2 = plt.subplots(figsize=(9, 5))

ax2.bar(category_counts.index, category_counts.values, color=colours)

ax2.set_title("Stories per Category", fontsize=14)
ax2.set_xlabel("Category")
ax2.set_ylabel("Number of Stories")

plt.tight_layout()

plt.savefig("outputs/chart2_categories.png")
plt.close()

print("Saved: outputs/chart2_categories.png")


# -------------------------------------------------------------------
# CHART 3: Score vs Comments — Scatter Plot
# Popular stories get a different colour using the is_popular column
# -------------------------------------------------------------------

# Split into two groups based on is_popular column
popular     = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

fig3, ax3 = plt.subplots(figsize=(9, 5))

# Plot not_popular first so popular dots appear on top
ax3.scatter(not_popular["score"], not_popular["num_comments"],
            color="steelblue", alpha=0.6, label="Not Popular")

ax3.scatter(popular["score"], popular["num_comments"],
            color="tomato", alpha=0.8, label="Popular")

ax3.set_title("Score vs Number of Comments", fontsize=14)
ax3.set_xlabel("Score")
ax3.set_ylabel("Number of Comments")
ax3.legend()   # shows the colour key for popular vs not popular

plt.tight_layout()

plt.savefig("outputs/chart3_scatter.png")
plt.close()

print("Saved: outputs/chart3_scatter.png")


# -------------------------------------------------------------------
# BONUS — Dashboard: All 3 charts combined into one single figure
# plt.subplots(1, 3) creates 1 row with 3 panels side by side
# -------------------------------------------------------------------

fig, axes = plt.subplots(1, 3, figsize=(22, 6))

# Overall title for the entire dashboard figure
fig.suptitle("TrendPulse Dashboard", fontsize=16, fontweight="bold")

# --- Panel 1: Top 10 Stories by Score ---
axes[0].barh(top10["short_title"][::-1], top10["score"][::-1], color="steelblue")
axes[0].set_title("Top 10 Stories by Score")
axes[0].set_xlabel("Score")
axes[0].set_ylabel("Story Title")
axes[0].tick_params(axis="y", labelsize=7)   # smaller font so titles fit

# --- Panel 2: Stories per Category ---
axes[1].bar(category_counts.index, category_counts.values, color=colours)
axes[1].set_title("Stories per Category")
axes[1].set_xlabel("Category")
axes[1].set_ylabel("Number of Stories")

# --- Panel 3: Score vs Comments Scatter ---
axes[2].scatter(not_popular["score"], not_popular["num_comments"],
                color="steelblue", alpha=0.6, label="Not Popular")
axes[2].scatter(popular["score"], popular["num_comments"],
                color="tomato", alpha=0.8, label="Popular")
axes[2].set_title("Score vs Comments")
axes[2].set_xlabel("Score")
axes[2].set_ylabel("Number of Comments")
axes[2].legend()

plt.tight_layout()

plt.savefig("outputs/dashboard.png")
plt.close()

print("Saved: outputs/dashboard.png")

print("\nAll charts saved successfully in outputs/ folder!")