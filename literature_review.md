# Literature Review: How does the model count in French?

## Research Area Overview
The representation of numbers in Large Language Models (LLMs) is a growing field of study, particularly focusing on how compositional numeral systems are processed. The French counting system is notably "opaque" or counterintuitive compared to "transparent" systems like Japanese, primarily due to its partial vigesimal (base-20) structure for numbers 70-99. This research area investigates whether LLMs internally map these linguistic forms to their numeric values and how the complexity of the numeral system affects this mapping.

## Key Papers

### Paper 1: Probing for Multilingual Numerical Understanding in Transformer-Based Language Models
- **Authors**: Devin Johnson, Denise Mak, Andrew Barker, Lexi Loessberg-Zahl
- **Year**: 2020
- **Source**: BlackboxNLP workshop at EMNLP 2020
- **Key Contribution**: Introduces probing tasks (Grammaticality Judgment and Value Comparison) for numerical understanding in English, Japanese, Danish, and French.
- **Methodology**: Used a Multilayer Perceptron (MLP) classifier on top of frozen pretrained embeddings (BERT, DistilBERT, XLM).
- **Results**: Models are good at judging if a number word string is grammatical but poor at comparing values (magnitude).
- **Relevance to Our Research**: Specifically identifies French as "the worst" in terms of transparency due to its vigesimal system. It provides a baseline for how older models (BERT-era) handled French numbers.

### Paper 2: Investigating the interaction of linguistic and mathematical reasoning in language models using multilingual number puzzles
- **Authors**: Antara Raaghavi Bhattacharya, Isabel Papadimitriou, Kathryn Davidson, David Alvarez-Melis
- **Year**: 2025 (Recent ArXiv: 2506.13886)
- **Source**: ArXiv / Recent Conference (NeurIPS 2024 context)
- **Key Contribution**: Analyzes how LLMs solve linguistics puzzles involving complex numeral systems.
- **Methodology**: "Mathifies" linguistics puzzles by making implicit operations (like the multiplication in vigesimal systems) explicit to see if it improves performance.
- **Results**: SOTA models (OpenAI o1, DeepSeek-R1) struggle with implicit structure but succeed when mathematical operations are made explicit.
- **Relevance to Our Research**: Directly addresses the "implicit mathematical structure" of numeral systems like French. It suggests that LLMs fail to automatically "see" the math behind words like `quatre-vingts` (4 * 20) without explicit cues.

## Common Methodologies
- **Probing**: Using linear or MLP classifiers on frozen embeddings to detect specific information (like magnitude).
- **Zero-shot/Few-shot Prompting**: Testing SOTA models' ability to solve number puzzles or translate between number names and digits.
- **Mathification**: Converting linguistic number representations into explicit mathematical expressions to isolate the source of failure (linguistic vs. mathematical).

## Standard Baselines
- **Random/Majority Class**: For classification tasks.
- **English performance**: Often used as a high-resource baseline.
- **Japanese/Chinese performance**: Used as "transparent" or "regular" number system baselines.

## Evaluation Metrics
- **Accuracy**: For grammaticality and value comparison.
- **Mean Absolute Error (MAE)**: For number estimation/decoding.
- **Token Overlap**: Analyzing how tokenization (subwords) affects number representation.

## Datasets in the Literature
- **UKLO/IOL**: Linguistics Olympiad puzzles.
- **num2words**: Python library used to generate spelled-out numbers.
- **MGSM**: Multilingual Grade School Math.

## Gaps and Opportunities
- **Cross-Dialect Analysis**: Comparing Standard French (vigesimal) with Swiss/Belgian French (decimal) is a powerful way to isolate the effect of the vigesimal structure while keeping the core language (French) constant.
- **Internal Mapping**: Probing the *residual stream* or *attention heads* for specific "vigesimal" vs "decimal" circuits.

## Recommendations for Our Experiment
- **Primary Dataset**: A comparative dataset of Standard French vs. Swiss French number names (1-100).
- **Baseline**: Comparison with English (decimal) and Japanese (regular decimal).
- **Approach**: Test if models (e.g., GPT-4o, Claude 3.5, Llama 3) have higher error rates or different tokenization patterns for 70-99 in Standard French compared to Swiss French.
- **Hypothesis**: The vigesimal structure in Standard French induces specific failure modes in magnitude estimation that are absent in Swiss French for the same numeric values.
