# Marketing Report Automation

Python script that reads raw marketing data from a CSV file and generates an HTML performance report.

## What it does
- Aggregates marketing data by channel
- Calculates CTR and ROAS per channel
- Produces a self-contained HTML report with a bar chart and summary table

## Tech stack
- Python 3
- Pandas
- Matplotlib
- Jinja2

## How to run

```bash
pip3 install pandas matplotlib jinja2
python3 report.py
```

Open `report.html` in your browser to view the report.

## Sample insight
In the sample dataset, Email delivers a 19.29x ROAS compared to 4.29x for Google and 4.17x for Meta, at a fraction of the spend.