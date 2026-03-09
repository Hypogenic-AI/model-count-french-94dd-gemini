import pandas as pd
import os
import json
import requests
from tqdm import tqdm
import time

# Create directories
os.makedirs('results/responses', exist_ok=True)

# Load dataset
df = pd.read_csv('datasets/french_numbers_1_1000.csv')

# Configure API
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
    
    for _ in range(3): # Retry logic
        try:
            response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            else:
                print(f"Error {response.status_code}: {response.text}")
        except Exception as e:
            print(f"Request failed: {e}")
        time.sleep(1)
    return None

def extract_number(response_text):
    # Simple extraction: look for digits in the response
    import re
    nums = re.findall(r'\d+', str(response_text))
    if nums:
        return int(nums[0])
    return None

# Sample data: All 70-99 (vigesimal range) + 30 random non-vigesimal for comparison
vigesimal_range = df[df['is_vigesimal_std'] == True]
decimal_range = df[df['is_vigesimal_std'] == False].sample(n=30, random_state=42)
test_set = pd.concat([vigesimal_range, decimal_range])

models = {
    "gpt-4o": "openai/gpt-4o",
    "claude-3.5-sonnet": "anthropic/claude-3.5-sonnet",
    "llama-3.1-70b": "meta-llama/llama-3.1-70b-instruct"
}

results = []

for model_name, model_id in models.items():
    print(f"Testing model: {model_name}")
    for _, row in tqdm(test_set.iterrows(), total=len(test_set)):
        number = row['number']
        
        # Test Standard French (Vigesimal for 70-99)
        prompt_std = f"Translate the following French number word to Arabic digits. Output only the digits: {row['fr_standard']}"
        resp_std = call_openrouter(prompt_std, model_id)
        pred_std = extract_number(resp_std)
        
        # Test Swiss French (Decimal)
        prompt_swiss = f"Translate the following French number word to Arabic digits. Output only the digits: {row['fr_swiss']}"
        resp_swiss = call_openrouter(prompt_swiss, model_id)
        pred_swiss = extract_number(resp_swiss)
        
        results.append({
            "model": model_name,
            "number": number,
            "system": "standard",
            "text": row['fr_standard'],
            "prediction": pred_std,
            "is_correct": pred_std == number,
            "is_vigesimal": row['is_vigesimal_std']
        })
        
        results.append({
            "model": model_name,
            "number": number,
            "system": "swiss",
            "text": row['fr_swiss'],
            "prediction": pred_swiss,
            "is_correct": pred_swiss == number,
            "is_vigesimal": row['is_vigesimal_std']
        })
    
    # Save intermediate results
    temp_df = pd.DataFrame(results)
    temp_df.to_csv(f'results/decoding_results_partial_{model_name}.csv', index=False)

final_df = pd.DataFrame(results)
final_df.to_csv('results/decoding_results_final.csv', index=False)
print("Experiment 1 complete. Results saved to results/decoding_results_final.csv")
