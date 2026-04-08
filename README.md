# MSEF 2026 School-by-Domain Abstract Counts

This repository contains a reproducible parser and cleaned outputs for the uploaded PDF `2026HS-Abstract-final.pdf`.

msef-school-domain-summary/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── abstract_index.csv
│   ├── school_domain_counts.csv
│   ├── school_domain_counts.md
│   └── school_totals.csv
├── scripts/
│   └── parse_msef_abstracts.py
└── wiki/
    ├── Home.md
    ├── Data-Dictionary.md
    ├── Methodology.md
    └── Usage.md
    

## Included files
- `data/abstract_index.csv`
- `data/school_domain_counts.csv`
- `data/school_totals.csv`
- `data/school_domain_counts.md`
- `scripts/parse_msef_abstracts.py`
- `wiki/` documentation pages

## Parsed summary
- Total parsed abstracts: **297**
- Unique schools: **114**

## Quick start
```bash
pip install -r requirements.txt
python scripts/parse_msef_abstracts.py
```
