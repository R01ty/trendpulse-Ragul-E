import json
import csv
import os

# Input JSON file (update name if needed)
input_file = "data/trends_20260409.json"

# Output CSV file
output_file = "data/cleaned_trends.csv"

# Load JSON data
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

cleaned_data = []
seen_titles = set()

for item in data:
    # Skip if any important field is missing
    if not all([
        item.get("post_id"),
        item.get("title"),
        item.get("category"),
        item.get("score") is not None,
        item.get("num_comments") is not None,
        item.get("author"),
        item.get("collected_at")
    ]):
        continue

    # Remove duplicate titles
    title = item["title"].strip()
    if title in seen_titles:
        continue
    seen_titles.add(title)

    # Ensure correct types
    try:
        item["score"] = int(item["score"])
        item["num_comments"] = int(item["num_comments"])
    except:
        continue

    cleaned_data.append(item)

# Ensure data folder exists
os.makedirs("data", exist_ok=True)

# Write to CSV
with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "post_id",
        "title",
        "category",
        "score",
        "num_comments",
        "author",
        "collected_at"
    ])
    
    writer.writeheader()
    writer.writerows(cleaned_data)

print(f"Cleaned {len(cleaned_data)} records and saved to {output_file}")
