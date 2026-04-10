import re
from typing import Dict, List

import pdfplumber


def _normalize_string(value: str) -> str:
    return value.strip().replace('\r', '').replace('\n', ' ').strip()


def _safe_search(pattern: str, text: str) -> str:
    match = re.search(pattern, text, re.IGNORECASE)
    return _normalize_string(match.group(1)) if match else 'UNKNOWN'


def _parse_cost(raw_cost: str) -> float:
    if raw_cost == 'UNKNOWN':
        return 0.0
    normalized = raw_cost.replace('$', '').replace(',', '').strip()
    try:
        return float(normalized)
    except ValueError:
        return 0.0


def _normalize_date(raw_date: str) -> str:
    if raw_date == 'UNKNOWN':
        return 'UNKNOWN'
    raw_date = raw_date.strip()
    if re.match(r'^\d{2}/\d{2}/\d{4}$', raw_date):
        month, day, year = raw_date.split('/')
        return f'{year}-{month.zfill(2)}-{day.zfill(2)}'
    return raw_date


def extract_invoice_data(pdf_paths: List[str]) -> List[Dict[str, object]]:
    """Extract invoice metadata from PDF files."""
    records = []
    if not pdf_paths:
        return records

    invoice_pattern = r'(?:Invoice(?: Number| No\.?| No)?)[\s:\-]*([A-Z0-9-]+)'
    date_pattern = r'(?:Invoice Date|Date)[\s:\-]*([0-9]{4}-[0-9]{2}-[0-9]{2}|[0-9]{2}/[0-9]{2}/[0-9]{4})'
    cost_pattern = r'(?:Total Cost|Cost|Amount Due|Total)[\s:\-]*\$?\s*([0-9,]+(?:\.[0-9]{2})?)'
    origin_pattern = r'(?:Origin|From)[\s:\-]*([A-Za-z0-9 ,\-.#]+)'
    destination_pattern = r'(?:Destination|To)[\s:\-]*([A-Za-z0-9 ,\-.#]+)'

    for pdf_path in pdf_paths:
        with pdfplumber.open(pdf_path) as pdf:
            text = ' '.join(
                _normalize_string(page.extract_text() or '')
                for page in pdf.pages
            )

        invoice_number = _safe_search(invoice_pattern, text)
        invoice_date = _normalize_date(_safe_search(date_pattern, text))
        raw_cost = _safe_search(cost_pattern, text)
        cost = _parse_cost(raw_cost)
        origin = _safe_search(origin_pattern, text)
        destination = _safe_search(destination_pattern, text)

        records.append({
            'invoice_number': invoice_number,
            'invoice_date': invoice_date,
            'cost': cost,
            'origin': origin,
            'destination': destination,
            'source_file': pdf_path,
        })

    return records
