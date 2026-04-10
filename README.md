# CWT Logistics Agent Project

This repository contains a simple multi-agent logistics pipeline written in Python.

## Agents

1. `agents/agent1_loader.py` - load PDF files from the `data/` folder
2. `agents/agent2_extractor.py` - extract invoice number, date, cost, origin, and destination from PDF content using `pdfplumber`
3. `agents/agent3_deduper.py` - save invoice data into SQLite and skip duplicates
4. `agents/agent4_calculator.py` - calculate the average shipping cost from the database
5. `agents/agent5_price_fetcher.py` - return a fallback market rate of `2800.0`
6. `agents/agent6_reporter.py` - generate a comparison report and save it to `output/report.txt`
7. `agents/agent7_improver.py` - find records with `UNKNOWN` values and log improvement recommendations to `output/improvement_log.txt`

## Usage

1. Install dependencies:
```bash
pip install -r requirements.txt
```
2. Place invoice PDFs into the `data/` folder.
3. Run the pipeline:
```bash
python main.py
```
