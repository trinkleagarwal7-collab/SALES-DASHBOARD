# 📊 Sales Dashboard (Streamlit + Plotly + TextBlob)

An interactive sales analytics dashboard built with **Streamlit**, **Plotly**, and
**TextBlob** (for sentiment analysis on customer reviews). Includes 1,500 rows of
realistic sample sales data.

## Project Structure

```
sales_dashboard/
├── app.py                  # Main Streamlit application
├── generate_data.py         # Script that generated the sample dataset (optional to re-run)
├── requirements.txt         # Python dependencies
├── data/
│   └── sales_data.csv       # Sample sales dataset (1,500 rows)
└── README.md                 # This file
```

## Features

- 📈 Sales trend over time, sales by region, category, and top products (Plotly charts)
- 🎛️ Sidebar filters: date range, region, category, review sentiment
- 💬 TextBlob sentiment analysis on customer reviews (polarity, subjectivity, label)
- 🧪 Live text box to test sentiment analysis on any custom text
- 📄 Filterable raw data table + CSV download button
- 🖥️ KPI summary cards (Total Sales, Orders, Units Sold, Avg Order Value, Avg Sentiment)

## Prerequisites

- **Python 3.9+** installed
- **VS Code** installed (with the Python extension recommended)

Check your Python version in a terminal:
```bash
python --version
```

## Step-by-Step Setup in VS Code

### 1. Unzip and open the project
Unzip the downloaded `sales_dashboard.zip` file, then open the folder in VS Code:
- `File → Open Folder...` → select the unzipped `sales_dashboard` folder

### 2. Open a terminal in VS Code
`Terminal → New Terminal` (or `` Ctrl+` ``)

### 3. Create a virtual environment (recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should now see `(venv)` at the start of your terminal prompt.

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Download TextBlob's language corpora (one-time)
TextBlob needs NLTK corpora for tokenization/POS-tagging:
```bash
python -m textblob.download_corpora
```

### 6. Run the app
```bash
streamlit run app.py
```

### 7. View it in your browser
Streamlit will automatically open your default browser. If it doesn't, open:
```
http://localhost:8501
```
manually in your browser. The terminal will also print this URL.

### 8. Stop the app
Go back to the VS Code terminal and press `Ctrl+C`.

## Using Your Own Data

Replace `data/sales_data.csv` with your own file, keeping these columns
(or adjust `app.py` to match your column names):

| Column           | Type   | Description                          |
|------------------|--------|---------------------------------------|
| Order_ID         | text   | Unique order identifier               |
| Date             | date   | Order date (YYYY-MM-DD)               |
| Region           | text   | Sales region                          |
| Category         | text   | Product category                      |
| Product          | text   | Product name                          |
| Quantity         | number | Units sold                            |
| Unit_Price       | number | Price per unit                        |
| Sales            | number | Total sale amount (Quantity × Price)  |
| Customer_Review  | text   | Customer review text (for sentiment)  |

## Regenerating Sample Data (optional)

If you want a fresh random sample dataset:
```bash
python generate_data.py
```

## Troubleshooting

- **`streamlit: command not found`** → Make sure your virtual environment is activated
  and dependencies installed (`pip install -r requirements.txt`).
- **Port 8501 already in use** → Run `streamlit run app.py --server.port 8502` and open
  `http://localhost:8502`.
- **TextBlob corpora errors** → Re-run `python -m textblob.download_corpora`.
- **Blank/empty dashboard** → Check that `data/sales_data.csv` exists in the `data/` folder.

## Tech Stack

- [Streamlit](https://streamlit.io/) — web app framework
- [Plotly Express](https://plotly.com/python/plotly-express/) — interactive charts
- [TextBlob](https://textblob.readthedocs.io/) — sentiment analysis (polarity & subjectivity)
- [Pandas](https://pandas.pydata.org/) — data manipulation
