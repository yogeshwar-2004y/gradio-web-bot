import re
import random_responses
import gradio
import json
import os

# Load JSON data
def load_json(file):
    with open(file) as bot_responses:
        print(f"Loaded '{file}' successfully!")
        return json.load(bot_responses)


# Store JSON data
response_data = load_json("bot.json")

invalid_inputs=" "
def load_invalid_inputs():
    if os.path.exists("invalid_inputs.json"):
        with open("invalid_inputs.json", "r") as file:
            return json.load(file)
    else:
        return {}

def save_invalid_inputs(invalid_inputs):
    with open("invalid_inputs.json", "w") as file:
        json.dump(invalid_inputs, file)

def history_inputs():
    if os.path.exists("history_input.json"):
        with open("history_input.json", "r") as file:
            return json.load(file)
    else:
        return {}     
bo_response=" "     
def history(bo_response):
    with open("history_input.json","w") as file:
        json.dump(bo_response,file)

def get_response(input_string):
    split_message = re.split(r'\s+|[,;?!.-]\s*', input_string.lower())
    score_list = []

    # Check all the responses
    for response in response_data:
        response_score = 0
        required_score = 0
        required_words = response["required_words"]

        # Check if there are any required words
        if required_words:
            for word in split_message:
                if word in required_words:
                    required_score += 1

        # Amount of required words should match the required score
        if required_score == len(required_words):
            # print(required_score == len(required_words))
            # Check each word the user has typed
            for word in split_message:
                # If the word is in the response, add to the score
                if word in response["user_input"]:
                    response_score += 1

        # Add score to list
        score_list.append(response_score)
        # Debugging: Find the best phrase
        # print(response_score, response["user_input"])

    # Find the best response and return it if they're not all 0
    best_response = max(score_list)
    response_index = score_list.index(best_response)

    # Check if input is empty
    if input_string == "":
        return "Please type something so we can chat :("
    # If there is no good response, return a random one.
    if best_response != 0:
        bo_response=history_inputs()
        result=response_data[response_index]["bot_response"]
        bo_response[input_string]=result
        history(bo_response)
        return result

    else:
        invalid_inputs = load_invalid_inputs()
        if input_string in invalid_inputs:
            res = invalid_inputs[input_string]
        else:
            res = random_responses.random_string()
            invalid_inputs[input_string] = res
            save_invalid_inputs(invalid_inputs)
        return res
    
ADMIN =input("ADMIN: ")
if(ADMIN == "velan"):
    print("SUCESSFULLY UNLOCKED")
    print("BOT IS INITIATED - START WITH AN DEMO")
    print("----------------------")
    user_input = input("You: ")
    print("Bot:", get_response(user_input))
    demo = gradio.Interface(fn=get_response, inputs = "text", outputs = "text", title = "yogi the bot")
    demo.launch

    demo.launch(share=True)
else:
    print("ASK ADMIN TO UNLOCK WITH CORRECT KEY")    
