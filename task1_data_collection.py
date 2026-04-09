# task1_data_collection.py
# TrendPulse - Task 1: Fetch trending stories from HackerNews API
# Author: Muskan
# Date: April 2026

import requests
import json
import time
import os
from datetime import datetime

# Categories and keywords for matching story titles
# HackerNews is tech-heavy so sports/entertainment use a fallback strategy
CATEGORIES = {
    "technology":    ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm", "python", "model", "developer", "open source"],
    "worldnews":     ["war", "government", "country", "president", "election", "climate", "attack", "global", "policy", "military", "russia", "china"],
    "sports":        ["nfl", "nba", "fifa", "sport", "team", "player", "league", "championship", "olympic", "cricket", "tennis", "tournament", "athlete"],
    "science":       ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome", "quantum", "brain", "cancer", "experiment"],
    "entertainment": ["movie", "film", "music", "netflix", "book", "show", "award", "streaming", "spotify", "youtube", "album", "podcast", "gaming"],
}

HEADERS = {"User-Agent": "TrendPulse/1.0"}
MAX_PER_CATEGORY = 25


def assign_category(title):
    # Lowercase the title once so keyword matching is case-insensitive
    title_lower = title.lower()
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in title_lower:
                return category
    return "unmatched"   # no keyword matched


def fetch_top_story_ids():
    # Fetch top 1000 story IDs from HackerNews
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        all_ids = response.json()
        return all_ids[:1000]
    except requests.RequestException as e:
        print(f"Failed to fetch story IDs: {e}")
        return []


def fetch_story(story_id):
    # Fetch details of one story — return None if anything fails
    url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Failed to fetch story {story_id}: {e}")
        return None


def build_record(story, category):
    # Build the 7-field record required by the task
    return {
        "post_id":      story.get("id"),
        "title":        story.get("title", ""),
        "category":     category,
        "score":        story.get("score", 0),
        "num_comments": story.get("descendants", 0),  # HN calls comments 'descendants'
        "author":       story.get("by", "unknown"),
        "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def collect_stories(story_ids):
    collected = {category: [] for category in CATEGORIES}

    # seen_ids prevents the same story appearing in multiple categories
    seen_ids = set()

    for category in CATEGORIES:
        print(f"\n  Collecting stories for: [{category}]")

        for story_id in story_ids:

            # Stop once this category has 25 stories
            if len(collected[category]) >= MAX_PER_CATEGORY:
                break

            print(f"    Checking story ID: {story_id}...")
            story = fetch_story(story_id)

            # Skip failed fetches or items with no title (jobs, polls etc.)
            if not story or "title" not in story:
                continue

            # THIS IS THE KEY FIX — skip stories already saved in another category
            if story.get("id") in seen_ids:
                continue

            title = story.get("title", "")
            assigned = assign_category(title)

            if assigned == category:
                # Keyword matched — accept and mark as seen
                collected[category].append(build_record(story, category))
                seen_ids.add(story.get("id"))

            elif assigned == "unmatched" and len(collected[category]) < 20:
                # Fallback for categories rare on HackerNews (sports/entertainment)
                collected[category].append(build_record(story, category))
                seen_ids.add(story.get("id"))

        print(f"  Finished [{category}]: {len(collected[category])} stories")
        time.sleep(2)   # wait 2 seconds between categories as required

    return collected


def save_to_json(collected):
    # Flatten all category lists into one list
    all_stories = []
    for stories in collected.values():
        all_stories.extend(stories)

    os.makedirs("data", exist_ok=True)

    today = datetime.now().strftime("%Y%m%d")
    filename = f"data/trends_{today}.json"

    with open(filename, "w") as f:
        json.dump(all_stories, f, indent=2)

    print(f"\nCollected {len(all_stories)} stories. Saved to {filename}")

    print("\nBreakdown by category:")
    for category, stories in collected.items():
        print(f"  {category}: {len(stories)} stories")


if __name__ == "__main__":
    print("Fetching top story IDs from HackerNews...")
    story_ids = fetch_top_story_ids()

    if not story_ids:
        print("No story IDs fetched. Exiting.")
    else:
        print(f"Got {len(story_ids)} story IDs. Starting collection...")
        collected = collect_stories(story_ids)
        save_to_json(collected)