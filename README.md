# How LLMs Represent the French Counting System

This project investigates the internal representation of the French vigesimal (base-20) counting system in Large Language Models (LLMs) compared to the more "transparent" decimal systems of Swiss and Belgian French.

## Key Findings
1.  **H2 (Tokenization Complexity) Confirmed**: Standard French numerals (70-99) are represented by **~2.3-2.8x more tokens** than their Swiss counterparts across all tested tokenizers.
2.  **H1 (The Vigesimal Tax) Refined**: Modern SOTA models (GPT-4o, Claude 3.5 Sonnet) have mastered *decoding* French numerals into digits with ~100% accuracy.
3.  **H3 (Magnitude Inconsistency) Confirmed**: Cross-system magnitude comparison (Standard vs. Swiss) reveals significant reasoning gaps, with Claude 3.5 Sonnet and Llama 3.1 accuracy dropping to **76%** when comparing systems.
4.  **Novel Bias Discovered**: Claude 3.5 Sonnet exhibits a consistent **"Standard Overestimation" bias**, incorrectly claiming that Standard French forms are larger than Swiss forms even when they represent lower numeric values.

## File Structure
- `REPORT.md`: Full research report with detailed findings.
- `src/`: Python scripts for experiments and analysis.
- `datasets/`: Custom dataset comparing French variants.
- `figures/`: Visualizations of results.
- `results/`: CSV files containing raw experiment data.

## How to Reproduce
1.  Install dependencies: `uv pip install -r pyproject.toml`
2.  Set API key: `export OPENROUTER_KEY=your_key`
3.  Run experiments:
    ```bash
    python src/analyze_tokenization.py
    python src/decoding_experiment.py
    python src/magnitude_comparison.py
    python src/mathification_experiment.py
    python src/analyze_results.py
    ```

For full details, see the [REPORT.md](REPORT.md).
