import json
import openai

API_KEY = ''
# Initialize OpenAI client
client = openai.Client(api_key=API_KEY)

def compare_words(word1, word2):
    print(word1, word2)
    """Ask GPT-4o which word is semantically stronger."""
    prompt = f"In terms of meaning and real-world impact, which word could beat, prevail, or conquer over the other: '{word1}' or '{word2}'? Answer only with the stronger word."
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()

def generate_training_data(json_file="words.json", output_file="training_data.jsonl"):
    """Generate training data for fine-tuning GPT-4."""
    
    # Load words from JSON file
    with open(json_file, "r") as file:
        words_data = json.load(file)
    
    words_list = [{"id": key, "text": value["text"], "cost": value["cost"]} for key, value in words_data.items()]
    
    training_examples = []

    for target_word in [entry["text"] for entry in words_list]:
        print(f"Target word: {target_word}")
        stronger_words = [entry for entry in words_list if compare_words(entry["text"], target_word) == entry["text"]]

        if stronger_words:
            best_choice = min(stronger_words, key=lambda x: x["cost"])  # Find the cheapest strong word
            training_examples.append({
                "messages": [
                    {"role": "system", "content": "Select the cheapest word that is guaranteed to be stronger than the target."},
                    {"role": "user", "content": f"Target: {target_word} | Candidates: {json.dumps(words_data)}"},
                    {"role": "assistant", "content": best_choice["text"]}
                ]
            })

    # Save as JSONL
    with open(output_file, "w") as file:
        for example in training_examples:
            file.write(json.dumps(example) + "\n")
    
    print(f"Training data saved to {output_file}")

# Run the script
generate_training_data()
