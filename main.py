from pathlib import Path

from agents.agent1_loader import load_pdfs
from agents.agent2_extractor import extract_invoice_data
from agents.agent3_deduper import save_records_to_database, initialize_database
from agents.agent4_calculator import calculate_average_shipping_cost
from agents.agent5_price_fetcher import get_market_rate
from agents.agent6_reporter import generate_report
from agents.agent7_improver import log_unknown_records


def main() -> None:
    output_dir = Path('output')
    output_dir.mkdir(parents=True, exist_ok=True)

    print('Loading PDF files from data/...')
    pdf_paths = load_pdfs('data')
    print(f'Found {len(pdf_paths)} PDF files.')

    invoice_records = extract_invoice_data(pdf_paths)
    print(f'Extracted {len(invoice_records)} invoice records.')

    initialize_database('output/invoices.db')
    inserted, skipped = save_records_to_database(invoice_records, 'output/invoices.db')
    print(f'Inserted {inserted} new records; skipped {skipped} duplicates.')

    avg_cost = calculate_average_shipping_cost('output/invoices.db')
    market_rate = get_market_rate()
    report = generate_report(avg_cost, market_rate, 'output/report.txt')
    print('Generated report at output/report.txt')

    unknown_records = log_unknown_records('output/invoices.db', 'output/improvement_log.txt')
    print(f'Logged {len(unknown_records)} records needing improvement to output/improvement_log.txt')
    print('\nSummary:')
    print(report)


if __name__ == '__main__':
    main()
