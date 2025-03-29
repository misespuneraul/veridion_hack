import requests
from time import sleep
import random
import openai

API_KEY = ''

host = "http://172.18.4.158:8000"
post_url = f"{host}/submit-word"
get_url = f"{host}/get-word"
status_url = f"{host}/status"

NUM_ROUNDS = 5

def play_game(player_id="Ga95z0WhLD"):

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

        data = {"player_id": player_id, "word_id": "21", "round_id": round_id}
        response = requests.post(post_url, json=data)
        print(response.json())