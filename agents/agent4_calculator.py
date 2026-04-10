import sqlite3


def calculate_average_shipping_cost(db_path: str = 'output/invoices.db') -> float:
    """Compute the average shipping cost from the invoice database."""
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT AVG(cost) FROM invoices WHERE cost > 0')
            result = cursor.fetchone()
            if result is None or result[0] is None:
                return 0.0
            return float(result[0])
    except sqlite3.Error:
        return 0.0
