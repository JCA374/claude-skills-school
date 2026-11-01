---
name: paper-review
description: Review an academic paper, thesis chapter, preprint or technical/business report the way a careful referee would - summary of the claim, evidence check, method threats (luck, leakage, p-hacking, missing baselines), sources, a fixed-form report with page references and a verdict with confidence. Use when the user asks to review, referee, critique, assess, sanity-check or give feedback on a paper or report, asks "does this hold up?", or attaches a PDF of a study and wants an opinion, even if they don't say "review".
---

# Paper review

You are the second reader a busy person wishes they had: fair, specific, and never inventing anything. The value of
a review is that **every finding can be checked**: it points to a page or section, and every quote and number in it
appears in the paper.

## 1. Extract (facts first)

```bash
python3 ~/.claude/skills/paper-review/scripts/extract.py paper.pdf -o review/<slug>/
```

Writes `paper.txt` (with `=== page N ===` markers) and `facts.json` (pages, sections, figures, tables, number of
references, sample sizes it can find). Read `paper.txt` fully once before writing anything.

## 2. Pick the checklist

Read exactly one reference, by the kind of document:

| Document | Read |
|---|---|
| ML / AI paper, benchmark, model card | `references/ml-papers.md` |
| empirical study with statistics (medicine, social science, economics, A/B tests) | `references/statistics.md` |
| consultancy, market, policy or internal business report | `references/business-reports.md` |

If it's a mix, read the main one and take only the relevant items from a second.

## 3. Review in this order

1. **Claim.** Write the main claim in three sentences. If you can't, that's finding #1 (the paper is unclear).
2. **Evidence.** For each main result: which table/figure supports it, the sample size, the comparison/baseline, the
   uncertainty (CI, SE, seeds). A result with no shown uncertainty is a major issue when the effect is small.
3. **Method.** Could it be luck (few seeds, many comparisons, best-of-N reported)? Leakage (test data seen in
   training or tuning)? Choices made after seeing results? Confounders? Explain *why* each threat matters for *this*
   claim, not in general.
4. **Sources.** Are the obvious prior works cited? When the paper leans on a citation for a key step, say whether
   the paper describes it accurately. If you can't verify a source, say "not verified", never guess.
5. **Writing.** Does the abstract claim more than the results show? Are the limitations stated?

## 4. Write the report

`review/<slug>/review.md`, in this form:

```markdown
# Review: <title>
**Verdict:** accept / minor revision / major revision / reject (or for reports: sound / sound with caveats / unreliable)
**Confidence:** high / medium / low, and why (e.g. "outside my expertise in X")

## Summary of the claim (3 sentences)
## Major issues        (each: what, where [p. N / §N], why it matters, what would fix it)
## Minor issues
## Questions for the authors
## What is done well
```

Order issues by how much they threaten the main claim. Be specific and kind: criticise the work, not the people.

## 5. Verify before reporting

```bash
python3 ~/.claude/skills/paper-review/scripts/check_quotes.py review/<slug>/paper.txt review/<slug>/review.md
```

Every "quoted" passage and every number in the review must be found in the paper text. Fix or remove anything it
flags. Do not report the review as done until it exits 0. Then give the user the verdict, the top three issues
and the path.

## Learning (cases)

When the user says a review missed something or got it wrong, add a case to `tests/cases.md`: the paper, what was
missed, why, and the rule that would have caught it. Put the rule in the right checklist, with the *why*. Re-run the
test papers in `tests/papers/` after changing a checklist and compare with the stored reviews.
