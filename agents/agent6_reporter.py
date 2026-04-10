from pathlib import Path


def generate_report(avg_cost: float, market_rate: float, report_path: str = 'output/report.txt') -> str:
    """Generate a report comparing average shipping cost with the market rate."""
    Path(report_path).parent.mkdir(parents=True, exist_ok=True)
    variance = market_rate - avg_cost
    status = 'below' if avg_cost < market_rate else 'above or equal to'
    lines = [
        'Logistics Pricing Report',
        '========================',
        f'Average shipping cost: {avg_cost:.2f}',
        f'Market fallback rate: {market_rate:.2f}',
        f'Average cost is {status} the market rate by {abs(variance):.2f}.',
    ]

    if avg_cost == 0.0:
        lines.append('No invoice cost data was available to compute an average.')

    content = '\n'.join(lines) + '\n'
    with open(report_path, 'w', encoding='utf-8') as report_file:
        report_file.write(content)
    return content
