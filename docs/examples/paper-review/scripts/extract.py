#!/usr/bin/env python3
"""Extract a paper's text with page markers, plus a few facts to start the review from.

    python3 extract.py paper.pdf -o review/<slug>/      -> paper.txt, facts.json
Uses pdftotext (poppler) if installed, else pypdf. A .txt or .md input is copied as one page.
"""
import argparse
import json
import os
import re
import shutil
import subprocess


def pages_of(path):
    if not path.lower().endswith('.pdf'):
        return [open(path, errors='ignore').read()]
    if shutil.which('pdftotext'):
        out = subprocess.run(['pdftotext', '-layout', path, '-'], capture_output=True, text=True).stdout
        return out.split('\f')
    from pypdf import PdfReader
    return [p.extract_text() or '' for p in PdfReader(path).pages]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src')
    ap.add_argument('-o', '--out', required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    pages = [p for p in pages_of(a.src)]
    while pages and not pages[-1].strip():
        pages.pop()
    text = ''.join(f'\n=== page {i} ===\n{p}' for i, p in enumerate(pages, 1))
    open(os.path.join(a.out, 'paper.txt'), 'w').write(text)

    body = '\n'.join(pages)
    ref_start = max(body.rfind('\nReferences'), body.rfind('\nREFERENCES'), body.rfind('\nBibliography'))
    refs = body[ref_start:] if ref_start > 0 else ''
    facts = {
        'pages': len(pages),
        'words': len(body.split()),
        'sections': re.findall(r'^\s*(\d+(?:\.\d+)?\.?\s+[A-Z][^\n]{2,60})$', body, re.M)[:40],
        'figures': len(set(re.findall(r'\b(?:Figure|Fig\.)\s*(\d+)', body))),
        'tables': len(set(re.findall(r'\bTable\s*(\d+)', body))),
        'references': len(re.findall(r'^\s*\[\d+\]', refs, re.M)) or len(re.findall(r'\(\d{4}[a-z]?\)\.?', refs)),
        'sample_sizes': sorted(set(re.findall(r'\b[nN]\s*=\s*([\d,]+)', body)))[:30],
        'p_values': len(re.findall(r'\bp\s*[<=>]\s*0?\.\d+', body)),
        'mentions': {k: len(re.findall(k, body, re.I)) for k in
                     ['confidence interval', 'standard deviation', 'seed', 'baseline', 'ablation', 'pre-regist',
                      'limitation', 'random']},
    }
    json.dump(facts, open(os.path.join(a.out, 'facts.json'), 'w'), indent=1)
    print(f"{facts['pages']} pages, {facts['words']} words, {facts['figures']} figures, {facts['tables']} tables, "
          f"{facts['references']} references -> {a.out}")


if __name__ == '__main__':
    main()
