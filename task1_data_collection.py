import requests
import time
import json
import os
from datetime import datetime

# Base URLs for HackerNews API
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Header as required
headers = {"User-Agent": "TrendPulse/1.0"}

# Keywords for each category
CATEGORIES = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

# Store collected stories
collected_stories = []

# Track how many per category
category_counts = {key: 0 for key in CATEGORIES.keys()}

# Get current timestamp
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Function to assign category based on title
def get_category(title):
    title = title.lower()
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in title:
                return category
    return None


# Step 1: Fetch top story IDs
try:
    response = requests.get(TOP_STORIES_URL, headers=headers)
    response.raise_for_status()
    story_ids = response.json()[:500]
except Exception as e:
    print(f"Error fetching top stories: {e}")
    story_ids = []

# Step 2: Loop category-wise
for category in CATEGORIES.keys():
    print(f"Collecting {category} stories...")

    for story_id in story_ids:
        # Stop if we already have 25 for this category
        if category_counts[category] >= 25:
            break

        try:
            res = requests.get(ITEM_URL.format(story_id), headers=headers)
            res.raise_for_status()
            story = res.json()

            # Skip if story is None or missing title
            if not story or "title" not in story:
                continue

            title = story["title"]
            assigned_category = get_category(title)

            # Only collect if category matches current loop
            if assigned_category == category:
                collected_stories.append({
                    "post_id": story.get("id"),
                    "title": title,
                    "category": assigned_category,
                    "score": story.get("score", 0),
                    "num_comments": story.get("descendants", 0),
                    "author": story.get("by", "unknown"),
                    "collected_at": current_time
                })

                category_counts[category] += 1

        except Exception as e:
            print(f"Failed to fetch story {story_id}: {e}")
            continue

    # Sleep AFTER each category loop (as required)
    time.sleep(2)

# Step 3: Save to JSON
if not os.path.exists("data"):
    os.makedirs("data")

filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

with open(filename, "w", encoding="utf-8") as f:
    json.dump(collected_stories, f, indent=4)

# Final output
print(f"Collected {len(collected_stories)} stories. Saved to {filename}")
