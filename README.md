# Retail Orders Data Cleaning Lab

A Python data-cleaning project built around a messy retail orders dataset: missing values, duplicate rows, inconsistent dates, noisy text fields, and revenue validation.

The theme is **back-office retail operations** — the less glamorous but very real work that makes dashboards reliable.

## What this project shows

- Reading CSV files with Pandas
- Handling missing values and duplicate records
- Standardizing text columns
- Converting dates and numeric fields
- Creating and validating clean revenue metrics
- Exporting cleaned data and a cleaning summary

## Run locally

```bash
pip install -r requirements.txt
python scripts/clean_retail_orders.py
```

## Outputs

- `data/cleaned/retail_orders_cleaned.csv`
- `reports/cleaning_summary.md`

## Portfolio summary

Cleaned messy retail transaction data and prepared it for dashboarding by validating IDs, dates, revenue fields, and customer/product dimensions.
