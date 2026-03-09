import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style
sns.set_theme(style="whitegrid")
os.makedirs('figures', exist_ok=True)

# Load data
df_decoding = pd.read_csv('results/decoding_results_final.csv')
df_magnitude = pd.read_csv('results/magnitude_comparison_results.csv')
df_math = pd.read_csv('results/mathification_results.csv')
df_tokens = pd.read_csv('results/tokenization_analysis.csv')

# --- 1. Decoding Analysis ---
decoding_summary = df_decoding.groupby(['model', 'system', 'is_vigesimal'])['is_correct'].mean().reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(data=decoding_summary[decoding_summary['is_vigesimal'] == True], x='model', y='is_correct', hue='system')
plt.title('Accuracy on Vigesimal Numbers (70-99) - Standard vs Swiss')
plt.ylabel('Accuracy')
plt.ylim(0, 1.1)
plt.savefig('figures/decoding_accuracy_vigesimal.png')

# --- 2. Magnitude Comparison Analysis ---
mag_melted = df_magnitude.melt(id_vars=['model'], value_vars=['correct_std', 'correct_swiss', 'correct_mixed'], 
                               var_name='test_type', value_name='is_correct')
mag_summary = mag_melted.groupby(['model', 'test_type'])['is_correct'].mean().reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(data=mag_summary, x='model', y='is_correct', hue='test_type')
plt.title('Magnitude Comparison Accuracy (70-99)')
plt.ylabel('Accuracy')
plt.ylim(0, 1.1)
plt.savefig('figures/magnitude_accuracy.png')

# --- 3. Mathification Analysis ---
math_summary = df_math.groupby(['model'])[['correct_base', 'correct_math']].mean().reset_index()
math_melted = math_summary.melt(id_vars='model', value_vars=['correct_base', 'correct_math'],
                                var_name='prompt_type', value_name='accuracy')

plt.figure(figsize=(10, 6))
sns.barplot(data=math_melted, x='model', y='accuracy', hue='prompt_type')
plt.title('Effect of Mathification on Standard French Decoding')
plt.ylabel('Accuracy')
plt.ylim(0, 1.1)
plt.savefig('figures/mathification_effect.png')

# --- 4. Correlation: Tokenization vs Accuracy ---
# Join decoding results with token counts
# We'll use GPT-4o tokenizer for GPT-4o, and Llama-3 for Llama-3.1
tok_map = {
    'gpt-4o': 'gpt-4o (o200k_base)',
    'claude-3.5-sonnet': 'gpt-4/3.5 (cl100k_base)',
    'llama-3.1-70b': 'llama-3'
}

df_decoding['token_count'] = df_decoding.apply(
    lambda row: df_tokens.loc[df_tokens['number'] == row['number'], 
                             f"tokens_{'std' if row['system'] == 'standard' else 'swiss'}_{tok_map[row['model']]}"].values[0],
    axis=1
)

# Calculate error rate per token count
corr_df = df_decoding.groupby(['token_count'])['is_correct'].mean().reset_index()
corr_df['error_rate'] = 1 - corr_df['is_correct']

plt.figure(figsize=(10, 6))
sns.regplot(data=corr_df, x='token_count', y='error_rate')
plt.title('Correlation: Token Count vs Error Rate')
plt.xlabel('Number of Tokens')
plt.ylabel('Error Rate')
plt.savefig('figures/token_vs_error_correlation.png')

# Print Summary Table
print("--- SUMMARY STATISTICS ---")
print("\nDecoding Accuracy (Vigesimal Range 70-99):")
print(decoding_summary[decoding_summary['is_vigesimal'] == True])

print("\nMagnitude Comparison Accuracy:")
print(mag_summary)

print("\nMathification Effect:")
print(math_summary)

print("\nAnalysis complete. Figures saved to figures/.")
