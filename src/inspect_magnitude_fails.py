import pandas as pd

df_mag = pd.read_csv('results/magnitude_comparison_results.csv')

def analyze_bias(row):
    # n1 is standard, n2 is swiss
    # Correct should be n1 > n2 (if First) or n2 > n1 (if Second)
    # We don't have the raw responses here, but we have the 'correct_mixed' flag.
    pass

# Just print summary of mixed comparison
print(df_mag.groupby('model')['correct_mixed'].mean())

# Look at specific failures in mixed for Claude
claude_mixed_fails = df_mag[(df_mag['model'] == 'claude-3.5-sonnet') & (df_mag['correct_mixed'] == False)]
print("\nClaude Mixed Comparison Failures (n1=std, n2=swiss):")
print(claude_mixed_fails[['n1', 'n2']].head(10))
