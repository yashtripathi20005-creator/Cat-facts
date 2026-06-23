"""
Cat Facts / Dog Facts Display
A Flask web application that displays random cat and dog facts.
"""

from flask import Flask, render_template, request, jsonify
import requests
import random
import json
import os

app = Flask(__name__)

# List of cat facts (fallback if API fails)
CAT_FACTS_FALLBACK = [
    "Cats sleep for approximately 70% of their lives.",
    "A group of cats is called a clowder.",
    "Cats have 32 muscles in each ear.",
    "The average cat can jump up to 6 times its length.",
    "Cats have 230 bones in their bodies.",
    "A cat's nose pad is unique, like a human fingerprint.",
    "Cats can make over 100 different sounds.",
    "The oldest known pet cat existed 9,500 years ago.",
    "Cats spend 30-50% of their day grooming themselves.",
    "A cat's heart beats twice as fast as a human heart.",
    "Cats have whiskers on the backs of their front legs.",
    "The world's largest cat measured 48.5 inches long.",
    "Cats can rotate their ears 180 degrees.",
    "A cat's purr vibrates at a frequency of 25-150 Hz.",
    "Cats use their tails for balance and communication."
]

# List of dog facts (fallback if API fails)
DOG_FACTS_FALLBACK = [
    "Dogs have about 1,700 taste buds, compared to 9,000 in humans.",
    "A dog's nose is 10,000 to 100,000 times more sensitive than a human's.",
    "The average dog can learn about 165 words.",
    "Dogs have 42 teeth in their mouths.",
    "A dog's sense of smell is at least 40 times better than humans.",
    "The world's oldest dog lived to be 29 years old.",
    "Dogs dream just like humans do.",
    "A dog's heart beats 60 to 140 times per minute.",
    "Dogs are about as intelligent as a 2-year-old human child.",
    "The Basenji dog breed doesn't bark; it yodels.",
    "Dogs have three eyelids.",
    "Dogs can see in the dark better than humans.",
    "The average dog runs about 19 miles per hour.",
    "Dogs' noses can detect thermal radiation.",
    "Dogs have 319 bones in their bodies (varies by breed)."
]

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/get_cat_fact')
def get_cat_fact():
    """Fetch a random cat fact from the Cat Facts API or use fallback."""
    try:
        response = requests.get('https://catfact.ninja/fact', timeout=5)
        if response.status_code == 200:
            data = response.json()
            return jsonify({'fact': data.get('fact', random.choice(CAT_FACTS_FALLBACK))})
        else:
            return jsonify({'fact': random.choice(CAT_FACTS_FALLBACK)})
    except (requests.RequestException, json.JSONDecodeError) as e:
        print(f"Error fetching cat fact: {e}")
        return jsonify({'fact': random.choice(CAT_FACTS_FALLBACK)})

@app.route('/get_dog_fact')
def get_dog_fact():
    """Fetch a random dog fact from the Dog Facts API or use fallback."""
    try:
        response = requests.get('https://dog-api.kinduff.com/api/facts', timeout=5)
        if response.status_code == 200:
            data = response.json()
            facts = data.get('facts', [])
            if facts and len(facts) > 0:
                return jsonify({'fact': facts[0]})
            else:
                return jsonify({'fact': random.choice(DOG_FACTS_FALLBACK)})
        else:
            return jsonify({'fact': random.choice(DOG_FACTS_FALLBACK)})
    except (requests.RequestException, json.JSONDecodeError) as e:
        print(f"Error fetching dog fact: {e}")
        return jsonify({'fact': random.choice(DOG_FACTS_FALLBACK)})

@app.route('/get_both_facts')
def get_both_facts():
    """Fetch both cat and dog facts simultaneously."""
    import concurrent.futures
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        cat_future = executor.submit(get_cat_fact)
        dog_future = executor.submit(get_dog_fact)
        
        # Wait for both to complete
        cat_response = cat_future.result()
        dog_response = dog_future.result()
        
        # Extract facts from JSON responses
        cat_fact = cat_response.get_json().get('fact', 'Unable to fetch cat fact')
        dog_fact = dog_response.get_json().get('fact', 'Unable to fetch dog fact')
        
        return jsonify({
            'cat_fact': cat_fact,
            'dog_fact': dog_fact
        })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
