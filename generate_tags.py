import json
import openai
import time

# Initialize OpenAI API client
API_KEY = "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"

# Initialize OpenAI client
client = openai.Client(api_key=API_KEY)

# Function to generate tags using GPT-4
def generate_tags(word):
    prompt = 'I want to compare words from different categories to see which one could destroy / prevail over / conquer the other. Generate 10 tags for the word ' + word + ' such as "Energy Based", "Plant", "Building", "Fire Based", "Flammable", "Fragile", "Breakable", "Water Based", "Weather Phenomenon", "Abstract Concept", "Destructive", "Hard", "Soft" and other tags related to an objects durability, material, various resistances and destructive force. Do not include tags related to use, functionality or purpose. Only answer with the 10 tags, each on a new line.'
    
    # Call the Completion endpoint with GPT-4 model
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    
    # Extract the generated tags
    tags = response.choices[0].message.content.strip("- 0123456789.").split("\n")
    print(word + " - " + str(tags))
    return [tag.strip("- 0123456789.") for tag in tags if tag.strip("- 1203456789.")]

# Load the original JSON file
with open('training_set.json', 'r') as infile:
    data = json.load(infile)

# Prepare the new data with tags
new_data = {}

# Iterate over each entry in the JSON file and generate tags
for id, entry in data.items():
    word = entry['text']
    try:
        tags = generate_tags(word)
        new_data[id] = {"text": word, "tags": tags}
    except Exception as e:
        print(f"Error generating tags for word '{word}': {e}")
        new_data[id] = {"text": word, "tags": []}

    # Optional: sleep to avoid hitting rate limits for the API
    # time.sleep(1)

# Save the new data with tags in a new JSON file
with open('new_output_with_tags.json', 'w') as outfile:
    json.dump(new_data, outfile, indent=4)

print("Tags generated and saved successfully.")
