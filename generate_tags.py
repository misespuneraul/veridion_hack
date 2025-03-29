import json
import openai
import time

# Initialize OpenAI API client
openai.api_key = "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"
  # Replace with your actual API key

# Function to generate tags using GPT-4o
def generate_tags(word):
    prompt = f"Generate 10 relevant tags for the word '{word}' that are related to its meaning and context."
    
    # Call the ChatCompletion endpoint with GPT-4o model
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Specify GPT-4 model
        messages=[{"role": "user", "content": prompt}]
    )
    
    # Extract the generated tags
    tags = response['choices'][0]['message']['content'].strip().split("\n")
    return [tag.strip() for tag in tags if tag.strip()]

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
    time.sleep(1)

# Save the new data with tags in a new JSON file
with open('output_with_tags.json', 'w') as outfile:
    json.dump(new_data, outfile, indent=4)

print("Tags generated and saved successfully.")
