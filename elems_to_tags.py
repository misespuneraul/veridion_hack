import json

# Load the original JSON file (with words and their tags)
with open('output_with_tags.json', 'r') as infile:
    data = json.load(infile)

# Initialize a dictionary to track tag counts
tag_counts = {}

# Iterate over each entry in the original JSON to gather tags
for entry in data.values():
    for tag in entry['tags']:
        if tag not in tag_counts:
            tag_counts[tag] = 0
        tag_counts[tag] += 1

# Create a new dictionary with unique tag IDs and their counts
tag_info = {}
for idx, (tag, count) in enumerate(tag_counts.items(), start=1):
    tag_info[idx] = {"tag": tag, "count": count}

# Save the result to a new JSON file
with open('tag_info.json', 'w') as outfile:
    json.dump(tag_info, outfile, indent=4)

print("Tag info saved to 'tag_info.json'.")
