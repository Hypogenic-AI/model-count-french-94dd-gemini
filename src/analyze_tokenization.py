import pandas as pd
import tiktoken
from transformers import AutoTokenizer
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create directories
os.makedirs('results', exist_ok=True)
os.makedirs('figures', exist_ok=True)

# Load dataset
df = pd.read_csv('datasets/french_numbers_1_1000.csv')

# Define tokenizers
tokenizers = {
    'gpt-4o (o200k_base)': tiktoken.get_encoding("o200k_base"),
    'gpt-4/3.5 (cl100k_base)': tiktoken.get_encoding("cl100k_base"),
    'gpt-3 (p50k_base)': tiktoken.get_encoding("p50k_base"),
}

# Add open-source tokenizers (fallback to gpt2 if others fail)
try:
    tokenizers['llama-3'] = AutoTokenizer.from_pretrained("hf-internal-testing/llama-tokenizer", trust_remote_code=True)
except Exception as e:
    print(f"Llama-3 tokenizer fail: {e}")

try:
    tokenizers['mistral'] = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1", trust_remote_code=True)
except Exception as e:
    print(f"Mistral tokenizer fail: {e}")

def count_tokens(text, enc_name, enc):
    if 'gpt' in enc_name:
        return len(enc.encode(text))
    else:
        return len(enc.encode(text, add_special_tokens=False))

# Calculate token counts for each system
for name, enc in tokenizers.items():
    df[f'tokens_std_{name}'] = df['fr_standard'].apply(lambda x: count_tokens(x, name, enc))
    df[f'tokens_swiss_{name}'] = df['fr_swiss'].apply(lambda x: count_tokens(x, name, enc))
    df[f'token_diff_{name}'] = df[f'tokens_std_{name}'] - df[f'tokens_swiss_{name}']

# Save detailed results
df.to_csv('results/tokenization_analysis.csv', index=False)

# Analyze the 70-99 range specifically
range_70_99 = df[(df['number'] >= 70) & (df['number'] <= 99)]

print("Token count analysis for 70-99 range (Standard vs Swiss French):")
results_summary = []
for name in tokenizers.keys():
    avg_std = range_70_99[f'tokens_std_{name}'].mean()
    avg_swiss = range_70_99[f'tokens_swiss_{name}'].mean()
    diff = avg_std - avg_swiss
    print(f"Tokenizer: {name}")
    print(f"  Avg Tokens (Standard): {avg_std:.2f}")
    print(f"  Avg Tokens (Swiss):    {avg_swiss:.2f}")
    print(f"  Difference:            {diff:.2f}")
    results_summary.append({
        'tokenizer': name,
        'avg_std': avg_std,
        'avg_swiss': avg_swiss,
        'diff': diff
    })

# Plotting
plt.figure(figsize=(12, 6))
plot_df = pd.DataFrame(results_summary)
plot_df_melted = plot_df.melt(id_vars='tokenizer', value_vars=['avg_std', 'avg_swiss'], 
                             var_name='system', value_name='avg_tokens')
plot_df_melted['system'] = plot_df_melted['system'].replace({'avg_std': 'Standard (Vigesimal)', 'avg_swiss': 'Swiss (Decimal)'})

sns.barplot(data=plot_df_melted, x='tokenizer', y='avg_tokens', hue='system')
plt.title('Average Token Count for Numbers 70-99')
plt.ylabel('Average Number of Tokens')
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig('figures/tokenization_comparison_70_99.png')

# Plot token count over 1-100 range for Standard French
plt.figure(figsize=(15, 7))
range_1_100 = df[df['number'] <= 100]
for name in tokenizers.keys():
    plt.plot(range_1_100['number'], range_1_100[f'tokens_std_{name}'], label=name)

plt.axvspan(70, 99, color='red', alpha=0.1, label='Vigesimal Range')
plt.title('Token Count for Standard French Numerals (1-100)')
plt.xlabel('Number')
plt.ylabel('Token Count')
plt.legend()
plt.savefig('figures/token_count_std_1_100.png')

print("Tokenization analysis complete. Figures saved to figures/.")
