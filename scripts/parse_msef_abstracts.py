from pathlib import Path
import re
import pandas as pd
import fitz

PDF_NAME = "2026HS-Abstract-final.pdf"
REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
PATTERN = re.compile(r"^[A-Z]{2,3}R?-\d{2,3}-[A-Z]{2,4}$")

def parse_pdf(pdf_path: Path) -> pd.DataFrame:
    doc = fitz.open(pdf_path)
    rows = []
    for i, page in enumerate(doc):
        lines = [ln.strip() for ln in page.get_text("text").splitlines() if ln.strip()]
        if lines and PATTERN.match(lines[0]) and len(lines) >= 4:
            rows.append({
                "page": i + 1,
                "project_code": lines[0],
                "domain": " ".join(lines[1].split()),
                "school": " ".join(lines[2].split()),
                "title": " ".join(lines[3].split()),
            })
    return pd.DataFrame(rows)

def main() -> None:
    pdf_path = REPO_ROOT / PDF_NAME
    if not pdf_path.exists():
        raise FileNotFoundError(f"Missing PDF: {pdf_path}")
    abstract_df = parse_pdf(pdf_path).sort_values(["school", "domain", "project_code"]).reset_index(drop=True)
    counts_df = (abstract_df.groupby(["school", "domain"], as_index=False).size()
                 .rename(columns={"size": "count"})
                 .sort_values(["school", "domain"]).reset_index(drop=True))
    school_totals_df = (counts_df.groupby("school", as_index=False)["count"].sum()
                        .rename(columns={"count": "total_abstracts"})
                        .sort_values("school").reset_index(drop=True))
    abstract_df.to_csv(DATA_DIR / "abstract_index.csv", index=False)
    counts_df.to_csv(DATA_DIR / "school_domain_counts.csv", index=False)
    school_totals_df.to_csv(DATA_DIR / "school_totals.csv", index=False)
    md_lines = ["# School Domain Counts", "", "| School | Domain | Count |", "|---|---|---:|"]
    for _, r in counts_df.iterrows():
        md_lines.append(f"| {r['school']} | {r['domain']} | {int(r['count'])} |")
    (DATA_DIR / "school_domain_counts.md").write_text("\n".join(md_lines), encoding="utf-8")

if __name__ == "__main__":
    main()
