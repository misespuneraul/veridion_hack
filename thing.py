import requests
from time import sleep
import random
import openai

API_KEY = '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'



def compare_words(word1, word2):
    """Ask GPT-4o which word is semantically stronger."""
    prompt = (f"In terms of meaning and real-world impact, which word could beat, prevail, or conquer over the other: \n"
              f"'{word1}' or '{word2}'? Answer only with the stronger word.")
    
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        api_key=API_KEY
    )
    
    return response["choices"][0]["message"]["content"].strip()

def what_beats(target_word, json_file="words.json"):
    """Find the least expensive word that GPT-4o considers stronger than the target_word."""
    
    # Load words from JSON file
    with open(json_file, "r") as file:
        words_data = json.load(file)  # Expecting a dictionary with keys as IDs and values as word data
    
    # Convert to list of dictionaries for processing
    words_list = [{"id": key, "text": value["text"], "cost": value["cost"]} for key, value in words_data.items()]
    
    # Filter words that GPT-4o considers stronger
    stronger_words = [entry for entry in words_list if compare_words(entry["text"], target_word) == entry["text"]]
    
    # Find the least expensive among the stronger words
    if stronger_words:
        best_choice = min(stronger_words, key=lambda x: x["cost"])
        return best_choice["id"]  # Return the ID of the most inexpensive strong word
    
    return None  # Return None if no stronger word is found

# # Example usage
# word_list = ["wood", "water", "rock", "storm", "wind"]
# target = "fire"

# stronger_words = find_stronger_words(target, word_list)
# print(f"Words stronger than '{target}': {stronger_words}")

host = ""
post_url = f"{host}/submit-word"
get_url = f"{host}/get-word"
status_url = f"{host}/status"

NUM_ROUNDS = 5

def play_game(player_id):

    for round_id in range(1, NUM_ROUNDS+1):
        round_num = -1
        while round_num != round_id:
            response = requests.get(get_url)
            print(response.json())
            sys_word = response.json()['word']
            round_num = response.json()['round']

            sleep(1)

        if round_id > 1:
            status = requests.get(status_url)
            print(status.json())

        choosen_word = what_beats(sys_word)
        data = {"player_id": player_id, "word_id": 5, "round_id": round_id}
        response = requests.post(post_url, json=data)
        print(response.json())