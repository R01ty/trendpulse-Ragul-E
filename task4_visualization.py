import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# -----------------------------
# Step 0 — Load analysed CSV
# -----------------------------
input_csv = "data/trends_analysed.csv"
df = pd.read_csv(input_csv)

# -----------------------------
# Step 1 — Create output folder
# -----------------------------
os.makedirs("data/plots", exist_ok=True)

# -----------------------------
# Step 2 — Stories per category (bar chart)
# -----------------------------
plt.figure(figsize=(8,5))
sns.countplot(data=df, x='category', order=df['category'].value_counts().index, palette='viridis')
plt.title("Number of Stories per Category")
plt.xlabel("Category")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("data/plots/stories_per_category.png")
plt.close()

# -----------------------------
# Step 3 — Score distribution (histogram)
# -----------------------------
plt.figure(figsize=(8,5))
sns.histplot(df['score'], bins=20, kde=True, color='skyblue')
plt.title("Distribution of Scores")
plt.xlabel("Score")
plt.ylabel("Number of Stories")
plt.tight_layout()
plt.savefig("data/plots/score_distribution.png")
plt.close()

# -----------------------------
# Step 4 — Engagement distribution (histogram)
# -----------------------------
plt.figure(figsize=(8,5))
sns.histplot(df['engagement'], bins=20, kde=True, color='orange')
plt.title("Distribution of Engagement")
plt.xlabel("Engagement (num_comments / (score+1))")
plt.ylabel("Number of Stories")
plt.tight_layout()
plt.savefig("data/plots/engagement_distribution.png")
plt.close()

# -----------------------------
# Step 5 — Popular vs Non-popular stories (bar chart)
# -----------------------------
plt.figure(figsize=(6,4))
sns.countplot(data=df, x='is_popular', palette='coolwarm')
plt.title("Popular vs Non-popular Stories")
plt.xlabel("Is Popular")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("data/plots/popular_stories.png")
plt.close()

# -----------------------------
# Step 6 — Confirmation message
# -----------------------------
print("Plots saved to data/plots folder:")
print("- stories_per_category.png")
print("- score_distribution.png")
print("- engagement_distribution.png")
print("- popular_stories.png")
