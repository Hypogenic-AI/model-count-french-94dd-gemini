import pandas as pd

df_mag = pd.read_csv('results/magnitude_comparison_results.csv')

def analyze_bias(row):
    # n1 is standard, n2 is swiss
    if row['correct_mixed']:
        return "Correct"
    if row['n1'] > row['n2']:
        return "Standard_underestimated" # Said Second (Swiss) is larger
    if row['n1'] < row['n2']:
        return "Standard_overestimated" # Said First (Standard) is larger
    return "Unknown"

df_mag['bias'] = df_mag.apply(analyze_bias, axis=1)

print("\nBias analysis for mixed comparison (n1=std, n2=swiss):")
for model in df_mag['model'].unique():
    print(f"\nModel: {model}")
    print(df_mag[df_mag['model'] == model]['bias'].value_counts())
