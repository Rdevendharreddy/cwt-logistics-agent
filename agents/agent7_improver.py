import sqlite3
from pathlib import Path
from typing import List, Tuple


def log_unknown_records(db_path: str = 'output/invoices.db', log_path: str = 'output/improvement_log.txt') -> List[Tuple]:
    """Inspect the database for UNKNOWN values and write improvement recommendations."""
    Path(log_path).parent.mkdir(parents=True, exist_ok=True)
    suggestions = []

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''SELECT id, invoice_number, invoice_date, cost, origin, destination, source_file
                   FROM invoices
                   WHERE invoice_number = 'UNKNOWN'
                      OR invoice_date = 'UNKNOWN'
                      OR origin = 'UNKNOWN'
                      OR destination = 'UNKNOWN'
                      OR cost = 0'''
            )
            records = cursor.fetchall()
    except sqlite3.Error:
        records = []

    with open(log_path, 'w', encoding='utf-8') as log_file:
        if not records:
            log_file.write('No records with UNKNOWN or missing values were found.\n')
            return []

        log_file.write('Improvement Log for Unknown Invoice Fields\n')
        log_file.write('========================================\n')
        for row in records:
            record_id, invoice_number, invoice_date, cost, origin, destination, source_file = row
            issues = []
            if invoice_number == 'UNKNOWN':
                issues.append('missing invoice number')
            if invoice_date == 'UNKNOWN':
                issues.append('missing invoice date')
            if origin == 'UNKNOWN':
                issues.append('missing origin')
            if destination == 'UNKNOWN':
                issues.append('missing destination')
            if cost == 0:
                issues.append('missing or zero cost')

            issue_text = '; '.join(issues) if issues else 'unknown issue'
            line = (f'Invoice id={record_id} from {source_file}: {issue_text}. '
                    f'Recommended action: review PDF content and update metadata manually.\n')
            log_file.write(line)
            suggestions.append(row)

    return suggestions
