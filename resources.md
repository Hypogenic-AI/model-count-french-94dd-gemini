# Resources Catalog: How does the model count in French?

## Summary
This catalog summarizes all resources gathered for the research project, including scientific papers, a custom-generated dataset, and code repositories from relevant studies.

## Papers
Total papers downloaded: 5

| Title | Authors | Year | File | Key Info |
|-------|---------|------|------|----------|
| Probing for Multilingual Numerical Understanding | Johnson et al. | 2020 | papers/2020.blackboxnlp-1.18_Johnson_Probing_Multilingual_Numerical.pdf | Found French is the "worst" due to vigesimal system. |
| Multilingual Number Puzzles | Bhattacharya et al. | 2025 | papers/2506.13886_Bhattacharya_2025_Multilingual_Number_Puzzles.pdf | Tested SOTA models (o1, R1) on linguistic puzzles. |
| mOthello: Cross-Lingual Alignment | Hua et al. | 2024 | papers/2404.12444_Hua_2024_mOthello_Cross_Lingual.pdf | Representation alignment in multilingual models. |
| QTC Dataset (Question Complexity) | Kokot & Poelman | 2025 | papers/2510.06304_QTC_Dataset.pdf | Multilingual signals in question representation. |
| DistilCamemBERT | Delestre & Amar | 2022 | papers/2205.11111_Delestre_2022_DistilCamemBERT.pdf | French-specific model distillation info. |

See `literature_review.md` for detailed analysis.

## Datasets
Total datasets downloaded/generated: 1

| Name | Source | Size | Task | Location | Notes |
|------|--------|------|------|----------|-------|
| French Numbers 1-1000 | Custom (num2words) | 1000 samples | Probing / Evaluation | datasets/french_numbers_1_1000.csv | Compares Standard, Swiss, and Belgian French. |

### Dataset Details: French Numbers 1-1000
- **Format**: CSV
- **Columns**: `number`, `fr_standard`, `fr_swiss`, `fr_belgian`, `is_vigesimal_std`, `structure_std`
- **Utility**: Allows comparative analysis of vigesimal (Standard: *soixante-dix*) vs. decimal (Swiss: *septante*) forms.

## Code Repositories
Total repositories cloned: 1

| Name | URL | Purpose | Location | Notes |
|------|-----|---------|----------|-------|
| Multilingual Number Puzzles | https://github.com/antara-raaghavi/multilingual-number-puzzles | Official impl of Bhattacharya 2025 | code/multilingual-number-puzzles | Includes "mathifying" logic. |

### Code Usage Note
The `mathify.py` script in `code/multilingual-number-puzzles/code/` contains logic for standardizing linguistics puzzles and could be adapted for a French-specific study.

## Recommendations for Experiment Design

1.  **Primary Experiment**: Use the `datasets/french_numbers_1_1000.csv` to evaluate how models (GPT-4, Claude 3, Llama 3) translate number words to digits.
2.  **Comparative Study**: Specifically compare performance on 70-79, 80-89, and 90-99 between Standard and Swiss French.
3.  **Probing Strategy**: Test if the *tokenization* of vigesimal forms (e.g., `quatre-vingt-onze`) is more fragmented than decimal forms (`nonante-et-un`) and if this correlates with error rates.
4.  **Mathification Test**: Test if prompting the model to *think* about the mathematical structure (e.g., "75 is 60+15 in French") helps in Standard French more than in Swiss French.
