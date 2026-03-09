from num2words import num2words
import pandas as pd
import os

os.makedirs('datasets', exist_ok=True)

data = []
for i in range(1, 1001):
    # Standard French
    fr_std = num2words(i, lang='fr')
    # Swiss French (septante, huitante, nonante)
    # num2words supports 'fr_CH' or similar?
    try:
        fr_ch = num2words(i, lang='fr_CH')
    except:
        fr_ch = fr_std # Fallback

    # Belgian French (septante, nonante, but usually quatre-vingts)
    try:
        fr_be = num2words(i, lang='fr_BE')
    except:
        fr_be = fr_std

    data.append({
        'number': i,
        'fr_standard': fr_std,
        'fr_swiss': fr_ch,
        'fr_belgian': fr_be,
        'is_vigesimal_std': 70 <= i <= 99,
        'structure_std': 'vigesimal' if 70 <= i <= 99 else 'decimal'
    })

df = pd.DataFrame(data)
df.to_csv('datasets/french_numbers_1_1000.csv', index=False)
print('Dataset generated: datasets/french_numbers_1_1000.csv')

# Show some samples
print(df[df['number'].between(68, 72)])
print(df[df['number'].between(78, 82)])
print(df[df['number'].between(88, 92)])
