# Downloaded Datasets

This directory contains datasets for the research project "How does the model count in French?".

## Dataset 1: French Numbers 1-1000

### Overview
- **Source**: Custom generated using `num2words` Python library.
- **Size**: 1000 samples (numbers 1 to 1000).
- **Format**: CSV
- **Task**: Probing / Magnitude Estimation / Linguistic-Numeric Mapping.

### Dataset Structure
| Column | Description |
|--------|-------------|
| `number` | The integer value (1-1000). |
| `fr_standard` | Standard French name (e.g., *soixante-dix*). |
| `fr_swiss` | Swiss French name (e.g., *septante*). |
| `fr_belgian` | Belgian French name (e.g., *septante*). |
| `is_vigesimal_std` | Boolean, True if the standard name is vigesimal (70-99). |
| `structure_std` | 'vigesimal' or 'decimal'. |

### Sample Data
```csv
number,fr_standard,fr_swiss,fr_belgian,is_vigesimal_std,structure_std
69,soixante-neuf,soixante-neuf,soixante-neuf,False,decimal
70,soixante-dix,septante,septante,True,vigesimal
80,quatre-vingts,huitante,quatre-vingt,True,vigesimal
90,quatre-vingt-dix,nonante,nonante,True,vigesimal
```

### Usage
Use this dataset to compare model performance on Standard French (vigesimal) versus Swiss/Belgian French (decimal) for the same numbers.
