# 💸 Student Subscription Waste Detector

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://student-subscription-detector-6hjrqczujaftfvjsvuapmx.streamlit.app/)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

> **[🚀 Try the Live Demo](https://student-subscription-detector-6hjrqczujaftfvjsvuapmx.streamlit.app/)** — No installation required!

A privacy-first tool that helps students identify and optimize their subscription spending.

## Features

- **Smart Detection**: Automatically identifies 40+ common subscriptions from bank statement CSVs
- **Student Discount Alerts**: Flags subscriptions that offer student discounts you might not be using
- **Expiration Alerts**: Warns you when student discounts are about to expire based on your graduation date
- **Duplicate Detection**: Identifies overlapping services (e.g., multiple streaming platforms)
- **"What If" Calculator**: Shows what your subscription money could become if invested
- **Post-Graduation Cost Estimator**: Calculates how much more you'll pay after losing student pricing
- **Privacy First**: All processing happens locally - your data never leaves your device

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the App

```bash
streamlit run app.py
```

### 3. Open in Browser

Navigate to `http://localhost:8501`

## Usage

### Option 1: Upload Your Bank Statement
1. Export your bank statement as CSV from your bank's website
2. Upload the CSV file in the app
3. Select the column containing transaction descriptions
4. View your results!

### Option 2: Try Demo Mode
1. Click on the "Demo Mode" tab
2. Click "Run Demo Analysis"
3. See sample results with pre-loaded data

### Option 3: Use Sample Data
A sample bank statement (`sample_bank_statement.csv`) is included for testing.

## Supported Banks & Formats

The app works with most CSV exports that contain:
- A date column
- A description/memo column
- An amount column

Common column names are auto-detected:
- `description`, `Description`, `DESCRIPTION`
- `memo`, `Memo`
- `transaction`, `Transaction`
- `merchant`, `Merchant`

## CSV Format Requirements

### Required Columns

| Column | Purpose | Accepted Names |
|--------|---------|----------------|
| **Date** | Transaction date | `date`, `Date`, `DATE`, `transaction_date`, `Transaction Date` |
| **Description** | Merchant/transaction name | `description`, `Description`, `memo`, `Memo`, `transaction`, `Transaction`, `name`, `Name`, `merchant`, `Merchant` |
| **Amount** | Transaction amount | `amount`, `Amount`, `AMOUNT` |

### Example CSV Format

```csv
date,description,amount
2024-01-15,SPOTIFY PREMIUM,-10.99
2024-01-18,NETFLIX.COM,-15.49
2024-01-20,AMAZON PRIME*,-14.99
2024-02-01,CHEGG INC,-19.95
2024-02-05,ADOBE CREATIVE,-54.99
```

### Tips for Best Results

1. **Negative amounts**: Charges should be negative (e.g., `-10.99`) or the app will use absolute values
2. **Date format**: Most common formats work (YYYY-MM-DD, MM/DD/YYYY, etc.)
3. **Description text**: The app searches for keywords like "SPOTIFY", "NETFLIX", "HULU" - partial matches work
4. **Headers**: First row should contain column names

### Exporting from Your Bank

Most banks allow CSV export from their online banking:
- **Chase**: Statements → Download → CSV
- **Bank of America**: Activity → Download → Spreadsheet (CSV)
- **Wells Fargo**: Download Account Activity → CSV
- **Capital One**: Download Transactions → CSV
- **Discover**: Statements → Export → CSV

### Sample Data

A sample CSV file (`sample_bank_statement.csv`) is included for testing. You can use it to see how the app works before uploading your own data.

## Detected Subscriptions

The app recognizes 40+ common student subscriptions including:

| Category | Services |
|----------|----------|
| Streaming | Netflix, Hulu, Disney+, HBO Max, Amazon Prime, Apple TV+ |
| Music | Spotify, Apple Music, YouTube Music, Tidal, Pandora |
| Education | Chegg, Coursera, Skillshare, LinkedIn Learning |
| Software | Adobe Creative Cloud, Microsoft 365, Canva, GitHub |
| Fitness | Planet Fitness, Peloton, Headspace, Calm |
| Food Delivery | DoorDash, Uber Eats, Grubhub |
| Gaming | Xbox Game Pass, PlayStation Plus, Nintendo Online |
| Cloud Storage | Dropbox, iCloud, Google One |

## Investment Comparison

The "What If" calculator compares your spending against:
- **Bitcoin**: ~45% annual return (10-year historical average, source: Morgan Stanley)
- **Ethereum**: ~38% annual return (conservative estimate, source: PortfoliosLab)
- **S&P 500**: ~12% annual return (10-year average, source: Trade That Swing)
- **High-Yield Savings**: ~5% annual return (current top-tier APY, source: Bankrate)

*Note: Past performance doesn't guarantee future results. Cryptocurrency investments are highly volatile. These are simplified estimates for educational purposes only.*

## Project Structure

```
subscription_detector/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── sample_bank_statement.csv # Sample data for testing
└── README.md                 # This file
```

## Tech Stack

- **Frontend**: Streamlit
- **Data Processing**: Pandas
- **Visualization**: Plotly
- **Pattern Matching**: Python regex

## Privacy

🔒 **Your data stays with you.**

- No data is uploaded to any server
- All processing happens in your browser/local machine
- No accounts or sign-ups required

## Future Enhancements

- [ ] PayPal/Apple/Google transaction support (detect hidden subscriptions)
- [ ] Manual entry for subscriptions we can't detect
- [ ] Roommate CSV merge feature
- [ ] Native iOS/Android mobile app
- [ ] Push notifications for expiring discounts
- [ ] One-click cancel links
- [ ] Export results as PDF report
- [ ] University partnership integrations

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Priority areas:**
- Adding more subscription services
- Supporting additional file formats (OFX, QFX)
- UI/UX improvements
- Writing tests

## Team

Built for Weekend Hackathon 2025 | Data Science & Analytics

- **Lilian Mara Onyambu** - Data Engineer
- **Ujwal Dasari** - Data Engineer  
- **Christian Rodas** - Financial Data Analyst
- **Namra Joshi** - Data Analyst

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Stop the leak. Start the growth.** 💰

⭐ Star this repo if you found it helpful!
