# Planning: How does the model count in French?

## Motivation & Novelty Assessment

### Why This Research Matters
The French counting system is a classic example of linguistic "opacity" in numeral systems. While most modern Indo-European languages use a base-10 (decimal) system, Standard French retains vigesimal (base-20) elements for numbers 70-99 (e.g., *quatre-vingts* for 80, literally "four twenties"). This research matters because it probes the boundary between linguistic representation and mathematical reasoning in LLMs. If a model "understands" a number, is that understanding tied to the linguistic surface form or an abstract numeric value? The French system provides a unique stress test for this mapping.

### Gap in Existing Work
Existing work (Johnson et al., 2020) has shown that older models struggle with French numeral magnitude comparison. Recent work (Bhattacharya et al., 2025) has explored "mathifying" linguistic puzzles but hasn't deeply analyzed the *internal* representational difference between the vigesimal Standard French and the decimal Swiss/Belgian variants (e.g., *septante*, *huitante/octante*, *nonante*). Most studies treat "French" as a monolithic entity, ignoring these natural "controlled experiments" provided by regional variations.

### Our Novel Contribution
We will perform a systematic comparative analysis between **Standard French** (vigesimal) and **Swiss French** (decimal) numeral systems across multiple state-of-the-art LLMs. By using the same underlying language (French) but varying the numeral structure, we can isolate the "vigesimal tax" — the performance or representational cost associated with the more complex base-20 structure. We will also investigate **tokenization patterns** to see if the increased complexity of Standard French numerals (e.g., *quatre-vingt-dix-sept* vs. *nonante-sept*) leads to higher fragmentation and subsequent errors.

### Experiment Justification
- **Experiment 1: Number-to-Digit Translation (Decoding)**: Measures how accurately the model maps linguistic forms to numeric values. This is the most direct test of the "vigesimal tax".
- **Experiment 2: Magnitude Comparison**: Tests if the internal representation of a number (e.g., 75 vs. 85) is consistent regardless of the linguistic form (*soixante-quinze* vs. *quatre-vingt-cinq*).
- **Experiment 3: Tokenization Analysis**: Investigates if the surface-level complexity (number of tokens) correlates with error rates, providing a mechanistic explanation for performance gaps.
- **Experiment 4: "Mathification" Intervention**: Tests if prompting the model to explicitly decompose vigesimal forms (e.g., "80 is 4 times 20") improves performance, as suggested by Bhattacharya et al. (2025).

## Research Question
How does the vigesimal structure of the Standard French counting system affect the accuracy and internal representation of numbers in LLMs compared to the more "transparent" decimal systems of Swiss and Belgian French?

## Hypothesis Decomposition
1.  **H1 (The Vigesimal Tax)**: LLMs will show significantly higher error rates in number-to-digit translation for Standard French numerals in the 70-99 range compared to Swiss French equivalents.
2.  **H2 (Tokenization Complexity)**: Standard French numerals in the 70-99 range will be represented by more tokens than their Swiss/Belgian counterparts, and token count will positively correlate with error rate.
3.  **H3 (Magnitude Inconsistency)**: Magnitude comparison will be less accurate for Standard French vigesimal forms than for decimal forms, even when controlling for numeric value.
4.  **H4 (Mathification Benefit)**: Explicit mathematical decomposition will bridge the performance gap between Standard and Swiss French more effectively than simple few-shot prompting.

## Proposed Methodology

### Approach
A comparative behavioral and tokenization analysis of SOTA LLMs (GPT-4o, Claude 3.5 Sonnet, Llama 3.1) using a custom dataset of Standard, Swiss, and Belgian French numerals (1-1000).

### Experimental Steps
1.  **Data Preparation**: Load and validate `datasets/french_numbers_1_1000.csv`.
2.  **Tokenization Study**: Use the `transformers` library to count tokens for all numeral variants across different model tokenizers (GPT-4, Llama 3).
3.  **Decoding Task**: Zero-shot and few-shot translation of French numeral words to Arabic digits. Focus on the 70-99 range.
4.  **Comparison Task**: Prompt models to compare two numerals (e.g., "Which is larger: soixante-quinze or septante-deux?") and analyze the success rate.
5.  **Mathification Intervention**: Compare standard prompting with "mathified" prompting (explaining the vigesimal structure) for the 70-99 range.

### Baselines
- **English**: High-resource decimal baseline.
- **Swiss French**: The primary "controlled" decimal baseline within the same language.
- **Random Choice**: For comparison tasks.

### Evaluation Metrics
- **Accuracy**: For translation and comparison.
- **Mean Absolute Error (MAE)**: For number-to-digit translation.
- **Token Count**: Mean tokens per numeral range.
- **Correlation (Pearson/Spearman)**: Between token count and error rate.

### Statistical Analysis Plan
- **T-tests/ANOVA**: To compare error rates between Standard and Swiss French.
- **Regression**: To model error rate as a function of tokenization complexity and numeral system.

## Timeline and Milestones
- **M1 (Setup)**: Environment and data verification (1 hour).
- **M2 (Implementation)**: Scripts for API calls and tokenization analysis (2 hours).
- **M3 (Execution)**: Running all experiments (3 hours).
- **M4 (Analysis)**: Statistical testing and visualization (1.5 hours).
- **M5 (Documentation)**: Final report (1 hour).

## Potential Challenges
- **API Rate Limits**: Mitigate with caching and retries.
- **Model Biases**: Models might be primarily trained on Standard French, potentially *over-performing* on it despite the complexity. This makes the comparison even more interesting.
- **Tokenization Variability**: Different models use different tokenizers; we must analyze each model's specific tokenizer.

## Success Criteria
- Quantified "vigesimal tax" for Standard French across at least three SOTA models.
- Statistical evidence (or lack thereof) linking tokenization complexity to error rates.
- Validated "mathification" effect for the 70-99 range.
