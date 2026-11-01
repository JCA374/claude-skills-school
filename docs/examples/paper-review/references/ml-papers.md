# Checklist: ML / AI papers

Read the paper first; use this to find what you missed. Each item says why it matters.

## Evidence
- **Seeds and variance.** How many runs per number? Mean ± what? RL and small-data results swing a lot between
  seeds; a gain smaller than the seed spread is not a gain.
- **Best-of-N.** Is the reported model the best of many runs or checkpoints, picked on the same data it's scored
  on? Selection inflates the score (winner's curse). Ask for a fresh evaluation set.
- **Baselines.** Are baselines tuned with the same budget as the new method? An untuned baseline makes any method
  look good.
- **Ablations.** Does each new component get removed once to show it matters?

## Leakage
- Test data used for early stopping, hyper-parameter search or prompt tuning.
- Benchmark contamination: could the test set be in the pre-training data (web-scraped benchmarks)?
- Near-duplicates between train and test (same patient, same game seed, same document in two splits).

## Claims
- "State of the art" on which benchmark, as of when, and against which numbers (copied or re-run)?
- Compute: are the compared methods given similar compute? Is it reported?
- Generalisation claims from one dataset or one environment.

## Reproducibility
- Code, data, hyper-parameters, number of GPUs/hours. Missing details are a minor issue unless the claim depends
  on them.
