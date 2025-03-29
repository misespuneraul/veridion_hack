import json
import random
import time
import openai

API_KEY = ''

# Initialize OpenAI client
client = openai.Client(api_key=API_KEY)

# Load words and training set
with open("words.json", "r") as words_file:
    words_data = json.load(words_file)  # Expecting a dictionary with keys as IDs

with open("training_set.json", "r") as training_file:
    training_data = json.load(training_file)  # Expecting a dictionary with keys as IDs

# Convert words.json into a list of dictionaries for processing
words_list = [{"id": key, "text": value["text"], "cost": value["cost"]} for key, value in words_data.items()]

def compare_words(word1, word2):
    """Simulate a comparison function that determines which word is stronger."""
    prompt = (f"What word could logically beat the other? \n"
              f"'{word1}' or '{word2}'? Answer only with the stronger word.")
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content.strip()

def find_best_counter(target_word):
    """Find the cheapest word in words.json that beats the target word."""
    for entry in sorted(words_list, key=lambda x: x["cost"]):  # Sort by cost for efficiency
        if compare_words(entry["text"], target_word) == entry["text"]:
            print(target_word + " - " + entry["id"])
            return entry["id"]  # Return immediately on first valid match

    


# Prepare results dictionary
results = {}

# Iterate through training_set.json and find best counters
for train_id, train_entry in training_data.items():
    target_word = train_entry["text"]
    best_word_id = find_best_counter(target_word)
    results[train_id] = {"text": target_word, "best_counter_id": best_word_id}
    time.sleep(0.1)  # Simulate API delay

# Save results to a JSON file
with open("best_counters.json", "w") as outfile:
    json.dump(results, outfile, indent=4)

print("Comparison complete. Results saved to best_counters.json.")
