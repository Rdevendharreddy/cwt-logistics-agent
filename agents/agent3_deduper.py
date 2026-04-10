import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple


def initialize_database(db_path: str = 'output/invoices.db') -> None:
    """Initialize the SQLite database and create invoice table if needed."""
    db_file = Path(db_path)
    db_file.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            '''CREATE TABLE IF NOT EXISTS invoices (
                id INTEGER PRIMARY KEY,
                invoice_number TEXT,
                invoice_date TEXT,
                cost REAL,
                origin TEXT,
                destination TEXT,
                source_file TEXT,
                created_at TEXT,
                UNIQUE(invoice_number, invoice_date, cost, origin, destination, source_file)
            )'''
        )
        conn.commit()


def _already_saved(cursor: sqlite3.Cursor, record: Dict[str, object]) -> bool:
    invoice_number = record['invoice_number']
    if invoice_number != 'UNKNOWN':
        cursor.execute(
            'SELECT 1 FROM invoices WHERE invoice_number = ? LIMIT 1',
            (invoice_number,),
        )
        return cursor.fetchone() is not None

    cursor.execute(
        'SELECT 1 FROM invoices WHERE invoice_number = ? AND invoice_date = ? AND cost = ? AND origin = ? AND destination = ? LIMIT 1',
        (
            record['invoice_number'],
            record['invoice_date'],
            record['cost'],
            record['origin'],
            record['destination'],
        ),
    )
    return cursor.fetchone() is not None


def save_records_to_database(records: List[Dict[str, object]], db_path: str = 'output/invoices.db') -> Tuple[int, int]:
    """Save extracted invoice records to SQLite and skip duplicates."""
    if not records:
        return 0, 0

    initialize_database(db_path)
    inserted = 0
    skipped = 0

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        for record in records:
            if _already_saved(cursor, record):
                skipped += 1
                continue

            cursor.execute(
                '''INSERT INTO invoices (invoice_number, invoice_date, cost, origin, destination, source_file, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?)''',
                (
                    record['invoice_number'],
                    record['invoice_date'],
                    record['cost'],
                    record['origin'],
                    record['destination'],
                    record['source_file'],
                    datetime.utcnow().isoformat(),
                ),
            )
            inserted += 1
        conn.commit()

    return inserted, skipped
