import pandas as pd
import os
import requests
from tqdm import tqdm
import time
import random

# Load dataset
df = pd.read_csv('datasets/french_numbers_1_1000.csv')
OPENROUTER_KEY = os.getenv('OPENROUTER_KEY')

def call_openrouter(prompt, model):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0
    }
    for _ in range(3):
        try:
            response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
        except:
            pass
        time.sleep(1)
    return None

# Focus on 70-99 range
vigesimal_range = df[(df['number'] >= 70) & (df['number'] <= 99)]

models = {
    "gpt-4o": "openai/gpt-4o",
    "claude-3.5-sonnet": "anthropic/claude-3.5-sonnet",
    "llama-3.1-70b": "meta-llama/llama-3.1-70b-instruct"
}

results = []

# Generate comparison pairs
pairs = []
for _ in range(50):
    n1 = random.randint(70, 99)
    n2 = random.randint(70, 99)
    while n1 == n2:
        n2 = random.randint(70, 99)
    pairs.append((n1, n2))

for model_name, model_id in models.items():
    print(f"Testing model: {model_name}")
    for n1, n2 in tqdm(pairs):
        row1 = df[df['number'] == n1].iloc[0]
        row2 = df[df['number'] == n2].iloc[0]
        
        # Test 1: Standard vs Standard
        prompt_std = f"Which number is larger? Answer only with 'First' or 'Second'.\nFirst: {row1['fr_standard']}\nSecond: {row2['fr_standard']}"
        resp_std = call_openrouter(prompt_std, model_id)
        correct_std = (n1 > n2 and "First" in str(resp_std)) or (n2 > n1 and "Second" in str(resp_std))
        
        # Test 2: Swiss vs Swiss
        prompt_swiss = f"Which number is larger? Answer only with 'First' or 'Second'.\nFirst: {row1['fr_swiss']}\nSecond: {row2['fr_swiss']}"
        resp_swiss = call_openrouter(prompt_swiss, model_id)
        correct_swiss = (n1 > n2 and "First" in str(resp_swiss)) or (n2 > n1 and "Second" in str(resp_swiss))

        # Test 3: Mixed (Standard vs Swiss)
        prompt_mixed = f"Which number is larger? Answer only with 'First' or 'Second'.\nFirst: {row1['fr_standard']}\nSecond: {row2['fr_swiss']}"
        resp_mixed = call_openrouter(prompt_mixed, model_id)
        correct_mixed = (n1 > n2 and "First" in str(resp_mixed)) or (n2 > n1 and "Second" in str(resp_mixed))

        results.append({
            "model": model_name,
            "n1": n1,
            "n2": n2,
            "correct_std": correct_std,
            "correct_swiss": correct_swiss,
            "correct_mixed": correct_mixed
        })

final_df = pd.DataFrame(results)
final_df.to_csv('results/magnitude_comparison_results.csv', index=False)
print("Experiment 2 complete. Results saved to results/magnitude_comparison_results.csv")
