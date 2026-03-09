import pandas as pd
import os
import requests
from tqdm import tqdm
import time
import re

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

def extract_number(text):
    nums = re.findall(r'\d+', str(text))
    return int(nums[0]) if nums else None

# Vigesimal range only
vigesimal = df[df['is_vigesimal_std'] == True]

models = {
    "gpt-4o": "openai/gpt-4o",
    "claude-3.5-sonnet": "anthropic/claude-3.5-sonnet",
    "llama-3.1-70b": "meta-llama/llama-3.1-70b-instruct"
}

def get_mathification(number):
    if 70 <= number <= 79:
        return f"60 + {number - 60}"
    elif 80 <= number <= 99:
        return f"4 * 20 + {number - 80}"
    return None

results = []

for model_name, model_id in models.items():
    print(f"Testing model: {model_name}")
    for _, row in tqdm(vigesimal.iterrows(), total=len(vigesimal)):
        number = row['number']
        text = row['fr_standard']
        math_expr = get_mathification(number)
        
        # Test 1: Baseline
        prompt_base = f"Translate the following French number word to Arabic digits. Output only the digits: {text}"
        resp_base = call_openrouter(prompt_base, model_id)
        pred_base = extract_number(resp_base)
        
        # Test 2: Mathified
        prompt_math = f"The French number '{text}' literally means '{math_expr}'. What is its value in Arabic digits? Output only the digits."
        resp_math = call_openrouter(prompt_math, model_id)
        pred_math = extract_number(resp_math)
        
        results.append({
            "model": model_name,
            "number": number,
            "text": text,
            "math_expr": math_expr,
            "pred_base": pred_base,
            "correct_base": pred_base == number,
            "pred_math": pred_math,
            "correct_math": pred_math == number
        })

final_df = pd.DataFrame(results)
final_df.to_csv('results/mathification_results.csv', index=False)
print("Experiment 3 complete. Results saved to results/mathification_results.csv")
