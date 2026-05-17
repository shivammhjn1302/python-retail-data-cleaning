import pandas as pd
from pathlib import Path

RAW = Path('data/raw/retail_orders_dirty.csv')
OUT = Path('data/cleaned/retail_orders_cleaned.csv')
REPORT = Path('reports/cleaning_summary.md')


def clean_orders() -> pd.DataFrame:
    df = pd.read_csv(RAW)
    starting_rows = len(df)

    df.columns = df.columns.str.strip().str.lower()
    df = df.drop_duplicates()
    duplicate_rows_removed = starting_rows - len(df)

    df['order_id'] = pd.to_numeric(df['order_id'], errors='coerce')
    df = df.dropna(subset=['order_id'])
    df['order_id'] = df['order_id'].astype(int)

    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    df = df.dropna(subset=['order_date'])

    text_columns = ['customer_email', 'product', 'category', 'sales_channel', 'city']
    for col in text_columns:
        df[col] = df[col].fillna('Unknown').astype(str).str.strip()

    df['customer_email'] = df['customer_email'].str.lower().replace('', 'unknown@email.com')
    df['product'] = df['product'].replace('', 'Unknown Product').str.title()
    df['category'] = df['category'].replace('', 'Unknown').str.title()
    df['sales_channel'] = df['sales_channel'].replace('', 'Unknown').str.title()
    df['city'] = df['city'].replace('', 'Unknown').str.title()

    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(1)
    df['quantity'] = df['quantity'].clip(lower=1)
    df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')
    df['unit_price'] = df['unit_price'].fillna(df['unit_price'].median())
    df['revenue'] = df['quantity'] * df['unit_price']

    df = df.sort_values(['order_date', 'order_id']).reset_index(drop=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)

    summary = f"""# Cleaning Summary\n\n- Starting rows: {starting_rows}\n- Duplicate rows removed: {duplicate_rows_removed}\n- Final cleaned rows: {len(df)}\n- Missing dates/order IDs removed during validation.\n- Text fields standardized with title/lower case formatting.\n- Revenue column created as `quantity * unit_price`.\n\n## Final Columns\n{', '.join(df.columns)}\n"""
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(summary)
    return df


if __name__ == '__main__':
    cleaned = clean_orders()
    print(cleaned.head())
    print(f'Cleaned file written to {OUT}')
