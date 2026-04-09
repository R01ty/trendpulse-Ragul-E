import pandas as pd
import numpy as np
import os

# -----------------------------
# Step 0 — File paths
# -----------------------------
input_csv = "data/trends_clean.csv"        # from Task 2
output_csv = "data/trends_analysed.csv"   # new CSV for Task 4

# -----------------------------
# Step 1 — Load and explore data
# -----------------------------
df = pd.read_csv(input_csv)

print(f"Loaded data: {df.shape}\n")
print("First 5 rows:")
print(df.head())

# Average score and comments
avg_score = df['score'].mean()
avg_comments = df['num_comments'].mean()
print(f"\nAverage score   : {avg_score:.0f}")
print(f"Average comments: {avg_comments:.0f}")

# -----------------------------
# Step 2 — NumPy statistics
# -----------------------------
scores = df['score'].to_numpy()

mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)
max_score = np.max(scores)
min_score = np.min(scores)

print("\n--- NumPy Stats ---")
print(f"Mean score   : {mean_score:.0f}")
print(f"Median score : {median_score:.0f}")
print(f"Std deviation: {std_score:.0f}")
print(f"Max score    : {max_score}")
print(f"Min score    : {min_score}")

# Category with most stories
most_stories_cat = df['category'].value_counts().idxmax()
most_stories_count = df['category'].value_counts().max()
print(f"\nMost stories in: {most_stories_cat} ({most_stories_count} stories)")

# Story with most comments
max_comments_idx = df['num_comments'].idxmax()
max_comments_story = df.loc[max_comments_idx, 'title']
max_comments_count = df.loc[max_comments_idx, 'num_comments']
print(f"\nMost commented story: \"{max_comments_story}\"  — {max_comments_count} comments")

# -----------------------------
# Step 3 — Add new columns
# -----------------------------
# Engagement = num_comments / (score + 1) to avoid divide by zero
df['engagement'] = df['num_comments'] / (df['score'] + 1)

# is_popular = True if score > average score
df['is_popular'] = df['score'] > avg_score

# -----------------------------
# Step 4 — Save updated CSV
# -----------------------------
os.makedirs("data", exist_ok=True)
df.to_csv(output_csv, index=False)
print(f"\nSaved to {output_csv}")
