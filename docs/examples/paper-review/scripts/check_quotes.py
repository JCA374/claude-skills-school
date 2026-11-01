#!/usr/bin/env python3
"""Second reader: every quoted passage and every number in the review must appear in the paper text.

    python3 check_quotes.py paper.txt review.md        exit 0 = all found, 1 = something to fix
Quotes: text inside "…" or “…” of 4+ words, compared ignoring case, whitespace and hyphenation at line ends.
Numbers: decimals, percentages and integers >= 10, except page/section references (p. 4, §3) and years.
"""
import re
import sys


def norm(s):
    s = re.sub(r'-\s*\n\s*', '', s)            # re-join hyphenated line breaks
    s = s.replace('“', '"').replace('”', '"').replace('’', "'")
    return re.sub(r'\s+', ' ', s).lower()


def main(paper_path, review_path):
    paper = norm(open(paper_path, errors='ignore').read())
    review = open(review_path).read()
    problems = []

    for q in re.findall(r'["“]([^"”]{10,400})["”]', review):
        if len(q.split()) >= 4 and norm(q).strip(' .,') not in paper:
            problems.append(('quote not found', q))

    scrubbed = re.sub(r'(?:pp?\.|page|§|section|sec\.|table|figure|fig\.)\s*\d+(?:[-–]\d+)?', ' ', review, flags=re.I)
    paper_nums = set(re.findall(r'\d+(?:[.,]\d+)?', paper))
    for n in re.findall(r'(?<![\w.])(\d+(?:[.,]\d+)?)(%?)', scrubbed):
        num = n[0]
        if re.fullmatch(r'(19|20)\d\d', num) or (num.isdigit() and int(num) < 10):
            continue
        if num not in paper_nums:
            problems.append(('number not found', num + n[1]))

    for kind, what in problems:
        print(f'{kind}: {what}')
    print(f'{len(problems)} problem(s)' if problems else 'all quotes and numbers found in the paper')
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main(*sys.argv[1:3]))
